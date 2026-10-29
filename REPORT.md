# Quant Lab report

_Updated 2026-10-29 09:44 UTC · paper money only._

## Meme coins (Solana) — live paper trading

Running **0.6 days** · 172 market checks · last check 2026-10-29T09:43:56Z · each bot started with $100.00

> **Season 2.** All bots were reset with fresh paper money; gates and stats count this season only. Earlier seasons:
> - Season 1: 2026-10-11 to 2026-10-28, $10 per bot; ended with `fresh_launch`, `momentum`, `random_control`, `volume_spike` out of money. Archived in `data/crypto/archive/season-1/`.

| Bot | Equity | Return | Trades | Win % | Avg win / loss | Per-trade avg (95% CI) | Profit factor | Max DD | Open |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|
| `random_control` | $100.90 | +0.9% | 7 | 57 | 29.4% / -35.3% | 1.6% (-28.3 to 28.4) | 1.11 | 20.0% | 3 |
| `claude_analyst` _(off: no API key)_ | $100.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `hold_sol` | $97.34 | -2.7% | 0 | – | – | – | – | 3.6% | 1 |
| `dip_reclaim` | $96.44 | -3.6% | 1 | 0 | 0.0% / -0.6% | -0.6% (– to –) | 0.00 | 4.1% | 1 |
| `volume_spike` | $77.71 | -22.3% | 4 | 0 | 0.0% / -22.3% | -22.3% (-29.6 to -12.7) | 0.00 | 22.7% | 0 |
| `momentum` | $59.30 | -40.7% | 8 | 12 | 71.6% / -32.8% | -19.7% (-37.3 to 8.0) | 0.31 | 44.5% | 2 |
| `fresh_launch` | $20.31 | -79.7% | 25 | 32 | 54.6% / -57.1% | -21.4% (-44.7 to 3.0) | 0.40 | 90.2% | 1 |

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
| `dip_reclaim` | 0 | 0 | 1 | 0 | 0 | 0 |
| `fresh_launch` | 5 | 12 | 4 | 1 | 3 | 0 |
| `momentum` | 1 | 7 | 0 | 0 | 0 | 0 |
| `random_control` | 3 | 2 | 1 | 1 | 0 | 0 |
| `volume_spike` | 0 | 3 | 0 | 1 | 0 | 0 |

</details>

## Stocks & ETFs — live paper trading (daily)

_No runs yet. Needs Alpaca paper keys; see README._

