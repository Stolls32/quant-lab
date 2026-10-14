# Quant Lab report

_Updated 2026-10-14 01:11 UTC · paper money only._

## Meme coins (Solana) — live paper trading

Running **2.3 days** · 628 market checks · last check 2026-10-14T01:11:21Z · each bot started with $10.00

| Bot | Equity | Return | Trades | Win % | Avg win / loss | Per-trade avg (95% CI) | Profit factor | Max DD | Open |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|
| `volume_spike` | $12.34 | +23.4% | 5 | 60 | 47.7% / -20.5% | 20.4% (-15.6 to 70.3) | 3.49 | 10.3% | 1 |
| `claude_analyst` _(off: no API key)_ | $10.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `hold_sol` | $9.47 | -5.3% | 0 | – | – | – | – | 9.3% | 1 |
| `dip_reclaim` | $8.80 | -12.0% | 4 | 25 | 12.7% / -20.2% | -12.0% (-21.8 to 4.4) | 0.21 | 16.8% | 0 |
| `random_control` | $7.84 | -21.6% | 31 | 26 | 22.8% / -12.1% | -3.1% (-10.0 to 4.7) | 0.66 | 37.5% | 3 |
| `momentum` | $6.25 | -37.5% | 15 | 33 | 28.0% / -29.0% | -10.0% (-25.4 to 7.0) | 0.48 | 42.4% | 0 |
| `fresh_launch` | $2.86 | -71.4% | 81 | 38 | 68.5% / -53.0% | -6.5% (-21.6 to 9.3) | 0.81 | 90.9% | 2 |

### Real-money gates (all must be ✅)

| Bot | 100+ trades | 30+ days | Profitable | Profitable at 2x costs | Edge CI above 0 | Beats coin flip | Beats holding SOL | Drawdown < 40% | Verdict |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| `volume_spike` | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | collecting data |
| `claude_analyst` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `dip_reclaim` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | collecting data |
| `momentum` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `fresh_launch` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |

_Coin-flip test = permutation test of per-trade returns vs. `random_control` (same tokens, exits and size, random entries). ✅ needs p < 0.010: 0.05 split across the 5 bots being tested, so one lucky bot out of several doesn't count as proof._

<details><summary>How positions closed</summary>

| Bot | take_profit | stop_loss | trailing_stop | time_exit | liquidity_pulled | vanished |
|---|---:|---:|---:|---:|---:|---:|
| `dip_reclaim` | 1 | 3 | 0 | 0 | 0 | 0 |
| `fresh_launch` | 21 | 27 | 14 | 6 | 13 | 0 |
| `momentum` | 3 | 7 | 5 | 0 | 0 | 0 |
| `random_control` | 3 | 7 | 8 | 13 | 0 | 0 |
| `volume_spike` | 2 | 2 | 1 | 0 | 0 | 0 |

</details>

## Stocks & ETFs — live paper trading (daily)

_No runs yet. Needs Alpaca paper keys; see README._

