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
BINDINGS = {'A01': ([], '从自己提供的参考中选一个可见特征，说出借鉴与不借鉴什么。', '参考分析，无软件Lab门槛；没有图不捏造作品内容。', 'P0'),
 'A02': (['game/scenes/lab.tscn'], '固定父空间，只改对象Position的一个轴，再恢复。', '空间子实验；不一次操作所有模式。', 'P1'),
 'A03': (['game/lessons/b02/starter.tscn', 'game/lessons/b02/broken.tscn'],
         '打开现成starter，选中模块整体和外观子节点分别观察；再另存副本改一项。',
         '这是A03的真实起点与故障对照；历史目录名b02不代表当前B02，不先读reference答案。',
         'P1'),
 'A04': (['game/labs/collision_roles_lab.tscn'],
         '把角色目标移到墙另一侧，分别切换外观和阻挡；复位后再切检测角色/装饰。',
         '真实Area与物理；改Mask后让角色或白色装饰重新进入，分别验证谁被检测。不是只由M1替M2。',
         'P1/P2'),
 'A05': (['game/labs/motion_lab.tscn', 'game/scenes/main.tscn'],
         '在现成运动Lab只改速度，比较相同时间位移；再在主游戏检查直走/斜走。',
         'Lab是简化运动模型；真实控制器、帧率差异与碰撞在提供的主游戏副本和实际运行条件中检查。',
         'P2'),
 'A06': (['game/labs/motion_lab.tscn', 'game/scenes/main.tscn'],
         '固定重力只改起跳速度，按跳跃观察；用“仅回到起点”重播对照。',
         '恢复全部初值会复位参数和控件，重播保留参数；边缘/墙边真实落地仍在主游戏检查。',
         'P2'),
 'A07': (['game/scenes/lab.tscn', 'blender/labs/transform_origin_lab.blend'],
         '任选门轴实验，闭门位置相同，再分别观察中心/侧边旋转。',
         'Godot与Blender坐标轴不同，按文件实际轴观察，不背同一个轴名。',
         'P1'),
 'A08': (['game/labs/camera_lab.tscn', 'game/scenes/main.tscn'],
         '在镜头Lab保持其他条件，只切透视/正交，分别比较FOV/Size；再试向右移动。',
         '真实Camera3D投影和地面方向；没有完整分区切镜或事件镜头，未选这些增强不增加作业。',
         'P1'),
 'B01': (['blender/labs/kitbash_style_lab.blend'], '固定视图先比较Base与Variant大形，不先画纹理。', '小屋比例示例，不是商业品质标杆。', 'P4/P6'),
 'B02': (['blender/labs/transform_origin_lab.blend', 'blender/labs/kitbash_style_lab.blend'],
         '直接打开现成静态样本，在副本中比较对象变换与网格编辑；再选小屋轮廓。',
         '原点/缩放样本已给；平滑/倒角局部对照可在副本用现有方块作一次设置，不要求从零搭模型。',
         'P4'),
 'B03': (['blender/labs/kitbash_style_lab.blend'], '固定机位光照，只调整变体一处颜色，先看焦点和大色块。', '原生材质参数练习，不自带自动色彩评分器。', 'P4/P8'),
 'B04': (['game/labs/material_lab.tscn', 'blender/labs/uv_material_lab.blend'],
         '保持灯光不动，先只改左球粗糙度；复位后切换共享材质，再改一次。',
         '双球可切真实共享/独立资源，自发光与实际光源可分开；不把自发光球当环境照明或Glow已实现。',
         'P4/P6'),
 'B05': (['blender/labs/kitbash_style_lab.blend', 'game/scenes/main.tscn'],
         '在副本中选一个静态部件导出，再接到自己的游戏视觉包装。',
         '给出源样本与参考工程；学员GLB往返、原点与功能保持仍须实际做。',
         'P4/P7'),
 'B06': (['game/labs/event_lab.tscn', 'game/scenes/main.tscn'],
         '在事件Lab先发一次正确对象请求，再发错误对象和同帧双请求，比较计数。',
         '按钮注入事件用于时序与状态实验，不伪称鼠标点击就是Area碰撞；真实拾取在主游戏，故障开关不带到成品。',
         'P2'),
 'B07': (['game/labs/event_lab.tscn', 'game/scenes/main.tscn'],
         '在事件Lab切换可见反馈，比较成功计数和显示；再观察主游戏真实拾取。',
         '现成反馈与规则分离；本Lab未提供完整音频/粒子/打击感库，不以反馈关掉判规则失败。',
         'P2/P9'),
 'B08': (['game/labs/event_lab.tscn', 'game/scenes/main.tscn'],
         '先在事件Lab完成、重开并再次请求，再在主游戏改变窗口检查布局。',
         '事件Lab有独立状态和显示、可重复重开；主游戏的完整十星与窗口布局仍分别实测。',
         'P2/P3'),
 'B09': (['game/scenes/visual_lab.tscn'], '固定FOV，只改主光强度，对照亮面、暗部和目标。', '光强样例，不包含所有环境光/阴影配置。', 'P4/P9'),
 'B10': (['game/scenes/visual_lab.tscn'], '将一条参考规则用于同机位对照，解释为什么不继续加细节。', '参考来源由学员提供；Lab是原创示意，不是假大师截图。', 'P4/P8'),
 'B11': (['game/scenes/main.tscn'], '记录实际设备/分辨率/路线，再测一次基线，不先盲目优化。', '不自带已验证性能收益；结果来自你的设备。', 'P2/P11'),
 'B12': (['game/lessons/b02/broken.tscn', 'game/labs/event_lab.tscn', 'game/scenes/main.tscn'],
         '先在现成故障副本说明实际现象，再提出一个可能原因和最小验证，不先读答案。',
         '可用A03故障或事件防重故障练排查；工程diff/版本恢复仍用自己的修改记录，不能自动判会。',
         'P3'),
 'B13': (['game/scenes/main.tscn'], '沿本课任务换一种可用物品，先写允许改与必须保留项。', '完整参考用于比较；检查使用自己的快照和未揭示变式。', 'P3'),
 'C01': (['game/world/exploration.tscn'],
         '先运行三段路线，指出主路、找钥匙的支路和回程；另存副本只改变一个路口。',
         '三段参考已实现，不等于自己的地图已通过；新路线仍要实走与陌生玩家检验。',
         'P1/P7'),
 'C02': (['game/scenes/visual_lab.tscn', 'game/world/exploration.tscn'],
         '先在疏密实验作对照，再用实际玩家镜头检查庭院、林路、观景台的焦点。',
         '原生实验与原创资产参考都已备好；视觉选择由真人验收，未冒称商业品质。',
         'P4/P8'),
 'C03': (['game/labs/animation_lab.tscn', 'blender/labs/animation_fixture.blend', 'game/scenes/main.tscn'],
         '先打开原创动作样本查看骨架、蒙皮、三段片段，再比较角色大小与控制器职责。',
         '原创教学角色与实际动画现成可用；不是正式美术选型或通用骨架兼容保证，替换自己的角色还需验证。',
         'P4/P10'),
 'C04': (['game/labs/animation_lab.tscn', 'blender/labs/animation_fixture.blend'],
         '在动作Lab只调待机到行走的融合值和过渡时间，观察肢体而非读源码。',
         '真实AnimationTree与导入片段；Walk原地播放，主游戏移动/动画同步和脚滑验收仍需接到自己的控制器。',
         'P10'),
 'C05': (['game/labs/material_lab.tscn', 'blender/labs/uv_material_lab.blend', 'game/lessons/b02/starter.tscn'],
         '先切Godot材质共享/独立，再在Blender检查Shared_A/B与Independent_C的数据引用。',
         '提供真实材质和网格共享对照；动画引用及独立运行状态在实际角色实例中另验，不用一个静态图包办。',
         'P6/P7'),
 'C06': (['game/labs/interaction_lab.tscn', 'game/labs/platform_lab.tscn'],
         '先在门实验观察靠近与开门；需要平台变式时，打开平台实验比较站立跟随和起跳离开。',
         '门与平台均已可交互；平台是实际独立CharacterBody与AnimatableBody，完整机关阻挡/关卡集成仍需实际项目验证。',
         'P2/P7'),
 'C07': (['blender/labs/uv_material_lab.blend', 'blender/labs/kitbash_style_lab.blend'],
         '打开UV样本，上排几何和光照相同，先观察棋盘格；只调整中间板的UV，不改几何尺寸。',
         '纹理已打包，正常/拉伸/密度样本现成；模块连接用小屋部件，复杂角色UV不列入当前必修。',
         'P6'),
 'C08': (['game/labs/effects_lab.tscn'],
         '全关基线开始，一次开Fog、Glow或景深；观察实际渲染器和对应参数。',
         '普通雾/辉光已实现；景深需Forward+或Mobile，Compatibility明确禁用；不冒充体积雾。',
         'P4/P9'),
 'C09': (['game/scenes/main.tscn'], '对同一构建/机位选择一项真实测量，不改多种设置。', '基准由目标设备提供，headless不代表GPU画面性能。', 'P7/P11'),
 'C10': (['game/labs/interaction_lab.tscn', 'game/world/exploration.tscn'],
         '先用隔离实验区分靠近、允许和结果，再在林路拿钥匙、到门前按E。',
         '门和钥匙已接入主游戏；实验文件与主游戏存档完全隔离。',
         'P2/P7'),
 'C11': (['game/labs/interaction_lab.tscn', 'game/world/exploration.tscn'],
         '先在实验测试缺失/损坏文件，再在主游戏主动保存、退出并继续。',
         '主游戏有独立版本存档和备份；恢复到安全检查点，不保存攻击中间帧；不承诺抗所有断电故障。',
         'P2/P11'),
 'C12': (['game/world/exploration.tscn'], '先运行完整三段主线和暂停菜单，再按自己的目标平台实际导出验收。', '源码与自动测试不是全部设备体验认证；发布包仍须目标设备检查。', 'P11'),
 'D01': (['blender/labs/kitbash_style_lab.blend'], '先另存副本，选Variant_Roof只改一项比例，比较Base。', '原创几何二开样例，不是已购买的完整资产套装。', 'P6'),
 'D02': (['blender/labs/kitbash_style_lab.blend', 'game/labs/material_lab.tscn'],
         '固定光照，先统一一件变体色彩，再单独调粗糙度。',
         '支持局部材质观察，不等于整库风格已经统一。',
         'P6/P8'),
 'D03': (['blender/labs/kitbash_style_lab.blend'], '为一件变体记录源、用途、版本、引用和预览机位。', '样例不自带完整商业资产库，按本地实际资源建立。', 'P5/P7'),
 'D04': (['blender/labs/kitbash_style_lab.blend', 'game/world/exploration.tscn'],
         '用现成原创GLB库替换或调整一处，固定机位作前后对照，再走完整路线。',
         '三段原创生产参考已接入12类静态资产；不是已购买外部套装或最终美术签收。',
         'P8'),
 'D05': (['blender/labs/animation_fixture.blend', 'game/labs/animation_lab.tscn'],
         '先直接播放原创角色的三段现成片段，观察骨骼/网格关系，再到Godot比较导入和融合。',
         '有真实骨架、蒙皮与动作；不是外部动作库或通用重定向，新角色仍先做一段兼容小试。',
         'P4/P10'),
 'D06': (['game/labs/animation_lab.tscn', 'game/world/exploration.tscn'],
         '先看隔离命中窗口，再在主游戏面对木桩按J；比较远处/背对/关闭训练。',
         '动作、命中、恢复控制已整合；训练可关闭且不影响十星，不是完整敌人/战斗系统。',
         'P10'),
 'D07': (['game/world/exploration.tscn'],
         '从庭院经过林路拿钥匙到观景台，完成十星；测试保存、继续、重开与训练关闭。',
         '这是可玩的完整参考版本；儿童掌握、商业视觉质量与全部设备兼容仍需独立验收。',
         'P11'),
 'E01': (['game/labs/navigation_lab.tscn'],
         '保持导航半径，调大真实碰撞球；先猜路径存在是否等于能过窄门。',
         '使用真实NavigationServer与碰撞；网格是预制规则生成，非自动烘焙或动态避障系统。',
         '按需专项'),
 'E02': (['game/labs/large_scene_lab.tscn', 'game/world/exploration.tscn'],
         '固定机位与渲染器，单独切批量或LOD，重新采样并记录条件。',
         '界面帧间隔和draw calls是真实当前运行值；无渲染模式不代表GPU性能，不保证每项优化都会更快。',
         'P11'),
 'E03': (['game/labs/shader_lab.tscn'],
         '先保持左侧参考不变，只在右侧启用条纹、边缘强调或风摆一项。',
         '真实空间Shader含关闭与冻结；不是完整Shader效果库或材质自动转换。',
         'P9'),
 'E04': (['game/scenes/lab.tscn'], '先用现有门轴说明预期轨迹，再定义复杂旋转问题。', '基础Lab不能代替复杂旋转专项验证。', '按需专项'),
 'E05': (['game/labs/large_scene_lab.tscn'],
         '只切分块驻留并移动相机，观察远区节点实际创建/释放，再分别对照MultiMesh和LOD。',
         '9区块432物体的有界实验；另有真实场景异步读取按钮；共享资源可能缓存，不等于无限地图或全部显存卸载。',
         '按需专项'),
 'E06': ([], '只解释联网增加了哪类协调问题，以及本项目是否需要。', '全K，只理解用途，不要求实操或背诵。', '不加入单机生产门槛'),
 'E07': ([], '选一个真实专项问题，整理已测、未测和采用理由。', '用自己的专项证据，不凭目录存在宣布通过。', '按需专项')}


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
                     f'**打开方式与分工：** [现成实验入口]({link("LABS-START.md",key)})。Godot打开当前场景按F6；Blender直接打开已有文件，先另存副本。默认先体验，不为上课重新搭建。\n\n'
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
            launch = binding_text(ident) + '\n默认先用现成实验体验；下方连接/实现任务属于之后的项目迁移，不作为打开本实验的前置。OpenMAIC已提供同等概念证据时不重复刷题，但真实资源/物理/导出等软件证据不可由模拟代替。\n先复用上述现有样本，不重新生成同一个Lab。练习可提示；检查先只读快照，不一边改答案一边评分。\n'
            text = text.replace(prompt_anchor, launch + prompt_anchor, 1)
            text = text.replace('## 7. 后续真机任务（配套待做，不作为当前课堂依赖）', '## 7. 正式项目迁移（达到相应阶段再做）')
            text = text.replace('以下是后续真机操作的对应范围，不要求本轮打开软件。', '以下是软件操作的对应范围；优先使用0A已给出的实验，尚无配套的部分如实标待验证。')
            text = text.replace('按用户安排，当前先完成全部课件，之后再统一补素材、Godot/Blender起始与参考工程。',
                                '已有Lab先随课使用；完整生产按任务单推进，未交付的逐课配套不冒充完成。')
            if row['m']:
                mode = runpy.run_path(str(AUTHOR/'lesson_modes.py'))
                text = text.replace('## 7. 正式项目迁移（达到相应阶段再做）', mode['PROJECT_OPEN'] + '## 7. 正式项目迁移（达到相应阶段再做）', 1)
                text = text.replace('## 9. 复现与延迟检查', mode['PROJECT_CLOSE'] + '\n## 9. 复现与延迟检查', 1)
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
    output.update(runpy.run_path(str(AUTHOR/'ready_lab_pages.py'))['make_pages'](BINDINGS, by_id, order))
    for name in ('game/README.md','curriculum/delivery-status.md','docs/improvements.md'):
        if name in output:
            prefix = '../' if name.count('/') == 1 else ''
            output[name] = '> **现成配套更新：** 共享实验、四个Blender文件和操作分工见[实验入口](' + prefix + 'LABS-START.md)。旧轮次的待做说明不代表本轮文件仍缺失；项目迁移与真实试教依然分别取证。\n\n' + output[name]
    output['AGENTS.md'] += '\n## 使用收尾维护\n\nlesson_modes.py控制体验/作品分流，默认会话物理移除作品段落；TODAY是孩子短卡，SESSION是教练输入。StudySession仅保留内存游戏状态；变更必须运行study_safety和原275项回归。workspace只写私人副本，恢复先备份；独立导出必须运行release模板，不把编辑器运行说成成品。\n'
    output['AGENTS.md'] += '\n## 现成配套维护\n\n现成实验优先于重复搭建；ready_lab_pages.py与BINDINGS维护入口、首步和局限。修改game/labs要在Godot4.7.2运行practical_labs及原回归；Blender5.2.0重开已提交四个文件，不能由生成器存在代替实物。骨架动作、UV纹理都是原创样本，不冒充最终美术。实验完成、学员掌握和正式项目交付分开。\n'
    for name in ('README.md','START-HERE.md'):
        output[name] = '> **现成场景入口：** [直接打开Godot / Blender实验](LABS-START.md) · [亲子学习](FAMILY-START.md)。不需要先从空项目搭建。\n\n' + output[name]
    for name in ('README.md', 'START-HERE.md'):
        output[name] = '> **新主游戏：** [庭院—林路—观景台](WORLD-START.md)，F5直接开始；旧参考和实验全部保留。\n\n' + output[name]
        output[name] = output[name].replace('新地图、整图美术和训练角仍需单独制作和验证。', '三段地图、原创资产和木桩训练/存档已有可运行参考；真实试教、最终美术和全部设备仍单独验收。')
    output['AGENTS.md'] += '\n## 三段生产参考\n\n默认主场景为game/world/exploration.tscn，旧main保留作教学回归。修改须同时运行production_suite和全部原测试；12类原创GLB由build_world_assets.py复建。普通雾/辉光/景深按实际渲染器核对，不假启用不支持的效果。OpenMAIC课堂由用户稍后自行生成。不要记录虚构儿童试教或全设备通过。\n'
    return output
