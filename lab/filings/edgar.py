"""SEC EDGAR client: company filing lists, documents, and point-in-time XBRL frames.

SEC's fair-access rules: identify yourself with a User-Agent of the form
"Your Name your@email.com" and stay under 10 requests per second. Set the
SEC_USER_AGENT environment variable (or a GitHub Actions secret) before running.
https://www.sec.gov/os/accessing-edgar-data

Everything downloaded is cached gzip-compressed under cache_dir, so a rerun
never hits the SEC twice for the same document.
"""
from __future__ import annotations

import gzip
import json
import logging
import os
from dataclasses import dataclass

from ..util import RateLimiter, http_json, http_text

log = logging.getLogger("lab.filings")

DATA_API = "https://data.sec.gov"
ARCHIVES = "https://www.sec.gov/Archives/edgar/data"
ANNUAL_FORMS = ("10-K", "10-K405")  # amendments (10-K/A) skipped on purpose


@dataclass(frozen=True)
class Filing:
    cik: int
    accession: str
    form: str
    filing_date: str
    report_date: str
    primary_doc: str

    @property
    def url(self) -> str:
        return f"{ARCHIVES}/{self.cik}/{self.accession.replace('-', '')}/{self.primary_doc}"


@dataclass
class Company:
    cik: int
    name: str
    tickers: list[str]
    former_names: list[str]
    sic: int
    filings: list[Filing]

    def annual_reports(self) -> list[Filing]:
        """10-K filings, oldest first."""
        return sorted((f for f in self.filings if f.form in ANNUAL_FORMS), key=lambda f: f.filing_date)


class Edgar:
    def __init__(self, cache_dir: str, user_agent: str | None = None, per_second: float = 8):
        ua = user_agent if user_agent is not None else os.environ.get("SEC_USER_AGENT", "")
        if "@" not in ua:
            raise ValueError(
                "SEC requires a contact in the User-Agent. Set SEC_USER_AGENT to "
                "'Your Name your@email.com' and run again."
            )
        self.headers = {"User-Agent": ua}
        self.limiter = RateLimiter(per_second * 60)
        self.cache_dir = cache_dir

    # ------------------------------------------------------------------ cache
    def _cache_get(self, rel: str) -> str | None:
        path = os.path.join(self.cache_dir, rel + ".gz")
        if not os.path.exists(path):
            return None
        with gzip.open(path, "rt", encoding="utf-8") as f:
            return f.read()

    def _cache_put(self, rel: str, text: str) -> None:
        path = os.path.join(self.cache_dir, rel + ".gz")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tmp = path + ".tmp"
        with gzip.open(tmp, "wt", encoding="utf-8") as f:
            f.write(text)
        os.replace(tmp, path)

    def _get_json(self, url: str, rel: str) -> dict:
        cached = self._cache_get(rel)
        if cached is not None:
            return json.loads(cached)
        data = http_json(url, headers=self.headers, limiter=self.limiter, timeout=30)
        self._cache_put(rel, json.dumps(data))
        return data

    # ------------------------------------------------------------------ API
    def public_float_frame(self, year: int) -> list[dict]:
        """Every filer's public float as of mid-`year`, as reported on its 10-K cover.

        Point-in-time and includes companies that later went bankrupt or were
        delisted, which is what keeps the universe free of survivorship bias.
        Each row: cik, entityName, val (USD), end (date measured), accn (the 10-K
        that reported it).
        """
        url = f"{DATA_API}/api/xbrl/frames/dei/EntityPublicFloat/USD/CY{year}Q2I.json"
        return self._get_json(url, f"frames/public_float_CY{year}Q2I.json")["data"]

    def company(self, cik: int) -> Company:
        cik10 = f"{int(cik):010d}"
        sub = self._get_json(f"{DATA_API}/submissions/CIK{cik10}.json", f"submissions/CIK{cik10}.json")
        tables = [sub["filings"]["recent"]]
        for extra in sub["filings"].get("files", []):
            name = extra["name"]
            tables.append(self._get_json(f"{DATA_API}/submissions/{name}", f"submissions/{name}"))
        filings: list[Filing] = []
        for t in tables:
            for i, form in enumerate(t["form"]):
                filings.append(Filing(
                    cik=int(cik), accession=t["accessionNumber"][i], form=form,
                    filing_date=t["filingDate"][i], report_date=t.get("reportDate", [""] * len(t["form"]))[i],
                    primary_doc=t["primaryDocument"][i],
                ))
        try:
            sic = int(sub.get("sic") or 0)
        except ValueError:
            sic = 0
        return Company(
            cik=int(cik), name=sub.get("name", ""), tickers=list(sub.get("tickers") or []),
            former_names=[x["name"] for x in sub.get("formerNames") or []], sic=sic, filings=filings,
        )

    def document(self, filing: Filing) -> str:
        rel = f"docs/{filing.cik}/{filing.accession}/{filing.primary_doc}"
        cached = self._cache_get(rel)
        if cached is not None:
            return cached
        text = http_text(filing.url, headers=self.headers, limiter=self.limiter, timeout=60)
        self._cache_put(rel, text)
        return text
