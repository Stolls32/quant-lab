"""The meme-coin trading bots.

Every bot sees the same market data, passes the same safety screen, pays the
same costs, and starts with the same cash. They differ only in WHEN they buy
and HOW they exit. That's what makes the leaderboard a fair fight.

Entry logic returns a score (higher = stronger signal) or None (no trade).
Exit logic is shared and parameterised by each bot's ExitRules.

Rules of thumb behind the defaults (see RESEARCH.md for evidence):
* Momentum: short-horizon momentum is the most documented effect in crypto
  returns, but it reverses violently in illiquid coins, so stops are tight.
* Losses must be cut faster than wins: with ~3-5% round-trip costs, a bot
  needs either a high win rate or wins much bigger than losses to break even.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field

from .market import Snapshot


@dataclass
class ExitRules:
    take_profit_pct: float
    stop_loss_pct: float
    trail_arm_pct: float      # trailing stop switches on after this gain...
    trail_pct: float          # ...and sells if price falls this far from its peak
    max_hold_min: float


@dataclass
class Context:
    """What a strategy may look at: the snapshot plus this token's recent path."""
    snap: Snapshot
    history: list = field(default_factory=list)   # [[ts, price, liquidity], ...] oldest first
    now_ts: float = 0.0

    def price_n_ago(self, minutes: float) -> float | None:
        cutoff = self.now_ts - minutes * 60
        older = [p for t, p, _ in self.history if t <= cutoff]
        return older[-1] if older else None

    def high_since(self, minutes: float) -> float | None:
        cutoff = self.now_ts - minutes * 60
        pts = [p for t, p, _ in self.history if t >= cutoff]
        return max(pts) if pts else None


class Strategy:
    name = "base"
    description = ""
    is_benchmark = False
    is_control = False
    size_frac = 0.25          # fraction of STARTING cash per trade
    max_positions = 3
    cooldown_min = 360        # don't re-buy the same token within this window
    exits = ExitRules(40, 20, 20, 15, 360)

    def score(self, ctx: Context) -> float | None:
        raise NotImplementedError

    def wants_to_trade_now(self) -> bool:
        """Hook for bots that only trade some ticks (the random control)."""
        return True

    def params(self) -> dict:
        e = self.exits
        return {
            "size_frac": self.size_frac, "max_positions": self.max_positions,
            "tp": e.take_profit_pct, "sl": e.stop_loss_pct, "trail_arm": e.trail_arm_pct,
            "trail": e.trail_pct, "max_hold_min": e.max_hold_min,
        }


class MomentumBreakout(Strategy):
    name = "momentum"
    description = "Established token breaking out: up on 5m AND 1h, buyers outnumber sellers, real volume."
    exits = ExitRules(take_profit_pct=40, stop_loss_pct=18, trail_arm_pct=20, trail_pct=15, max_hold_min=360)

    def score(self, ctx: Context) -> float | None:
        s = ctx.snap
        if s.age_min < 60 or s.liquidity < 50_000:
            return None
        if not (4 <= s.c("m5") <= 25 and 8 <= s.c("h1") <= 150):
            return None
        if s.b("m5") < 1.5 * max(1, s.s("m5")) or s.v("m5") < 8_000:
            return None
        return s.c("m5") + s.c("h1") / 4


class DipReclaim(Strategy):
    name = "dip_reclaim"
    description = "Token up on the day pulls back hard over the last hour, then starts bouncing."
    exits = ExitRules(take_profit_pct=18, stop_loss_pct=12, trail_arm_pct=10, trail_pct=8, max_hold_min=720)

    def score(self, ctx: Context) -> float | None:
        s = ctx.snap
        if s.age_min < 24 * 60 or s.liquidity < 100_000:
            return None
        if not (s.c("h24") >= 10 and s.c("h1") <= -10 and s.c("m5") >= 1):
            return None
        if s.b("m5") <= s.s("m5"):
            return None
        return -s.c("h1")  # deeper dip (that's bouncing) = stronger signal


