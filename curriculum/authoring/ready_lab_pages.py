"""Ready-file navigation generated from the same 47-lesson binding registry."""
from __future__ import annotations

START = '''# 现成实验入口：先打开、试一试，不从零搭建

打开完整仓库的 `game/project.godot`，使用 **Godot 4.7.2**。在文件面板打开 **`labs/lab_hub.tscn`**，按 **F6（运行当前场景）**；也可F5进入主游戏后点 `Concept labs`。F5是运行整个项目，不一定运行你选中的实验。

实验目录共12个入口，含已有参考与A03起点；不是新增12套独立课程。每课只用0A指向的一个模式，先预测，再改一项。新实验的中文侧栏可滚动、可键盘聚焦；旧参考界面中保留的英文可对照逐课说明，不要求背按钮名。

**孩子不需要先写脚本、搭完整场景、创建测试骨架或下载角色。** 实验脚本在运行时装配的节点，可在运行后的Remote场景树看见；编辑器启动前看到一个根节点不表示场景没做完。要保留修改请另存副本/记录参数，Remote临时修改不是保存到原场景。

## 先按当前问题选择

|想理解什么|直接打开什么|本次只做什么|
|---|---|---|
|位置、旋转、父空间、门轴|`game/scenes/lab.tscn`；`blender/labs/transform_origin_lab.blend`|切到一个相关模式，改变一项，再恢复；Godot与Blender轴向分别看|
|节点、实例、外观与功能职责|`game/lessons/b02/starter.tscn`，再按需用`broken.tscn`|选择整体或子节点做一次局部修改；历史路径b02对应的是现在A03|
|看得见、挡得住、检测谁|`game/labs/collision_roles_lab.tscn`|移动黄色角色；分别切外观/阻挡，再让角色和白球进入蓝区比较Mask|
|速度、起跳与重力|`game/labs/motion_lab.tscn`；真实控制器在主游戏|对照同一参数；“仅回到起点”保留参数，“恢复全部初值”连参数一起恢复|
|固定镜头、透视/正交、移动方向|`game/labs/camera_lab.tscn`|切投影，只调对应FOV或Size；预测“向右”相对谁|
|材质参数、自发光、资源共享|`game/labs/material_lab.tscn`|独立材质时只改左球；再切共享，比较右球；实际灯光与自发光分开|
|事件、条件、防重复、反馈和重开|`game/labs/event_lab.tscn`|发送一次/错误对象/同帧双请求；关掉防重作反例，再复位|
|固定机位的疏密、焦点、光照|`game/scenes/visual_lab.tscn`|只切密度或主光，观察角色、主路和焦点；不当商业美术标杆|
|移动平台和角色关系|`game/labs/platform_lab.tscn`|站稳后比较跟随，起跳和离开；角色不是平台的子节点|
|靠近、允许、交互结果、保存恢复|`game/labs/interaction_lab.tscn`|靠近但没钥匙、拿钥匙、重复开门；再试正常/缺失/坏档/旧档|
|骨骼、蒙皮、动作片段、融合和命中窗口|`game/labs/animation_lab.tscn`；`blender/labs/animation_fixture.blend`|现成原创角色的待机/行走融合；攻击/中断/远近各一次，不先绑骨架|
|真实收集、走跑跳、UI与项目回归|`game/scenes/main.tscn`|WASD移动，Shift跑，空格跳，R重开；这是参考工程，不是孩子已完成的作品|

## Blender：直接开已有文件，不先运行生成器

使用 **Blender 5.2 LTS**（本轮自动检查固定5.2.0）。直接打开 `blender/labs/` 下现成 `.blend`，先另存到自己的练习副本。无需装插件或联网取图；新增UV文件已打包棋盘格图像。

`transform_origin_lab.blend`：比较中心/侧边支点，以及外观相同的Applied/Unapplied Scale；不把静态修正套到绑定角色。

`kitbash_style_lab.blend`：已有小屋的Base与Variant部件。改一个比例、颜色或组合，不要求从零建模。B02的平滑着色/倒角可在现成静态块副本各设一次，比较轮廓；这不是反复搭场景练快捷键。

`uv_material_lab.blend`：上排已有正常、拉伸、密度不同的UV棋盘格；下排Shared_A/B共享网格和材质，Independent_C独立。选中`UV_Stretched`，进入UV编辑，仅改UV再比较；先别改几何尺寸来掩盖拉伸。

`animation_fixture.blend`：真实骨架、蒙皮和Idle/Walk/Attack三个片段已准备。播放时间轴；需要换动作时在NLA编辑器单独Solo对应轨道，每次只开一段。`game/assets/practice_robot_roundtrip.glb`是该原创角色经Blender回导的样本，不代表任意商用角色都兼容。

文件中有`START_HERE_中文说明`文本（两个新增文件）。撤销恢复本次修改，或者不保存关闭并重开原文件；不让孩子运行作者用的`build_*.py`来准备上课材料。

## OpenMAIC、原生软件、正式项目怎样分工

**OpenMAIC适合先理解：** 预测、方向示意、事件/状态时间线、选择与对照、概念讲回去。已得到等价证据的环节不重复做三份作业。没有在本轮提供课堂导出文件，所以这里没有声称逐课生成的页面都经过实测。

**Godot / Blender用来确认真实行为：** Area/碰撞与Layer/Mask、资源共享、真实UV与原点/导出、骨架/蒙皮/动画导入、实际Camera投影、读写和恢复、运行窗口与目标设备。模拟按钮改变示意，不等于引擎或文件真的执行过。

**正式项目用来迁移：** 仅当本课概念已能说明，才把局部选择接进自己的游戏并回归。对话卡中“让AI连接/实现”的项目任务不是体验模式的入场条件。谁负责状态、哪些旧功能必须保持等判断仍由孩子作；AI和爸爸可以代实现，不代写孩子的预测。

## 恢复、文件与安全边界

新实验的“恢复全部初值”会恢复参数、对象、开关和动画/事件状态；运动另有保参重播。门实验是例外：**重置场景保留专用存档**，删除按钮只操作`user://teaching_interaction_lab_v1.json`，不读取你的其他游戏存档。测试坏档也只写这个实验文件；先看按钮文字，不使用个人唯一存档做测试。

事件Lab通过按钮注入请求，不伪装物理碰撞。动作Lab使用真实蒙皮/AnimationTree和窗口/距离判定，不含与主游戏合体的完整战斗。新资产是原创教学样本，不是最终选型、通用重定向或成品美术。

[逐课配套核对表](curriculum/practical-resource-audit.md) · [验证与未验证项](docs/practical-lab-validation.md) · [家庭学习](FAMILY-START.md) · [全部课程](curriculum/lesson-index.md)
'''

