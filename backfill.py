#!/usr/bin/env python3
"""
Backfill script: downloads historic OHLCV from yfinance and writes CSV files
in the trading-prices-archive format.

Usage:
    python backfill.py                          # update default tickers (incremental)
    python backfill.py AAPL MSFT GOOGL          # update specific tickers
    python backfill.py --start 2010-01-01 AAPL  # full re-download from specific date
    python backfill.py --full AAPL              # force full re-download (ignore existing)

Layout per instrument:
    {asset_class}/{exchange}/{ticker}/
        README.md     # metadata (instrument_id, ticker, exchange, date range, etc.)
        prices.csv    # pure CSV: date,open,high,low,close,adj_close,volume

Incremental updates:
    If prices.csv already exists, the script reads the last date and only
    downloads from (last_date - 1 day) onwards. The last existing row is
    re-downloaded in case it was revised (e.g. today's bar updated). New
    rows are appended; the last row is replaced if it changed.

This is a quick-start tool. The Go CLI (tpa) will replace it for production use.
"""

import argparse
import csv
import hashlib
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yfinance as yf


# ─── Ticker metadata ──────────────────────────────────────────────────
# Maps yfinance tickers to our {asset_class}/{exchange}/{ticker} paths.

TICKER_META = {
    # US stocks
    'AAPL':   {'asset_class': 'us', 'exchange': 'nasdaq', 'instrument_id': 'nasdaq_aapl',   'name': 'Apple Inc.',                        'slug': 'aapl'},
    'MSFT':   {'asset_class': 'us', 'exchange': 'nasdaq', 'instrument_id': 'nasdaq_msft',   'name': 'Microsoft Corporation',             'slug': 'msft'},
    'GOOGL':  {'asset_class': 'us', 'exchange': 'nasdaq', 'instrument_id': 'nasdaq_googl',  'name': 'Alphabet Inc. (Class A)',           'slug': 'googl'},
    'AMZN':   {'asset_class': 'us', 'exchange': 'nasdaq', 'instrument_id': 'nasdaq_amzn',   'name': 'Amazon.com Inc.',                   'slug': 'amzn'},
    'TSLA':   {'asset_class': 'us', 'exchange': 'nasdaq', 'instrument_id': 'nasdaq_tsla',   'name': 'Tesla Inc.',                        'slug': 'tsla'},
    'NVDA':   {'asset_class': 'us', 'exchange': 'nasdaq', 'instrument_id': 'nasdaq_nvda',   'name': 'NVIDIA Corporation',                'slug': 'nvda'},
    'META':   {'asset_class': 'us', 'exchange': 'nasdaq', 'instrument_id': 'nasdaq_meta',   'name': 'Meta Platforms Inc.',               'slug': 'meta'},
    'BRK-B':  {'asset_class': 'us', 'exchange': 'nyse',   'instrument_id': 'nyse_brk-b',    'name': 'Berkshire Hathaway Inc. (Class B)', 'slug': 'brk-b'},
    # EU stocks (yfinance uses .DE suffix for XETRA)
    'NEM.DE': {'asset_class': 'eu', 'exchange': 'xetra',  'instrument_id': 'xetra_nem',     'name': 'Newmont Corporation (XETRA)',       'slug': 'nem-de'},
    # Crypto
    'BTC-USD': {'asset_class': 'crypto', 'exchange': 'yahoo', 'instrument_id': 'yahoo_btc-usd',  'name': 'Bitcoin / USD',          'slug': 'btc-usd'},
    'ETH-USD': {'asset_class': 'crypto', 'exchange': 'yahoo', 'instrument_id': 'yahoo_eth-usd',  'name': 'Ethereum / USD',         'slug': 'eth-usd'},
    # FX
    'EURUSD=X': {'asset_class': 'fx', 'exchange': 'yahoo', 'instrument_id': 'yahoo_eurusd', 'name': 'Euro / US Dollar',           'slug': 'eurusd'},
    'GBPUSD=X': {'asset_class': 'fx', 'exchange': 'yahoo', 'instrument_id': 'yahoo_gbpusd', 'name': 'British Pound / US Dollar',  'slug': 'gbpusd'},
    'JPYUSD=X': {'asset_class': 'fx', 'exchange': 'yahoo', 'instrument_id': 'yahoo_jpyusd', 'name': 'Japanese Yen / US Dollar',   'slug': 'jpyusd'},
    # Commodities
    'GC=F':   {'asset_class': 'commodity', 'exchange': 'yahoo', 'instrument_id': 'yahoo_gc-f',  'name': 'Gold Futures',           'slug': 'gold'},
    'SI=F':   {'asset_class': 'commodity', 'exchange': 'yahoo', 'instrument_id': 'yahoo_si-f',  'name': 'Silver Futures',         'slug': 'silver'},
    'CL=F':   {'asset_class': 'commodity', 'exchange': 'yahoo', 'instrument_id': 'yahoo_cl-f',  'name': 'Crude Oil Futures (WTI)','slug': 'wti-oil'},
    # Indices
    '^GSPC':  {'asset_class': 'index', 'exchange': 'cboe',   'instrument_id': 'cboe_spx',     'name': 'S&P 500 Index',              'slug': 'spx'},
    '^DJI':   {'asset_class': 'index', 'exchange': 'nyse',   'instrument_id': 'nyse_dji',     'name': 'Dow Jones Industrial Average','slug': 'dji'},
    '^IXIC':  {'asset_class': 'index', 'exchange': 'nasdaq', 'instrument_id': 'nasdaq_ixic',  'name': 'Nasdaq Composite Index',     'slug': 'ixic'},
    '^GDAXI': {'asset_class': 'index', 'exchange': 'xetra',  'instrument_id': 'xetra_dax',    'name': 'DAX Performance Index',      'slug': 'dax'},
}

