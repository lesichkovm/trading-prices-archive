# trading-prices-archive

Historic OHLCV price data for trading instruments, stored as one CSV file per instrument.

## Structure

```
{asset_class}/{exchange}/{slug}/
    README.md     # metadata (instrument_id, ticker, date range, etc.)
    prices.csv    # pure CSV: date,open,high,low,close,adj_close,volume
```

## Instrument Map

65 instruments across 6 asset classes (us, eu, crypto, fx, commodity, index, etf).

| Slug | Ticker | Exchange | Asset Class | Name | Path |
|------|--------|----------|-------------|------|------|
| `aapl` | AAPL | NASDAQ | us | Apple Inc. | [`us/nasdaq/aapl/`](us/nasdaq/aapl/) |
| `adbe` | ADBE | NASDAQ | us | Adobe Inc. | [`us/nasdaq/adbe/`](us/nasdaq/adbe/) |
| `amd` | AMD | NASDAQ | us | Advanced Micro Devices | [`us/nasdaq/amd/`](us/nasdaq/amd/) |
| `amzn` | AMZN | NASDAQ | us | Amazon.com Inc. | [`us/nasdaq/amzn/`](us/nasdaq/amzn/) |
| `googl` | GOOGL | NASDAQ | us | Alphabet Inc. (Class A) | [`us/nasdaq/googl/`](us/nasdaq/googl/) |
| `intc` | INTC | NASDAQ | us | Intel Corporation | [`us/nasdaq/intc/`](us/nasdaq/intc/) |
| `meta` | META | NASDAQ | us | Meta Platforms Inc. | [`us/nasdaq/meta/`](us/nasdaq/meta/) |
| `msft` | MSFT | NASDAQ | us | Microsoft Corporation | [`us/nasdaq/msft/`](us/nasdaq/msft/) |
| `nflx` | NFLX | NASDAQ | us | Netflix Inc. | [`us/nasdaq/nflx/`](us/nasdaq/nflx/) |
| `nvda` | NVDA | NASDAQ | us | NVIDIA Corporation | [`us/nasdaq/nvda/`](us/nasdaq/nvda/) |
| `tsla` | TSLA | NASDAQ | us | Tesla Inc. | [`us/nasdaq/tsla/`](us/nasdaq/tsla/) |
| `baba` | BABA | NYSE | us | Alibaba Group Holding | [`us/nyse/baba/`](us/nyse/baba/) |
| `brk-b` | BRK-B | NYSE | us | Berkshire Hathaway Inc. (Class B) | [`us/nyse/brk-b/`](us/nyse/brk-b/) |
| `crm` | CRM | NYSE | us | Salesforce Inc. | [`us/nyse/crm/`](us/nyse/crm/) |
| `dis` | DIS | NYSE | us | The Walt Disney Company | [`us/nyse/dis/`](us/nyse/dis/) |
| `hd` | HD | NYSE | us | The Home Depot Inc. | [`us/nyse/hd/`](us/nyse/hd/) |
| `jnj` | JNJ | NYSE | us | Johnson & Johnson | [`us/nyse/jnj/`](us/nyse/jnj/) |
| `jpm` | JPM | NYSE | us | JPMorgan Chase & Co. | [`us/nyse/jpm/`](us/nyse/jpm/) |
| `ma` | MA | NYSE | us | Mastercard Inc. | [`us/nyse/ma/`](us/nyse/ma/) |
| `pg` | PG | NYSE | us | Procter & Gamble Co. | [`us/nyse/pg/`](us/nyse/pg/) |
| `unh` | UNH | NYSE | us | UnitedHealth Group | [`us/nyse/unh/`](us/nyse/unh/) |
| `v` | V | NYSE | us | Visa Inc. | [`us/nyse/v/`](us/nyse/v/) |
| `wmt` | WMT | NYSE | us | Walmart Inc. | [`us/nyse/wmt/`](us/nyse/wmt/) |
| `alv` | ALV.DE | XETRA | eu | Allianz SE | [`eu/xetra/alv/`](eu/xetra/alv/) |
| `bmw` | BMW.DE | XETRA | eu | BMW AG | [`eu/xetra/bmw/`](eu/xetra/bmw/) |
| `nem-de` | NEM.DE | XETRA | eu | Newmont Corporation (XETRA) | [`eu/xetra/nem-de/`](eu/xetra/nem-de/) |
| `sap` | SAP.DE | XETRA | eu | SAP SE | [`eu/xetra/sap/`](eu/xetra/sap/) |
| `sie` | SIE.DE | XETRA | eu | Siemens AG | [`eu/xetra/sie/`](eu/xetra/sie/) |
| `azn` | AZN.L | LSE | eu | AstraZeneca plc | [`eu/lse/azn/`](eu/lse/azn/) |
| `bp` | BP.L | LSE | eu | BP plc | [`eu/lse/bp/`](eu/lse/bp/) |
| `gsk` | GSK.L | LSE | eu | GSK plc | [`eu/lse/gsk/`](eu/lse/gsk/) |
| `shel` | SHEL.L | LSE | eu | Shell plc | [`eu/lse/shel/`](eu/lse/shel/) |
| `ada-usd` | ADA-USD | YAHOO | crypto | Cardano / USD | [`crypto/yahoo/ada-usd/`](crypto/yahoo/ada-usd/) |
| `btc-usd` | BTC-USD | YAHOO | crypto | Bitcoin / USD | [`crypto/yahoo/btc-usd/`](crypto/yahoo/btc-usd/) |
| `doge-usd` | DOGE-USD | YAHOO | crypto | Dogecoin / USD | [`crypto/yahoo/doge-usd/`](crypto/yahoo/doge-usd/) |
| `eth-usd` | ETH-USD | YAHOO | crypto | Ethereum / USD | [`crypto/yahoo/eth-usd/`](crypto/yahoo/eth-usd/) |
| `sol-usd` | SOL-USD | YAHOO | crypto | Solana / USD | [`crypto/yahoo/sol-usd/`](crypto/yahoo/sol-usd/) |
| `xrp-usd` | XRP-USD | YAHOO | crypto | XRP / USD | [`crypto/yahoo/xrp-usd/`](crypto/yahoo/xrp-usd/) |
| `audusd` | AUDUSD=X | YAHOO | fx | Australian Dollar / US Dollar | [`fx/yahoo/audusd/`](fx/yahoo/audusd/) |
| `eurusd` | EURUSD=X | YAHOO | fx | Euro / US Dollar | [`fx/yahoo/eurusd/`](fx/yahoo/eurusd/) |
| `gbpusd` | GBPUSD=X | YAHOO | fx | British Pound / US Dollar | [`fx/yahoo/gbpusd/`](fx/yahoo/gbpusd/) |
| `jpyusd` | JPYUSD=X | YAHOO | fx | Japanese Yen / US Dollar | [`fx/yahoo/jpyusd/`](fx/yahoo/jpyusd/) |
| `usdcad` | USDCAD=X | YAHOO | fx | US Dollar / Canadian Dollar | [`fx/yahoo/usdcad/`](fx/yahoo/usdcad/) |
| `usdchf` | USDCHF=X | YAHOO | fx | US Dollar / Swiss Franc | [`fx/yahoo/usdchf/`](fx/yahoo/usdchf/) |
| `copper` | HG=F | YAHOO | commodity | Copper Futures | [`commodity/yahoo/copper/`](commodity/yahoo/copper/) |
| `gold` | GC=F | YAHOO | commodity | Gold Futures | [`commodity/yahoo/gold/`](commodity/yahoo/gold/) |
| `natgas` | NG=F | YAHOO | commodity | Natural Gas Futures | [`commodity/yahoo/natgas/`](commodity/yahoo/natgas/) |
| `silver` | SI=F | YAHOO | commodity | Silver Futures | [`commodity/yahoo/silver/`](commodity/yahoo/silver/) |
| `wti-oil` | CL=F | YAHOO | commodity | Crude Oil Futures (WTI) | [`commodity/yahoo/wti-oil/`](commodity/yahoo/wti-oil/) |
| `ixic` | ^IXIC | NASDAQ | index | Nasdaq Composite Index | [`index/nasdaq/ixic/`](index/nasdaq/ixic/) |
| `dji` | ^DJI | NYSE | index | Dow Jones Industrial Average | [`index/nyse/dji/`](index/nyse/dji/) |
| `rut` | ^RUT | NYSE | index | Russell 2000 Index | [`index/nyse/rut/`](index/nyse/rut/) |
| `dax` | ^GDAXI | XETRA | index | DAX Performance Index | [`index/xetra/dax/`](index/xetra/dax/) |
| `ftse` | ^FTSE | LSE | index | FTSE 100 Index | [`index/lse/ftse/`](index/lse/ftse/) |
| `spx` | ^GSPC | CBOE | index | S&P 500 Index | [`index/cboe/spx/`](index/cboe/spx/) |
| `vix` | ^VIX | CBOE | index | CBOE Volatility Index | [`index/cboe/vix/`](index/cboe/vix/) |
| `nikkei` | ^N225 | TSE | index | Nikkei 225 Index | [`index/tse/nikkei/`](index/tse/nikkei/) |
| `hsi` | ^HSI | HKEX | index | Hang Seng Index | [`index/hkex/hsi/`](index/hkex/hsi/) |
| `qqq` | QQQ | NASDAQ | etf | Invesco QQQ Trust (Nasdaq 100) | [`etf/nasdaq/qqq/`](etf/nasdaq/qqq/) |
| `eem` | EEM | NYSE | etf | iShares MSCI Emerging Markets ETF | [`etf/nyse/eem/`](etf/nyse/eem/) |
| `gld` | GLD | NYSE | etf | SPDR Gold Shares ETF | [`etf/nyse/gld/`](etf/nyse/gld/) |
| `spy` | SPY | NYSE | etf | SPDR S&P 500 ETF | [`etf/nyse/spy/`](etf/nyse/spy/) |
| `tlt` | TLT | NYSE | etf | iShares 20+ Year Treasury Bond ETF | [`etf/nyse/tlt/`](etf/nyse/tlt/) |
| `voo` | VOO | NYSE | etf | Vanguard S&P 500 ETF | [`etf/nyse/voo/`](etf/nyse/voo/) |
| `vti` | VTI | NYSE | etf | Vanguard Total Stock Market ETF | [`etf/nyse/vti/`](etf/nyse/vti/) |

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
