"""Writes data/dashboard.json: everything the live dashboard (docs/index.html)
needs, in one small file the page re-downloads every minute."""
from __future__ import annotations

import os
from collections import defaultdict

from . import metrics as M
from .report import CRYPTO_GATES
from .util import iso, load_json, parse_iso, read_csv, save_json_atomic, utcnow

DESCRIPTIONS = {
    "momentum": "Rides tokens breaking out with real volume and more buyers than sellers.",
    "dip_reclaim": "Buys hard pullbacks in tokens that are up on the day, once they bounce.",
    "fresh_launch": "Snipes brand-new pools with strong early buying. Highest risk.",
    "volume_spike": "Jumps on sudden bursts of volume while price ticks up.",
    "claude_analyst": "Claude scores each setup 0-10 and only buys the strong ones.",
    "random_control": "The coin flip. Random entries, same exits. Everyone must beat this.",
    "hold_sol": "Benchmark: bought SOL once and holds it.",
}


def _thin(ser: list, n: int = 400) -> list:
    """Downsample a [[ts, value], ...] series to about n points, keeping the last."""
    if len(ser) <= n:
        return ser
    k = len(ser) / n
    out = [ser[int(i * k)] for i in range(n)]
    if out[-1] is not ser[-1]:
        out.append(ser[-1])
    return out


def _num(x, d=4):
    try:
        v = float(x)
        return None if v != v or v in (float("inf"), float("-inf")) else round(v, d)
    except (TypeError, ValueError):
        return None


