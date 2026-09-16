#!/usr/bin/env python3
"""Check published learning/Lab links and diagnostic data. Not a classroom trial."""
from pathlib import Path
import json
import runpy
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'tools'))
from course_order import ORDER
from learning_review import validate, render, self_test


def main() -> None:
    bindings = json.loads((ROOT/'curriculum/lab-bindings.json').read_text())['bindings']
    assert set(bindings) == set(ORDER) and len(bindings) == 47
    objectives = json.loads((ROOT/'assessments/learning-objectives.json').read_text())['objectives']
    assert sum(o['level'] == 'M' for o in objectives.values()) == 92
    assert not any(k.startswith('E06.M') for k in objectives)
    assert all(o['lesson'] in ORDER and o['level'] in ('M','K') and o['text'] for o in objectives.values())
    count = 0
    for ident in ORDER:
        binding = bindings[ident]
        assert binding['first'] and binding['limits'] and binding['production']
        for p in binding['paths']:
            assert '..' not in Path(p).parts and p.startswith(('game/','blender/'))
            assert (ROOT/p).is_file(), p
        for folder in ('curriculum/lessons', 'curriculum/dialogues', 'openmaic/lessons'):
            text = (ROOT/folder/(ident+'.md')).read_text()
            assert text.count('## 0A. 这课怎样学、怎样查缺口') == 1, ident
            first_prompt = text.split('### 对话1｜建立本课上下文',1)[1].split('```text',1)[1].split('```',1)[0]
            assert binding['first'] in first_prompt and binding['limits'] in first_prompt
            assert all(p in first_prompt for p in binding['paths'])
            assert '一边改答案一边评分' in first_prompt
            if folder != 'openmaic/lessons':
                assert '## 11. 教师反馈' not in text
            if ident == 'E06':
                assert '不要求实操' in text and not binding['paths']
            count += 1
    memory = (ROOT/'print/memory-by-lesson.md').read_text()
    assert all(f'id="{i.lower()}"' in memory for i in ORDER)
    report = json.loads((ROOT/'assessments/learning-report.example.json').read_text())
    validate(report, objectives)
    assert '待验证' in render(report, objectives)
    self_test()
    pages = runpy.run_path(str(ROOT/'curriculum/authoring/novice_pages.py'))['PAGES']
    for name in pages:
        assert (ROOT/name).read_text() == pages[name], name
    print(f'LEARNING PATHWAY PASS: {count} lesson/input/dialogue files; 47 bindings; 92 M objectives')
    print('No AI grading, classroom trial, learner mastery or visual quality is verified by this check.')

if __name__ == '__main__':
    main()
