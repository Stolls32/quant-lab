# Quant Lab report

_Updated 2026-11-01 03:27 UTC · paper money only._

## Meme coins (Solana) — live paper trading

Running **3.4 days** · 895 market checks · last check 2026-11-01T03:27:34Z · each bot started with $100.00

> **Season 2.** All bots were reset with fresh paper money; gates and stats count this season only. Earlier seasons:
> - Season 1: 2026-10-11 to 2026-10-28, $10 per bot; ended with `fresh_launch`, `momentum`, `random_control`, `volume_spike` out of money. Archived in `data/crypto/archive/season-1/`.

| Bot | Equity | Return | Trades | Win % | Avg win / loss | Per-trade avg (95% CI) | Profit factor | Max DD | Open |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|
| `dip_reclaim` | $100.21 | +0.2% | 8 | 50 | 11.6% / -11.3% | 0.1% (-8.8 to 8.8) | 1.02 | 6.3% | 0 |
| `claude_analyst` _(off: no API key)_ | $100.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `random_control` | $95.85 | -4.2% | 48 | 38 | 23.7% / -15.1% | -0.6% (-7.8 to 6.4) | 0.95 | 46.8% | 3 |
| `hold_sol` | $92.80 | -7.2% | 0 | – | – | – | – | 9.9% | 1 |
| `volume_spike` | $25.79 | -74.2% | 21 | 14 | 8.3% / -18.0% | -14.3% (-19.2 to -8.4) | 0.08 | 74.2% | 0 |
| `momentum` | $0.46 | -99.5% | 35 | 20 | 36.7% / -30.6% | -17.2% (-26.8 to -6.6) | 0.31 | 99.5% | 0 |
| `fresh_launch` | $0.01 | -100.0% | 33 | 33 | 53.3% / -61.1% | -23.0% (-44.1 to -0.8) | 0.44 | 100.0% | 0 |

### Real-money gates (all must be ✅)

| Bot | 100+ trades | 30+ days | Profitable | Profitable at 2x costs | Edge CI above 0 | Beats coin flip | Beats holding SOL | Drawdown < 40% | Verdict |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| `dip_reclaim` | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ | collecting data |
| `claude_analyst` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `volume_spike` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `momentum` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `fresh_launch` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |

_Coin-flip test = permutation test of per-trade returns vs. `random_control` (same tokens, exits and size, random entries). ✅ needs p < 0.010: 0.05 split across the 5 bots being tested, so one lucky bot out of several doesn't count as proof._

<details><summary>How positions closed</summary>

| Bot | take_profit | stop_loss | trailing_stop | time_exit | liquidity_pulled | vanished |
|---|---:|---:|---:|---:|---:|---:|
| `dip_reclaim` | 3 | 2 | 2 | 1 | 0 | 0 |
| `fresh_launch` | 6 | 14 | 6 | 1 | 6 | 0 |
| `momentum` | 5 | 26 | 3 | 1 | 0 | 0 |
| `random_control` | 10 | 10 | 5 | 23 | 0 | 0 |
| `volume_spike` | 1 | 13 | 4 | 3 | 0 | 0 |

</details>

## Stocks & ETFs — live paper trading (daily)

_No runs yet. Needs Alpaca paper keys; see README._

