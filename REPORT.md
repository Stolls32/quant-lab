# Quant Lab report

_Updated 2026-11-03 09:21 UTC · paper money only._

## Meme coins (Solana) — live paper trading

Running **5.6 days** · 1,487 market checks · last check 2026-11-03T09:21:10Z · each bot started with $100.00

> **Season 2.** All bots were reset with fresh paper money; gates and stats count this season only. Earlier seasons:
> - Season 1: 2026-10-11 to 2026-10-28, $10 per bot; ended with `fresh_launch`, `momentum`, `random_control`, `volume_spike` out of money. Archived in `data/crypto/archive/season-1/`.

| Bot | Equity | Return | Trades | Win % | Avg win / loss | Per-trade avg (95% CI) | Profit factor | Max DD | Open |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|
| `claude_analyst` _(off: no API key)_ | $100.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `dip_reclaim` | $97.86 | -2.1% | 12 | 50 | 12.2% / -10.5% | 0.8% (-6.5 to 7.7) | 1.16 | 11.7% | 1 |
| `hold_sol` | $89.51 | -10.5% | 0 | – | – | – | – | 11.8% | 1 |
| `random_control` | $12.61 | -87.4% | 79 | 30 | 22.6% / -17.9% | -5.6% (-11.5 to 0.1) | 0.60 | 89.2% | 1 |
| `volume_spike` | $2.02 | -98.0% | 35 | 20 | 22.6% / -20.5% | -11.9% (-19.6 to -3.9) | 0.13 | 98.9% | 0 |
| `momentum` | $0.46 | -99.5% | 35 | 20 | 36.7% / -30.6% | -17.2% (-26.8 to -6.6) | 0.31 | 99.5% | 0 |
| `fresh_launch` | $0.01 | -100.0% | 33 | 33 | 53.3% / -61.1% | -23.0% (-44.1 to -0.8) | 0.44 | 100.0% | 0 |

### Real-money gates (all must be ✅)

| Bot | 100+ trades | 30+ days | Profitable | Profitable at 2x costs | Edge CI above 0 | Beats coin flip | Beats holding SOL | Drawdown < 40% | Verdict |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| `claude_analyst` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `dip_reclaim` | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ | collecting data |
| `volume_spike` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `momentum` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `fresh_launch` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |

_Coin-flip test = permutation test of per-trade returns vs. `random_control` (same tokens, exits and size, random entries). ✅ needs p < 0.010: 0.05 split across the 5 bots being tested, so one lucky bot out of several doesn't count as proof._

<details><summary>How positions closed</summary>

| Bot | take_profit | stop_loss | trailing_stop | time_exit | liquidity_pulled | vanished |
|---|---:|---:|---:|---:|---:|---:|
| `dip_reclaim` | 5 | 3 | 3 | 1 | 0 | 0 |
| `fresh_launch` | 6 | 14 | 6 | 1 | 6 | 0 |
| `momentum` | 5 | 26 | 3 | 1 | 0 | 0 |
| `random_control` | 12 | 22 | 7 | 37 | 1 | 0 |
| `volume_spike` | 5 | 19 | 7 | 4 | 0 | 0 |

</details>

## Stocks & ETFs — live paper trading (daily)

_No runs yet. Needs Alpaca paper keys; see README._

