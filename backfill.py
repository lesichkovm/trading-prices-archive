#!/usr/bin/env python3
"""
Backfill script: downloads historic OHLCV from yfinance and writes CSV files
in the trading-prices-archive format.

Usage:
    python backfill.py                          # backfill default tickers
    python backfill.py AAPL MSFT GOOGL          # backfill specific tickers
    python backfill.py --start 2010-01-01 AAPL  # from specific date

Layout per instrument:
    {asset_class}/{exchange}/{ticker}/
        README.md     # metadata (instrument_id, ticker, exchange, date range, etc.)
        prices.csv    # pure CSV: date,open,high,low,close,adj_close,volume

This is a quick-start tool. The Go CLI (tpa) will replace it for production use.
"""

import argparse
import csv
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import yfinance as yf


# ─── Ticker metadata ──────────────────────────────────────────────────
# Maps yfinance tickers to our {asset_class}/{exchange}/{ticker} paths.

TICKER_META = {
    # US stocks
    'AAPL':   {'asset_class': 'us', 'exchange': 'nasdaq', 'instrument_id': 'nasdaq_aapl',   'name': 'Apple Inc.'},
    'MSFT':   {'asset_class': 'us', 'exchange': 'nasdaq', 'instrument_id': 'nasdaq_msft',   'name': 'Microsoft Corporation'},
    'GOOGL':  {'asset_class': 'us', 'exchange': 'nasdaq', 'instrument_id': 'nasdaq_googl',  'name': 'Alphabet Inc. (Class A)'},
    'AMZN':   {'asset_class': 'us', 'exchange': 'nasdaq', 'instrument_id': 'nasdaq_amzn',   'name': 'Amazon.com Inc.'},
    'TSLA':   {'asset_class': 'us', 'exchange': 'nasdaq', 'instrument_id': 'nasdaq_tsla',   'name': 'Tesla Inc.'},
    'NVDA':   {'asset_class': 'us', 'exchange': 'nasdaq', 'instrument_id': 'nasdaq_nvda',   'name': 'NVIDIA Corporation'},
    'META':   {'asset_class': 'us', 'exchange': 'nasdaq', 'instrument_id': 'nasdaq_meta',   'name': 'Meta Platforms Inc.'},
    'BRK-B':  {'asset_class': 'us', 'exchange': 'nyse',   'instrument_id': 'nyse_brk-b',    'name': 'Berkshire Hathaway Inc. (Class B)'},
    # EU stocks (yfinance uses .DE suffix for XETRA)
    'NEM.DE': {'asset_class': 'eu', 'exchange': 'xetra',  'instrument_id': 'xetra_nem',     'name': 'Newmont Corporation (XETRA)'},
    # Crypto
    'BTC-USD': {'asset_class': 'crypto', 'exchange': 'yahoo', 'instrument_id': 'yahoo_btc-usd',  'name': 'Bitcoin / USD'},
    'ETH-USD': {'asset_class': 'crypto', 'exchange': 'yahoo', 'instrument_id': 'yahoo_eth-usd',  'name': 'Ethereum / USD'},
    # FX
    'EURUSD=X': {'asset_class': 'fx', 'exchange': 'yahoo', 'instrument_id': 'yahoo_eurusd', 'name': 'Euro / US Dollar'},
    'GBPUSD=X': {'asset_class': 'fx', 'exchange': 'yahoo', 'instrument_id': 'yahoo_gbpusd', 'name': 'British Pound / US Dollar'},
    'JPYUSD=X': {'asset_class': 'fx', 'exchange': 'yahoo', 'instrument_id': 'yahoo_jpyusd', 'name': 'Japanese Yen / US Dollar'},
    # Commodities
    'GC=F':   {'asset_class': 'commodity', 'exchange': 'yahoo', 'instrument_id': 'yahoo_gc-f',  'name': 'Gold Futures'},
    'SI=F':   {'asset_class': 'commodity', 'exchange': 'yahoo', 'instrument_id': 'yahoo_si-f',  'name': 'Silver Futures'},
    'CL=F':   {'asset_class': 'commodity', 'exchange': 'yahoo', 'instrument_id': 'yahoo_cl-f',  'name': 'Crude Oil Futures (WTI)'},
    # Indices
    '^GSPC':  {'asset_class': 'index', 'exchange': 'cboe',   'instrument_id': 'cboe_gspc',   'name': 'S&P 500 Index'},
    '^DJI':   {'asset_class': 'index', 'exchange': 'nyse',   'instrument_id': 'nyse_dji',    'name': 'Dow Jones Industrial Average'},
    '^IXIC':  {'asset_class': 'index', 'exchange': 'nasdaq', 'instrument_id': 'nasdaq_ixic', 'name': 'Nasdaq Composite Index'},
    '^GDAXI': {'asset_class': 'index', 'exchange': 'xetra',  'instrument_id': 'xetra_gdaxi', 'name': 'DAX Performance Index'},
}

