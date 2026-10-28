# Quant Lab report

_Updated 2026-10-28 23:09 UTC · paper money only._

## Meme coins (Solana) — live paper trading

Running **0.2 days** · 55 market checks · last check 2026-10-28T23:09:23Z · each bot started with $100.00

> **Season 2.** All bots were reset with fresh paper money; gates and stats count this season only. Earlier seasons:
> - Season 1: 2026-10-11 to 2026-10-28, $10 per bot; ended with `fresh_launch`, `momentum`, `random_control`, `volume_spike` out of money. Archived in `data/crypto/archive/season-1/`.

| Bot | Equity | Return | Trades | Win % | Avg win / loss | Per-trade avg (95% CI) | Profit factor | Max DD | Open |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|
| `random_control` | $107.76 | +7.8% | 1 | 100 | 45.3% / 0.0% | 45.3% (– to –) | ∞ | 3.2% | 2 |
| `claude_analyst` _(off: no API key)_ | $100.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `dip_reclaim` | $100.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `hold_sol` | $99.65 | -0.4% | 0 | – | – | – | – | 1.2% | 1 |
| `volume_spike` | $97.29 | -2.7% | 0 | – | – | – | – | 2.7% | 1 |
| `momentum` | $96.20 | -3.8% | 3 | 33 | 71.6% / -43.4% | -5.1% (-50.2 to 71.6) | 0.83 | 25.5% | 0 |
| `fresh_launch` | $67.41 | -32.6% | 14 | 43 | 45.4% / -61.2% | -15.5% (-46.1 to 17.0) | 0.56 | 46.6% | 0 |

### Real-money gates (all must be ✅)

| Bot | 100+ trades | 30+ days | Profitable | Profitable at 2x costs | Edge CI above 0 | Beats coin flip | Beats holding SOL | Drawdown < 40% | Verdict |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| `claude_analyst` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `dip_reclaim` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `volume_spike` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `momentum` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | collecting data |
| `fresh_launch` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |

_Coin-flip test = permutation test of per-trade returns vs. `random_control` (same tokens, exits and size, random entries). ✅ needs p < 0.010: 0.05 split across the 5 bots being tested, so one lucky bot out of several doesn't count as proof._

<details><summary>How positions closed</summary>

| Bot | take_profit | stop_loss | trailing_stop | time_exit | liquidity_pulled | vanished |
|---|---:|---:|---:|---:|---:|---:|
| `fresh_launch` | 3 | 7 | 2 | 1 | 1 | 0 |
| `momentum` | 1 | 2 | 0 | 0 | 0 | 0 |
| `random_control` | 1 | 0 | 0 | 0 | 0 | 0 |

</details>

## Stocks & ETFs — live paper trading (daily)

_No runs yet. Needs Alpaca paper keys; see README._