def make_pages(bindings, by_id, order):
    rows = ['# 逐课配套核对：47课共用少量真实实验', '',
            '[直接打开现成实验](../LABS-START.md)。此表与各课0A、对话1及家庭会话共用一个BINDINGS源；不另造课号。', '',
            '本表是材料与路径审查，不是所有M已通过、所有课已试教或游戏已完成。实验只覆盖明确切片；真实工程迁移按原M检查。', '',
            '|课号/主题|建议主要环境|现成文件|先做的一件事|仍须注意的边界|', '|---|---|---|---|---|']
    for ident in order:
        paths, first, limit, _ = bindings[ident]
        if ident == 'E06': mode = 'OpenMAIC/对话即可，全K'
        elif not paths: mode = '参考/概念讨论；所选专项另备实际样本'
        elif any(p.startswith('blender/') for p in paths) and any(p.startswith('game/') for p in paths): mode='OpenMAIC先理解；Godot/Blender各验相关部分'
        elif any(p.startswith('blender/') for p in paths): mode='Blender现成副本'
        elif paths == ['game/scenes/main.tscn']: mode='已有游戏参考/自己的工程/目标设备'
        else: mode='OpenMAIC先理解；Godot真实对照'
        files='、'.join(f'[{p.rsplit("/",1)[-1]}](../{p})' for p in paths) or '本课不需要专用3D文件，或专项按需'
        title=by_id[ident]['title'].replace('|','／')
        rows.append(f'|[{ident} {title}](lessons/{ident}.md)|{mode}|{files}|{first}|{limit}|')
    rows += ['', '## 不把缺材料当孩子不会', '',
             'A01/B10的参考必须真实可查看；没拿到图片先用文字/原创体块表达，不虚构大师画面。E01导航、E03专项Shader、E05大场景等没有完整专用包；未选不阻塞主线，选定后围绕实际需求由成人/AI补最小样本，不强迫孩子先重造系统。', '',
             'C01/C02/D04/D07的三段地图、正式资产统一与最终试玩是孩子作品的生产任务，参考场景和实验不能代替该作品交付。C08并未提供Fog/Glow/DOF全套开关；非当前必要效果不为凑课强加。', '',
             '需要亲手理解的是选择、预测、改变条件、观察、恢复和验收；不是把生成器已经能完成的空场景搭建逐步抄一遍。构建关系本身是学习目标时，在现成副本做一次局部修改即可。', '']
    godot = '''# Godot共享实验目录

[统一入口与分工](../../LABS-START.md) · [逐课核对](../../curriculum/practical-resource-audit.md)

打开`lab_hub.tscn`按F6；主游戏`Concept labs`按钮也进入此目录。相邻课共享实验，只看当前任务。新增侧栏中文、可滚动，固定相机避免不必要的镜头控制。

camera：真实透视/正交和方向；event：按钮注入的条件/状态/反馈/重开；interaction：实际Area/门条件/专用存档及异常；platform：真实物理承载；animation：已导入原创骨架、蒙皮、三动作与AnimationTree。

collision补真实Layer/Mask与装饰对照，Reset同时恢复开关；motion区分恢复参数和保参重播；material支持真实共享/独立及Emission/实际光源。现有空间、视觉和A03起点保留。

多数实验在运行时构建节点；Remote场景树可观察，不需要在编辑器里重建。完整恢复重置当前实验，门的持久化文件另有专用删除按钮。脚本实现与实验结果不是学员已掌握的证明。
'''
    blender = '''# Blender共享起始文件

[直接打开与操作说明](../../LABS-START.md) · [逐课对应](../../curriculum/practical-resource-audit.md)

直接打开现成`.blend`，先另存副本。运行基线Blender5.2 LTS；本轮作者检查固定5.2.0。无需插件、密钥或另找网络模型。

- `transform_origin_lab.blend`：中心/侧边门轴、静态变换与尺度。
- `kitbash_style_lab.blend`：Base/Variant小屋、比例、部件、风格统一；不要求从零建模。
- `uv_material_lab.blend`：内嵌棋盘格，正常/拉伸/密度对照，真实共享/独立网格和材质。
- `animation_fixture.blend`：原创5骨骼蒙皮小人，Idle/Walk/Attack片段与NLA；不要求先绑骨架。

新文件有中文说明文本。原有场景的英文对象名是定位标记，不考记忆。按实际软件轴向观察；Blender预览或渲染不等同于Godot成品效果。

`build_labs.py`与`build_practical_labs.py`是**作者复建/验证工具**，不是孩子开始课程的步骤。新增构建器会将同一原创角色导出`game/assets/practice_robot_roundtrip.glb`，为往返检查提供已完成样本；真正改动后的项目仍由学员验收。所有样本保留源，软件课程完成不代表正式美术库已完成。
'''
    return {'LABS-START.md':START,'curriculum/practical-resource-audit.md':'\n'.join(rows),'game/labs/README.md':godot,'blender/labs/README.md':blender}
