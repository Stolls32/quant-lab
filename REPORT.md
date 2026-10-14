# Quant Lab report

_Updated 2026-10-14 02:01 UTC · paper money only._

## Meme coins (Solana) — live paper trading

Running **2.3 days** · 638 market checks · last check 2026-10-14T02:01:21Z · each bot started with $10.00

| Bot | Equity | Return | Trades | Win % | Avg win / loss | Per-trade avg (95% CI) | Profit factor | Max DD | Open |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|
| `volume_spike` | $12.07 | +20.7% | 6 | 50 | 47.7% / -22.7% | 12.5% (-17.8 to 56.1) | 2.10 | 10.3% | 0 |
| `claude_analyst` _(off: no API key)_ | $10.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `hold_sol` | $9.50 | -5.0% | 0 | – | – | – | – | 9.3% | 1 |
| `dip_reclaim` | $8.80 | -12.0% | 4 | 25 | 12.7% / -20.2% | -12.0% (-21.8 to 4.4) | 0.21 | 16.8% | 0 |
| `random_control` | $7.56 | -24.4% | 32 | 28 | 21.5% / -12.1% | -2.7% (-9.6 to 5.2) | 0.69 | 37.5% | 3 |
| `momentum` | $6.70 | -33.0% | 15 | 33 | 28.0% / -29.0% | -10.0% (-25.4 to 7.0) | 0.48 | 43.7% | 1 |
| `fresh_launch` | $2.34 | -76.6% | 82 | 38 | 68.5% / -52.7% | -6.9% (-21.8 to 8.4) | 0.80 | 90.9% | 2 |

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
| `fresh_launch` | 21 | 28 | 14 | 6 | 13 | 0 |
| `momentum` | 3 | 7 | 5 | 0 | 0 | 0 |
| `random_control` | 3 | 7 | 9 | 13 | 0 | 0 |
| `volume_spike` | 2 | 3 | 1 | 0 | 0 | 0 |

</details>

## Stocks & ETFs — live paper trading (daily)

_No runs yet. Needs Alpaca paper keys; see README._

