#!/usr/bin/env python3
"""Check checklist identifiers, levels, names, and links against W3C metadata."""

import argparse
import collections
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE_SHA256 = '3a034865a879a7d874b60ff2aec7f430cf37bc1597a1e00985680fd80ef5cf75'
ROW = re.compile(
    r'^- \[ \] \*\*(\d+\.\d+\.\d+) (.+?) \((A|AA|AAA)\):\*\*.*'
    r'\[W3C\]\(https://www\.w3\.org/TR/WCAG22/#([a-z0-9-]+)\)$',
    re.MULTILINE,
)


def source_items(data):
    items = []
    for principle in data['principles']:
        for guideline in principle['guidelines']:
            for criterion in guideline.get('successcriteria', []):
                if '2.2' not in criterion['versions'] or criterion['level'] not in ('A', 'AA', 'AAA'):
                    continue
                items.append({
                    'number': criterion['num'],
                    'name': criterion['handle'],
                    'level': criterion['level'],
                    'anchor': criterion['id'],
                    'principle': principle['handle'],
                })
    return items


def verify(index, checklist):
    items = index['criteria']
    official = {row['number']: row for row in items}
    if len(items) != 86 or len(official) != 86:
        raise ValueError('Expected 86 distinct active criteria.')
    if collections.Counter(row['level'] for row in items) != {'A': 31, 'AA': 24, 'AAA': 31}:
        raise ValueError('Unexpected criterion levels or counts.')
    matches = ROW.findall(checklist)
    if len(matches) != 86:
        raise ValueError(f'Expected 86 linked checklist rows, found {len(matches)}.')
    seen = set()
    for number, name, level, anchor in matches:
        if number in seen or number not in official:
            raise ValueError(f'Duplicate or unknown checklist criterion: {number}.')
        seen.add(number)
        item = official[number]
        if (name, level, anchor) != (item['name'], item['level'], item['anchor']):
            raise ValueError(f'Name, level, or W3C anchor mismatch: {number}.')
    if seen != set(official):
        raise ValueError(f'Missing criteria: {sorted(set(official) - seen)}.')
    return collections.Counter(level for _, _, level, _ in matches)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--index', type=Path, default=HERE / 'wcag22-criteria-index.json')
    parser.add_argument('--checklist', type=Path, default=HERE / 'master-checklist.md')
    parser.add_argument('--w3c-json', type=Path, help='Optional matching W3C serialization for source verification')
    args = parser.parse_args()
    index = json.loads(args.index.read_text(encoding='utf-8'))
    if args.w3c_json:
        data = args.w3c_json.read_bytes()
        if hashlib.sha256(data).hexdigest() != SOURCE_SHA256:
            raise ValueError('W3C source snapshot hash mismatch.')
        if source_items(json.loads(data)) != index['criteria']:
            raise ValueError('Criterion index differs from W3C source metadata.')
        print('W3C snapshot hash and criterion metadata match.')
    counts = verify(index, args.checklist.read_text(encoding='utf-8'))
    print(f"Checklist coverage: {counts['A']} A, {counts['AA']} AA, {counts['AAA']} AAA.")
    print('Criterion presence and metadata checked; content accuracy and actual conformance require human review.')


if __name__ == '__main__':
    main()