class FreshLaunch(Strategy):
    name = "fresh_launch"
    description = "Brand-new pool (10m-3h old) with strong buying. Highest risk, smallest size."
    size_frac = 0.15
    max_positions = 4
    exits = ExitRules(take_profit_pct=80, stop_loss_pct=30, trail_arm_pct=40, trail_pct=25, max_hold_min=120)

    def score(self, ctx: Context) -> float | None:
        s = ctx.snap
        if not (10 <= s.age_min <= 180) or s.liquidity < 25_000:
            return None
        if s.v("m5") < 5_000 or s.c("h1") < 15 or s.c("m5") <= 0:
            return None
        if s.b("m5") < 1.3 * max(1, s.s("m5")):
            return None
        return s.v("m5") / max(1.0, s.liquidity) * 100


class VolumeSpike(Strategy):
    name = "volume_spike"
    description = "Last 5 minutes traded 3x+ the hour's average pace while price ticks up."
    exits = ExitRules(take_profit_pct=30, stop_loss_pct=15, trail_arm_pct=15, trail_pct=12, max_hold_min=240)

    def score(self, ctx: Context) -> float | None:
        s = ctx.snap
        if s.age_min < 120 or s.liquidity < 40_000:
            return None
        avg5 = s.v("h1") / 12
        if avg5 <= 0 or s.v("m5") < max(5_000, 3 * avg5):
            return None
        if not (2 <= s.c("m5") <= 20) or s.b("m5") <= s.s("m5"):
            return None
        return s.v("m5") / avg5


class ClaudeAnalyst(Strategy):
    """Rule-based pre-filter, then Claude reads the setup and scores it.

    Uses the SAME exits as `momentum`, so comparing the two answers one
    question cleanly: does an AI's judgment improve on the plain rules?
    The scoring call itself lives in lab/ai.py; the runner wires it in.
    """
    name = "claude_analyst"
    description = "Momentum/volume candidates scored 0-10 by Claude; buys only high-conviction setups."
    exits = MomentumBreakout.exits

    def score(self, ctx: Context) -> float | None:
        s = ctx.snap
        if s.age_min < 60 or s.liquidity < 40_000:
            return None
        loose_momo = s.c("m5") >= 2 and s.c("h1") >= 5 and s.b("m5") > s.s("m5")
        avg5 = s.v("h1") / 12
        loose_vol = avg5 > 0 and s.v("m5") >= 2 * avg5 and s.c("m5") > 0
        if not (loose_momo or loose_vol):
            return None
        return s.c("m5") + s.c("h1") / 4   # used only to rank who gets sent to Claude


class RandomControl(Strategy):
    """The coin flip. Buys random tokens from the same safe universe, with the
    same exits and sizing as `momentum`. Any bot that can't beat this has no
    real entry signal — its results are luck plus exits."""
    name = "random_control"
    description = "Control group: random entries, same universe/exits/size as momentum."
    is_control = True
    exits = MomentumBreakout.exits
    entry_prob_per_tick = 0.12

    def __init__(self, seed: int = 0):
        self.rng = random.Random(seed)

    def reseed(self, seed: int) -> None:
        self.rng = random.Random(seed)

    def wants_to_trade_now(self) -> bool:
        return self.rng.random() < self.entry_prob_per_tick

    def score(self, ctx: Context) -> float | None:
        s = ctx.snap
        if s.age_min < 60 or s.liquidity < 50_000:
            return None
        return self.rng.random()


class HoldSOL(Strategy):
    """Benchmark: put all $10 into SOL on day one and never touch it.
    A meme-coin bot that loses to this was a worse bet than the plain asset."""
    name = "hold_sol"
    description = "Benchmark: buy SOL once, hold forever."
    is_benchmark = True

    def score(self, ctx: Context) -> float | None:
        return None


def all_strategies(seed: int = 0) -> list[Strategy]:
    return [MomentumBreakout(), DipReclaim(), FreshLaunch(), VolumeSpike(),
            ClaudeAnalyst(), RandomControl(seed), HoldSOL()]
