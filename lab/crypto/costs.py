"""Realistic fill simulation for swaps on a Solana DEX.

Paper trading lies when it fills you at the screen price. Every simulated
fill here pays four costs, which is roughly what a real swap pays:

  1. Venue/aggregator fee (percent of trade)
  2. Latency slippage (price moves while your order is in flight)
  3. Price impact (your own trade moves an AMM pool's price; ~2x size/liquidity)
  4. Network/priority fee (flat dollars per transaction)

Each fill returns how many dollars the costs ate, so the stress test can later
ask "what if real costs were double this?"
"""
from __future__ import annotations

from dataclasses import dataclass

from .config import CostConfig


@dataclass
class Fill:
    price: float      # effective price paid/received per token
    qty: float        # tokens bought or sold
    usd: float        # dollars spent (buy) or received (sell), net of all costs
    cost_usd: float   # dollars lost to costs vs. a perfect fill at mid price


class DexCostModel:
    def __init__(self, cfg: CostConfig):
        self.cfg = cfg

    def impact_pct(self, usd: float, liquidity: float) -> float:
        if liquidity <= 0:
            return self.cfg.max_impact_pct
        return min(self.cfg.max_impact_pct, self.cfg.impact_mult * usd / liquidity * 100)

    def buy(self, mid: float, usd: float, liquidity: float) -> Fill | None:
        c = self.cfg
        spendable = usd - c.network_fee_usd
        if spendable <= 0 or mid <= 0:
            return None
        after_fee = spendable * (1 - c.fee_pct / 100)
        move = (c.latency_slip_pct + self.impact_pct(after_fee, liquidity)) / 100
        eff = mid * (1 + move)
        qty = after_fee / eff
        return Fill(price=eff, qty=qty, usd=usd, cost_usd=usd - qty * mid)

    def sell(self, mid: float, qty: float, liquidity: float) -> Fill:
        c = self.cfg
        if mid <= 0 or qty <= 0:
            return Fill(price=0.0, qty=qty, usd=0.0, cost_usd=0.0)
        gross = qty * mid
        move = (c.latency_slip_pct + self.impact_pct(gross, liquidity)) / 100
        eff = mid * max(0.0, 1 - move)
        proceeds = max(0.0, qty * eff * (1 - c.fee_pct / 100) - c.network_fee_usd)
        return Fill(price=eff, qty=qty, usd=proceeds, cost_usd=gross - proceeds)
