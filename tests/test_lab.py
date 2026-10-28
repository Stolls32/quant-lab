"""Run with:  python -m unittest discover -s tests -v"""
from __future__ import annotations

import os
import random
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lab import metrics as M  # noqa: E402
from lab.ai import parse_score  # noqa: E402
from lab.crypto.config import CostConfig, CryptoConfig  # noqa: E402
from lab.crypto.costs import DexCostModel  # noqa: E402
from lab.crypto.engine import CryptoLab  # noqa: E402
from lab.crypto.market import SOL_MINT, Snapshot, snapshot_from_pair  # noqa: E402
from lab.crypto.strategies import ExitRules, Strategy  # noqa: E402
from lab.stocks import backtest as BT  # noqa: E402
from lab.stocks.engine import StockCosts, new_book, rebalance  # noqa: E402
from lab.stocks.live import StockLab  # noqa: E402
from lab.stocks.strategies import Ctx, RSI2Reversion, StockStrategy, rsi, sma  # noqa: E402
from lab.stocks.synthetic import make_bars  # noqa: E402
from lab.util import read_csv  # noqa: E402


def snap(addr="TOK", price=1.0, liq=100_000, **kw) -> Snapshot:
    base = dict(address=addr, symbol=addr, price=price, liquidity=liq, fdv=liq * 5, age_min=600,
                chg={"m5": 5, "h1": 10, "h6": 10, "h24": 10}, vol={"m5": 20_000, "h1": 60_000},
                buys={"m5": 30, "h1": 200}, sells={"m5": 10, "h1": 100})
    base.update(kw)
    return Snapshot(**base)


class ScriptedMarket:
    """Market whose prices we control tick by tick."""

    def __init__(self):
        self.snaps: dict[str, Snapshot] = {}

    def discover(self):
        return list(self.snaps)

    def snapshots(self, addrs):
        return {a: s for a, s in self.snaps.items() if a in addrs}


class AlwaysBuy(Strategy):
    name = "always"
    exits = ExitRules(take_profit_pct=40, stop_loss_pct=20, trail_arm_pct=1000, trail_pct=10, max_hold_min=600)
    max_positions = 1

    def score(self, ctx):
        return 1.0


class TestCosts(unittest.TestCase):
    def test_round_trip_costs(self):
        cm = DexCostModel(CostConfig(fee_pct=1, latency_slip_pct=1, network_fee_usd=0.0))
        buy = cm.buy(1.0, 10.0, 1e12)
        sell = cm.sell(1.0, buy.qty, 1e12)
        # ~1% fee + ~1% slip each side => ~4% round trip at an unchanged price
        self.assertAlmostEqual(sell.usd / 10.0, 0.99 / 1.01 * 0.99 * 0.99, places=4)
        self.assertAlmostEqual(buy.cost_usd + sell.cost_usd, 10.0 - sell.usd, places=6)

    def test_price_impact_grows_with_size(self):
        cm = DexCostModel(CostConfig())
        self.assertLess(cm.impact_pct(10, 100_000), cm.impact_pct(1000, 100_000))
        self.assertEqual(cm.impact_pct(1e9, 1), CostConfig().max_impact_pct)


