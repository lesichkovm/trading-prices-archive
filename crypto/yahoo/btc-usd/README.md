# Bitcoin / USD

**BTC-USD** on YAHOO (crypto)

| Field | Value |
|-------|-------|
| instrument_id | `yahoo_btc-usd` |
| ticker | `BTC-USD` |
| exchange | `YAHOO` |
| asset_class | `crypto` |
| first_date | `2014-09-17` |
| last_date | `2026-09-05` |
| row_count | 4372 |
| file_size | 328,898 bytes |
| schema_version | 1 |
| generated_at | 2026-09-05 12:56:47 UTC |

## Data

Price history is in [`prices.csv`](prices.csv) — pure CSV, no comments.

Columns: `date,open,high,low,close,adj_close,volume`

- `date` — ISO 8601 (`YYYY-MM-DD`)
- `open`, `high`, `low`, `close` — raw prices
- `adj_close` — split/dividend-adjusted close
- `volume` — trading volume (0 = not applicable for FX/indices)
