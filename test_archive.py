"""
Tests for trading-prices-archive.

Validates that every CSV file:
  1. Exists at the path declared in manifest.json
  2. Has a README.md alongside it with the correct metadata
  3. Parses as standard CSV (no comment lines, no malformed rows)
  4. Has the correct header row: date,open,high,low,close,adj_close,volume
  5. Every data row has exactly 7 fields
  6. Dates are ISO 8601 (YYYY-MM-DD) and sorted ascending
  7. Numeric fields parse as float/int
  8. Row count matches manifest.json
  9. first_date / last_date match manifest.json
 10. sha256 matches manifest.json

Run:
    pytest test_archive.py -v
"""

import csv
import hashlib
import json
import re
from datetime import date
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent
MANIFEST_PATH = REPO_ROOT / 'manifest.json'

EXPECTED_HEADER = ['date', 'open', 'high', 'low', 'close', 'adj_close', 'volume']
DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')


# ─── Fixtures ─────────────────────────────────────────────────────────

@pytest.fixture(scope='module')
def manifest():
    """Load manifest.json."""
    with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


@pytest.fixture(scope='module')
def instruments(manifest):
    """Extract instruments list from manifest."""
    return manifest['instruments']


# ─── Manifest-level tests ─────────────────────────────────────────────

class TestManifest:
    def test_manifest_exists(self):
        assert MANIFEST_PATH.exists(), 'manifest.json not found at repo root'

    def test_manifest_has_required_fields(self, manifest):
        assert 'schema_version' in manifest, 'missing schema_version'
        assert 'generated_at' in manifest, 'missing generated_at'
        assert 'instruments' in manifest, 'missing instruments'
        assert isinstance(manifest['instruments'], list), 'instruments is not a list'
        assert len(manifest['instruments']) > 0, 'no instruments in manifest'

    def test_manifest_instrument_ids_unique(self, instruments):
        ids = [i['instrument_id'] for i in instruments]
        duplicates = [x for x in ids if ids.count(x) > 1]
        assert not duplicates, f'duplicate instrument_ids: {set(duplicates)}'

    def test_manifest_paths_unique(self, instruments):
        paths = [i['path'] for i in instruments]
        duplicates = [x for x in paths if paths.count(x) > 1]
        assert not duplicates, f'duplicate paths: {set(duplicates)}'


# ─── Per-instrument tests ─────────────────────────────────────────────

def parse_csv(filepath: Path) -> tuple[list[str], list[list[str]]]:
    """Parse a CSV file, returning (header, rows). Raises on malformed rows."""
    with open(filepath, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)
    return header, rows


def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


