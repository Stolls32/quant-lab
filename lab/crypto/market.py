"""Live Solana market data from DexScreener's free public API (no key needed).

Docs: https://docs.dexscreener.com/api/reference
Discovery endpoints are limited to 60 requests/minute, pair endpoints are more
generous. We stay well under both.
"""
from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field

from ..util import HttpError, RateLimiter, fnum, http_json

log = logging.getLogger("lab.market")

BASE = "https://api.dexscreener.com"
CHAIN = "solana"
SOL_MINT = "So11111111111111111111111111111111111111112"
USDC_MINT = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
QUOTES = {SOL_MINT, USDC_MINT}


@dataclass
class Snapshot:
    """One token's market state at one moment (its most liquid SOL/USDC pool)."""

    address: str
    symbol: str
    name: str = ""
    pair_address: str = ""
    dex: str = ""
    url: str = ""
    price: float = 0.0           # USD
    liquidity: float = 0.0       # USD in the pool (both sides)
    fdv: float = 0.0
    mcap: float = 0.0
    age_min: float = 0.0         # minutes since the pool was created
    chg: dict = field(default_factory=dict)    # % change: m5, h1, h6, h24
    vol: dict = field(default_factory=dict)    # USD volume: m5, h1, h6, h24
    buys: dict = field(default_factory=dict)   # tx counts per window
    sells: dict = field(default_factory=dict)
    boosted: bool = False        # paid promotion on DexScreener right now

    def c(self, w: str) -> float:
        return fnum(self.chg.get(w))

    def v(self, w: str) -> float:
        return fnum(self.vol.get(w))

    def b(self, w: str) -> int:
        return int(fnum(self.buys.get(w)))

    def s(self, w: str) -> int:
        return int(fnum(self.sells.get(w)))

    def to_brief(self) -> dict:
        return {
            "symbol": self.symbol, "price": self.price, "liq": round(self.liquidity),
            "fdv": round(self.fdv), "age_h": round(self.age_min / 60, 1),
            "chg": self.chg, "vol": {k: round(fnum(v)) for k, v in self.vol.items()},
            "buys": self.buys, "sells": self.sells, "boosted": self.boosted, "dex": self.dex,
        }


def snapshot_from_pair(p: dict, now_ms: float) -> Snapshot | None:
    base = p.get("baseToken") or {}
    quote = (p.get("quoteToken") or {}).get("address")
    price = fnum(p.get("priceUsd"))
    if not base.get("address") or quote not in QUOTES or price <= 0:
        return None
    txns = p.get("txns") or {}
    created = fnum(p.get("pairCreatedAt"))
    return Snapshot(
        address=base["address"],
        symbol=(base.get("symbol") or "?")[:20],
        name=(base.get("name") or "")[:40],
        pair_address=p.get("pairAddress", ""),
        dex=p.get("dexId", ""),
        url=p.get("url", ""),
        price=price,
        liquidity=fnum((p.get("liquidity") or {}).get("usd")),
        fdv=fnum(p.get("fdv")),
        mcap=fnum(p.get("marketCap")),
        age_min=(now_ms - created) / 60000 if created else 0.0,
        chg={k: fnum(v) for k, v in (p.get("priceChange") or {}).items()},
        vol={k: fnum(v) for k, v in (p.get("volume") or {}).items()},
        buys={k: int(fnum((v or {}).get("buys"))) for k, v in txns.items()},
        sells={k: int(fnum((v or {}).get("sells"))) for k, v in txns.items()},
        boosted=bool(((p.get("boosts") or {}).get("active") or 0) > 0),
    )


class DexScreener:
    def __init__(self) -> None:
        self.slow = RateLimiter(50)    # discovery endpoints (limit 60/min)
        self.fast = RateLimiter(200)   # pair endpoints (limit 300/min)

    def discover(self) -> list[str]:
        """Token addresses that are new, promoted, or trending right now."""
        found: list[str] = []
        for path in ("/token-profiles/latest/v1", "/token-profiles/recent-updates/v1",
                     "/community-takeovers/latest/v1", "/token-boosts/latest/v1", "/token-boosts/top/v1"):
            try:
                rows = http_json(BASE + path, limiter=self.slow) or []
            except (HttpError, OSError) as e:
                log.warning("discovery %s failed: %s", path, e)
                continue
            if isinstance(rows, dict):
                rows = rows.get("data") or rows.get("pairs") or []
            for r in rows:
                if r.get("chainId") == CHAIN and r.get("tokenAddress"):
                    found.append(r["tokenAddress"])
        return list(dict.fromkeys(found))  # de-dupe, keep order

    def snapshots(self, addresses: list[str]) -> dict[str, Snapshot]:
        """Best (most liquid) SOL/USDC pool for each token, 30 tokens per call."""
        now_ms = time.time() * 1000
        out: dict[str, Snapshot] = {}
        self.last_failed: set[str] = set()  # tokens we couldn't check (not "missing")
        addrs = list(dict.fromkeys(addresses))
        for i in range(0, len(addrs), 30):
            chunk = addrs[i:i + 30]
            try:
                pairs = http_json(f"{BASE}/tokens/v1/{CHAIN}/{','.join(chunk)}", limiter=self.fast) or []
            except (HttpError, OSError) as e:
                log.warning("pairs chunk failed (%d tokens): %s", len(chunk), e)
                self.last_failed.update(chunk)
                continue
            if isinstance(pairs, dict):
                pairs = pairs.get("pairs") or []
            wanted = set(chunk)
            for p in pairs:
                snap = snapshot_from_pair(p, now_ms)
                if not snap or snap.address not in wanted:
                    continue
                cur = out.get(snap.address)
                if cur is None or snap.liquidity > cur.liquidity:
                    out[snap.address] = snap
        return out
