# Quant Lab report

_Updated 2026-10-12 15:29 UTC · paper money only._

## Meme coins (Solana) — live paper trading

Running **0.9 days** · 250 market checks · last check 2026-10-12T15:29:25Z · each bot started with $10.00

| Bot | Equity | Return | Trades | Win % | Avg win / loss | Per-trade avg (95% CI) | Profit factor | Max DD | Open |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|
| `fresh_launch` | $13.98 | +39.8% | 26 | 46 | 74.5% / -44.9% | 10.2% (-16.6 to 39.5) | 1.42 | 26.8% | 0 |
| `claude_analyst` _(off: no API key)_ | $10.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `dip_reclaim` | $10.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `hold_sol` | $9.64 | -3.6% | 0 | – | – | – | – | 5.3% | 1 |
| `volume_spike` | $8.97 | -10.3% | 2 | 0 | 0.0% / -20.5% | -20.5% (-20.9 to -20.2) | 0.00 | 10.3% | 0 |
| `random_control` | $8.37 | -16.3% | 10 | 30 | 4.0% / -10.6% | -6.2% (-13.1 to -0.4) | 0.16 | 21.5% | 2 |
| `momentum` | $7.94 | -20.6% | 6 | 33 | 19.8% / -30.4% | -13.7% (-38.0 to 10.8) | 0.32 | 26.9% | 0 |

### Real-money gates (all must be ✅)

| Bot | 100+ trades | 30+ days | Profitable | Profitable at 2x costs | Edge CI above 0 | Beats coin flip | Beats holding SOL | Drawdown < 40% | Verdict |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| `fresh_launch` | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | collecting data |
| `claude_analyst` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `dip_reclaim` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `volume_spike` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | collecting data |
| `momentum` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | collecting data |

_Coin-flip test = permutation test of per-trade returns vs. `random_control` (same tokens, exits and size, random entries). ✅ needs p < 0.010: 0.05 split across the 5 bots being tested, so one lucky bot out of several doesn't count as proof._

<details><summary>How positions closed</summary>

| Bot | take_profit | stop_loss | trailing_stop | time_exit | liquidity_pulled | vanished |
|---|---:|---:|---:|---:|---:|---:|
| `fresh_launch` | 8 | 7 | 6 | 2 | 3 | 0 |
| `momentum` | 1 | 3 | 2 | 0 | 0 | 0 |
| `random_control` | 0 | 1 | 2 | 7 | 0 | 0 |
| `volume_spike` | 0 | 2 | 0 | 0 | 0 | 0 |

</details>

## Stocks & ETFs — live paper trading (daily)

_No runs yet. Needs Alpaca paper keys; see README._

