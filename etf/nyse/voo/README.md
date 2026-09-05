# Vanguard S&P 500 ETF

**VOO** on NYSE (etf)

| Field | Value |
|-------|-------|
| instrument_id | `nyse_voo` |
| ticker | `VOO` |
| exchange | `NYSE` |
| asset_class | `etf` |
| first_date | `2010-09-09` |
| last_date | `2026-09-04` |
| row_count | 4022 |
| file_size | 260,134 bytes |
| schema_version | 1 |
| generated_at | 2026-09-05 13:41:05 UTC |

## Data

Price history is in [`prices.csv`](prices.csv) — pure CSV, no comments.

Columns: `date,open,high,low,close,adj_close,volume`

- `date` — ISO 8601 (`YYYY-MM-DD`)
- `open`, `high`, `low`, `close` — raw prices
- `adj_close` — split/dividend-adjusted close
- `volume` — trading volume (0 = not applicable for FX/indices)