DEFAULT_TICKERS = ['AAPL', 'MSFT', 'NEM.DE']


def get_meta(ticker: str) -> dict:
    """Get metadata for a ticker, inferring if not in the predefined map."""
    if ticker in TICKER_META:
        return TICKER_META[ticker]

    t = ticker.upper()
    if t.endswith('.DE'):
        return {'asset_class': 'eu', 'exchange': 'xetra',
                'instrument_id': f'xetra_{t.lower().replace(".", "-")}'}
    elif t.endswith('.L'):
        return {'asset_class': 'eu', 'exchange': 'lse',
                'instrument_id': f'lse_{t.lower().replace(".", "-")}'}
    elif '-USD' in t or '=X' in t:
        return {'asset_class': 'fx', 'exchange': 'yahoo',
                'instrument_id': f'yahoo_{t.lower().replace("=", "-").replace("-", "-")}'}
    elif t.endswith('=F'):
        return {'asset_class': 'commodity', 'exchange': 'yahoo',
                'instrument_id': f'yahoo_{t.lower().replace("=f", "-f")}'}
    else:
        return {'asset_class': 'us', 'exchange': 'nasdaq',
                'instrument_id': f'nasdaq_{t.lower().replace(".", "-")}'}


def normalize_ticker_for_path(ticker: str) -> str:
    """Normalize ticker for folder name: lowercase, slashes→hyphens, dots stripped."""
    return ticker.lower().replace('/', '-').replace('.', '-')


def write_instrument(instrument_dir: Path, meta: dict, df) -> dict:
    """Write README.md + prices.csv for one instrument. Returns manifest entry."""
    import pandas as pd

    instrument_dir.mkdir(parents=True, exist_ok=True)

    # Format dates as YYYY-MM-DD
    dates = df.index.strftime('%Y-%m-%d').tolist()

    # Flatten multi-index columns if present
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    first_date = dates[0] if dates else ''
    last_date = dates[-1] if dates else ''
    row_count = len(dates)

    # ─── Write pure CSV (no comments, no metadata — just data) ───
    csv_path = instrument_dir / 'prices.csv'
    with open(csv_path, 'w', newline='\n', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['date', 'open', 'high', 'low', 'close', 'adj_close', 'volume'])
        for i, date in enumerate(dates):
            writer.writerow([
                date,
                f'{df["Open"].iloc[i]:.4f}',
                f'{df["High"].iloc[i]:.4f}',
                f'{df["Low"].iloc[i]:.4f}',
                f'{df["Close"].iloc[i]:.4f}',
                f'{df["Adj Close"].iloc[i]:.4f}',
                str(int(df["Volume"].iloc[i])),
            ])

    csv_size = csv_path.stat().st_size

    # ─── Write README.md (metadata, renders on GitHub) ───
    name = meta.get('name', meta['ticker_upper'])
    readme_path = instrument_dir / 'README.md'
    with open(readme_path, 'w', newline='\n', encoding='utf-8') as f:
        f.write(f'# {name}\n\n')
        f.write(f'**{meta["ticker_upper"]}** on {meta["exchange"].upper()} ({meta["asset_class"]})\n\n')
        f.write(f'| Field | Value |\n')
        f.write(f'|-------|-------|\n')
        f.write(f'| instrument_id | `{meta["instrument_id"]}` |\n')
        f.write(f'| ticker | `{meta["ticker_upper"]}` |\n')
        f.write(f'| exchange | `{meta["exchange"].upper()}` |\n')
        f.write(f'| asset_class | `{meta["asset_class"]}` |\n')
        f.write(f'| first_date | `{first_date}` |\n')
        f.write(f'| last_date | `{last_date}` |\n')
        f.write(f'| row_count | {row_count} |\n')
        f.write(f'| file_size | {csv_size:,} bytes |\n')
        f.write(f'| schema_version | 1 |\n')
        f.write(f'| generated_at | {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")} UTC |\n')
        f.write(f'\n')
        f.write(f'## Data\n\n')
        f.write(f'Price history is in [`prices.csv`](prices.csv) — pure CSV, no comments.\n\n')
        f.write(f'Columns: `date,open,high,low,close,adj_close,volume`\n\n')
        f.write(f'- `date` — ISO 8601 (`YYYY-MM-DD`)\n')
        f.write(f'- `open`, `high`, `low`, `close` — raw prices\n')
        f.write(f'- `adj_close` — split/dividend-adjusted close\n')
        f.write(f'- `volume` — trading volume (0 = not applicable for FX/indices)\n')

    # ─── Compute sha256 of the CSV ───
    with open(csv_path, 'rb') as f:
        sha256 = hashlib.sha256(f.read()).hexdigest()

    ticker_path = normalize_ticker_for_path(meta['ticker_upper'])
    return {
        'instrument_id': meta['instrument_id'],
        'ticker': meta['ticker_upper'],
        'exchange': meta['exchange'].upper(),
        'asset_class': meta['asset_class'],
        'path': f'{meta["asset_class"]}/{meta["exchange"]}/{ticker_path}/prices.csv',
        'first_date': first_date,
        'last_date': last_date,
        'row_count': row_count,
        'file_size': csv_size,
        'sha256': sha256,
        'git_sha': '',
        'spaces_url': None,
    }


