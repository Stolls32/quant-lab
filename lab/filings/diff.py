"""Compare the same 10-K section across two consecutive years.

Two outputs:
1. Baseline similarity scores, as in Cohen, Malloy & Nguyen, "Lazy Prices"
   (Journal of Finance, 2020): cosine and Jaccard similarity of the words.
   Cheap, no LLM, no look-ahead. The LLM score has to beat these to be worth paying for.
2. A paragraph-level change list (added / removed / edited, with word-level
   edits marked) that the LLM reads.

Years are masked before matching, so "fiscal 2023" becoming "fiscal 2024" doesn't
count as a change. Other numbers do count: a customer going from 40% to 65% of
revenue is exactly the kind of change we want the model to see.
"""
from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass, field
from difflib import SequenceMatcher

_WORD = re.compile(r"[a-z][a-z'\-]+")


_YEAR = re.compile(r"(?<!\d)(?:19[5-9]\d|20[0-4]\d)(?!\d)")


_QUOTES = str.maketrans({"’": "'", "‘": "'", "“": '"', "”": '"', "–": "-", "—": "-"})


def _norm(p: str) -> str:
    """Comparison key: case, curly quotes, bullets and year bumps don't count as changes."""
    p = _YEAR.sub("<y>", p.lower().translate(_QUOTES))
    p = re.sub(r"^[\s•●▪◦·\-\*]+", "", p)
    return re.sub(r"\s+", " ", p).strip()


def _is_table_row(p: str) -> bool:
    """Financial-table rows ('Home sales $ 1,392,750 $ 936,400') are mostly numbers."""
    toks = p.split()
    alpha = sum(1 for t in toks if re.search(r"[A-Za-z]{2,}", t))
    if alpha / max(1, len(toks)) < 0.5:
        return True
    # a label followed by a run of figures, with no sentence ending
    tail = [t for t in toks[-3:] if t not in ("$", "%")]
    numeric = sum(1 for t in tail if re.fullmatch(r"[\(\$]*[\d,\.]+%?\)?|[—–-]", t))
    return numeric >= 2 and not p.rstrip().endswith((".", ":", ";"))


def paragraphs(section: str, min_words: int = 4) -> list[str]:
    return [p.strip() for p in section.split("\n") if len(p.split()) >= min_words and not _is_table_row(p)]


# ---------------------------------------------------------------- baseline similarity
# Without dropping filler words every long section scores ~0.999, because "the",
# "of" and "our" dominate the counts and never change.
_STOP = set("""a about above after again against all also am an and any are as at be because been before being
below between both but by can could did do does doing down during each few for from further had has have having
he her here hers him his how i if in into is it its itself just may might more most must no nor not now of off
on once only or other our ours ourselves out over own same shall she should so some such than that the their
theirs them themselves then there these they this those through to too under until up upon us very was we were
what when where which while who whom why will with within without would you your company company's""".split())


def _bag(text: str) -> Counter:
    return Counter(w for w in _WORD.findall(text.lower()) if w not in _STOP)


def cosine(a: str, b: str) -> float:
    ca, cb = _bag(a), _bag(b)
    if not ca or not cb:
        return float("nan")
    dot = sum(v * cb.get(k, 0) for k, v in ca.items())
    return dot / (math.sqrt(sum(v * v for v in ca.values())) * math.sqrt(sum(v * v for v in cb.values())))


def jaccard(a: str, b: str) -> float:
    sa, sb = set(_bag(a)), set(_bag(b))
    if not sa or not sb:
        return float("nan")
    return len(sa & sb) / len(sa | sb)


# ---------------------------------------------------------------- paragraph diff
@dataclass
class SectionChanges:
    section: str
    added: list[str] = field(default_factory=list)
    removed: list[str] = field(default_factory=list)
    edited: list[tuple[str, str, float]] = field(default_factory=list)  # (old, new, similarity)
    unchanged: int = 0
    old_words: int = 0
    new_words: int = 0

    @property
    def changed_share(self) -> float:
        total = self.unchanged + len(self.edited) + max(len(self.added), len(self.removed))
        return 0.0 if total == 0 else 1 - self.unchanged / total


def _quick_overlap(a: str, b: str) -> float:
    sa, sb = set(a.split()), set(b.split())
    return len(sa & sb) / max(1, len(sa | sb))


