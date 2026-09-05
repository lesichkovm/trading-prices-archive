"""Convert all prices.csv files from CRLF to LF line endings."""
from pathlib import Path

repo = Path('.')
converted = 0
for p in sorted(repo.rglob('prices.csv')):
    with open(p, 'rb') as f:
        data = f.read()
    if b'\r\n' in data:
        lf_data = data.replace(b'\r\n', b'\n')
        with open(p, 'wb') as f:
            f.write(lf_data)
        converted += 1
        print(f'  Converted: {p}')

print(f'\nTotal converted: {converted} files')
