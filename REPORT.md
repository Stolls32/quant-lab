# Quant Lab report

_Updated 2026-10-13 19:06 UTC · paper money only._

## Meme coins (Solana) — live paper trading

Running **2.0 days** · 566 market checks · last check 2026-10-13T19:06:01Z · each bot started with $10.00

| Bot | Equity | Return | Trades | Win % | Avg win / loss | Per-trade avg (95% CI) | Profit factor | Max DD | Open |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|
| `claude_analyst` _(off: no API key)_ | $10.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `hold_sol` | $9.55 | -4.5% | 0 | – | – | – | – | 9.3% | 1 |
| `volume_spike` | $9.40 | -6.0% | 4 | 50 | 13.5% / -20.5% | -3.5% (-20.5 to 13.5) | 0.66 | 10.3% | 1 |
| `dip_reclaim` | $8.32 | -16.8% | 3 | 0 | 0.0% / -20.2% | -20.2% (-23.0 to -17.0) | 0.00 | 16.8% | 1 |
| `random_control` | $8.07 | -19.3% | 28 | 29 | 22.8% / -11.2% | -1.5% (-8.8 to 7.1) | 0.81 | 37.5% | 3 |
| `momentum` | $7.89 | -21.1% | 13 | 38 | 28.0% / -28.1% | -6.5% (-24.3 to 12.4) | 0.62 | 34.2% | 0 |
| `fresh_launch` | $7.26 | -27.4% | 73 | 40 | 70.3% / -51.2% | -2.9% (-19.3 to 13.7) | 0.91 | 50.9% | 1 |

### Real-money gates (all must be ✅)

| Bot | 100+ trades | 30+ days | Profitable | Profitable at 2x costs | Edge CI above 0 | Beats coin flip | Beats holding SOL | Drawdown < 40% | Verdict |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| `claude_analyst` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `volume_spike` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | collecting data |
| `dip_reclaim` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | collecting data |
| `momentum` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | collecting data |
| `fresh_launch` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |

_Coin-flip test = permutation test of per-trade returns vs. `random_control` (same tokens, exits and size, random entries). ✅ needs p < 0.010: 0.05 split across the 5 bots being tested, so one lucky bot out of several doesn't count as proof._

<details><summary>How positions closed</summary>

| Bot | take_profit | stop_loss | trailing_stop | time_exit | liquidity_pulled | vanished |
|---|---:|---:|---:|---:|---:|---:|
| `dip_reclaim` | 0 | 3 | 0 | 0 | 0 | 0 |
| `fresh_launch` | 20 | 23 | 13 | 6 | 11 | 0 |
| `momentum` | 3 | 5 | 5 | 0 | 0 | 0 |
| `random_control` | 3 | 6 | 8 | 11 | 0 | 0 |
| `volume_spike` | 1 | 2 | 1 | 0 | 0 | 0 |

</details>

## Stocks & ETFs — live paper trading (daily)

_No runs yet. Needs Alpaca paper keys; see README._

