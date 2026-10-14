# Quant Lab report

_Updated 2026-10-14 23:12 UTC · paper money only._

## Meme coins (Solana) — live paper trading

Running **3.2 days** · 883 market checks · last check 2026-10-14T23:12:47Z · each bot started with $10.00

| Bot | Equity | Return | Trades | Win % | Avg win / loss | Per-trade avg (95% CI) | Profit factor | Max DD | Open |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|
| `claude_analyst` _(off: no API key)_ | $10.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `volume_spike` | $9.70 | -3.0% | 11 | 27 | 47.7% / -20.5% | -1.9% (-20.9 to 25.3) | 0.87 | 23.8% | 2 |
| `hold_sol` | $9.22 | -7.8% | 0 | – | – | – | – | 9.3% | 1 |
| `dip_reclaim` | $8.76 | -12.4% | 5 | 20 | 12.7% / -15.5% | -9.9% (-20.9 to 2.7) | 0.20 | 16.8% | 0 |
| `random_control` | $5.15 | -48.5% | 42 | 21 | 21.5% / -12.0% | -4.8% (-10.2 to 1.2) | 0.50 | 50.6% | 3 |
| `momentum` | $1.27 | -87.3% | 24 | 25 | 23.8% / -31.0% | -17.3% (-29.7 to -3.9) | 0.29 | 88.3% | 0 |
| `fresh_launch` | $0.12 | -98.8% | 96 | 38 | 65.5% / -52.9% | -8.5% (-21.9 to 5.8) | 0.77 | 99.2% | 0 |

### Real-money gates (all must be ✅)

| Bot | 100+ trades | 30+ days | Profitable | Profitable at 2x costs | Edge CI above 0 | Beats coin flip | Beats holding SOL | Drawdown < 40% | Verdict |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| `claude_analyst` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `volume_spike` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | collecting data |
| `dip_reclaim` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | collecting data |
| `momentum` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `fresh_launch` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |

_Coin-flip test = permutation test of per-trade returns vs. `random_control` (same tokens, exits and size, random entries). ✅ needs p < 0.010: 0.05 split across the 5 bots being tested, so one lucky bot out of several doesn't count as proof._

<details><summary>How positions closed</summary>

| Bot | take_profit | stop_loss | trailing_stop | time_exit | liquidity_pulled | vanished |
|---|---:|---:|---:|---:|---:|---:|
| `dip_reclaim` | 1 | 3 | 1 | 0 | 0 | 0 |
| `fresh_launch` | 23 | 35 | 15 | 9 | 14 | 0 |
| `momentum` | 3 | 12 | 8 | 0 | 1 | 0 |
| `random_control` | 3 | 8 | 9 | 22 | 0 | 0 |
| `volume_spike` | 2 | 6 | 3 | 0 | 0 | 0 |

</details>

## Stocks & ETFs — live paper trading (daily)

_No runs yet. Needs Alpaca paper keys; see README._

