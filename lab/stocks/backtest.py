"""Daily backtester for the stock strategies.

Honesty rules baked in:
* No look-ahead: signals use closes through day t; trades fill at day t+1's
  OPEN plus slippage. (Using day t's close to both decide and fill is the most
  common backtest lie.)
* Adjusted prices (splits + dividends), so buy-and-hold gets its dividends.
* Costs on every fill.
* In-sample / out-of-sample split: the report shows the first and second half
  separately. A real edge works in both halves; a fluke usually doesn't.
* Same strategy code as live trading.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

from .. import metrics as M
from .data import Bar
from .engine import StockCosts, age_positions, book_equity, holdings_view, new_book, rebalance
from .strategies import Ctx, StockStrategy

WARMUP = 260  # bars of history needed before the first signal (12m momentum + 200d avg)


@dataclass
class BacktestResult:
    name: str
    dates: list[str]
    equity: list[float]
    trades: list[dict] = field(default_factory=list)
    exposure_pct: float = 0.0


def align(bars: dict[str, list[Bar]], calendar_sym: str = "SPY") -> tuple[list[str], dict, dict]:
    """Closes and opens aligned to the calendar symbol's trading days.
    A symbol has None before it starts trading; gaps are forward-filled."""
    dates = [b.date for b in bars[calendar_sym]]
    closes, opens = {}, {}
    for sym, bs in bars.items():
        by = {b.date: b for b in bs}
        c_row, o_row, last = [], [], None
        for d in dates:
            b = by.get(d)
            if b:
                last = b
                c_row.append(b.c)
                o_row.append(b.o)
            else:
                c_row.append(last.c if last else None)
                o_row.append(last.c if last else None)
        closes[sym], opens[sym] = c_row, o_row
    return dates, closes, opens


def run(strategy: StockStrategy, dates: list[str], closes: dict, opens: dict,
        start_cash: float = 10_000.0, costs: StockCosts | None = None, start_index: int = WARMUP) -> BacktestResult:
    costs = costs or StockCosts()
    book = new_book(start_cash)
    syms = [s for s in strategy.universe if s in closes]
    first_valid = {s: next((i for i, v in enumerate(closes[s]) if v is not None), len(dates)) for s in syms}
    res = BacktestResult(strategy.name, [], [])
    invested_days = 0
    for i in range(start_index, len(dates) - 1):
        d, nxt = dates[i], dates[i + 1]
        age_positions(book)
        view = {s: closes[s][first_valid[s]: i + 1] for s in syms if first_valid[s] <= i}
        reb = nxt[:7] != d[:7] or not book["positions"]
        ctx_holdings = holdings_view(book)
        tgt = strategy.targets(Ctx(date=d, closes=view, holdings=ctx_holdings, rebalance_day=reb))
        if tgt is not None:
            fills = {s: opens[s][i + 1] for s in syms if opens[s][i + 1] is not None}
            res.trades += rebalance(book, tgt, fills, nxt, costs, strategy.resize_existing, strategy.name)
        marks = {s: closes[s][i + 1] for s in syms if closes[s][i + 1] is not None}
        eq = book_equity(book, marks)
        for s, p in book["positions"].items():
            if s in marks:
                p["last_mark"] = marks[s]
        res.dates.append(nxt)
        res.equity.append(eq)
        if book["positions"] and not set(book["positions"]) <= {"BIL"}:
            invested_days += 1
    res.exposure_pct = invested_days / max(1, len(res.dates)) * 100
    return res


def summarize(r: BacktestResult) -> dict:
    if len(r.equity) < 3:
        return {}
    years = len(r.equity) / 252
    rets = M.period_returns(r.equity)
    ts = M.trade_stats(r.trades)
    return {
        "cagr": M.cagr(r.equity[0], r.equity[-1], years),
        "total": (r.equity[-1] / r.equity[0] - 1) * 100,
        "vol": (sum(x * x for x in rets) / len(rets)) ** 0.5 * math.sqrt(252) * 100,
        "sharpe": M.sharpe(rets, 252),
        "sortino": M.sortino(rets, 252),
        "mdd": M.max_drawdown(r.equity),
        "trades": ts.n, "win_rate": ts.win_rate, "pf": ts.profit_factor,
        "exposure": r.exposure_pct, "years": years,
    }


def split_halves(r: BacktestResult) -> tuple[BacktestResult, BacktestResult]:
    h = len(r.dates) // 2
    mid = r.dates[h]
    a = BacktestResult(r.name, r.dates[:h], r.equity[:h], [t for t in r.trades if t["closed_at"] < mid])
    b = BacktestResult(r.name, r.dates[h:], r.equity[h:], [t for t in r.trades if t["closed_at"] >= mid])
    return a, b
