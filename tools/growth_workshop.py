#!/usr/bin/env python3
"""Create one local project-learning worksheet. No network, grading or game edits.
Usage: python3 tools/growth_workshop.py plan
       python3 tools/growth_workshop.py session prototype --cycle route-test
"""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
PLAN = 'learning-system/growth-plan.json'
STAGES = ('independent', 'prototype', 'slice', 'production', 'release', 'maintenance')
FIELDS = ('key', 'title', 'entry', 'question', 'mission', 'learning', 'experiment', 'explain', 'parent_question', 'stop')
DOCS = ('learning-system/commercial-growth.md', 'learning-system/growth-knowledge-map.md',
        'learning-system/templates/growth-cycle.md', 'learning-system/templates/release-readiness.md')
LESSONS = {f'{g}{i:02}' for g, n in [('A',8), ('B',13), ('C',12), ('D',7), ('E',7)] for i in range(1, n+1)}
MAX_BYTES = 250_000


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def load_plan(root: Path = ROOT) -> list[dict]:
    path = root / PLAN
    require(path.is_file() and path.stat().st_size <= MAX_BYTES, '成长配置不存在或过大')
    data = json.loads(path.read_text(encoding='utf-8'))
    require(isinstance(data, dict) and type(data.get('schema_version')) is int and data['schema_version'] == 1,
            '不支持的成长配置版本')
    rows = data.get('stages')
    require(isinstance(rows, list) and len(rows) == len(STAGES), '阶段配置不完整')
    for row in rows:
        require(isinstance(row, dict), '阶段必须为对象')
        for key in FIELDS:
            value = row.get(key)
            require(isinstance(value, str) and 0 < len(value.strip()) <= 3000, '缺少有效字段：' + key)
        for key in ('lessons', 'evidence'):
            value = row.get(key)
            require(isinstance(value, list) and 1 <= len(value) <= 12 and
                    all(isinstance(x, str) and 0 < len(x.strip()) <= 3000 for x in value), '无效列表：' + key)
            require(len(set(value)) == len(value), '列表不能重复：' + key)
        require(set(row['lessons']) <= LESSONS, '未知的基础课号')
    require(tuple(row['key'] for row in rows) == STAGES, '阶段顺序、标识或唯一性错误')
    return rows


def render(row: dict, cycle: str, root: Path = ROOT, openmaic: bool = False) -> str:
    require(re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,59}', cycle) is not None, 'cycle使用1–60位安全英文/数字标识')
    header = '# 教师生成输入：成长工作坊' if openmaic else '# 成长工作坊：给AI教练的单轮任务'
    lines = [header, '', f'阶段：{row["title"]}；本轮：{cycle}。阶段不是新课号，也不是已通过状态。', '',
             '固定/有限视角、风格化自然世界、素材拼装与适度二开的范围保持不变；商业化是未来可选目标，不给孩子销量压力。',
             '只用用户明确提供的最少材料。此文件不含个人历史，不能假称已读取电脑、保存成绩或安排通知。', '',
             '## 现在只推进一步', '',
             '先让孩子说这次想改善什么，等待回答；依据已提供材料给一个可做首步。不要把整张卡朗读成一节理论课。',
             '仅在缺材料阻塞时追问。没有可用工程就明确采用纸图/状态卡，不能把模拟记成软件通过。',
             '已有相关基础就减少示范；遇到反复误解先补一个短专题，再回作品，不无限猜测或扩功能。']
    if openmaic:
        lines += ['', '## 给课堂生成器', '',
                  '本轮只生成解决一个实际知识缺口的短互动课，不一次生成整个阶段。先确认一个可实现的预测—对照—复位，再生成。',
                  '教师反馈与孩子题面分开；参考解不提前显示。生成后实测控件，不能把规格或静态图称为已运行课堂。',
                  '没有新软件连接、素材授权或付费授权时不自行调用；此输入不附私人记录，也不包含现成高级工程。']
    for label, key in [('进入条件（需人核对）','entry'), ('核心问题','question'), ('本轮任务','mission'),
                       ('只补这些知识','learning'), ('先做的小实验','experiment'), ('孩子讲给爸爸','explain'),
                       ('爸爸的候选反问','parent_question'), ('何时停下或改变方向','stop')]:
        lines += ['', f'**{label}：** {row[key]}']
    lines += ['', '爸爸可直接教、灵活追问或用等价问题替换，不叠加全套题。卡上公开反问是练习，不天然是未见迁移；独立检查另换情境并记录提示。',
              'AI可提方案、实现局部与建议测试；孩子负责范围、取舍与理解，成人核对关键风险。不能由AI修改断言后自批通过。',
              '', '## 当前证据关口：逐项记录，不算总分', '']
    lines += ['- [ ] ' + x + '（待验证）' for x in row['evidence']]
    lines += ['', '产物可运行、玩家体验、孩子理解、商业投入与平台审批分别判断。没有证据就待验证。',
              '', '基础回查：' + '、'.join('curriculum/lessons/' + x + '.md' for x in row['lessons']) + '。这些是入口，不代表已有完整商业专项课。',
              '进一步资料：learning-system/commercial-growth.md；learning-system/growth-knowledge-map.md。']
    if row['key'] in ('release', 'maintenance'):
        lines += ['使用learning-system/templates/release-readiness.md逐项核对；实际发布前由成人再次查官方平台规则，不把本工作单当批准。']
    template = root / DOCS[2]
    require(template.is_file() and template.stat().st_size <= MAX_BYTES, '本轮记录模板不存在或过大')
    lines += ['', '---', '', template.read_text(encoding='utf-8'), '']
    text = '\n'.join(lines)
    require(len(text.encode('utf-8')) <= MAX_BYTES, '输出过大，不会写入')
    return text


