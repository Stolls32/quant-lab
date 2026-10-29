# Quant Lab report

_Updated 2026-10-29 03:29 UTC · paper money only._

## Meme coins (Solana) — live paper trading

Running **0.4 days** · 106 market checks · last check 2026-10-29T03:29:40Z · each bot started with $100.00

> **Season 2.** All bots were reset with fresh paper money; gates and stats count this season only. Earlier seasons:
> - Season 1: 2026-10-11 to 2026-10-28, $10 per bot; ended with `fresh_launch`, `momentum`, `random_control`, `volume_spike` out of money. Archived in `data/crypto/archive/season-1/`.

| Bot | Equity | Return | Trades | Win % | Avg win / loss | Per-trade avg (95% CI) | Profit factor | Max DD | Open |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|
| `random_control` | $100.81 | +0.8% | 4 | 75 | 28.0% / -71.3% | 3.2% (-45.1 to 39.4) | 1.18 | 20.0% | 1 |
| `claude_analyst` _(off: no API key)_ | $100.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `dip_reclaim` | $99.60 | -0.4% | 0 | – | – | – | – | 3.7% | 2 |
| `hold_sol` | $96.92 | -3.1% | 0 | – | – | – | – | 3.6% | 1 |
| `volume_spike` | $86.45 | -13.6% | 2 | 0 | 0.0% / -25.5% | -25.5% (-28.5 to -22.5) | 0.00 | 16.4% | 1 |
| `momentum` | $81.74 | -18.3% | 5 | 20 | 71.6% / -36.9% | -15.2% (-42.3 to 29.4) | 0.49 | 25.5% | 2 |
| `fresh_launch` | $41.50 | -58.5% | 19 | 37 | 49.3% / -60.6% | -20.1% (-46.2 to 8.9) | 0.47 | 58.5% | 1 |

### Real-money gates (all must be ✅)

| Bot | 100+ trades | 30+ days | Profitable | Profitable at 2x costs | Edge CI above 0 | Beats coin flip | Beats holding SOL | Drawdown < 40% | Verdict |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| `claude_analyst` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `dip_reclaim` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `volume_spike` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | collecting data |
| `momentum` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | collecting data |
| `fresh_launch` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |

_Coin-flip test = permutation test of per-trade returns vs. `random_control` (same tokens, exits and size, random entries). ✅ needs p < 0.010: 0.05 split across the 5 bots being tested, so one lucky bot out of several doesn't count as proof._

<details><summary>How positions closed</summary>

| Bot | take_profit | stop_loss | trailing_stop | time_exit | liquidity_pulled | vanished |
|---|---:|---:|---:|---:|---:|---:|
| `fresh_launch` | 4 | 11 | 2 | 1 | 1 | 0 |
| `momentum` | 1 | 4 | 0 | 0 | 0 | 0 |
| `random_control` | 2 | 1 | 1 | 0 | 0 | 0 |
| `volume_spike` | 0 | 2 | 0 | 0 | 0 | 0 |

</details>

## Stocks & ETFs — live paper trading (daily)

_No runs yet. Needs Alpaca paper keys; see README._

