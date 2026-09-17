#!/usr/bin/env python3
"""Validate an AI-assisted learning report, then render limited-scope feedback.
No LLM call, grading of prose, command execution, or evidence authenticity claim.
"""
from __future__ import annotations
import argparse
import copy
import json
from pathlib import Path
import sys

AXES = ('recall', 'reasoning', 'application', 'transfer')
LABELS = {'recall': '回忆', 'reasoning': '解释', 'application': '软件应用', 'transfer': '换情境'}
KINDS = {'recall': {'answer'}, 'reasoning': {'answer'}, 'application': {'software'}, 'transfer': {'transfer'}}
ROOT = Path(__file__).resolve().parents[2]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate(report: dict, objectives: dict) -> list[dict]:
    require(isinstance(report, dict) and report.get('schema_version') == 1, 'schema_version must be 1')
    targets = report.get('target_objectives')
    require(isinstance(targets, list) and 0 < len(targets) <= 200, 'select 1–200 target objectives')
    require(all(isinstance(x, str) and x in objectives for x in targets), 'unknown target objective')
    require(len(set(targets)) == len(targets), 'duplicate target objective')
    items = report.get('items')
    require(isinstance(items, list) and len(items) <= 200, 'items must be a bounded list')
    seen = set()
    for item in items:
        require(isinstance(item, dict), 'each item must be an object')
        ident = item.get('objective')
        require(isinstance(ident, str) and ident in targets and ident not in seen, 'unexpected/duplicate item')
        seen.add(ident)
        evidence = item.get('evidence', [])
        require(isinstance(evidence, list) and len(evidence) <= 30, ident + ': invalid evidence list')
        ev = {}
        for entry in evidence:
            require(isinstance(entry, dict), ident + ': evidence must be an object')
            eid = entry.get('id')
            require(isinstance(eid, str) and eid and eid not in ev, ident + ': duplicate/empty evidence id')
            require(entry.get('kind') in {'answer', 'software', 'transfer'}, ident + ': unsupported evidence kind')
            require(all(isinstance(entry.get(k), str) and 0 < len(entry[k].strip()) <= 4000
                        for k in ('reference', 'summary')), ident + ': cite evidence location and observation')
            ev[eid] = entry
        observations = item.get('observations')
        require(isinstance(observations, dict) and set(observations) == set(AXES), ident + ': need four separate observations')
        for axis in AXES:
            obs = observations[axis]
            require(isinstance(obs, dict), ident + ': invalid observation')
            score = obs.get('score')
            require(score is None or type(score) is int and 0 <= score <= 2, ident + ': score is null or 0–2')
            require(obs.get('support') in ('L0', 'L1', 'L2', 'L3'), ident + ': record hint level')
            refs = obs.get('evidence_ids')
            require(isinstance(refs, list) and all(isinstance(r, str) and r in ev for r in refs), ident + ': unknown evidence ref')
            if objectives[ident]['level'] == 'K':
                require(axis == 'reasoning' or score is None, ident + ': K only checks use, not implementation or memorization')
            if score is not None:
                require(bool(refs) and any(ev[r]['kind'] in KINDS[axis] for r in refs), ident + ': score needs matching evidence')
                require(not (score == 2 and obs['support'] in ('L2', 'L3')), ident + ': revealed solution cannot count as independent')
        diagnosis = item.get('diagnosis')
        require(isinstance(diagnosis, dict), ident + ': missing diagnostic explanation')
        require(diagnosis.get('status') in ('pending-evidence', 'hypothesis', 'needs-practice', 'no-gap-observed'), ident + ': invalid diagnosis status')
        for key in ('basis', 'next_question', 'next_task', 'recheck'):
            require(isinstance(diagnosis.get(key), str) and 0 < len(diagnosis[key].strip()) <= 4000,
                    ident + ': diagnosis needs ' + key)
    return items


def priority(item: dict) -> int:
    scores = [o['score'] for o in item['observations'].values() if o['score'] is not None]
    if 0 in scores:
        return 0
    if 1 in scores:
        return 1
    return 2 if any(o['score'] is None for o in item['observations'].values()) else 3


def clean(value: str) -> str:
    return str(value).replace('|', '／').replace('\n', ' ').replace('<', '〈').replace('>', '〉')


