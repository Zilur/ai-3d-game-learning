"""Structural contract tests for guided lesson delivery; not visual or learner tests."""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

def main():
    manifest = json.loads((ROOT / 'curriculum/materials-manifest.json').read_text(encoding='utf-8'))
    units = manifest['units']
    assert len(units) == 47 and len({u['id'] for u in units}) == 47, '47 unique lesson units required'
    assert len({u['display'] for u in units}) == 47, 'Unique ABCDE labels required'
    for unit in units:
        ident = unit['id']
        texts = {}
        for folder in ('curriculum/lessons','openmaic/lessons','curriculum/dialogues'):
            path = ROOT / folder / (ident + '.md')
            text = path.read_text(encoding='utf-8')
            texts[folder] = text
            assert '### 对话1' in text and '### 对话2' in text, (ident, folder, 'missing start')
            assert text.count('```') % 2 == 0, (ident, folder, 'unbalanced fences')
            assert '```mermaid' in text, (ident, folder, 'missing concept structure')
            if ident != 'A05':
                for step in range(3, 7):
                    assert f'### 对话{step}' in text, (ident, folder, step)
                for word in ('预计看到','必须保持','暂停','恢复','证据'):
                    assert word in text, (ident, folder, word)
            else:
                assert '本课全K' in text, (ident, 'K-only label')
                assert '### 对话4' not in text, (ident, 'must not require six practical steps')
        assert '教师反馈与评分依据' not in texts['curriculum/lessons'], ident
        assert '教师反馈与评分依据' in texts['openmaic/lessons'], ident
        assert '## 8. 实际应用验收' in texts['openmaic/lessons'], ident
        assert texts['curriculum/lessons'].count('## 2A.') == 1, (ident, 'duplicate coaching')
    for ident in ('I13', 'I14'):
        text = (ROOT / 'openmaic/lessons' / (ident + '.md')).read_text(encoding='utf-8')
        assert 'M 必须掌握' in text and 'K 理解即可' in text and '停止线' in text
    combat = (ROOT / 'openmaic/lessons/X02.md').read_text(encoding='utf-8')
    for case in ('空挥','有效窗口','中断','重开','木桩','第二次','预览'):
        assert case in combat, ('combat acceptance case missing', case)
    index = (ROOT / 'curriculum/lesson-index.md').read_text(encoding='utf-8')
    assert len(re.findall(r'\]\(dialogues/[^)]+\.md\)', index)) == 47, '47 direct conversation links'
    print('GUIDED DELIVERY PASS: 47 units; 141 manuscript/input/dialogue files; 2 new world lessons; K-only boundary retained')
    print('This does not generate OpenMAIC classrooms or validate new game features, images or learning outcomes.')
    return 0

if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (AssertionError, KeyError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
