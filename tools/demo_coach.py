"""Render bounded, lesson-specific AI conversations. No AI/service execution."""
from __future__ import annotations
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[1]
AUTHOR = ROOT / 'curriculum/authoring'
EXT = runpy.run_path(str(AUTHOR / 'demo_extension.py'))
COACH = runpy.run_path(str(AUTHOR / 'conversation_plans.py'))
PLANS, DIAGRAMS = COACH['PLANS'], COACH['DIAGRAMS']
ORDER = EXT['ORDER']
prepare_lessons = EXT['prepare_lessons']

def next_lesson(ident):
    # The default continuation never silently enrolls a learner in an optional track.
    skips = {'I07':'I09', 'I10':'I11', 'R08':'I11', 'X02':'I11', 'I12':None, 'A06':None}
    if ident in skips:
        return skips[ident]
    index = ORDER.index(ident)
    return ORDER[index + 1] if index + 1 < len(ORDER) else None

def validate_coaching(by_id):
    if set(by_id) != set(PLANS) or len(by_id) != 47:
        raise ValueError('Every one of the 47 lessons needs a unique authored conversation plan')
    for ident, plan in PLANS.items():
        if len(plan) != 4 or not all(isinstance(s, str) and s.strip() for s in plan):
            raise ValueError(ident + ': incomplete conversation plan')
        if plan[3] not in DIAGRAMS:
            raise ValueError(ident + ': missing conceptual diagram')
        if next_lesson(ident) is not None and next_lesson(ident) not in by_id:
            raise ValueError(ident + ': unknown next lesson')
    if by_id['A05']['m']:
        raise ValueError('K-only recognition must not become a software execution assessment')

def block(text):
    return '```text\n' + text.strip() + '\n```'

