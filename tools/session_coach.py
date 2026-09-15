"""Learner readiness and cold-start prompt support, applied to existing outputs.
No services, tools, models or game changes are executed by this module.
"""
from __future__ import annotations
import json
from pathlib import Path
import re
import runpy

ROOT = Path(__file__).resolve().parents[1]
AUTHOR = ROOT / 'curriculum/authoring'
DATA = runpy.run_path(str(AUTHOR / 'session_readiness.py'))
STARTS, REFERENCES, FALLBACKS = (DATA[key] for key in ('STARTS','REFERENCES','FALLBACKS'))
FADE = DATA['SUPPORT_FADE']


def validate_session_data(by_id, starts=None, references=None):
    starts = STARTS if starts is None else starts
    references = REFERENCES if references is None else references
    if set(starts) != set(by_id) or len(starts) != 47:
        raise ValueError('Readiness must cover exactly the existing 47 lessons')
    if not set(references) <= set(by_id) or not FADE <= set(by_id):
        raise ValueError('Unknown lesson in reference/support records')
    for ident, record in starts.items():
        if not isinstance(record, tuple) or len(record) != 2:
            raise ValueError(ident + ': readiness requires kind and minimum material')
        kind, material = record
        if kind not in FALLBACKS or not isinstance(material, str) or not material.strip():
            raise ValueError(ident + ': empty or unknown readiness')
        if (kind == 'decision') != (not by_id[ident]['m']):
            raise ValueError(ident + ': K-only boundary changed')
    for ident, record in references.items():
        if len(record) != 2 or not all(record):
            raise ValueError(ident + ': reference needs limitation')
        rel = Path(record[0])
        if rel.is_absolute() or '..' in rel.parts or not str(rel).startswith('game/'):
            raise ValueError(ident + ': unsafe reference path')
        if not (ROOT / rel).is_file():
            raise ValueError(ident + ': claimed reference file is absent')
    return True


def session_card(row, display):
    ident = row['id']
    kind, material = STARTS[ident]
    lines = ['## 0. 开始前：只准备本课需要的东西', '',
             '**本次起点：** ' + material,
             '**缺材料时：** ' + FALLBACKS[kind],
             '**当前配套：** ' + (f'仓库已有 `{REFERENCES[ident][0]}`。{REFERENCES[ident][1]}' if ident in REFERENCES else '本课起始包尚未由这一轮交付；不要把下方目标、代码建议或示意看成已经存在的工程。'), '']
    if not row['m']:
        lines.append('**本次结束：** 用一个情境说明用途与当前不做什么；不要求实操、软件截图或M评分。')
    else:
        lines += ['**今天的最小任务：** ' + row['goal'],
                  '**怎样读：** 先看两项M和概念图，再复制对话1。启动框已带首步、继续条件和结束证据；之后用自己的话回复即可，不必把六框逐一重发。',
                  '**怎样停：** 完成当前小步可以暂停，记录下次起点；只有本课两项M都有相应证据才标本课应用通过。暂停不是失败，模拟完成不是软件通过。']
        if ident in FADE:
            lines.append('**逐渐减少代答：** 本课先由你写一个目标、修改范围和验证办法，AI再执行或补一个线索。可以请求示范，但那次记录为有提示练习，不以拒绝帮助作为考核。')
        else:
            lines.append('**先学再验：** 初次允许AI示范一小步，你再换一个值/对象作选择；需要检查独立判断时换未讲过的变式，不要求从零手写代码。')
    return '\n'.join(lines) + '\n\n'


def cold_start_context(row, scenarios, plans):
    ident = row['id']
    kind, material = STARTS[ident]
    first, gate, second, _graph = plans[ident]
    d = scenarios[ident]
    lines = ['本课入场材料：' + material,
             '材料不足的处理：' + FALLBACKS[kind],
             '以下是本课连续推进卡，不是一次性执行授权；收到我的观察后每轮最多推进一个有意义的小步。']
    if not row['m']:
        lines += ['用途任务：' + first, '结束判断：' + gate,
                  '随后：' + second + '；保持全K，不生成实现。']
    else:
        lines += ['首步：' + first, '继续条件：' + gate, '随后一步：' + second,
                  '结束证据：' + '；'.join(d['accept']),
                  '相关回归：' + d['regress']]
        if ident in FADE:
            lines.append('验收时先等我提出目标、修改范围和验证办法，不先替我判断；若我请求帮助，切回练习并如实记录提示。')
    lines += ['这些是待执行要求，不是我的已完成进度。不要凭课号推断前置已通过；只复用我已提供的实际材料和证据。',
              '对话1之后我可直接回复完成/不符/报错/暂停，无需重贴整课；你应沿这张推进卡继续，不临时增加系统。']
    return '\n'.join(lines) + '\n'


