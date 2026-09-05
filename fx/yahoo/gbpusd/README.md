# British Pound / US Dollar

**GBPUSD=X** on YAHOO (fx)

| Field | Value |
|-------|-------|
| instrument_id | `yahoo_gbpusd` |
| ticker | `GBPUSD=X` |
| exchange | `YAHOO` |
| asset_class | `fx` |
| first_date | `2003-12-01` |
| last_date | `2026-09-04` |
| row_count | 5918 |
| file_size | 290,025 bytes |
| schema_version | 1 |
| generated_at | 2026-09-05 13:04:10 UTC |

## Data

Price history is in [`prices.csv`](prices.csv) — pure CSV, no comments.

Columns: `date,open,high,low,close,adj_close,volume`

- `date` — ISO 8601 (`YYYY-MM-DD`)
- `open`, `high`, `low`, `close` — raw prices
- `adj_close` — split/dividend-adjusted close
- `volume` — trading volume (0 = not applicable for FX/indices)