def compare(section: str, old: str, new: str, min_words: int = 4, edit_threshold: float = 0.6) -> SectionChanges:
    old_p, new_p = paragraphs(old, min_words), paragraphs(new, min_words)
    out = SectionChanges(section, old_words=len(old.split()), new_words=len(new.split()))

    old_keys = Counter(_norm(p) for p in old_p)
    rem_old: list[str] = []
    seen = Counter()
    new_keys = Counter(_norm(p) for p in new_p)
    for p in old_p:
        k = _norm(p)
        seen[k] += 1
        if seen[k] > new_keys.get(k, 0):
            rem_old.append(p)
    seen.clear()
    rem_new: list[str] = []
    for p in new_p:
        k = _norm(p)
        seen[k] += 1
        if seen[k] > old_keys.get(k, 0):
            rem_new.append(p)
        else:
            out.unchanged += 1

    # Pair up leftovers that are edits of each other (greedy, best match first).
    cands = []
    old_n = [_norm(p) for p in rem_old]
    new_n = [_norm(p) for p in rem_new]
    for j, nb in enumerate(new_n):
        for i, ob in enumerate(old_n):
            if _quick_overlap(ob, nb) < 0.35:
                continue
            r = SequenceMatcher(None, ob.split(), nb.split(), autojunk=False).ratio()
            if r >= edit_threshold:
                cands.append((r, i, j))
    used_o, used_n = set(), set()
    for r, i, j in sorted(cands, reverse=True):
        if i in used_o or j in used_n:
            continue
        used_o.add(i)
        used_n.add(j)
        out.edited.append((rem_old[i], rem_new[j], r))
    out.removed = [p for i, p in enumerate(rem_old) if i not in used_o]
    out.added = [p for j, p in enumerate(rem_new) if j not in used_n]
    out.edited.sort(key=lambda e: e[2])  # most heavily edited first
    return out


def inline_edit(old: str, new: str) -> str:
    """Word-level diff: unchanged words plain, [-removed-] and {+added+}."""
    a, b = old.split(), new.split()
    ka, kb = [_norm(w) for w in a], [_norm(w) for w in b]  # a year bump alone isn't an edit
    parts = []
    for op, i1, i2, j1, j2 in SequenceMatcher(None, ka, kb, autojunk=False).get_opcodes():
        if op == "equal":
            parts.append(" ".join(b[j1:j2]))
        if op in ("delete", "replace"):
            parts.append("[-" + " ".join(a[i1:i2]) + "-]")
        if op in ("insert", "replace"):
            parts.append("{+" + " ".join(b[j1:j2]) + "+}")
    return " ".join(parts)


SECTION_NAMES = {"1a": "Risk Factors", "3": "Legal Proceedings", "7": "MD&A",
                 "9a": "Controls and Procedures"}


def build_payload(changes: list[SectionChanges], max_words: int) -> tuple[str, bool]:
    """Text the LLM reads. Edits and additions first, removals last, capped at max_words.

    Returns (payload, truncated).
    """
    budget = max_words
    truncated = False
    blocks: list[str] = []

    def take(text: str) -> str | None:
        nonlocal budget, truncated
        n = len(text.split())
        if n <= budget:
            budget -= n
            return text
        truncated = True
        return None

    per_section: dict[str, list[str]] = {c.section: [] for c in changes}
    # Pass 1: edits and additions, section by section (round-robin so one long MD&A can't hog it)
    queues = {c.section: [("EDITED", inline_edit(o, n)) for o, n, _ in c.edited] + [("ADDED", p) for p in c.added]
              for c in changes}
    removed = {c.section: [("REMOVED", p) for p in c.removed] for c in changes}
    for q in (queues, removed):
        while any(q.values()):
            for sec in list(q):
                if q[sec]:
                    tag, text = q[sec].pop(0)
                    got = take(f"{tag}: {text}")
                    if got:
                        per_section[sec].append(got)
    for c in changes:
        name = SECTION_NAMES.get(c.section, c.section)
        head = (f"## {name} (prior {c.old_words} words → now {c.new_words} words; "
                f"{len(c.added)} paragraphs added, {len(c.removed)} removed, {len(c.edited)} edited, "
                f"{c.unchanged} unchanged)")
        body = per_section[c.section] or ["(no substantive changes)"]
        blocks.append(head + "\n" + "\n".join(body))
    if truncated:
        blocks.append("(Some changes omitted for length.)")
    return "\n\n".join(blocks), truncated
