# Quant Lab report

_Updated 2026-10-14 13:27 UTC · paper money only._

## Meme coins (Solana) — live paper trading

Running **2.8 days** · 775 market checks · last check 2026-10-14T13:27:02Z · each bot started with $10.00

| Bot | Equity | Return | Trades | Win % | Avg win / loss | Per-trade avg (95% CI) | Profit factor | Max DD | Open |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|
| `volume_spike` | $11.20 | +12.0% | 8 | 38 | 47.7% / -19.0% | 6.0% (-18.2 to 40.9) | 1.50 | 10.8% | 0 |
| `claude_analyst` _(off: no API key)_ | $10.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `hold_sol` | $9.28 | -7.2% | 0 | – | – | – | – | 9.3% | 1 |
| `dip_reclaim` | $8.76 | -12.4% | 5 | 20 | 12.7% / -15.5% | -9.9% (-20.9 to 2.7) | 0.20 | 16.8% | 0 |
| `random_control` | $6.35 | -36.5% | 37 | 24 | 21.5% / -11.6% | -3.6% (-9.4 to 3.1) | 0.59 | 37.5% | 2 |
| `momentum` | $3.53 | -64.7% | 20 | 25 | 28.0% / -26.6% | -12.9% (-25.2 to -0.1) | 0.35 | 67.5% | 0 |
| `fresh_launch` | $0.54 | -94.6% | 94 | 38 | 65.5% / -52.7% | -7.4% (-21.0 to 6.5) | 0.78 | 96.3% | 1 |

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
| `dip_reclaim` | 1 | 3 | 1 | 0 | 0 | 0 |
| `fresh_launch` | 23 | 33 | 15 | 9 | 14 | 0 |
| `momentum` | 3 | 10 | 7 | 0 | 0 | 0 |
| `random_control` | 3 | 7 | 9 | 18 | 0 | 0 |
| `volume_spike` | 2 | 4 | 2 | 0 | 0 | 0 |

</details>

## Stocks & ETFs — live paper trading (daily)

_No runs yet. Needs Alpaca paper keys; see README._

