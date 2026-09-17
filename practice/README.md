# 实践包｜打开就能试

用户平台仅macOS、Windows。工程固定Godot 4.7.2；Blender现成文件的检查基线为5.2.0。具体实验边界见当课教案，不让孩子为理解一个概念先搭半个游戏。

## 打开主游戏和实验

用Godot导入本目录`godot/project.godot`。**F5**运行三段主游戏；打开`labs/lab_hub.tscn`后按**F6**运行实验目录。17个入口包括参考游戏和共享实验，不是17套重复课程。

主线：庭院3颗星 → 林路4颗星与钥匙 → 打开门 → 观景台3颗星。固定高角度镜头沿路线平移。WASD移动、Shift跑、空格跳、E交互、J木桩训练、Esc菜单、F9保存、F10读取。训练可关闭，不影响十星主线。

实验与游戏来回有当前会话暂存；右上角“继续刚才的游戏”恢复到区域安全点。未保存变化的退出／读取操作会保护进度；**暂存不是磁盘存档**，要跨启动保留请主动保存。强制结束或断电不保证未写盘变化。

读取旧档可先另存当前保护副本，不覆盖要读取的主档。实验档与游戏档分开；重新开始不删除原磁盘存档。自己的工作副本还有独立的用户数据目录。

部分实验运行时生成节点，编辑器里只看到根节点是正常的；运行后在Remote场景树观察。Remote临时修改不会自动保存设计值。

## 保存自己的创作

在仓库根运行`python3 tools/workspace.py create my-world`，再打开`.learning/projects/my-world/game/project.godot`。只维护这一个副本。

`world/creation.tres`可在Inspector调整走跑、起跳、重力或道路颜色；`world/exploration.tscn`的StarLayout可微调十个星星标记。保存、关闭、重新打开，确认改动仍在，再新开局实走。不要改稳定物品ID或把标记放到不可达处；旧档的收集记录不会因标记移动而清空。

恢复单项先运行`python3 tools/workspace.py restore my-world --file parameters`预览，再加`--confirm`。`--file layout`同理；确认后先备份当前文件，再恢复创建副本时的基线，不覆盖参考。

Blender练习文件另存到`.learning/`或自己的私人目录；不要把孩子的修改直接保存进共享参考。

## 先按当前问题选择

|想理解什么|直接打开什么|本次只做什么|
|---|---|---|
|位置、旋转、父空间、门轴|`godot/scenes/lab.tscn`；`blender/transform_origin_lab.blend`|切到一个相关模式，改变一项，再恢复；Godot与Blender轴向分别看|
|节点、实例、外观与功能职责|`godot/labs/scene_nodes/starter.tscn`，再按需用`broken.tscn`|选择整体或子节点做一次局部修改；这就是A03的节点起点|
|看得见、挡得住、检测谁|`godot/labs/collision_roles_lab.tscn`|移动黄色角色；分别切外观/阻挡，再让角色和白球进入蓝区比较Mask|
|速度、起跳与重力|`godot/labs/motion_lab.tscn`；真实控制器在主游戏|对照同一参数；“仅回到起点”保留参数，“恢复全部初值”连参数一起恢复|
|固定镜头、透视/正交、移动方向|`godot/labs/camera_lab.tscn`|切投影，只调对应FOV或Size；预测“向右”相对谁|
|材质参数、自发光、资源共享|`godot/labs/material_lab.tscn`|独立材质时只改左球；再切共享，比较右球；实际灯光与自发光分开|
|事件、条件、防重复、反馈和重开|`godot/labs/event_lab.tscn`|发送一次/错误对象/同帧双请求；关掉防重作反例，再复位|
|固定机位的疏密、焦点、光照|`godot/scenes/visual_lab.tscn`|只切密度或主光，观察角色、主路和焦点；不当商业美术标杆|
|移动平台和角色关系|`godot/labs/platform_lab.tscn`|站稳后比较跟随，起跳和离开；角色不是平台的子节点|
|靠近、允许、交互结果、保存恢复|`godot/labs/interaction_lab.tscn`|靠近但没钥匙、拿钥匙、重复开门；再试正常/缺失/坏档/旧档|
|骨骼、蒙皮、动作片段、融合和命中窗口|`godot/labs/animation_lab.tscn`；`blender/animation_fixture.blend`|现成原创角色的待机/行走融合；攻击/中断/远近各一次，不先绑骨架|
|导航与真实通行|`godot/labs/navigation_lab.tscn`|分别改变导航预留半径与真实碰撞半径，比较路径和窄门通行|
|单效果Shader|`godot/labs/shader_lab.tscn`|只开条纹、边缘强调或风摆，保留左侧参考；可冻结与关闭|
|Fog／Glow／景深|`godot/labs/effects_lab.tscn`|原生参数对照；Compatibility无景深时禁用，Forward+／Mobile再验|
|批量、LOD、剔除、分块与异步读取|`godot/labs/large_scene_lab.tscn`|保持分布不变逐项对照；再异步读一个真实场景，观察驻留变化|
|三段地图、钥匙门、战斗与存档|`godot/world/exploration.tscn`|F5启动；真实走通十星，试可选训练和主动保存；详见主游戏说明|
|旧收集参考、走跑跳、UI与回归|`godot/scenes/main.tscn`|WASD移动，Shift跑，空格跳，R重开；这是参考工程，不是孩子已完成的作品|

