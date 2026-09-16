"""Final authoring layer: novice loop, honest Lab bindings, memory and evidence IDs."""
from __future__ import annotations
import json
import posixpath
import re
import runpy
from pathlib import Path

AUTHOR = Path(__file__).resolve().parent
ROOT = AUTHOR.parents[1]
SPACE = 'game/scenes/lab.tscn'
COLLISION = 'game/labs/collision_roles_lab.tscn'
MOTION = 'game/labs/motion_lab.tscn'
VISUAL = 'game/scenes/visual_lab.tscn'
MATERIAL = 'game/labs/material_lab.tscn'
ORIGIN = 'blender/labs/transform_origin_lab.blend'
KIT = 'blender/labs/kitbash_style_lab.blend'
MAIN = 'game/scenes/main.tscn'
# paths, first observation, coverage limitation, production step. Never implies whole-lesson coverage.
BINDINGS = {
'A01': ([], '从自己提供的参考中选一个可见特征，说出借鉴与不借鉴什么。', '参考分析，无软件Lab门槛；没有图不捏造作品内容。', 'P0'),
'A02': ([SPACE], '固定父空间，只改对象Position的一个轴，再恢复。', '空间子实验；不一次操作所有模式。', 'P1'),
'A03': ([MAIN], '先只观察参考场景树，指出整体与外观子节点；另建小副本再改。', '完整参考不是隔离起始工程，不阅读后半程答案来完成检查。', 'P1'),
'A04': ([COLLISION], '把目标移到墙另一侧；比较只隐藏墙外观和只禁用阻挡，再恢复。', '开关Lab先覆盖职责；Layer/Mask与排除装饰球需Inspector及对照对象，不能由M1替M2。', 'P1/P2'),
'A05': ([MOTION], '只改Speed，按同一跑动按钮，比较相同时间的距离。', '简化运动实验，不等同于完整CharacterBody控制器验收。', 'P2'),
'A06': ([MOTION], '固定Gravity，改变Jump velocity，比较腾空与落地，再重播。', '重播位置不等于参数恢复；需要基线时重开场景。', 'P2'),
'A07': ([SPACE, ORIGIN], '任选门轴实验，闭门位置相同，再分别观察中心/侧边旋转。', 'Godot与Blender坐标轴不同，按文件实际轴观察，不背同一个轴名。', 'P1'),
'A08': ([VISUAL], '固定相机位置，只改FOV，解释看见范围与物体屏幕大小。', '现有Lab只有透视FOV；正交Size与事件镜头不冒充已经配套。', 'P1'),
'B01': ([KIT], '固定视图先比较Base与Variant大形，不先画纹理。', '小屋比例示例，不是商业品质标杆。', 'P4/P6'),
'B02': ([ORIGIN], '选一个静态对象检查Dimensions、Scale与Origin；先保存副本。', '静态门轴/缩放样本，不包含绑定角色修复。', 'P4'),
'B03': ([KIT], '固定机位光照，只调整变体一处颜色，先看焦点和大色块。', '原生材质参数练习，不自带自动色彩评分器。', 'P4/P8'),
'B04': ([MATERIAL], '只改左球Roughness，对照右球，保持灯光不动。', '现有两球使用独立材质；共享实验需另建共享样本，不能声称本Lab已覆盖共享M。', 'P4/P6'),
'B05': ([KIT, MAIN], '在副本中选一个静态部件导出，再接到自己的游戏视觉包装。', '给出源样本与参考工程；学员GLB往返、原点与功能保持仍须实际做。', 'P4/P7'),
'B06': ([MAIN], '先预测重复请求的结果，再在自己的副本检查一次性收集。', '这是完整参考；时序故障需隔离副本，不用读实现代替自己判断。', 'P2'),
'B07': ([MAIN], '观察一次收集后的状态与可见反馈，区分成功规则与表现。', '基础反馈参考，不包含完整打击感效果库。', 'P2/P9'),
'B08': ([MAIN], '完整收集后重开，再拾取第一颗，看实际计数而不只看标题。', '布局/窗口变化和重开要分别验，不用一张图证明。', 'P2/P3'),
'B09': ([VISUAL], '固定FOV，只改主光强度，对照亮面、暗部和目标。', '光强样例，不包含所有环境光/阴影配置。', 'P4/P9'),
'B10': ([VISUAL], '将一条参考规则用于同机位对照，解释为什么不继续加细节。', '参考来源由学员提供；Lab是原创示意，不是假大师截图。', 'P4/P8'),
'B11': ([MAIN], '记录实际设备/分辨率/路线，再测一次基线，不先盲目优化。', '不自带已验证性能收益；结果来自你的设备。', 'P2/P11'),
'B12': ([MAIN], '在副本中检查一个局部改动及恢复点，先提出可验证假设。', '源码和自动测试仅提供部分证据，不证明学员判断。', 'P3'),
'B13': ([MAIN], '沿本课任务换一种可用物品，先写允许改与必须保留项。', '完整参考用于比较；检查使用自己的快照和未揭示变式。', 'P3'),
'C01': ([MAIN], '先画主路与返回路径，用代理块在副本扩一个区域。', '当前主场景不是已完成的庭院/林路/观景台三段地图。', 'P1/P7'),
'C02': ([VISUAL], '只切换Clutter，指出焦点、路径和留白变化。', '密度样例；不包含全套视差/背景层实现。', 'P4/P8'),
'C03': ([], '先列已选角色的尺寸、骨架、动作与许可条件，再试一个片段。', '无预置正式角色包；没有资源时先做选择任务，接入待验证。', 'P4/P10'),
'C04': ([], '用已有兼容角色先比较待机与走路，不同时加所有动作。', '无完整动画融合样例；需先满足C03入场条件。', 'P10'),
'C05': ([KIT], '观察两件部件的数据/材质引用，先决定共享或独立。', '静态样例；动画资源共享另在实际角色副本验证。', 'P6/P7'),
'C06': ([SPACE], '先观察门轴，再把相同职责用于自己的门包装。', '门轴有样例，移动平台承载/速度尚无完整配套。', 'P2/P7'),
'C07': ([KIT], '先测模块尺寸与连接位置，再检查实际使用的纹理。', '本文件不提供完整棋盘格UV实验，UV部分需另备样本。', 'P6'),
'C08': ([VISUAL], '先对照主光基线，再按设备与渲染器选择一个效果。', 'Fog/Glow/DOF等不在现有Lab中，不能把目录当已实现控件。', 'P4/P9'),
'C09': ([MAIN], '对同一构建/机位选择一项真实测量，不改多种设置。', '基准由目标设备提供，headless不代表GPU画面性能。', 'P7/P11'),
'C10': ([COLLISION], '先说明检测与允许交互的区别，再准备自己的交互对象。', '这里只提供检测对照，非完整提示/条件/结果系统。', 'P2/P7'),
'C11': ([], '先列应恢复的状态和可接受的异常处理，再准备最小存取副本。', '主项目重开不是存档系统；无完整存档实验。', 'P2/P11'),
'C12': ([MAIN], '核对目标平台和当前导出条件，再生成自己的可运行包。', '有项目源码不等于已给出跨平台成品包。', 'P11'),
'D01': ([KIT], '先另存副本，选Variant_Roof只改一项比例，比较Base。', '原创几何二开样例，不是已购买的完整资产套装。', 'P6'),
'D02': ([KIT, MATERIAL], '固定光照，先统一一件变体色彩，再单独调粗糙度。', '支持局部材质观察，不等于整库风格已经统一。', 'P6/P8'),
'D03': ([KIT], '为一件变体记录源、用途、版本、引用和预览机位。', '样例不自带完整商业资产库，按本地实际资源建立。', 'P5/P7'),
'D04': ([KIT, MAIN], '挑一个小区域组合已合格部件，固定机位做减法。', '当前文件只是起点，不是已验收美术结业作品。', 'P8'),
'D05': ([], '锁定一个角色和一段许可合适的动作，先测兼容。', '无预置动作包，不能把静态模型当重定向已成功。', 'P4/P10'),
'D06': ([], '先完成一段攻击和恢复移动，再加一次有效命中规则。', '无完整木桩/动作工程；未选增强路线无需做。', 'P10'),
'D07': ([MAIN], '按已选范围检查自己的完整构建和真实试玩，不增新玩法。', '现有参考不代表精致三段地图已完成。', 'P11'),
'E01': ([], '有真实寻路需要时，先分清可画路径与角色能通过。', '导航选修无专用Lab，不阻塞基础版。', '按需专项'),
'E02': ([MAIN], '先固定实际设备与构建，定义要解决的一个性能问题。', '参考场景不是通用性能测试集。', 'P11'),
'E03': ([], '有明确视觉缺口时准备隔离样例和可关闭的单效果。', 'Shader专项无预置完整效果库。', 'P9'),
'E04': ([SPACE], '先用现有门轴说明预期轨迹，再定义复杂旋转问题。', '基础Lab不能代替复杂旋转专项验证。', '按需专项'),
'E05': ([], '先以测量确认批量/加载问题，再选择专项，不先扩大地图。', '大场景无完整样例，基础项目无需强做。', '按需专项'),
'E06': ([], '只解释联网增加了哪类协调问题，以及本项目是否需要。', '全K，只理解用途，不要求实操或背诵。', '不加入单机生产门槛'),
'E07': ([], '选一个真实专项问题，整理已测、未测和采用理由。', '用自己的专项证据，不凭目录存在宣布通过。', '按需专项'),
}


