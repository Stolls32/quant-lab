"""Rug-pull and honeypot screen applied before ANY bot (including the random
control) may buy a token. Most meme coins die; this removes the most obvious
traps so the experiment measures strategy skill, not scam exposure.

It is a screen, not a guarantee: a token can pass every check and still be
rugged an hour later. That's why the engine also force-exits on liquidity
pulls and closes vanished tokens at $0.
"""
from __future__ import annotations

from .config import SafetyConfig
from .market import Snapshot


def check(s: Snapshot, cfg: SafetyConfig) -> str | None:
    """Returns None if the token is tradable, otherwise the reason it isn't."""
    if s.symbol.upper() in cfg.exclude_symbols:
        return "excluded"
    if s.price <= 0:
        return "no_price"
    if s.liquidity < cfg.min_liquidity_usd:
        return "low_liquidity"
    if s.age_min < cfg.min_age_min:
        return "too_new"
    if s.s("h1") < cfg.min_sells_h1:
        return "few_sellers"  # possible honeypot: buys work, sells don't
    if s.s("h1") < cfg.min_sell_buy_ratio_h1 * max(1, s.b("h1")):
        return "one_sided_flow"
    if s.fdv > 0 and s.fdv / max(1.0, s.liquidity) > cfg.max_fdv_to_liquidity:
        return "thin_vs_valuation"
    if abs(s.c("m5")) > cfg.max_abs_change_m5_pct:
        return "vertical_candle"
    return None
