# Quant Lab report

_Updated 2026-10-29 05:04 UTC · paper money only._

## Meme coins (Solana) — live paper trading

Running **0.4 days** · 116 market checks · last check 2026-10-29T05:03:56Z · each bot started with $100.00

> **Season 2.** All bots were reset with fresh paper money; gates and stats count this season only. Earlier seasons:
> - Season 1: 2026-10-11 to 2026-10-28, $10 per bot; ended with `fresh_launch`, `momentum`, `random_control`, `volume_spike` out of money. Archived in `data/crypto/archive/season-1/`.

| Bot | Equity | Return | Trades | Win % | Avg win / loss | Per-trade avg (95% CI) | Profit factor | Max DD | Open |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|
| `random_control` | $104.85 | +4.8% | 5 | 60 | 28.0% / -40.4% | 0.6% (-38.0 to 32.5) | 1.04 | 20.0% | 1 |
| `claude_analyst` _(off: no API key)_ | $100.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `dip_reclaim` | $97.53 | -2.5% | 1 | 0 | 0.0% / -0.6% | -0.6% (– to –) | 0.00 | 3.7% | 1 |
| `hold_sol` | $97.29 | -2.7% | 0 | – | – | – | – | 3.6% | 1 |
| `volume_spike` | $83.67 | -16.3% | 2 | 0 | 0.0% / -25.5% | -25.5% (-28.5 to -22.5) | 0.00 | 16.4% | 2 |
| `momentum` | $66.97 | -33.0% | 7 | 14 | 71.6% / -33.1% | -18.2% (-38.2 to 13.6) | 0.36 | 33.0% | 1 |
| `fresh_launch` | $47.21 | -52.8% | 19 | 37 | 49.3% / -60.6% | -20.1% (-46.2 to 8.9) | 0.47 | 61.7% | 1 |

### Real-money gates (all must be ✅)

| Bot | 100+ trades | 30+ days | Profitable | Profitable at 2x costs | Edge CI above 0 | Beats coin flip | Beats holding SOL | Drawdown < 40% | Verdict |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| `claude_analyst` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `dip_reclaim` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | collecting data |
| `volume_spike` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | collecting data |
| `momentum` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | collecting data |
| `fresh_launch` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |

_Coin-flip test = permutation test of per-trade returns vs. `random_control` (same tokens, exits and size, random entries). ✅ needs p < 0.010: 0.05 split across the 5 bots being tested, so one lucky bot out of several doesn't count as proof._

<details><summary>How positions closed</summary>

| Bot | take_profit | stop_loss | trailing_stop | time_exit | liquidity_pulled | vanished |
|---|---:|---:|---:|---:|---:|---:|
| `dip_reclaim` | 0 | 0 | 1 | 0 | 0 | 0 |
| `fresh_launch` | 4 | 11 | 2 | 1 | 1 | 0 |
| `momentum` | 1 | 6 | 0 | 0 | 0 | 0 |
| `random_control` | 2 | 1 | 1 | 1 | 0 | 0 |
| `volume_spike` | 0 | 2 | 0 | 0 | 0 | 0 |

</details>

## Stocks & ETFs — live paper trading (daily)

_No runs yet. Needs Alpaca paper keys; see README._

