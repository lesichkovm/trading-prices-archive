# London Stock Exchange Group plc

**LSEG.L** on LSE (eu)

| Field | Value |
|-------|-------|
| instrument_id | `lse_lseg` |
| ticker | `LSEG.L` |
| exchange | `LSE` |
| asset_class | `eu` |
| first_date | `2001-07-20` |
| last_date | `2026-09-04` |
| row_count | 6385 |
| file_size | 425,689 bytes |
| schema_version | 1 |
| generated_at | 2026-09-05 14:05:35 UTC |

## Data

Price history is in [`prices.csv`](prices.csv) — pure CSV, no comments.

Columns: `date,open,high,low,close,adj_close,volume`

- `date` — ISO 8601 (`YYYY-MM-DD`)
- `open`, `high`, `low`, `close` — raw prices
- `adj_close` — split/dividend-adjusted close
- `volume` — trading volume (0 = not applicable for FX/indices)
