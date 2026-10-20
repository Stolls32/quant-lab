# Quant Lab report

_Updated 2026-10-20 02:20 UTC · paper money only._

## Meme coins (Solana) — live paper trading

Running **8.3 days** · 2,278 market checks · last check 2026-10-20T02:20:29Z · each bot started with $10.00

| Bot | Equity | Return | Trades | Win % | Avg win / loss | Per-trade avg (95% CI) | Profit factor | Max DD | Open |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|
| `claude_analyst` _(off: no API key)_ | $10.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `hold_sol` | $9.25 | -7.5% | 0 | – | – | – | – | 11.1% | 1 |
| `dip_reclaim` | $7.23 | -27.7% | 16 | 25 | 21.3% / -16.3% | -6.9% (-15.2 to 2.8) | 0.44 | 28.8% | 0 |
| `volume_spike` | $4.82 | -51.8% | 35 | 29 | 31.8% / -23.4% | -7.6% (-17.4 to 4.1) | 0.56 | 61.6% | 0 |
| `random_control` | $1.14 | -88.6% | 93 | 27 | 24.9% / -14.6% | -3.9% (-8.4 to 0.7) | 0.59 | 95.0% | 1 |
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
| `dip_reclaim` | 4 | 9 | 3 | 0 | 0 | 0 |
| `fresh_launch` | 23 | 35 | 15 | 9 | 14 | 0 |
| `momentum` | 5 | 17 | 9 | 0 | 1 | 0 |
| `random_control` | 12 | 25 | 15 | 41 | 0 | 0 |
| `volume_spike` | 7 | 20 | 4 | 4 | 0 | 0 |

</details>

## Stocks & ETFs — live paper trading (daily)

_No runs yet. Needs Alpaca paper keys; see README._