def dialogue_card(row, data, display):
    ident = row['id']
    first, gate, second, graph = PLANS[ident]
    label = display[ident]
    k_only = not row['m']
    lines = ['## 2A. 场景、概念图与逐步AI对话', '',
        f"**实际位置：** {data['place']}。", '',
        '|操作前的问题|本课希望得到的结果|', '|---|---|',
        f"|{data['before']}|{data['after']}|", '',
        '这是目标对照，不是已完成的游戏截图。概念图为职责/因果示意，不是继承图或完整运行证明。',
        '```mermaid', DIAGRAMS[graph], '```',
        'OpenMAIC不能渲染Mermaid时画等价方框图；无3D或真实连接时仅标课堂模拟，不伪造软件运行。', '',
        '### 复制第1框开始；以后每次只发当前一步', '',
        '**学员用法：** 无需一次读完所有提示。将当前框发给你使用的AI；做完后回“完成＋观察”，结果不符回“不符＋现象”，报错回“报错＋原文”，需要停下回“暂停”。自然语言也可以。不要一口气把六步当成自动执行授权。', '',
        '### 对话1｜建立本课上下文', '',
        block(f"请做我这节课的协作教练：{label}（兼容课号{ident}）《{row['title']}》。\n"
              f"我们逐步制作同一个「星光小庭院」，当前只解决：{data['before']}\n"
              f"目标：{data['after']}\n"
              f"必须掌握：{'；'.join(row['m']) if row['m'] else '无；本课仅理解用途'}。理解即可：{'；'.join(row['k'])}\n"
              f"停止线：{row['stop']}\n必须保持：{data['keep']}\n"
              '先读取我已提供的进度和材料，只问真正缺失的一项。需要软件操作时核对实际版本、当前截图或场景树、可访问的工具；不要求我发密钥或整个电脑。\n'
              '先给一个预测问题并等我回答，再给一个最小步骤。不跳课、不自动做整款游戏。能执行才说已执行，否则给明确操作单或脚本，并标未执行。\n'
              '后续每轮用四项回应：现在是哪一步；只改什么/怎样恢复；我应观察什么；目前还缺什么证据。没有证据不要替我勾通过。'), '',
        '**AI此时应做：** 确认当前场景与学习范围，不直接输出几十个文件。已经提供过的版本、素材和约束应复用，不重复问。', '',
        '### 对话2｜先理解一个因果关系', '',
        block(f"先问我：{row['questions'][0][1]}\n等我写预测和理由后，再指出一个证据缺口，只给一个提示，不先公布完整答案。用词不专业时先确认意思，再补术语。"), '',
        '**转入下一步：** 有自己的预测即可；预测错可以用实验纠正，不要求先背定义。', '']
    if k_only:
        lines += ['### 对话3｜K用途选择与结束', '',
            block(first + '\n' + second + '\n只核对我的用途解释，缺口用一个追问；不生成实现，不要求操作或长报告。最后给我一份认识记录，写明本项目不因为此课就增加联网。'), '',
            '**结束证据：** ' + gate,
            '**本课全K：** 不出现软件执行门槛、六步实操或M成绩。', '']
    else:
        lines += ['### 对话3｜AI只完成第一小步', '',
            block('沿用已确认的版本、材料和修改边界。现在只做：' + first + '\n先列影响对象和原值，再提供一个可撤销初稿。没有实际软件连接时给我可执行的局部操作单/脚本，不说已经修改。做完先停下。'), '',
            '**预计看到／拿到：** ' + gate,
            '**不是自动保证：** 这是验收目标，取决于实际模型、工具和输入；结果不同就走下方“不符”分支。', '',
            '### 对话4｜人观察与亲调，再继续第二小步', '',
            block('这是我刚才的实际结果：我会附一张当前图、短演示或必要日志，并用一句话描述差异。\n先检查是否满足：' + gate + '\n若满足，指导我先亲调下面表格的一项；我回报观察后才继续：' + second + '\n一次只动一项可见参数。方向接近就手调；结构有误才给局部修复，不能不断重生成整个场景。'), '',
            '|选中哪里与参数性质|这次亲自试什么|观察与停手依据|', '|---|---|---|']
        for entry, action, observe in data['tweaks']:
            lines.append(f'|{entry}|{action}|{observe}|')
        lines += ['',
            '**保存与恢复：** 先记录原值和实际对象。优先在安全副本试；运行中Remote Inspector的变化不要当成已保存的设计值，确认后将选定值写回本地场景/资源或配置并重新运行。菜单路径随版本核对，自定义变量不冒充内置属性。',
            '**采用哪种沟通：** 大方向偏了，用参考图圈出要借鉴的轮廓/色彩/光感，并指出不要照搬什么；单个视觉值接近了，先拖或输入数值；原因不明，固定条件做一次对照。参考图不是可自动反推所有参数的答案。', '',
            '### 对话5｜成功验收，或失败时只修一处', '',
            '**达到目标时发送：**', block('请只根据我提供的证据检查：\n' + '\n'.join('- ' + s for s in data['accept']) + '\n旧功能回归：' + data['regress'] + '\n缺少过程证据就标待验证；不得用一张截图证明走跳或一次性事件。不要新增需求或把所有候选题变成作业。'), '',
            '**结果不符或报错时发送：**', block('不符/报错：我会提供触发步骤、预期、实际现象和必要原始日志。\n保留：' + data['keep'] + '\n本课优先风险：' + data['risk'] + '\n先提出一个可推翻的假设和一个最小验证；不要同时改多个系统。若两次验证仍无进展，回到基线并列出缺失证据，不反复抽卡。不要删除测试、关闭需求或扩大权限来假装修好。'), '',
            '**AI评分边界：** 代码和初稿可以由AI提供；判断、亲调与证据解释由学员完成。得到根因提示记为有提示，不因此重复考试所有概念。', '',
            '### 对话6｜存进度，下一次接着做', '',
            block(f"请总结本课{label}（{ident}）的进度卡，不把预测当已完成。\n记录：真实软件版本/渲染器；当前场景与变更对象；选定参数和原值；我做的判断；实际证据；通过/待验证；使用过的提示；恢复方法；下一步唯一任务。\n只有实际验证才标通过，没有生成或真机执行就明确写模拟/待验证。给我一段可以复制到新AI对话的摘要，不假称你已持久保存。\n先核对下一课前置和我的已选路线，未完成就停在当前步骤，不催着扩范围。"), '',
            '**学员保存：** 把进度卡存本地或私人笔记；下次粘贴进度卡和下一课第1框。不要公开API Key、账户、本地私密路径或个人录像。', '']
    lines += ['### 当前风险与长期责任', '',
        '**本课风险检查：** ' + data['risk'],
        '这是需要在当前工具版本下核验的风险，不是所有AI必然失败的排行榜，也不预测何时改善。长期保留需求、参考选择、影响范围、结果认可与取舍责任；测量、批量设置和重复验证可以由AI协助。',
        '**不把学习变成额外六次考试：** 六个对话阶段共享本课原有M/K证据；只在薄弱关键能力上追加一处故障或变式。没有实际材料时先做课堂模拟，真机状态单独记录。', '']
    return '\n'.join(lines)

def standalone(row, data, display):
    text = dialogue_card(row, data, display)
    nxt = next_lesson(row['id'])
    footer = ('下一建议：[' + display[nxt] + '](../dialogues/' + nxt + '.md)。先检查前置；选修未选可以跳过。' if nxt else '已到本路线收束点：先验收、整理证据；高级专项按实际问题另选。')
    return f"# {display[row['id']]}｜跟AI一步步做：{row['title']}\n\n状态：对话脚本已编写，不代表课堂或软件已经执行。\n\n" + text + '\n' + footer + '\n'

