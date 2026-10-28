"""Builds REPORT.md: the leaderboard plus a pass/fail checklist for every bot.

The checklist ("promotion gates") is the line between "it made money" and "it
has an edge worth risking real money on". A bot is only a real-money candidate
when EVERY gate is green. The bar is set in advance on purpose: deciding the
rules after seeing results is how people fool themselves.
"""
from __future__ import annotations

import os
import statistics as st
from collections import defaultdict

from . import metrics as M
from .util import load_json, parse_iso, read_csv, utcnow

CRYPTO_GATES = {
    "min_trades": 100,
    "min_days": 30,
    "max_drawdown_pct": 40.0,
    "control_p_value": 0.05,
}
STOCK_GATES = {
    "min_days": 126,        # ~6 months of forward (live paper) trading
    "max_dd_vs_spy": 1.0,   # drawdown no worse than SPY's over the same period
}


def _ok(b: bool) -> str:
    return "✅" if b else "❌"


def _series(rows: list[dict], key: str, val: str = "equity") -> dict[str, list[float]]:
    out: dict[str, list[float]] = defaultdict(list)
    for r in rows:
        out[r[key]].append(float(r[val]))
    return out


# ------------------------------------------------------------------ crypto
def crypto_section(d: str) -> list[str]:
    state = load_json(f"{d}/state.json", None)
    if not state:
        return ["## Meme coins (Solana)", "", "_No runs yet._", ""]
    trades = read_csv(f"{d}/trades.csv")
    eq = _series(read_csv(f"{d}/equity.csv"), "bot")
    by_bot: dict[str, list[dict]] = defaultdict(list)
    for t in trades:
        by_bot[t["bot"]].append(t)
    started = parse_iso(state["started_at"])
    last = parse_iso(state.get("last_tick") or state["started_at"])
    days = (last - started).total_seconds() / 86400
    control_rets = [float(t["ret_pct"]) for t in by_bot.get("random_control", [])]
    sol_book = state["bots"].get("hold_sol")
    sol_ret = (eq["hold_sol"][-1] / sol_book["start_cash"] - 1) * 100 if eq.get("hold_sol") and sol_book else 0.0

    L = ["## Meme coins (Solana) — live paper trading", "",
         f"Running **{days:.1f} days** · {state['ticks']:,} market checks · last check {state.get('last_tick')} · "
         f"each bot started with ${CRYPTO_START(state):.2f}", "",
         *_seasons_note(state),
         "| Bot | Equity | Return | Trades | Win % | Avg win / loss | Per-trade avg (95% CI) | Profit factor | Max DD | Open |",
         "|---|---:|---:|---:|---:|---|---|---:|---:|---:|"]
    rows = []
    for name, book in state["bots"].items():
        series = eq.get(name, [book["start_cash"]])
        ret = (series[-1] / book["start_cash"] - 1) * 100
        s = M.trade_stats(by_bot.get(name, []))
        rows.append((ret, name, series, s, book))
    rows.sort(key=lambda r: r[0], reverse=True)
    for ret, name, series, s, book in rows:
        ci = f"{M.fmt(s.mean_ret_pct, 1, '%')} ({M.fmt(s.ci_low_pct, 1)} to {M.fmt(s.ci_high_pct, 1)})" if s.n else "–"
        wl = f"{M.fmt(s.avg_win_pct, 1, '%')} / {M.fmt(s.avg_loss_pct, 1, '%')}" if s.n else "–"
        label = f"`{name}`" + (" _(off: no API key)_" if name == "claude_analyst" and not state.get("ai_enabled") else "")
        L.append(f"| {label} | ${series[-1]:.2f} | {ret:+.1f}% | {s.n} | {M.fmt(s.win_rate, 0) if s.n else '–'} | "
                 f"{wl} | {ci} | {M.fmt(s.profit_factor) if s.n else '–'} | "
                 f"{M.max_drawdown([book['start_cash'], *series]):.1f}% | {len(book['positions'])} |")

    L += ["", "### Real-money gates (all must be ✅)", "",
          "| Bot | 100+ trades | 30+ days | Profitable | Profitable at 2x costs | Edge CI above 0 | Beats coin flip | Beats holding SOL | Drawdown < 40% | Verdict |",
          "|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|"]
    tested = [r for r in rows if r[1] not in ("hold_sol", "random_control")]
    # Bonferroni: testing several bots at once makes a lucky "winner" likely,
    # so each one must clear 0.05 / (number of bots tested).
    p_bar = CRYPTO_GATES["control_p_value"] / max(1, len(tested))
    for ret, name, series, s, book in tested:
        rets = [float(t["ret_pct"]) for t in by_bot.get(name, [])]
        p = M.permutation_pvalue(rets, control_rets)
        mdd = M.max_drawdown([book["start_cash"], *series])
        has = s.n > 0
        g = [s.n >= CRYPTO_GATES["min_trades"], days >= CRYPTO_GATES["min_days"], has and s.total_pnl > 0,
             has and s.stressed_pnl > 0, s.n >= 2 and s.ci_low_pct > 0,
             p == p and p < p_bar, has and ret > sol_ret, has and mdd < CRYPTO_GATES["max_drawdown_pct"]]
        verdict = "**CANDIDATE**" if all(g) else ("collecting data" if not (g[0] and g[1]) else "no proven edge")
        L.append(f"| `{name}` | " + " | ".join(_ok(x) for x in g) + f" | {verdict} |")
    L += ["", "_Coin-flip test = permutation test of per-trade returns vs. `random_control` "
          f"(same tokens, exits and size, random entries). ✅ needs p < {p_bar:.3f}: 0.05 split across "
          f"the {len(tested)} bots being tested, so one lucky bot out of several doesn't count as proof._", ""]

    exits = defaultdict(lambda: defaultdict(int))
    for t in trades:
        exits[t["bot"]][t["exit_reason"]] += 1
    if exits:
        L += ["<details><summary>How positions closed</summary>", "",
              "| Bot | " + " | ".join(REASONS) + " |", "|---|" + "---:|" * len(REASONS)]
        for b, r in sorted(exits.items()):
            L.append(f"| `{b}` | " + " | ".join(str(r.get(x, 0)) for x in REASONS) + " |")
        L += ["", "</details>", ""]

    ai = read_csv(f"{d}/ai_journal.csv")
    if ai or state.get("ai_enabled"):
        L += ["### Does Claude's judgment predict anything?", ""]
        L += _ai_section(ai)
    return L


