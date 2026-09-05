from pathlib import Path

remaining = 0
total = 0
for p in sorted(Path('.').rglob('prices.csv')):
    total += 1
    with open(p, 'rb') as f:
        data = f.read()
    if b'\r\n' in data:
        print(f'STILL CRLF: {p}')
        remaining += 1
print(f'Files with remaining CRLF: {remaining}')
print(f'Total CSV files: {total}')
