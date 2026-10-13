# Quant Lab report

_Updated 2026-10-13 17:51 UTC · paper money only._

## Meme coins (Solana) — live paper trading

Running **2.0 days** · 551 market checks · last check 2026-10-13T17:51:01Z · each bot started with $10.00

| Bot | Equity | Return | Trades | Win % | Avg win / loss | Per-trade avg (95% CI) | Profit factor | Max DD | Open |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|
| `claude_analyst` _(off: no API key)_ | $10.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `volume_spike` | $9.65 | -3.5% | 4 | 50 | 13.5% / -20.5% | -3.5% (-20.5 to 13.5) | 0.66 | 10.3% | 0 |
| `hold_sol` | $9.49 | -5.1% | 0 | – | – | – | – | 9.3% | 1 |
| `random_control` | $8.94 | -10.6% | 27 | 30 | 22.8% / -10.6% | -0.7% (-8.2 to 7.8) | 0.91 | 37.5% | 3 |
| `dip_reclaim` | $8.93 | -10.7% | 2 | 0 | 0.0% / -18.8% | -18.8% (-20.6 to -17.0) | 0.00 | 11.0% | 1 |
| `fresh_launch` | $8.40 | -16.0% | 71 | 41 | 70.3% / -51.9% | -2.0% (-18.1 to 14.6) | 0.94 | 50.7% | 1 |
| `momentum` | $7.89 | -21.1% | 13 | 38 | 28.0% / -28.1% | -6.5% (-24.3 to 12.4) | 0.62 | 34.2% | 0 |

### Real-money gates (all must be ✅)

| Bot | 100+ trades | 30+ days | Profitable | Profitable at 2x costs | Edge CI above 0 | Beats coin flip | Beats holding SOL | Drawdown < 40% | Verdict |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| `claude_analyst` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `volume_spike` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | collecting data |
| `dip_reclaim` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | collecting data |
| `fresh_launch` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `momentum` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | collecting data |

_Coin-flip test = permutation test of per-trade returns vs. `random_control` (same tokens, exits and size, random entries). ✅ needs p < 0.010: 0.05 split across the 5 bots being tested, so one lucky bot out of several doesn't count as proof._

<details><summary>How positions closed</summary>

| Bot | take_profit | stop_loss | trailing_stop | time_exit | liquidity_pulled | vanished |
|---|---:|---:|---:|---:|---:|---:|
| `dip_reclaim` | 0 | 2 | 0 | 0 | 0 | 0 |
| `fresh_launch` | 20 | 21 | 13 | 6 | 11 | 0 |
| `momentum` | 3 | 5 | 5 | 0 | 0 | 0 |
| `random_control` | 3 | 5 | 8 | 11 | 0 | 0 |
| `volume_spike` | 1 | 2 | 1 | 0 | 0 | 0 |

</details>

## Stocks & ETFs — live paper trading (daily)

_No runs yet. Needs Alpaca paper keys; see README._

