# Quant Lab report

_Updated 2026-10-13 00:05 UTC · paper money only._

## Meme coins (Solana) — live paper trading

Running **1.2 days** · 347 market checks · last check 2026-10-13T00:05:02Z · each bot started with $10.00

| Bot | Equity | Return | Trades | Win % | Avg win / loss | Per-trade avg (95% CI) | Profit factor | Max DD | Open |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|
| `fresh_launch` | $10.43 | +4.3% | 46 | 39 | 79.3% / -50.1% | 0.5% (-21.3 to 23.3) | 1.02 | 36.1% | 2 |
| `claude_analyst` _(off: no API key)_ | $10.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `dip_reclaim` | $10.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `volume_spike` | $9.41 | -5.9% | 3 | 33 | 22.9% / -20.5% | -6.0% (-20.9 to 22.9) | 0.56 | 10.3% | 1 |
| `hold_sol` | $9.33 | -6.7% | 0 | – | – | – | – | 6.9% | 1 |
| `random_control` | $8.03 | -19.7% | 16 | 25 | 19.8% / -12.0% | -4.0% (-12.9 to 7.5) | 0.55 | 37.5% | 1 |
| `momentum` | $7.77 | -22.3% | 12 | 33 | 33.8% / -28.1% | -7.4% (-26.0 to 12.3) | 0.60 | 34.2% | 0 |

### Real-money gates (all must be ✅)

| Bot | 100+ trades | 30+ days | Profitable | Profitable at 2x costs | Edge CI above 0 | Beats coin flip | Beats holding SOL | Drawdown < 40% | Verdict |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| `fresh_launch` | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ | collecting data |
| `claude_analyst` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `dip_reclaim` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `volume_spike` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | collecting data |
| `momentum` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | collecting data |

_Coin-flip test = permutation test of per-trade returns vs. `random_control` (same tokens, exits and size, random entries). ✅ needs p < 0.010: 0.05 split across the 5 bots being tested, so one lucky bot out of several doesn't count as proof._

<details><summary>How positions closed</summary>

| Bot | take_profit | stop_loss | trailing_stop | time_exit | liquidity_pulled | vanished |
|---|---:|---:|---:|---:|---:|---:|
| `fresh_launch` | 14 | 14 | 8 | 3 | 7 | 0 |
| `momentum` | 3 | 5 | 4 | 0 | 0 | 0 |
| `random_control` | 1 | 3 | 4 | 8 | 0 | 0 |
| `volume_spike` | 1 | 2 | 0 | 0 | 0 | 0 |

</details>

## Stocks & ETFs — live paper trading (daily)

_No runs yet. Needs Alpaca paper keys; see README._

