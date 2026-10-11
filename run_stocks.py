#!/usr/bin/env python3
"""Daily stock/ETF paper-trading run (GitHub Actions calls this each weekday).

  python run_stocks.py                         normal daily run (skips if market closed / already ran)
  python run_stocks.py --force                 run even if closed or already ran (testing)
  python run_stocks.py --mirror dual_momentum  also place real orders in your Alpaca PAPER account
                                               to match that one strategy (or set MIRROR_STRATEGY)
"""
from __future__ import annotations

import argparse
import json
import logging
import os

from lab.report import write_report
from lab.stocks.data import Alpaca
from lab.stocks.live import StockLab
from lab.util import setup_logging

log = logging.getLogger("lab")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data/stocks")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--mirror", default=os.environ.get("MIRROR_STRATEGY") or None)
    args = ap.parse_args()
    setup_logging()

    broker = Alpaca()
    if not broker.configured:
        log.warning("ALPACA_API_KEY / ALPACA_API_SECRET not set; skipping stock run.")
        return
    lab = StockLab(args.data_dir, broker)
    summary = lab.run(force=args.force, mirror=args.mirror)
    log.info("stocks: %s", json.dumps(summary, default=str))
    write_report()


if __name__ == "__main__":
    main()
