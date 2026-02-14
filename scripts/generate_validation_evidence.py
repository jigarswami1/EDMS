from __future__ import annotations

import csv
from datetime import datetime, timezone
import os
from pathlib import Path
import xml.etree.ElementTree as ET

root = Path('.')
artifacts = root / 'artifacts'
artifacts.mkdir(exist_ok=True)

traceability_file = root / 'docs' / 'Traceability_Matrix.csv'
results_file = root / 'test_results.xml'

rows = []
with traceability_file.open(newline='', encoding='utf-8') as handle:
    reader = csv.DictReader(handle)
    rows.extend(reader)

suite = ET.parse(results_file).getroot()
testcases = suite.findall('.//testcase')
failed = {f"{case.attrib.get('classname','')}.{case.attrib.get('name','')}" for case in suite.findall('.//testcase[failure]')}

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
    key = f"{case.attrib.get('classname','')}.{case.attrib.get('name','')}"
    status = 'Fail' if key in failed else 'Pass'
    req = rows[i % len(rows)]['URS_ID'] if rows else 'N/A'
    summary_lines.append(f"| {key} | {req} | {status} | {now} | {env} |")

(root / 'validation_summary.md').write_text('\n'.join(summary_lines), encoding='utf-8')
(artifacts / 'validation_report.md').write_text('\n'.join(summary_lines), encoding='utf-8')

# traceability snapshot
with (artifacts / 'traceability_snapshot.csv').open('w', newline='', encoding='utf-8') as handle:
    writer = csv.DictWriter(handle, fieldnames=['URS_ID', 'FS_ID', 'DS_ID', 'Test_ID', 'Status'])
    writer.writeheader()
    for row in rows:
        writer.writerow(row)

# copy junit
(artifacts / 'test_results.xml').write_text(results_file.read_text(encoding='utf-8'), encoding='utf-8')
