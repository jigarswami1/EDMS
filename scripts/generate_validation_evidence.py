from __future__ import annotations

import csv
from datetime import datetime, timezone
import os
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path('.')
ARTIFACTS_DIR = ROOT / 'artifacts'
ARTIFACTS_DIR.mkdir(exist_ok=True)
TRACEABILITY_FILE = ROOT / 'docs' / 'Traceability_Matrix.csv'
RESULTS_FILE = ROOT / 'test_results.xml'


def _load_traceability() -> list[dict[str, str]]:
    with TRACEABILITY_FILE.open(newline='', encoding='utf-8') as handle:
        return list(csv.DictReader(handle))


def _load_testsuite() -> ET.Element:
    if not RESULTS_FILE.exists():
        raise FileNotFoundError(f"Missing junit xml file: {RESULTS_FILE}")
    return ET.parse(RESULTS_FILE).getroot()


def main() -> None:
    rows = _load_traceability()
    suite = _load_testsuite()

    testcases = suite.findall('.//testcase')
    failed = {
        f"{case.attrib.get('classname', '')}.{case.attrib.get('name', '')}"
        for case in suite.findall('.//testcase[failure]')
    }

    now = datetime.now(timezone.utc).isoformat()
    env = os.getenv('GITHUB_RUN_ID', 'local')

    summary_lines = [
        '# Validation Summary',
        '',
        f'- Timestamp (UTC): {now}',
        f'- Environment: {env}',
        '',
        '| Test name | Requirement ID | Pass/Fail | Timestamp | Environment |',
        '|---|---|---|---|---|',
    ]

    for i, case in enumerate(testcases):
        key = f"{case.attrib.get('classname', '')}.{case.attrib.get('name', '')}"
        status = 'Fail' if key in failed else 'Pass'
        req = rows[i % len(rows)]['URS_ID'] if rows else 'N/A'
        summary_lines.append(f"| {key} | {req} | {status} | {now} | {env} |")

    (ROOT / 'validation_summary.md').write_text('\n'.join(summary_lines), encoding='utf-8')
    (ARTIFACTS_DIR / 'validation_report.md').write_text('\n'.join(summary_lines), encoding='utf-8')

    with (ARTIFACTS_DIR / 'traceability_snapshot.csv').open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=['URS_ID', 'FS_ID', 'DS_ID', 'Test_ID', 'Status'])
        writer.writeheader()
        writer.writerows(rows)

    (ARTIFACTS_DIR / 'test_results.xml').write_text(RESULTS_FILE.read_text(encoding='utf-8'), encoding='utf-8')


if __name__ == '__main__':
    main()
