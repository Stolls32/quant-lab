"""The meme-coin paper-trading engine. One call to `tick()` = one market check.

GitHub Actions calls this every ~5 minutes. Each tick:
  1. find tokens (new + promoted + trending + everything we're watching/holding)
  2. pull live snapshots for all of them
  3. run exits for every open position (stop, target, trailing, time, rug)
  4. screen tokens for safety, then let each bot pick entries
  5. log trades, mark equity, save state

Everything that matters is persisted in data/crypto/ so the bot has memory
between runs: open positions, price history, cooldowns, the AI budget.
"""
from __future__ import annotations

import logging
import time
from datetime import datetime, timezone

from ..ai import ClaudeScorer
from ..util import append_csv, iso, load_json, save_json_atomic
from . import safety
from .config import CostConfig, CryptoConfig
from .costs import DexCostModel
from .market import SOL_MINT, Snapshot
from .strategies import ClaudeAnalyst, Context, HoldSOL, Strategy, all_strategies

log = logging.getLogger("lab.crypto")

TRADE_FIELDS = ["closed_at", "bot", "symbol", "address", "entry_at", "hold_min", "entry_mid", "exit_mid",
                "usd_in", "usd_out", "pnl_usd", "ret_pct", "cost_usd", "exit_reason", "url"]
EQUITY_FIELDS = ["ts", "bot", "equity", "cash", "open_positions"]
AI_FIELDS = ["scored_at", "symbol", "address", "score", "reason", "bought", "price", "ret_60m", "ret_240m"]