DEFAULT_TICKERS = ['AAPL', 'MSFT', 'NEM.DE']


def get_meta(ticker: str) -> dict:
    """Get metadata for a ticker, inferring if not in the predefined map."""
    if ticker in TICKER_META:
        return TICKER_META[ticker]

    t = ticker.upper()
    # Default slug: lowercase, strip ^, =X, =F, replace . and / with -
    slug = t.lower().lstrip('^').replace('=x', '').replace('=f', '-f').replace('.', '-').replace('/', '-')
    slug = slug.rstrip('-')

    if t.endswith('.DE'):
        return {'asset_class': 'eu', 'exchange': 'xetra',
                'instrument_id': f'xetra_{slug}', 'name': t, 'slug': slug}
    elif t.endswith('.L'):
        return {'asset_class': 'eu', 'exchange': 'lse',
                'instrument_id': f'lse_{slug}', 'name': t, 'slug': slug}
    elif '-USD' in t or '=X' in t:
        return {'asset_class': 'fx', 'exchange': 'yahoo',
                'instrument_id': f'yahoo_{slug}', 'name': t, 'slug': slug}
    elif t.endswith('=F'):
        return {'asset_class': 'commodity', 'exchange': 'yahoo',
                'instrument_id': f'yahoo_{slug}', 'name': t, 'slug': slug}
    else:
        return {'asset_class': 'us', 'exchange': 'nasdaq',
                'instrument_id': f'nasdaq_{slug}', 'name': t, 'slug': slug}


def normalize_ticker_for_path(ticker: str) -> str:
    """Normalize ticker for folder name: lowercase, slashes→hyphens, dots stripped."""
    return ticker.lower().replace('/', '-').replace('.', '-')