def write_new(home: Path, cycle: str, text: str, root: Path = ROOT) -> Path:
    require(re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,59}', cycle) is not None, '无效cycle')
    require(len(text.encode('utf-8')) <= MAX_BYTES, '输出过大')
    root = root.resolve()
    raw = home.absolute()
    require(not any(p.is_symlink() for p in (raw, *raw.parents)), '输出目录不能经过符号链接')
    home = raw.resolve()
    require(home != root and (root not in home.parents or root / '.learning' in home.parents),
            '仓库内只能写到.learning/子目录；也可选仓库外私人目录')
    home.mkdir(parents=True, exist_ok=True, mode=0o700)
    path = home / (cycle + '.md')
    # Exclusive creation also rejects existing symlinks. Never overwrite learner notes.
    fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8', newline='\n') as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
    except BaseException:
        path.unlink(missing_ok=True)
        raise
    return path


def check(root: Path = ROOT) -> None:
    rows = load_plan(root)
    for doc in DOCS:
        require((root / doc).is_file(), '缺少成长资料：' + doc)
    for row in rows:
        for lesson in row['lessons']:
            require((root / 'curriculum/lessons' / (lesson + '.md')).is_file(), '缺少基础课：' + lesson)
        for teacher in (False, True):
            render(row, 'validation-only', root, teacher)
    require('.learning/' in (root / '.gitignore').read_text(encoding='utf-8'), '个人目录未被忽略')
    require('commercial-growth.md' in (root / 'FAMILY-START.md').read_text(encoding='utf-8'), '亲子入口未链接成长路线')
    require('growth_workshop.py' in (root / 'learning-system/coach.md').read_text(encoding='utf-8'), '教练协议缺少阶段衔接')
    print('GROWTH CHECK PASS: 6 stages, course references, handoff and templates; no game or learning claim')


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('plan'); sub.add_parser('check')
    p = sub.add_parser('session')
    p.add_argument('stage', choices=STAGES)
    p.add_argument('--cycle', required=True)
    p.add_argument('--home', type=Path, default=ROOT / '.learning/growth')
    p.add_argument('--openmaic', action='store_true')
    args = parser.parse_args(argv)
    if args.command == 'check':
        check(); return 0
    rows = load_plan()
    if args.command == 'plan':
        print('成长阶段（不是新增课号；按证据选择，不要求依次全部完成）')
        for row in rows:
            print(row['key'] + '｜' + row['title'] + '：' + row['question'])
        return 0
    row = next(row for row in rows if row['key'] == args.stage)
    text = render(row, args.cycle, openmaic=args.openmaic)
    path = write_new(args.home, args.cycle, text)
    print('已生成本地任务：' + str(path))
    print('未调用AI、未评分、未读取个人历史、未修改游戏、未启用通知。成人检查后交给AI开始。')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, OSError, KeyError) as exc:
        print('未完成：' + str(exc), file=sys.stderr)
        raise SystemExit(1)
