"""Every tunable number for the meme-coin side, in one place.

Change values here, never inside strategy code, so every bot is compared on the
same rules. If you change a cost or safety setting mid-experiment, note the date:
results before and after are no longer comparable.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class CostConfig:
    # Fee charged by the venue/aggregator on each side, in percent.
    # Conservative on purpose: in-app DEX trading and aggregators commonly
    # charge around 0.5-1%+ per swap. Check the real fee before Phase 3.
    fee_pct: float = 1.0
    # Extra slippage per side from the price moving between "signal" and
    # "filled" (latency, other bots front-running, priority fees). 5-minute
    # polling makes this worse, so it's set high.
    latency_slip_pct: float = 1.5
    # Constant-product AMM price impact ~= 2 x trade size / pool liquidity.
    impact_mult: float = 2.0
    max_impact_pct: float = 90.0
    # Solana network + priority fee per transaction, in USD.
    network_fee_usd: float = 0.01


@dataclass
class SafetyConfig:
    min_liquidity_usd: float = 20_000
    min_age_min: float = 10
    # Honeypot screen: a token where nobody is selling may be unsellable.
    min_sells_h1: int = 5
    min_sell_buy_ratio_h1: float = 0.15
    # FDV far above pool liquidity = a price that can't be exited in size.
    max_fdv_to_liquidity: float = 60.0
    # Don't chase a single 5-minute candle that's already gone vertical.
    max_abs_change_m5_pct: float = 60.0
    # Tokens we never treat as meme coins.
    exclude_symbols: tuple = ("SOL", "WSOL", "USDC", "USDT", "JUP", "JITOSOL", "MSOL", "BSOL")


@dataclass
class EngineConfig:
    start_cash_usd: float = 100.0         # each bot starts with this
    # Bump to start a new "season": every bot (benchmarks included) gets a fresh
    # book, and the old trades/equity/journal are archived to
    # data/crypto/archive/season-N/ so gates only count the current season.
    # Season 1 (2026-10-11 to 2026-10-28) ran on $10 per bot.
    season: int = 2
    min_trade_usd: float = 0.50
    # Price/liquidity history kept per token (one point per tick).
    history_points: int = 72               # ~6h at 5-minute ticks
    # How long a discovered token stays on the watchlist.
    watch_hours: float = 8.0
    max_watchlist: int = 270               # 9 API calls of 30 tokens
    # A held token missing from the API this many ticks in a row is treated
    # as dead (rugged/delisted) and closed at $0. Harsh, but honest.
    vanish_ticks: int = 3
    # A pool that loses this share of its liquidity since entry = rug pull.
    rug_liquidity_drop: float = 0.80
    equity_log_minutes: int = 10


@dataclass
class AIConfig:
    model: str = "claude-haiku-5-5"
    max_calls_per_day: int = 150
    max_calls_per_tick: int = 2
    buy_threshold: int = 7                # score 0-10
    # Forward returns of every scored token are logged at these horizons,
    # bought or not, to measure whether the scores predict anything.
    eval_horizons_min: tuple = (60, 240)


@dataclass
class CryptoConfig:
    costs: CostConfig = field(default_factory=CostConfig)
    safety: SafetyConfig = field(default_factory=SafetyConfig)
    engine: EngineConfig = field(default_factory=EngineConfig)
    ai: AIConfig = field(default_factory=AIConfig)
