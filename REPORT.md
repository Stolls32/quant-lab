# Quant Lab report

_Updated 2026-10-23 10:56 UTC · paper money only._

## Meme coins (Solana) — live paper trading

Running **11.7 days** · 3,179 market checks · last check 2026-10-23T10:56:04Z · each bot started with $10.00

| Bot | Equity | Return | Trades | Win % | Avg win / loss | Per-trade avg (95% CI) | Profit factor | Max DD | Open |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|
| `claude_analyst` _(off: no API key)_ | $10.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `hold_sol` | $9.21 | -7.9% | 0 | – | – | – | – | 11.1% | 1 |
| `dip_reclaim` | $5.07 | -49.3% | 24 | 25 | 19.5% / -17.5% | -8.2% (-17.6 to 0.6) | 0.37 | 54.8% | 0 |
| `volume_spike` | $2.26 | -77.4% | 50 | 28 | 34.4% / -23.6% | -7.3% (-15.8 to 1.9) | 0.57 | 82.0% | 0 |
| `momentum` | $0.48 | -95.2% | 32 | 28 | 24.4% / -30.3% | -14.9% (-25.4 to -3.6) | 0.31 | 95.6% | 0 |
| `random_control` | $0.19 | -98.1% | 112 | 30 | 26.5% / -16.4% | -3.4% (-8.0 to 1.3) | 0.61 | 98.1% | 0 |
| `fresh_launch` | $0.12 | -98.8% | 96 | 38 | 65.5% / -52.9% | -8.5% (-21.9 to 5.8) | 0.77 | 99.2% | 0 |

### Real-money gates (all must be ✅)

| Bot | 100+ trades | 30+ days | Profitable | Profitable at 2x costs | Edge CI above 0 | Beats coin flip | Beats holding SOL | Drawdown < 40% | Verdict |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| `claude_analyst` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `dip_reclaim` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `volume_spike` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `momentum` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `fresh_launch` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |

_Coin-flip test = permutation test of per-trade returns vs. `random_control` (same tokens, exits and size, random entries). ✅ needs p < 0.010: 0.05 split across the 5 bots being tested, so one lucky bot out of several doesn't count as proof._

<details><summary>How positions closed</summary>

| Bot | take_profit | stop_loss | trailing_stop | time_exit | liquidity_pulled | vanished |
|---|---:|---:|---:|---:|---:|---:|
| `dip_reclaim` | 6 | 11 | 6 | 1 | 0 | 0 |
| `fresh_launch` | 23 | 35 | 15 | 9 | 14 | 0 |
| `momentum` | 5 | 17 | 9 | 0 | 1 | 0 |
| `random_control` | 17 | 32 | 16 | 47 | 0 | 0 |
| `volume_spike` | 11 | 27 | 7 | 5 | 0 | 0 |

</details>

## Stocks & ETFs — live paper trading (daily)

_No runs yet. Needs Alpaca paper keys; see README._

