# Russell 2000 Index

**^RUT** on NYSE (index)

| Field | Value |
|-------|-------|
| instrument_id | `nyse_rut` |
| ticker | `^RUT` |
| exchange | `NYSE` |
| asset_class | `index` |
| first_date | `2000-01-03` |
| last_date | `2026-09-04` |
| row_count | 6709 |
| file_size | 472,559 bytes |
| schema_version | 1 |
| generated_at | 2026-09-05 13:40:58 UTC |

## Data

Price history is in [`prices.csv`](prices.csv) — pure CSV, no comments.

Columns: `date,open,high,low,close,adj_close,volume`

- `date` — ISO 8601 (`YYYY-MM-DD`)
- `open`, `high`, `low`, `close` — raw prices
- `adj_close` — split/dividend-adjusted close
- `volume` — trading volume (0 = not applicable for FX/indices)
