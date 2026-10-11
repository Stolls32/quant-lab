"""Performance statistics, and the tests that separate skill from luck.

The core question of this whole project is: "Is this strategy's edge real, or
did it get lucky?"  Three tools answer it:

* Bootstrap confidence interval on the mean trade return. If the 95% CI's
  lower bound is above 0, a run of luck is an unlikely explanation.
* Permutation test against the random-entry control bot. The control trades the
  same universe with the same exits, but picks entries by coin flip. If the
  strategy can't beat that, its entry signal adds nothing.
* Cost stress test. Double every fee and slippage charge. Real execution is
  almost always worse than the model, so an edge that vanishes here is fragile.
"""
from __future__ import annotations

import math
import random
import statistics as st
from dataclasses import dataclass, field


@dataclass
class TradeStats:
    n: int = 0
    wins: int = 0
    win_rate: float = 0.0
    avg_win_pct: float = 0.0
    avg_loss_pct: float = 0.0
    payoff_ratio: float = 0.0       # avg win / avg loss (absolute)
    profit_factor: float = 0.0      # gross profit / gross loss
    mean_ret_pct: float = 0.0       # expectancy per trade, after costs
    median_ret_pct: float = 0.0
    total_pnl: float = 0.0
    total_cost: float = 0.0         # fees + slippage + price impact actually paid
    stressed_pnl: float = 0.0       # P&L if every cost were doubled
    ci_low_pct: float = 0.0         # 95% bootstrap CI of mean trade return
    ci_high_pct: float = 0.0
    t_stat: float = 0.0
    breakeven_win_rate: float = 0.0  # win rate needed at current payoff ratio
    by_reason: dict = field(default_factory=dict)


def bootstrap_mean_ci(xs: list[float], n_boot: int = 4000, alpha: float = 0.05, seed: int = 7) -> tuple[float, float]:
    if len(xs) < 2:
        return (float("nan"), float("nan"))
    rng = random.Random(seed)
    n = len(xs)
    means = sorted(sum(rng.choices(xs, k=n)) / n for _ in range(n_boot))
    lo = means[int(alpha / 2 * n_boot)]
    hi = means[int((1 - alpha / 2) * n_boot) - 1]
    return lo, hi


def t_stat(xs: list[float]) -> float:
    if len(xs) < 2:
        return 0.0
    sd = st.stdev(xs)
    return 0.0 if sd == 0 else st.mean(xs) / (sd / math.sqrt(len(xs)))


def trade_stats(trades: list[dict]) -> TradeStats:
    """`trades` rows need: ret_pct, pnl_usd, cost_usd, exit_reason."""
    s = TradeStats()
    if not trades:
        return s
    rets = [float(t["ret_pct"]) for t in trades]
    pnls = [float(t["pnl_usd"]) for t in trades]
    costs = [float(t.get("cost_usd") or 0) for t in trades]
    wins = [r for r in rets if r > 0]
    losses = [r for r in rets if r <= 0]
    s.n = len(rets)
    s.wins = len(wins)
    s.win_rate = len(wins) / s.n * 100
    s.avg_win_pct = st.mean(wins) if wins else 0.0
    s.avg_loss_pct = st.mean(losses) if losses else 0.0
    s.payoff_ratio = (s.avg_win_pct / abs(s.avg_loss_pct)) if losses and s.avg_loss_pct else float("inf")
    gp = sum(p for p in pnls if p > 0)
    gl = -sum(p for p in pnls if p <= 0)
    s.profit_factor = gp / gl if gl > 0 else float("inf")
    s.mean_ret_pct = st.mean(rets)
    s.median_ret_pct = st.median(rets)
    s.total_pnl = sum(pnls)
    s.total_cost = sum(costs)
    s.stressed_pnl = s.total_pnl - s.total_cost
    s.ci_low_pct, s.ci_high_pct = bootstrap_mean_ci(rets)
    s.t_stat = t_stat(rets)
    if s.payoff_ratio not in (0, float("inf")):
        s.breakeven_win_rate = 100 / (1 + s.payoff_ratio)
    reasons: dict[str, int] = {}
    for t in trades:
        reasons[t.get("exit_reason", "?")] = reasons.get(t.get("exit_reason", "?"), 0) + 1
    s.by_reason = reasons
    return s


def permutation_pvalue(a: list[float], b: list[float], n_perm: int = 4000, seed: int = 11) -> float:
    """One-sided p-value for H0: mean(a) <= mean(b).

    Shuffles the pooled trades between the two groups many times and asks how
    often chance alone produces a gap at least as big as the one observed.
    """
    if len(a) < 5 or len(b) < 5:
        return float("nan")
    rng = random.Random(seed)
    observed = st.mean(a) - st.mean(b)
    pooled = a + b
    na = len(a)
    hits = 0
    for _ in range(n_perm):
        rng.shuffle(pooled)
        if st.mean(pooled[:na]) - st.mean(pooled[na:]) >= observed:
            hits += 1
    return (hits + 1) / (n_perm + 1)


# ------------------------------------------------------------ equity curves
def max_drawdown(equity: list[float]) -> float:
    """Largest peak-to-trough drop, in percent (positive number)."""
    peak = -math.inf
    mdd = 0.0
    for e in equity:
        peak = max(peak, e)
        if peak > 0:
            mdd = max(mdd, (peak - e) / peak * 100)
    return mdd


def period_returns(equity: list[float]) -> list[float]:
    return [equity[i] / equity[i - 1] - 1 for i in range(1, len(equity)) if equity[i - 1] > 0]


def sharpe(rets: list[float], periods_per_year: float, rf_per_period: float = 0.0) -> float:
    if len(rets) < 3:
        return 0.0
    ex = [r - rf_per_period for r in rets]
    sd = st.stdev(ex)
    return 0.0 if sd == 0 else st.mean(ex) / sd * math.sqrt(periods_per_year)


def sortino(rets: list[float], periods_per_year: float) -> float:
    if len(rets) < 3:
        return 0.0
    downside = [min(0.0, r) ** 2 for r in rets]
    dd = math.sqrt(sum(downside) / len(rets))
    return 0.0 if dd == 0 else st.mean(rets) / dd * math.sqrt(periods_per_year)


def cagr(start: float, end: float, years: float) -> float:
    if start <= 0 or years <= 0 or end <= 0:
        return -100.0 if end <= 0 else 0.0
    return ((end / start) ** (1 / years) - 1) * 100


def fmt(x: float, d: int = 2, suffix: str = "") -> str:
    if x is None or (isinstance(x, float) and (math.isnan(x))):
        return "–"
    if x == float("inf"):
        return "∞"
    return f"{x:,.{d}f}{suffix}"
