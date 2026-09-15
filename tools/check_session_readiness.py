#!/usr/bin/env python3
"""Check readiness, copied-frame coverage and meaningful negative probes.
Static checks only: do not run AI, OpenMAIC, Godot, Blender or a learner session.
"""
from __future__ import annotations
from copy import deepcopy
from pathlib import Path
import runpy
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import build_course_materials as builder
import session_coach as session


def main():
    lessons = []
    for name in builder.FILES:
        lessons.extend(runpy.run_path(str(builder.AUTHOR / name))['LESSONS'])
    sources = runpy.run_path(str(builder.AUTHOR / 'sources.py'))['SOURCES']
    lessons = builder.prepare_lessons(lessons, sources)
    lessons = builder.apply_review(lessons, builder.ROWS, sources)
    lessons = builder.apply_fixed_view_strategy(lessons, builder.ROWS, builder.PLANS, builder.DIAGRAMS, builder.REVIEWS, builder.STARTS, sources)
    by_id = builder.validate(lessons, sources)
    session.validate_session_data(by_id)
    output = {f'{folder}/{ident}.md': (ROOT / folder / f'{ident}.md').read_text(encoding='utf-8')
              for ident in by_id for folder in ('curriculum/lessons','openmaic/lessons','curriculum/dialogues')}
    session.validate_first_prompts(output, by_id)
    for ident, row in by_id.items():
        for folder in ('curriculum/lessons','openmaic/lessons','curriculum/dialogues'):
            text = output[f'{folder}/{ident}.md']
            assert text.count('## 0. 开始前：只准备本课需要的东西') == 1
            if folder != 'openmaic/lessons':
                assert '## 11. 教师反馈' not in text, ident
            if not row['m']:
                assert '本次结束：' in text and '不要求实操' in text
    probes = []
    missing = deepcopy(session.STARTS); missing.pop('A02')
    probes.append(lambda: session.validate_session_data(by_id, starts=missing))
    wrong = deepcopy(session.STARTS); wrong['A03'] = ('unknown','some material')
    probes.append(lambda: session.validate_session_data(by_id, starts=wrong))
    k_bad = deepcopy(session.STARTS); k_bad['E06'] = ('engine','server')
    probes.append(lambda: session.validate_session_data(by_id, starts=k_bad))
    fake = deepcopy(session.REFERENCES); fake['A02'] = ('game/not-delivered.tscn','not real')
    probes.append(lambda: session.validate_session_data(by_id, references=fake))
    unsafe = deepcopy(session.REFERENCES); unsafe['A02'] = ('game/../AGENTS.md','not a scene')
    probes.append(lambda: session.validate_session_data(by_id, references=unsafe))
    no_gate = dict(output)
    key = 'curriculum/dialogues/B09.md'
    no_gate[key] = no_gate[key].replace('继续条件：', 'deleted-marker：', 1)
    probes.append(lambda: session.validate_first_prompts(no_gate, by_id))
    rejected = 0
    for probe in probes:
        try:
            probe()
        except ValueError:
            rejected += 1
        else:
            raise AssertionError('A deliberate readiness defect was accepted')
    for path in ('curriculum/first-session.md','curriculum/preview-and-save.md','assessments/transfer-stations.md','assessments/transfer-teacher.md','openmaic/pilot-protocol.md'):
        assert (ROOT / path).is_file(), path
    print(f'SESSION READINESS PASS: {len(by_id)} lessons, {len(output)} existing-format outputs; {rejected} negative probes rejected')
    print('No classroom, new game content or human learning outcome tested.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
