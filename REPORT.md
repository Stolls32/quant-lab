# Quant Lab report

_Updated 2026-10-15 11:08 UTC · paper money only._

## Meme coins (Solana) — live paper trading

Running **3.7 days** · 1,016 market checks · last check 2026-10-15T11:08:29Z · each bot started with $10.00

| Bot | Equity | Return | Trades | Win % | Avg win / loss | Per-trade avg (95% CI) | Profit factor | Max DD | Open |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|
| `claude_analyst` _(off: no API key)_ | $10.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `dip_reclaim` | $9.12 | -8.8% | 6 | 33 | 13.4% / -15.5% | -5.9% (-17.6 to 6.1) | 0.43 | 16.8% | 0 |
| `hold_sol` | $9.04 | -9.6% | 0 | – | – | – | – | 10.4% | 1 |
| `volume_spike` | $8.17 | -18.3% | 15 | 27 | 36.2% / -21.9% | -6.4% (-21.9 to 14.2) | 0.60 | 34.9% | 0 |
| `random_control` | $6.41 | -35.9% | 50 | 26 | 20.0% / -11.6% | -3.4% (-8.4 to 2.1) | 0.61 | 51.1% | 1 |
| `momentum` | $1.28 | -87.2% | 27 | 30 | 23.4% / -31.0% | -14.9% (-26.8 to -2.4) | 0.31 | 92.5% | 0 |
| `fresh_launch` | $0.12 | -98.8% | 96 | 38 | 65.5% / -52.9% | -8.5% (-21.9 to 5.8) | 0.77 | 99.2% | 0 |

### Real-money gates (all must be ✅)

| Bot | 100+ trades | 30+ days | Profitable | Profitable at 2x costs | Edge CI above 0 | Beats coin flip | Beats holding SOL | Drawdown < 40% | Verdict |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| `claude_analyst` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `dip_reclaim` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | collecting data |
| `volume_spike` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | collecting data |
| `momentum` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `fresh_launch` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |

_Coin-flip test = permutation test of per-trade returns vs. `random_control` (same tokens, exits and size, random entries). ✅ needs p < 0.010: 0.05 split across the 5 bots being tested, so one lucky bot out of several doesn't count as proof._

<details><summary>How positions closed</summary>

| Bot | take_profit | stop_loss | trailing_stop | time_exit | liquidity_pulled | vanished |
|---|---:|---:|---:|---:|---:|---:|
| `dip_reclaim` | 2 | 3 | 1 | 0 | 0 | 0 |
| `fresh_launch` | 23 | 35 | 15 | 9 | 14 | 0 |
| `momentum` | 4 | 13 | 9 | 0 | 1 | 0 |
| `random_control` | 4 | 9 | 10 | 27 | 0 | 0 |
| `volume_spike` | 2 | 8 | 3 | 2 | 0 | 0 |

</details>

## Stocks & ETFs — live paper trading (daily)

_No runs yet. Needs Alpaca paper keys; see README._

