# Quant Lab report

_Updated 2026-10-29 17:19 UTC · paper money only._

## Meme coins (Solana) — live paper trading

Running **0.9 days** · 257 market checks · last check 2026-10-29T17:19:30Z · each bot started with $100.00

> **Season 2.** All bots were reset with fresh paper money; gates and stats count this season only. Earlier seasons:
> - Season 1: 2026-10-11 to 2026-10-28, $10 per bot; ended with `fresh_launch`, `momentum`, `random_control`, `volume_spike` out of money. Archived in `data/crypto/archive/season-1/`.

| Bot | Equity | Return | Trades | Win % | Avg win / loss | Per-trade avg (95% CI) | Profit factor | Max DD | Open |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|
| `claude_analyst` _(off: no API key)_ | $100.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `hold_sol` | $98.91 | -1.1% | 0 | – | – | – | – | 3.6% | 1 |
| `dip_reclaim` | $97.67 | -2.3% | 2 | 0 | 0.0% / -4.7% | -4.7% (-8.7 to -0.6) | 0.00 | 4.3% | 0 |
| `random_control` | $81.65 | -18.4% | 12 | 33 | 29.4% / -23.2% | -5.7% (-23.5 to 11.9) | 0.63 | 32.1% | 3 |
| `volume_spike` | $72.36 | -27.6% | 6 | 0 | 0.0% / -18.4% | -18.4% (-26.5 to -9.9) | 0.00 | 31.2% | 0 |
| `momentum` | $44.54 | -55.5% | 11 | 9 | 71.6% / -31.7% | -22.3% (-35.2 to -1.6) | 0.23 | 62.6% | 2 |
| `fresh_launch` | $0.01 | -100.0% | 33 | 33 | 53.3% / -61.1% | -23.0% (-44.1 to -0.8) | 0.44 | 100.0% | 0 |

### Real-money gates (all must be ✅)

| Bot | 100+ trades | 30+ days | Profitable | Profitable at 2x costs | Edge CI above 0 | Beats coin flip | Beats holding SOL | Drawdown < 40% | Verdict |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| `claude_analyst` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `dip_reclaim` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | collecting data |
| `volume_spike` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | collecting data |
| `momentum` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `fresh_launch` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |

_Coin-flip test = permutation test of per-trade returns vs. `random_control` (same tokens, exits and size, random entries). ✅ needs p < 0.010: 0.05 split across the 5 bots being tested, so one lucky bot out of several doesn't count as proof._

<details><summary>How positions closed</summary>

| Bot | take_profit | stop_loss | trailing_stop | time_exit | liquidity_pulled | vanished |
|---|---:|---:|---:|---:|---:|---:|
| `dip_reclaim` | 0 | 0 | 1 | 1 | 0 | 0 |
| `fresh_launch` | 6 | 14 | 6 | 1 | 6 | 0 |
| `momentum` | 1 | 10 | 0 | 0 | 0 | 0 |
| `random_control` | 3 | 4 | 2 | 3 | 0 | 0 |
| `volume_spike` | 0 | 4 | 1 | 1 | 0 | 0 |

</details>

## Stocks & ETFs — live paper trading (daily)

_No runs yet. Needs Alpaca paper keys; see README._

