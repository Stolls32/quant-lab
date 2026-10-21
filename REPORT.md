# Quant Lab report

_Updated 2026-10-21 23:48 UTC · paper money only._

## Meme coins (Solana) — live paper trading

Running **10.2 days** · 2,786 market checks · last check 2026-10-21T23:48:25Z · each bot started with $10.00

| Bot | Equity | Return | Trades | Win % | Avg win / loss | Per-trade avg (95% CI) | Profit factor | Max DD | Open |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|
| `claude_analyst` _(off: no API key)_ | $10.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `hold_sol` | $9.45 | -5.5% | 0 | – | – | – | – | 11.1% | 1 |
| `dip_reclaim` | $6.58 | -34.2% | 20 | 25 | 20.2% / -15.4% | -6.5% (-13.5 to 1.7) | 0.44 | 35.3% | 1 |
| `volume_spike` | $5.46 | -45.4% | 40 | 30 | 33.8% / -22.8% | -5.8% (-15.3 to 4.7) | 0.65 | 67.0% | 2 |
| `random_control` | $1.66 | -83.4% | 103 | 29 | 27.0% / -15.1% | -2.8% (-7.3 to 1.8) | 0.63 | 95.0% | 1 |
| `momentum` | $0.48 | -95.2% | 32 | 28 | 24.4% / -30.3% | -14.9% (-25.4 to -3.6) | 0.31 | 95.6% | 0 |
| `fresh_launch` | $0.12 | -98.8% | 96 | 38 | 65.5% / -52.9% | -8.5% (-21.9 to 5.8) | 0.77 | 99.2% | 0 |

### Real-money gates (all must be ✅)

| Bot | 100+ trades | 30+ days | Profitable | Profitable at 2x costs | Edge CI above 0 | Beats coin flip | Beats holding SOL | Drawdown < 40% | Verdict |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| `claude_analyst` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `dip_reclaim` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | collecting data |
| `volume_spike` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `momentum` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `fresh_launch` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |

_Coin-flip test = permutation test of per-trade returns vs. `random_control` (same tokens, exits and size, random entries). ✅ needs p < 0.010: 0.05 split across the 5 bots being tested, so one lucky bot out of several doesn't count as proof._

<details><summary>How positions closed</summary>

| Bot | take_profit | stop_loss | trailing_stop | time_exit | liquidity_pulled | vanished |
|---|---:|---:|---:|---:|---:|---:|
| `dip_reclaim` | 5 | 10 | 4 | 1 | 0 | 0 |
| `fresh_launch` | 23 | 35 | 15 | 9 | 14 | 0 |
| `momentum` | 5 | 17 | 9 | 0 | 1 | 0 |
| `random_control` | 15 | 28 | 15 | 45 | 0 | 0 |
| `volume_spike` | 9 | 22 | 5 | 4 | 0 | 0 |

</details>

## Stocks & ETFs — live paper trading (daily)

_No runs yet. Needs Alpaca paper keys; see README._

