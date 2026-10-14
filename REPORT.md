# Quant Lab report

_Updated 2026-10-14 20:32 UTC · paper money only._

## Meme coins (Solana) — live paper trading

Running **3.1 days** · 851 market checks · last check 2026-10-14T20:32:47Z · each bot started with $10.00

| Bot | Equity | Return | Trades | Win % | Avg win / loss | Per-trade avg (95% CI) | Profit factor | Max DD | Open |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|
| `volume_spike` | $10.98 | +9.8% | 9 | 33 | 47.7% / -19.7% | 2.8% (-19.0 to 34.8) | 1.21 | 13.0% | 3 |
| `claude_analyst` _(off: no API key)_ | $10.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `hold_sol` | $9.21 | -7.9% | 0 | – | – | – | – | 9.3% | 1 |
| `dip_reclaim` | $8.76 | -12.4% | 5 | 20 | 12.7% / -15.5% | -9.9% (-20.9 to 2.7) | 0.20 | 16.8% | 0 |
| `random_control` | $5.43 | -45.7% | 40 | 22 | 21.5% / -12.1% | -4.5% (-10.1 to 1.9) | 0.52 | 50.6% | 3 |
| `momentum` | $1.74 | -82.6% | 22 | 23 | 28.0% / -31.2% | -17.7% (-31.4 to -3.4) | 0.30 | 85.1% | 1 |
| `fresh_launch` | $0.12 | -98.8% | 96 | 38 | 65.5% / -52.9% | -8.5% (-21.9 to 5.8) | 0.77 | 99.2% | 0 |

### Real-money gates (all must be ✅)

| Bot | 100+ trades | 30+ days | Profitable | Profitable at 2x costs | Edge CI above 0 | Beats coin flip | Beats holding SOL | Drawdown < 40% | Verdict |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| `volume_spike` | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ | collecting data |
| `claude_analyst` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `dip_reclaim` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | collecting data |
| `momentum` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `fresh_launch` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |

_Coin-flip test = permutation test of per-trade returns vs. `random_control` (same tokens, exits and size, random entries). ✅ needs p < 0.010: 0.05 split across the 5 bots being tested, so one lucky bot out of several doesn't count as proof._

<details><summary>How positions closed</summary>

| Bot | take_profit | stop_loss | trailing_stop | time_exit | liquidity_pulled | vanished |
|---|---:|---:|---:|---:|---:|---:|
| `dip_reclaim` | 1 | 3 | 1 | 0 | 0 | 0 |
| `fresh_launch` | 23 | 35 | 15 | 9 | 14 | 0 |
| `momentum` | 3 | 11 | 7 | 0 | 1 | 0 |
| `random_control` | 3 | 8 | 9 | 20 | 0 | 0 |
| `volume_spike` | 2 | 5 | 2 | 0 | 0 | 0 |

</details>

## Stocks & ETFs — live paper trading (daily)

_No runs yet. Needs Alpaca paper keys; see README._