def link(path: str, from_path: str) -> str:
    return posixpath.relpath(path, posixpath.dirname(from_path))


def binding_text(ident: str) -> str:
    paths, first, limit, production = BINDINGS[ident]
    resources = '、'.join(paths) if paths else '没有专用软件Lab；使用本课明确的材料分支'
    return f'概念配套：{resources}\n练习首步：{first}\n覆盖边界：{limit}\n对应生产阶段：{production}；达到当前阶段才迁移，不把实验完成当成项目通过。'


def enrich_pathway(output: dict, by_id: dict, order: list) -> dict:
    if set(BINDINGS) != set(order):
        raise ValueError('Every canonical lesson needs a deliberate Lab binding')
    for ident, (paths, *_rest) in BINDINGS.items():
        for path in paths:
            if '..' in Path(path).parts or not (ROOT/path).is_file():
                raise ValueError(f'{ident}: Lab/reference missing: {path}')
    output.update(runpy.run_path(str(AUTHOR/'novice_pages.py'))['PAGES'])
    for ident in order:
        row = by_id[ident]
        paths, first, limit, production = BINDINGS[ident]
        for folder in ('curriculum/lessons', 'openmaic/lessons', 'curriculum/dialogues'):
            key = f'{folder}/{ident}.md'
            text = output[key]
            resources = '、'.join(f'[{Path(p).name}]({link(p,key)})' for p in paths) or '没有专用软件Lab；先按本课材料分支做认识/模拟，不虚构文件。'
            intro = ('## 0A. 这课怎样学、怎样查缺口\n\n'
                     '**学习顺序：** 短示范或预测 → 课堂随练 → 软件概念对照 → 自己解释 → 只补薄弱项。\n\n'
                     f'**实际配套：** {resources}\n\n**练习首步：** {first}\n\n**配套局限：** {limit}\n\n'
                     f'**正式项目落点：** {production}。实验只为理解；进入相应生产阶段再迁移。\n\n'
                     f'**回忆与检查：** [本课记忆规则]({link("print/memory-by-lesson.md",key)}#{ident.lower()}) · '
                     f'[单元检查]({link("assessments/unit-checkpoints.md",key)}) · '
                     f'[AI追问与弱项诊断]({link("assessments/ai-diagnostic-review.md",key)})。\n\n'
                     '**记录分开：** 回忆/解释/软件应用/换情境；没有证据写待验证。菜单/API可查；得到根因提示记有提示。\n\n')
            if not row['m']:
                intro = intro.replace('短示范或预测 → 课堂随练 → 软件概念对照 → 自己解释 → 只补薄弱项。',
                                      '本课全K：只做用途认识；不要求实操，不考反复记忆或迁移。')
            anchor = '## 1. 本课任务卡' if '## 1. 本课任务卡' in text else '## 2A. 场景、概念图与逐步AI对话'
            if anchor not in text:
                raise ValueError(key + ': missing insertion anchor')
            text = text.replace(anchor, intro + anchor, 1)
            text = re.sub(r'\*\*当前配套：\*\*[^\n]*', '**当前配套：** 见0A的真实文件、首步与覆盖边界；文件存在不表示本课所有M已有完整配套。', text, count=1)
            prompt_anchor = '先读取我已提供的进度和材料'
            if prompt_anchor not in text:
                raise ValueError(key + ': first prompt missing')
            launch = binding_text(ident) + '\n先复用上述现有样本，不重新生成同一个Lab。练习可提示；检查先只读快照，不一边改答案一边评分。\n'
            text = text.replace(prompt_anchor, launch + prompt_anchor, 1)
            text = text.replace('## 7. 后续真机任务（配套待做，不作为当前课堂依赖）', '## 7. 正式项目迁移（达到相应阶段再做）')
            text = text.replace('以下是后续真机操作的对应范围，不要求本轮打开软件。', '以下是软件操作的对应范围；优先使用0A已给出的实验，尚无配套的部分如实标待验证。')
            text = text.replace('按用户安排，当前先完成全部课件，之后再统一补素材、Godot/Blender起始与参考工程。',
                                '已有Lab先随课使用；完整生产按任务单推进，未交付的逐课配套不冒充完成。')
            if folder == 'openmaic/lessons':
                text = ('> 新手教学循环：先用一个现象和控件随练，再转0A指定软件样例；根据结果渐撤提示。AI诊断先引用证据并追问，不能直接代做后判掌握。下面的维护规则和提示词不逐字朗读成课。\n\n' + text)
            output[key] = text
    memory = ['# 逐课记忆索引：只复习当前已经学过的部分', '',
              '与47课作者源同步。优先随手卡见[核心卡](essential-memory.md)；这不是要求背完47课。每课先遮住规则，回答自测；K只认识用途。', '']
    objectives = {}
    for ident in order:
        row = by_id[ident]
        memory += [f'<a id="{ident.lower()}"></a>', f'## {ident}｜{row["title"]}', '',
                   ('可选认识：不反复背诵。' if not row['m'] else '必须掌握的限定能力：'),
                   '\n'.join('- '+x for x in row['m']) or '本课无M。',
                   '', '必记/用途提示：', '\n'.join('- '+x for x in row['remember']), '',
                   '**遮住上面后自问：** '+row['questions'][0][1],
                   f'**不会时：** 回[{ident}学生稿](../curriculum/lessons/{ident}.md)，只做相应对照；不要背教师答案。', '']
        for level, rows in (('M', row['m']), ('K', row['k'])):
            for i, objective in enumerate(rows, 1):
                objectives[f'{ident}.{level}{i}'] = {'lesson': ident, 'level': level, 'text': objective}
    output['print/memory-by-lesson.md'] = '\n'.join(memory)
    output['assessments/learning-objectives.json'] = json.dumps({'schema_version':1, 'objectives': objectives}, ensure_ascii=False, indent=2)+'\n'
    output['curriculum/lab-bindings.json'] = json.dumps({'schema_version':1, 'bindings':{
        ident: {'paths': v[0], 'first': v[1], 'limits': v[2], 'production': v[3]} for ident,v in BINDINGS.items()}}, ensure_ascii=False, indent=2)+'\n'
    sample_obs = {axis: {'score':None, 'support':'L0', 'evidence_ids':[]} for axis in ('recall','reasoning','application','transfer')}
    sample_obs['reasoning'] = {'score': 0, 'support': 'L0', 'evidence_ids': ['answer-1']}
    sample = {'schema_version':1, 'notice':'教学构造示例，不是真人测评；未实际调用AI或软件。',
              'target_objectives':['A04.M1','A04.M2'], 'items':[{'objective':'A04.M1','observations':sample_obs,
              'evidence':[{'id':'answer-1','kind':'answer','reference':'本文件构造答复1','summary':'“隐藏墙之后肯定能穿过，因为墙已经没了。”'}],
              'diagnosis':{'status':'hypothesis','basis':'答复可能把外观与阻挡混淆；软件行为尚未观察，不能判应用失败。',
              'next_question':'这次改的是哪个对象的哪个属性？其他形状的状态是什么？',
              'next_task':'在collision_roles_lab中只隐藏外观并观察，再单独禁用形状；先预测，不直接改正式地图。',
              'recheck':'下次会话改用不可见边界检查；若已提示根因，保留L2，不立即判独立2分。'}}]}
    output['assessments/learning-report.example.json'] = json.dumps(sample, ensure_ascii=False, indent=2)+'\n'
    for key in ('START-HERE.md','README.md'):
        if key in output:
            output[key] = ('> **第一次学习：** [三段学习路径](curriculum/learning-journey.md) → '
                           '[核心记忆卡](print/essential-memory.md) → [单元/阶段检查](assessments/unit-checkpoints.md)。'
                           'A/B基础后即可按[生产任务单](curriculum/production-work-orders.md)开发；C/D按需继续，不等47课全学完。\n\n' + output[key])
    key = 'curriculum/lesson-index.md'
    output[key] = output[key].replace('**基本路线：**', '**完整内容路线（不是进入实战的前置门槛）：**', 1)
    output[key] = ('> [新手三段路径](learning-journey.md)：课堂随练＋概念Lab；[记忆](../print/essential-memory.md)与[诊断](../assessments/unit-checkpoints.md)；'
                   'A/B基础通过后按[生产任务单](production-work-orders.md)干活。每课0A和对话1已列真实文件及局限。\n\n' + output[key])
    output['AGENTS.md'] += ('\n## 新手学习与诊断\n\nnovice_learning.py/novice_pages.py是单课Lab绑定、记忆索引和学习路径的作者源。'
        '概念Lab、提交快照检查、真实生产三种模式不能混用。检测先只读，不替学员改好再判会；缺证据为待验证，K不升级。'
        '早做导出/性能/角色兼容小试，最后做完整验收；不把全部47课变为进入项目的门槛。'
        '个人学习记录放.learning/或仓库外；learning_review.py只校验整理，不是自动判卷模型。\n')
    output['openmaic/lesson-template.md'] += '\n## 新手回路\n\n另见[课堂回路规范](learning-loop-contract.md)：文件/首步/局限进入单课0A与第1提示框，随练、软件、回忆、诊断、生产迁移分清；不把缺素材当不会。\n'
    return output
