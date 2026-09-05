# CBOE Volatility Index

**^VIX** on CBOE (index)

| Field | Value |
|-------|-------|
| instrument_id | `cboe_vix` |
| ticker | `^VIX` |
| exchange | `CBOE` |
| asset_class | `index` |
| first_date | `2000-01-03` |
| last_date | `2026-09-04` |
| row_count | 6710 |
| file_size | 362,063 bytes |
| schema_version | 1 |
| generated_at | 2026-09-05 13:40:59 UTC |

## Data

Price history is in [`prices.csv`](prices.csv) — pure CSV, no comments.

Columns: `date,open,high,low,close,adj_close,volume`

- `date` — ISO 8601 (`YYYY-MM-DD`)
- `open`, `high`, `low`, `close` — raw prices
- `adj_close` — split/dividend-adjusted close
- `volume` — trading volume (0 = not applicable for FX/indices)