class TestInstrumentCSV:
    """One set of tests per instrument — parametrized over all manifest entries."""

    @pytest.fixture(scope='class')
    def instrument_data(self, instruments):
        """Pre-parse all CSVs once, cache for all tests."""
        data = {}
        for inst in instruments:
            csv_path = REPO_ROOT / inst['path']
            if csv_path.exists():
                header, rows = parse_csv(csv_path)
                data[inst['instrument_id']] = {
                    'inst': inst,
                    'csv_path': csv_path,
                    'header': header,
                    'rows': rows,
                    'sha256': compute_sha256(csv_path),
                }
        return data

    def test_csv_file_exists(self, instruments):
        """Every path in manifest.json must exist on disk."""
        for inst in instruments:
            csv_path = REPO_ROOT / inst['path']
            assert csv_path.exists(), f'CSV not found: {inst["path"]} (instrument_id={inst["instrument_id"]})'

    def test_readme_exists(self, instruments):
        """Every instrument folder must have a README.md alongside the CSV."""
        for inst in instruments:
            csv_path = REPO_ROOT / inst['path']
            readme_path = csv_path.parent / 'README.md'
            assert readme_path.exists(), f'README.md not found in {csv_path.parent}'

    def test_header_row(self, instrument_data):
        """Every CSV must have the exact expected header row."""
        for inst_id, data in instrument_data.items():
            assert data['header'] == EXPECTED_HEADER, (
                f'{inst_id}: header mismatch. '
                f'Expected {EXPECTED_HEADER}, got {data["header"]}'
            )

    def test_no_comment_lines(self, instrument_data):
        """CSV must be pure data — no # comment lines."""
        for inst_id, data in instrument_data.items():
            with open(data['csv_path'], 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    assert not line.startswith('#'), (
                        f'{inst_id}: line {line_num} starts with # — CSV should be pure data'
                    )

    def test_row_field_count(self, instrument_data):
        """Every data row must have exactly 7 fields."""
        for inst_id, data in instrument_data.items():
            for row_num, row in enumerate(data['rows'], 2):  # +2: header is line 1, data starts at 2
                assert len(row) == 7, (
                    f'{inst_id}: row {row_num} has {len(row)} fields, expected 7: {row}'
                )

    def test_dates_are_iso8601(self, instrument_data):
        """Every date field must be YYYY-MM-DD."""
        for inst_id, data in instrument_data.items():
            for row_num, row in enumerate(data['rows'], 2):
                assert DATE_RE.match(row[0]), (
                    f'{inst_id}: row {row_num} date "{row[0]}" is not ISO 8601'
                )

    def test_dates_sorted_ascending(self, instrument_data):
        """Dates must be sorted ascending (oldest first)."""
        for inst_id, data in instrument_data.items():
            dates = [row[0] for row in data['rows']]
            assert dates == sorted(dates), (
                f'{inst_id}: dates are not sorted ascending'
            )

    def test_no_duplicate_dates(self, instrument_data):
        """No duplicate dates within a file."""
        for inst_id, data in instrument_data.items():
            dates = [row[0] for row in data['rows']]
            duplicates = [d for d in dates if dates.count(d) > 1]
            assert not duplicates, (
                f'{inst_id}: duplicate dates: {set(duplicates)}'
            )

    def test_numeric_fields_parse(self, instrument_data):
        """Open, high, low, close, adj_close must be floats; volume must be int."""
        for inst_id, data in instrument_data.items():
            for row_num, row in enumerate(data['rows'], 2):
                for col_idx, col_name in enumerate(['open', 'high', 'low', 'close', 'adj_close'], 1):
                    try:
                        float(row[col_idx])
                    except ValueError:
                        pytest.fail(f'{inst_id}: row {row_num} {col_name}="{row[col_idx]}" is not a float')
                # volume must be a non-negative integer
                try:
                    vol = int(row[6])
                    assert vol >= 0, f'{inst_id}: row {row_num} volume={vol} is negative'
                except ValueError:
                    pytest.fail(f'{inst_id}: row {row_num} volume="{row[6]}" is not an integer')

    def test_row_count_matches_manifest(self, instrument_data):
        """Row count in CSV must match manifest.json."""
        for inst_id, data in instrument_data.items():
            actual = len(data['rows'])
            expected = data['inst']['row_count']
            assert actual == expected, (
                f'{inst_id}: row count mismatch. CSV has {actual}, manifest says {expected}'
            )

    def test_first_date_matches_manifest(self, instrument_data):
        """First date in CSV must match manifest.json."""
        for inst_id, data in instrument_data.items():
            if not data['rows']:
                continue
            actual = data['rows'][0][0]
            expected = data['inst']['first_date']
            assert actual == expected, (
                f'{inst_id}: first_date mismatch. CSV has {actual}, manifest says {expected}'
            )

    def test_last_date_matches_manifest(self, instrument_data):
        """Last date in CSV must match manifest.json."""
        for inst_id, data in instrument_data.items():
            if not data['rows']:
                continue
            actual = data['rows'][-1][0]
            expected = data['inst']['last_date']
            assert actual == expected, (
                f'{inst_id}: last_date mismatch. CSV has {actual}, manifest says {expected}'
            )

    def test_sha256_matches_manifest(self, instrument_data):
        """sha256 of CSV file must match manifest.json."""
        for inst_id, data in instrument_data.items():
            actual = data['sha256']
            expected = data['inst']['sha256']
            assert actual == expected, (
                f'{inst_id}: sha256 mismatch. File has {actual}, manifest says {expected}'
            )

    def test_path_follows_convention(self, instruments):
        """Path must follow {asset_class}/{exchange}/{ticker}/prices.csv convention."""
        for inst in instruments:
            path = inst['path']
            parts = path.split('/')
            assert len(parts) == 4, (
                f'{inst["instrument_id"]}: path "{path}" should have 4 parts '
                f'(asset_class/exchange/ticker/prices.csv)'
            )
            assert parts[0] == inst['asset_class'], (
                f'{inst["instrument_id"]}: path asset_class "{parts[0]}" '
                f'does not match manifest "{inst["asset_class"]}"'
            )
            assert parts[1].lower() == inst['exchange'].lower(), (
                f'{inst["instrument_id"]}: path exchange "{parts[1]}" '
                f'does not match manifest "{inst["exchange"]}"'
            )
            assert parts[3] == 'prices.csv', (
                f'{inst["instrument_id"]}: path must end with prices.csv, got "{parts[3]}"'
            )

    def test_readme_metadata_matches_manifest(self, instruments):
        """README.md metadata table must match manifest.json values."""
        for inst in instruments:
            csv_path = REPO_ROOT / inst['path']
            readme_path = csv_path.parent / 'README.md'
            readme_text = readme_path.read_text(encoding='utf-8')

            # Check key fields appear in README
            assert f'`{inst["instrument_id"]}`' in readme_text, (
                f'{inst["instrument_id"]}: instrument_id not found in README.md'
            )
            assert f'`{inst["ticker"]}`' in readme_text, (
                f'{inst["instrument_id"]}: ticker not found in README.md'
            )
            assert f'`{inst["first_date"]}`' in readme_text, (
                f'{inst["instrument_id"]}: first_date not found in README.md'
            )
            assert f'`{inst["last_date"]}`' in readme_text, (
                f'{inst["instrument_id"]}: last_date not found in README.md'
            )
