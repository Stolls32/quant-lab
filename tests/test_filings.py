"""Tests for the filing-change pipeline. Offline: no SEC or Anthropic calls.

Run with:  python -m unittest discover -s tests -v
"""
from __future__ import annotations

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lab.filings import diff as D  # noqa: E402
from lab.filings.anonymize import anonymize, name_aliases  # noqa: E402
from lab.filings.config import FilingsConfig, period_of  # noqa: E402
from lab.filings.edgar import Company, Filing  # noqa: E402
from lab.filings.pipeline import consecutive_pair  # noqa: E402
from lab.filings.score import estimate_cost, parse_score, probe_hit  # noqa: E402
from lab.filings.sections import extract_sections, flags, to_text  # noqa: E402

RISK = "Our business depends on a small number of customers and the loss of any one would hurt revenue."
DOC = f"""<html><head><title>10-K</title></head><body>
<div style="display:none"><ix:header><ix:hidden>dei:EntityRegistrantName ACME SECRET DATA</ix:hidden></ix:header></div>
<script>var x = 1;</script>
<p>TABLE OF CONTENTS</p>
<table><tr><td>Item 1A.</td><td>Risk Factors</td><td>12</td></tr>
<tr><td>Item 1B.</td><td>Unresolved Staff Comments</td><td>30</td></tr>
<tr><td>Item 7.</td><td>Management's Discussion and Analysis</td><td>40</td></tr>
<tr><td>Item 7A.</td><td>Quantitative and Qualitative Disclosures</td><td>50</td></tr></table>
<p>Item 1. Business</p><p>We make widgets in Ohio and sell them to retailers nationwide.</p>
<p>1A. Risk Factors</p>
<p>{RISK}</p>
<p>We may need additional financing, which may not be available on acceptable terms in fiscal 2023.</p>
<p>Acme Widget Corp. | 2023 Form 10-K | 14</p>
<p>Item 1B. Unresolved Staff Comments</p><p>None.</p>
<p>Item 7. Management&#8217;s Discussion and Analysis</p>
<p>Revenue increased 12% to $45.2 million as a result of higher unit volume across our channels.</p>
<table><tr><td>Total revenue</td><td>$</td><td>45,200</td><td>$</td><td>40,300</td></tr></table>
<p>7. Debt</p><p>This note numbering must not be mistaken for an item heading in the filing.</p>
<p>Item 7A. Quantitative and Qualitative Disclosures</p><p>Not applicable.</p>
<p>There is substantial doubt about our ability to continue as a going concern.</p>
</body></html>"""


class TestSections(unittest.TestCase):
    def setUp(self):
        self.text = to_text(DOC)

    def test_hidden_and_noise_removed(self):
        self.assertNotIn("SECRET", self.text)
        self.assertNotIn("var x", self.text)
        self.assertNotIn("Form 10-K | 14", self.text)
        self.assertNotIn("TABLE OF CONTENTS", self.text)

    def test_body_beats_table_of_contents(self):
        s = extract_sections(self.text, ("1a", "7"))
        self.assertIn(RISK, s["1a"])            # found via the bare "1A. Risk Factors" heading
        self.assertNotIn("Unresolved", s["1a"])  # stops at the next item
        self.assertIn("Revenue increased", s["7"])
        self.assertIn("note numbering", s["7"])  # "7. Debt" isn't a heading
        self.assertNotIn("Not applicable", s["7"])

    def test_flags(self):
        self.assertEqual(flags(self.text)["going_concern"], 1)


class TestDiff(unittest.TestCase):
    def test_year_bumps_quotes_and_bullets_are_not_changes(self):
        old = "• We expect to spend $3 million in fiscal 2022 on our company’s expansion plans.\nFiller line about stable ops here."
        new = "•We expect to spend $3 million in fiscal 2023 on our company's expansion plans.\nFiller line about stable ops here."
        c = D.compare("7", old, new)
        self.assertEqual((len(c.added), len(c.removed), len(c.edited), c.unchanged), (0, 0, 0, 2))

    def test_added_removed_edited(self):
        old = "\n".join([RISK, "We have no outstanding debt and ample cash for operations.",
                         "Our largest customer accounted for 40% of revenue last year."])
        new = "\n".join([RISK, "Our largest customer accounted for 65% of revenue last year.",
                         "Our lender has waived a covenant default, and the waiver expires soon."])
        c = D.compare("1a", old, new)
        self.assertEqual(c.unchanged, 1)
        self.assertEqual(len(c.edited), 1)
        self.assertIn("[-40%-] {+65%+}", D.inline_edit(*c.edited[0][:2]))
        self.assertEqual(c.added, ["Our lender has waived a covenant default, and the waiver expires soon."])
        self.assertEqual(c.removed, ["We have no outstanding debt and ample cash for operations."])

    def test_table_rows_ignored(self):
        self.assertEqual(D.paragraphs("Home sales $ 1,392,750 $ 936,400\nEquity in net income of ventures 149 1,262"), [])

    def test_similarity(self):
        self.assertAlmostEqual(D.cosine(RISK, RISK), 1.0)
        self.assertLess(D.cosine(RISK, "Completely unrelated sentence about weather patterns in spring."), 0.2)

    def test_payload_cap_and_order(self):
        c = D.compare("1a", "x " * 3, "\n".join(f"New risk number {i} about lenders and liquidity today." for i in range(50)))
        payload, truncated = D.build_payload([c], max_words=60)
        self.assertTrue(truncated)
        self.assertLessEqual(sum(len(l.split()) for l in payload.split("\n") if l.startswith("ADDED")), 60)


