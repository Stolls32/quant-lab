# Quant Lab

Automated trading bots for **Solana meme coins** and **US stocks/ETFs**, running on free
cloud infrastructure, with paper money, real market data, realistic costs, and a
scoreboard that tells you whether any bot has an edge or just got lucky.

Every bot uses the same code path it would use with real money. The only thing that
changes when a bot "graduates" is where the orders go.

```
                ┌──────────────── GitHub Actions (free, runs on its own) ────────────────┐
 every 5 min →  │ run_crypto.py  → DexScreener live data → 7 meme-coin bots → paper fills │
 10:05am ET  →  │ run_stocks.py  → Alpaca live data      → 6 stock bots     → paper fills │
 monthly     →  │ run_backtest.py→ 2016-today history    → BACKTEST.md                    │
                │                     ↓ results committed back to this repo               │
                └──────────────────────── REPORT.md (leaderboard + gates) ────────────────┘
                                                ↓
                          Claude reads it each morning and messages you
```

**What's inside**
- `lab/crypto/` — market data, rug/honeypot screen, cost model, 5 strategies + coin-flip control + hold-SOL benchmark, engine
- `lab/stocks/` — Alpaca data/broker client, 4 strategies + control + SPY benchmark, portfolio engine, backtester, live runner
- `lab/ai.py` — Claude as a trade analyst (optional), with a journal that measures whether its scores predict anything
- `lab/metrics.py` — bootstrap confidence intervals, permutation tests vs. the control, Sharpe/Sortino/drawdown
- `RESEARCH.md` — why each strategy exists, the evidence, and how each one fails. **Read this.**
- `tests/` — 18 tests, including a no-look-ahead check on the backtester

---

## Setup (about 15 minutes, once)

### 1. Try it offline first (optional, needs Python 3.11+)
```bash
python run_crypto.py --demo 2000      # 7 crypto bots on a fake market
python run_backtest.py --synthetic    # stock backtester on fake prices
python -m unittest discover -s tests  # all tests
```
Demo numbers are meaningless; the fake market has a pattern built in on purpose and
some bots find it. Real markets don't hand you that.

### 2. Create the GitHub repo
1. Make a free account at github.com.
2. **New repository** → name it `quant-lab` → **Public** (Actions are free for public
   repos; your keys stay private in Secrets either way) → Create.
3. **Add file → Upload files** → drag in everything from this folder, including the
   hidden `.github` folder (on a Mac press `Cmd+Shift+.` in Finder to see it) → Commit.

### 3. Get free Alpaca paper-trading keys (for the stock bots)
1. Sign up at alpaca.markets with an email. Paper-only accounts don't need ID or money.
2. In the dashboard, make sure you're on the **Paper** account, then generate API keys.

### 4. Add your keys to GitHub
Repo → **Settings → Secrets and variables → Actions → New repository secret**:

| Secret | Value | Needed for |
|---|---|---|
| `ALPACA_API_KEY` | Alpaca paper key ID | stock bots, backtest |
| `ALPACA_API_SECRET` | Alpaca paper secret | stock bots, backtest |
| `ANTHROPIC_API_KEY` | key from console.anthropic.com | `claude_analyst` bot only (optional, costs a little per call; capped at 150 calls/day in `lab/crypto/config.py`) |

Optional **Variable** (same page, Variables tab): `MIRROR_STRATEGY` = e.g. `dual_momentum`
places real orders in your Alpaca **paper** account matching that one strategy, as a dress
rehearsal with real order fills.

### 5. Turn it on
Repo → **Actions** tab → enable workflows if asked → open **stock-backtest** → **Run
workflow** (makes BACKTEST.md in a few minutes). The crypto bot starts by itself within
~5 minutes; the stock bot runs at 10:05am New York each trading day.

That's it. Check **REPORT.md** in the repo any time. If GitHub ever shows a scheduled
workflow as paused, click **Enable workflow**.

---

## Reading REPORT.md
- **Leaderboard**: equity, return, win rate, average win vs. loss, and the per-trade
  average with a 95% confidence interval. If that interval includes 0, you can't tell the
  bot apart from luck yet.
- **Real-money gates**: a bot is a candidate only when *every* box is ✅. "Collecting
  data" means it hasn't had enough trades/days to judge.
- **Does Claude's judgment predict anything?**: compares what happened after tokens Claude
  rated 7-10 vs. 0-3. This answers the "train an AI on meme coins" question directly.

## Changing things
All numbers live in `lab/crypto/config.py` (costs, safety screen, budgets) and at the top
of each strategy class. Add a crypto bot by subclassing `Strategy` in
`lab/crypto/strategies.py` and adding it to `all_strategies()`; a stock bot by subclassing
`StockStrategy`. If you change costs or rules mid-experiment, write down the date: results
before and after aren't comparable.

## The road to real money (not built on purpose)
- **Stocks:** the same code trades a live Alpaca account by switching keys and
  `ALPACA_BASE_URL`, and refuses unless `LIVE_TRADING_CONFIRM` is set to the exact phrase in
  `lab/stocks/live.py`. Live brokerage accounts require an adult account holder.
- **Meme coins:** start by placing a graduated bot's signals by hand in a parent-owned
  account (Coinbase's in-app Solana DEX supports these tokens), with $10-$25 per bot. Full
  automation (a dedicated wallet plus a swap API) comes last, because a bug or leaked key can
  drain the wallet.
- Real-money results go through the same gates. If live results fall short of paper, stop.
