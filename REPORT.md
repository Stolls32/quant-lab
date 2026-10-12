# Quant Lab report

_Updated 2026-10-12 22:35 UTC · paper money only._

## Meme coins (Solana) — live paper trading

Running **1.2 days** · 329 market checks · last check 2026-10-12T22:35:02Z · each bot started with $10.00

| Bot | Equity | Return | Trades | Win % | Avg win / loss | Per-trade avg (95% CI) | Profit factor | Max DD | Open |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|
| `fresh_launch` | $12.20 | +22.0% | 43 | 42 | 79.3% / -51.0% | 3.6% (-18.3 to 26.7) | 1.12 | 36.1% | 1 |
| `claude_analyst` _(off: no API key)_ | $10.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `dip_reclaim` | $10.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `volume_spike` | $9.55 | -4.5% | 3 | 33 | 22.9% / -20.5% | -6.0% (-20.9 to 22.9) | 0.56 | 10.3% | 0 |
| `hold_sol` | $9.45 | -5.5% | 0 | – | – | – | – | 5.8% | 1 |
| `momentum` | $7.59 | -24.1% | 10 | 30 | 33.1% / -28.0% | -9.7% (-29.1 to 12.2) | 0.51 | 30.2% | 0 |
| `random_control` | $6.90 | -31.0% | 15 | 20 | 4.0% / -12.0% | -8.8% (-14.2 to -3.5) | 0.08 | 36.3% | 1 |

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
| `fresh_launch` | 14 | 12 | 8 | 3 | 7 | 0 |
| `momentum` | 2 | 4 | 4 | 0 | 0 | 0 |
| `random_control` | 0 | 3 | 4 | 8 | 0 | 0 |
| `volume_spike` | 1 | 2 | 0 | 0 | 0 | 0 |

</details>

## Stocks & ETFs — live paper trading (daily)

_No runs yet. Needs Alpaca paper keys; see README._