REASONS = ["take_profit", "stop_loss", "trailing_stop", "time_exit", "liquidity_pulled", "vanished"]


def _seasons_note(state: dict) -> list[str]:
    past = state.get("seasons") or []
    if not past:
        return []
    out = [f"> **Season {state.get('season', 1)}.** All bots were reset with fresh paper money; "
           "gates and stats count this season only. Earlier seasons:"]
    for p in past:
        broke = [n for n, c in p["end_cash"].items() if c < 0.5 and n != "hold_sol"]
        out.append(f"> - Season {p['season']}: {(p['started_at'] or '?')[:10]} to {(p['ended_at'] or '?')[:10]}, "
                   f"${p['start_cash']:.0f} per bot" + (f"; ended with {', '.join(f'`{b}`' for b in broke)} out of money"
                   if broke else "") + f". Archived in `{p['archive']}/`.")
    return out + [""]


def CRYPTO_START(state: dict) -> float:
    books = list(state["bots"].values())
    return books[0]["start_cash"] if books else 0.0


def _ai_section(ai: list[dict]) -> list[str]:
    if not ai:
        return ["_Scores logged; forward returns appear after 4 hours._", ""]
    L = ["| Claude score | Tokens scored | Avg return 1h later | Avg return 4h later |", "|---|---:|---:|---:|"]
    for lo, hi, label in ((0, 3, "0-3 (avoid)"), (4, 6, "4-6 (coin flip)"), (7, 10, "7-10 (buy)")):
        grp = [r for r in ai if lo <= int(r["score"]) <= hi]
        r1 = [float(r["ret_60m"]) for r in grp if r.get("ret_60m") not in (None, "")]
        r4 = [float(r["ret_240m"]) for r in grp if r.get("ret_240m") not in (None, "")]
        L.append(f"| {label} | {len(grp)} | {M.fmt(st.mean(r1), 1, '%') if r1 else '–'} | "
                 f"{M.fmt(st.mean(r4), 1, '%') if r4 else '–'} |")
    L += ["", "_If the 7-10 row doesn't clearly beat the 0-3 row after a few hundred scores, the AI adds nothing._", ""]
    return L


