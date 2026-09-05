# CL=F

| Field | Value |
|-------|-------|
| instrument_id | `yahoo_cl-f` |
| ticker | `CL=F` |
| exchange | `YAHOO` |
| asset_class | `commodity` |
| first_date | `2010-01-04` |
| last_date | `2026-09-04` |
| row_count | 4194 |
| file_size | 249,463 bytes |
| schema_version | 1 |
| generated_at | 2026-09-05 12:49:27 UTC |

## Data

Price history is in [`prices.csv`](prices.csv) — pure CSV, no comments.

Columns: `date,open,high,low,close,adj_close,volume`

- `date` — ISO 8601 (`YYYY-MM-DD`)
- `open`, `high`, `low`, `close` — raw prices
- `adj_close` — split/dividend-adjusted close
- `volume` — trading volume
