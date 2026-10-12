# Quant Lab report

_Updated 2026-10-12 04:38 UTC · paper money only._

## Meme coins (Solana) — live paper trading

Running **0.4 days** · 121 market checks · last check 2026-10-12T04:38:52Z · each bot started with $10.00

| Bot | Equity | Return | Trades | Win % | Avg win / loss | Per-trade avg (95% CI) | Profit factor | Max DD | Open |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|
| `fresh_launch` | $12.20 | +22.0% | 14 | 50 | 70.1% / -48.3% | 10.9% (-24.8 to 45.8) | 1.45 | 26.8% | 1 |
| `momentum` | $10.76 | +7.6% | 3 | 33 | 37.2% / -15.6% | 2.0% (-23.2 to 37.2) | 1.19 | 7.4% | 1 |
| `claude_analyst` _(off: no API key)_ | $10.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `dip_reclaim` | $10.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `hold_sol` | $9.90 | -1.0% | 0 | – | – | – | – | 5.3% | 1 |
| `volume_spike` | $9.50 | -5.0% | 1 | 0 | 0.0% / -20.2% | -20.2% (– to –) | 0.00 | 5.0% | 0 |
| `random_control` | $8.59 | -14.1% | 4 | 25 | 4.7% / -19.4% | -13.4% (-24.8 to -1.0) | 0.08 | 21.5% | 3 |

### Real-money gates (all must be ✅)

| Bot | 100+ trades | 30+ days | Profitable | Profitable at 2x costs | Edge CI above 0 | Beats coin flip | Beats holding SOL | Drawdown < 40% | Verdict |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| `fresh_launch` | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | collecting data |
| `momentum` | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ | collecting data |
| `claude_analyst` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `dip_reclaim` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `volume_spike` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | collecting data |

_Coin-flip test = permutation test of per-trade returns vs. `random_control` (same tokens, exits and size, random entries). ✅ needs p < 0.010: 0.05 split across the 5 bots being tested, so one lucky bot out of several doesn't count as proof._

<details><summary>How positions closed</summary>

| Bot | take_profit | stop_loss | trailing_stop | time_exit | liquidity_pulled | vanished |
|---|---:|---:|---:|---:|---:|---:|
| `fresh_launch` | 5 | 3 | 3 | 1 | 2 | 0 |
| `momentum` | 1 | 1 | 1 | 0 | 0 | 0 |
| `random_control` | 0 | 1 | 0 | 3 | 0 | 0 |
| `volume_spike` | 0 | 1 | 0 | 0 | 0 | 0 |

</details>

## Stocks & ETFs — live paper trading (daily)

_No runs yet. Needs Alpaca paper keys; see README._

