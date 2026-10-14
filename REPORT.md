# Quant Lab report

_Updated 2026-10-14 12:22 UTC · paper money only._

## Meme coins (Solana) — live paper trading

Running **2.8 days** · 762 market checks · last check 2026-10-14T12:22:02Z · each bot started with $10.00

| Bot | Equity | Return | Trades | Win % | Avg win / loss | Per-trade avg (95% CI) | Profit factor | Max DD | Open |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|
| `volume_spike` | $11.20 | +12.0% | 8 | 38 | 47.7% / -19.0% | 6.0% (-18.2 to 40.9) | 1.50 | 10.8% | 0 |
| `claude_analyst` _(off: no API key)_ | $10.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `hold_sol` | $9.52 | -4.8% | 0 | – | – | – | – | 9.3% | 1 |
| `dip_reclaim` | $8.76 | -12.4% | 5 | 20 | 12.7% / -15.5% | -9.9% (-20.9 to 2.7) | 0.20 | 16.8% | 0 |
| `random_control` | $7.06 | -29.4% | 36 | 25 | 21.5% / -11.8% | -3.5% (-9.5 to 3.1) | 0.60 | 37.5% | 3 |
| `momentum` | $4.15 | -58.5% | 19 | 26 | 28.0% / -26.7% | -12.3% (-25.0 to 1.6) | 0.37 | 64.5% | 0 |
| `fresh_launch` | $0.90 | -91.0% | 93 | 39 | 65.5% / -53.0% | -7.1% (-20.7 to 6.8) | 0.78 | 93.9% | 1 |

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
| `fresh_launch` | 23 | 32 | 15 | 9 | 14 | 0 |
| `momentum` | 3 | 9 | 7 | 0 | 0 | 0 |
| `random_control` | 3 | 7 | 9 | 17 | 0 | 0 |
| `volume_spike` | 2 | 4 | 2 | 0 | 0 | 0 |

</details>

## Stocks & ETFs — live paper trading (daily)

_No runs yet. Needs Alpaca paper keys; see README._

