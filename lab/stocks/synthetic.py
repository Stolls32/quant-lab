"""Random-but-plausible daily ETF prices for testing the backtester offline.
Like the crypto simulator, results on this data mean nothing about real markets."""
from __future__ import annotations

import math
import random
from datetime import date, timedelta

from .data import Bar


def make_bars(symbols: list[str], days: int = 2700, seed: int = 3) -> dict[str, list[Bar]]:
    rng = random.Random(seed)
    d = date(2016, 1, 4)
    dates = []
    while len(dates) < days:
        if d.weekday() < 5:
            dates.append(d.isoformat())
        d += timedelta(days=1)
    params = {}
    for s in symbols:
        if s == "BIL":
            params[s] = (0.02 / 252, 0.0003, 0.0)
        elif s == "AGG":
            params[s] = (0.03 / 252, 0.003, 0.1)
        else:
            params[s] = (rng.uniform(0.04, 0.12) / 252, rng.uniform(0.010, 0.018), rng.uniform(0.6, 1.0))
    px = {s: 100.0 for s in symbols}
    out = {s: [] for s in symbols}
    regime = 1
    for dt in dates:
        if rng.random() < 0.004:
            regime = -regime
        mkt = rng.gauss(0.0006 if regime > 0 else -0.0012, 0.009 if regime > 0 else 0.018)
        for s in symbols:
            mu, vol, beta = params[s]
            r = mu + beta * mkt + rng.gauss(0, vol * math.sqrt(max(0.0, 1 - beta**2)))
            o = px[s] * math.exp(rng.gauss(0, vol * 0.3))
            c = px[s] * math.exp(r)
            out[s].append(Bar(dt, o, max(o, c) * 1.003, min(o, c) * 0.997, c, 1e6))
            px[s] = c
    return out
