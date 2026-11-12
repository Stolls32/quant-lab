#!/usr/bin/env python3
"""Filing-change research pipeline (RESEARCH.md, Part 5). Needs SEC_USER_AGENT set.

  python run_filings.py universe --year 2022           small caps by public float, mid-2022
  python run_filings.py build --year 2022 --sample 25  fetch + compare 10-K pairs for 25 random companies
  python run_filings.py cost                           what scoring everything built so far would cost
  python run_filings.py probe --n 20                   leak test: can the model name the company/year?
  python run_filings.py score --period development --max-calls 50

`build` is resumable: rerun it and it skips pairs already done. Raw filings are
cached under data/filings/cache/, so nothing is downloaded twice.
"""
from __future__ import annotations

import argparse
import json
import logging

from lab.filings import pipeline as P
from lab.filings.config import FilingsConfig
from lab.filings.edgar import Edgar
from lab.util import read_csv, setup_logging

log = logging.getLogger("lab")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    u = sub.add_parser("universe")
    u.add_argument("--year", type=int, required=True)
    b = sub.add_parser("build")
    b.add_argument("--year", type=int, required=True)
    b.add_argument("--sample", type=int, default=None, help="random sample size (default: whole universe)")
    b.add_argument("--seed", type=int, default=7)
    c = sub.add_parser("cost")
    c.add_argument("--period", default=None)
    s = sub.add_parser("score")
    s.add_argument("--period", default=None, choices=["development", "validation", "holdout"])
    s.add_argument("--max-calls", type=int, default=50)
    p = sub.add_parser("probe")
    p.add_argument("--n", type=int, default=20)
    p.add_argument("--seed", type=int, default=7)
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()
    setup_logging(args.verbose)
    cfg = FilingsConfig()

    if args.cmd == "universe":
        P.build_universe(Edgar(cfg.cache_dir), cfg, args.year)
    elif args.cmd == "build":
        rows = P.build(Edgar(cfg.cache_dir), cfg, args.year, args.sample, args.seed)
        ok = [r for r in rows if r["status"] == "ok"]
        log.info("built %d pairs (%d with comparable sections)", len(rows), len(ok))
    elif args.cmd == "cost":
        sizes = [len(read_csv(f"{cfg.out_dir}/universe_CY{y}.csv")) for y in range(2000, 2030)]
        biggest = max(sizes) or None
        print(json.dumps(P.cost_report(cfg, args.period, biggest), indent=1))
    elif args.cmd == "score":
        n = P.score_all(cfg, args.period, args.max_calls)
        log.info("scored %d filing pairs → %s/scores.csv", n, cfg.out_dir)
    elif args.cmd == "probe":
        print(json.dumps(P.run_probe(cfg, args.n, args.seed), indent=1))


if __name__ == "__main__":
    main()
