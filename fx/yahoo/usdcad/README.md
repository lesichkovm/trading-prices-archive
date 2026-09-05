# US Dollar / Canadian Dollar

**USDCAD=X** on YAHOO (fx)

| Field | Value |
|-------|-------|
| instrument_id | `yahoo_usdcad` |
| ticker | `USDCAD=X` |
| exchange | `YAHOO` |
| asset_class | `fx` |
| first_date | `2003-09-17` |
| last_date | `2026-09-05` |
| row_count | 5975 |
| file_size | 292,818 bytes |
| schema_version | 1 |
| generated_at | 2026-09-05 13:40:50 UTC |

## Data

Price history is in [`prices.csv`](prices.csv) — pure CSV, no comments.

Columns: `date,open,high,low,close,adj_close,volume`

- `date` — ISO 8601 (`YYYY-MM-DD`)
- `open`, `high`, `low`, `close` — raw prices
- `adj_close` — split/dividend-adjusted close
- `volume` — trading volume (0 = not applicable for FX/indices)
