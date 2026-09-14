"""Render the authored scenario links into the SAME 45 lessons. No model calls.
Checks here cover editorial structure, not software execution or learner mastery.
"""
from __future__ import annotations
import json
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[1]
AUTHOR = ROOT / 'curriculum/authoring'
FILES = ('application_beginner.py', 'application_intermediate.py', 'application_art.py', 'application_optional.py')
SERIES = (
    ('A', '基础认知与风格对话', ('R01','B01A','B02','B01B')),
    ('B', 'Godot核心与小游戏闭环', ('B04','B03','B05','B06','B10','B11','B12','B13','B14','B16')),
    ('C', 'Blender与审美、资产改造', ('R02','B07','R03','B08','B09','R04','R05','R06','R07','R08')),
    ('D', 'AI协作、复用与可靠交付', ('B15','I03','I10','I11')),
    ('E', '角色、进阶与按需专题', ('I01','I02','I04','I05','I06','I07','I08','I09','I12','X01','X02','A01','A02','A03','A04','A05','A06')),
)
DISPLAY = {old: f'{letter}-{i:02}' for letter, _, ids in SERIES for i, old in enumerate(ids, 1)}
ROWS = {}
for filename in FILES:
    block = runpy.run_path(str(AUTHOR / filename))['SCENARIOS']
    if set(block) & set(ROWS):
        raise ValueError('Duplicate application record in ' + filename)
    ROWS.update(block)
FIELDS = {'place','before','after','task','keep','tweaks','accept','regress','transfer','risk'}
SANDBOX = {'X01','X02','A01','A02','A03','A04','A06'}
CRITICAL = {'B01A','B01B','B02','B03','B04','B05','B06','B08','B09','B10','B12','B14','B15','B16','I01','I02','I03','I10','I11','I12','R05','R07','R08'}


def mode(ident):
    if ident == 'A05':
        return 'K用途决策：不实现'
    if ident in SANDBOX:
        return '选修隔离实验：有价值才接入'
    if ident == 'I08':
        return '可选导航：不阻塞机关路线'
    return '主项目中的功能、视觉或交付决定'


def validate_scenarios(by_id):
    if set(ROWS) != set(by_id) or set(DISPLAY) != set(by_id):
        raise ValueError('Application/ABCDE coverage differs from canonical lessons')
    if len(DISPLAY) != 45 or len(set(DISPLAY.values())) != 45:
        raise ValueError('ABCDE labels must be one-to-one with the existing 45 units')
    tasks = set()
    for ident, data in ROWS.items():
        if set(data) != FIELDS:
            raise ValueError(f'{ident}: incomplete scenario fields')
        for key in FIELDS - {'tweaks','accept'}:
            if not isinstance(data[key], str) or not data[key].strip():
                raise ValueError(f'{ident}: empty {key}')
        count = 1 if ident == 'A05' else 2
        if len(data['accept']) != count or len(data['tweaks']) != count:
            raise ValueError(f'{ident}: evidence/tweak load violates M/K scope')
        if any(len(t) != 3 or not all(t) for t in data['tweaks']):
            raise ValueError(f'{ident}: each tweak needs entry, action and observation')
        if data['task'] in tasks:
            raise ValueError(f'{ident}: generic duplicate work prompt')
        tasks.add(data['task'])
        if any(x in str(data) for x in ('TODO','待填写','<填入')):
            raise ValueError(f'{ident}: unfilled authoring placeholder')
        if ident == 'A05' and by_id[ident]['m']:
            raise ValueError('The multiplayer recognition topic must remain K-only')
    return True


def _mermaid_label(text):
    return json.dumps(text.replace('\n',' ').replace('|',' / '), ensure_ascii=False)


