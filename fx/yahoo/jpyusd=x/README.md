# JPYUSD=X

| Field | Value |
|-------|-------|
| instrument_id | `yahoo_jpyusd-x` |
| ticker | `JPYUSD=X` |
| exchange | `YAHOO` |
| asset_class | `fx` |
| first_date | `2010-01-01` |
| last_date | `2026-09-04` |
| row_count | 4341 |
| file_size | 212,752 bytes |
| schema_version | 1 |
| generated_at | 2026-09-05 12:49:09 UTC |

## Data

Price history is in [`prices.csv`](prices.csv) — pure CSV, no comments.

Columns: `date,open,high,low,close,adj_close,volume`

- `date` — ISO 8601 (`YYYY-MM-DD`)
- `open`, `high`, `low`, `close` — raw prices
- `adj_close` — split/dividend-adjusted close
- `volume` — trading volume
