# Quant Lab report

_Updated 2026-10-12 17:54 UTC · paper money only._

## Meme coins (Solana) — live paper trading

Running **1.0 days** · 277 market checks · last check 2026-10-12T17:54:44Z · each bot started with $10.00

| Bot | Equity | Return | Trades | Win % | Avg win / loss | Per-trade avg (95% CI) | Profit factor | Max DD | Open |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|
| `fresh_launch` | $12.59 | +25.9% | 29 | 45 | 74.3% / -51.7% | 4.8% (-22.9 to 32.9) | 1.17 | 26.8% | 2 |
| `claude_analyst` _(off: no API key)_ | $10.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `dip_reclaim` | $10.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `hold_sol` | $9.51 | -4.9% | 0 | – | – | – | – | 5.3% | 1 |
| `volume_spike` | $8.97 | -10.3% | 2 | 0 | 0.0% / -20.5% | -20.5% (-20.9 to -20.2) | 0.00 | 10.3% | 0 |
| `momentum` | $7.93 | -20.7% | 6 | 33 | 19.8% / -30.4% | -13.7% (-38.0 to 10.8) | 0.32 | 28.2% | 1 |
| `random_control` | $7.17 | -28.3% | 12 | 25 | 4.0% / -11.6% | -7.7% (-14.2 to -2.1) | 0.11 | 28.8% | 3 |

### Real-money gates (all must be ✅)

| Bot | 100+ trades | 30+ days | Profitable | Profitable at 2x costs | Edge CI above 0 | Beats coin flip | Beats holding SOL | Drawdown < 40% | Verdict |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| `fresh_launch` | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ | collecting data |
| `claude_analyst` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `dip_reclaim` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `volume_spike` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | collecting data |
| `momentum` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | collecting data |

_Coin-flip test = permutation test of per-trade returns vs. `random_control` (same tokens, exits and size, random entries). ✅ needs p < 0.010: 0.05 split across the 5 bots being tested, so one lucky bot out of several doesn't count as proof._

<details><summary>How positions closed</summary>

| Bot | take_profit | stop_loss | trailing_stop | time_exit | liquidity_pulled | vanished |
|---|---:|---:|---:|---:|---:|---:|
| `fresh_launch` | 9 | 7 | 6 | 2 | 5 | 0 |
| `momentum` | 1 | 3 | 2 | 0 | 0 | 0 |
| `random_control` | 0 | 2 | 3 | 7 | 0 | 0 |
| `volume_spike` | 0 | 2 | 0 | 0 | 0 | 0 |

</details>

## Stocks & ETFs — live paper trading (daily)

_No runs yet. Needs Alpaca paper keys; see README._