def ai_card(row):
    ident = row['id']
    d = ROWS[ident]
    lines = ['## 2A. 这次在实际场景里解决什么', '',
        f"**应用位置：** {d['place']}；{mode(ident)}。", '',
        '|开始时遇到的问题|本课期望得到的变化|', '|---|---|',
        f"|{d['before']}|{d['after']}|", '',
        '**这是目标状态对照，不是已完成截图。** 首次操作应使用匹配当前进度的最小场景；还没有配套时，只能记为课堂模拟，不能直接勾选真机应用通过。', '',
        '### 概念关系示意', '', '```mermaid', 'flowchart LR',
        f"  S[{_mermaid_label(d['place'].split('｜')[-1])}] --> K[{_mermaid_label(row['concepts'])}]",
        '  K --> AI["AI准备局部初稿"]', '  AI --> H["人选择、亲调或作用途决定"]',
        '  H --> V["对照证据与旧功能回归"]', '```',
        '图中箭头表示教学流程，不是引擎节点继承。OpenMAIC不支持Mermaid时改画等价方框图，不能把代码原文冒充运行示意。', '',
        '### 先让AI帮助理解，再让AI帮助工作', '',
        '**学习指令：**', '```text',
        f"现在只检查这道判断：{row['questions'][0][1]}",
        '先等我给预测和理由，再指出一个证据缺口；一次只给一个线索，不先公布完整答案。',
        '我的用词不专业时，先用人话确认意思，再补对应术语。', '```', '',
        '**工作指令：可复制；先补实际版本与当前材料，不粘贴密钥。**', '```text',
        '我正在逐步制作同一个小型单机「星光小庭院」，不是重新生成整款游戏。',
        '我会提供实际软件版本、当前场景/文件和必要截图；先确认你能访问哪些材料和工具。',
        f"这次只做：{d['task']}", f"必须保持：{d['keep']}",
        '先列出将改的对象、原值和预期结果，提供最小可撤销初稿及检查步骤。',
        '没有真实软件连接时只提供操作单/脚本，不声称已经编辑、运行或看过未提供的截图。',
        '不要自动安装插件、联网下载素材、购买服务或读取无关文件；必要操作另说明并取得授权。',
        '完成后报告实际做了什么、还没验证什么；我负责选择和最终验收。', '```', '',
        '### 哪些地方比继续发指令更适合亲自试', '',
        '|入口与性质|一次只做的微调/选择|亲眼观察什么|', '|---|---|---|']
    for entry, action, observe in d['tweaks']:
        lines.append(f'|{entry}|{action}|{observe}|')
    lines += ['',
        '**初值与恢复：** 先读取并记录当前值；表里的方向是对照办法，不是通用最佳参数。先在副本上操作，不覆盖基底；返回前用撤销或记录值恢复并重新预览。自定义变量不是软件内置参数。',
        '**选择下一步：** 方向不对，补一张明确参考并圈出要借鉴的部分；结构/因果不对，让AI做局部修复；已接近目标且入口可直接操作，先亲调一项。原因不明先做对照，不靠反复重生成抽卡。', '',
        '**局部修复指令：**', '```text',
        '保留本课「必须保持」的部分。我会给出同条件的当前结果和目标差异。',
        f"只围绕「{d['after']}」检查一个根因假设；先给最小验证，未经证据不要重写全部内容。",
        '若只是一个可见参数偏差，告诉我该选哪个对象、哪个入口、怎么小幅调和恢复。', '```', '',
        f"**本课风险检查：** {d['risk']}",
        '**时间边界：** 上述是需要在当前模型/工具/软件版本下验证的风险清单，不是所有AI必然失败的结论，也不预测何时会解决。长期保留的是目标、约束、参考选择、结果认可和取舍责任；测量和重复调整可以继续交给AI协助。', '']
    return '\n'.join(lines)


