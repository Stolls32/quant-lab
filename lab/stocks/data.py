"""Stock/ETF market data and broker access through Alpaca.

Why Alpaca: free paper-trading account (email signup only), free market data,
a clean API, and fractional shares. The SAME code that trades the paper
account trades a live account by swapping keys + base URL, which is exactly
what "if it's proven, it works in the real market" requires.

Keys live in environment variables (GitHub Actions secrets), never in code:
    ALPACA_API_KEY, ALPACA_API_SECRET, ALPACA_BASE_URL (defaults to paper)
"""
from __future__ import annotations

import logging
import os
import urllib.parse
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from ..util import HttpError, RateLimiter, fnum, http_json, load_json, save_json_atomic

log = logging.getLogger("lab.stocks.data")

DATA_URL = "https://data.alpaca.markets"
PAPER_URL = "https://paper-api.alpaca.markets"


@dataclass
class Bar:
    date: str      # YYYY-MM-DD (exchange date)
    o: float
    h: float
    l: float
    c: float
    v: float


class Alpaca:
    def __init__(self, key: str | None = None, secret: str | None = None, base_url: str | None = None):
        self.key = key or os.environ.get("ALPACA_API_KEY", "")
        self.secret = secret or os.environ.get("ALPACA_API_SECRET", "")
        self.base = (base_url or os.environ.get("ALPACA_BASE_URL") or PAPER_URL).rstrip("/")
        self.limiter = RateLimiter(150)  # free plan allows 200/min

    @property
    def configured(self) -> bool:
        return bool(self.key and self.secret)

    @property
    def is_paper(self) -> bool:
        return "paper-api" in self.base

    def _h(self) -> dict:
        return {"APCA-API-KEY-ID": self.key, "APCA-API-SECRET-KEY": self.secret}

    def _get(self, url: str, params: dict | None = None):
        if params:
            url += "?" + urllib.parse.urlencode(params)
        return http_json(url, headers=self._h(), limiter=self.limiter)

    # ------------------------------------------------------------ market data
    def daily_bars(self, symbols: list[str], start: str, end: str | None = None) -> dict[str, list[Bar]]:
        """Split- AND dividend-adjusted daily bars (adjustment=all), so returns
        include dividends like a real total-return investor would get."""
        if end is None:  # free plan: SIP data must be >15 minutes old
            end = (datetime.now(timezone.utc) - timedelta(minutes=20)).strftime("%Y-%m-%dT%H:%M:%SZ")
        out: dict[str, list[Bar]] = {s: [] for s in symbols}
        for feed in ("sip", "iex"):
            try:
                token = None
                while True:
                    params = {"symbols": ",".join(symbols), "timeframe": "1Day", "start": start, "end": end,
                              "adjustment": "all", "feed": feed, "limit": 10000}
                    if token:
                        params["page_token"] = token
                    resp = self._get(f"{DATA_URL}/v2/stocks/bars", params) or {}
                    for sym, rows in (resp.get("bars") or {}).items():
                        out.setdefault(sym, []).extend(
                            Bar(r["t"][:10], fnum(r["o"]), fnum(r["h"]), fnum(r["l"]), fnum(r["c"]), fnum(r["v"]))
                            for r in rows)
                    token = resp.get("next_page_token")
                    if not token:
                        break
                break
            except HttpError as e:
                if e.status in (402, 403, 422) and feed == "sip":
                    log.warning("SIP feed refused (%s); falling back to IEX", e.status)
                    out = {s: [] for s in symbols}
                    continue
                raise
        for sym in out:
            dedup = {b.date: b for b in out[sym]}
            out[sym] = [dedup[d] for d in sorted(dedup)]
        return out

    def quotes(self, symbols: list[str]) -> dict[str, dict]:
        """Real-time IEX quote per symbol: {'bid','ask','last'}."""
        resp = self._get(f"{DATA_URL}/v2/stocks/snapshots", {"symbols": ",".join(symbols), "feed": "iex"}) or {}
        out = {}
        for sym, snap in resp.items():
            q = (snap or {}).get("latestQuote") or {}
            t = (snap or {}).get("latestTrade") or {}
            out[sym] = {"bid": fnum(q.get("bp")), "ask": fnum(q.get("ap")), "last": fnum(t.get("p"))}
        return out

    # ------------------------------------------------------------- trading
    def clock(self) -> dict:
        return self._get(f"{self.base}/v2/clock") or {}

    def account(self) -> dict:
        return self._get(f"{self.base}/v2/account") or {}

    def positions(self) -> list[dict]:
        return self._get(f"{self.base}/v2/positions") or []

    def submit_order(self, symbol: str, side: str, notional: float | None = None, qty: float | None = None) -> dict:
        body = {"symbol": symbol, "side": side, "type": "market", "time_in_force": "day"}
        if notional is not None:
            body["notional"] = f"{notional:.2f}"
        else:
            body["qty"] = f"{qty:.6f}"
        return http_json(f"{self.base}/v2/orders", method="POST", headers=self._h(), body=body,
                         limiter=self.limiter, retries=0)

    def close_position(self, symbol: str) -> dict:
        return http_json(f"{self.base}/v2/positions/{symbol}", method="DELETE", headers=self._h(),
                         limiter=self.limiter, retries=0)


# ------------------------------------------------------------------ caching
def save_bars(path: str, bars: dict[str, list[Bar]]) -> None:
    save_json_atomic(path, {s: [[b.date, b.o, b.h, b.l, b.c, b.v] for b in bs] for s, bs in bars.items()})


def load_bars(path: str) -> dict[str, list[Bar]]:
    raw = load_json(path, {})
    return {s: [Bar(*r) for r in rows] for s, rows in raw.items()}
