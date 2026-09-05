# trading-prices-archive

Historic OHLCV price data for trading instruments, stored as one CSV file per instrument.

## Structure

```
{asset_class}/{exchange}/{slug}/
    README.md     # metadata (instrument_id, ticker, date range, etc.)
    prices.csv    # pure CSV: date,open,high,low,close,adj_close,volume
```

## Instrument Map

| Slug | Ticker | Exchange | Asset Class | Name | Path |
|------|--------|----------|-------------|------|------|
| `aapl` | AAPL | NASDAQ | us | Apple Inc. | [`us/nasdaq/aapl/`](us/nasdaq/aapl/) |
| `msft` | MSFT | NASDAQ | us | Microsoft Corporation | [`us/nasdaq/msft/`](us/nasdaq/msft/) |
| `googl` | GOOGL | NASDAQ | us | Alphabet Inc. (Class A) | [`us/nasdaq/googl/`](us/nasdaq/googl/) |
| `amzn` | AMZN | NASDAQ | us | Amazon.com Inc. | [`us/nasdaq/amzn/`](us/nasdaq/amzn/) |
| `tsla` | TSLA | NASDAQ | us | Tesla Inc. | [`us/nasdaq/tsla/`](us/nasdaq/tsla/) |
| `nvda` | NVDA | NASDAQ | us | NVIDIA Corporation | [`us/nasdaq/nvda/`](us/nasdaq/nvda/) |
| `meta` | META | NASDAQ | us | Meta Platforms Inc. | [`us/nasdaq/meta/`](us/nasdaq/meta/) |
| `brk-b` | BRK-B | NYSE | us | Berkshire Hathaway Inc. (Class B) | [`us/nyse/brk-b/`](us/nyse/brk-b/) |
| `nem-de` | NEM.DE | XETRA | eu | Newmont Corporation (XETRA) | [`eu/xetra/nem-de/`](eu/xetra/nem-de/) |
| `btc-usd` | BTC-USD | YAHOO | crypto | Bitcoin / USD | [`crypto/yahoo/btc-usd/`](crypto/yahoo/btc-usd/) |
| `eth-usd` | ETH-USD | YAHOO | crypto | Ethereum / USD | [`crypto/yahoo/eth-usd/`](crypto/yahoo/eth-usd/) |
| `eurusd` | EURUSD=X | YAHOO | fx | Euro / US Dollar | [`fx/yahoo/eurusd/`](fx/yahoo/eurusd/) |
| `gbpusd` | GBPUSD=X | YAHOO | fx | British Pound / US Dollar | [`fx/yahoo/gbpusd/`](fx/yahoo/gbpusd/) |
| `jpyusd` | JPYUSD=X | YAHOO | fx | Japanese Yen / US Dollar | [`fx/yahoo/jpyusd/`](fx/yahoo/jpyusd/) |
| `gold` | GC=F | YAHOO | commodity | Gold Futures | [`commodity/yahoo/gold/`](commodity/yahoo/gold/) |
| `silver` | SI=F | YAHOO | commodity | Silver Futures | [`commodity/yahoo/silver/`](commodity/yahoo/silver/) |
| `wti-oil` | CL=F | YAHOO | commodity | Crude Oil Futures (WTI) | [`commodity/yahoo/wti-oil/`](commodity/yahoo/wti-oil/) |
| `spx` | ^GSPC | CBOE | index | S&P 500 Index | [`index/cboe/spx/`](index/cboe/spx/) |
| `dji` | ^DJI | NYSE | index | Dow Jones Industrial Average | [`index/nyse/dji/`](index/nyse/dji/) |
| `ixic` | ^IXIC | NASDAQ | index | Nasdaq Composite Index | [`index/nasdaq/ixic/`](index/nasdaq/ixic/) |
| `dax` | ^GDAXI | XETRA | index | DAX Performance Index | [`index/xetra/dax/`](index/xetra/dax/) |

## CSV Format

```
date,open,high,low,close,adj_close,volume
2000-01-03,0.9364,1.0045,0.9079,0.9994,0.8370,535796800
2000-01-04,0.9665,0.9877,0.9035,0.9152,0.7664,512377600
```

- `date` — ISO 8601 (`YYYY-MM-DD`)
- `open`, `high`, `low`, `close` — raw prices
- `adj_close` — split/dividend-adjusted close
- `volume` — trading volume (0 = not applicable for FX/indices)

## Manifest

[`manifest.json`](manifest.json) at the repo root indexes all instruments with paths, date ranges, row counts, and SHA-256 checksums.

## Tools

- `backfill.py` — download/update prices from yfinance
- `test_archive.py` — validates all CSVs, paths, and manifest integrity
- `rebuild_manifest.py` — rebuilds manifest.json from files on disk

## License

Public domain data (OHLCV prices). Scripts are MIT.
