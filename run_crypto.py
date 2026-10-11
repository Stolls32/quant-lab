#!/usr/bin/env python3
"""Run the meme-coin bots.

  python run_crypto.py                  one live tick (what GitHub Actions runs)
  python run_crypto.py --loop 300       live, forever, every 300s (laptop mode)
  python run_crypto.py --demo 2000      2000 ticks on the fake market (offline test)
"""
from __future__ import annotations

import argparse
import logging
import shutil
import time

from lab.crypto.engine import CryptoLab
from lab.report import write_report
from lab.util import setup_logging

log = logging.getLogger("lab")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data/crypto")
    ap.add_argument("--loop", type=int, default=0, help="seconds between live ticks; 0 = run once")
    ap.add_argument("--demo", type=int, default=0, help="run N ticks on the simulated market")
    ap.add_argument("--no-report", action="store_true")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()
    setup_logging(args.verbose)

    if args.demo:
        from lab.crypto.sim import SimMarket
        data_dir = "data/demo/crypto"
        shutil.rmtree(data_dir, ignore_errors=True)
        sim = SimMarket()
        lab = CryptoLab(data_dir, sim)
        logging.getLogger("lab.crypto").setLevel(logging.WARNING)
        for i in range(args.demo):
            sim.advance()
            lab.tick(now=sim.now)
        write_report(crypto_dir=data_dir, stocks_dir="data/demo/stocks", out="data/demo/REPORT.md", demo=True)
        print(open("data/demo/REPORT.md", encoding="utf-8").read())
        return

    from lab.crypto.market import DexScreener
    lab = CryptoLab(args.data_dir, DexScreener())
    while True:
        t0 = time.time()
        ev = lab.tick()
        log.info("tick: %d discovered, %d snapshots, %d safe, opened=%s closed=%s ai=%d (%.1fs)",
                 ev["discovered"], ev["snapshots"], ev.get("safe_candidates", 0),
                 ev["opened"], ev["closed"], ev["ai_scored"], time.time() - t0)
        if ev["snapshots"] == 0:
            log.warning("No market data returned. API down or blocked? State saved; nothing traded.")
        if not args.no_report:
            write_report()
        if not args.loop:
            break
        time.sleep(max(5, args.loop - (time.time() - t0)))


if __name__ == "__main__":
    main()
