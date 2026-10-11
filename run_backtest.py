#!/usr/bin/env python3
"""Backtest every stock strategy on real daily data, 2016 to today.

  python run_backtest.py               real data from Alpaca (needs keys) -> BACKTEST.md
  python run_backtest.py --synthetic   offline test on fake prices -> data/demo/BACKTEST.md
"""
from __future__ import annotations

import argparse
import os

from lab import metrics as M
from lab.stocks.backtest import align, run, split_halves, summarize
from lab.stocks.data import Alpaca, load_bars, save_bars
from lab.stocks.engine import StockCosts
from lab.stocks.strategies import all_strategies, full_universe
from lab.util import append_csv, setup_logging, utcnow


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--synthetic", action="store_true")
    ap.add_argument("--start", default="2016-01-01")
    ap.add_argument("--refresh", action="store_true", help="re-download even if cached")
    args = ap.parse_args()
    setup_logging()

    syms = full_universe()
    if args.synthetic:
        from lab.stocks.synthetic import make_bars
        bars, out_md, out_dir = make_bars(syms), "data/demo/BACKTEST.md", "data/demo/backtest"
    else:
        cache = "data/backtest/bars.json"
        bars = {} if args.refresh else load_bars(cache)
        if not bars or any(s not in bars for s in syms):
            alp = Alpaca()
            if not alp.configured:
                raise SystemExit("Set ALPACA_API_KEY and ALPACA_API_SECRET (free paper account) first.")
            bars = alp.daily_bars(syms, start=args.start)
            save_bars(cache, bars)
        out_md, out_dir = "BACKTEST.md", "data/backtest"

    dates, closes, opens = align(bars)
    results, results_3x = {}, {}
    for strat in all_strategies():
        results[strat.name] = run(strat, dates, closes, opens)
        results_3x[strat.name] = run(strat, dates, closes, opens, costs=StockCosts(slippage_bps=15))

    os.makedirs(out_dir, exist_ok=True)
    eq_path = f"{out_dir}/equity_curves.csv"
    if os.path.exists(eq_path):
        os.remove(eq_path)
    append_csv(eq_path, ["date", "strategy", "equity"],
               ({"date": d, "strategy": n, "equity": round(e, 2)}
                for n, r in results.items() for d, e in zip(r.dates, r.equity)))

    write_md(out_md, results, results_3x, args.synthetic)
    print(open(out_md, encoding="utf-8").read())


def write_md(path: str, results: dict, results_3x: dict, synthetic: bool) -> None:
    spy = results["buy_hold_spy"]
    first, last = spy.dates[0], spy.dates[-1]
    S = {n: summarize(r) for n, r in results.items()}
    S3 = {n: summarize(r) for n, r in results_3x.items()}
    halves = {n: tuple(summarize(h) for h in split_halves(r)) for n, r in results.items()}
    spy_is, spy_oos = halves["buy_hold_spy"]

    L = ["# Stock strategy backtests", "",
         f"_{first} → {last} · signals at the close, fills at the next open + 5bp slippage per side · "
         f"dividend-adjusted prices · generated {utcnow():%Y-%m-%d}_", ""]
    if synthetic:
        L += ["> ⚠️ **SYNTHETIC DATA.** Proves the backtester runs; says nothing about real performance.", ""]
    L += ["| Strategy | CAGR | Total | Volatility | Sharpe | Sortino | Max drawdown | Trades | Win % | Time invested |",
          "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for n, s in sorted(S.items(), key=lambda kv: -kv[1]["sharpe"]):
        L.append(f"| `{n}` | {s['cagr']:.1f}% | {s['total']:+.0f}% | {s['vol']:.1f}% | {s['sharpe']:.2f} | "
                 f"{s['sortino']:.2f} | {s['mdd']:.1f}% | {s['trades']} | {M.fmt(s['win_rate'], 0)} | {s['exposure']:.0f}% |")

    L += ["", "## Does it hold up out of sample?", "",
          "Strategies are fixed in advance; the split just checks the result isn't one lucky stretch.", "",
          "| Strategy | 1st half CAGR / Sharpe | 2nd half CAGR / Sharpe | CAGR at 3x costs | Positive both halves | Beats SPY risk-adjusted (2nd half) | Drawdown < SPY's |",
          "|---|---|---|---:|:-:|:-:|:-:|"]
    for n, (a, b) in halves.items():
        if n == "buy_hold_spy":
            continue
        g = [a["cagr"] > 0 and b["cagr"] > 0, b["sharpe"] > spy_oos["sharpe"], S[n]["mdd"] < S["buy_hold_spy"]["mdd"]]
        L.append(f"| `{n}` | {a['cagr']:.1f}% / {a['sharpe']:.2f} | {b['cagr']:.1f}% / {b['sharpe']:.2f} | "
                 f"{S3[n]['cagr']:.1f}% | " + " | ".join("✅" if x else "❌" for x in g) + " |")
    L += ["", f"_SPY: 1st half {spy_is['cagr']:.1f}% / {spy_is['sharpe']:.2f}, "
          f"2nd half {spy_oos['cagr']:.1f}% / {spy_oos['sharpe']:.2f}._", ""]

    rsi = [float(t["ret_pct"]) for t in results["rsi2_reversion"].trades]
    rnd = [float(t["ret_pct"]) for t in results["random_control"].trades]
    if rsi and rnd:
        p = M.permutation_pvalue(rsi, rnd)
        ts = M.trade_stats(results["rsi2_reversion"].trades)
        tr = M.trade_stats(results["random_control"].trades)
        L += ["## RSI(2) vs. the coin flip", "",
              f"`rsi2_reversion`: {ts.n} trades, {ts.win_rate:.0f}% wins, {ts.mean_ret_pct:+.2f}% per trade "
              f"(95% CI {ts.ci_low_pct:+.2f} to {ts.ci_high_pct:+.2f}).  ",
              f"`random_control`: {tr.n} trades, {tr.win_rate:.0f}% wins, {tr.mean_ret_pct:+.2f}% per trade.  ",
              f"Chance of a gap this big if the signal were useless: **p = {p:.3f}** "
              f"({'signal beats random' if p < 0.05 else 'no evidence the signal beats random'}).", ""]
    L += ["Equity curves: `data/backtest/equity_curves.csv`.", ""]
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
