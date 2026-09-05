# Natural Gas Futures

**NG=F** on YAHOO (commodity)

| Field | Value |
|-------|-------|
| instrument_id | `yahoo_natgas` |
| ticker | `NG=F` |
| exchange | `YAHOO` |
| asset_class | `commodity` |
| first_date | `2000-08-30` |
| last_date | `2026-09-04` |
| row_count | 6534 |
| file_size | 350,492 bytes |
| schema_version | 1 |
| generated_at | 2026-09-05 13:40:52 UTC |

## Data

Price history is in [`prices.csv`](prices.csv) — pure CSV, no comments.

Columns: `date,open,high,low,close,adj_close,volume`

- `date` — ISO 8601 (`YYYY-MM-DD`)
- `open`, `high`, `low`, `close` — raw prices
- `adj_close` — split/dividend-adjusted close
- `volume` — trading volume (0 = not applicable for FX/indices)