def enrich_demo(output, by_id, order, scenarios, display):
    validate_coaching(by_id)
    for ident in order:
        output[f'curriculum/dialogues/{ident}.md'] = standalone(by_id[ident], scenarios[ident], display)
    prefix = '> v6：每课可直接使用的逐步AI对话见 [启动入口](START-HERE.md)。本轮完成课件/对话设计，不是新Demo已实现。\n\n'
    pages = runpy.run_path(str(AUTHOR / 'demo_pages.py'))['PAGES']
    output.update(pages)
    index = ['# 课程索引：学一课，借助AI推进一小步', '',
        '47个课件单元，每个都有学生稿、独立OpenMAIC输入和逐步AI对话。它们是同一课的三种用途，不是141堂课。原45课保留；新增I13小地图和I14世界美化；X02升级为可选轻战斗闭环。',
        '主题展示继续ABCDE；旧文件路径和题号稳定。B-11/B-12是新增扩展，不是要求入门时一起做。', '',
        '**默认路线：** 初级循环 → B-11小地图 → B-12世界美化 → 角色与复用/交付。详细美术C线和动作E-10/E-11按需插入。AI协作从第一课开始。',
        '**单课开始：** 点“跟AI继续”，只复制第1框。需要互动课堂时，把“OpenMAIC全文”整份交给生成器。无需先把整套资料读完。', '',
        '|展示号 / 稳定号|主题|前置|学生稿|OpenMAIC全文|跟AI继续|', '|---|---|---|---|---|---|']
    for ident in order:
        r = by_id[ident]
        deps = '、'.join(display[d] for d in r['prereq']) or '无'
        index.append(f"|{display[ident]} / {ident}|{r['title']}|{deps}|[阅读](lessons/{ident}.md)|[复制](../openmaic/lessons/{ident}.md)|[开始](dialogues/{ident}.md)|")
    index += ['', 'I08导航、X动作和A高级按需选择；未选不计入基础版验收。制作顺序先文本、再课堂验证、再软件配套；学员使用时每课交替理解与实践。',
        '[精致Demo验收](demo-quality.md) · [界面参数深度](interface-map.md) · [全部应用情境](application-map.md)', '']
    output['curriculum/lesson-index.md'] = '\n'.join(index)
    roadmap = ['# 路线v6：同一项目，逐步达到精致Demo', '',
        '先完成最小十星循环，再把庭院接成三段可探索小地图，统一美术、接入现成角色，最后交付。选择增强版时加入旁路训练角，不让战斗成为收集通关门槛。',
        'M是具体选择/操作/验收能力；K只认识用途。所有学习结束条件按当课证据，不按提示词或代码长度。', '',
        '[逐课入口与对话](lesson-index.md) · [最终质量目标](demo-quality.md) · [学习合同](learning-contract.md)', '']
    for ident in order:
        r = by_id[ident]
        roadmap += [f"## {display[ident]}｜{r['title']}（{ident}）", '',
            '**产出：** ' + r['goal'], '**M 必须掌握：** ' + ('；'.join(r['m']) or '无，本课全K'),
            '**K 理解即可：** ' + '；'.join(r['k']), '**停止线：** ' + r['stop'],
            '**第一小步：** ' + PLANS[ident][0], '**继续条件：** ' + PLANS[ident][1],
            f"[本课讲义](lessons/{ident}.md) · [逐步对话](dialogues/{ident}.md)", '']
    output['curriculum/roadmap.md'] = '\n'.join(roadmap)
    review = ['# v6逐课复核：一步一证据，不让AI一口气做完', '',
        '这是作者内容/结构复核，不是独立教学评审、真实软件执行或学习效果证明。47课都以原来的M/K要求核对首步、继续条件和后续一步；不用额外增加六次作业。', '',
        '|课号|首个可检查结果|下一个局部步骤|真实执行状态|', '|---|---|---|---|']
    for ident in order:
        review.append(f'|{display[ident]} / {ident}|{PLANS[ident][1]}|{PLANS[ident][2]}|新课堂/新配套未验证|')
    review += ['', '专项修订：扩图先路线；美化先一处样板；X02先动画恢复再判定，预览不当事件执行，已重叠目标和下一次攻击仍可命中；I12基础版与增强版分开。',
        '对话卡重用现有验收证据，失败时只做一个假设；进度摘要由学员保存，不承诺AI跨会话记忆。', '']
    output['curriculum/lesson-review.md'] = '\n'.join(review)
    output['AGENTS.md'] += '\n## v6每课连续对话与精致Demo\n\ndemo_extension.py是扩图、美化、X02和I12的作者修订源；conversation_plans.py保存每课首步、继续条件、后续一步和概念图。tools/demo_coach.py把它们加入同一份学生稿/教师稿并生成dialogues。修改源后重新构建，不单独修改生成MD。47课三份用途不是141课。新项目成果仍需逐课运行和学习证据。\n'
    output['curriculum/project-spine.md'] = '# 项目主线统一入口\n\n最新的核心版/增强版、三段地图、世界美化与训练角边界见 [精致Demo质量表](demo-quality.md)。逐课落点见 [应用地图](application-map.md)，操作从 [逐步对话](lesson-index.md) 开始。\n\n原项目主线详表保留在Git历史。本次是文本规划升级，不是扩大后的游戏已经实现。\n'
    output['openmaic/project-integration-template.md'] = '# 逐课集成已回填，不再让学员拼模板\n\n每课的完整输入见 [课程索引](../curriculum/lesson-index.md)，第2A节为逐步AI对话，第8节为实际应用验收。它们由同一作者源生成；无需把本文件再拼进课程要求。\n\n编写时填：具体问题、局部交付、继续证据、第二小步、可恢复微调、失败分支和接续摘要。K认识课不强制软件执行，模型无连接时只给操作单，不冒充运行。\n'
    return output
