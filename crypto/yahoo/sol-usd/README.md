# Solana / USD

**SOL-USD** on YAHOO (crypto)

| Field | Value |
|-------|-------|
| instrument_id | `yahoo_sol-usd` |
| ticker | `SOL-USD` |
| exchange | `YAHOO` |
| asset_class | `crypto` |
| first_date | `2020-04-10` |
| last_date | `2026-09-05` |
| row_count | 2340 |
| file_size | 149,266 bytes |
| schema_version | 1 |
| generated_at | 2026-09-05 13:40:46 UTC |

## Data

Price history is in [`prices.csv`](prices.csv) — pure CSV, no comments.

Columns: `date,open,high,low,close,adj_close,volume`

- `date` — ISO 8601 (`YYYY-MM-DD`)
- `open`, `high`, `low`, `close` — raw prices
- `adj_close` — split/dividend-adjusted close
- `volume` — trading volume (0 = not applicable for FX/indices)
