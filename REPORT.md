# Quant Lab report

_Updated 2026-10-31 15:02 UTC · paper money only._

## Meme coins (Solana) — live paper trading

Running **2.8 days** · 748 market checks · last check 2026-10-31T15:01:55Z · each bot started with $100.00

> **Season 2.** All bots were reset with fresh paper money; gates and stats count this season only. Earlier seasons:
> - Season 1: 2026-10-11 to 2026-10-28, $10 per bot; ended with `fresh_launch`, `momentum`, `random_control`, `volume_spike` out of money. Archived in `data/crypto/archive/season-1/`.

| Bot | Equity | Return | Trades | Win % | Avg win / loss | Per-trade avg (95% CI) | Profit factor | Max DD | Open |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|
| `dip_reclaim` | $106.76 | +6.8% | 6 | 67 | 11.6% / -4.7% | 6.2% (-1.4 to 12.8) | 4.97 | 5.4% | 1 |
| `claude_analyst` _(off: no API key)_ | $100.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `hold_sol` | $92.95 | -7.0% | 0 | – | – | – | – | 9.9% | 1 |
| `random_control` | $63.23 | -36.8% | 39 | 33 | 23.2% / -16.3% | -3.2% (-10.7 to 4.5) | 0.71 | 43.2% | 3 |
| `volume_spike` | $54.29 | -45.7% | 13 | 8 | 23.6% / -17.2% | -14.1% (-21.2 to -5.4) | 0.11 | 45.7% | 0 |
| `momentum` | $1.15 | -98.9% | 32 | 22 | 36.7% / -31.1% | -16.3% (-26.8 to -5.0) | 0.32 | 99.1% | 0 |
| `fresh_launch` | $0.01 | -100.0% | 33 | 33 | 53.3% / -61.1% | -23.0% (-44.1 to -0.8) | 0.44 | 100.0% | 0 |

### Real-money gates (all must be ✅)

| Bot | 100+ trades | 30+ days | Profitable | Profitable at 2x costs | Edge CI above 0 | Beats coin flip | Beats holding SOL | Drawdown < 40% | Verdict |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| `dip_reclaim` | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | collecting data |
| `claude_analyst` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `volume_spike` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `momentum` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `fresh_launch` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |

_Coin-flip test = permutation test of per-trade returns vs. `random_control` (same tokens, exits and size, random entries). ✅ needs p < 0.010: 0.05 split across the 5 bots being tested, so one lucky bot out of several doesn't count as proof._

<details><summary>How positions closed</summary>

| Bot | take_profit | stop_loss | trailing_stop | time_exit | liquidity_pulled | vanished |
|---|---:|---:|---:|---:|---:|---:|
| `dip_reclaim` | 3 | 0 | 2 | 1 | 0 | 0 |
| `fresh_launch` | 6 | 14 | 6 | 1 | 6 | 0 |
| `momentum` | 5 | 23 | 3 | 1 | 0 | 0 |
| `random_control` | 7 | 9 | 5 | 18 | 0 | 0 |
| `volume_spike` | 1 | 8 | 2 | 2 | 0 | 0 |

</details>

## Stocks & ETFs — live paper trading (daily)

_No runs yet. Needs Alpaca paper keys; see README._

