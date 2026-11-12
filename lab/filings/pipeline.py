"""Universe → consecutive 10-K pairs → section changes → anonymized payloads → scores."""
from __future__ import annotations

import json
import logging
import os
import random
from datetime import date

from ..util import append_csv, read_csv, save_json_atomic, utcnow, iso
from . import diff as D
from .anonymize import anonymize
from .config import FilingsConfig, period_of
from .edgar import Company, Edgar, Filing
from .score import FilingScorer, estimate_cost, probe_hit
from .sections import extract_sections, flags, to_text

log = logging.getLogger("lab.filings")

UNIVERSE_FIELDS = ["cik", "name", "public_float", "float_date", "accn"]
CHANGE_FIELDS = (
    ["cik", "name", "sic", "public_float", "period", "old_accession", "new_accession", "old_filing_date",
     "new_filing_date", "report_date", "sections_found", "missing_sections", "cosine_all", "jaccard_all",
     "changed_share", "added", "removed", "edited"]
    + [f"cosine_{s}" for s in ("1a", "3", "7", "9a")]
    + [f"{f}_{w}" for f in ("going_concern", "material_weakness", "not_effective", "restatement")
       for w in ("old", "new")]
    + ["payload_words", "truncated", "payload_file", "status"]
)
SCORE_FIELDS = ["cik", "new_accession", "new_filing_date", "period", "model", "score", "materiality", "tags",
                "reason", "input_tokens", "output_tokens", "scored_at"]
PROBE_FIELDS = ["cik", "new_accession", "period", "real_name", "company_guess", "company_confidence", "hit",
                "year_guess", "real_year", "year_error"]


def _p(cfg: FilingsConfig, *parts: str) -> str:
    return os.path.join(cfg.out_dir, *parts)


# ------------------------------------------------------------------ universe
def build_universe(edgar: Edgar, cfg: FilingsConfig, year: int) -> list[dict]:
    rows = []
    for r in edgar.public_float_frame(year):
        if cfg.min_public_float <= float(r["val"]) <= cfg.max_public_float:
            rows.append({"cik": r["cik"], "name": r["entityName"], "public_float": r["val"],
                         "float_date": r["end"], "accn": r["accn"]})
    rows.sort(key=lambda r: int(r["cik"]))
    path = _p(cfg, f"universe_CY{year}.csv")
    if os.path.exists(path):
        os.remove(path)
    append_csv(path, UNIVERSE_FIELDS, rows)
    log.info("universe CY%s: %d companies with public float $%.0fM-$%.0fM → %s", year, len(rows),
             cfg.min_public_float / 1e6, cfg.max_public_float / 1e6, path)
    return rows


# ------------------------------------------------------------------ pairs
def _days(a: str, b: str) -> int:
    return (date.fromisoformat(b) - date.fromisoformat(a)).days


def consecutive_pair(company: Company, new_accession: str) -> tuple[Filing, Filing] | None:
    """The 10-K with this accession number and the one filed roughly a year earlier."""
    annual = company.annual_reports()
    for i, f in enumerate(annual):
        if f.accession == new_accession and i > 0:
            prev = annual[i - 1]
            if 270 <= _days(prev.filing_date, f.filing_date) <= 460:
                return prev, f
    return None


def process_pair(edgar: Edgar, cfg: FilingsConfig, company: Company, old: Filing, new: Filing) -> tuple[dict, dict]:
    old_text, new_text = to_text(edgar.document(old)), to_text(edgar.document(new))
    old_sec = extract_sections(old_text, cfg.sections)
    new_sec = extract_sections(new_text, cfg.sections)
    both = [s for s in cfg.sections if s in old_sec and s in new_sec]
    missing = [s for s in cfg.sections if s not in both]

    changes = [D.compare(s, old_sec[s], new_sec[s], cfg.min_paragraph_words) for s in both]
    payload, truncated = D.build_payload(changes, cfg.max_payload_words)
    fy = int(new.report_date[:4]) if new.report_date else int(new.filing_date[:4]) - 1
    payload = anonymize(payload, [company.name] + company.former_names, company.tickers, fy)

    old_all = "\n".join(old_sec[s] for s in both)
    new_all = "\n".join(new_sec[s] for s in both)
    fo, fn = flags(old_text), flags(new_text)
    row = {
        "cik": company.cik, "name": company.name, "sic": company.sic,
        "period": period_of(new.filing_date, cfg),
        "old_accession": old.accession, "new_accession": new.accession,
        "old_filing_date": old.filing_date, "new_filing_date": new.filing_date, "report_date": new.report_date,
        "sections_found": ",".join(both), "missing_sections": ",".join(missing),
        "cosine_all": _r(D.cosine(old_all, new_all)), "jaccard_all": _r(D.jaccard(old_all, new_all)),
        "changed_share": _r(_weighted_changed_share(changes)),
        "added": sum(len(c.added) for c in changes), "removed": sum(len(c.removed) for c in changes),
        "edited": sum(len(c.edited) for c in changes),
        "payload_words": len(payload.split()), "truncated": int(truncated), "status": "ok" if both else "no_sections",
    }
    for s in ("1a", "3", "7", "9a"):
        row[f"cosine_{s}"] = _r(D.cosine(old_sec[s], new_sec[s])) if s in both else ""
    for k in fo:
        row[f"{k}_old"], row[f"{k}_new"] = fo[k], fn[k]
    meta = {"cik": company.cik, "real_names": [company.name] + company.former_names, "fiscal_year": fy,
            "new_accession": new.accession, "new_filing_date": new.filing_date, "period": row["period"],
            "payload": payload}
    return row, meta