def update_manifest(repo_root: Path, entries: list):
    """Update or create manifest.json with the given entries."""
    manifest_path = repo_root / 'manifest.json'

    existing = {}
    if manifest_path.exists():
        with open(manifest_path, 'r') as f:
            data = json.load(f)
            for entry in data.get('instruments', []):
                existing[entry['instrument_id']] = entry

    for entry in entries:
        existing[entry['instrument_id']] = entry

    manifest = {
        'schema_version': 1,
        'generated_at': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
        'commit_sha': '',
        'instruments': list(existing.values()),
    }

    with open(manifest_path, 'w', newline='\n', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)
        f.write('\n')

    print(f'  manifest.json updated ({len(existing)} instruments)')


def backfill_ticker(ticker: str, repo_root: Path, start_date: str = None) -> dict | None:
    """Download a ticker from yfinance and write to the repo. Returns manifest entry."""
    import pandas as pd

    meta = get_meta(ticker)
    meta['ticker_upper'] = ticker.upper()

    print(f'  Downloading {ticker} from yfinance...', end=' ', flush=True)

    try:
        df = yf.download(ticker, start=start_date, progress=False, auto_adjust=False)
    except Exception as e:
        print(f'FAILED: {e}')
        return None

    if df is None or df.empty:
        print('NO DATA')
        return None

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    print(f'{len(df)} rows ({df.index[0].strftime("%Y-%m-%d")} to {df.index[-1].strftime("%Y-%m-%d")})')

    ticker_path = normalize_ticker_for_path(ticker)
    instrument_dir = repo_root / meta['asset_class'] / meta['exchange'] / ticker_path

    entry = write_instrument(instrument_dir, meta, df)
    print(f'  Written: {instrument_dir.relative_to(repo_root)}/  ({entry["file_size"]:,} bytes)')

    return entry


def main():
    parser = argparse.ArgumentParser(description='Backfill trading-prices-archive from yfinance')
    parser.add_argument('tickers', nargs='*', default=DEFAULT_TICKERS,
                        help='Tickers to backfill (default: AAPL MSFT NEM.DE)')
    parser.add_argument('--start', default=None, help='Start date YYYY-MM-DD (default: full history)')
    parser.add_argument('--repo', default='.', help='Repo root path (default: current dir)')
    args = parser.parse_args()

    repo_root = Path(args.repo).resolve()
    if not (repo_root / 'README.md').exists():
        print(f'WARNING: {repo_root} does not look like the repo root (no README.md)')

    print(f'Repo: {repo_root}')
    print(f'Tickers: {", ".join(args.tickers)}')
    print(f'Start date: {args.start or "full history"}')
    print()

    entries = []
    for ticker in args.tickers:
        entry = backfill_ticker(ticker, repo_root, args.start)
        if entry:
            entries.append(entry)

    if entries:
        print()
        update_manifest(repo_root, entries)
        print()
        print(f'Done. {len(entries)} instruments written. Run "git add -A && git commit" to publish.')
    else:
        print('No data downloaded. Check ticker symbols.')
        sys.exit(1)


if __name__ == '__main__':
    main()