def render(report: dict, objectives: dict) -> str:
    items = validate(report, objectives)
    lines = ['# 学习诊断摘要', '',
             '范围：仅本次选择的能力；不生成阶段总分，不宣布结业。证据真实性与判断仍需人工/教师核对。',
             '本工具只检查记录结构和明显越界，不理解或评分自然语言，不调用AI，不运行工程。', '',
             '|能力|回忆|解释|软件应用|换情境|', '|---|---|---|---|---|']
    for item in sorted(items, key=priority):
        cells = []
        for axis in AXES:
            obs = item['observations'][axis]
            if objectives[item['objective']]['level'] == 'K' and axis != 'reasoning':
                cells.append('不要求')
            else:
                cells.append('待验证' if obs['score'] is None else f"{obs['score']} / {obs['support']}")
        ident = item['objective']
        lines.append('|'+clean(ident + ' ' + objectives[ident]['text'])+'|'+'|'.join(cells)+'|')
    missing = [x for x in report['target_objectives'] if x not in {i['objective'] for i in items}]
    if missing:
        lines += ['', '**尚无记录（不是0分）：** ' + '、'.join(missing)]
    lines += ['', '## 下一次只处理一至两项', '',
              '下列顺序是整理规则，不是已证实的最优学习算法；优先修明确错误，再处理提示依赖和证据缺口。']
    candidates = [i for i in sorted(items, key=priority) if i['diagnosis']['status'] != 'no-gap-observed']
    if not candidates:
        lines += ['', '已提交证据中暂无待补练项；未测部分不等于已通过，也不因此自动追加作业。']
    for item in candidates[:2]:
        ident, d = item['objective'], item['diagnosis']
        lines += ['', '### ' + clean(ident),
                  '**证据/假设：** ' + clean(d['basis']),
                  '**先追问：** ' + clean(d['next_question']),
                  '**只补这一项：** ' + clean(d['next_task']),
                  '**再检查：** ' + clean(d['recheck']),
                  '**回课件：** ' + objectives[ident]['lesson'] + '；只复习相应M/K，不重学整章。']
    lines += ['', '代码/自动测试成功不等于学习掌握；一张静态图不证明时序、碰撞或重复事件。', '']
    return '\n'.join(lines)


def self_test() -> None:
    objectives = {'A04.M1': {'level': 'M', 'text': '区分可见/阻挡/检测', 'lesson': 'A04'},
                  'E06.K1': {'level': 'K', 'text': '用途', 'lesson': 'E06'}}
    empty = {axis: {'score': None, 'support': 'L0', 'evidence_ids': []} for axis in AXES}
    sample = {'schema_version': 1, 'target_objectives': ['A04.M1'], 'items': [{
        'objective': 'A04.M1', 'observations': copy.deepcopy(empty),
        'evidence': [{'id': 'e1', 'kind': 'answer', 'reference': '构造样例：答复1', 'summary': '只作解释，不声称运行'}],
        'diagnosis': {'status': 'pending-evidence', 'basis': '缺软件记录', 'next_question': '预测隐藏后怎样？',
                      'next_task': '在副本做一次对照', 'recheck': '下次会话换物体'}}]}
    sample['items'][0]['observations']['reasoning'] = {'score': 2, 'support': 'L0', 'evidence_ids': ['e1']}
    validate(sample, objectives)
    cases = []
    for mutate in [
        lambda r: r['items'][0]['observations']['reasoning'].update(score=True),
        lambda r: r['items'][0]['observations']['reasoning'].update(score=3),
        lambda r: r['items'][0]['observations']['reasoning'].update(evidence_ids=[]),
        lambda r: r['items'][0]['observations']['reasoning'].update(support='L2'),
        lambda r: r['items'][0]['observations']['application'].update(score=2, evidence_ids=['e1']),
        lambda r: r['items'][0]['observations']['transfer'].update(score=2, evidence_ids=['e1']),
        lambda r: r['items'].append(copy.deepcopy(r['items'][0])),
        lambda r: r['target_objectives'].append('Z99.M1'),
        lambda r: r['items'][0]['observations']['reasoning'].update(evidence_ids=['absent']),
    ]:
        bad = copy.deepcopy(sample)
        mutate(bad)
        cases.append(bad)
    k = copy.deepcopy(sample)
    k['target_objectives'] = ['E06.K1']; k['items'][0]['objective'] = 'E06.K1'
    validate(k, objectives)
    require('|不要求|2 / L0|不要求|不要求|' in render(k, objectives), 'K implementation must be not-required, not pending')
    no_gap = copy.deepcopy(k)
    no_gap['items'][0]['diagnosis']['status'] = 'no-gap-observed'
    require('暂无待补练项' in render(no_gap, objectives), 'no invented remediation for no-gap')
    k['items'][0]['observations']['application'] = {'score': 1, 'support': 'L3', 'evidence_ids': ['e1']}
    cases.append(k)
    for i, bad in enumerate(cases):
        try:
            validate(bad, objectives)
        except ValueError:
            continue
        raise AssertionError('negative probe accepted: ' + str(i))
    pending = copy.deepcopy(sample); pending['items'] = []
    require('尚无记录' in render(pending, objectives), 'missing must remain pending')
    print(f'LEARNING REPORT PASS: valid examples and {len(cases)} negative probes; not an AI/learner test')