def decorate_session(text, row, scenarios, display, plans, teacher, dialogue):
    if '## 0. 开始前：只准备本课需要的东西' in text:
        raise ValueError(row['id'] + ': readiness applied twice')
    anchor = '## 2A. 场景、概念图与逐步AI对话' if dialogue else '## 1. 本课任务卡'
    if text.count(anchor) != 1:
        raise ValueError(row['id'] + ': unknown lesson layout')
    text = text.replace(anchor, session_card(row, display) + anchor, 1)
    prompt_anchor = '先给一个预测问题并等我回答，再给一个最小步骤。'
    if text.count(prompt_anchor) != 1:
        raise ValueError(row['id'] + ': missing cold-start prompt anchor')
    text = text.replace(prompt_anchor, cold_start_context(row, scenarios, plans) + prompt_anchor, 1)
    # Keep instructional prompts as resources, not compulsory narration or six exams.
    if teacher:
        note = ('> 课堂编排补充：不要把全部协作提示词、权限边界和检查清单逐字朗读成幻灯片。先显示本课目标和一个概念对照，安排一次可操作实验，再按学员需要展示可复制对话资源。\n'
                '> 缺少真实软件/图片时可以做明示的概念模拟；模拟目标通过与真机应用通过分别记录。不得创建无响应的滑杆，不能渲染3D时选能保留同一因果关系的替代，否则标该实验未完成。\n\n')
        text = note + text
    return text


def validate_first_prompts(output, by_id):
    for ident, row in by_id.items():
        for folder in ('curriculum/lessons','openmaic/lessons','curriculum/dialogues'):
            text = output[f'{folder}/{ident}.md']
            found = re.search(r'### 对话1[^\n]*\n.*?```text\n(.*?)\n```', text, re.S)
            if not found:
                raise ValueError(ident + ': missing first copyable frame')
            frame = found.group(1)
            tokens = ('本课入场材料：','材料不足的处理：','连续推进卡','不是我的已完成进度')
            tokens += ('首步：','继续条件：','随后一步：','结束证据：','相关回归：') if row['m'] else ('用途任务：','结束判断：','保持全K')
            if not all(token in frame for token in tokens):
                raise ValueError(ident + ': copied first frame is not self-contained')
            if not row['m'] and '结束证据：' in frame:
                raise ValueError('K-only topic gained an M execution gate')
    return True


def enrich_sessions(output, by_id, order, scenarios, display):
    from demo_coach import PLANS
    validate_session_data(by_id)
    for ident in order:
        for folder, teacher, dialogue in [('curriculum/lessons',False,False),('openmaic/lessons',True,False),('curriculum/dialogues',False,True)]:
            key = f'{folder}/{ident}.md'
            output[key] = decorate_session(output[key], by_id[ident], scenarios, display, PLANS, teacher, dialogue)
    pages = runpy.run_path(str(AUTHOR / 'session_pages.py'))['PAGES']
    allowed_replacements = {'START-HERE.md'}
    conflict = set(pages) & set(output) - allowed_replacements
    if conflict:
        raise ValueError('Unapproved page replacement: ' + repr(conflict))
    output.update(pages)
    output['curriculum/lesson-index.md'] += ('\n## 开始之前与复测\n\n[第一次学习怎么开始](first-session.md) · [预览、亲调与保存](preview-and-save.md) · [不含答案的迁移任务](../assessments/transfer-stations.md)。每课对话1已含准备条件、首步和结束证据；不必重复粘贴六个提示框。\n')
    output['README.md'] = '> 学习接续修订：[第一次怎么开始](curriculum/first-session.md) · [预览与保存](curriculum/preview-and-save.md)。47课启动框可独立带出本课路线；缺配套不冒充完成。\n\n' + output['README.md']
    output['curriculum/delivery-status.md'] = ('> 学习接续修订：47课已写入最小入场材料、缺材料分支和可独立复制的推进卡；加入预览保存指引、迁移任务与试教协议。现有参考路径仅核对存在，新的OpenMAIC课堂、逐课工程和真人试学仍未由本轮完成。\n\n' + output['curriculum/delivery-status.md'])
    output['AGENTS.md'] += ('\n## 学习接续维护\n\nsession_readiness.py与session_pages.py维护入场材料/缺失分支和使用说明；tools/session_coach.py在原课件装配后补同一份输出，不增加第四套课号。对话1必须自带首步、继续条件与证据；公开迁移题只是自测，不是防作弊系统。执行check_session_readiness.py与现有验证，不把静态检查称为课堂试教。\n')
    validate_first_prompts(output, by_id)
    trace = {'kind':'author-designed-readiness; not-runtime-or-learner-validation','date':'2026-09-15', 'count':len(by_id),
             'units':[{'id':ident,'display':display[ident],'mode':STARTS[ident][0], 'minimum':STARTS[ident][1],
                       'reference':REFERENCES.get(ident), 'support_fade':ident in FADE} for ident in order]}
    output['curriculum/session-readiness.json'] = json.dumps(trace, ensure_ascii=False, indent=2) + '\n'
    return output
