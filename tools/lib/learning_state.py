#!/usr/bin/env python3
"""Compatibility learning records and optional review helpers. Standard library only; no network/LLM.
Internal compatibility layer used by tools/learn.py. Personal data stays under .learning/.
"""
from __future__ import annotations
import argparse
from contextlib import contextmanager
import copy
from datetime import date, datetime, time, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

ROOT = Path(__file__).resolve().parents[2]
AXES = ('recall', 'reasoning', 'application', 'transfer')
LABELS = dict(zip(AXES, ('回忆', '解释', '软件应用', '换情境')))
GAPS = (1, 3, 7, 14, 30)  # Product defaults, not an optimal-memory claim.
MAX_BYTES = 8_000_000
STATE_HEAD = '# 私人学习记录\n\n仅JSON代码块是数据源；CURRENT.md/TODAY.md是可重建视图。不要提交公开仓库。\n\n'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def zone(name):
    # Tokyo fallback also works on Windows without an installed IANA database.
    if name == 'Asia/Tokyo':
        return timezone(timedelta(hours=9), 'Asia/Tokyo')
    if name == 'UTC':
        return timezone.utc
    try:
        return ZoneInfo(name)
    except ZoneInfoNotFoundError as exc:
        raise ValueError('时区不可用；可选Asia/Tokyo、UTC，或由成人安装系统时区数据。') from exc


