# Quant Lab report

_Updated 2026-10-29 05:34 UTC · paper money only._

## Meme coins (Solana) — live paper trading

Running **0.5 days** · 122 market checks · last check 2026-10-29T05:33:56Z · each bot started with $100.00

> **Season 2.** All bots were reset with fresh paper money; gates and stats count this season only. Earlier seasons:
> - Season 1: 2026-10-11 to 2026-10-28, $10 per bot; ended with `fresh_launch`, `momentum`, `random_control`, `volume_spike` out of money. Archived in `data/crypto/archive/season-1/`.

| Bot | Equity | Return | Trades | Win % | Avg win / loss | Per-trade avg (95% CI) | Profit factor | Max DD | Open |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|
| `random_control` | $109.14 | +9.1% | 6 | 67 | 29.4% / -40.4% | 6.1% (-28.8 to 32.7) | 1.45 | 20.0% | 1 |
| `claude_analyst` _(off: no API key)_ | $100.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `hold_sol` | $97.69 | -2.3% | 0 | – | – | – | – | 3.6% | 1 |
| `dip_reclaim` | $97.56 | -2.4% | 1 | 0 | 0.0% / -0.6% | -0.6% (– to –) | 0.00 | 3.7% | 1 |
| `volume_spike` | $77.27 | -22.7% | 4 | 0 | 0.0% / -22.3% | -22.3% (-29.6 to -12.7) | 0.00 | 22.7% | 0 |
| `momentum` | $60.55 | -39.5% | 8 | 12 | 71.6% / -32.8% | -19.7% (-37.3 to 8.0) | 0.31 | 39.5% | 0 |
| `fresh_launch` | $42.40 | -57.6% | 20 | 35 | 49.3% / -56.1% | -19.2% (-43.9 to 8.8) | 0.47 | 61.7% | 0 |

### Real-money gates (all must be ✅)

| Bot | 100+ trades | 30+ days | Profitable | Profitable at 2x costs | Edge CI above 0 | Beats coin flip | Beats holding SOL | Drawdown < 40% | Verdict |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| `claude_analyst` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `dip_reclaim` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | collecting data |
| `volume_spike` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | collecting data |
| `momentum` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | collecting data |
| `fresh_launch` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |

_Coin-flip test = permutation test of per-trade returns vs. `random_control` (same tokens, exits and size, random entries). ✅ needs p < 0.010: 0.05 split across the 5 bots being tested, so one lucky bot out of several doesn't count as proof._

<details><summary>How positions closed</summary>

| Bot | take_profit | stop_loss | trailing_stop | time_exit | liquidity_pulled | vanished |
|---|---:|---:|---:|---:|---:|---:|
| `dip_reclaim` | 0 | 0 | 1 | 0 | 0 | 0 |
| `fresh_launch` | 4 | 11 | 3 | 1 | 1 | 0 |
| `momentum` | 1 | 7 | 0 | 0 | 0 | 0 |
| `random_control` | 3 | 1 | 1 | 1 | 0 | 0 |
| `volume_spike` | 0 | 3 | 0 | 1 | 0 | 0 |

</details>

## Stocks & ETFs — live paper trading (daily)

_No runs yet. Needs Alpaca paper keys; see README._

