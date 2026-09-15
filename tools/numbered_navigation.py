"""Build learner navigation from canonical IDs, without a second display namespace.
No model, browser, engine, image or learner execution is performed here.
"""
from __future__ import annotations
import re
from course_order import GROUPS, ORDER, GROUP_RESULTS, route_label

DATE = '2026-09-15'


def _clean(text):
    text = re.sub(r'^> 兼容课号：[^\n]*\n\n', '', text, flags=re.M)
    text = re.sub(r'（兼容课号[A-E]\d{2}）', '', text)
    text = re.sub(r'\b([A-E]\d{2})（\1）', r'\1', text)
    text = re.sub(r'\b([A-E]\d{2}) / \1\b', r'\1', text)
    return text


def finalize_navigation(output, by_id, order, scenarios):
    if list(order) != ORDER or set(by_id) != set(ORDER):
        raise ValueError('The generator must use the single sequential course registry')
    for ident in ORDER:
        for folder in ('curriculum/lessons', 'openmaic/lessons', 'curriculum/dialogues'):
            key = f'{folder}/{ident}.md'
            text = _clean(output[key])
            text = re.sub(r'^版本：[^\n]*$', '版本：统一课号课程版｜2026-09-15', text, flags=re.M)
            headline = re.search(r'^# ([A-E]\d{2})[｜\s]', text, re.M)
            if not headline or headline[1] != ident:
                raise ValueError(f'{key}: title does not match the canonical filename')
            metadata = f'**学习分组：** {ident[0]}组；**本课编号：** {ident}；**路线：** {route_label(ident)}。'
            start = '## 0. 开始前：只准备本课需要的东西'
            text = text.replace(start, metadata + '\n\n' + start, 1)
            output[key] = text

    table = ['# 课程索引：文件名、课内编号和学习顺序一致', '',
        '共47课。A、B、C、D、E只是按学习先后排列的分组编号，不是软件名或英文词首字母。A组从零开始。每课使用同一个编号：文件名、标题、前置、题号和对话启动卡一致。', '',
        '**首次学习：从A01开始，再到A02、A03。** 按表向下学；遇到选修可以跳过，不把字母更靠后当作必须精通的证明。',
        '**三份材料是同一课的三种用途：** 学生稿供阅读；OpenMAIC全文供生成课堂；跟AI继续供实际操作。47份输入不等于47堂课堂已生成或试教通过。', '',
        '**基本路线：** A01–A08 → B01–B13 → C01–C12 → D01–D04 → D07。D01–D04是本项目的美术生产主线；D05–D06动作增强、E组专项按需选修。', '',
        '|课号|课程|前置|路线|学生稿|OpenMAIC全文|跟AI继续|', '|---|---|---|---|---|---|---|']
    for ident in ORDER:
        row = by_id[ident]
        deps = '、'.join(row['prereq']) or '无'
        table.append(f'|{ident}|{row["title"]}|{deps}|{route_label(ident)}|[阅读](lessons/{ident}.md)|[复制全文](../openmaic/lessons/{ident}.md)|[开始](dialogues/{ident}.md)|')
    table += ['', '## 使用时只打开当前一课', '',
        '生成互动课：复制对应OpenMAIC文件全文，不先把全部47课一起提交。软件实操：复制“跟AI继续”的对话1，带上自己的必要材料与进度；之后回报完成、不符、报错或暂停。',
        'M为本课必须掌握的限定能力，K只需理解用途。借助AI实现不等于放弃判断；同一个小项目中的操作、解释、回归可共同取证，不重复叠加作业。', '',
        '[预览与保存](preview-and-save.md) · [学习深度](learning-contract.md) · [真实交付进度](delivery-status.md) · [下一步完善](../docs/improvements.md)',
        '[旧进度或旧链接的迁移说明](../docs/numbering-migration.md)', '']
    output['curriculum/lesson-index.md'] = '\n'.join(table)

    groups = ['# 学习分组：ABCDE仅表示先后', '',
        '不再有“文件号”和“展示号”两套号码。统一格式为A01、A02、B01，不使用A-01，也不按Godot/Blender/AI拆开编号。各工具围绕同一个游戏交叉使用。', '',
        '|分组|课号|课数|这一段的阶段成果|', '|---|---|---|---|']
    for letter, _label, ids in GROUPS:
        groups.append(f'|{letter}|{ids[0]}–{ids[-1]}|{len(ids)}|{GROUP_RESULTS[letter]}|')
    groups += ['', 'A、B、C按学习路径推进；D01–D04继续主线的套装二开与风格统一，D05–D06动作增强按需，D07收束；E组各专题按需要和前置选择。',
        '课号如C01指一节课；技术概念使用KN01–KN32，艺术词使用ART编号。概念标识用于作者核对覆盖，学员不需要背编号。', '',
        '[逐课索引](lesson-index.md) · [完整大纲](roadmap.md)', '']
    output['curriculum/series-guide.md'] = '\n'.join(groups)

    roadmap = ['# 课程大纲：按编号逐步做成一个精致Demo', '',
        'A最基础；字母只作先后分组。先做同一庭院中的十星循环，再扩成庭院—林路—观景台的小关卡。精修与动作按已选目标加入；不扩成开放世界或复杂战斗系统。', '',
        '每课顺序是：必要概念 → 一个交互对照 → 有边界的AI初稿 → 人作选择或微调 → 相关项目验收。下面的M/K是学习要求，不是说真机任务已经执行。', '']
    for letter, label, ids in GROUPS:
        roadmap += [f'## {label}', '', GROUP_RESULTS[letter], '',
            '|课号与任务|必须掌握M|理解即可K|当前不深入|', '|---|---|---|---|']
        for ident in ids:
            r = by_id[ident]
            m = '；'.join(r['m']) or '无，全K认识课'
            roadmap.append(f'|[{ident} {r["title"]}](lessons/{ident}.md)（{route_label(ident)}）|{m}|{"；".join(r["k"])}|{r["stop"]}|')
    roadmap += ['', '## 完成不是看完所有文件', '',
        '基础版完成以D07验收约定为准。没有选动作增强版就不考D06；没有性能或特殊效果需求，不必进入E组。只查菜单、用AI写代码不扣独立判断分；已被提示本题根因则如实记录，再用新变式检查。',
        '[课程入口](lesson-index.md) · [Demo质量标准](demo-quality.md) · [实操证据](../assessments/application-evidence.md)', '']
    output['curriculum/roadmap.md'] = '\n'.join(roadmap)

    app = ['# 逐课应用地图', '',
        '每项必学能力都有同一项目中的应用位置。这里是设计与取证要求，不是运行结果。K可以只作用途决定；选修没有实际收益就不接入。', '',
        '|课号|遇到的实际问题|本课应有的变化|路线|', '|---|---|---|---|']
    for ident in ORDER:
        d = scenarios[ident]
        app.append(f'|[{ident}](lessons/{ident}.md)|{d["place"].replace("｜", "：")}：{d["before"]}|{d["after"]}|{route_label(ident)}|')
    app += ['', '只检查已学且实际存在的功能，不提前要求尚未制作的拾取、存档或战斗。模拟完成、软件执行、工程验收和学员迁移分别记录。',
        '[最小证据单](../assessments/application-evidence.md) · [AI职责与把关](../assessments/ai-collaboration.md)', '']
    output['curriculum/application-map.md'] = '\n'.join(app)

    output['START-HERE.md'] = '''# 从A01开始：学一课，和AI推进一个小步骤

**[打开47课索引](curriculum/lesson-index.md)**。按A01、A02……往下学。ABCDE仅是先后分组；标题、文件名和课内引用使用同一个课号。

第一次建议打开 **[A01 跟AI开始](curriculum/dialogues/A01.md)**。它从风格目标和可观察描述入手，不要求已有模型、编程基础或完整游戏。已有明确目标也可先读 **[A02 空间入门](curriculum/lessons/A02.md)**。

|今天要做什么|打开哪份|怎么用|
|---|---|---|
|生成互动概念课|索引的OpenMAIC全文|复制这一课全文，一次只生成一课|
|让AI陪你做|索引的跟AI继续|只复制对话1，提供必要材料，然后回报观察|
|自己复习|索引的学生稿|看M/K、概念图和当前实操，不先看教师答案|

“完成：我看见……”让AI检查后推进；“不符/报错：实际现象……”进入局部验证；“暂停”生成进度卡，由自己保存。缺软件连接就给操作单，不宣称已经修改电脑；缺场景时先做明示模拟，不判工程通过。

**主线路线：** A → B → C → D01–D04 → D07。D01–D04是套装二开与风格统一主线；D05–D06动作增强、E组专项按需选择。完成当前任务与相关证据比看完47课更重要。

[第一次如何准备](curriculum/first-session.md) · [预览、亲调与保存](curriculum/preview-and-save.md) · [哪些已交付](curriculum/delivery-status.md) · [待完善](docs/improvements.md)
'''
    output['README.md'] = '''# AI时代3D游戏学习

把必要概念、审美判断和AI协作应用到同一个逐步成长的小游戏：从方块庭院到可探索的卡通小关卡，再按需加入一段攻击与训练木桩。

## 学习入口

**[从A01开始](START-HERE.md)** · **[全部47课](curriculum/lesson-index.md)** · **[全部OpenMAIC输入](openmaic/lessons)**

ABCDE是按学习顺序的分组编号，不代表某款软件。A组最基础。每课的文件名、标题、题号和引用一致，例如`openmaic/lessons/A01.md`内的课号就是`A01`。

每课有学生稿、OpenMAIC生成输入和可直接对话推进的协作卡。M必须掌握具体选择与验收，K知道用途即可；AI可以承担实现，人负责目标、取舍和证据判断。不是提示词抽卡，也不是软件百科。

## 当前交付范围

47课的文本与生成规格已经编写并做内容一致性检查；这不等于47堂互动课堂已生成，更不等于逐课真机应用已通过。已有参考工程保留；新地图、整图美术和训练角仍需单独制作和验证。

[课程大纲](curriculum/roadmap.md) · [Demo目标](curriculum/demo-quality.md) · [交付状态](curriculum/delivery-status.md) · [下一步完善](docs/improvements.md)

[AI协作要领](assessments/ai-collaboration.md) · [打印要点](print/必须牢记.md) · [打印AI随手卡](print/ai-control-card.md) · [上游OpenMAIC Skill](openmaic/upstream-reference.md)

旧书签与进度可能使用旧号；请用[迁移说明](docs/numbering-migration.md)核对标题，不凭旧文件名猜课。
'''
    output['openmaic/README.md'] = '''# OpenMAIC课程输入

`lessons/`内的47份Markdown是全部独立课程的教师生成输入，不是已经生成的课堂文件。文件名与课内编号一致：A01.md对应A01，B01.md对应B01。

从[统一索引](../curriculum/lesson-index.md)选择一课，复制全文作为课程要求。需要软件实践时改用同课的“跟AI继续”，不要让学员在教师答案区中做独立测验。

课堂应先给目标和一个可操作对照，协作提示词按需展开，不把所有作者规则朗读成幻灯片。检查控件、复位、答案时机与缺材料分支后，才记录该课堂通过。

[固定上游Skill与许可证](upstream-reference.md) · [生成与审查约束](review-contract.md) · [试教协议](pilot-protocol.md)
'''
    output['curriculum/delivery-status.md'] = '''# 交付状态：编号统一不等于课堂已验证

记录日期：2026-09-15。唯一交付分支main。

|内容|已经具备|仍待完成|
|---|---|---|
|47课编号|文件、标题、前置、题号、对话与索引统一；A组从零开始|后续改号必须再次运行一致性检查|
|课程正文与AI引导|47份学生稿、47份教师输入、47份对话卡；M/K和项目证据对应|新版本逐课课堂生成与真人试学|
|OpenMAIC输入|每课可独立复制，上游Skill固定保存|控件运行、复位、答案时机、图像和真实学习效果|
|已有参考工程|原有空间、材质、场景练习及十星参考解保留|视觉手感与逐课起始包覆盖；已有文件不代表全部课都可直接实操|
|扩图与美化|C01、C02完整教学与验收设计|三段新地图工程、统一美术素材和真实截图|
|动作增强|D05、D06资源选择与单次攻击闭环设计|许可清楚的动作、适配、命中和恢复的实际运行|
|最终Demo|D07区分基础版与已选增强版的质量标准|扩展后完整可玩包、目标设备运行与人工验收|

四项状态分开：课件文本 → 课堂控件 → 软件应用 → 学员迁移。结构测试只检查本次覆盖的结构，不替代后三项。旧版本的课堂好评不能自动算当前47课已验证。

[课程索引](lesson-index.md) · [接下来完善](../docs/improvements.md) · [实际试教协议](../openmaic/pilot-protocol.md)
'''
    output['docs/improvements.md'] = '''# 接下来值得完善的地方

按学习收益排序，不再增加一批大纲或术语。编号与链接统一是基础，不能代替内容或实践验证。

## 1. 先把不同类型的代表课实际生成一次

使用A03节点、B04材质、B06拾取、C02世界美化作为不同类型样本；已选动作增强时再测D06。重点观察控件是否真改变条件、复位是否完整、答案是否提前泄露，以及对话1能否独立继续。按[试教协议](../openmaic/pilot-protocol.md)记录第一处真实卡点。

**当前状态：待真实执行。** 不以Markdown检查通过代替OpenMAIC生成或课堂可用性。

## 2. 把最小起点与整个Demo的阶段版本对齐

每课写明继承上课什么、这课只改什么、下课留下什么。制作配套时先覆盖A组和B组最小场景，再扩图和美化；保留完成参考但不要求学生一开始阅读整个工程。重点区分能运行的完整参考解与适合该课的新手起点。

**当前状态：说明已有，逐课起始包未齐。** 用户原先约定先课件、后素材与工程，此次未扩写运行实现。

## 3. 用真正的视觉对照补强美术判断

优先准备同机位、同条件的灰盒/AI初稿/人工微调后对照，以及玩家距离的轮廓、材质和目标可读性。过程图、真实截图、原创概念示意必须分别标注；外部作品展示要有合适许可。

**当前状态：已有概念结构示意，完整视觉对照未齐。** 不把结构图当美术成品，不把参考网址当图片授权。

## 4. 精简学员真正需要读的部分

保留给OpenMAIC的完整规格，但课堂先呈现本课目标、两项M、一个对照和当前一步；安全与教师评分说明按需展开。试教后再依据实际负担调整，而不是继续把所有规则叠在第一页。

## 5. 关键能力用换情境验收，而不是继续增加选择题

已有[迁移任务](../assessments/transfer-stations.md)替代对应复测。分别看人有没有作判断、AI有没有越界、工程有没有证据；允许保留原方案或判断证据不足。题目的区分力、负担和隔次掌握仍需试学，不称课程已完美。

[课程入口](../curriculum/lesson-index.md) · [Demo质量终点](../curriculum/demo-quality.md) · [交付状态](../curriculum/delivery-status.md)
'''
    output['AGENTS.md'] = '''# AI协作与课程维护约定

唯一交付分支main。当前先完善课件并验证代表课堂，再补参考素材与Godot/Blender配套。没有明确切换阶段，不扩写game/、blender/、web/运行实现，不调用收费生成或索取密钥。

## 唯一编号

课程唯一编号由tools/course_order.py定义：A01–A08、B01–B13、C01–C12、D01–D07、E01–E07，共47课。ABCDE只是顺序分组，A最基础，不按软件含义归组。文件名、课内标题、前置、练习题号、对话启动框及索引必须一致。不再使用另一套展示号或兼容课号。

作者源中的LESSONS、SCENARIOS、PLANS、REVIEWS和准备材料索引也使用同一课号，不保留一套隐藏旧课程ID。技术概念为KN01–KN32，艺术词用ART；不与C组课号混淆。旧版本映射只保留在docs/numbering-migration.md。

## 内容与生成

curriculum/authoring/维护逐课正文、应用、对话、审核与准备材料；tools/build_course_materials.py生成学生稿、OpenMAIC全文和对话卡。先改源，再构建；不能只改生成MD。tools/numbered_navigation.py负责统一入口，不更改学习内容或评分。

M/K描述限定能力，不把整个学科升级必修。API、菜单、快捷键可查；常用可见参数适合亲调但不以机械拖滑杆证明掌握。学生稿不得包含教师答案。没有过程证据，不将模拟或文字解释标成软件应用通过。

起始材料缺失时明确分支，不让学员临时重建大工程。第一条提示必须自带首步、继续条件、下一步和结束证据；AI根据实际材料说明建议、执行、验证三个状态，不能假称已读电脑或保存进度。

## 校验

运行python3 tools/build_course_materials.py --check、python3 tools/check_course_numbering.py和python3 tools/validate_repo.py。现有质量/准备/对话检查保留；结构检查不证明课堂、视觉或学习效果。运行代码另按实际固定版本验证，区分历史结果与新结果。

openmaic/vendor是固定上游参考，保留原字节、许可证和摘要，不自动执行。参考链接、临摹、公开分发的条件分别核对；密钥、个人日志和未授权原作不进入公开仓库。
'''
    for name, value in list(output.items()):
        if name.endswith('.md'):
            output[name] = _clean(value)
    return output
