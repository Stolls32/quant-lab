"""Claude reads what changed between two 10-Ks and scores it.

Fail-safe like lab/ai.py: no API key or an unparseable answer means "no score",
never a guess. Every call is budgeted, and `estimate_cost` tells you what a run
will cost before you spend anything.

The recognition probe is the leak test: it asks the model to name the company
and year from an anonymized excerpt. If it often can, the historical backtest
of the LLM score can't be trusted, and only post-cutoff filings count.
"""
from __future__ import annotations

import json
import logging
import os
import re
from dataclasses import dataclass

from ..util import HttpError, http_json

log = logging.getLogger("lab.filings")

API_URL = "https://api.anthropic.com/v1/messages"

TAGS = ["liquidity", "going_concern", "debt_covenants", "financing_dilution", "customer_concentration",
        "supplier", "demand_weakness", "margin_pressure", "litigation", "regulatory", "material_weakness",
        "impairment", "restructuring", "management_change", "new_contract", "risk_resolved", "boilerplate"]

SYSTEM = f"""You are a forensic financial analyst. You will see only what CHANGED between \
two consecutive annual reports (Form 10-K) of one small, anonymized US public company: \
paragraphs added, removed, and edited (inside edited paragraphs, [-words-] were removed \
and {{+words+}} were added). Sections: Risk Factors, Legal Proceedings, MD&A, Controls and \
Procedures. The company's name is replaced with "the Company". Years are relative to the \
newer report: [FY+0] is its fiscal year, [FY-1] the year before.

Judge what the changes reveal about the business over the next 6-12 months, compared \
with what the prior report said. Most year-over-year changes are routine: updated dates, \
rewording, and generic macro, cyber or regulatory language that every company adds. Treat \
those as neutral. Weigh specific new information: worsening liquidity or financing needs, \
going-concern doubt, covenant problems, dependence on a customer or supplier, lost \
contracts, new litigation or investigations, material weaknesses, impairments, \
restructurings, confident statements softened or deleted. Score improvements (problems \
resolved, doubts removed, weaknesses fixed, new contracts) the same way in the other direction.

Do not try to identify the company or the calendar year, and do not use outside knowledge \
of what happened later. Judge only the text.

Reply with ONLY a JSON object:
{{"score": <int -5 to 5>, "materiality": <int 0-3>, "tags": [<up to 4 of: {", ".join(TAGS)}>], \
"reason": "<max 30 words>"}}
score: -5 serious deterioration, 0 neutral or boilerplate, +5 serious improvement.
materiality: 0 nothing substantive changed, 3 major new information."""

PROBE_SYSTEM = """You will see an excerpt from an anonymized annual report of a US public \
company (names, tickers and absolute years removed). Say whether you can tell WHICH company \
it is and roughly WHICH calendar year it covers. Guessing is fine, but be honest about confidence.
Reply with ONLY a JSON object:
{"company_guess": "<name or unknown>", "company_confidence": <int 0-100>, "year_guess": <int or null>}"""


@dataclass
class Score:
    score: int
    materiality: int
    tags: list[str]
    reason: str
    input_tokens: int = 0
    output_tokens: int = 0


def estimate_tokens(text: str) -> int:
    """Rough: ~4 characters per token for English prose."""
    return max(1, len(text) // 4)


def estimate_cost(payloads: list[str], price_in: float, price_out: float, out_tokens: int) -> dict:
    tin = sum(estimate_tokens(SYSTEM) + estimate_tokens(p) for p in payloads)
    tout = out_tokens * len(payloads)
    usd = tin / 1e6 * price_in + tout / 1e6 * price_out
    return {"calls": len(payloads), "input_tokens": tin, "output_tokens": tout, "usd": round(usd, 4),
            "usd_batch_api": round(usd / 2, 4)}


def _text(resp: dict | None) -> str:
    return "".join(b.get("text", "") for b in (resp or {}).get("content", []) if b.get("type") == "text")


def _json(text: str) -> dict | None:
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None


def parse_score(resp: dict | None) -> Score | None:
    data = _json(_text(resp))
    try:
        s, mat = int(data["score"]), int(data["materiality"])
    except (TypeError, KeyError, ValueError):
        return None
    if not (-5 <= s <= 5 and 0 <= mat <= 3):
        return None
    tags = [t for t in data.get("tags", []) if t in TAGS][:4] if isinstance(data.get("tags"), list) else []
    usage = (resp or {}).get("usage", {})
    return Score(s, mat, tags, str(data.get("reason", ""))[:240],
                 int(usage.get("input_tokens", 0)), int(usage.get("output_tokens", 0)))


class FilingScorer:
    def __init__(self, model: str, max_calls: int, api_key: str | None = None, max_tokens: int = 1000):
        self.api_key = api_key if api_key is not None else os.environ.get("ANTHROPIC_API_KEY", "")
        self.model = model
        self.calls_left = max_calls
        self.max_tokens = max_tokens

    @property
    def enabled(self) -> bool:
        return bool(self.api_key)

    def _call(self, system: str, user: str) -> dict | None:
        if not self.enabled or self.calls_left <= 0:
            return None
        self.calls_left -= 1
        body = {"model": self.model, "max_tokens": self.max_tokens, "system": system,
                "messages": [{"role": "user", "content": user}]}
        headers = {"x-api-key": self.api_key, "anthropic-version": "2023-06-01"}
        try:
            return http_json(API_URL, method="POST", headers=headers, body=body, timeout=90, retries=2)
        except (HttpError, OSError) as e:
            log.warning("Claude call failed: %s", e)
            return None

    def score(self, payload: str) -> Score | None:
        return parse_score(self._call(SYSTEM, payload))

    def probe(self, excerpt: str) -> dict | None:
        return _json(_text(self._call(PROBE_SYSTEM, excerpt[:12000])))


def probe_hit(guess: str, real_names: list[str]) -> bool:
    """Did the model name the real company? Loose match on the first distinctive word."""
    g = (guess or "").lower()
    if not g or g == "unknown":
        return False
    for name in real_names:
        words = [w for w in re.findall(r"[a-z0-9]+", name.lower()) if len(w) >= 3
                 and w not in {"inc", "corp", "the", "company", "holdings", "group", "ltd"}]
        if words and words[0] in g:
            return True
    return False