class TestAnonymize(unittest.TestCase):
    def test_names_tickers_years(self):
        text = ("Acme Widget Corp. (Nasdaq: AWC) and Acme's subsidiaries reported results for fiscal 2023, "
                "compared with 2022, as of January 1,2023. See www.acmewidget.com. The core ACME brand grew. "
                "Its Widget line too. Notes are due 2026. Ratio was 0.2019.")
        out = anonymize(text, ["Acme Widget Corp", "Acme Tools Inc"], ["AWC"], 2023)
        self.assertNotIn("Acme", out)
        self.assertNotIn("ACME", out)
        self.assertNotIn("AWC", out)
        self.assertIn("the Company's subsidiaries", out)
        self.assertIn("fiscal [FY+0], compared with [FY-1], as of January 1,[FY+0]", out)
        self.assertIn("due [FY+3]", out)
        self.assertIn("0.2019", out)
        self.assertIn("[URL]", out)
        self.assertNotIn("Widget line", out)

    def test_single_word_alias_only_when_capitalized(self):
        out = anonymize("Core Molding's core business is molding.", ["Core Molding Technologies Inc"], [], None)
        self.assertEqual(out, "the Company's core business is molding.")

    def test_short_ticker_only_in_exchange_context(self):
        out = anonymize("Listed on NYSE under the symbol: GE. A GE turbine.", [], ["GE"], None)
        self.assertIn("symbol: [TICKER]", out)
        self.assertIn("A GE turbine", out)

    def test_aliases(self):
        self.assertIn("El Pollo Loco", name_aliases(["El Pollo Loco Holdings, Inc."]))
        self.assertIn("Pollo", name_aliases(["El Pollo Loco Holdings, Inc."]))
        self.assertNotIn("Pharmaceuticals", name_aliases(["Rigel Pharmaceuticals Inc"]))


class TestPipelineBits(unittest.TestCase):
    def test_consecutive_pair(self):
        def f(acc, d, form="10-K"):
            return Filing(1, acc, form, d, d, "x.htm")
        co = Company(1, "X", [], [], 100, [f("a", "2021-03-01"), f("b", "2022-03-02"), f("c", "2022-05-01", "10-Q"),
                                            f("d", "2024-03-01")])
        self.assertEqual([x.accession for x in consecutive_pair(co, "b")], ["a", "b"])
        self.assertIsNone(consecutive_pair(co, "d"))  # gap of 2 years: not consecutive
        self.assertIsNone(consecutive_pair(co, "a"))  # nothing before it

    def test_periods(self):
        cfg = FilingsConfig()
        self.assertEqual(period_of("2015-03-01", cfg), "development")
        self.assertEqual(period_of("2026-06-30", cfg), "validation")
        self.assertEqual(period_of("2027-02-15", cfg), "holdout")

    def test_parse_score(self):
        ok = {"content": [{"type": "text", "text": '{"score": -3, "materiality": 2, "tags": ["liquidity", "bogus"], '
                                                     '"reason": "new covenant waiver"}'}],
              "usage": {"input_tokens": 900, "output_tokens": 40}}
        s = parse_score(ok)
        self.assertEqual((s.score, s.materiality, s.tags, s.input_tokens), (-3, 2, ["liquidity"], 900))
        self.assertIsNone(parse_score({"content": [{"type": "text", "text": '{"score": 9, "materiality": 1}'}]}))
        self.assertIsNone(parse_score({"content": [{"type": "text", "text": "I think it's bad"}]}))
        self.assertIsNone(parse_score(None))

    def test_cost(self):
        est = estimate_cost(["word " * 4000], 0.10, 0.50, 400)
        self.assertEqual(est["calls"], 1)
        self.assertLess(est["usd"], 0.01)

    def test_probe_hit(self):
        self.assertTrue(probe_hit("Probably Rigel Pharmaceuticals", ["RIGEL PHARMACEUTICALS INC"]))
        self.assertFalse(probe_hit("unknown", ["RIGEL PHARMACEUTICALS INC"]))
        self.assertFalse(probe_hit("Pfizer", ["RIGEL PHARMACEUTICALS INC"]))


if __name__ == "__main__":
    unittest.main()
