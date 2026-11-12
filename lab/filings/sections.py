"""Turn a 10-K document into plain text and cut out the sections we compare.

10-K HTML is messy: tables of contents repeat every heading, inline-XBRL
filings carry a hidden block of tagged data, and page numbers and "Table of
Contents" links interrupt paragraphs. The approach here is deliberately simple:
find every line that looks like an "Item N." heading, and for each section we
want, take the longest stretch between its heading and the next later item.
The table-of-contents copy is always short, so the body copy wins.
"""
from __future__ import annotations

import html
import re
from html.parser import HTMLParser

ITEM_ORDER = ["1", "1a", "1b", "1c", "2", "3", "4", "5", "6", "7", "7a", "8", "9", "9a", "9b", "9c",
              "10", "11", "12", "13", "14", "15", "16"]
_RANK = {k: i for i, k in enumerate(ITEM_ORDER)}

_BLOCK = {"p", "div", "br", "tr", "li", "h1", "h2", "h3", "h4", "h5", "h6", "table", "section",
          "article", "ul", "ol", "center", "blockquote", "pre", "hr", "title"}
_SKIP = {"script", "style", "head", "ix:header"}  # ix:header = hidden inline-XBRL data block


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in _SKIP:
            self.skip_depth += 1
        elif tag in _BLOCK:
            self.parts.append("\n")
        elif tag in ("td", "th"):
            self.parts.append(" ")

    def handle_startendtag(self, tag, attrs):
        if tag in _BLOCK:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in _SKIP:
            self.skip_depth = max(0, self.skip_depth - 1)
        elif tag in _BLOCK:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.skip_depth:
            self.parts.append(data)


_PAGE_NOISE = re.compile(
    r"^(?:\(?\s*(?:page\s*)?[ivxlc\d]{1,4}\s*\)?|-\s*\d+\s*-|table\s+of\s+contents|index|back\s+to\s+(?:top|contents))$",
    re.I,
)


def _is_footer(line: str) -> bool:
    """Running page footers like 'Acme Corp. | 2022 Form 10-K | 42'."""
    return len(line) < 120 and re.search(r"form\s+10-k", line, re.I) is not None \
        and re.search(r"(?<![\d,])\d{1,3}\s*$", line) is not None


def to_text(doc: str) -> str:
    """HTML (or old plain-text SGML) filing → clean text, one paragraph per line."""
    looks_html = re.search(r"<(?:html|body|p|div|table)\b", doc[:20000], re.I) is not None
    if looks_html:
        p = _TextExtractor()
        p.feed(doc)
        p.close()
        raw = "".join(p.parts)
    else:
        raw = html.unescape(re.sub(r"<[^>]{1,40}>", "\n", doc))  # SGML tags like <PAGE>
    raw = raw.replace("\xa0", " ").replace("​", "").replace("\r", "\n")
    lines = []
    for line in raw.split("\n"):
        line = re.sub(r"[ \t\f\v]+", " ", line).strip()
        if line and not _PAGE_NOISE.match(line) and not _is_footer(line):
            lines.append(line)
    return _join_broken_lines(lines)


def _join_broken_lines(lines: list[str]) -> str:
    """Re-join paragraphs that were split across lines (common in PDF-converted filings)."""
    out: list[str] = []
    for line in lines:
        if out and out[-1] and not out[-1].endswith((".", ":", ";", "?", "!", '"', "”")) \
                and line[:1].islower() and len(out[-1]) > 40:
            out[-1] = out[-1] + " " + line
        else:
            out.append(line)
    return "\n".join(out)


# "Item 1A.", "ITEM 7 -", "Item 9A(T)", "Items 1 and 2." ...
_HEADING = re.compile(r"^\s*items?\s*(\d{1,2})\s*([a-c])?\b\s*(?:\(t\))?\s*[\.\:\-–—]?", re.I)


# Some filers drop the word "Item" ("1A. Risk Factors"). A bare number is only
# trusted when the standard title follows, since notes to the financial
# statements are numbered too ("7. Debt").
_TITLES = {
    "1": r"business", "1a": r"risk\s+factors", "1b": r"unresolved\s+staff", "1c": r"cybersecurity",
    "2": r"(?:description\s+of\s+)?propert", "3": r"legal\s+proceedings", "4": r"(?:mine\s+safety|submission\s+of\s+matters)",
    "5": r"market\s+for", "6": r"(?:selected\s+financial|\[?reserved)", "7": r"management.?s\s+discussion",
    "7a": r"quantitative\s+and\s+qualitative", "8": r"financial\s+statements", "9": r"changes\s+in\s+and\s+disagreements",
    "9a": r"controls\s+and\s+procedures", "9b": r"other\s+information", "9c": r"disclosure\s+regarding\s+foreign",
    "10": r"directors", "15": r"exhibits",
}
_BARE = re.compile(r"^\s*(\d{1,2})\s*([a-c])?\s*(?:\(t\))?\s*[\.\:\-–—]\s*(.*)$", re.I)


def headings(text: str) -> list[tuple[int, str]]:
    """(character offset, item key) for every line that looks like an item heading."""
    found = []
    pos = 0
    for line in text.split("\n"):
        if len(line) <= 160:
            key = None
            m = _HEADING.match(line)
            if m:
                key = m.group(1) + (m.group(2) or "").lower()
            else:
                b = _BARE.match(line)
                if b:
                    k = b.group(1) + (b.group(2) or "").lower()
                    if k in _TITLES and re.match(_TITLES[k], b.group(3), re.I):
                        key = k
            if key in _RANK:
                found.append((pos, key))
        pos += len(line) + 1
    return found


def extract_sections(text: str, wanted: tuple[str, ...]) -> dict[str, str]:
    """Longest body for each wanted item, bounded by the next later item heading."""
    heads = headings(text)
    out: dict[str, str] = {}
    for key in wanted:
        best = ""
        for i, (start, k) in enumerate(heads):
            if k != key:
                continue
            end = len(text)
            for start2, k2 in heads[i + 1:]:
                if _RANK[k2] > _RANK[key]:
                    end = start2
                    break
            body = text[start:end]
            if len(body) > len(best):
                best = body
        if best:
            out[key] = best.strip()
    return out


# Phrases worth flagging across the whole document (cheap, no LLM needed).
FLAG_PATTERNS = {
    "going_concern": r"substantial doubt\b[^.]{0,120}\bgoing concern|going concern\b[^.]{0,120}\bsubstantial doubt",
    "material_weakness": r"material weakness(?:es)?\b",
    "not_effective": r"(?:disclosure controls|internal control)[^.]{0,200}\bwere not effective|\bnot effective\b",
    "restatement": r"\brestate(?:d|ment)\b",
}


def flags(text: str) -> dict[str, int]:
    low = text.lower()
    return {name: len(re.findall(pat, low)) for name, pat in FLAG_PATTERNS.items()}
