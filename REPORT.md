# Quant Lab report

_Updated 2026-10-13 20:26 UTC · paper money only._

## Meme coins (Solana) — live paper trading

Running **2.1 days** · 582 market checks · last check 2026-10-13T20:26:01Z · each bot started with $10.00

| Bot | Equity | Return | Trades | Win % | Avg win / loss | Per-trade avg (95% CI) | Profit factor | Max DD | Open |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|
| `volume_spike` | $12.55 | +25.5% | 5 | 60 | 47.7% / -20.5% | 20.4% (-15.6 to 70.3) | 3.49 | 10.3% | 0 |
| `claude_analyst` _(off: no API key)_ | $10.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `hold_sol` | $9.48 | -5.2% | 0 | – | – | – | – | 9.3% | 1 |
| `dip_reclaim` | $8.80 | -12.0% | 4 | 25 | 12.7% / -20.2% | -12.0% (-21.8 to 4.4) | 0.21 | 16.8% | 0 |
| `random_control` | $7.40 | -26.0% | 29 | 28 | 22.8% / -11.5% | -2.1% (-9.1 to 6.2) | 0.75 | 37.5% | 3 |
| `momentum` | $6.84 | -31.6% | 14 | 36 | 28.0% / -29.6% | -9.0% (-25.2 to 9.0) | 0.53 | 37.1% | 0 |
| `fresh_launch` | $3.55 | -64.5% | 76 | 38 | 70.3% / -53.1% | -6.0% (-21.8 to 10.4) | 0.82 | 76.0% | 1 |

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
| `fresh_launch` | 20 | 24 | 13 | 6 | 13 | 0 |
| `momentum` | 3 | 6 | 5 | 0 | 0 | 0 |
| `random_control` | 3 | 6 | 8 | 12 | 0 | 0 |
| `volume_spike` | 2 | 2 | 1 | 0 | 0 | 0 |

</details>

## Stocks & ETFs — live paper trading (daily)

_No runs yet. Needs Alpaca paper keys; see README._

