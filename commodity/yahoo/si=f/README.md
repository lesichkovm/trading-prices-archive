# Silver Futures

**SI=F** on YAHOO (commodity)

| Field | Value |
|-------|-------|
| instrument_id | `yahoo_si-f` |
| ticker | `SI=F` |
| exchange | `YAHOO` |
| asset_class | `commodity` |
| first_date | `2000-08-30` |
| last_date | `2026-09-04` |
| row_count | 6530 |
| file_size | 353,006 bytes |
| schema_version | 1 |
| generated_at | 2026-09-05 12:56:53 UTC |

## Data

Price history is in [`prices.csv`](prices.csv) — pure CSV, no comments.

Columns: `date,open,high,low,close,adj_close,volume`

- `date` — ISO 8601 (`YYYY-MM-DD`)
- `open`, `high`, `low`, `close` — raw prices
- `adj_close` — split/dividend-adjusted close
- `volume` — trading volume (0 = not applicable for FX/indices)