## Blender：直接开已有文件，不先运行生成器

使用 **Blender 5.2.0**（本轮自动检查固定5.2.0）。直接打开 `blender/` 下现成 `.blend`，先另存到自己的练习副本。无需装插件或联网取图；新增UV文件已打包棋盘格图像。

`transform_origin_lab.blend`：比较中心/侧边支点，以及外观相同的Applied/Unapplied Scale；不把静态修正套到绑定角色。

`kitbash_style_lab.blend`：已有小屋的Base与Variant部件。改一个比例、颜色或组合，不要求从零建模。B02的平滑着色/倒角可在现成静态块副本各设一次，比较轮廓；这不是反复搭场景练快捷键。

`uv_material_lab.blend`：上排已有正常、拉伸、密度不同的UV棋盘格；下排Shared_A/B共享网格和材质，Independent_C独立。选中`UV_Stretched`，进入UV编辑，仅改UV再比较；先别改几何尺寸来掩盖拉伸。

`animation_fixture.blend`：真实骨架、蒙皮和Idle/Walk/Attack三个片段已准备。播放时间轴；需要换动作时在NLA编辑器单独Solo对应轨道，每次只开一段。`godot/assets/practice_robot_roundtrip.glb`是该原创角色经Blender回导的样本，不代表任意商用角色都兼容。

文件中有`START_HERE_中文说明`文本（两个新增文件）。撤销恢复本次修改，或者不保存关闭并重开原文件；不让孩子运行作者用的`build_*.py`来准备上课材料。

## OpenMAIC、原生软件、正式项目怎样分工

**OpenMAIC适合先理解：** 预测、方向示意、事件/状态时间线、选择与对照、概念讲回去。已得到等价证据的环节不重复做三份作业。没有在本轮提供课堂导出文件，所以这里没有声称逐课生成的页面都经过实测。

**Godot / Blender用来确认真实行为：** Area/碰撞与Layer/Mask、资源共享、真实UV与原点/导出、骨架/蒙皮/动画导入、实际Camera投影、读写和恢复、运行窗口与目标设备。模拟按钮改变示意，不等于引擎或文件真的执行过。

**正式项目用来迁移：** 仅当本课概念已能说明，才把局部选择接进自己的游戏并回归。对话卡中“让AI连接/实现”的项目任务不是体验模式的入场条件。谁负责状态、哪些旧功能必须保持等判断仍由孩子作；AI和爸爸可以代实现，不代写孩子的预测。

## 恢复、文件与安全边界

新实验的“恢复全部初值”会恢复参数、对象、开关和动画/事件状态；运动另有保参重播。门实验是例外：**重置场景保留专用存档**，删除按钮只操作`user://teaching_interaction_lab_v1.json`，不读取你的其他游戏存档。测试坏档也只写这个实验文件；先看按钮文字，不使用个人唯一存档做测试。

事件Lab通过按钮注入请求，不伪装物理碰撞。动作Lab使用真实蒙皮/AnimationTree和窗口/距离判定，现在可在新主游戏对照整合后的木桩训练。新主游戏使用12类原创GLB生产参考资产，不虚构采购外部包，也不把参考美术当成最终审美验收；不包含通用重定向。


[全部课程](../course/README.md) · [记忆清单](../course/memory.md) · [美术方向](style.md)
