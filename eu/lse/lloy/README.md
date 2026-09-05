# Lloyds Banking Group plc

**LLOY.L** on LSE (eu)

| Field | Value |
|-------|-------|
| instrument_id | `lse_lloy` |
| ticker | `LLOY.L` |
| exchange | `LSE` |
| asset_class | `eu` |
| first_date | `2000-01-03` |
| last_date | `2026-09-04` |
| row_count | 6789 |
| file_size | 423,030 bytes |
| schema_version | 1 |
| generated_at | 2026-09-05 14:05:25 UTC |

## Data

Price history is in [`prices.csv`](prices.csv) — pure CSV, no comments.

Columns: `date,open,high,low,close,adj_close,volume`

- `date` — ISO 8601 (`YYYY-MM-DD`)
- `open`, `high`, `low`, `close` — raw prices
- `adj_close` — split/dividend-adjusted close
- `volume` — trading volume (0 = not applicable for FX/indices)