def read_existing_csv(csv_path: Path) -> tuple[str, list[list[str]]]:
    """Read existing prices.csv. Returns (last_date, all_rows) or ('', []) if not found."""
    if not csv_path.exists():
        return '', []
    with open(csv_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        rows = list(reader)
    last_date = rows[-1][0] if rows else ''
    return last_date, rows


def write_full_csv(csv_path: Path, df) -> int:
    """Write full CSV from a DataFrame. Returns file size."""
    import pandas as pd

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    with open(csv_path, 'w', newline='\n', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['date', 'open', 'high', 'low', 'close', 'adj_close', 'volume'])
        for i in range(len(df)):
            writer.writerow([
                df.index[i].strftime('%Y-%m-%d'),
                f'{df["Open"].iloc[i]:.4f}',
                f'{df["High"].iloc[i]:.4f}',
                f'{df["Low"].iloc[i]:.4f}',
                f'{df["Close"].iloc[i]:.4f}',
                f'{df["Adj Close"].iloc[i]:.4f}',
                str(int(df["Volume"].iloc[i])),
            ])
    return csv_path.stat().st_size


def append_new_rows(csv_path: Path, existing_rows: list[list[str]], df) -> tuple[int, int, int]:
    """
    Append new rows from df to existing CSV.
    Replaces the last existing row if the date matches (revision).
    Returns (file_size, rows_appended, rows_replaced).
    """
    import pandas as pd

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # Build dict of new rows: {date: [row]}
    new_rows = {}
    for i in range(len(df)):
        date_str = df.index[i].strftime('%Y-%m-%d')
        new_rows[date_str] = [
            date_str,
            f'{df["Open"].iloc[i]:.4f}',
            f'{df["High"].iloc[i]:.4f}',
            f'{df["Low"].iloc[i]:.4f}',
            f'{df["Close"].iloc[i]:.4f}',
            f'{df["Adj Close"].iloc[i]:.4f}',
            str(int(df["Volume"].iloc[i])),
        ]

    # Drop the last existing row if it's in the new data (revision)
    rows_replaced = 0
    if existing_rows and existing_rows[-1][0] in new_rows:
        existing_rows = existing_rows[:-1]
        rows_replaced = 1

    # Append only rows with dates > last existing date
    if existing_rows:
        last_existing_date = existing_rows[-1][0]
        to_append = [row for date_str, row in new_rows.items() if date_str > last_existing_date]
    else:
        to_append = list(new_rows.values())

    # Sort by date
    to_append.sort(key=lambda r: r[0])

    # Rewrite the full file (existing + new)
    with open(csv_path, 'w', newline='\n', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['date', 'open', 'high', 'low', 'close', 'adj_close', 'volume'])
        writer.writerows(existing_rows)
        writer.writerows(to_append)

    file_size = csv_path.stat().st_size
    return file_size, len(to_append), rows_replaced


def write_readme(readme_path: Path, meta: dict, first_date: str, last_date: str,
                 row_count: int, csv_size: int):
    """Write README.md with metadata."""
    name = meta.get('name', meta['ticker_upper'])
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


def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def count_csv_rows(csv_path: Path) -> tuple[int, str, str]:
    """Returns (row_count, first_date, last_date) from an existing CSV."""
    with open(csv_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        rows = list(reader)
    if not rows:
        return 0, '', ''
    return len(rows), rows[0][0], rows[-1][0]


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


def backfill_ticker(ticker: str, repo_root: Path, start_date: str = None,
                    force_full: bool = False) -> dict | None:
    """
    Download a ticker from yfinance and write to the repo.
    If prices.csv exists and force_full is False, do an incremental update.
    Returns manifest entry.
    """
    import pandas as pd

    meta = get_meta(ticker)
    meta['ticker_upper'] = ticker.upper()

    slug = meta['slug']
    instrument_dir = repo_root / meta['asset_class'] / meta['exchange'] / slug
    csv_path = instrument_dir / 'prices.csv'
    readme_path = instrument_dir / 'README.md'

    # ─── Check for existing data ───
    existing_last_date, existing_rows = read_existing_csv(csv_path)

    if existing_last_date and not force_full and not start_date:
        # Incremental: download from last_date - 1 day
        last_dt = datetime.strptime(existing_last_date, '%Y-%m-%d')
        fetch_start = (last_dt - timedelta(days=1)).strftime('%Y-%m-%d')
        print(f'  {ticker}: incremental from {fetch_start} (existing last_date={existing_last_date})...', end=' ', flush=True)
    elif start_date:
        # Explicit start date → full re-download
        fetch_start = start_date
        print(f'  {ticker}: full from {fetch_start}...', end=' ', flush=True)
    else:
        # No existing data → full history
        fetch_start = None
        print(f'  {ticker}: full history...', end=' ', flush=True)

    # ─── Download ───
    try:
        df = yf.download(ticker, start=fetch_start, progress=False, auto_adjust=False)
    except Exception as e:
        print(f'FAILED: {e}')
        return None

    if df is None or df.empty:
        print('NO NEW DATA')
        # Still return existing manifest entry if we have one
        if existing_last_date:
            row_count, first_date, last_date = count_csv_rows(csv_path)
            csv_size = csv_path.stat().st_size
            return build_entry(meta, slug, first_date, last_date, row_count, csv_size, csv_path)
        return None

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    print(f'{len(df)} rows downloaded')

    # ─── Write ───
    instrument_dir.mkdir(parents=True, exist_ok=True)

    if existing_last_date and not force_full and not start_date:
        # Incremental append
        csv_size, appended, replaced = append_new_rows(csv_path, existing_rows, df)
        if appended == 0 and replaced == 0:
            print(f'  {ticker}: up to date (no new rows)')
        else:
            parts = []
            if appended: parts.append(f'{appended} new')
            if replaced: parts.append(f'{replaced} revised')
            print(f'  {ticker}: {", ".join(parts)}')
    else:
        # Full write
        csv_size = write_full_csv(csv_path, df)
        print(f'  {ticker}: full write ({len(df)} rows)')

    # ─── Read back final state ───
    row_count, first_date, last_date = count_csv_rows(csv_path)

    # ─── Write README ───
    write_readme(readme_path, meta, first_date, last_date, row_count, csv_size)

    return build_entry(meta, slug, first_date, last_date, row_count, csv_size, csv_path)


def build_entry(meta: dict, slug: str, first_date: str, last_date: str,
                row_count: int, csv_size: int, csv_path: Path) -> dict:
    """Build a manifest entry dict."""
    return {
        'instrument_id': meta['instrument_id'],
        'ticker': meta['ticker_upper'],
        'exchange': meta['exchange'].upper(),
        'asset_class': meta['asset_class'],
        'path': f'{meta["asset_class"]}/{meta["exchange"]}/{slug}/prices.csv',
        'first_date': first_date,
        'last_date': last_date,
        'row_count': row_count,
        'file_size': csv_size,
        'sha256': compute_sha256(csv_path),
        'git_sha': '',
        'spaces_url': None,
    }


def main():
    parser = argparse.ArgumentParser(description='Backfill trading-prices-archive from yfinance')
    parser.add_argument('tickers', nargs='*', default=DEFAULT_TICKERS,
                        help='Tickers to backfill (default: AAPL MSFT NEM.DE)')
    parser.add_argument('--start', default=None, help='Start date YYYY-MM-DD (forces full re-download)')
    parser.add_argument('--full', action='store_true', help='Force full re-download (ignore existing data)')
    parser.add_argument('--repo', default='.', help='Repo root path (default: current dir)')
    args = parser.parse_args()

    import pandas as pd  # noqa: F401 — needed by yfinance

    repo_root = Path(args.repo).resolve()
    if not (repo_root / 'README.md').exists():
        print(f'WARNING: {repo_root} does not look like the repo root (no README.md)')

    print(f'Repo: {repo_root}')
    print(f'Tickers: {", ".join(args.tickers)}')
    print(f'Mode: {"full" if args.full or args.start else "incremental"}')
    print()

    entries = []
    for ticker in args.tickers:
        entry = backfill_ticker(ticker, repo_root, args.start, args.full)
        if entry:
            entries.append(entry)

    if entries:
        print()
        update_manifest(repo_root, entries)
        print()
        print(f'Done. {len(entries)} instruments processed. Run "git add -A && git commit" to publish.')
    else:
        print('No data downloaded. Check ticker symbols.')
        sys.exit(1)


if __name__ == '__main__':
    main()
