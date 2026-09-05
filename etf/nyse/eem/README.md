# iShares MSCI Emerging Markets ETF

**EEM** on NYSE (etf)

| Field | Value |
|-------|-------|
| instrument_id | `nyse_eem` |
| ticker | `EEM` |
| exchange | `NYSE` |
| asset_class | `etf` |
| first_date | `2003-04-14` |
| last_date | `2026-09-04` |
| row_count | 5887 |
| file_size | 358,455 bytes |
| schema_version | 1 |
| generated_at | 2026-09-05 13:41:06 UTC |

## Data

Price history is in [`prices.csv`](prices.csv) — pure CSV, no comments.

Columns: `date,open,high,low,close,adj_close,volume`

- `date` — ISO 8601 (`YYYY-MM-DD`)
- `open`, `high`, `low`, `close` — raw prices
- `adj_close` — split/dividend-adjusted close
- `volume` — trading volume (0 = not applicable for FX/indices)