def build(crypto_dir: str = "data/crypto", stocks_dir: str = "data/stocks") -> dict:
    st = load_json(f"{crypto_dir}/state.json", None)
    out: dict = {"generated_at": iso(utcnow()), "crypto": None, "stocks": None}
    if st:
        trades = read_csv(f"{crypto_dir}/trades.csv")
        by_bot = defaultdict(list)
        for t in trades:
            by_bot[t["bot"]].append(t)
        eq_rows = read_csv(f"{crypto_dir}/equity.csv")
        series = defaultdict(list)
        for r in eq_rows:
            series[r["bot"]].append([r["ts"], float(r["equity"])])
        started = parse_iso(st["started_at"])
        last = parse_iso(st.get("last_tick") or st["started_at"])
        days = (last - started).total_seconds() / 86400
        control = [float(t["ret_pct"]) for t in by_bot.get("random_control", [])]
        tested = [n for n in st["bots"] if n not in ("hold_sol", "random_control")]
        p_bar = CRYPTO_GATES["control_p_value"] / max(1, len(tested))
        hist = st.get("hist", {})

        def last_px(a):
            h = hist.get(a)
            return h[-1][1] if h else None

        sol_eq = series.get("hold_sol", [[0, 10.0]])[-1][1]
        sol_ret = (sol_eq / st["bots"].get("hold_sol", {"start_cash": 10})["start_cash"] - 1) * 100
        bots = []
        for name, book in st["bots"].items():
            s = M.trade_stats(by_bot.get(name, []))
            ser = series.get(name) or [[st["started_at"], book["start_cash"]]]
            eq = ser[-1][1]
            ret = (eq / book["start_cash"] - 1) * 100
            mdd = M.max_drawdown([book["start_cash"], *[v for _, v in ser]])
            positions = []
            for a, p in book["positions"].items():
                cur = last_px(a) or p["entry_mid"]
                positions.append({"symbol": p["symbol"], "entry": p["entry_mid"], "price": cur,
                                  "ret_pct": _num((cur / p["entry_mid"] - 1) * 100, 2), "usd_in": _num(p["usd_in"], 2),
                                  "since": p.get("entry_at"), "url": p.get("url", "")})
            gates = None
            if name in tested:
                rets = [float(t["ret_pct"]) for t in by_bot.get(name, [])]
                pv = M.permutation_pvalue(rets, control)
                has = s.n > 0  # no trades = nothing proven, so no green lights yet
                gates = [
                    ["100+ trades", s.n >= CRYPTO_GATES["min_trades"], f"{s.n}/100"],
                    ["30+ days", days >= CRYPTO_GATES["min_days"], f"{days:.1f}/30"],
                    ["Profitable", has and s.total_pnl > 0, f"${s.total_pnl:+.2f}"],
                    ["Survives 2x costs", has and s.stressed_pnl > 0, f"${s.stressed_pnl:+.2f}"],
                    ["Edge CI > 0", s.n >= 2 and s.ci_low_pct > 0, f"{M.fmt(s.ci_low_pct, 1)}%"],
                    ["Beats coin flip", pv == pv and pv < p_bar, f"p={M.fmt(pv, 3)}"],
                    ["Beats SOL", has and ret > sol_ret, f"{ret:+.1f}% vs {sol_ret:+.1f}%"],
                    ["Drawdown < 40%", has and mdd < CRYPTO_GATES["max_drawdown_pct"], f"{mdd:.1f}%"],
                ]
            verdict = None
            if gates:
                verdict = "CANDIDATE" if all(g[1] for g in gates) else (
                    "COLLECTING DATA" if not (gates[0][1] and gates[1][1]) else "NO PROVEN EDGE")
            bots.append({
                "name": name, "description": DESCRIPTIONS.get(name, ""), "equity": _num(eq, 4),
                "start": book["start_cash"], "return_pct": _num(ret, 2), "cash": _num(book["cash"], 4),
                "trades": s.n, "win_rate": _num(s.win_rate, 1), "avg_win": _num(s.avg_win_pct, 2),
                "avg_loss": _num(s.avg_loss_pct, 2), "mean_ret": _num(s.mean_ret_pct, 2),
                "ci": [_num(s.ci_low_pct, 2), _num(s.ci_high_pct, 2)], "profit_factor": _num(s.profit_factor, 2),
                "max_dd": _num(mdd, 2), "positions": positions, "gates": gates, "verdict": verdict,
                "series": [[t, round(v, 4)] for t, v in _thin(ser)],
                "role": "benchmark" if name == "hold_sol" else "control" if name == "random_control" else "bot",
                "enabled": not (name == "claude_analyst" and not st.get("ai_enabled")),
            })
        bots.sort(key=lambda b: b["return_pct"] or 0, reverse=True)
        ai = read_csv(f"{crypto_dir}/ai_journal.csv")
        ai_groups = []
        for lo, hi, label in ((0, 3, "0-3"), (4, 6, "4-6"), (7, 10, "7-10")):
            g = [r for r in ai if lo <= int(r["score"]) <= hi]
            r4 = [float(r["ret_240m"]) for r in g if r.get("ret_240m") not in (None, "")]
            ai_groups.append({"label": label, "n": len(g), "avg_4h": _num(sum(r4) / len(r4), 2) if r4 else None})
        out["crypto"] = {
            "started_at": st["started_at"], "last_tick": st.get("last_tick"), "ticks": st["ticks"],
            "days": _num(days, 2), "watching": len(st.get("watch", {})), "bots": bots,
            "recent_trades": [{k: t[k] for k in ("closed_at", "bot", "symbol", "ret_pct", "pnl_usd", "exit_reason",
                                                   "hold_min", "url")} for t in trades[-60:]][::-1],
            "events": st.get("recent_events", [])[-40:][::-1], "scan": st.get("last_scan", []),
            "ai": {"enabled": bool(st.get("ai_enabled")), "groups": ai_groups,
                   "calls_today": st.get("ai_usage", {}).get("calls", 0)},
            "p_bar": p_bar,
        }
    ss = load_json(f"{stocks_dir}/state.json", None)
    if ss and ss.get("runs"):
        rows = read_csv(f"{stocks_dir}/equity.csv")
        series = defaultdict(list)
        for r in rows:
            series[r["bot"]].append([r["date"], float(r["equity"])])
        out["stocks"] = {"started_at": ss.get("started_at"), "runs": ss["runs"], "strategies": [
            {"name": n, "equity": _num(series[n][-1][1], 2) if series.get(n) else b["start_cash"],
             "return_pct": _num((series[n][-1][1] / b["start_cash"] - 1) * 100, 2) if series.get(n) else 0,
             "holding": list(b["positions"]), "series": _thin(series.get(n, []))}
            for n, b in ss["books"].items()]}
    return out


def write(path: str = "data/dashboard.json", **kw) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    save_json_atomic(path, build(**kw))
