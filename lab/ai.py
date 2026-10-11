"""Claude as a trade analyst, called through the Anthropic Messages API.

Optional: if ANTHROPIC_API_KEY isn't set, the `claude_analyst` bot simply sits
out and every other bot runs normally.

Design choices:
* Small, fast model and a hard daily call budget, so cost stays predictable.
* Claude returns strict JSON: a 0-10 score and a short reason. Anything that
  doesn't parse is treated as "no trade" (fail safe, never fail open).
* Every score is logged with what the price did 1h and 4h later, whether or
  not the bot bought. After a few hundred scores you can measure directly
  whether high scores predict better outcomes than low scores.
"""
from __future__ import annotations

import json
import logging
import os
import re

from .util import HttpError, http_json

log = logging.getLogger("lab.ai")

API_URL = "https://api.anthropic.com/v1/messages"

SYSTEM = """You are a skeptical quantitative analyst screening Solana meme-coin \
trades for a paper-trading experiment. Base rates are brutal: most meme coins \
lose most of their value, momentum often reverses within minutes, and round-trip \
costs are about 5%. You will see one token's live metrics and its recent price \
path. Estimate whether price is more likely to rise 20%+ before it falls 18% \
within the next 6 hours.

Score 0-10: 0-3 likely loser or likely manipulation; 4-6 coin flip; 7-8 \
clearly favorable setup; 9-10 exceptional, which should be very rare. Look for: \
sustainable volume vs liquidity, buyer/seller balance across windows, whether \
the move is extended or early, liquidity depth vs valuation, signs of a single \
whale pump, paid promotion (boosted) without organic flow.

Reply with ONLY a JSON object: {"score": <int 0-10>, "reason": "<max 20 words>"}"""


class ClaudeScorer:
    def __init__(self, model: str, max_calls_per_day: int, usage: dict, api_key: str | None = None):
        self.api_key = api_key if api_key is not None else os.environ.get("ANTHROPIC_API_KEY", "")
        self.model = model
        self.max_calls_per_day = max_calls_per_day
        self.usage = usage  # persisted dict: {"day": "YYYY-MM-DD", "calls": n}

    @property
    def enabled(self) -> bool:
        return bool(self.api_key)

    def budget_left(self, today: str) -> int:
        if self.usage.get("day") != today:
            self.usage.clear()
            self.usage.update({"day": today, "calls": 0})
        return self.max_calls_per_day - self.usage["calls"]

    def score(self, brief: dict, price_path: list[float], today: str) -> tuple[int, str] | None:
        if not self.enabled or self.budget_left(today) <= 0:
            return None
        self.usage["calls"] += 1
        path = ", ".join(f"{p:.6g}" for p in price_path[-24:]) or "n/a"
        user = (
            "Token metrics (chg = % price change, vol = USD volume, buys/sells = tx counts, "
            "by window m5/h1/h6/h24; liq = pool liquidity USD; age_h = pool age in hours):\n"
            f"{json.dumps(brief, separators=(',', ':'))}\n\n"
            f"Price every ~5 minutes, oldest to newest: [{path}]"
        )
        body = {
            "model": self.model,
            "max_tokens": 120,
            "system": SYSTEM,
            "messages": [{"role": "user", "content": user}],
        }
        headers = {"x-api-key": self.api_key, "anthropic-version": "2023-06-01"}
        try:
            resp = http_json(API_URL, method="POST", headers=headers, body=body, timeout=45, retries=2)
        except (HttpError, OSError) as e:
            log.warning("Claude call failed: %s", e)
            return None
        return parse_score(resp)


def parse_score(resp: dict | None) -> tuple[int, str] | None:
    try:
        text = "".join(b.get("text", "") for b in resp.get("content", []) if b.get("type") == "text")
        m = re.search(r"\{.*\}", text, re.S)
        data = json.loads(m.group(0)) if m else {}
        score = int(data["score"])
        if not 0 <= score <= 10:
            return None
        return score, str(data.get("reason", ""))[:160]
    except (AttributeError, KeyError, ValueError, TypeError, json.JSONDecodeError):
        return None