def completion_card(row):
    ident = row['id']
    d = ROWS[ident]
    lines = ['## 8. 实际应用验收：把结果放回同一个项目', '',
        f"**本课产物：** {d['after']}",
        f"**接入边界：** {d['keep']}", '',
        '以下是要采集的证据，不是宣称已经执行。记录“未尝试 / 有提示完成 / 独立验证 / 隔次仍会”；不把这四种状态与M/K学习要求混淆。', '']
    if ident == 'A05':
        lines += ['本课全部K：只提交一次用途判断，不要求操作、实现或深度故障排查。',
                  '- [ ] ' + d['accept'][0]]
    else:
        lines += ['|原有M能力|本次在哪里取证|', '|---|---|']
        for goal, proof in zip(row['m'], d['accept']):
            lines.append(f'|{goal}|{proof}|')
        lines += ['', f"**旧功能回归：** {d['regress']}",
            '**最小记录：** 一段现场演示，或同条件前后图/日志，加一句“我改了什么、为什么”。截图不足以证明运动/一次性事件时，要演示动作或查看对应状态。记录用过的提示，不要求写长报告。',
            ('**关键能力复测：** 本课高频或返工风险较高，已有有效证据可复用；薄弱处增加一个未知故障或隔次变式，不把每个词都变成一套试卷。' if ident in CRITICAL else '**一般能力取证：** 一次有效操作/选择与解释即可；只有证据不足才补练，不强制反复考试。')]
    lines += ['', f"**换情境的候选任务：** {d['transfer']}",
        '**判定：** 普通M按原0–2锚点；有针对性根因提示记练习，换变式再验证。K只查用途，不能抵消关键M失败。没有真实操作的M只记待验证，模拟通过不能自动升级为真机通过。未选专题不阻塞主线。', '',
        '**接入不等于新增系统：** 美术课可交风格卡、参数决定或改造样本；性能课可得出“不优化”。隔离实验只有对当前项目有收益才接入，不强迫庭院变成战斗、开放世界或联网游戏。', '']
    return '\n'.join(lines)


def decorate_lesson(row, text, teacher):
    ident = row['id']
    old_heading = f"# {ident}｜{row['title']}"
    if text.count(old_heading) != 1:
        raise ValueError(f'{ident}: unexpected lesson title')
    text = text.replace(old_heading, f"# {DISPLAY[ident]}｜{row['title']}\n\n> 兼容课号：{ident}。ABCDE是主题入口，不是必须按字母顺序完成；文件链接与题号保留稳定。", 1)
    text = text.replace('版本：Course Manuscripts v4｜2026-09-15', '版本：Applied Curriculum v5｜2026-09-15', 1)
    anchor = '## 3. 界面与参数学习深度'
    if text.count(anchor) != 1:
        raise ValueError(f'{ident}: missing insertion anchor')
    text = text.replace(anchor, ai_card(row) + '\n' + anchor, 1)
    start = text.index('## 8. 与AI协作的最小任务')
    end = text.index('## 9. 复现与延迟检查', start)
    text = text[:start] + completion_card(row) + '\n' + text[end:]
    if teacher:
        text = text.replace('## 12. 生成后的验收清单',
            '## 12. 生成后的验收清单\n\n- [ ] 概念之后立即出现本课真实情境、学习/工作指令和微调入口，不只在结尾贴通用提示。\n- [ ] AI模拟执行与真实工具执行明确区分，主项目成果必须另有应用证据。', 1)
    return text


