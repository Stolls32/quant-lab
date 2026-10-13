# Quant Lab report

_Updated 2026-10-13 19:41 UTC · paper money only._

## Meme coins (Solana) — live paper trading

Running **2.1 days** · 573 market checks · last check 2026-10-13T19:41:01Z · each bot started with $10.00

| Bot | Equity | Return | Trades | Win % | Avg win / loss | Per-trade avg (95% CI) | Profit factor | Max DD | Open |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|
| `volume_spike` | $12.55 | +25.5% | 5 | 60 | 47.7% / -20.5% | 20.4% (-15.6 to 70.3) | 3.49 | 10.3% | 0 |
| `claude_analyst` _(off: no API key)_ | $10.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `hold_sol` | $9.52 | -4.8% | 0 | – | – | – | – | 9.3% | 1 |
| `dip_reclaim` | $8.80 | -12.0% | 4 | 25 | 12.7% / -20.2% | -12.0% (-21.8 to 4.4) | 0.21 | 16.8% | 0 |
| `random_control` | $8.26 | -17.4% | 28 | 29 | 22.8% / -11.2% | -1.5% (-8.8 to 7.1) | 0.81 | 37.5% | 3 |
| `momentum` | $6.84 | -31.6% | 14 | 36 | 28.0% / -29.6% | -9.0% (-25.2 to 9.0) | 0.53 | 37.1% | 0 |
| `fresh_launch` | $5.93 | -40.7% | 74 | 39 | 70.3% / -52.2% | -4.2% (-20.6 to 12.6) | 0.87 | 59.9% | 0 |

### Real-money gates (all must be ✅)

| Bot | 100+ trades | 30+ days | Profitable | Profitable at 2x costs | Edge CI above 0 | Beats coin flip | Beats holding SOL | Drawdown < 40% | Verdict |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| `volume_spike` | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | collecting data |
| `claude_analyst` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `dip_reclaim` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | collecting data |
| `momentum` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | collecting data |
| `fresh_launch` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |

_Coin-flip test = permutation test of per-trade returns vs. `random_control` (same tokens, exits and size, random entries). ✅ needs p < 0.010: 0.05 split across the 5 bots being tested, so one lucky bot out of several doesn't count as proof._

<details><summary>How positions closed</summary>

| Bot | take_profit | stop_loss | trailing_stop | time_exit | liquidity_pulled | vanished |
|---|---:|---:|---:|---:|---:|---:|
| `dip_reclaim` | 1 | 3 | 0 | 0 | 0 | 0 |
| `fresh_launch` | 20 | 23 | 13 | 6 | 12 | 0 |
| `momentum` | 3 | 6 | 5 | 0 | 0 | 0 |
| `random_control` | 3 | 6 | 8 | 11 | 0 | 0 |
| `volume_spike` | 2 | 2 | 1 | 0 | 0 | 0 |

</details>

## Stocks & ETFs — live paper trading (daily)

_No runs yet. Needs Alpaca paper keys; see README._

