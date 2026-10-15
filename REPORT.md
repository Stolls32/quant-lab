# Quant Lab report

_Updated 2026-10-15 04:33 UTC · paper money only._

## Meme coins (Solana) — live paper trading

Running **3.4 days** · 942 market checks · last check 2026-10-15T04:33:10Z · each bot started with $10.00

| Bot | Equity | Return | Trades | Win % | Avg win / loss | Per-trade avg (95% CI) | Profit factor | Max DD | Open |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|
| `claude_analyst` _(off: no API key)_ | $10.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `volume_spike` | $9.42 | -5.8% | 13 | 31 | 36.2% / -20.6% | -3.1% (-19.2 to 20.6) | 0.78 | 25.0% | 1 |
| `hold_sol` | $9.18 | -8.2% | 0 | – | – | – | – | 10.3% | 1 |
| `dip_reclaim` | $9.12 | -8.8% | 6 | 33 | 13.4% / -15.5% | -5.9% (-17.6 to 6.1) | 0.43 | 16.8% | 0 |
| `random_control` | $5.27 | -47.3% | 45 | 24 | 20.5% / -11.7% | -3.8% (-8.9 to 1.9) | 0.57 | 51.1% | 3 |
| `momentum` | $0.87 | -91.3% | 25 | 24 | 23.8% / -31.0% | -17.9% (-30.1 to -5.2) | 0.28 | 92.0% | 0 |
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
| `dip_reclaim` | 2 | 3 | 1 | 0 | 0 | 0 |
| `fresh_launch` | 23 | 35 | 15 | 9 | 14 | 0 |
| `momentum` | 3 | 13 | 8 | 0 | 1 | 0 |
| `random_control` | 3 | 8 | 9 | 25 | 0 | 0 |
| `volume_spike` | 2 | 7 | 3 | 1 | 0 | 0 |

</details>

## Stocks & ETFs — live paper trading (daily)

_No runs yet. Needs Alpaca paper keys; see README._

