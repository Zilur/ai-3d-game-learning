"""Temporary byte-verified source transfer; removed before the final source commit."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import re

root = Path.cwd()
rows = json.loads((root/'tools/_question_review_delta.json').read_text(encoding='utf-8'))
assert len(rows) == 14
order = [f'{g}{i:02}' for g,n in [('A',8),('B',13),('C',12),('D',7),('E',7)] for i in range(1,n+1)]
no_core_extension = {'A02','A03','B01','B07','E06'}
special = {'A01':'T3','A06':'T3','B03':'T3','B08':'T3','B10':'T3','B13':'T3','C04':'T3','D07':'T3','E03':'T3'}
ext_core = {i+'-'+special.get(i,'D2') for i in order if i not in no_core_extension}
ext_extra = {'KN08-T','KN09-T','KN03-T','KN10-T','KN02-T','KN11-T','KN12-T','KN15-T','KN07-T','KN16-T','KN13-T','KN19-T','KN20-T','KN21-T','KN14-T','KN25-T','KN24-T','KN23-T','KN27-T','KN28-T','KN29-T','KN30-T'}
outputs = []
seen = set()
for row in rows:
    name = row['path']
    rel = PurePosixPath(name)
    assert not rel.is_absolute() and '..' not in rel.parts and '\\' not in name
    assert name.startswith(('course/','docs/','openmaic/skills/')) or name == 'tools/tests/test_question_design.py'
    assert name not in seen
    seen.add(name)
    path = root/name
    assert not path.is_symlink()
    raw = path.read_bytes() if path.exists() else None
    assert (hashlib.sha256(raw).hexdigest() if raw is not None else None) == row['before'], name+' baseline changed'
    lines = raw.decode('utf-8').splitlines(keepends=True) if raw is not None else []
    limit = len(lines)
    for start,end,replacement in reversed(row['changes']):
        assert 0 <= start <= end <= limit
        lines[start:end] = [replacement]
        limit = start
    text = ''.join(lines)
    if name == 'course/teacher-notes.md':
        ids = []
        def label(match):
            qid = match.group(2)
            ids.append(qid)
            level = '扩展候选；基础稳定后按需选，未完成不单独阻塞继续。' if qid in ext_core|ext_extra else '基础；已学后的单一关系或用途判断，必要时提供入口或小示范。'
            return match.group(1)+'**预设层次：** '+level+'\n'
        text = re.sub(r'(^### ((?:[A-E]\d{2}-[PDTK]\d+|KN\d+-[PT]|K\d+))\n)', label, text, flags=re.M)
        assert len(ids) == len(set(ids)) == 264
        assert ext_core|ext_extra <= set(ids)
    data = text.encode('utf-8')
    assert hashlib.sha256(data).hexdigest() == row['after'], name+' does not match locally tested bytes'
    outputs.append((path,data))
for path,data in outputs:
    path.write_bytes(data)
for name in ('tools/_question_review_delta.json','tools/_apply_question_review.py','.github/workflows/question-review-temp.yml'):
    (root/name).unlink()
print('Applied 14 source files; every before/after hash verified; temporary files removed.')
