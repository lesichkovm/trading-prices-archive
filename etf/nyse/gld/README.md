# SPDR Gold Shares ETF

**GLD** on NYSE (etf)

| Field | Value |
|-------|-------|
| instrument_id | `nyse_gld` |
| ticker | `GLD` |
| exchange | `NYSE` |
| asset_class | `etf` |
| first_date | `2004-11-18` |
| last_date | `2026-09-04` |
| row_count | 5483 |
| file_size | 352,161 bytes |
| schema_version | 1 |
| generated_at | 2026-09-05 13:41:07 UTC |

## Data

Price history is in [`prices.csv`](prices.csv) — pure CSV, no comments.

Columns: `date,open,high,low,close,adj_close,volume`

- `date` — ISO 8601 (`YYYY-MM-DD`)
- `open`, `high`, `low`, `close` — raw prices
- `adj_close` — split/dividend-adjusted close
- `volume` — trading volume (0 = not applicable for FX/indices)
