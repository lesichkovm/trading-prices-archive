# Copper Futures

**HG=F** on YAHOO (commodity)

| Field | Value |
|-------|-------|
| instrument_id | `yahoo_copper` |
| ticker | `HG=F` |
| exchange | `YAHOO` |
| asset_class | `commodity` |
| first_date | `2000-08-30` |
| last_date | `2026-09-04` |
| row_count | 6533 |
| file_size | 334,036 bytes |
| schema_version | 1 |
| generated_at | 2026-09-05 13:40:53 UTC |

## Data

Price history is in [`prices.csv`](prices.csv) — pure CSV, no comments.

Columns: `date,open,high,low,close,adj_close,volume`

- `date` — ISO 8601 (`YYYY-MM-DD`)
- `open`, `high`, `low`, `close` — raw prices
- `adj_close` — split/dividend-adjusted close
- `volume` — trading volume (0 = not applicable for FX/indices)
