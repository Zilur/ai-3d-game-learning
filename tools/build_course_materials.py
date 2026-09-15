#!/usr/bin/env python3
"""Expand authored teaching content into Markdown. No LLM calls or game changes.
Usage: python3 tools/build_course_materials.py [--check]
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import runpy
import sys
from course_order import ORDER as CANONICAL_ORDER
from numbered_navigation import finalize_navigation
from session_coach import enrich_sessions, STARTS
from scenario_sections import validate_scenarios, decorate_lesson, enrich_output, ROWS, DISPLAY
from demo_coach import prepare_lessons, enrich_demo, validate_coaching, PLANS, DIAGRAMS
from quality_review import apply_review, enrich_review, REVIEWS

ROOT = Path(__file__).resolve().parents[1]
AUTHOR = ROOT / 'curriculum/authoring'
FIXED_VIEW = runpy.run_path(str(AUTHOR / 'fixed_view_strategy.py'))
apply_fixed_view_strategy = FIXED_VIEW['apply_fixed_view_strategy']
enrich_fixed_view = FIXED_VIEW['enrich_fixed_view']
FIXED_EFFECTS = runpy.run_path(str(AUTHOR / 'fixed_view_effects.py'))
apply_fixed_view_effects = FIXED_EFFECTS['apply_fixed_view_effects']
enrich_fixed_view_effects = FIXED_EFFECTS['enrich_fixed_view_effects']
FILES = ['beginner_a.py', 'beginner_b.py', 'intermediate.py', 'advanced.py', 'art.py', 'motion.py']
ORDER = CANONICAL_ORDER
REQUIRED = {'id','title','prereq','concepts','goal','m','k','stop','body','initial','controls','steps','feedback','failure','reset','ui','questions','remember','recall','practice','sources'}

def bullets(values):
    return '\n'.join('- ' + value for value in values)

def validate(lessons, sources):
    expected = set(CANONICAL_ORDER)
    ids = [row['id'] for row in lessons]
    if set(ids) != expected or len(ids) != 47 or len(set(ORDER)) != 47 or set(ORDER) != expected:
        raise ValueError('Exactly 47 canonical generation units and order entries are required')
    by_id = {row['id']: row for row in lessons}
    for row in lessons:
        missing = REQUIRED - row.keys()
        if missing:
            raise ValueError(f"{row['id']} missing {missing}")
        if len(row['m']) != (0 if row['id'] == 'E06' else 2) or not (1 <= len(row['k']) <= 2):
            raise ValueError(f"{row['id']} learning depth mismatch")
        kinds = [q[0] for q in row['questions']]
        if kinds != (['K'] * 4 if row['id'] == 'E06' else ['P','D','T','K']):
            raise ValueError(f"{row['id']} question depth mismatch")
        if len(row['ui']) != 3 or len(row['steps']) != 3 or len(row['body']) < 2:
            raise ValueError(f"{row['id']} missing practical/teaching detail")
        for ref in row['prereq'] + row['recall']:
            if ref not in expected:
                raise ValueError(f"Unknown dependency {ref}")
        for ref in row['sources']:
            if ref not in sources:
                raise ValueError(f"Unknown source {ref}")
        for q in row['questions']:
            if len(q) != 4 or any(not str(x).strip() for x in q):
                raise ValueError(f"{row['id']} incomplete question/feedback")
        if any(token in str(row) for token in ['TODO', '待填写', '<填入']):
            raise ValueError(f"{row['id']} contains a placeholder")
    visiting, done = set(), set()
    def visit(key):
        if key in visiting:
            raise ValueError(f'Dependency cycle at {key}')
        if key in done:
            return
        visiting.add(key)
        for dep in by_id[key]['prereq']:
            visit(dep)
        visiting.remove(key)
        done.add(key)
    for key in ids:
        visit(key)
    pos = {key: i for i, key in enumerate(ORDER)}
    for row in lessons:
        if any(pos[x] >= pos[row['id']] for x in row['prereq'] + row['recall']):
            raise ValueError(f"{row['id']}: recall or dependency appears before it is learned")
    validate_scenarios(by_id)
    return by_id

def make_lesson(row, sources, teacher):
    ident = row['id']
    lines = [f"# {ident}｜{row['title']}", '', '版本：Course Manuscripts v4｜2026-09-15',
        '状态：课件正文与互动规格已编写；尚未逐课生成OpenMAIC课堂或试教。', '',
        '## 1. 本课任务卡', '', f"**产出：** {row['goal']}",
        f"**前置：** {', '.join(row['prereq']) or '无'}；**对应概念：** {row['concepts']}。",
        '**预计课堂：** ' + ('5–10分钟的认识讨论，可选。' if ident == 'E06' else '20–30分钟，可在实验前后暂停；不含后续真实软件制作时间。'),
        '**M 必须掌握：**', bullets(row['m']) if row['m'] else '无。本课全为K认识选修，不进入单机毕业细考。',
        '**K 理解即可：**', bullets(row['k']), f"**停止线：** {row['stop']}", '',
        '## 2. 必要讲解：先看现象，再给术语', '', '\n\n'.join(row['body']), '',
        '## 3. 界面与参数学习深度', '',
        '以下是后续真机操作的对应范围，不要求本轮打开软件。模拟滑块是教学控件，不代表软件都有同名按钮。会调是指看懂作用、主动选择与恢复；会定位是知道去哪找；按需查不考菜单路径、快捷键和API记忆。',
        bullets(row['ui']), '', '## 4. 互动实验规格', '',
        f"**初始状态：** {row['initial']}", f"**可操作项：** {row['controls']}",
        '**实验步骤：**', '\n'.join(f'{i+1}. {s}' for i,s in enumerate(row['steps'])),
        f"**预期反馈：** {row['feedback']}", f"**故障或反例：** {row['failure']}", f"**复位：** {row['reset']}",
        '**无图/无3D替代：** 用原创简单形状、状态卡或给定时间序列表达同一因果关系；标明“示意”，不得把预设结果说成Godot/Blender实测。不能以假按钮或不响应的截图代替交互。',
        '**完成判据：** ' + ('只做用途识别，不强制实操、诊断或迁移。' if ident == 'E06' else '对本课两项M提供操作或判断及解释；一个实验可覆盖多项。只有关键M或发现薄弱处才追加故障/变式，不为每个术语加作业。'), '',
        '## 5. 小结与必须牢记', '', bullets(row['remember']), '',
        '## 6. 训练：先作答，再看反馈', '',
        'P=预测，D=诊断，T=迁移，K=用途认识。下面是候选训练，不是每个词都做四次作业。课堂先用预测和一个操作，重点未达标再选D或T；延迟复测换对象，不重复抄答案。', '']
    for i, (kind, question, answer, hint) in enumerate(row['questions']):
        lines += [f'### {ident}-{kind}{i+1}', question, '']
    lines += ['## 7. 后续真机任务（配套待做，不作为当前课堂依赖）', '', row['practice'],
        '即使已有参考工程，也要区分课件、运行测试、人工体验、学习掌握四种证据。按用户安排，当前先完成全部课件，之后再统一补素材、Godot/Blender起始与参考工程。', '',
        '## 8. 与AI协作的最小任务', '',
        f"请围绕“{row['goal']}”准备最小演示或实现。先说明允许改变与必须保持的部分；只暴露本课参数；不要添加本课停止线中的功能。学生先预测和选参数，再由AI辅助实现，最终根据实际记录验收。", '',
        '## 9. 复现与延迟检查', '', f"本课复现：{', '.join(row['recall']) or '无前置复习，直接开始'}。只复习已学的关键M。",
        '下次课抽一个本课关键判断，换对象或数值后先独立解释。查菜单和API不扣独立判断分；被提示根因或目标值后完成，记录有提示，换变式再验。K不反复背定义。', '',
        '## 10. 依据与观看入口', '']
    lines += [f'- [{sources[s][0]}]({sources[s][1]})' for s in row['sources']]
    lines += ['', '技术来源支持术语和软件边界；具体实验与课程顺序是本项目教学设计，不代表已证明学习效果。艺术家入口用于观看研习，不等于获得图片或素材再分发许可。', '']
    if teacher:
        lines = ['> 给OpenMAIC生成器：复制本文件全文作为课程要求即可，不需要再拼接其他规则文件。本文件是教师生成规格，不是直接发给学生的讲义。',
            '> 用中文授课，英文术语附人话；优先操作与因果对照。不要扩展软件百科，不调用仓库工具，不索取密钥。',
            '> 先提出可实现的页面与互动计划，再生成本课；生成后必须实测控件。参考答案只用于教师反馈，不放在题干或初始幻灯片。前端隐藏不是保密措施。', ''] + lines
        lines += ['## 11. 教师反馈与评分依据（初始课堂不可展示）', '',
            '沿用全仓库0–2锚点：0=缺证据或错误；1=提示后完成或理由不清；2=能选择、解释并验证。实现可由AI提供，评价的是学员判断。课堂不强制凑100分；结业仍按M90/K10反馈，K不能补救关键M失败。',
            '两项M都需要有效证据，不能按四道题等权平均掩盖能力缺口。普通M用一次有效操作和解释；关键M增加故障/迁移与延迟复测。E06全K只确认用途，没有M成绩。', '']
        for i, (kind, question, answer, hint) in enumerate(row['questions']):
            lines += [f"**{ident}-{kind}{i+1} 核对要点：** {answer}", f'**错因提示：** {hint}',
                '**反馈策略：** 先指出证据缺口，给该提示；仍困难再示范。看答案后立即复述不算独立掌握。', '']
        lines += ['## 12. 生成后的验收清单', '',
            '- [ ] 先有本课目标和M/K/停止线，未把K扩为深度考试。',
            '- [ ] 参数/条件实际改变画面、状态或时间序列，数值和结果一致。',
            '- [ ] 初始状态、单变量对照、故障和复位均可运行；没有图片时替代方案有标示。',
            '- [ ] 学生作答前不展示教师答案；有针对错因的反馈与新变式。',
            '- [ ] 可用键盘/点击操作，文字可读，可暂停；不强制自动音频或高强度闪烁。',
            '- [ ] 技术实测、审美喜好和学习掌握没有混作同一个通过状态。',
            '- [ ] 外部原图/动作仅在许可允许的情况下展示；未伪造来源和运行记录。', '']
    return decorate_lesson(row, '\n'.join(lines), teacher)

def generated(lessons, sources, by_id):
    output = {}
    for row in lessons:
        output[f"openmaic/lessons/{row['id']}.md"] = make_lesson(row, sources, True)
        output[f"curriculum/lessons/{row['id']}.md"] = make_lesson(row, sources, False)
    index = ['# 课程索引：先课件，后素材与真实工程', '',
        '47份独立生成课件：初级17（A02拆A/B）、中级12、高级6、审美/美术8、动作复用2。编号保留连续性；不要求全部按表学完。',
        '每课都有正文、实验、深度、题目、评分反馈与来源。正文完成不等于课堂生成或试教完成。', '',
        '## 推荐路线', '',
        'A01 → A02 → A03 → A04 → A05 → A06 → A07 → A08 → B01 → B02 → B03 → B04–B09 → B10 → B11–B13。',
        '中级C03–D07，E01导航可跳过且不阻塞C10。D01–D04在C07/C08及B10后作为Blender美术进阶。D05/D06与高级A线按实际问题选修。', '',
        '|课号|主题|前置|深度|学生讲义|OpenMAIC完整输入|', '|---|---|---|---|---|---|']
    for ident in ORDER:
        row = by_id[ident]
        depth = '全K选修' if ident == 'E06' else '2项M + 必要K'
        index.append(f"|{ident}|{row['title']}|{', '.join(row['prereq']) or '无'}|{depth}|[阅读](lessons/{ident}.md)|[复制全文](../openmaic/lessons/{ident}.md)|")
    output['curriculum/lesson-index.md'] = '\n'.join(index) + '\n'
    review = ['# 逐课作者自审记录', '',
        '日期：2026-09-15。这是内容一致性作者自审，不是独立评审、课堂运行或真人试教。大纲两轮审核后填充正文；逐课检查了难度、反例与考核对应。',
        '自动检查只验证结构/依赖/题型/输出一致性，不能代替教学质量判断。', '',
        '|课号|本课保留的核心任务|已检查/约束的越界风险|生成后仍需实测|', '|---|---|---|---|']
    for ident in ORDER:
        row = by_id[ident]
        review.append(f"|{ident}|{row['goal']}|{row['stop']}|控件因果、复位、答案时机、迁移；未生成/未试教|")
    output['curriculum/lesson-review.md'] = '\n'.join(review) + '\n'
    refs = ['# 本轮来源索引', '', '核对日期：2026-09-15。stable/latest链接可能更新；录制或配套工程阶段另固定实际软件版本。部分手册保留已核对的旧版通用原理参考，不据此保证新版本菜单不变。', '']
    refs += [f'- `{key}`：[{title}]({url})' for key,(title,url) in sources.items()]
    refs += ['', '艺术偏好、M/K比例、时长和学习顺序是设计选择，不是研究证明的唯一最佳方案。缺图时用明确原创示意，不猜测或伪造页面内容。', '']
    output['curriculum/sources-index.md'] = '\n'.join(refs)
    for name in ['site_content.py','site_openmaic.py','site_art.py']:
        pages = runpy.run_path(str(AUTHOR / name))['PAGES']
        overlap = set(pages) & set(output)
        if overlap:
            raise ValueError(f'Duplicate authored pages: {overlap}')
        output.update(pages)
    # Existing practical files remain; point readers to the canonical classroom text.
    markers = {
        'curriculum/beginner/01-3d-space/practice.md': '> v4学生讲义：[A02](../../lessons/A02.md)、[A07](../../lessons/A07.md)。本操作单保留作后续真机补充，课程生成先用统一规格。',
        'curriculum/beginner/02-scene-node/lesson.md': '> v4课堂主稿：[A03学生讲义](../../lessons/A03.md)；[OpenMAIC完整输入](../../../openmaic/lessons/A03.md)。下方起始/参考工程保留，配套完善在课件之后。',
        'curriculum/concept-map.md': '> v4技术KN01–KN32编号保持不变。新增美术词汇见 [美术词汇表](../art/visual-vocabulary.md)，完整课件映射见 [课程索引](lesson-index.md)。',
        'assessments/exam-blueprint.md': '> v4每课配套题在 [课程索引](../curriculum/lesson-index.md) 的学生讲义中。KNxx-P/T仍为跨课题库；课号题为场景化题，不需要两套都做。审美题按说明与证据评，不按固定审美偏好评。',
        'docs/validation.md': '> v4仅新增/修订课件与作者工具，未修改game/、blender/或web/实现。旧引擎结果属于其原提交；新课堂均未逐课生成和试教。课件验证另见 [审核记录](../curriculum/lesson-review.md)。',
    }
    for name, marker in markers.items():
        original = (ROOT / name).read_text(encoding='utf-8')
        if not original.startswith(marker):
            original = marker + '\n\n' + original
        output[name] = original
    output['curriculum/beginner/01-3d-space/openmaic-spec.md'] = '# A02统一入口\n\n新版使用 [A02完整生成规格](../../../openmaic/lessons/A02.md) 和 [A07完整生成规格](../../../openmaic/lessons/A07.md)。每次复制一份全文，不再使用旧版一次讲完的长规格。历史文本保留在Git历史，避免并列不同要求。\n'
    output['curriculum/workshop-recipes.md'] = '# 工作坊规格已并入统一单课\n\n[A04碰撞](../openmaic/lessons/A04.md) · [B04材质](../openmaic/lessons/B04.md) · [B06事件](../openmaic/lessons/B06.md)。三份均含完整讲解、控件、故障、题目和教师反馈。\n\n既有game工程保留，新的逐课素材和起始/完成工程依照用户安排在课件之后完善。不能把生成输入称为已运行课堂。\n'
    # Other old requirement links remain valid but cannot compete with the canonical input.
    for path in sorted((ROOT / 'openmaic/requirements').glob('*.md')):
        ident = path.stem.split('-')[0]
        key = path.relative_to(ROOT).as_posix()
        if key not in output and ident in by_id:
            output[key] = f'# {ident}旧入口\n\n请复制 [{ident}完整OpenMAIC课件](../lessons/{ident}.md) 全文。本页只是兼容旧链接的入口，不是生成要求。\n'
    enrich_output(output, by_id, ORDER)
    enrich_demo(output, by_id, ORDER, ROWS, DISPLAY)
    enrich_review(output, by_id, ORDER, ROWS, DISPLAY)
    enrich_sessions(output, by_id, ORDER, ROWS, DISPLAY)
    finalize_navigation(output, by_id, ORDER, ROWS)
    enrich_fixed_view(output, by_id, ORDER, ROWS)
    enrich_fixed_view_effects(output, by_id, ORDER, ROWS)
    manifest = {'version':'fixed-view-effects-2026-09-15','date':'2026-09-15','lesson_count':47,
        'units':[{'id':ident,'display':DISPLAY[ident],'dialogue':'curriculum/dialogues/'+ident+'.md','prerequisites':by_id[ident]['prereq'],'concepts':by_id[ident]['concepts'],
                  'status':'manuscript-reviewed; classroom-not-generated; learner-not-tested'} for ident in ORDER],
        'source_sha256':{path.relative_to(ROOT).as_posix():hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(AUTHOR.glob('*.py'))},
        'sha256':{name:hashlib.sha256(text.encode()).hexdigest() for name,text in output.items()}}
    output['curriculum/materials-manifest.json'] = json.dumps(manifest, ensure_ascii=False, indent=2) + '\n'
    return output

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    lessons = []
    for name in FILES:
        lessons.extend(runpy.run_path(str(AUTHOR / name))['LESSONS'])
    sources = runpy.run_path(str(AUTHOR / 'sources.py'))['SOURCES']
    lessons = prepare_lessons(lessons, sources)
    lessons = apply_review(lessons, ROWS, sources)
    lessons = apply_fixed_view_strategy(lessons, ROWS, PLANS, DIAGRAMS, REVIEWS, STARTS, sources)
    lessons = apply_fixed_view_effects(lessons, ROWS, PLANS, DIAGRAMS, REVIEWS, STARTS, sources)
    by_id = validate(lessons, sources)
    validate_coaching(by_id)
    output = generated(lessons, sources, by_id)
    mismatched = []
    for name, text in output.items():
        path = ROOT / name
        if args.check:
            if not path.exists() or path.read_text(encoding='utf-8') != text:
                mismatched.append(name)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding='utf-8')
    if mismatched:
        raise RuntimeError('Out-of-date generated files: ' + ', '.join(mismatched))
    print(f'MANUSCRIPT CHECK PASS: 47 units; 188 local questions (E06 all K); {len(output)} outputs; dependency graph acyclic')
    print('No classroom generated; no game, Blender or learning outcome validated by this command.')
    return 0

if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, RuntimeError, KeyError) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
