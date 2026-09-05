# Salesforce Inc.

**CRM** on NYSE (us)

| Field | Value |
|-------|-------|
| instrument_id | `nyse_crm` |
| ticker | `CRM` |
| exchange | `NYSE` |
| asset_class | `us` |
| first_date | `2004-06-23` |
| last_date | `2026-09-04` |
| row_count | 5587 |
| file_size | 343,398 bytes |
| schema_version | 1 |
| generated_at | 2026-09-05 13:19:36 UTC |

## Data

Price history is in [`prices.csv`](prices.csv) — pure CSV, no comments.

Columns: `date,open,high,low,close,adj_close,volume`

- `date` — ISO 8601 (`YYYY-MM-DD`)
- `open`, `high`, `low`, `close` — raw prices
- `adj_close` — split/dividend-adjusted close
- `volume` — trading volume (0 = not applicable for FX/indices)
