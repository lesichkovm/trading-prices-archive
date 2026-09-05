# Dogecoin / USD

**DOGE-USD** on YAHOO (crypto)

| Field | Value |
|-------|-------|
| instrument_id | `yahoo_doge-usd` |
| ticker | `DOGE-USD` |
| exchange | `YAHOO` |
| asset_class | `crypto` |
| first_date | `2017-11-09` |
| last_date | `2026-09-05` |
| row_count | 3223 |
| file_size | 183,743 bytes |
| schema_version | 1 |
| generated_at | 2026-09-05 13:40:48 UTC |

## Data

Price history is in [`prices.csv`](prices.csv) — pure CSV, no comments.

Columns: `date,open,high,low,close,adj_close,volume`

- `date` — ISO 8601 (`YYYY-MM-DD`)
- `open`, `high`, `low`, `close` — raw prices
- `adj_close` — split/dividend-adjusted close
- `volume` — trading volume (0 = not applicable for FX/indices)
