# ^GDAXI

| Field | Value |
|-------|-------|
| instrument_id | `xetra_gdaxi` |
| ticker | `^GDAXI` |
| exchange | `XETRA` |
| asset_class | `index` |
| first_date | `2010-01-04` |
| last_date | `2026-09-04` |
| row_count | 4232 |
| file_size | 315,947 bytes |
| schema_version | 1 |
| generated_at | 2026-09-05 12:50:52 UTC |

## Data

Price history is in [`prices.csv`](prices.csv) — pure CSV, no comments.

Columns: `date,open,high,low,close,adj_close,volume`

- `date` — ISO 8601 (`YYYY-MM-DD`)
- `open`, `high`, `low`, `close` — raw prices
- `adj_close` — split/dividend-adjusted close
- `volume` — trading volume
