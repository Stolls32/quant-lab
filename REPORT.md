# Quant Lab report

_Updated 2026-10-15 13:03 UTC · paper money only._

## Meme coins (Solana) — live paper trading

Running **3.8 days** · 1,039 market checks · last check 2026-10-15T13:03:49Z · each bot started with $10.00

| Bot | Equity | Return | Trades | Win % | Avg win / loss | Per-trade avg (95% CI) | Profit factor | Max DD | Open |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|
| `claude_analyst` _(off: no API key)_ | $10.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `dip_reclaim` | $9.12 | -8.8% | 6 | 33 | 13.4% / -15.5% | -5.9% (-17.6 to 6.1) | 0.43 | 16.8% | 0 |
| `hold_sol` | $8.98 | -10.2% | 0 | – | – | – | – | 10.4% | 1 |
| `volume_spike` | $8.17 | -18.3% | 15 | 27 | 36.2% / -21.9% | -6.4% (-21.9 to 14.2) | 0.60 | 34.9% | 0 |
| `random_control` | $7.72 | -22.8% | 54 | 28 | 23.7% / -11.7% | -1.8% (-7.3 to 4.0) | 0.79 | 51.1% | 0 |
| `momentum` | $0.91 | -90.9% | 29 | 28 | 23.4% / -30.4% | -15.6% (-26.9 to -4.1) | 0.30 | 92.5% | 0 |
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
| `momentum` | 4 | 15 | 9 | 0 | 1 | 0 |
| `random_control` | 6 | 10 | 11 | 27 | 0 | 0 |
| `volume_spike` | 2 | 8 | 3 | 2 | 0 | 0 |

</details>

## Stocks & ETFs — live paper trading (daily)

_No runs yet. Needs Alpaca paper keys; see README._

