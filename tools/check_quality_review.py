"""Consistency and deliberate-corruption checks for the editorial review.
Does NOT assert educational effectiveness, engine correctness or visual quality.
"""
from __future__ import annotations
import copy
import json
from pathlib import Path
import runpy
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import build_course_materials as builder
import quality_review as review


def main():
    lessons = []
    for name in builder.FILES:
        lessons.extend(runpy.run_path(str(builder.AUTHOR / name))['LESSONS'])
    sources = runpy.run_path(str(builder.AUTHOR / 'sources.py'))['SOURCES']
    lessons = builder.prepare_lessons(lessons, sources)
    lessons = review.apply_review(lessons, builder.ROWS, sources)
    by_id = builder.validate(lessons, sources)
    review.validate_review(by_id)
    trace = json.loads((ROOT / 'curriculum/quality-trace.json').read_text(encoding='utf-8'))
    assert trace['lesson_count'] == 47 and trace['diagnostic_count'] == 46
    assert {r['id'] for r in trace['units']} == set(by_id)
    trace_by_id = {r['id']:r for r in trace['units']}
    checks = 0
    for ident, row in by_id.items():
        rec = review.REVIEWS[ident]
        entry = trace_by_id[ident]
        assert entry['m'] == row['m'] and entry['k'] == row['k']
        assert entry['practical_evidence'] == rec['proof']
        assert entry['human'] == rec['decision'] and entry['ai'] == rec['ai']
        assert len(entry['questions']) == 4
        for folder in ('curriculum/lessons','openmaic/lessons','curriculum/dialogues'):
            text = (ROOT / folder / (ident + '.md')).read_text(encoding='utf-8')
            assert text.count('### 本课人和AI分别负责什么') == 1, (ident, folder)
            assert '本课由我负责：' + rec['decision'] in text, (ident, 'roles must be inside copied prompt')
            assert '可以交给你：' + rec['ai'] in text
            checks += 3
        student = (ROOT / 'curriculum/lessons' / (ident+'.md')).read_text(encoding='utf-8')
        teacher = (ROOT / 'openmaic/lessons' / (ident+'.md')).read_text(encoding='utf-8')
        dialogue = (ROOT / 'curriculum/dialogues' / (ident+'.md')).read_text(encoding='utf-8')
        assert '## 1A. 必学内容' in student and '## 1A. 必学内容' in teacher
        assert '## 11. 教师反馈' not in student and '## 11A.' not in student
        assert '## 11A.' not in dialogue
        if ident == 'A05':
            assert row['m'] == [] and rec['proof'] == []
            assert [q[0] for q in row['questions']] == ['K'] * 4
            assert '### A05-D2' not in teacher and '### 对话4' not in dialogue
        else:
            assert len(rec['proof']) == len(row['m']) == 2
            assert row['questions'][1][0] == 'D'
            assert rec['diagnostic'][0] in student and rec['diagnostic'][0] in teacher
            assert rec['diagnostic'][3] in teacher
            assert rec['diagnostic'][3] not in student and rec['diagnostic'][3] not in dialogue
            for proof in rec['proof']:
                assert proof in student and proof in teacher
        checks += 8
    # Guard the actual fixes that motivated this review.
    assert 'Origin' in by_id['B01B']['questions'][3][1]
    assert 'Quaternion' not in by_id['B01B']['questions'][3][1]
    assert '还没制作拾取计数' in by_id['B09']['questions'][2][1]
    assert '到B10/B12再补' in builder.ROWS['B09']['regress']
    for folder in ('curriculum/lessons', 'curriculum/dialogues', 'openmaic/lessons'):
        b09 = (ROOT / folder / 'B09.md').read_text(encoding='utf-8')
        assert '核对已有包装、形状和标记仍保留' in b09
        assert '验证包装的碰撞与拾取仍存在' not in b09
        assert '更新静态外观并保留当前包装职责' in b09
    assert '形状、比例、色彩、光照、表面五栏' in (ROOT / 'curriculum/dialogues/R01.md').read_text(encoding='utf-8')
    assert '窗口' in review.REVIEWS['B12']['proof'][1]
    assert review.REVIEWS['B12']['target'] == 1
    assert '同步重入' in by_id['B10']['failure']
    assert '当前范围内目标' in review.REVIEWS['X02']['diagnostic'][1]
    assert '错误或无证据' not in (ROOT / 'assessments/mastery.md').read_text(encoding='utf-8')
    checks += 9
    # Check that malformed mappings are rejected, rather than testing only happy-path markers.
    mutations = []
    bad = copy.deepcopy(review.REVIEWS); bad['B08']['proof'].pop(); mutations.append(bad)
    bad = copy.deepcopy(review.REVIEWS); bad['B08']['target'] = 3; mutations.append(bad)
    bad = copy.deepcopy(review.REVIEWS); bad.pop('I14'); mutations.append(bad)
    bad = copy.deepcopy(review.REVIEWS); bad['A05']['proof'] = ['illegal software gate']; mutations.append(bad)
    bad = copy.deepcopy(review.REVIEWS); bad['B03']['diagnostic'] = bad['B04']['diagnostic']; mutations.append(bad)
    bad = copy.deepcopy(review.REVIEWS); bad['B03']['ai'] = ''; mutations.append(bad)
    for bad in mutations:
        try:
            review.validate_review(by_id, bad)
        except ValueError:
            checks += 1
        else:
            raise AssertionError('Deliberate review corruption was not rejected')
    print(f'QUALITY REVIEW PASS: {checks} consistency checks; 47 roles; 92 M evidence mappings; 46 revised diagnostics; 6 corruption probes rejected')
    print('Author review and structure checks only. No OpenMAIC generation, new engine feature or learner mastery was tested.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
