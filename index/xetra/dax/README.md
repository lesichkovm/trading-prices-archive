# DAX Performance Index

**^GDAXI** on XETRA (index)

| Field | Value |
|-------|-------|
| instrument_id | `xetra_dax` |
| ticker | `^GDAXI` |
| exchange | `XETRA` |
| asset_class | `index` |
| first_date | `2000-01-03` |
| last_date | `2026-09-04` |
| row_count | 6774 |
| file_size | 497,643 bytes |
| schema_version | 1 |
| generated_at | 2026-09-05 13:04:19 UTC |

## Data

Price history is in [`prices.csv`](prices.csv) — pure CSV, no comments.

Columns: `date,open,high,low,close,adj_close,volume`

- `date` — ISO 8601 (`YYYY-MM-DD`)
- `open`, `high`, `low`, `close` — raw prices
- `adj_close` — split/dividend-adjusted close
- `volume` — trading volume (0 = not applicable for FX/indices)
