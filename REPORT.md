# Quant Lab report

_Updated 2026-10-12 05:33 UTC · paper money only._

## Meme coins (Solana) — live paper trading

Running **0.5 days** · 132 market checks · last check 2026-10-12T05:33:52Z · each bot started with $10.00

| Bot | Equity | Return | Trades | Win % | Avg win / loss | Per-trade avg (95% CI) | Profit factor | Max DD | Open |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|
| `fresh_launch` | $11.34 | +13.4% | 16 | 50 | 61.8% / -48.3% | 6.7% (-25.1 to 39.7) | 1.28 | 26.8% | 1 |
| `momentum` | $10.21 | +2.1% | 4 | 50 | 19.8% / -15.6% | 2.1% (-16.8 to 25.9) | 1.27 | 7.4% | 0 |
| `claude_analyst` _(off: no API key)_ | $10.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `dip_reclaim` | $10.00 | +0.0% | 0 | – | – | – | – | 0.0% | 0 |
| `hold_sol` | $9.93 | -0.7% | 0 | – | – | – | – | 5.3% | 1 |
| `volume_spike` | $9.50 | -5.0% | 1 | 0 | 0.0% / -20.2% | -20.2% (– to –) | 0.00 | 5.0% | 0 |
| `random_control` | $9.05 | -9.5% | 5 | 20 | 4.7% / -15.4% | -11.3% (-21.9 to -1.6) | 0.08 | 21.5% | 2 |

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
| `fresh_launch` | 5 | 4 | 4 | 1 | 2 | 0 |
| `momentum` | 1 | 1 | 2 | 0 | 0 | 0 |
| `random_control` | 0 | 1 | 1 | 3 | 0 | 0 |
| `volume_spike` | 0 | 1 | 0 | 0 | 0 | 0 |

</details>

## Stocks & ETFs — live paper trading (daily)

_No runs yet. Needs Alpaca paper keys; see README._

