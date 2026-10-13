# Quant Lab report

_Updated 2026-10-13 15:56 UTC · paper money only._

## Meme coins (Solana) — live paper trading

Running **1.9 days** · 528 market checks · last check 2026-10-13T15:56:01Z · each bot started with $10.00

| Bot | Equity | Return | Trades | Win % | Avg win / loss | Per-trade avg (95% CI) | Profit factor | Max DD | Open |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|
| `claude_analyst` _(off: no API key)_ | $10.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `random_control` | $9.78 | -2.2% | 25 | 32 | 22.8% / -10.3% | 0.3% (-7.8 to 9.3) | 1.04 | 37.5% | 3 |
| `volume_spike` | $9.65 | -3.5% | 4 | 50 | 13.5% / -20.5% | -3.5% (-20.5 to 13.5) | 0.66 | 10.3% | 0 |
| `dip_reclaim` | $9.48 | -5.2% | 1 | 0 | 0.0% / -20.6% | -20.6% (– to –) | 0.00 | 5.2% | 0 |
| `hold_sol` | $9.45 | -5.5% | 0 | – | – | – | – | 9.3% | 1 |
| `fresh_launch` | $8.71 | -12.9% | 69 | 41 | 69.2% / -51.6% | -2.6% (-19.4 to 14.2) | 0.91 | 50.7% | 1 |
| `momentum` | $7.89 | -21.1% | 13 | 38 | 28.0% / -28.1% | -6.5% (-24.3 to 12.4) | 0.62 | 34.2% | 0 |

### Real-money gates (all must be ✅)

| Bot | 100+ trades | 30+ days | Profitable | Profitable at 2x costs | Edge CI above 0 | Beats coin flip | Beats holding SOL | Drawdown < 40% | Verdict |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| `claude_analyst` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `volume_spike` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | collecting data |
| `dip_reclaim` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | collecting data |
| `fresh_launch` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `momentum` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | collecting data |

_Coin-flip test = permutation test of per-trade returns vs. `random_control` (same tokens, exits and size, random entries). ✅ needs p < 0.010: 0.05 split across the 5 bots being tested, so one lucky bot out of several doesn't count as proof._

<details><summary>How positions closed</summary>

| Bot | take_profit | stop_loss | trailing_stop | time_exit | liquidity_pulled | vanished |
|---|---:|---:|---:|---:|---:|---:|
| `dip_reclaim` | 0 | 1 | 0 | 0 | 0 | 0 |
| `fresh_launch` | 19 | 20 | 13 | 6 | 11 | 0 |
| `momentum` | 3 | 5 | 5 | 0 | 0 | 0 |
| `random_control` | 3 | 4 | 8 | 10 | 0 | 0 |
| `volume_spike` | 1 | 2 | 1 | 0 | 0 | 0 |

</details>

## Stocks & ETFs — live paper trading (daily)

_No runs yet. Needs Alpaca paper keys; see README._

