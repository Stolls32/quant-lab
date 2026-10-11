"""Portfolio accounting for the stock strategies, shared by backtest and live.

Each strategy gets its own virtual book (cash + positions). `rebalance()`
turns target weights into trades, charging slippage on every fill, and logs a
completed trade whenever a position is fully closed.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class StockCosts:
    # Per-side cost in basis points (1 bp = 0.01%). Liquid ETFs trade with
    # ~1-2bp spreads; 5bp per side also absorbs a little market impact.
    # Commissions are $0 at Alpaca/Schwab for stocks & ETFs.
    slippage_bps: float = 5.0
    min_trade_usd: float = 1.0


def new_book(cash: float) -> dict:
    return {"cash": cash, "start_cash": cash, "positions": {}}


def book_equity(book: dict, marks: dict[str, float]) -> float:
    return book["cash"] + sum(p["qty"] * marks.get(s, p["last_mark"]) for s, p in book["positions"].items())


def age_positions(book: dict) -> None:
    """Call once per trading day before asking the strategy for targets."""
    for p in book["positions"].values():
        p["bars_held"] += 1


def holdings_view(book: dict) -> dict[str, dict]:
    return {s: {"entry_date": p["entry_date"], "bars_held": p["bars_held"]} for s, p in book["positions"].items()}


def rebalance(book: dict, targets: dict[str, float], fills: dict[str, float], date: str,
              costs: StockCosts, resize_existing: bool, strategy: str) -> list[dict]:
    """Move the book toward `targets` at `fills` prices (mid). Returns closed trades.

    Sells first (to free cash), then buys. Fractional shares are allowed, as at
    Alpaca. Positions already held are left alone unless `resize_existing`.
    """
    bps = costs.slippage_bps / 10_000
    for s, p in book["positions"].items():
        if s in fills:
            p["last_mark"] = fills[s]
    equity = book_equity(book, fills)
    closed: list[dict] = []

    # --- sells
    for sym in list(book["positions"]):
        pos = book["positions"][sym]
        w = targets.get(sym, 0.0)
        px = fills.get(sym)
        if px is None:
            continue  # no price today: can't trade it, keep holding
        if w <= 0:
            qty = pos["qty"]
        elif resize_existing:
            excess = pos["qty"] * px - w * equity
            if excess < max(costs.min_trade_usd, 0.02 * equity):
                continue
            qty = excess / px
        else:
            continue
        proceeds = qty * px * (1 - bps)
        friction = qty * px * bps
        frac = qty / pos["qty"]
        basis = pos["cost_usd"] * frac
        book["cash"] += proceeds
        pos["realized"] += proceeds - basis
        pos["frictions"] += friction
        pos["proceeds"] += proceeds
        pos["qty"] -= qty
        pos["cost_usd"] -= basis
        if pos["qty"] <= 1e-9 or w <= 0:
            invested = pos["invested"]
            pnl = pos["realized"]
            closed.append({
                "closed_at": date, "bot": strategy, "symbol": sym, "entry_at": pos["entry_date"],
                "hold_days": pos["bars_held"], "entry_px": round(pos["entry_px"], 4), "exit_px": round(px, 4),
                "usd_in": round(invested, 4), "usd_out": round(pos["proceeds"], 4), "pnl_usd": round(pnl, 4),
                "ret_pct": round(pnl / invested * 100, 4) if invested else 0.0,
                "cost_usd": round(pos["frictions"], 4), "exit_reason": "signal",
            })
            del book["positions"][sym]

    # --- buys
    equity = book_equity(book, fills)
    for sym, w in sorted(targets.items(), key=lambda kv: -kv[1]):
        if w <= 0 or sym not in fills:
            continue
        px = fills[sym]
        held = book["positions"].get(sym)
        if held and not resize_existing:
            continue
        cur = held["qty"] * px if held else 0.0
        want = w * equity - cur
        usd = min(want, book["cash"])
        if usd < max(costs.min_trade_usd, (0.02 * equity) if held else 0):
            continue
        qty = usd * (1 - bps) / px
        book["cash"] -= usd
        if held:
            held["qty"] += qty
            held["cost_usd"] += usd
            held["invested"] += usd
            held["frictions"] += usd * bps
        else:
            book["positions"][sym] = {
                "qty": qty, "cost_usd": usd, "invested": usd, "entry_px": px, "entry_date": date,
                "bars_held": 0, "realized": 0.0, "frictions": usd * bps, "proceeds": 0.0, "last_mark": px,
            }
    return closed
