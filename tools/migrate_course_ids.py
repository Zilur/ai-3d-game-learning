#!/usr/bin/env python3
"""One-time, explicit source and path migration; never executes models or engines.
Run only against the reviewed pre-migration tree. Colliding filenames are staged
in memory before any rename. All editorial checks are run before publication.
"""
from __future__ import annotations
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
BASE = 'f3842c76edd19f5eeda754c0ecb108317110e8bb'
NEW_GROUPS = [
 ('A', ['R01','B01A','B02','B04','B03','B05','B01B','B06']),
 ('B', ['R02','B07','R03','B08','B09','B10','B11','B12','B13','R04','B14','B15','B16']),
 ('C', ['I13','I14','I01','I02','I03','I04','I05','I06','I07','I09','I10','I11']),
 ('D', ['R05','R06','R07','R08','X01','X02','I12']),
 ('E', ['I08','A01','A02','A03','A04','A05','A06']),
]
OLD_GROUPS = [
 ('A', ['R01','B01A','B02','B01B']),
 ('B', ['B04','B03','B05','B06','B10','B11','B12','B13','B14','B16','I13','I14']),
 ('C', ['R02','B07','R03','B08','B09','R04','R05','R06','R07','R08']),
 ('D', ['B15','I03','I10','I11']),
 ('E', ['I01','I02','I04','I05','I06','I07','I08','I09','I12','X01','X02','A01','A02','A03','A04','A05','A06']),
]
IDS = {old: f'{letter}{i:02}' for letter, ids in NEW_GROUPS for i, old in enumerate(ids, 1)}
OLD_DISPLAY = {old: f'{letter}-{i:02}' for letter, ids in OLD_GROUPS for i, old in enumerate(ids, 1)}
LABELS = {OLD_DISPLAY[old]: new for old, new in IDS.items()}
REPLACEMENTS = IDS | LABELS | {f'C{i:02}': f'KN{i:02}' for i in range(1, 33)} | {'Cxx':'KNxx','B01':'A02'}
PATTERN = re.compile(r'(?<![A-Za-z0-9_])(' + '|'.join(re.escape(x) for x in sorted(REPLACEMENTS, key=len, reverse=True)) + r')(?![A-Za-z0-9_])')
EXCLUDED = {'tools/migrate_course_ids.py','tools/course_order.py','tools/numbered_navigation.py','tools/check_course_numbering.py','docs/numbering-migration.md'}


def convert(text):
    result = PATTERN.sub(lambda m: REPLACEMENTS[m[0]], text)
    result = result.replace('f"C{i:02}"', 'f"KN{i:02}"').replace("f'C{i:02}'", "f'KN{i:02}'")
    result = result.replace(r'\bC\d', r'\bKN\d').replace(r'(C\d', r'(KN\d')
    result = result.replace('C编号', 'KN概念编号')
    return result


def tracked_files():
    names = subprocess.check_output(['git','ls-files','-z'], cwd=ROOT).decode().split('\0')
    return [p for p in names if p]


def protected(path):
    return path.startswith('openmaic/vendor/') or (path.startswith(('game/','blender/','web/')) and not path.endswith('.md'))


def digest_protected():
    return {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in tracked_files() if protected(p)}


def replace_ast_assignment(text, name, expression, function=None):
    tree = ast.parse(text)
    scope = tree.body if function is None else next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == function).body
    found = [n for n in scope if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in n.targets)]
    if len(found) != 1:
        raise ValueError(f'Expected one assignment {function or "module"}.{name}, found {len(found)}')
    node = found[0]
    lines = text.splitlines(keepends=True)
    lines[node.lineno-1:node.end_lineno] = [' ' * node.col_offset + name + ' = ' + expression + '\n']
    return ''.join(lines)


def replace_function(text, name, body):
    tree = ast.parse(text)
    found = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name]
    if len(found) != 1:
        raise ValueError('Unexpected function: ' + name)
    node = found[0]
    lines = text.splitlines(keepends=True)
    lines[node.lineno-1:node.end_lineno] = [body.strip() + '\n']
    return ''.join(lines)


def once(text, old, new):
    if text.count(old) != 1:
        raise ValueError('Unexpected source anchor: ' + repr(old))
    return text.replace(old, new, 1)


