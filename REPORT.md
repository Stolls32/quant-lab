# Quant Lab report

_Updated 2026-10-31 01:36 UTC · paper money only._

## Meme coins (Solana) — live paper trading

Running **2.3 days** · 601 market checks · last check 2026-10-31T01:36:18Z · each bot started with $100.00

> **Season 2.** All bots were reset with fresh paper money; gates and stats count this season only. Earlier seasons:
> - Season 1: 2026-10-11 to 2026-10-28, $10 per bot; ended with `fresh_launch`, `momentum`, `random_control`, `volume_spike` out of money. Archived in `data/crypto/archive/season-1/`.

| Bot | Equity | Return | Trades | Win % | Avg win / loss | Per-trade avg (95% CI) | Profit factor | Max DD | Open |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|
| `dip_reclaim` | $105.06 | +5.1% | 4 | 50 | 14.8% / -4.7% | 5.1% (-4.7 to 14.8) | 3.17 | 4.8% | 0 |
| `claude_analyst` _(off: no API key)_ | $100.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `hold_sol` | $93.84 | -6.2% | 0 | – | – | – | – | 9.9% | 1 |
| `random_control` | $92.95 | -7.0% | 31 | 35 | 26.9% / -15.7% | -0.6% (-9.7 to 8.6) | 0.94 | 34.9% | 2 |
| `volume_spike` | $54.29 | -45.7% | 13 | 8 | 23.6% / -17.2% | -14.1% (-21.2 to -5.4) | 0.11 | 45.7% | 0 |
| `momentum` | $2.74 | -97.3% | 26 | 19 | 42.8% / -32.2% | -17.8% (-29.7 to -4.6) | 0.31 | 98.2% | 1 |
| `fresh_launch` | $0.01 | -100.0% | 33 | 33 | 53.3% / -61.1% | -23.0% (-44.1 to -0.8) | 0.44 | 100.0% | 0 |

### Real-money gates (all must be ✅)

| Bot | 100+ trades | 30+ days | Profitable | Profitable at 2x costs | Edge CI above 0 | Beats coin flip | Beats holding SOL | Drawdown < 40% | Verdict |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| `dip_reclaim` | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ | collecting data |
| `claude_analyst` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `volume_spike` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `momentum` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `fresh_launch` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |

_Coin-flip test = permutation test of per-trade returns vs. `random_control` (same tokens, exits and size, random entries). ✅ needs p < 0.010: 0.05 split across the 5 bots being tested, so one lucky bot out of several doesn't count as proof._

<details><summary>How positions closed</summary>

| Bot | take_profit | stop_loss | trailing_stop | time_exit | liquidity_pulled | vanished |
|---|---:|---:|---:|---:|---:|---:|
| `dip_reclaim` | 2 | 0 | 1 | 1 | 0 | 0 |
| `fresh_launch` | 6 | 14 | 6 | 1 | 6 | 0 |
| `momentum` | 4 | 20 | 2 | 0 | 0 | 0 |
| `random_control` | 7 | 7 | 4 | 13 | 0 | 0 |
| `volume_spike` | 1 | 8 | 2 | 2 | 0 | 0 |

</details>

## Stocks & ETFs — live paper trading (daily)

_No runs yet. Needs Alpaca paper keys; see README._

