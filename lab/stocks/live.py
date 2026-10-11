"""Daily live paper-trading run for the stock strategies.

Runs once per trading day, shortly after the open (~10:05am New York):
  1. completed daily bars through yesterday  -> each strategy's signals
  2. live quotes right now                   -> simulated fills (mid + slippage)
  3. optional: mirror ONE strategy into the real Alpaca paper account, with
     real orders and real fills. That's the dress rehearsal for live money.

Live-money guard: if ALPACA_BASE_URL points at a live (non-paper) account,
orders are refused unless LIVE_TRADING_CONFIRM is set to the exact phrase
below. Alpaca live accounts require an adult account holder; that call belongs
to whoever owns the account.
"""
from __future__ import annotations

import logging
import os
from datetime import date, datetime, timedelta

from ..util import append_csv, iso, load_json, save_json_atomic, utcnow
from .data import Alpaca
from .engine import StockCosts, age_positions, book_equity, holdings_view, new_book, rebalance
from .strategies import Ctx, all_strategies, full_universe

log = logging.getLogger("lab.stocks")

LIVE_PHRASE = "I accept real-money risk"
TRADE_FIELDS = ["closed_at", "bot", "symbol", "entry_at", "hold_days", "entry_px", "exit_px",
                "usd_in", "usd_out", "pnl_usd", "ret_pct", "cost_usd", "exit_reason"]
EQUITY_FIELDS = ["date", "bot", "equity", "cash", "positions"]


class StockLab:
    def __init__(self, data_dir: str, broker: Alpaca, start_cash: float = 10_000.0,
                 costs: StockCosts | None = None, strategies=None):
        self.dir = data_dir
        self.broker = broker
        self.costs = costs or StockCosts()
        self.strats = strategies or all_strategies()
        self.state_path = f"{data_dir}/state.json"
        self.state = load_json(self.state_path, {"books": {}, "last_run_date": None, "started_at": None, "runs": 0})
        for s in self.strats:
            self.state["books"].setdefault(s.name, new_book(start_cash))

    def run(self, force: bool = False, mirror: str | None = None) -> dict:
        clock = self.broker.clock()
        today = (clock.get("timestamp") or iso(utcnow()))[:10]
        if not clock.get("is_open") and not force:
            return {"skipped": "market closed"}
        if self.state.get("last_run_date") == today and not force:
            return {"skipped": "already ran today"}

        universe = full_universe()
        start = (date.fromisoformat(today) - timedelta(days=430)).isoformat()
        bars = self.broker.daily_bars(universe, start=start)
        closes = {s: [b.c for b in bs if b.date < today] for s, bs in bars.items()}
        # Today's bar is still forming during market hours: signals use completed bars only.
        last_bar = max((b.date for bs in bars.values() for b in bs if b.date < today), default=None)
        if not last_bar or not closes.get("SPY"):
            raise RuntimeError("no SPY history returned; check Alpaca keys/data access")
        fills = self._fill_prices(universe)

        summary = {"date": today, "signal_bar": last_bar, "trades": [], "equity": {}}
        all_closed, eq_rows = [], []
        for strat in self.strats:
            book = self.state["books"][strat.name]
            age_positions(book)
            view = {s: closes[s] for s in strat.universe if closes.get(s)}
            reb = today[:7] != last_bar[:7] or not book["positions"]
            tgt = strat.targets(Ctx(date=last_bar, closes=view, holdings=holdings_view(book), rebalance_day=reb))
            if tgt is not None:
                prices = {s: fills[s] for s in strat.universe if s in fills}
                closed = rebalance(book, tgt, prices, today, self.costs, strat.resize_existing, strat.name)
                all_closed += closed
                summary["trades"].append({strat.name: tgt})
            eq = book_equity(book, fills)
            summary["equity"][strat.name] = round(eq, 2)
            eq_rows.append({"date": today, "bot": strat.name, "equity": round(eq, 4), "cash": round(book["cash"], 4),
                            "positions": " ".join(f"{s}:{p['qty']:.4f}" for s, p in book["positions"].items())})
            if mirror == strat.name and tgt is not None:
                summary["mirror"] = self.mirror(tgt, fills)

        append_csv(f"{self.dir}/trades.csv", TRADE_FIELDS, all_closed)
        append_csv(f"{self.dir}/equity.csv", EQUITY_FIELDS, eq_rows)
        self.state["last_run_date"] = today
        self.state["started_at"] = self.state.get("started_at") or today
        self.state["runs"] = self.state.get("runs", 0) + 1
        save_json_atomic(self.state_path, self.state)
        return summary

    def _fill_prices(self, universe: list[str]) -> dict[str, float]:
        """Mid of the live bid/ask when the quote is sane, else last trade."""
        out = {}
        for sym, q in self.broker.quotes(universe).items():
            bid, ask, last = q["bid"], q["ask"], q["last"]
            if bid > 0 and ask > 0 and (ask - bid) / ask < 0.01:
                out[sym] = (bid + ask) / 2
            elif last > 0:
                out[sym] = last
        return out

    # ------------------------------------------------------------- mirror
    def mirror(self, targets: dict[str, float], fills: dict[str, float]) -> list[str]:
        """Make the real Alpaca account match one strategy's target weights."""
        b = self.broker
        if not b.is_paper and os.environ.get("LIVE_TRADING_CONFIRM") != LIVE_PHRASE:
            log.error("Refusing to place orders on a LIVE account without LIVE_TRADING_CONFIRM.")
            return ["refused: live account without confirmation"]
        acct = b.account()
        equity = float(acct.get("equity") or 0) * 0.98  # keep a small cash buffer
        held = {p["symbol"]: float(p.get("market_value") or 0) for p in b.positions()}
        actions = []
        for sym in held:
            if targets.get(sym, 0) <= 0:
                try:
                    b.close_position(sym)
                    actions.append(f"close {sym}")
                except Exception as e:  # noqa: BLE001 - log and continue
                    actions.append(f"close {sym} FAILED: {e}")
        for sym, w in targets.items():
            if w <= 0 or sym not in fills:
                continue
            diff = w * equity - held.get(sym, 0.0)
            if abs(diff) < max(5.0, 0.02 * equity):
                continue
            try:
                if diff > 0:
                    b.submit_order(sym, "buy", notional=diff)
                    actions.append(f"buy ${diff:,.2f} {sym}")
                else:
                    b.submit_order(sym, "sell", qty=-diff / fills[sym])
                    actions.append(f"sell ${-diff:,.2f} {sym}")
            except Exception as e:  # noqa: BLE001
                actions.append(f"{sym} order FAILED: {e}")
        log.info("mirror: %s", actions or "no changes")
        return actions
