# Quant Lab report

_Updated 2026-10-14 04:16 UTC · paper money only._

## Meme coins (Solana) — live paper trading

Running **2.4 days** · 665 market checks · last check 2026-10-14T04:16:40Z · each bot started with $10.00

| Bot | Equity | Return | Trades | Win % | Avg win / loss | Per-trade avg (95% CI) | Profit factor | Max DD | Open |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|
| `volume_spike` | $11.88 | +18.8% | 6 | 50 | 47.7% / -22.7% | 12.5% (-17.8 to 56.1) | 2.10 | 10.3% | 0 |
| `claude_analyst` _(off: no API key)_ | $10.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `hold_sol` | $9.51 | -4.9% | 0 | – | – | – | – | 9.3% | 1 |
| `dip_reclaim` | $8.80 | -12.0% | 4 | 25 | 12.7% / -20.2% | -12.0% (-21.8 to 4.4) | 0.21 | 16.8% | 0 |
| `random_control` | $7.40 | -26.0% | 32 | 28 | 21.5% / -12.1% | -2.7% (-9.6 to 5.2) | 0.69 | 37.5% | 3 |
| `momentum` | $5.17 | -48.3% | 17 | 29 | 28.0% / -27.8% | -11.4% (-25.2 to 3.8) | 0.42 | 52.4% | 0 |
| `fresh_launch` | $2.30 | -77.0% | 85 | 38 | 68.6% / -52.8% | -7.1% (-21.4 to 7.3) | 0.80 | 91.7% | 0 |

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
| `fresh_launch` | 22 | 28 | 14 | 7 | 14 | 0 |
| `momentum` | 3 | 8 | 6 | 0 | 0 | 0 |
| `random_control` | 3 | 7 | 9 | 13 | 0 | 0 |
| `volume_spike` | 2 | 3 | 1 | 0 | 0 | 0 |

</details>

## Stocks & ETFs — live paper trading (daily)

_No runs yet. Needs Alpaca paper keys; see README._

