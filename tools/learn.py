#!/usr/bin/env python3
"""Optional self-study card + unscored notes. No AI calls, server, or parent approvals.
One visible CURRENT.md, the existing state.md store, and no duplicate transcript DB.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timedelta
import hashlib
import json
from pathlib import Path
import sys
from lib import learning_state as f
from workspace import clean_path, console
from lib.course import memory_cues

ROOT = Path(__file__).resolve().parents[1]


def home_path(path: Path, root: Path = ROOT) -> Path:
    home, root = clean_path(path), root.resolve()
    f.require(home != root and (root not in home.parents or root / '.learning' in home.parents),
              '仓库内私人笔记只能放在.learning的子目录。')
    for name in ('state.md', 'state.backup.md', 'CURRENT.md', '.write-lock'):
        f.require(not (home / name).is_symlink(), '私人记录或输出不能是符号链接。')
    return home


def state_or_empty(home: Path) -> dict:
    f.require(not (home / '.write-lock').exists(), '记录正在写入，未读取或修改。')
    return f.load_state(home) if (home / 'state.md').exists() else f.new_state()


def today_for(state: dict):
    return datetime.now(f.zone(state['timezone'])).date()


def note(state: dict, lesson: str, text: str, question: str, today, order) -> str:
    """Explicit saving of the learner's words, not NLP scoring or diagnosis."""
    f.require(lesson in order, '未知课号。')
    f.study_notes(state)
    f.require(isinstance(text, str) and 0 < len(text.strip()) <= 2000, '笔记需要1–2000字。')
    f.require(isinstance(question, str) and len(question) <= 400, '下一问限400字。')
    text, question = text.strip(), question.strip()
    digest = hashlib.sha256(json.dumps([lesson, text, question, today.isoformat()], ensure_ascii=False).encode()).hexdigest()[:16]
    ident = 'n-' + digest
    if any(row['id'] == ident for row in state.get('study_notes', [])):
        return ident
    row = {'id': ident, 'lesson': lesson, 'text': text, 'question': question,
           'created_on': today.isoformat(), 'due_on': (today+timedelta(days=1)).isoformat(), 'closed_on': None}
    f.require(len(state.get('study_notes', [])) < 10000, '笔记已达上限，请备份归档。')
    state.setdefault('study_notes', []).append(row)
    return ident


def finish(state: dict, ident: str, today) -> bool:
    for row in f.study_notes(state):
        if row['id'] == ident:
            f.require(today >= f.iso_day(row['created_on']), '结束日期早于记录。')
            if row['closed_on'] is not None:
                return False
            row['closed_on'] = today.isoformat()
            return True
    raise ValueError('没有这个轻量笔记ID；旧评分记录不能用done改写。')


def review_items(state: dict, objectives: dict, today, limit: int = 2) -> list:
    """At most two cues across new notes and legacy reports; no conversion to mastery."""
    rows = []
    for n in f.study_notes(state):
        f.require(n['lesson'] in {v['lesson'] for v in objectives.values()}, '笔记含未知课程，不自动忽略。')
        f.require(f.iso_day(n['created_on']) <= today, '发现未来笔记日期，请核对时钟。')
        if n['closed_on'] is None and f.iso_day(n['due_on']) <= today:
            rows.append({'id': n['id'], 'lesson': n['lesson'], 'due': n['due_on'],
                         'cue': n['question'] or '上次你记下：'+n['text']+'。现在有什么新理解？', 'source':'self-note'})
    for ident, _axis, track in f.due_items(state, objectives, today):
        rows.append({'id': ident, 'lesson': objectives[ident]['lesson'], 'due': track['due'].isoformat(),
                     'cue': track['diagnosis'].get('next_question') or objectives[ident]['text'], 'source':'legacy-report'})
    rows.sort(key=lambda row: (row['due'], row['id']))
    return rows[:min(2, max(0, limit))]


def review_text(state, objectives, today) -> str:
    rows = review_items(state, objectives, today)
    lines = ['## 下次先回想一两项', '', '可以跳过，不补打卡债；自述不是评分。', '']
    for row in rows:
        cue = f.safe_text(f.context_text(row['cue'], 480)).replace('[', '［').replace(']', '］')
        lines += [f'- {row["lesson"]}：{cue}（记录：`{row["id"]}`）']
    if not rows:
        lines += ['暂时没有到期问题，直接开始今天的任务。没有记录不代表已经掌握。']
    lines += ['', '笔记是私人内容；自动省略常见链接/路径不等于完全匿名，分享前请自行查看。', '']
    return '\n'.join(lines)


def start(home: Path, lesson: str, root: Path = ROOT) -> Path:
    home = home_path(home, root)
    objectives, cards, bindings, order = f.catalog(root)
    f.require(lesson in order, '未知课号，不生成文件。')
    home.mkdir(parents=True, exist_ok=True, mode=0o700)
    with f.locked(home):
        # Only our acquired lock is present. Never silently replace a broken store.
        state = f.load_state(home) if (home/'state.md').exists() else f.new_state()
        today = today_for(state)
        card = f.today_card(lesson, cards, bindings)
        title, _, body = card.partition('\n')
        result = title+'\n\n'+review_text(state, objectives, today)+'\n'+body+'\n'+memory_cues(lesson, root)
        result += ('\n完整讲解：`course/lessons/'+lesson+'.md`；在OpenMAIC已进入课堂就直接继续。\n'
                   '这张卡不是教师答案或自动接入插件；没有自动同步、评分和通知。\n')
        f.atomic_write(home/'CURRENT.md', result)
    return home/'CURRENT.md'


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--home', type=Path, default=ROOT/'.learning/family')
    sub = p.add_subparsers(dest='command', required=True)
    q = sub.add_parser('start', help='生成唯一当前任务卡；无需先init');q.add_argument('lesson')
    q = sub.add_parser('note', help='明确保存一句自己的疑问，不评分');q.add_argument('lesson');q.add_argument('text');q.add_argument('--question', default='')
    sub.add_parser('next', help='只读查看下次回想内容')
    q = sub.add_parser('done', help='结束一条笔记的回访，不标记掌握');q.add_argument('id')
    a = p.parse_args(argv)
    home = home_path(a.home)
    objectives, _cards, _bindings, order = f.catalog()
    if a.command == 'start':
        result = start(home,a.lesson)
        console('当前任务：'+str(result)+'；不需要爸爸评分或批准，未创建新成绩。')
        return 0
    state = state_or_empty(home)
    today = today_for(state)
    if a.command == 'next':
        console(review_text(state, objectives, today));return 0
    # Validate before creating any private files.
    if a.command == 'note':
        note(state,a.lesson,a.text,a.question,today,order)
    else:
        finish(state,a.id,today)
    home.mkdir(parents=True,exist_ok=True,mode=0o700)
    with f.locked(home):
        state = f.load_state(home) if (home/'state.md').exists() else f.new_state()
        before = json.dumps(state,ensure_ascii=False,sort_keys=True)
        today = today_for(state)
        ident = note(state,a.lesson,a.text,a.question,today,order) if a.command=='note' else a.id
        if a.command=='done':finish(state,a.id,today)
        if before != json.dumps(state,ensure_ascii=False,sort_keys=True):
            f.save_state(home,state)
    console(('已保留疑问原话：' if a.command=='note' else '已结束这条回访：')+ident+'；未评分、未上传、未宣称掌握。')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, OSError, KeyError, TypeError) as exc:
        console('未完成：'+str(exc),stream=sys.stderr)
        raise SystemExit(2)
