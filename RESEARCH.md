# Research notes: why these strategies, and how they fail

Every strategy here was chosen *before* seeing any results from this lab, and each
comes from published work or long-standing practice. That matters: if you try 200
ideas and keep the best one, you've found luck, not an edge.

---

## Part 1 — The traps this lab is built to avoid

**1. Backtest overfitting.** Search enough patterns and one will fit the past perfectly
and fail immediately after. A 2026 study of 749,816 pump.fun tokens is a perfect example:
a model predicting which tokens "graduate" scored an AUROC of 0.86 on its development
data, then **0.46, no better than a coin flip**, on the following period
([arXiv 2607.02823](https://arxiv.org/abs/2607.02823)). That's the most likely explanation
for a friend's "$100 → $12,000 simulation" too.
*Defense here:* fixed rules, forward testing on live data, a random-entry control bot,
and a multiple-testing correction on the pass/fail gates.

**2. Published edges shrink.** McLean & Pontiff, *"Does Academic Research Destroy Stock
Return Predictability?"* (Journal of Finance, 2016) found anomaly returns are roughly a
quarter lower out of sample and around half lower after publication.
*Defense:* treat backtest numbers as an upper bound; demand they hold in the 2nd half
of the data and in live paper trading.

**3. Testing many strategies at once.** With 5 bots each tested at p < 0.05, the chance
that at least one "passes" by pure luck is about 23%. Bailey & López de Prado
(*"The Deflated Sharpe Ratio"*, 2014; *"The Probability of Backtest Overfitting"*, 2015)
formalize this.
*Defense:* the coin-flip gate uses 0.05 ÷ number of bots (Bonferroni).

**4. Free fills.** Paper trading that fills at the screen price is fiction. Alpaca's own
docs say paper trading doesn't simulate market impact or latency slippage
([Alpaca paper trading docs](https://docs.alpaca.markets/docs/paper-trading)).
*Defense:* every simulated fill pays fees, latency slippage and price impact; gates
require profit even with costs doubled (crypto) or tripled (stock backtest).

**5. Survivorship bias.** Meme-coin history you can download today only contains coins
that still exist. Under 1% of pump.fun tokens even reached open trading in early 2025
([Cointelegraph, Mar 2025, Dune data](https://cointelegraph.com/news/pump-fun-memecoins-are-dying-at-record-rates-less-than-1-survive)).
A backtest on survivors is wildly optimistic.
*Defense:* no meme-coin backtest at all. Only forward testing on live data, where dead
coins are counted at $0.

---

## Part 2 — Meme-coin strategies (Solana, 5-minute checks)

What the evidence says: momentum is the best-documented return pattern in crypto
(Liu & Tsyvinski, *"Risks and Returns of Cryptocurrency"*, Review of Financial Studies 2021;
Liu, Tsyvinski & Wu, *"Common Risk Factors in Cryptocurrency"*, Journal of Finance 2022).
But that research covers established coins, not tokens that are hours old. For meme coins
there is **no credible published evidence of a durable edge**, which is exactly why this is
an experiment and not a plan.

| Bot | Idea | Main way it fails |
|---|---|---|
| `momentum` | Short-term momentum continues briefly in tokens with real volume and more buyers than sellers | Late entry right before insiders sell; reversals gap through stops |
| `dip_reclaim` | Tokens up on the day that pull back hard often bounce | "Catching a falling knife" when the pullback is the start of a dump |
| `fresh_launch` | Early buyers of the few launches that survive capture huge moves | Rug pulls and bot competition; most launches go to zero |
| `volume_spike` | A sudden burst of volume vs. the hour's pace precedes moves | Wash trading and paid bots fake volume |
| `claude_analyst` | An LLM weighing all signals together beats fixed rules | Plausible-sounding reasoning with no predictive power; tested directly by the score journal |
| `random_control` | Coin flip: random entries, same exits | It's the null hypothesis. Others must beat it |
| `hold_sol` | Just own SOL | Benchmark only |

**Costs used** (`lab/crypto/config.py`): 1% fee + 1.5% latency slippage per side, AMM price
impact ≈ 2 × size ÷ liquidity, $0.01 network fee per transaction. Roughly 5% per round trip.
To break even at that cost, a bot winning as often as it loses needs average wins about
5 percentage points bigger than its average losses.

**Safety screen** (`lab/crypto/safety.py`): skips tokens with thin liquidity, almost no
sellers (possible honeypot), one-sided flow, valuation far above pool depth, or a candle
that's already gone vertical. Open positions are force-sold if liquidity is pulled, and a
token that disappears from the data is booked at $0.

---

## Part 3 — Stock & ETF strategies (daily)

These are the opposite of meme coins: decades of evidence, cheap to trade, and much
harder to beat the index with. The realistic goal for most of them is **similar returns
with smaller crashes**, not getting rich faster than the S&P 500.

| Strategy | Source | What it's for | Known weakness |
|---|---|---|---|
| `trend_spy` | Faber, *"A Quantitative Approach to Tactical Asset Allocation"* (2007), 10-month/200-day moving-average timing | Sidestepping long bear markets | Whipsaws in choppy markets; lags in V-shaped recoveries |
| `dual_momentum` | Antonacci, *"Risk Premia Harvesting Through Dual Momentum"* (2012) and *Dual Momentum Investing* (2014) | Owning the stronger of US vs. international stocks, bonds in downtrends | Monthly checks react slowly to sudden crashes |
| `sector_momentum` | Jegadeesh & Titman (1993) momentum; Moskowitz & Grinblatt, *"Do Industries Explain Momentum?"* (1999) | Riding leading sectors | Momentum crashes at sharp market turns |
| `rsi2_reversion` | Connors & Alvarez, *Short Term Trading Strategies That Work* (2009) | Buying short, sharp dips in uptrends | Small edge per trade, so very cost-sensitive; widely known |
| `random_control` | Null hypothesis for `rsi2_reversion` | Shows whether the RSI signal matters | — |
| `buy_hold_spy` | Benchmark | The thing to beat | — |

Time-series momentum across asset classes is documented in Moskowitz, Ooi & Pedersen,
*"Time Series Momentum"* (Journal of Financial Economics, 2012).

**Costs used:** 5 basis points (0.05%) per side, fills at next day's open. The backtest
also reruns everything at 15 bp to see what survives.

---

## Part 4 — What "proven" means here

A bot or strategy is a **real-money candidate** only when every gate in REPORT.md is green:

*Meme coins:* 100+ closed trades, 30+ days, profitable, still profitable with costs doubled,
95% confidence interval of per-trade return above zero, beats the random control after the
multiple-testing correction, beats holding SOL, max drawdown under 40%.

*Stocks:* passes the backtest checks (positive in both halves, better risk-adjusted return
than SPY in the 2nd half, smaller drawdown) **and** 6+ months of live paper trading with
better Sharpe than SPY and drawdown no worse.

Expect most bots to fail. A clean "no edge" result is a real finding and saves you from
losing actual money. If one does pass, the next step is small real money with an adult's
account, and the gates keep running on the live results.

---

## Part 5 — Filing-change signal (pre-registered 2026-11-12, before any returns were looked at)

**Hypothesis.** When a small, thinly covered company changes what its 10-K says about its
risks, lawsuits, business or internal controls, the stock under-reacts, and the price keeps
drifting for months afterwards. This builds on Cohen, Malloy & Nguyen, *"Lazy Prices"*
(Journal of Finance, 2020), which found that companies whose annual reports change from one
year to the next go on to underperform, and that the market doesn't price this in when the
report comes out.

**What's new here.** That paper measured *how much* the wording changed. An LLM can read
*what* changed and judge whether it's bad: a new covenant waiver is not the same as a
reworded cybersecurity paragraph that every company added that year. If Claude's score
doesn't beat the word-overlap baseline, the LLM isn't worth paying for and we use the
free baseline instead.

**Why a small trader could have an edge here.** The universe is companies with a $10M–$300M
public float. Big funds can't buy enough of them to matter, few analysts cover them, and
very few people read their filings closely.

**Pipeline** (`run_filings.py`, code in `lab/filings/`):
1. Universe: public float from each 10-K's cover page, via SEC XBRL "frames". It's
   point-in-time and includes companies that later went bankrupt, so the universe itself
   has no survivorship bias. SPACs (SIC 6770) and commodity pools (SIC 6221) are excluded.
2. Consecutive 10-K pairs filed 9–15 months apart.
3. Sections compared: 1A Risk Factors, 3 Legal Proceedings, 7 MD&A, 9A Controls and
   Procedures. A section is compared only if it was found in both years.
4. Paragraph diff that ignores year bumps, quote styles, bullets, page footers and
   financial-table rows. Other number changes still count (a customer going from 40% to
   65% of revenue matters).
5. Anonymize: company names (current and former), tickers, URLs and absolute years
   are removed (years become relative: [FY+0], [FY-1]).
6. Claude scores the changes from −5 to +5, with materiality (0–3) and tags.

**Signals tested (fixed now):**
- `cosine_all`: the "Lazy Prices" baseline, with no LLM. Lower means more change.
- `llm_score`: Claude's −5 to +5 score.
- Flag changes: going-concern and material-weakness language appearing or disappearing.

**The test (fixed now):**
- Entry: buy at the open on the 2nd trading day after the filing date. Exit: at the
  close 63 trading days (about 3 months) later.
- Main measure: within each filing season, the average market-adjusted return of the top
  fifth of companies minus the bottom fifth, ranked by each signal. Long-only version:
  the top fifth minus the whole universe (shorting small stocks is expensive or impossible).
- Costs: 1% per round trip, because small stocks have wide bid-ask spreads.
- Pass bar: the spread is positive with a t-statistic above 3 (the hurdle Harvey, Liu &
  Zhu, *"...and the Cross-Section of Expected Returns"*, 2016, propose for new factors),
  it's positive in both halves of the validation period, and the LLM score adds
  significant information over `cosine_all` when both are in the same regression.

**Periods (by filing date):**
| Period | Dates | Use |
|---|---|---|
| development | 2012–2018 | Debug the pipeline and tune the payload and prompt. Returns may be looked at. |
| validation | 2019 – June 2026 | Run once, after the design is frozen. No tuning afterwards. |
| holdout | July 2026 onward | After the scoring model's training cutoff. The only fully clean test of the LLM score. The first big batch is the Feb–Apr 2027 10-K season. |

Extraction was debugged on a sample of 2023 filings, which fall in the validation period.
No returns were looked at.

**Known problems and how they're handled:**
1. *The model may know the future.* Claude was trained on text written after most of these
   filings. Anonymization lowers the risk, and the recognition probe (`run_filings.py
   probe`) measures it: if the model names the company in more than about 10% of probes,
   treat pre-cutoff LLM results as untrustworthy and rely on the holdout.
2. *Era clues.* Mentions of COVID or a specific law reveal the year even with dates masked,
   and the model knows how markets went in that year. The probe reports how far off its
   year guesses are.
3. *Prices for companies that no longer exist.* Free price feeds mostly drop delisted
   stocks, but failing companies are exactly where this signal should work best. Phase 2
   has to find prices for delisted companies, or the backtest will be too optimistic.
4. *Smaller reporting companies may omit Item 1A* ("not required"). Those pairs are compared
   on the other sections only.
5. *Heading parsing is heuristic.* Check `sections_found` in `changes.csv` and spot-check
   payloads before trusting a large run.

**Sample run, 2026-11-12:** 30 random companies from the mid-2022 universe of 1,881. After
removing SPACs, commodity pools and companies without a consecutive 10-K, 20 pairs were
usable, and 19 of them had all four sections. The cheap flags alone caught real events:
one company's going-concern doubt appeared, and another's material weakness and
going-concern language both disappeared ("were not effective" became "are effective").
Scoring cost estimate: about $0.002 per pair with Haiku 5.5 (about 16K input tokens), so
roughly $3.50 for a full year of the universe, or half that with the Batch API.
