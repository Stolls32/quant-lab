# Quant Lab report

_Updated 2026-10-13 00:50 UTC · paper money only._

## Meme coins (Solana) — live paper trading

Running **1.3 days** · 356 market checks · last check 2026-10-13T00:50:02Z · each bot started with $10.00

| Bot | Equity | Return | Trades | Win % | Avg win / loss | Per-trade avg (95% CI) | Profit factor | Max DD | Open |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|
| `claude_analyst` _(off: no API key)_ | $10.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `dip_reclaim` | $10.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `volume_spike` | $9.85 | -1.5% | 4 | 50 | 13.5% / -20.5% | -3.5% (-20.5 to 13.5) | 0.66 | 10.3% | 0 |
| `hold_sol` | $9.16 | -8.4% | 0 | – | – | – | – | 8.6% | 1 |
| `fresh_launch` | $7.91 | -20.9% | 49 | 37 | 79.3% / -50.3% | -2.7% (-22.3 to 19.1) | 0.92 | 46.5% | 3 |
| `momentum` | $7.89 | -21.1% | 12 | 33 | 33.8% / -28.1% | -7.4% (-26.0 to 12.3) | 0.60 | 34.2% | 1 |
| `random_control` | $7.78 | -22.2% | 17 | 24 | 19.8% / -12.8% | -5.2% (-13.4 to 5.9) | 0.47 | 37.5% | 2 |

### Real-money gates (all must be ✅)

| Bot | 100+ trades | 30+ days | Profitable | Profitable at 2x costs | Edge CI above 0 | Beats coin flip | Beats holding SOL | Drawdown < 40% | Verdict |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| `claude_analyst` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `dip_reclaim` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `volume_spike` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | collecting data |
| `fresh_launch` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `momentum` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | collecting data |

_Coin-flip test = permutation test of per-trade returns vs. `random_control` (same tokens, exits and size, random entries). ✅ needs p < 0.010: 0.05 split across the 5 bots being tested, so one lucky bot out of several doesn't count as proof._

<details><summary>How positions closed</summary>

| Bot | take_profit | stop_loss | trailing_stop | time_exit | liquidity_pulled | vanished |
|---|---:|---:|---:|---:|---:|---:|
| `fresh_launch` | 14 | 15 | 9 | 3 | 8 | 0 |
| `momentum` | 3 | 5 | 4 | 0 | 0 | 0 |
| `random_control` | 1 | 4 | 4 | 8 | 0 | 0 |
| `volume_spike` | 1 | 2 | 1 | 0 | 0 | 0 |

</details>

## Stocks & ETFs — live paper trading (daily)

_No runs yet. Needs Alpaca paper keys; see README._

