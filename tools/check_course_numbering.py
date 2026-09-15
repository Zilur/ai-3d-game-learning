#!/usr/bin/env python3
"""Check real file IDs, source IDs, question IDs and ordering; no learning claims."""
from __future__ import annotations
from pathlib import Path
import json
import re
import runpy
import sys
from course_order import GROUPS, ORDER, K_ONLY, next_unit
import build_course_materials as builder

ROOT = Path(__file__).resolve().parents[1]


def check_title(text, ident):
    found = re.search(r'^# ([A-E]\d{2})[｜\s]', text, re.M)
    if not found or found[1] != ident:
        raise ValueError('Heading mismatch: ' + ident)
    if '兼容课号' in text or re.search(r'(?<![A-Za-z0-9_])[A-E]-\d{2}(?![A-Za-z0-9_])', text):
        raise ValueError('Second display namespace reintroduced: ' + ident)


def validate_dependencies(rows):
    pos = {ident: i for i, ident in enumerate(ORDER)}
    if set(rows) != set(ORDER):
        raise ValueError('Canonical source IDs missing or duplicated')
    for ident, row in rows.items():
        for dep in row['prereq'] + row['recall']:
            if dep not in pos or pos[dep] >= pos[ident]:
                raise ValueError(f'Future or missing dependency: {ident} -> {dep}')


def main():
    assert ORDER == sorted(ORDER) and len(ORDER) == len(set(ORDER)) == 47
    for letter, _label, ids in GROUPS:
        assert list(ids) == [f'{letter}{i:02}' for i in range(1, len(ids) + 1)]
    lessons = []
    for name in builder.FILES:
        lessons.extend(runpy.run_path(str(builder.AUTHOR/name))['LESSONS'])
    sources = runpy.run_path(str(builder.AUTHOR/'sources.py'))['SOURCES']
    lessons = builder.prepare_lessons(lessons, sources)
    lessons = builder.apply_review(lessons, builder.ROWS, sources)
    lessons = builder.apply_fixed_view_strategy(lessons, builder.ROWS, builder.PLANS, builder.DIAGRAMS, builder.REVIEWS, builder.STARTS, sources)
    rows = builder.validate(lessons, sources)
    validate_dependencies(rows)
    assert list(builder.ORDER) == ORDER
    assert builder.DISPLAY == {ident: ident for ident in ORDER}
    manifest = json.loads((ROOT/'curriculum/materials-manifest.json').read_text())
    assert [u['id'] for u in manifest['units']] == ORDER
    assert all(u['id'] == u['display'] for u in manifest['units'])
    assert rows['A01']['prereq'] == [] and rows['A02']['prereq'] == []
    assert '空间' in rows['A02']['title'] and '高级测量' not in rows['A01']['title']
    assert rows[K_ONLY]['m'] == [] and all(q[0] == 'K' for q in rows[K_ONLY]['questions'])
    assert next_unit('C12') == 'D07' and next_unit('D07') is None
    for ident in [f'E{i:02}' for i in range(1, 8)]:
        assert next_unit(ident) is None, 'No automatic enrollment in unrelated optional topics'
    checks = 0
    sample = None
    for folder in ('curriculum/lessons', 'openmaic/lessons', 'curriculum/dialogues'):
        files = list((ROOT/folder).glob('*.md'))
        assert {p.stem for p in files} == set(ORDER) and len(files) == 47, folder
        for path in files:
            ident = path.stem
            text = path.read_text(encoding='utf-8')
            check_title(text, ident)
            assert not re.search(r'(?<![A-Za-z0-9_])[IRX]\d{2}(?![A-Za-z0-9_])', text), (ident, 'legacy ID')
            assert ident in text.split('### 对话1', 1)[1].split('```', 2)[1], (ident, 'first frame')
            if folder != 'curriculum/dialogues':
                qids = re.findall(r'^### ([A-E]\d{2})-[PDTK]\d+\s*$', text, re.M)
                assert qids == [ident] * 4, (ident, 'question IDs')
                assert '**前置：**' in text
            sample = text if ident == 'A01' else sample
            checks += 1
    rejected = 0
    for faulty in (sample.replace('# A01', '# B01', 1), sample + '\n兼容课号：R01\n'):
        try:
            check_title(faulty, 'A01')
        except ValueError:
            rejected += 1
    from copy import deepcopy
    faulty_rows = deepcopy(rows); faulty_rows['A01']['prereq'] = ['E07']
    try:
        validate_dependencies(faulty_rows)
    except ValueError:
        rejected += 1
    assert rejected == 3
    print(f'COURSE NUMBERING PASS: {checks} lesson files; 47 actual source IDs; 5 ordered groups; 3 negative probes rejected')
    print('File/order validation only: no classroom, runtime or learner mastery claim.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
