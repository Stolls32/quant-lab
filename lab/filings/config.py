"""Settings for the filing-change experiment. See RESEARCH.md, Part 5.

Change these BEFORE looking at results, and write down the date if you change
them afterwards. Every knob turned after seeing returns is another strategy
tried, and the multiple-testing math in Part 1 of RESEARCH.md applies.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class FilingsConfig:
    # --- universe: small, neglected companies (point-in-time, from the 10-K cover page)
    min_public_float: float = 10e6      # below this, too illiquid to trade even small
    max_public_float: float = 300e6     # above this, more analysts and funds are reading
    # 6770 blank-check shells / SPACs; 6221 commodity pools and commodity ETFs (no business to read about).
    # Non-traded REITs and partnerships get dropped later, when price data is matched (they have none).
    exclude_sic: tuple[int, ...] = (6770, 6221)

    # --- which 10-K sections to compare year over year
    # 1a Risk Factors, 3 Legal Proceedings, 7 MD&A, 9a Controls and Procedures
    sections: tuple[str, ...] = ("1a", "3", "7", "9a")

    # --- what the model sees
    max_payload_words: int = 10000      # per filing pair (~13K tokens); edits and additions go first
    min_paragraph_words: int = 4

    # --- scoring model
    model: str = "claude-haiku-5-5"
    # The model may "know" what happened to a company after any filing dated before
    # its training cutoff. Only filings AFTER this date are a clean test of the LLM
    # score. Check the model's documented training-data cutoff when you change models.
    model_knowledge_cutoff: str = "2026-06-30"
    # USD per million tokens, Haiku 5.5 standard rates for prompts up to 100K tokens
    # (Anthropic pricing page, Oct 2026). The Batch API is half price.
    price_in_per_mtok: float = 0.10
    price_out_per_mtok: float = 0.50
    est_output_tokens: int = 400        # JSON answer plus any thinking

    # --- pre-registered research periods (by filing date). See RESEARCH.md Part 5.
    periods: dict[str, tuple[str, str]] = field(default_factory=lambda: {
        "development": ("2012-01-01", "2018-12-31"),  # build and debug on this only
        "validation": ("2019-01-01", "2026-06-30"),   # run once, after the design is frozen
        "holdout": ("2026-07-01", "2099-12-31"),      # after the model's cutoff: the real test
    })

    cache_dir: str = "data/filings/cache"
    out_dir: str = "data/filings"


def period_of(filing_date: str, cfg: FilingsConfig) -> str:
    for name, (start, end) in cfg.periods.items():
        if start <= filing_date <= end:
            return name
    return "outside"