def _weighted_changed_share(changes: list[D.SectionChanges]) -> float:
    total = sum(c.new_words for c in changes)
    if not total:
        return float("nan")
    return sum(c.changed_share * c.new_words for c in changes) / total


def _r(x: float) -> str:
    return "" if x != x else f"{x:.4f}"  # NaN → blank


def build(edgar: Edgar, cfg: FilingsConfig, year: int, sample: int | None, seed: int) -> list[dict]:
    """Fetch and diff 10-K pairs for (a random sample of) the CY`year` universe."""
    path = _p(cfg, f"universe_CY{year}.csv")
    universe = read_csv(path) or build_universe(edgar, cfg, year)
    if sample:
        universe = random.Random(seed).sample(universe, min(sample, len(universe)))
    done = {r["new_accession"] for r in read_csv(_p(cfg, "changes.csv"))}
    rows = []
    for n, u in enumerate(universe, 1):
        if u["accn"] in done:
            continue
        try:
            company = edgar.company(int(u["cik"]))
            if company.sic in cfg.exclude_sic:
                log.info("[%d/%d] %s: skipped (SIC %s)", n, len(universe), u["name"], company.sic)
                continue
            pair = consecutive_pair(company, u["accn"])
            if not pair:
                log.info("[%d/%d] %s: no consecutive 10-K pair", n, len(universe), u["name"])
                continue
            row, meta = process_pair(edgar, cfg, company, *pair)
        except Exception as e:  # one bad filing shouldn't stop a 2,000-company run
            log.warning("[%d/%d] %s: failed (%s)", n, len(universe), u["name"], e)
            continue
        row["public_float"] = u["public_float"]
        pfile = _p(cfg, "payloads", f"{row['cik']}_{row['new_accession']}.json")
        row["payload_file"] = os.path.relpath(pfile, cfg.out_dir)
        save_json_atomic(pfile, meta)
        append_csv(_p(cfg, "changes.csv"), CHANGE_FIELDS, [row])
        rows.append(row)
        log.info("[%d/%d] %s: sections %s, cosine %s, %s payload words", n, len(universe), row["name"],
                 row["sections_found"] or "-", row["cosine_all"] or "-", row["payload_words"])
    return rows


# ------------------------------------------------------------------ scoring
def _payloads(cfg: FilingsConfig, period: str | None) -> list[dict]:
    out = []
    for r in read_csv(_p(cfg, "changes.csv")):
        if r.get("status") != "ok" or (period and r["period"] != period):
            continue
        with open(_p(cfg, r["payload_file"]), encoding="utf-8") as f:
            out.append(json.load(f))
    return out


def cost_report(cfg: FilingsConfig, period: str | None, universe_size: int | None = None) -> dict:
    metas = _payloads(cfg, period)
    est = estimate_cost([m["payload"] for m in metas], cfg.price_in_per_mtok, cfg.price_out_per_mtok,
                        cfg.est_output_tokens)
    if universe_size and metas:
        scale = universe_size / len(metas)
        est["full_universe_per_year_usd"] = round(est["usd"] * scale, 2)
    return est


def score_all(cfg: FilingsConfig, period: str | None, max_calls: int) -> int:
    scorer = FilingScorer(cfg.model, max_calls)
    if not scorer.enabled:
        raise SystemExit("Set ANTHROPIC_API_KEY to score (or use --dry-run to see the cost).")
    if period != "holdout":
        log.warning("Scoring %s filings, which are older than the model's training cutoff (%s). "
                    "Treat results as contaminated until the recognition probe says otherwise.",
                    period or "all", cfg.model_knowledge_cutoff)
    done = {r["new_accession"] for r in read_csv(_p(cfg, "scores.csv")) if r.get("model") == cfg.model}
    n = 0
    for m in _payloads(cfg, period):
        if m["new_accession"] in done or scorer.calls_left <= 0:
            continue
        s = scorer.score(m["payload"])
        if s is None:
            continue
        append_csv(_p(cfg, "scores.csv"), SCORE_FIELDS, [{
            "cik": m["cik"], "new_accession": m["new_accession"], "new_filing_date": m["new_filing_date"],
            "period": m["period"], "model": cfg.model, "score": s.score, "materiality": s.materiality,
            "tags": "|".join(s.tags), "reason": s.reason, "input_tokens": s.input_tokens,
            "output_tokens": s.output_tokens, "scored_at": iso(utcnow()),
        }])
        n += 1
    return n


def run_probe(cfg: FilingsConfig, n: int, seed: int) -> dict:
    scorer = FilingScorer(cfg.model, n)
    if not scorer.enabled:
        raise SystemExit("Set ANTHROPIC_API_KEY to run the recognition probe.")
    metas = _payloads(cfg, None)
    metas = random.Random(seed).sample(metas, min(n, len(metas)))
    hits, year_err = 0, []
    for m in metas:
        ans = scorer.probe(m["payload"])
        if not ans:
            continue
        hit = probe_hit(str(ans.get("company_guess", "")), m["real_names"])
        hits += hit
        yg = ans.get("year_guess")
        err = abs(int(yg) - m["fiscal_year"]) if isinstance(yg, (int, float)) else ""
        if err != "":
            year_err.append(err)
        append_csv(_p(cfg, "probe.csv"), PROBE_FIELDS, [{
            "cik": m["cik"], "new_accession": m["new_accession"], "period": m["period"],
            "real_name": m["real_names"][0], "company_guess": ans.get("company_guess"),
            "company_confidence": ans.get("company_confidence"), "hit": int(hit), "year_guess": yg,
            "real_year": m["fiscal_year"], "year_error": err,
        }])
    return {"probed": len(metas), "company_hits": hits,
            "median_year_error": sorted(year_err)[len(year_err) // 2] if year_err else None}
