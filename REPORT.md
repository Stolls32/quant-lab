# Quant Lab report

_Updated 2026-10-12 13:44 UTC · paper money only._

## Meme coins (Solana) — live paper trading

Running **0.8 days** · 229 market checks · last check 2026-10-12T13:44:25Z · each bot started with $10.00

| Bot | Equity | Return | Trades | Win % | Avg win / loss | Per-trade avg (95% CI) | Profit factor | Max DD | Open |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|
| `claude_analyst` _(off: no API key)_ | $10.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `dip_reclaim` | $10.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `fresh_launch` | $9.88 | -1.2% | 24 | 42 | 59.7% / -44.9% | -1.3% (-25.3 to 23.8) | 0.95 | 26.8% | 1 |
| `hold_sol` | $9.75 | -2.5% | 0 | – | – | – | – | 5.3% | 1 |
| `volume_spike` | $9.50 | -5.0% | 1 | 0 | 0.0% / -20.2% | -20.2% (– to –) | 0.00 | 5.0% | 0 |
| `momentum` | $8.46 | -15.4% | 5 | 40 | 19.8% / -31.9% | -11.2% (-39.7 to 18.1) | 0.41 | 24.2% | 1 |
| `random_control` | $8.36 | -16.4% | 8 | 25 | 5.2% / -12.1% | -7.8% (-15.7 to -0.6) | 0.14 | 21.5% | 2 |

### Real-money gates (all must be ✅)

| Bot | 100+ trades | 30+ days | Profitable | Profitable at 2x costs | Edge CI above 0 | Beats coin flip | Beats holding SOL | Drawdown < 40% | Verdict |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| `claude_analyst` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `dip_reclaim` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `fresh_launch` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | collecting data |
| `volume_spike` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | collecting data |
| `momentum` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | collecting data |

_Coin-flip test = permutation test of per-trade returns vs. `random_control` (same tokens, exits and size, random entries). ✅ needs p < 0.010: 0.05 split across the 5 bots being tested, so one lucky bot out of several doesn't count as proof._

<details><summary>How positions closed</summary>

| Bot | take_profit | stop_loss | trailing_stop | time_exit | liquidity_pulled | vanished |
|---|---:|---:|---:|---:|---:|---:|
| `fresh_launch` | 6 | 7 | 6 | 2 | 3 | 0 |
| `momentum` | 1 | 2 | 2 | 0 | 0 | 0 |
| `random_control` | 0 | 1 | 2 | 5 | 0 | 0 |
| `volume_spike` | 0 | 1 | 0 | 0 | 0 | 0 |

</details>

## Stocks & ETFs — live paper trading (daily)

_No runs yet. Needs Alpaca paper keys; see README._

