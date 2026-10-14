# Quant Lab report

_Updated 2026-10-14 12:07 UTC · paper money only._

## Meme coins (Solana) — live paper trading

Running **2.7 days** · 759 market checks · last check 2026-10-14T12:07:02Z · each bot started with $10.00

| Bot | Equity | Return | Trades | Win % | Avg win / loss | Per-trade avg (95% CI) | Profit factor | Max DD | Open |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|
| `volume_spike` | $11.64 | +16.4% | 7 | 43 | 47.7% / -18.0% | 10.2% (-16.8 to 47.8) | 1.99 | 10.3% | 1 |
| `claude_analyst` _(off: no API key)_ | $10.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `hold_sol` | $9.50 | -5.0% | 0 | – | – | – | – | 9.3% | 1 |
| `dip_reclaim` | $8.76 | -12.4% | 5 | 20 | 12.7% / -15.5% | -9.9% (-20.9 to 2.7) | 0.20 | 16.8% | 0 |
| `random_control` | $6.90 | -31.0% | 35 | 26 | 21.5% / -11.6% | -3.1% (-9.1 to 4.0) | 0.64 | 37.5% | 3 |
| `momentum` | $4.15 | -58.5% | 19 | 26 | 28.0% / -26.7% | -12.3% (-25.0 to 1.6) | 0.37 | 64.5% | 0 |
| `fresh_launch` | $1.12 | -88.8% | 93 | 39 | 65.5% / -53.0% | -7.1% (-20.7 to 6.8) | 0.78 | 93.7% | 1 |

### Real-money gates (all must be ✅)

| Bot | 100+ trades | 30+ days | Profitable | Profitable at 2x costs | Edge CI above 0 | Beats coin flip | Beats holding SOL | Drawdown < 40% | Verdict |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| `volume_spike` | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | collecting data |
| `claude_analyst` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `dip_reclaim` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | collecting data |
| `momentum` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |
| `fresh_launch` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | collecting data |

_Coin-flip test = permutation test of per-trade returns vs. `random_control` (same tokens, exits and size, random entries). ✅ needs p < 0.010: 0.05 split across the 5 bots being tested, so one lucky bot out of several doesn't count as proof._

<details><summary>How positions closed</summary>

| Bot | take_profit | stop_loss | trailing_stop | time_exit | liquidity_pulled | vanished |
|---|---:|---:|---:|---:|---:|---:|
| `dip_reclaim` | 1 | 3 | 1 | 0 | 0 | 0 |
| `fresh_launch` | 23 | 32 | 15 | 9 | 14 | 0 |
| `momentum` | 3 | 9 | 7 | 0 | 0 | 0 |
| `random_control` | 3 | 7 | 9 | 16 | 0 | 0 |
| `volume_spike` | 2 | 3 | 2 | 0 | 0 | 0 |

</details>

## Stocks & ETFs — live paper trading (daily)

_No runs yet. Needs Alpaca paper keys; see README._