def main():
    from course_order import ORDER, GROUPS
    if len(IDS) != 47 or set(IDS.values()) != set(ORDER):
        raise ValueError('Migration does not cover exactly 47 courses')
    if "id='B01A'" not in (ROOT/'curriculum/authoring/beginner_a.py').read_text():
        raise ValueError('Refusing to rerun a one-time migration on already-renumbered sources')
    frozen = digest_protected()
    old_manifest = json.loads((ROOT/'curriculum/materials-manifest.json').read_text())
    if {r['id'] for r in old_manifest['units']} != set(IDS):
        raise ValueError('Unexpected source lesson inventory')
    snapshot = {}
    for path in tracked_files():
        if path in EXCLUDED or path.startswith('.github/') or protected(path):
            continue
        if Path(path).suffix not in {'.md','.py','.json'}:
            continue
        snapshot[path] = (ROOT/path).read_text(encoding='utf-8')
    targets = {}
    for old_path, content in snapshot.items():
        new_path = convert(old_path)
        if new_path in targets:
            raise ValueError('Two files map to one path: ' + new_path)
        targets[new_path] = convert(content)
    for old_path in snapshot:
        if convert(old_path) != old_path:
            (ROOT/old_path).unlink()
    for path, content in targets.items():
        dest = ROOT/path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding='utf-8')

    path = ROOT/'tools/build_course_materials.py'
    text = path.read_text()
    text = once(text, 'import sys\n', 'import sys\nfrom course_order import ORDER as CANONICAL_ORDER\nfrom numbered_navigation import finalize_navigation\n')
    text = replace_ast_assignment(text, 'ORDER', 'CANONICAL_ORDER')
    text = replace_ast_assignment(text, 'expected', 'set(CANONICAL_ORDER)', 'validate')
    text = once(text, '    enrich_sessions(output, by_id, ORDER, ROWS, DISPLAY)\n',
                     '    enrich_sessions(output, by_id, ORDER, ROWS, DISPLAY)\n    finalize_navigation(output, by_id, ORDER, ROWS)\n')
    text = text.replace("'version':'v7-audited-collaboration'", "'version':'sequential-ids-2026-09-15'")
    path.write_text(text)

    path = ROOT/'curriculum/authoring/demo_extension.py'
    text = replace_ast_assignment(path.read_text(), 'ORDER', repr(ORDER))
    path.write_text(text)

    path = ROOT/'tools/scenario_sections.py'
    text = path.read_text()
    text = replace_ast_assignment(text, 'SERIES', repr(GROUPS))
    text = replace_ast_assignment(text, 'DISPLAY', '{ident: ident for _, _, ids in SERIES for ident in ids}')
    text = replace_function(text, 'decorate_lesson', '''def decorate_lesson(row, text, teacher):
    ident = row['id']
    if text.count(f"# {ident}｜{row['title']}") != 1:
        raise ValueError(ident + ': heading must match the canonical ID')
    text = text.replace('版本：Course Manuscripts v4｜2026-09-15', '版本：Applied Curriculum v5｜2026-09-15', 1)
    anchor = '## 3. 界面与参数学习深度'
    if text.count(anchor) != 1:
        raise ValueError(ident + ': missing insertion anchor')
    text = text.replace(anchor, ai_card(row) + '\\n' + anchor, 1)
    start = text.index('## 8. 与AI协作的最小任务')
    end = text.index('## 9. 复现与延迟检查', start)
    text = text[:start] + completion_card(row) + '\\n' + text[end:]
    if teacher:
        text = text.replace('## 12. 生成后的验收清单', '## 12. 生成后的验收清单\\n\\n- [ ] 概念后有局部AI工作、亲调入口与对应证据。\\n- [ ] 模拟和真实工具执行分开。', 1)
    return text
''')
    path.write_text(text)

    path = ROOT/'tools/demo_coach.py'
    text = path.read_text()
    text = once(text, 'import runpy\n', 'import runpy\nfrom course_order import next_unit\n')
    text = replace_function(text, 'next_lesson', '''def next_lesson(ident):
    return next_unit(ident)
''')
    path.write_text(text)

    path = ROOT/'tools/validate_repo.py'
    text = path.read_text()
    text = once(text, '    if errors:\n',
        '    numbered = subprocess.run([sys.executable, str(ROOT / "tools/check_course_numbering.py")], cwd=ROOT, check=False)\n'
        '    check(numbered.returncode == 0, "Canonical numbering, headers and prerequisite order failed")\n'
        '    if errors:\n')
    path.write_text(text)

    history = ['# 编号迁移记录（只用于旧书签与旧进度）', '',
        '2026-09-15完成一次统一迁移：A最基础，ABCDE为先后分组，不再是软件主题缩写。当前只使用新课号，不需要两套对照学习。',
        '**旧URL可能与新课同名，不能继续凭旧文件名判断内容。** 例如旧A01曾是高级测量，当前A01是零基础风格对话。下表的历史链接固定到旧提交，只用于核对；请从新索引重新收藏。',
        '所有作者源、前置、题号、讲义、教师输入和对话卡同时迁移。技术概念原C01–C32改成KN01–KN32以免与C组课程混淆；知识内容与M/K分级不因此改变。', '',
        '|旧文件课号（固定历史）|旧展示号|当前唯一课号|当前OpenMAIC输入|', '|---|---|---|---|']
    for letter, olds in NEW_GROUPS:
        for old in olds:
            new = IDS[old]
            url = f'https://github.com/Zilur/ai-3d-game-learning/blob/{BASE}/openmaic/lessons/{old}.md'
            history.append(f'|[{old}]({url})|{OLD_DISPLAY[old]}|{new}|[打开](../openmaic/lessons/{new}.md)|')
    history += ['', '运行资源如game/lessons/b02是既有参考包内部目录名，不是当前课程课号；新索引与讲义写明具体资源路径，本次不更改运行实现。',
        '[当前课程索引](../curriculum/lesson-index.md)', '']
    (ROOT/'docs/numbering-migration.md').write_text('\n'.join(history), encoding='utf-8')

    for script, args in [
        ('build_course_materials.py', []), ('build_course_materials.py', ['--check']),
        ('check_lesson_delivery.py', []), ('check_quality_review.py', []),
        ('check_session_readiness.py', []), ('check_course_numbering.py', []),
        ('validate_repo.py', []),
    ]:
        subprocess.run([sys.executable, str(ROOT/'tools'/script), *args], cwd=ROOT, check=True)
    if digest_protected() != frozen:
        raise ValueError('Runtime or upstream reference files changed during a documentation migration')
    print('NUMBERING MIGRATION PASS: 47 sources, filenames, headings and references; runtime and vendor unchanged')


if __name__ == '__main__':
    main()