class CryptoLab:
    def __init__(self, data_dir: str, market, cfg: CryptoConfig | None = None,
                 scorer: ClaudeScorer | None = None, strategies: list[Strategy] | None = None):
        self.dir = data_dir
        self.market = market
        self.cfg = cfg or CryptoConfig()
        self.costs = DexCostModel(self.cfg.costs)
        # SOL itself is extremely liquid: charging it meme-coin costs would make
        # the benchmark look worse than it is and flatter every bot against it.
        self.bench_costs = DexCostModel(CostConfig(fee_pct=0.3, latency_slip_pct=0.1, network_fee_usd=0.01))
        self.state_path = f"{data_dir}/state.json"
        self.state = load_json(self.state_path, {})
        self._init_state()
        self.bots = strategies or all_strategies()
        if not self.state.get("bench_costs_v2"):  # one-time: rebuy the benchmark at fair costs
            self.state["bots"].pop("hold_sol", None)
            self.state["bench_costs_v2"] = True
        for b in self.bots:
            self.state["bots"].setdefault(b.name, self._new_book())
        self.scorer = scorer or ClaudeScorer(self.cfg.ai.model, self.cfg.ai.max_calls_per_day,
                                             self.state["ai_usage"])
        self.scorer.usage = self.state["ai_usage"]

    # ------------------------------------------------------------------ state
    def _init_state(self) -> None:
        s = self.state
        s.setdefault("version", 1)
        s.setdefault("started_at", None)
        s.setdefault("ticks", 0)
        s.setdefault("watch", {})
        s.setdefault("hist", {})
        s.setdefault("missing", {})
        s.setdefault("bots", {})
        s.setdefault("ai_usage", {})
        s.setdefault("ai_pending", [])
        s.setdefault("last_equity_log", 0)

    def _new_book(self) -> dict:
        c = self.cfg.engine.start_cash_usd
        return {"cash": c, "start_cash": c, "positions": {}, "last_entry": {}}

    def save(self) -> None:
        save_json_atomic(self.state_path, self.state)

    # ------------------------------------------------------------------- tick
    def tick(self, now: float | None = None) -> dict:
        now = now or time.time()
        now_iso = iso(datetime.fromtimestamp(now, timezone.utc))
        st = self.state
        st["started_at"] = st["started_at"] or now_iso
        st["ticks"] += 1
        st["last_tick"] = now_iso
        st["ai_enabled"] = self.scorer.enabled
        ecfg = self.cfg.engine

        # 1) universe
        discovered = self.market.discover()
        for a in discovered:
            st["watch"][a] = now
        horizon = now - ecfg.watch_hours * 3600
        st["watch"] = dict(sorted(((a, t) for a, t in st["watch"].items() if t >= horizon),
                                  key=lambda kv: kv[1], reverse=True)[:ecfg.max_watchlist])
        held = {a for b in st["bots"].values() for a in b["positions"]}
        pending = {p["address"] for p in st["ai_pending"]}
        universe = [SOL_MINT, *held, *pending, *st["watch"].keys()]

        # 2) data
        snaps: dict[str, Snapshot] = self.market.snapshots(universe)
        if SOL_MINT not in snaps:
            # SOL always trades, so no SOL means a data outage, not dead tokens.
            # Do nothing rather than mistake an outage for a wave of rug pulls.
            st.setdefault("recent_events", []).append({"ts": now_iso, "outage": True, "discovered": len(discovered),
                                                       "snapshots": 0, "safe": 0, "opened": [], "closed": []})
            del st["recent_events"][:-80]
            self.save()
            return {"discovered": len(discovered), "universe": len(set(universe)), "snapshots": 0,
                    "closed": [], "opened": [], "ai_scored": 0, "outage": True}
        failed = getattr(self.market, "last_failed", set())
        for a in set(universe):
            if a in failed:
                continue
            if a in snaps:
                st["missing"].pop(a, None)
                h = st["hist"].setdefault(a, [])
                h.append([now, snaps[a].price, snaps[a].liquidity])
                del h[:-ecfg.history_points]
            else:
                st["missing"][a] = st["missing"].get(a, 0) + 1
        keep = set(universe)
        st["hist"] = {a: h for a, h in st["hist"].items() if a in keep}
        st["missing"] = {a: n for a, n in st["missing"].items() if a in keep}

        events = {"discovered": len(discovered), "universe": len(set(universe)), "snapshots": len(snaps),
                  "closed": [], "opened": [], "ai_scored": 0}

        # 3) exits
        trades = []
        for bot in self.bots:
            trades += self._run_exits(bot, snaps, now, now_iso)
        events["closed"] = [f"{t['bot']}:{t['symbol']}:{t['exit_reason']}:{t['ret_pct']}%" for t in trades]

        # 4) entries
        sol = snaps.get(SOL_MINT)
        candidates = []
        for a, s in snaps.items():
            if a == SOL_MINT or safety.check(s, self.cfg.safety):
                continue
            candidates.append(Context(snap=s, history=st["hist"].get(a, []), now_ts=now))
        events["safe_candidates"] = len(candidates)

        for bot in self.bots:
            book = st["bots"][bot.name]
            if isinstance(bot, HoldSOL):
                if not book["positions"] and sol and book["cash"] > ecfg.min_trade_usd:
                    self._open(bot, book, sol, book["cash"], now, now_iso, events)
                continue
            if hasattr(bot, "reseed"):
                bot.reseed(int(now // 60))
            if not bot.wants_to_trade_now() or len(book["positions"]) >= bot.max_positions:
                continue
            eligible = [c for c in candidates if self._can_enter(bot, book, c.snap.address, now)]
            scored = [(sc, c) for c in eligible if (sc := bot.score(c)) is not None]
            scored.sort(key=lambda x: x[0], reverse=True)
            if isinstance(bot, ClaudeAnalyst):
                scored = self._ai_filter(scored, now, now_iso, events)
            if scored:
                pick = scored[0][1].snap
                size = min(book["cash"], book["start_cash"] * bot.size_frac)
                if size >= ecfg.min_trade_usd:
                    self._open(bot, book, pick, size, now, now_iso, events)

        # what the scanner saw this tick (for the dashboard's radar)
        top = sorted(candidates, key=lambda c: c.snap.v("m5"), reverse=True)[:15]
        st["last_scan"] = [{
            "symbol": c.snap.symbol, "address": c.snap.address, "price": c.snap.price,
            "liq": round(c.snap.liquidity), "age_h": round(c.snap.age_min / 60, 1),
            "m5": c.snap.c("m5"), "h1": c.snap.c("h1"), "h24": c.snap.c("h24"), "vol_m5": round(c.snap.v("m5")),
            "buys_m5": c.snap.b("m5"), "sells_m5": c.snap.s("m5"), "url": c.snap.url,
        } for c in top]
        st.setdefault("recent_events", []).append({
            "ts": now_iso, "discovered": events["discovered"], "snapshots": len(snaps),
            "safe": len(candidates), "opened": events["opened"], "closed": events["closed"],
            "ai_scored": events["ai_scored"],
        })
        del st["recent_events"][:-80]

        # 5) AI forward-return journal
        self._update_ai_journal(snaps, now)

        # 6) equity log
        if now - st["last_equity_log"] >= ecfg.equity_log_minutes * 60:
            st["last_equity_log"] = now
            rows = []
            for bot in self.bots:
                book = st["bots"][bot.name]
                rows.append({"ts": now_iso, "bot": bot.name, "equity": round(self.equity(book, snaps, self.bench_costs if bot.is_benchmark else None), 6),
                             "cash": round(book["cash"], 6), "open_positions": len(book["positions"])})
            append_csv(f"{self.dir}/equity.csv", EQUITY_FIELDS, rows)

        self.save()
        return events

    # ------------------------------------------------------------ positions
    def _can_enter(self, bot: Strategy, book: dict, addr: str, now: float) -> bool:
        if addr in book["positions"]:
            return False
        last = book["last_entry"].get(addr)
        return not (last and now - last < bot.cooldown_min * 60)

    def _open(self, bot: Strategy, book: dict, s: Snapshot, usd: float, now: float, now_iso: str, events: dict):
        fill = (self.bench_costs if bot.is_benchmark else self.costs).buy(s.price, usd, s.liquidity)
        if not fill or fill.qty <= 0:
            return
        book["cash"] -= usd
        book["positions"][s.address] = {
            "symbol": s.symbol, "qty": fill.qty, "entry_mid": s.price, "entry_ts": now, "entry_at": now_iso,
            "usd_in": usd, "buy_cost": fill.cost_usd, "entry_liq": s.liquidity, "peak": s.price, "url": s.url,
        }
        book["last_entry"][s.address] = now
        # forget old cooldowns so the state file doesn't grow forever
        book["last_entry"] = {a: t for a, t in book["last_entry"].items() if now - t < 7 * 86400}
        events["opened"].append(f"{bot.name}:{s.symbol}:${usd:.2f}")
        log.info("OPEN  %-14s %-12s $%.2f @ %.8g (liq $%.0f)", bot.name, s.symbol, usd, s.price, s.liquidity)

    def _run_exits(self, bot: Strategy, snaps: dict, now: float, now_iso: str) -> list[dict]:
        if bot.is_benchmark:
            return []
        st = self.state
        book = st["bots"][bot.name]
        ex = bot.exits
        closed = []
        for addr, pos in list(book["positions"].items()):
            s = snaps.get(addr)
            reason, mid, liq = None, 0.0, 0.0
            if s is None:
                if st["missing"].get(addr, 0) >= self.cfg.engine.vanish_ticks:
                    reason = "vanished"  # closed at $0
                else:
                    continue
            else:
                mid, liq = s.price, s.liquidity
                pos["peak"] = max(pos["peak"], mid)
                ret = (mid / pos["entry_mid"] - 1) * 100
                peak_ret = (pos["peak"] / pos["entry_mid"] - 1) * 100
                held_min = (now - pos["entry_ts"]) / 60
                if liq < pos["entry_liq"] * (1 - self.cfg.engine.rug_liquidity_drop):
                    reason = "liquidity_pulled"
                elif ret <= -ex.stop_loss_pct:
                    reason = "stop_loss"
                elif ret >= ex.take_profit_pct:
                    reason = "take_profit"
                elif peak_ret >= ex.trail_arm_pct and mid <= pos["peak"] * (1 - ex.trail_pct / 100):
                    reason = "trailing_stop"
                elif held_min >= ex.max_hold_min:
                    reason = "time_exit"
            if not reason:
                continue
            fill = self.costs.sell(mid, pos["qty"], liq)
            book["cash"] += fill.usd
            del book["positions"][addr]
            pnl = fill.usd - pos["usd_in"]
            t = {
                "closed_at": now_iso, "bot": bot.name, "symbol": pos["symbol"], "address": addr,
                "entry_at": pos["entry_at"], "hold_min": round((now - pos["entry_ts"]) / 60, 1),
                "entry_mid": f"{pos['entry_mid']:.10g}", "exit_mid": f"{mid:.10g}",
                "usd_in": round(pos["usd_in"], 6), "usd_out": round(fill.usd, 6), "pnl_usd": round(pnl, 6),
                "ret_pct": round(pnl / pos["usd_in"] * 100, 3),
                "cost_usd": round(pos["buy_cost"] + fill.cost_usd, 6) if mid > 0 else round(pos["buy_cost"], 6),
                "exit_reason": reason, "url": pos.get("url", ""),
            }
            closed.append(t)
            log.info("CLOSE %-14s %-12s %-16s %+.1f%%", bot.name, pos["symbol"], reason, t["ret_pct"])
        append_csv(f"{self.dir}/trades.csv", TRADE_FIELDS, closed)
        return closed

    def equity(self, book: dict, snaps: dict, costs: DexCostModel | None = None) -> float:
        """Cash + what the positions would fetch if sold now, after costs."""
        costs = costs or self.costs
        total = book["cash"]
        for addr, pos in book["positions"].items():
            s = snaps.get(addr)
            if s:
                total += costs.sell(s.price, pos["qty"], s.liquidity).usd
            else:
                h = self.state["hist"].get(addr)
                if h:
                    total += costs.sell(h[-1][1], pos["qty"], h[-1][2]).usd
        return total

    # ------------------------------------------------------------------- AI
    def _ai_filter(self, scored: list, now: float, now_iso: str, events: dict) -> list:
        if not self.scorer.enabled:
            return []
        today = now_iso[:10]
        # Pace the daily budget across the whole day instead of burning it by
        # breakfast, and don't re-ask about a token scored in the last hour.
        day_frac = (now % 86400) / 86400
        self.scorer.budget_left(today)
        allowed = int(self.cfg.ai.max_calls_per_day * day_frac) + 5 - self.state["ai_usage"].get("calls", 0)
        recent = {p["address"] for p in self.state["ai_pending"] if now - p["ts"] < 3600}
        fresh = [(sc, c) for sc, c in scored if c.snap.address not in recent]
        out = []
        for _, ctx in fresh[: max(0, min(self.cfg.ai.max_calls_per_tick, allowed))]:
            res = self.scorer.score(ctx.snap.to_brief(), [p for _, p, _ in ctx.history], today)
            if res is None:
                continue
            score, reason = res
            events["ai_scored"] += 1
            self.state["ai_pending"].append({
                "scored_at": now_iso, "ts": now, "symbol": ctx.snap.symbol, "address": ctx.snap.address,
                "score": score, "reason": reason, "price": ctx.snap.price, "bought": False,
            })
            if score >= self.cfg.ai.buy_threshold:
                out.append((score, ctx))
        out.sort(key=lambda x: x[0], reverse=True)
        if out:  # mark the one that will be bought
            for p in reversed(self.state["ai_pending"]):
                if p["address"] == out[0][1].snap.address:
                    p["bought"] = True
                    break
        return out

    def _update_ai_journal(self, snaps: dict, now: float) -> None:
        horizons = self.cfg.ai.eval_horizons_min
        still, done = [], []
        for p in self.state["ai_pending"]:
            age = (now - p["ts"]) / 60
            s = snaps.get(p["address"])
            for h in horizons:
                key = f"ret_{h}m"
                if key not in p and age >= h:
                    if s:
                        p[key] = round((s.price / p["price"] - 1) * 100, 2)
                    elif self.state["missing"].get(p["address"], 0) >= self.cfg.engine.vanish_ticks:
                        p[key] = -100.0
            if all(f"ret_{h}m" in p for h in horizons) or age > max(horizons) + 120:
                done.append(p)
            else:
                still.append(p)
        self.state["ai_pending"] = still
        append_csv(f"{self.dir}/ai_journal.csv", AI_FIELDS, done)
