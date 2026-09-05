# Japanese Yen / US Dollar

**JPYUSD=X** on YAHOO (fx)

| Field | Value |
|-------|-------|
| instrument_id | `yahoo_jpyusd` |
| ticker | `JPYUSD=X` |
| exchange | `YAHOO` |
| asset_class | `fx` |
| first_date | `2000-01-03` |
| last_date | `2026-09-04` |
| row_count | 6926 |
| file_size | 339,417 bytes |
| schema_version | 1 |
| generated_at | 2026-09-05 13:04:11 UTC |

## Data

Price history is in [`prices.csv`](prices.csv) — pure CSV, no comments.

Columns: `date,open,high,low,close,adj_close,volume`

- `date` — ISO 8601 (`YYYY-MM-DD`)
- `open`, `high`, `low`, `close` — raw prices
- `adj_close` — split/dividend-adjusted close
- `volume` — trading volume (0 = not applicable for FX/indices)
