"""Stock/ETF strategies. Each one is a published, decades-tested idea, not
something curve-fit to recent data. See RESEARCH.md for the evidence and the
known ways each one fails.

A strategy is a pure function of price history: given closes up to the signal
day, it returns target portfolio weights. The SAME function runs in the
backtest and in live trading, so there's no gap between "what we tested" and
"what we trade".

Trading is daily-bar only. These are swing/position strategies held for days
to months, not day trading: retail traders have no speed edge intraday.
"""
from __future__ import annotations

import hashlib
import random
from dataclasses import dataclass, field

SECTORS = ["XLK", "XLF", "XLE", "XLV", "XLI", "XLY", "XLP", "XLU", "XLB"]
CASH = "BIL"  # 1-3 month T-bill ETF: the "cash" position that still earns interest


# ---------------------------------------------------------------- indicators
def sma(xs: list[float], n: int) -> float | None:
    return sum(xs[-n:]) / n if len(xs) >= n else None


def rsi(xs: list[float], n: int = 2, warmup: int = 100) -> float | None:
    """Wilder's RSI. Uses the last `warmup` bars, plenty for convergence at n=2."""
    xs = xs[-(warmup + 1):]
    if len(xs) < n + 1:
        return None
    gains = [max(0.0, xs[i] - xs[i - 1]) for i in range(1, len(xs))]
    losses = [max(0.0, xs[i - 1] - xs[i]) for i in range(1, len(xs))]
    ag, al = sum(gains[:n]) / n, sum(losses[:n]) / n
    for g, l in zip(gains[n:], losses[n:]):
        ag = (ag * (n - 1) + g) / n
        al = (al * (n - 1) + l) / n
    if al == 0:
        return 100.0
    return 100 - 100 / (1 + ag / al)


def total_return(xs: list[float], lookback: int, skip: int = 0) -> float | None:
    """Return from `lookback` bars ago to `skip` bars ago."""
    if len(xs) < lookback + 1:
        return None
    return xs[-1 - skip] / xs[-1 - lookback] - 1


# -------------------------------------------------------------------- base
@dataclass
class Ctx:
    date: str                          # signal date (last completed bar)
    closes: dict[str, list[float]]     # per symbol, oldest -> newest, ends at `date`
    holdings: dict[str, dict] = field(default_factory=dict)  # sym -> {"entry_date","bars_held"}
    rebalance_day: bool = False        # last trading day of the month (or first run)

    def px(self, sym: str) -> float | None:
        c = self.closes.get(sym)
        return c[-1] if c else None


class StockStrategy:
    name = "base"
    description = ""
    universe: list[str] = []
    is_benchmark = False
    is_control = False
    # False: only enter/exit positions, never trim/top-up winners and losers.
    resize_existing = False

    def targets(self, ctx: Ctx) -> dict[str, float] | None:
        """Target weights (0-1, sum <= 1). None means 'no change today'."""
        raise NotImplementedError


# ------------------------------------------------------------- strategies
class BuyHoldSPY(StockStrategy):
    name = "buy_hold_spy"
    description = "Benchmark: 100% S&P 500 (SPY), never sold. Everything else must beat this."
    universe = ["SPY"]
    is_benchmark = True

    def targets(self, ctx):
        return {"SPY": 1.0} if "SPY" not in ctx.holdings and ctx.px("SPY") else None


class TrendSPY(StockStrategy):
    """Faber-style trend filter: own stocks above the 200-day average, T-bills below.
    Goal isn't beating SPY's return; it's similar return with far smaller crashes."""
    name = "trend_spy"
    description = "SPY when above its 200-day average (2% exit band), T-bills when below."
    universe = ["SPY", CASH]

    def targets(self, ctx):
        c = ctx.closes.get("SPY", [])
        m = sma(c, 200)
        if m is None or ctx.px(CASH) is None:
            return None
        in_spy = "SPY" in ctx.holdings
        want_spy = c[-1] > m if not in_spy else c[-1] > m * 0.98
        if want_spy and not in_spy:
            return {"SPY": 1.0}
        if not want_spy and CASH not in ctx.holdings:
            return {CASH: 1.0}
        return None


class DualMomentum(StockStrategy):
    """Antonacci's Global Equities Momentum. Monthly: if US stocks beat T-bills
    over 12 months, hold the stronger of US vs. international stocks; otherwise
    hold bonds."""
    name = "dual_momentum"
    description = "Monthly: strongest of SPY/EFA if it beats T-bills over 12m, else bonds (AGG)."
    universe = ["SPY", "EFA", "AGG", CASH]
    resize_existing = True

    def targets(self, ctx):
        if not ctx.rebalance_day:
            return None
        r = {s: total_return(ctx.closes.get(s, []), 252) for s in ("SPY", "EFA", CASH)}
        if any(v is None for v in r.values()) or ctx.px("AGG") is None:
            return None
        if r["SPY"] > r[CASH]:
            return {"SPY" if r["SPY"] >= r["EFA"] else "EFA": 1.0}
        return {"AGG": 1.0}


