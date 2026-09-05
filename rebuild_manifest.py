"""Rebuild manifest.json from actual CSV files on disk."""
import csv
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

repo = Path('D:/PROJECTs/trading-prices-archive')
entries = []

for csv_path in sorted(repo.rglob('prices.csv')):
    rel = csv_path.relative_to(repo).as_posix()
    parts = rel.split('/')
    asset_class, exchange, ticker_dir = parts[0], parts[1], parts[2]

    with open(csv_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        rows = list(reader)

    if not rows:
        continue

    first_date = rows[0][0]
    last_date = rows[-1][0]
    row_count = len(rows)
    file_size = csv_path.stat().st_size

    h = hashlib.sha256()
    with open(csv_path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    sha256 = h.hexdigest()

    # Read instrument_id and ticker from README
    readme = (csv_path.parent / 'README.md').read_text(encoding='utf-8')
    m = re.search(r'instrument_id \| `([^`]+)`', readme)
    instrument_id = m.group(1) if m else f'{exchange}_{ticker_dir}'
    m2 = re.search(r'ticker \| `([^`]+)`', readme)
    ticker = m2.group(1) if m2 else ticker_dir.upper()

    entries.append({
        'instrument_id': instrument_id,
        'ticker': ticker,
        'exchange': exchange.upper(),
        'asset_class': asset_class,
        'path': rel,
        'first_date': first_date,
        'last_date': last_date,
        'row_count': row_count,
        'file_size': file_size,
        'sha256': sha256,
        'git_sha': '',
        'spaces_url': None,
    })

manifest = {
    'schema_version': 1,
    'generated_at': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
    'commit_sha': '',
    'instruments': entries,
}

with open(repo / 'manifest.json', 'w', newline='\n', encoding='utf-8') as f:
    json.dump(manifest, f, indent=2)
    f.write('\n')

print(f'Rebuilt manifest: {len(entries)} instruments')
for e in entries:
    print(f'  {e["instrument_id"]:25} {e["path"]}')