def enrich_output(output, by_id, order):
    validate_scenarios(by_id)
    guide = ['# ABCDE主题入口与旧课号对照', '',
        '新展示号带连字符，例如A-01；旧A01仍指旧高级测量课，不能当成新A-01。只调整展示分类，不改45个稳定文件路径、C01–C32或既有题号。不是第二套课程。',
        '主题不是难度。按课程索引前置顺序穿插学习，AI协作从第一课就使用，不等到D系列才开始。', '',
        '|新号|主题|兼容课号|学生讲义|OpenMAIC全文|', '|---|---|---|---|---|']
    for letter, label, ids in SERIES:
        for ident in ids:
            guide.append(f"|{DISPLAY[ident]}|{label}：{by_id[ident]['title']}|{ident}|[阅读](lessons/{ident}.md)|[生成输入](../openmaic/lessons/{ident}.md)|")
    output['curriculum/series-guide.md'] = '\n'.join(guide) + '\n'
    index = output['curriculum/lesson-index.md']
    index = index.replace('|课号|主题|', '|展示号 / 兼容课号|主题|', 1)
    for ident in order:
        index = index.replace(f'|{ident}|', f'|{DISPLAY[ident]} / {ident}|', 1)
    output['curriculum/lesson-index.md'] = '> v5：[逐课应用地图](application-map.md) · [ABCDE与旧号对照](series-guide.md)。先看本课解决的实际问题，再复制教师输入；不要求按字母顺序学习。\n\n' + index
    page = ['# 逐课应用地图：概念必须落在真实问题上', '',
        '版本v5，2026-09-15。45课的应用情境、AI局部指令、手动选择、证据和回归已回填到学生稿与教师输入。这里描述目标，不宣称新课堂或真机配套已运行。',
        '同一个「星光小庭院」从灰盒到完整收集循环，再到小型角色/机关扩展与美术精修。每课改一件事，之前会用的不能被改坏。', '',
        '**看懂 / 在模拟里做过 / 在真实软件用过 / 换情境仍会，是不同状态。** M的实际应用需要后两类的相应证据；K只要求用途判断。无配套、无执行证据时必须记待验证。', '',
        '|展示号（旧号）|实际问题与应用位置|预期变化|接入方式|', '|---|---|---|---|']
    for ident in order:
        d = ROWS[ident]
        place = d['place'].replace('｜','：')
        page.append(f"|[{DISPLAY[ident]} / {ident}](lessons/{ident}.md)|{place}：{d['before']}|{d['after']}|{mode(ident)}|")
    page += ['', '## 每课不用额外写一篇报告', '',
        '学员先预测，借助AI准备局部初稿，亲自作一个选择或微调，再证明当前目标与一项旧功能。关键薄弱能力换情境复测。允许查菜单/API和使用AI代码，评分不看提示词花哨程度、代码行数或模型复杂度。', '',
        '## 未选专题怎样处理', '',
        'X动作与高级专项先在副本；未选不考。A05多人全K，仅讨论两个玩家同时请求同一物品的需求，不要求部署。A06需先有一个实际专项/交付问题的证据，没有则不急着参加，不把未实现当通过。', '',
        '## 结构审查与后续验证', '',
        '本次按45条记录逐项写入情境和局部任务，并检查覆盖、M/K负担、输出一致性、单独提示和回归字段。这是作者审查加结构校验，不是独立评审，不保证教学效果已经验证。',
        '重点复核：B03速度不重复乘delta；B08共享阶段不能宣称对照球固定；B10两层防重分别看证据；I10不能覆盖唯一原档；R04来源与观察分开；X01不保证任意骨架兼容。', '',
        '下一步生成代表课堂并实操，再补真实软件配套；本轮没有扩大game/、blender/、web/。图表为文字结构示意，不是游戏截图或大师原作。', '',
        '[原项目里程碑](project-spine.md) · [场景化验收](../assessments/application-evidence.md) · [AI使用边界](ai-workflow.md)', '']
    output['curriculum/application-map.md'] = '\n'.join(page)
    prefix = '> v5更新：[逐课实际应用地图](curriculum/application-map.md) · [ABCDE主题索引](curriculum/series-guide.md)。45课已回填具体AI指令、亲调入口和应用验收；当前仍是课程设计，不能把它写成45课真机已通过。\n\n'
    for name in ('README.md','START-HERE.md'):
        if name in output:
            output[name] = prefix + output[name]
    if 'curriculum/delivery-status.md' in output:
        output['curriculum/delivery-status.md'] = '> v5：45课已回填实际场景、局部AI工作、人工微调、M证据与回归；ABCDE为展示分类，旧路径兼容。新增课堂生成、真机配套、图片成品和学习效果均尚未由本次文本回填验证。[逐课查验](application-map.md)。\n\n' + output['curriculum/delivery-status.md']
    if 'AGENTS.md' in output:
        output['AGENTS.md'] += '\n## v5逐课应用约束\n\napplication_*.py是每课真实情境的作者源，由tools/scenario_sections.py与原课源共同展开；不能只改单份生成MD。ABCDE展示号带连字符且有series-guide映射，旧文件/题号与C编号保持兼容。所有M都要有实际场景取证入口，K不升级深考；模拟、工具执行和学员应用分开记录。仍先课件再配套，不自动扩写引擎工程。\n'
    return output
