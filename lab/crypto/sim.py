"""A fake meme-coin market for testing the plumbing offline (`--demo`).

Tokens are born, pump, bleed, and get rugged at random. Results from this
market mean NOTHING about real strategy performance; it only proves the engine,
costs, exits, and reports work end to end before real data touches them.
"""
from __future__ import annotations

import math
import random

from .market import SOL_MINT, Snapshot

STEP = 300  # seconds per tick (5 minutes)
WINDOWS = {"m5": 1, "h1": 12, "h6": 72, "h24": 288}


class _Token:
    def __init__(self, rng: random.Random, addr: str, born: float, sym: str):
        self.addr, self.sym, self.born = addr, sym, born
        self.price = 10 ** rng.uniform(-7, -3)
        self.liq = rng.uniform(15_000, 400_000)
        self.regime, self.regime_left = "normal", 0
        self.rugged_at: float | None = None
        self.hist: list[tuple[float, float, float, int, int]] = []  # ts, price, vol, buys, sells
        self.supply_mult = rng.uniform(5, 80)  # fdv / liquidity

    def step(self, rng: random.Random, now: float) -> None:
        if self.regime_left <= 0:
            r = rng.random()
            self.regime = "pump" if r < 0.10 else "bleed" if r < 0.45 else "normal"
            self.regime_left = rng.randint(2, 18)
        self.regime_left -= 1
        drift = {"pump": 0.05, "bleed": -0.025, "normal": -0.002}[self.regime]
        ret = drift + rng.gauss(0, 0.045)
        if rng.random() < 0.01:                      # sudden dump
            ret -= rng.uniform(0.25, 0.6)
        self.price *= math.exp(ret)
        self.liq *= math.exp(ret * 0.5 + rng.gauss(0, 0.01))
        if self.rugged_at is None and rng.random() < 0.004:
            self.rugged_at = now
            self.liq *= 0.03
            self.price *= 0.05
        mult = 3.0 if self.regime == "pump" else 1.0
        vol = self.liq * rng.uniform(0.01, 0.12) * mult
        trades = max(2, int(vol / rng.uniform(80, 400)))
        buy_share = min(0.95, max(0.05, 0.5 + ret * 4 + rng.gauss(0, 0.08)))
        buys = int(trades * buy_share)
        self.hist.append((now, self.price, vol, buys, trades - buys))
        del self.hist[:-300]

    @property
    def dead(self) -> bool:
        return self.rugged_at is not None and self.hist and self.hist[-1][0] - self.rugged_at > 3 * STEP

    def snapshot(self, now: float) -> Snapshot:
        chg, vol, buys, sells = {}, {}, {}, {}
        for w, n in WINDOWS.items():
            pts = self.hist[-n:]
            prev = self.hist[-n - 1][1] if len(self.hist) > n else self.hist[0][1]
            chg[w] = round((self.price / prev - 1) * 100, 2)
            vol[w] = sum(p[2] for p in pts)
            buys[w] = sum(p[3] for p in pts)
            sells[w] = sum(p[4] for p in pts)
        return Snapshot(
            address=self.addr, symbol=self.sym, name=self.sym, pair_address="p" + self.addr, dex="simdex",
            url=f"sim://{self.sym}", price=self.price, liquidity=self.liq, fdv=self.liq * self.supply_mult,
            mcap=self.liq * self.supply_mult, age_min=(now - self.born) / 60, chg=chg, vol=vol, buys=buys,
            sells=sells, boosted=False,
        )


class SimMarket:
    def __init__(self, seed: int = 42, start: float = 1_760_000_000.0):
        self.rng = random.Random(seed)
        self.now = start
        self.tokens: dict[str, _Token] = {}
        self.new_this_step: list[str] = []
        self.sol_price = 150.0
        self._n = 0
        for _ in range(40):  # seed a market with some history
            self._spawn(self.now - self.rng.uniform(0, 3 * 86400))
        for _ in range(60):
            self.advance()

    def _spawn(self, born: float) -> None:
        self._n += 1
        addr = f"SIM{self._n:05d}" + "x" * 30
        t = _Token(self.rng, addr, born, f"MEME{self._n}")
        t.hist.append((born, t.price, 0.0, 1, 1))
        self.tokens[addr] = t
        self.new_this_step.append(addr)

    def advance(self) -> None:
        self.now += STEP
        self.new_this_step = []
        self.sol_price *= math.exp(self.rng.gauss(0.0001, 0.006))
        for _ in range(self.rng.choice([0, 0, 1, 1, 2, 3])):
            self._spawn(self.now - self.rng.uniform(0, 1800))
        for t in list(self.tokens.values()):
            t.step(self.rng, self.now)
            if t.dead or len(self.tokens) > 400 and t.hist[-1][1] < 1e-9:
                del self.tokens[t.addr]

    # ---- same interface as DexScreener ----
    def discover(self) -> list[str]:
        live = list(self.tokens)
        return self.new_this_step + self.rng.sample(live, min(25, len(live)))

    def snapshots(self, addresses: list[str]) -> dict[str, Snapshot]:
        out = {}
        for a in set(addresses):
            if a == SOL_MINT:
                out[a] = Snapshot(address=a, symbol="SOL", price=self.sol_price, liquidity=5e7, age_min=1e6,
                                  chg={"m5": 0, "h1": 0, "h6": 0, "h24": 0})
            elif a in self.tokens and self.tokens[a].hist:
                out[a] = self.tokens[a].snapshot(self.now)
        return out
