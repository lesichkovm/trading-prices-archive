# iShares 20+ Year Treasury Bond ETF

**TLT** on NYSE (etf)

| Field | Value |
|-------|-------|
| instrument_id | `nyse_tlt` |
| ticker | `TLT` |
| exchange | `NYSE` |
| asset_class | `etf` |
| first_date | `2002-07-30` |
| last_date | `2026-09-04` |
| row_count | 6065 |
| file_size | 378,740 bytes |
| schema_version | 1 |
| generated_at | 2026-09-05 13:41:08 UTC |

## Data

Price history is in [`prices.csv`](prices.csv) — pure CSV, no comments.

Columns: `date,open,high,low,close,adj_close,volume`

- `date` — ISO 8601 (`YYYY-MM-DD`)
- `open`, `high`, `low`, `close` — raw prices
- `adj_close` — split/dividend-adjusted close
- `volume` — trading volume (0 = not applicable for FX/indices)