class TestCryptoEngine(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.m = ScriptedMarket()
        self.m.snaps[SOL_MINT] = snap(SOL_MINT, 150, 5e7, symbol="SOL")
        self.lab = CryptoLab(self.dir, self.m, CryptoConfig(), strategies=[AlwaysBuy()])
        self.t = 1_800_000_000.0

    def tearDown(self):
        shutil.rmtree(self.dir)

    def step(self, **prices):
        for a, kw in prices.items():
            self.m.snaps[a] = snap(a, **kw)
        self.t += 300
        return self.lab.tick(now=self.t)

    def test_take_profit(self):
        self.step(TOK=dict(price=1.0))
        self.assertIn("TOK", self.lab.state["bots"]["always"]["positions"])
        self.step(TOK=dict(price=1.5))
        trades = read_csv(f"{self.dir}/trades.csv")
        self.assertEqual(trades[0]["exit_reason"], "take_profit")
        self.assertGreater(float(trades[0]["pnl_usd"]), 0)

    def test_stop_loss_fills_at_gap_price_not_stop(self):
        self.step(TOK=dict(price=1.0))
        self.step(TOK=dict(price=0.5))  # gapped straight through the 20% stop
        t = read_csv(f"{self.dir}/trades.csv")[0]
        self.assertEqual(t["exit_reason"], "stop_loss")
        self.assertLess(float(t["ret_pct"]), -45)  # honest: you get the gap, not the stop level

    def test_rug_and_vanish(self):
        self.step(TOK=dict(price=1.0))
        self.step(TOK=dict(price=1.0, liq=5_000))
        self.assertEqual(read_csv(f"{self.dir}/trades.csv")[0]["exit_reason"], "liquidity_pulled")
        self.step(TOK2=dict(price=1.0))
        del self.m.snaps["TOK2"]
        del self.m.snaps["TOK"]
        for _ in range(3):
            self.step()
        last = read_csv(f"{self.dir}/trades.csv")[-1]
        self.assertEqual(last["exit_reason"], "vanished")
        self.assertAlmostEqual(float(last["usd_out"]), 0.0)

    def test_outage_does_not_kill_positions(self):
        self.step(TOK=dict(price=1.0))
        saved = dict(self.m.snaps)
        self.m.snaps.clear()            # whole API down, SOL included
        for _ in range(5):
            self.step()
        self.assertIn("TOK", self.lab.state["bots"]["always"]["positions"])
        self.m.snaps.update(saved)

    def test_safety_blocks_honeypot(self):
        self.step(BAD=dict(price=1.0, sells={"m5": 0, "h1": 0}))
        self.assertNotIn("BAD", self.lab.state["bots"]["always"]["positions"])

    def test_state_survives_restart(self):
        self.step(TOK=dict(price=1.0))
        lab2 = CryptoLab(self.dir, self.m, CryptoConfig(), strategies=[AlwaysBuy()])
        self.assertIn("TOK", lab2.state["bots"]["always"]["positions"])

    def test_new_season_resets_books_and_archives_once(self):
        self.step(TOK=dict(price=1.0))
        self.step(TOK=dict(price=0.5))  # a closed trade in season 1
        self.lab.save()
        cfg = CryptoConfig()
        cfg.engine.season += 1
        lab2 = CryptoLab(self.dir, self.m, cfg, strategies=[AlwaysBuy()])
        book = lab2.state["bots"]["always"]
        self.assertEqual((book["cash"], book["positions"]), (cfg.engine.start_cash_usd, {}))
        self.assertEqual(lab2.state["ticks"], 0)
        self.assertFalse(os.path.exists(f"{self.dir}/trades.csv"))
        old = cfg.engine.season - 1
        self.assertEqual(len(read_csv(f"{self.dir}/archive/season-{old}/trades.csv")), 1)
        lab2.save()
        lab3 = CryptoLab(self.dir, self.m, cfg, strategies=[AlwaysBuy()])  # restart: no second reset
        self.assertEqual(len(lab3.state["seasons"]), 1)

    def test_pair_parsing(self):
        p = {"baseToken": {"address": "X", "symbol": "X"}, "quoteToken": {"address": SOL_MINT},
             "priceUsd": "0.0012", "liquidity": {"usd": 50000}, "pairCreatedAt": 0,
             "txns": {"m5": {"buys": 3, "sells": 2}}, "volume": {"m5": 100}, "priceChange": {"m5": 1.5}}
        s = snapshot_from_pair(p, 0)
        self.assertEqual((s.price, s.b("m5"), s.s("m5"), s.c("m5")), (0.0012, 3, 2, 1.5))
        p["quoteToken"]["address"] = "SOMETHING_ELSE"
        self.assertIsNone(snapshot_from_pair(p, 0))


class TestMetrics(unittest.TestCase):
    def test_bootstrap_detects_edge(self):
        rng = random.Random(1)
        good = [rng.gauss(2, 5) for _ in range(300)]
        lo, hi = M.bootstrap_mean_ci(good)
        self.assertGreater(lo, 0)
        noise = [rng.gauss(0, 5) for _ in range(300)]
        lo, hi = M.bootstrap_mean_ci(noise)
        self.assertLess(lo, 0)
        self.assertGreater(hi, 0)

    def test_permutation(self):
        rng = random.Random(2)
        a = [rng.gauss(1.5, 3) for _ in range(200)]
        b = [rng.gauss(0, 3) for _ in range(200)]
        self.assertLess(M.permutation_pvalue(a, b), 0.01)
        self.assertGreater(M.permutation_pvalue(b, a), 0.5)

    def test_drawdown(self):
        self.assertAlmostEqual(M.max_drawdown([100, 120, 60, 130]), 50.0)


class TestAI(unittest.TestCase):
    def test_parse(self):
        ok = {"content": [{"type": "text", "text": 'Sure: {"score": 8, "reason": "clean breakout"}'}]}
        self.assertEqual(parse_score(ok), (8, "clean breakout"))
        for bad in ({"content": [{"type": "text", "text": "no json"}]},
                    {"content": [{"type": "text", "text": '{"score": 42}'}]}, None):
            self.assertIsNone(parse_score(bad))


class TestStocks(unittest.TestCase):
    def test_indicators(self):
        self.assertEqual(sma([1, 2, 3, 4], 2), 3.5)
        self.assertEqual(rsi([1, 2, 3, 4, 5], 2), 100.0)
        self.assertLess(rsi([5, 4, 3, 2, 1], 2), 1)

    def test_rebalance_and_trade_log(self):
        book = new_book(1000)
        rebalance(book, {"A": 0.5, "B": 0.5}, {"A": 10, "B": 20}, "d1", StockCosts(slippage_bps=10), False, "t")
        self.assertAlmostEqual(book["cash"], 0, places=6)
        closed = rebalance(book, {"B": 0.5}, {"A": 11, "B": 20}, "d2", StockCosts(slippage_bps=10), False, "t")
        self.assertEqual(len(closed), 1)
        self.assertAlmostEqual(closed[0]["ret_pct"], (1.1 * 0.999 * 0.999 - 1) * 100, places=3)

    def test_no_lookahead(self):
        """A strategy that buys only when TODAY's close is visible must fill at
        TOMORROW's open: the backtest may never trade on the bar it decided on."""
        seen = []

        class Peek(StockStrategy):
            name = "peek"
            universe = ["SPY"]

            def targets(self, ctx):
                seen.append((ctx.date, len(ctx.closes["SPY"])))
                return {"SPY": 1.0}

        bars = make_bars(["SPY"], days=300)
        dates, closes, opens = BT.align(bars)
        r = BT.run(Peek(), dates, closes, opens, start_index=260)
        d0, n0 = seen[0]
        self.assertEqual(dates[n0 - 1], d0)        # sees exactly through signal day
        self.assertEqual(r.dates[0], dates[261])   # first equity point is the next day

    def test_rsi2_exits_after_max_hold(self):
        closes = {s: [100.0] * 199 + [100 - i * 0.0 for i in range(10)] for s in RSI2Reversion.universe}
        ctx = Ctx(date="x", closes=closes, holdings={"SPY": {"entry_date": "a", "bars_held": 10}})
        self.assertEqual(RSI2Reversion().targets(ctx)["SPY"], 0.0)


class FakeBroker:
    configured, is_paper = True, True

    def __init__(self):
        self.bars = make_bars(__import__("lab.stocks.strategies", fromlist=["x"]).full_universe(), days=400)
        self.today = self.bars["SPY"][-1].date
        self.orders = []

    def clock(self):
        return {"is_open": True, "timestamp": self.today + "T10:05:00-04:00"}

    def daily_bars(self, syms, start, end=None):
        return {s: self.bars[s] for s in syms}

    def quotes(self, syms):
        return {s: {"bid": self.bars[s][-1].o * 0.9999, "ask": self.bars[s][-1].o * 1.0001, "last": 0} for s in syms}

    def account(self):
        return {"equity": "100000"}

    def positions(self):
        return []

    def submit_order(self, sym, side, notional=None, qty=None):
        self.orders.append((sym, side, notional, qty))


class TestStockLive(unittest.TestCase):
    def test_daily_run(self):
        d = tempfile.mkdtemp()
        try:
            fb = FakeBroker()
            lab = StockLab(d, fb)
            s = lab.run(mirror="buy_hold_spy")
            self.assertIn("buy_hold_spy", s["equity"])
            self.assertEqual(fb.orders[0][:2], ("SPY", "buy"))
            self.assertEqual(lab.run()["skipped"], "already ran today")
            self.assertTrue(read_csv(f"{d}/equity.csv"))
        finally:
            shutil.rmtree(d)


if __name__ == "__main__":
    unittest.main()
