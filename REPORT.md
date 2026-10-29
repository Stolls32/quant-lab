# Quant Lab report

_Updated 2026-10-29 01:04 UTC · paper money only._

## Meme coins (Solana) — live paper trading

Running **0.3 days** · 77 market checks · last check 2026-10-29T01:04:40Z · each bot started with $100.00

> **Season 2.** All bots were reset with fresh paper money; gates and stats count this season only. Earlier seasons:
> - Season 1: 2026-10-11 to 2026-10-28, $10 per bot; ended with `fresh_launch`, `momentum`, `random_control`, `volume_spike` out of money. Archived in `data/crypto/archive/season-1/`.

| Bot | Equity | Return | Trades | Win % | Avg win / loss | Per-trade avg (95% CI) | Profit factor | Max DD | Open |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|
| `claude_analyst` _(off: no API key)_ | $100.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `dip_reclaim` | $100.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `hold_sol` | $98.90 | -1.1% | 0 | – | – | – | – | 1.4% | 1 |
| `volume_spike` | $94.36 | -5.6% | 1 | 0 | 0.0% / -22.5% | -22.5% (– to –) | 0.00 | 5.6% | 0 |
| `random_control` | $91.70 | -8.3% | 2 | 50 | 45.3% / -71.3% | -13.0% (-71.3 to 45.3) | 0.64 | 20.0% | 1 |
| `momentum` | $81.04 | -19.0% | 5 | 20 | 71.6% / -36.9% | -15.2% (-42.3 to 29.4) | 0.49 | 25.5% | 0 |
| `fresh_launch` | $52.43 | -47.6% | 16 | 38 | 45.4% / -60.4% | -20.7% (-47.8 to 9.4) | 0.45 | 47.6% | 1 |

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
| `fresh_launch` | 3 | 9 | 2 | 1 | 1 | 0 |
| `momentum` | 1 | 4 | 0 | 0 | 0 | 0 |
| `random_control` | 1 | 1 | 0 | 0 | 0 | 0 |
| `volume_spike` | 0 | 1 | 0 | 0 | 0 | 0 |

</details>

## Stocks & ETFs — live paper trading (daily)

_No runs yet. Needs Alpaca paper keys; see README._

