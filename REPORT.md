# Quant Lab report

_Updated 2026-10-31 16:57 UTC · paper money only._

## Meme coins (Solana) — live paper trading

Running **2.9 days** · 771 market checks · last check 2026-10-31T16:56:55Z · each bot started with $100.00

> **Season 2.** All bots were reset with fresh paper money; gates and stats count this season only. Earlier seasons:
> - Season 1: 2026-10-11 to 2026-10-28, $10 per bot; ended with `fresh_launch`, `momentum`, `random_control`, `volume_spike` out of money. Archived in `data/crypto/archive/season-1/`.

| Bot | Equity | Return | Trades | Win % | Avg win / loss | Per-trade avg (95% CI) | Profit factor | Max DD | Open |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|
| `dip_reclaim` | $104.75 | +4.7% | 6 | 67 | 11.6% / -4.7% | 6.2% (-1.4 to 12.8) | 4.97 | 5.4% | 2 |
| `claude_analyst` _(off: no API key)_ | $100.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `hold_sol` | $93.20 | -6.8% | 0 | – | – | – | – | 9.9% | 1 |
| `random_control` | $64.06 | -35.9% | 41 | 34 | 21.6% / -16.6% | -3.6% (-10.9 to 4.1) | 0.68 | 45.1% | 2 |
| `volume_spike` | $51.02 | -49.0% | 13 | 8 | 23.6% / -17.2% | -14.1% (-21.2 to -5.4) | 0.11 | 49.0% | 1 |
| `momentum` | $0.55 | -99.5% | 34 | 21 | 36.7% / -30.6% | -16.8% (-26.7 to -5.6) | 0.31 | 99.5% | 1 |
| `fresh_launch` | $0.01 | -100.0% | 33 | 33 | 53.3% / -61.1% | -23.0% (-44.1 to -0.8) | 0.44 | 100.0% | 0 |

### Real-money gates (all must be ✅)

| Bot | 100+ trades | 30+ days | Profitable | Profitable at 2x costs | Edge CI above 0 | Beats coin flip | Beats holding SOL | Drawdown < 40% | Verdict |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| `dip_reclaim` | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | collecting data |
| `claude_analyst` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `volume_spike` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `momentum` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `fresh_launch` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |

_Coin-flip test = permutation test of per-trade returns vs. `random_control` (same tokens, exits and size, random entries). ✅ needs p < 0.010: 0.05 split across the 5 bots being tested, so one lucky bot out of several doesn't count as proof._

<details><summary>How positions closed</summary>

| Bot | take_profit | stop_loss | trailing_stop | time_exit | liquidity_pulled | vanished |
|---|---:|---:|---:|---:|---:|---:|
| `dip_reclaim` | 3 | 0 | 2 | 1 | 0 | 0 |
| `fresh_launch` | 6 | 14 | 6 | 1 | 6 | 0 |
| `momentum` | 5 | 25 | 3 | 1 | 0 | 0 |
| `random_control` | 7 | 10 | 5 | 19 | 0 | 0 |
| `volume_spike` | 1 | 8 | 2 | 2 | 0 | 0 |

</details>

## Stocks & ETFs — live paper trading (daily)

_No runs yet. Needs Alpaca paper keys; see README._

