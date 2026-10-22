# Quant Lab report

_Updated 2026-10-22 22:25 UTC · paper money only._

## Meme coins (Solana) — live paper trading

Running **11.2 days** · 3,045 market checks · last check 2026-10-22T22:24:56Z · each bot started with $10.00

| Bot | Equity | Return | Trades | Win % | Avg win / loss | Per-trade avg (95% CI) | Profit factor | Max DD | Open |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|
| `claude_analyst` _(off: no API key)_ | $10.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `hold_sol` | $9.15 | -8.5% | 0 | – | – | – | – | 11.1% | 1 |
| `dip_reclaim` | $5.14 | -48.6% | 23 | 26 | 19.5% / -18.4% | -8.5% (-18.0 to 0.4) | 0.38 | 54.8% | 1 |
| `volume_spike` | $3.68 | -63.2% | 47 | 28 | 35.1% / -22.6% | -6.6% (-15.2 to 3.1) | 0.60 | 70.7% | 0 |
| `random_control` | $0.86 | -91.4% | 110 | 30 | 26.1% / -15.6% | -3.1% (-7.4 to 1.4) | 0.62 | 95.0% | 0 |
| `momentum` | $0.48 | -95.2% | 32 | 28 | 24.4% / -30.3% | -14.9% (-25.4 to -3.6) | 0.31 | 95.6% | 0 |
| `fresh_launch` | $0.12 | -98.8% | 96 | 38 | 65.5% / -52.9% | -8.5% (-21.9 to 5.8) | 0.77 | 99.2% | 0 |

### Real-money gates (all must be ✅)

| Bot | 100+ trades | 30+ days | Profitable | Profitable at 2x costs | Edge CI above 0 | Beats coin flip | Beats holding SOL | Drawdown < 40% | Verdict |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| `claude_analyst` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `dip_reclaim` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `volume_spike` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `momentum` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `fresh_launch` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |

_Coin-flip test = permutation test of per-trade returns vs. `random_control` (same tokens, exits and size, random entries). ✅ needs p < 0.010: 0.05 split across the 5 bots being tested, so one lucky bot out of several doesn't count as proof._

<details><summary>How positions closed</summary>

| Bot | take_profit | stop_loss | trailing_stop | time_exit | liquidity_pulled | vanished |
|---|---:|---:|---:|---:|---:|---:|
| `dip_reclaim` | 6 | 11 | 5 | 1 | 0 | 0 |
| `fresh_launch` | 23 | 35 | 15 | 9 | 14 | 0 |
| `momentum` | 5 | 17 | 9 | 0 | 1 | 0 |
| `random_control` | 16 | 31 | 16 | 47 | 0 | 0 |
| `volume_spike` | 10 | 25 | 7 | 5 | 0 | 0 |

</details>

## Stocks & ETFs — live paper trading (daily)

_No runs yet. Needs Alpaca paper keys; see README._