class SectorMomentum(StockStrategy):
    """Cross-sectional momentum on the 9 original S&P sector ETFs. Monthly:
    hold the top 3 by 12-month return skipping the latest month (12-1), but only
    while SPY is above its 200-day average."""
    name = "sector_momentum"
    description = "Monthly: top-3 sectors by 12-1 momentum, equal weight; T-bills if SPY < 200d avg."
    universe = SECTORS + ["SPY", CASH]
    resize_existing = True
    top_n = 3

    def targets(self, ctx):
        if not ctx.rebalance_day:
            return None
        spy = ctx.closes.get("SPY", [])
        m = sma(spy, 200)
        if m is None or ctx.px(CASH) is None:
            return None
        if spy[-1] < m:
            return {CASH: 1.0}
        scores = {s: total_return(ctx.closes.get(s, []), 252, skip=21) for s in SECTORS}
        ranked = sorted(((v, s) for s, v in scores.items() if v is not None and v > 0), reverse=True)
        picks = [s for _, s in ranked[: self.top_n]]
        if not picks:
            return {CASH: 1.0}
        w = {s: 1.0 / self.top_n for s in picks}
        if len(picks) < self.top_n:
            w[CASH] = 1.0 - sum(w.values())
        return w


class RSI2Reversion(StockStrategy):
    """Connors RSI(2) pullback: in an uptrend (above 200-day avg), buy a broad
    ETF after a sharp 2-day drop (RSI2 < 10); sell when it closes back above its
    5-day average or after 10 days. Short holds, high win rate, small wins."""
    name = "rsi2_reversion"
    description = "Buy uptrending ETFs on RSI(2)<10 dips, exit above 5-day avg or after 10 days. Max 5 x 20%."
    universe = ["SPY", "QQQ", "IWM", "DIA"] + SECTORS
    max_positions = 5
    entry_rsi = 10.0
    max_hold = 10

    def targets(self, ctx):
        w: dict[str, float] = {}
        for sym, h in ctx.holdings.items():
            c = ctx.closes.get(sym, [])
            m5 = sma(c, 5)
            exit_ = (m5 is not None and c[-1] > m5) or h["bars_held"] >= self.max_hold
            w[sym] = 0.0 if exit_ else 1.0 / self.max_positions
        slots = self.max_positions - sum(1 for v in w.values() if v > 0)
        cands = []
        for sym in self.universe:
            if sym in ctx.holdings:
                continue
            c = ctx.closes.get(sym, [])
            m200, r = sma(c, 200), rsi(c, 2)
            if m200 and r is not None and c[-1] > m200 and r < self.entry_rsi:
                cands.append((r, sym))
        for _, sym in sorted(cands)[: max(0, slots)]:
            w[sym] = 1.0 / self.max_positions
        return w


class RandomControlStocks(StockStrategy):
    """Coin-flip control for rsi2_reversion: same universe, same slot size,
    similar holding period, but random entries. If RSI2 can't beat this, its
    signal is not why it made money."""
    name = "random_control"
    description = "Control: random entries in the RSI2 universe, random 2-10 day holds."
    universe = RSI2Reversion.universe
    is_control = True
    max_positions = 5
    entry_prob = 0.06  # per free slot per day (roughly matches rsi2 trade count)

    @staticmethod
    def _hold_len(sym: str, entry_date: str) -> int:
        h = int(hashlib.sha256(f"{sym}{entry_date}".encode()).hexdigest(), 16)
        return 2 + h % 9

    def targets(self, ctx):
        rng = random.Random(ctx.date)
        w: dict[str, float] = {}
        for sym, h in ctx.holdings.items():
            done = h["bars_held"] >= self._hold_len(sym, h["entry_date"])
            w[sym] = 0.0 if done else 1.0 / self.max_positions
        slots = self.max_positions - sum(1 for v in w.values() if v > 0)
        pool = [s for s in self.universe if s not in ctx.holdings and ctx.px(s)]
        for _ in range(slots):
            if pool and rng.random() < self.entry_prob:
                sym = rng.choice(pool)
                pool.remove(sym)
                w[sym] = 1.0 / self.max_positions
        return w


def all_strategies() -> list[StockStrategy]:
    return [BuyHoldSPY(), TrendSPY(), DualMomentum(), SectorMomentum(), RSI2Reversion(), RandomControlStocks()]


def full_universe() -> list[str]:
    syms: list[str] = []
    for s in all_strategies():
        syms += s.universe
    return list(dict.fromkeys(syms))