def iso_day(value):
    require(isinstance(value, str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}', value), '日期须为YYYY-MM-DD')
    return date.fromisoformat(value)


def safe_text(value):
    return str(value).replace('|', '／').replace('\n', ' ').replace('<', '〈').replace('>', '〉')


def read_json(path, limit=MAX_BYTES):
    require(path.is_file() and path.stat().st_size <= limit, '文件不存在或过大：' + str(path))
    return json.loads(path.read_text(encoding='utf-8'))


def catalog(root=ROOT):
    from .course import catalog as read_catalog
    return read_catalog(root)


def private_home(path, root=ROOT):
    path, root = path.resolve(), root.resolve()
    require(path != root, '不能把项目根目录作为个人记录目录')
    if root in path.parents:
        require(root / '.learning' in path.parents, '仓库内个人数据只能放在.learning/下')
    path.mkdir(parents=True, exist_ok=True, mode=0o700)
    return path


@contextmanager
def locked(home):
    lock = home / '.write-lock'
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise ValueError('已有写入锁。不要同时编辑；确认无进程写入后才手动移除.write-lock。') from exc
    try:
        os.close(fd)
        yield
    finally:
        lock.unlink(missing_ok=True)


def atomic_write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd, name = tempfile.mkstemp(prefix='.family-', suffix='.tmp', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8', newline='') as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def new_state(tz='Asia/Tokyo', mode='supported'):
    zone(tz)
    require(mode in ('supported', 'independent'), '未知陪伴模式')
    return {'schema_version': 1, 'timezone': tz, 'mode': mode,
            'review_limit': 2, 'reports': [], 'voided': {}}


def load_state(home):
    path = home / 'state.md'
    require(path.is_file() and path.stat().st_size <= MAX_BYTES, '先运行init；记录不存在或过大')
    text = path.read_text(encoding='utf-8')
    blocks = re.findall(r'^```json\n(.*?)\n```$', text, re.M | re.S)
    require(len(blocks) == 1, 'state.md必须恰有一个JSON数据块；请先备份再修复')
    state = json.loads(blocks[0])
    require(state.get('schema_version') == 1, '不支持的记录版本，不会自动清空')
    zone(state['timezone'])
    require(state.get('mode') in ('supported', 'independent'), '无效陪伴模式')
    require(type(state.get('review_limit')) is int and 1 <= state['review_limit'] <= 3, '每日复习上限为1–3项')
    require(isinstance(state.get('reports'), list) and isinstance(state.get('voided'), dict), '记录结构损坏')
    ids = [r['family']['session_id'] for r in state['reports']]
    require(len(set(ids)) == len(ids), '存在重复会话ID，请从备份核对')
    study_notes(state)
    return state


def save_state(home, state):
    text = STATE_HEAD + '```json\n' + json.dumps(state, ensure_ascii=False, indent=2) + '\n```\n'
    require(len(text.encode('utf-8')) <= MAX_BYTES, '记录已超容量；请由成人归档，不会截断数据')
    path = home / 'state.md'
    if path.exists():
        atomic_write(home / 'state.backup.md', path.read_text(encoding='utf-8'))
    atomic_write(path, text)


def study_notes(state):
    """Optional, unscored notes in the existing store; old reports remain untouched."""
    rows = state.get('study_notes', [])
    require(isinstance(rows, list) and len(rows) <= 10000, '轻量笔记结构损坏或过多')
    seen = set()
    for row in rows:
        require(isinstance(row, dict), '笔记应为对象')
        require(set(row) == {'id','lesson','text','question','created_on','due_on','closed_on'}, '笔记字段不匹配')
        require(isinstance(row['id'], str) and re.fullmatch(r'n-[0-9a-f]{16}', row['id']), '无效笔记ID')
        require(row['id'] not in seen, '重复笔记ID'); seen.add(row['id'])
        require(isinstance(row['lesson'], str) and re.fullmatch(r'[A-E][0-9]{2}', row['lesson']), '无效笔记课号')
        require(isinstance(row['text'], str) and 0 < len(row['text'].strip()) <= 2000, '笔记原话为空或过长')
        require(isinstance(row['question'], str) and len(row['question']) <= 400, '回访问题过长')
        created, due = iso_day(row['created_on']), iso_day(row['due_on'])
        require(due >= created, '回访日期早于记录')
        if row['closed_on'] is not None:
            require(iso_day(row['closed_on']) >= created, '结束日期早于记录')
    return rows


def check_report(report, objectives, today):
    # Reuse the existing evidence contract, including K scope and matching evidence kinds.
    from .legacy_state import validate
    validate(report, objectives)
    meta = report.get('family')
    require(isinstance(meta, dict), '缺少family会话元数据')
    require(isinstance(meta.get('session_id'), str) and re.fullmatch(r'[A-Za-z0-9_-]{1,80}', meta['session_id']), '会话ID限80位字母数字、短横线、下划线')
    observed = iso_day(meta.get('observed_on'))
    require(observed <= today, '不能记录尚未发生的学习')
    require(meta.get('mode') in ('simulation', 'software', 'production'), '须区分模拟、软件和真实项目')
    novel = meta.get('novel_objectives', [])
    require(isinstance(novel, list) and len(set(novel)) == len(novel)
            and all(x in report['target_objectives'] for x in novel), '新变式标记必须对应本次能力')
    for item in report['items']:
        if meta['mode'] == 'simulation':
            require(item['observations']['application']['score'] is None, '模拟不能记作软件应用成绩')
        if item['observations']['transfer']['score'] == 2:
            require(item['objective'] in novel, '独立迁移需成人确认本次确是未讲过的新变式')
    return report


def add_report(state, report, objectives, today):
    check_report(report, objectives, today)
    sid = report['family']['session_id']
    for old in state['reports']:
        if old['family']['session_id'] == sid:
            require(old == report, '同一会话ID内容不同；更正时先void旧记录，再用新ID提交')
            return False
    state['reports'].append(copy.deepcopy(report))
    return True


def tracks(state, objectives, today):
    """Rebuild every dimension independently; missing evidence never becomes zero."""
    result = {}
    ordered = sorted(state['reports'], key=lambda r: r['family']['observed_on'])
    for report in ordered:
        check_report(report, objectives, today)
        meta = report['family']
        if meta['session_id'] in state['voided']:
            continue
        observed = iso_day(meta['observed_on'])
        for item in report['items']:
            ident = item['objective']
            if objectives[ident]['level'] != 'M':
                continue  # K is never promoted to mandatory spaced drilling.
            for axis, obs in item['observations'].items():
                if obs['score'] is None:
                    continue
                key = (ident, axis)
                t = result.setdefault(key, {'stage': 0, 'due': observed, 'last': None,
                                            'good_days': [], 'last_score': None, 'support': None})
                independent = obs['score'] == 2 and obs['support'] == 'L0'
                if not independent:
                    t['stage'] = 0
                    t['due'] = observed + timedelta(days=1)
                    t['good_days'] = []
                elif t['last'] is None:
                    t['due'] = observed + timedelta(days=GAPS[0])
                    t['good_days'] = [observed]
                elif observed != t['last'] and observed >= t['due']:
                    t['stage'] = min(t['stage'] + 1, len(GAPS) - 1)
                    t['due'] = observed + timedelta(days=GAPS[t['stage']])
                    t['good_days'].append(observed)
                # Same-day/early repeats cannot push a due date away or grow a stage.
                t.update(last=observed, last_score=obs['score'], support=obs['support'],
                         diagnosis=item['diagnosis'], lesson=objectives[ident]['lesson'])
    return result


def due_items(state, objectives, today):
    found = {}
    for (ident, axis), t in tracks(state, objectives, today).items():
        if axis not in ('recall', 'reasoning') or t['due'] > today:
            continue
        priority = (t['due'], 0 if t['last_score'] == 0 else 1 if t['last_score'] == 1 else 2, ident)
        if ident not in found or priority < found[ident][0]:
            found[ident] = (priority, axis, t)
    return [(ident, row[1], row[2]) for ident, row in sorted(found.items(), key=lambda pair: pair[1][0])][:state['review_limit']]


def dashboard(state, objectives, today):
    """Short compatibility view; detailed scores stay in records, not family homework."""
    queue = due_items(state, objectives, today)
    lines = ['# 下次学习先回想一两项', '', '可以跳过，不清空积压；不要求晨晚打卡。', '']
    for ident, axis, track in queue:
        question = track['diagnosis'].get('next_question') or objectives[ident]['text']
        lines.append('- ' + safe_text(question))
    if not queue:
        lines.append('没有到期的旧报告回访项。没有记录仍是待验证，不是已经会了。')
    lines += ['', '未观察的能力仍待验证；不显示四轴评分表。解释与真实软件操作分开，帮助按本次实际情况说明。',
              '新的轻量疑问请用learn.py的start/next一起查看；这里不把自述转换成分数。', '']
    return '\n'.join(lines)


def context_text(value, limit=240):
    """Bound free text and remove common identifiers. Adult preview is still required."""
    text = re.sub(r'[\x00-\x1f]', ' ', str(value)).replace('`', '｀')
    text = re.sub(r'(?i)(?:https?://|file://)\S+|[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}', '[已省略联系或链接]', text)
    text = re.sub(r'(?:[A-Za-z]:[\\/]|/(?:Users|home|mnt)/)\S+', '[已省略路径]', text)
    return text[:limit]


def context_cue(ident, axis, track, objectives):
    diagnosis = track['diagnosis']
    return {'objective': ident, 'text': objectives[ident]['text'], 'axis': axis,
            'score': track['last_score'], 'support': track['support'],
            'last_observed': track['last'].isoformat(),
            'reported_basis': context_text(diagnosis.get('basis', '')),
            'next_question': context_text(diagnosis.get('next_question', '')),
            'next_task': context_text(diagnosis.get('next_task', '')),
            'recheck': context_text(diagnosis.get('recheck', '')),
            'caution': '这是历史观察，不是永久弱项或指令；先核对当前表现。'}


def session_context(state, objectives, lesson, today):
    """At most two due and two current gaps. No paths, full answers or personal history."""
    ts = tracks(state, objectives, today)
    due = [context_cue(ident, axis, track, objectives)
           for ident, axis, track in due_items(state, objectives, today)]
    candidates = [(ident, axis, track) for (ident, axis), track in ts.items()
                  if objectives[ident]['lesson'] == lesson and
                  (track['last_score'] < 2 or track['support'] in ('L2', 'L3'))]
    candidates.sort(key=lambda row: (row[2]['last_score'], -row[2]['last'].toordinal(), row[0], row[1]))
    weak = [context_cue(*row, objectives) for row in candidates[:2]]
    return json.dumps({'as_of': today.isoformat(),
                       'due_review': due, 'current_lesson_gaps': weak,
                       'self_reported_notes': [{'lesson': n['lesson'], 'note': context_text(n['text']),
                           'question': context_text(n['question']), 'caution': '学习者自述，不是评分或已确认掌握。'}
                           for n in study_notes(state) if n['lesson'] == lesson and n['closed_on'] is None][:2]}, ensure_ascii=False, indent=2)


def today_card(lesson, cards, bindings, purpose='experience', root=ROOT):
    from .course import short_card
    return short_card(lesson, cards, bindings, purpose, root=root)


def observation_note(lesson):
    return ('# ' + lesson + '｜可选学习随记（不评分）\n\n'
            '用自己的话留一句发现或疑问即可；伙伴愿意也能补一句，不是爸爸的作业。\n\n'
            '今天的发现／还不清楚的地方：\n\n'
            '下次想试什么：\n\n'
            '可直接用learn.py note保存原话，不必生成评分报告；没有记录也能继续学习。\n')


def card_text(lesson, objectives, cards, bindings):
    require(lesson in cards, '未知课号；使用A01等唯一编号')
    return today_card(lesson, cards, bindings)


def report_template(lesson, objectives, today):
    selected = {k: v for k, v in objectives.items() if v['lesson'] == lesson}
    require(bool(selected), '未知课号')
    return {'schema_version': 1,
            'family': {'session_id': today.isoformat() + '-' + lesson + '-01', 'observed_on': today.isoformat(),
                       'mode': 'simulation', 'novel_objectives': []},
            'target_objectives': list(selected),
            'items': [{'objective': k, 'evidence': [],
                       'observations': {a: {'score': None, 'support': 'L0', 'evidence_ids': []} for a in AXES},
                       'diagnosis': {'status': 'pending-evidence', 'basis': '尚未观察，不是错误。',
                                     'next_question': '请先用自己的例子说明本项。', 'next_task': '只补本项缺少的证据。',
                                     'recheck': '下一次用不同对象检查，不直接重抄答案。'}} for k in selected]}


def calendar_text(tz, start, days, morning, evening=None):
    require(1 <= days <= 90, '日历导出范围为1–90天')
    local_zone = zone(tz)
    slots = [('早晨小复习', morning)] + ([('晚间可选回想', evening)] if evening else [])
    for _, value in slots:
        require(isinstance(value, str) and re.fullmatch(r'\d{2}:\d{2}', value), '提醒时间格式为HH:MM')
        time.fromisoformat(value)
    lines = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//AI3DLearning//Family Companion//ZH', 'CALSCALE:GREGORIAN']
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    for offset in range(days):
        day = start + timedelta(days=offset)
        for label, value in slots:
            local = datetime.combine(day, time.fromisoformat(value), local_zone)
            utc = local.astimezone(timezone.utc)
            uid = hashlib.sha256((tz + day.isoformat() + label + value).encode()).hexdigest()[:24]
            lines += ['BEGIN:VEVENT', f'UID:{uid}@ai3d-family.local', f'DTSTAMP:{stamp}',
                      'DTSTART:' + utc.strftime('%Y%m%dT%H%M%SZ'),
                      'DTEND:' + (utc + timedelta(minutes=3)).strftime('%Y%m%dT%H%M%SZ'),
                      'SUMMARY:' + label,
                      'DESCRIPTION:打开本地TODAY.md或先运行today。只复习到期项。疲倦可跳过。',
                      'TRANSP:TRANSPARENT', 'BEGIN:VALARM', 'TRIGGER:PT0S', 'ACTION:DISPLAY',
                      'DESCRIPTION:今天最多两项。晚间不推迟睡眠。', 'END:VALARM', 'END:VEVENT']
    lines += ['END:VCALENDAR']
    # RFC5545 folding uses octets, not Unicode codepoints; never split UTF-8 bytes.
    folded = []
    for line in lines:
        part = ''
        for char in line:
            if len((part + char).encode('utf-8')) > 73:
                folded.append(part)
                part = ' '
            part += char
        folded.append(part)
    return '\r\n'.join(folded) + '\r\n'