# ------------------------------------------------------------------ stocks
def stocks_section(d: str) -> list[str]:
    state = load_json(f"{d}/state.json", None)
    L = ["## Stocks & ETFs — live paper trading (daily)", ""]
    if not state or not state.get("runs"):
        return L + ["_No runs yet. Needs Alpaca paper keys; see README._", ""]
    rows = read_csv(f"{d}/equity.csv")
    eq = _series(rows, "bot")
    trades = read_csv(f"{d}/trades.csv")
    by_bot: dict[str, list[dict]] = defaultdict(list)
    for t in trades:
        by_bot[t["bot"]].append(t)
    days = state["runs"]
    spy = eq.get("buy_hold_spy", [])
    spy_ret = (spy[-1] / state["books"]["buy_hold_spy"]["start_cash"] - 1) * 100 if spy else 0.0
    spy_mdd = M.max_drawdown([state["books"]["buy_hold_spy"]["start_cash"], *spy]) if spy else 0.0
    spy_sharpe = M.sharpe(M.period_returns(spy), 252)
    L += [f"Running **{days} trading days** since {state['started_at']} · each strategy started with "
          f"${list(state['books'].values())[0]['start_cash']:,.0f} (virtual)", "",
          "| Strategy | Equity | Return | Sharpe | Max DD | Trades | Win % | Holding now |",
          "|---|---:|---:|---:|---:|---:|---:|---|"]
    gate_rows = []
    for name, book in sorted(state["books"].items(), key=lambda kv: -(eq.get(kv[0]) or [0])[-1]):
        series = eq.get(name, [book["start_cash"]])
        ret = (series[-1] / book["start_cash"] - 1) * 100
        sh = M.sharpe(M.period_returns(series), 252)
        mdd = M.max_drawdown([book["start_cash"], *series])
        s = M.trade_stats(by_bot.get(name, []))
        L.append(f"| `{name}` | ${series[-1]:,.0f} | {ret:+.1f}% | {sh:.2f} | {mdd:.1f}% | {s.n} | "
                 f"{M.fmt(s.win_rate, 0)} | {', '.join(book['positions']) or 'cash'} |")
        if name not in ("buy_hold_spy", "random_control"):
            gate_rows.append((name, days >= STOCK_GATES["min_days"], sh > spy_sharpe, ret > 0,
                              mdd <= spy_mdd * STOCK_GATES["max_dd_vs_spy"] + 0.5))
    L += ["", "### Real-money gates (forward test; backtest must also pass, see BACKTEST.md)", "",
          "| Strategy | 6+ months live | Better risk-adjusted return than SPY (Sharpe) | Profitable | Drawdown ≤ SPY's | Verdict |",
          "|---|:-:|:-:|:-:|:-:|---|"]
    for name, *g in gate_rows:
        v = "**CANDIDATE**" if all(g) else ("collecting data" if not g[0] else "not better than SPY")
        L.append(f"| `{name}` | " + " | ".join(_ok(x) for x in g) + f" | {v} |")
    L += ["", f"_SPY over the same period: {spy_ret:+.1f}%, Sharpe {spy_sharpe:.2f}, max drawdown {spy_mdd:.1f}%._", ""]
    return L


def write_report(crypto_dir: str = "data/crypto", stocks_dir: str = "data/stocks", out: str = "REPORT.md",
                 demo: bool = False) -> None:
    L = ["# Quant Lab report", "",
         f"_Updated {utcnow().strftime('%Y-%m-%d %H:%M UTC')} · paper money only._", ""]
    if demo:
        L += ["> ⚠️ **DEMO on a simulated market.** These numbers only prove the software works. "
              "They say nothing about real performance.", ""]
    L += crypto_section(crypto_dir)
    L += stocks_section(stocks_dir)
    if os.path.exists("BACKTEST.md") and not demo:
        L += ["## Backtests", "", "See [BACKTEST.md](BACKTEST.md) for 2016-present stock backtests.", ""]
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
