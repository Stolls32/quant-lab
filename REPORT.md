# Quant Lab report

_Updated 2026-10-29 21:59 UTC · paper money only._

## Meme coins (Solana) — live paper trading

Running **1.1 days** · 304 market checks · last check 2026-10-29T21:59:49Z · each bot started with $100.00

> **Season 2.** All bots were reset with fresh paper money; gates and stats count this season only. Earlier seasons:
> - Season 1: 2026-10-11 to 2026-10-28, $10 per bot; ended with `fresh_launch`, `momentum`, `random_control`, `volume_spike` out of money. Archived in `data/crypto/archive/season-1/`.

| Bot | Equity | Return | Trades | Win % | Avg win / loss | Per-trade avg (95% CI) | Profit factor | Max DD | Open |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|
| `dip_reclaim` | $101.09 | +1.1% | 3 | 33 | 13.7% / -4.7% | 1.5% (-8.7 to 13.7) | 1.47 | 4.8% | 0 |
| `claude_analyst` _(off: no API key)_ | $100.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `hold_sol` | $94.52 | -5.5% | 0 | – | – | – | – | 5.8% | 1 |
| `random_control` | $86.17 | -13.8% | 16 | 38 | 28.0% / -21.8% | -3.1% (-17.8 to 11.6) | 0.77 | 34.9% | 1 |
| `volume_spike` | $72.36 | -27.6% | 6 | 0 | 0.0% / -18.4% | -18.4% (-26.5 to -9.9) | 0.00 | 31.2% | 0 |
| `momentum` | $52.58 | -47.4% | 17 | 24 | 43.9% / -30.1% | -12.7% (-27.6 to 4.5) | 0.48 | 65.8% | 0 |
| `fresh_launch` | $0.01 | -100.0% | 33 | 33 | 53.3% / -61.1% | -23.0% (-44.1 to -0.8) | 0.44 | 100.0% | 0 |

### Real-money gates (all must be ✅)

| Bot | 100+ trades | 30+ days | Profitable | Profitable at 2x costs | Edge CI above 0 | Beats coin flip | Beats holding SOL | Drawdown < 40% | Verdict |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| `dip_reclaim` | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ | collecting data |
| `claude_analyst` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `volume_spike` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | collecting data |
| `momentum` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `fresh_launch` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |

_Coin-flip test = permutation test of per-trade returns vs. `random_control` (same tokens, exits and size, random entries). ✅ needs p < 0.010: 0.05 split across the 5 bots being tested, so one lucky bot out of several doesn't count as proof._

<details><summary>How positions closed</summary>

| Bot | take_profit | stop_loss | trailing_stop | time_exit | liquidity_pulled | vanished |
|---|---:|---:|---:|---:|---:|---:|
| `dip_reclaim` | 1 | 0 | 1 | 1 | 0 | 0 |
| `fresh_launch` | 6 | 14 | 6 | 1 | 6 | 0 |
| `momentum` | 3 | 13 | 1 | 0 | 0 | 0 |
| `random_control` | 4 | 5 | 2 | 5 | 0 | 0 |
| `volume_spike` | 0 | 4 | 1 | 1 | 0 | 0 |

</details>

## Stocks & ETFs — live paper trading (daily)

_No runs yet. Needs Alpaca paper keys; see README._

