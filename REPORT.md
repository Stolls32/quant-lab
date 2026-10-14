# Quant Lab report

_Updated 2026-10-14 10:32 UTC · paper money only._

## Meme coins (Solana) — live paper trading

Running **2.7 days** · 740 market checks · last check 2026-10-14T10:32:02Z · each bot started with $10.00

| Bot | Equity | Return | Trades | Win % | Avg win / loss | Per-trade avg (95% CI) | Profit factor | Max DD | Open |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|
| `volume_spike` | $11.88 | +18.8% | 6 | 50 | 47.7% / -22.7% | 12.5% (-17.8 to 56.1) | 2.10 | 10.3% | 0 |
| `claude_analyst` _(off: no API key)_ | $10.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `hold_sol` | $9.44 | -5.6% | 0 | – | – | – | – | 9.3% | 1 |
| `dip_reclaim` | $8.76 | -12.4% | 5 | 20 | 12.7% / -15.5% | -9.9% (-20.9 to 2.7) | 0.20 | 16.8% | 0 |
| `random_control` | $6.94 | -30.6% | 35 | 26 | 21.5% / -11.6% | -3.1% (-9.1 to 4.0) | 0.64 | 37.5% | 3 |
| `momentum` | $4.25 | -57.5% | 18 | 28 | 28.0% / -28.5% | -12.8% (-26.2 to 2.1) | 0.38 | 60.9% | 0 |
| `fresh_launch` | $2.51 | -74.9% | 90 | 39 | 65.9% / -53.0% | -6.8% (-20.1 to 7.7) | 0.80 | 91.7% | 1 |

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
| `fresh_launch` | 23 | 30 | 15 | 8 | 14 | 0 |
| `momentum` | 3 | 9 | 6 | 0 | 0 | 0 |
| `random_control` | 3 | 7 | 9 | 16 | 0 | 0 |
| `volume_spike` | 2 | 3 | 1 | 0 | 0 | 0 |

</details>

## Stocks & ETFs — live paper trading (daily)

_No runs yet. Needs Alpaca paper keys; see README._

