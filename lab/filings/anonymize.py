"""Strip what would let the model recognize the company or the calendar year.

Why: the scoring model was trained on text written after most of these
filings. If it recognizes "Acme Corp, 2019", it may already know Acme went
bankrupt in 2020, and the backtest would quietly use the future. We mask:
company names (current and former, with and without suffixes), tickers,
web addresses and emails, and absolute years, which become years relative to
the newer report: [FY+0] is the newer report's fiscal year, [FY-1] the one before.

This lowers the risk; it doesn't remove it (era clues like a pandemic or a
specific law still leak). The recognition probe in score.py measures how much leaks.
"""
from __future__ import annotations

import re

_SUFFIXES = r"(?:,?\s+(?:inc|incorporated|corp|corporation|co|company|ltd|limited|llc|l\.p|lp|plc|n\.v|s\.a|ag|" \
            r"holdings?|group|international|technologies|technology|bancorp|trust|/\w{2}/?)\.?)+$"
_COMMON_FIRST = {
    "american", "first", "united", "general", "national", "international", "global", "capital", "new",
    "north", "south", "east", "west", "western", "eastern", "central", "pacific", "atlantic", "great",
    "the", "bank", "energy", "applied", "advanced", "digital", "integrated", "standard", "universal",
    "community", "citizens", "peoples", "home", "medical", "health", "data", "royal", "southern", "northern",
}
# Industry words that appear in company names but also in every filing in that industry.
_GENERIC = {
    "industries", "brands", "homes", "pharmaceuticals", "pharma", "therapeutics", "biosciences", "bioscience",
    "biologics", "biotherapeutics", "biotech", "systems", "solutions", "resources", "partners", "financial",
    "bancorp", "bancshares", "bankshares", "savings", "value", "plus", "fund", "trust", "reit", "realty",
    "properties", "oil", "gas", "petroleum", "mining", "minerals", "gold", "silver", "metals", "software",
    "networks", "communications", "media", "entertainment", "foods", "restaurants", "motors", "automotive",
    "insurance", "services", "products", "enterprises", "ventures", "investors", "investment", "investments",
    "acquisition", "materials", "devices", "diagnostics", "labs", "laboratories", "sciences", "science",
    "healthcare", "care", "power", "electric", "water", "airlines", "air", "marine", "shipping", "logistics",
    "retail", "stores", "brewing", "beverage", "beverages", "apparel", "robotics", "semiconductor",
}


def name_aliases(names: list[str]) -> list[str]:
    """'ACME UNITED CORP' → ['ACME UNITED CORP', 'ACME UNITED', 'ACME']; longest first."""
    out: set[str] = set()
    for name in names:
        name = re.sub(r"\s+", " ", name or "").strip()
        if not name:
            continue
        out.add(name)
        core = re.sub(_SUFFIXES, "", name, flags=re.I).strip(" ,.")
        if len(core) >= 3:
            out.add(core)
        words = [w.strip(",.") for w in core.split()]
        if words:
            if len(words[0]) < 4 or words[0].lower() in _COMMON_FIRST:
                if len(words) >= 2:
                    out.add(" ".join(words[:2]))
            # every distinctive word on its own ("El Pollo Loco" → "Pollo", "Loco": brand names reuse them)
            for w in words:
                if len(w) >= 4 and w.lower() not in _COMMON_FIRST and w.lower() not in _GENERIC:
                    out.add(w)
    return sorted(out, key=len, reverse=True)


def anonymize(text: str, names: list[str], tickers: list[str], fiscal_year: int | None) -> str:
    def sub_company(m: re.Match) -> str:
        return "the Company's" if m.group(0).lower().endswith(("'s", "’s")) else "the Company"

    for alias in name_aliases(names):
        if " " in alias:
            text = re.sub(r"(?<![\w])" + re.escape(alias) + r"(?:['’]s)?(?![\w])", sub_company, text, flags=re.I)
        else:
            # a single word like "Core" or "Apple" is also an ordinary word: only mask capitalized uses
            forms = {alias, alias.upper(), alias.title()}
            pat = "|".join(re.escape(f) for f in forms)
            text = re.sub(r"(?<![\w])(?:" + pat + r")(?:['’]s)?(?![\w])", sub_company, text)
    for t in tickers:
        if len(t) >= 3:
            text = re.sub(r"(?<![\w])" + re.escape(t) + r"(?![\w])", "[TICKER]", text)
        elif t:
            # short tickers collide with ordinary words; only mask them in an exchange context
            text = re.sub(r"(?i)((?:nasdaq|nyse|amex|otc\w*|symbol)\W{1,20})" + re.escape(t) + r"\b",
                          r"\1[TICKER]", text)
    text = re.sub(r"(?i)\b(?:https?://|www\.)\S+", "[URL]", text)
    text = re.sub(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b", "[EMAIL]", text)
    if fiscal_year:
        def rel(m: re.Match) -> str:
            off = int(m.group(0)) - fiscal_year
            return f"[FY{off:+d}]"
        text = re.sub(r"(?<![\d$])(?<!\d\.)(?:19[5-9]\d|20[0-4]\d)(?!\d|[,.]\d)", rel, text)
    return text
