# TSLA

| Field | Value |
|-------|-------|
| instrument_id | `nasdaq_tsla` |
| ticker | `TSLA` |
| exchange | `NASDAQ` |
| asset_class | `us` |
| first_date | `2010-06-29` |
| last_date | `2026-09-04` |
| row_count | 4072 |
| file_size | 253,275 bytes |
| schema_version | 1 |
| generated_at | 2026-09-05 12:48:53 UTC |

## Data

Price history is in [`prices.csv`](prices.csv) — pure CSV, no comments.

Columns: `date,open,high,low,close,adj_close,volume`

- `date` — ISO 8601 (`YYYY-MM-DD`)
- `open`, `high`, `low`, `close` — raw prices
- `adj_close` — split/dividend-adjusted close
- `volume` — trading volume
