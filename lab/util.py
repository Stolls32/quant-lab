"""Shared helpers: HTTP with retries, rate limiting, atomic file writes, CSV logs.

Standard library only, so the bot runs anywhere Python 3.11+ runs (GitHub
Actions, your laptop, a Raspberry Pi) with no `pip install` step.
"""
from __future__ import annotations

import csv
import json
import logging
import os
import random
import tempfile
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from typing import Any, Iterable

log = logging.getLogger("lab")


def setup_logging(verbose: bool = False) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
    )


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_iso(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


# --------------------------------------------------------------------------- HTTP
class HttpError(Exception):
    def __init__(self, status: int, body: str, url: str):
        super().__init__(f"HTTP {status} for {url}: {body[:200]}")
        self.status = status
        self.body = body
        self.url = url


class RateLimiter:
    """Guarantees at least `min_interval` seconds between calls."""

    def __init__(self, calls_per_minute: float):
        self.min_interval = 60.0 / calls_per_minute
        self._last = 0.0

    def wait(self) -> None:
        gap = time.monotonic() - self._last
        if gap < self.min_interval:
            time.sleep(self.min_interval - gap)
        self._last = time.monotonic()


def http_json(
    url: str,
    *,
    method: str = "GET",
    headers: dict[str, str] | None = None,
    body: Any = None,
    timeout: float = 20,
    retries: int = 3,
    backoff: float = 1.5,
    limiter: RateLimiter | None = None,
) -> Any:
    """GET/POST JSON with exponential backoff on 429/5xx/network errors.

    4xx errors other than 429 are raised immediately (retrying a bad request
    or a bad API key never helps).
    """
    data = json.dumps(body).encode() if body is not None else None
    hdrs = {"User-Agent": "quant-lab/1.0", "Accept": "application/json"}
    if data is not None:
        hdrs["Content-Type"] = "application/json"
    hdrs.update(headers or {})
    last_err: Exception | None = None
    for attempt in range(retries + 1):
        if limiter:
            limiter.wait()
        req = urllib.request.Request(url, data=data, headers=hdrs, method=method)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read()
                return json.loads(raw) if raw else None
        except urllib.error.HTTPError as e:
            text = e.read().decode(errors="replace")
            last_err = HttpError(e.code, text, url)
            if e.code == 429 or e.code >= 500:
                time.sleep(backoff * (2**attempt) + random.random())
                continue
            raise last_err
        except (urllib.error.URLError, TimeoutError, ConnectionError, json.JSONDecodeError) as e:
            last_err = e
            time.sleep(backoff * (2**attempt) + random.random())
    assert last_err is not None
    raise last_err


# ---------------------------------------------------------------------- files
def load_json(path: str, default: Any) -> Any:
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default


def save_json_atomic(path: str, obj: Any) -> None:
    """Write to a temp file then rename, so a crash never leaves half a file."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path) or ".", suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1, sort_keys=True, default=str)
    os.replace(tmp, path)


def append_csv(path: str, fieldnames: list[str], rows: Iterable[dict]) -> int:
    rows = list(rows)
    if not rows:
        return 0
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    new = not os.path.exists(path) or os.path.getsize(path) == 0
    with open(path, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        if new:
            w.writeheader()
        for r in rows:
            w.writerow(r)
    return len(rows)


def read_csv(path: str) -> list[dict]:
    try:
        with open(path, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        return []


def fnum(x: Any, default: float = 0.0) -> float:
    """Tolerant float conversion for API fields that may be None/str/missing."""
    try:
        if x is None or x == "":
            return default
        return float(x)
    except (TypeError, ValueError):
        return default
