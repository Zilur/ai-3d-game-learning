> v4课堂主稿：[A03学生讲义](../../lessons/A03.md)；[OpenMAIC完整输入](../../../openmaic/lessons/A03.md)。下方起始/参考工程保留，配套完善在课件之后。

# A03｜用场景树搭一个可以复用的灰盒

前置：A02 的位置、旋转、缩放。当前不需要 Blender、角色代码或大模型 API。

## 开课任务卡

产物：两个来自同一个场景的模块，分别位于 X=-2 和 X=2；修改外观不误删功能节点。

|深度|本课能力|停止线|
|---|---|---|
|M 必须掌握 · KN05|区分 Node、Scene、Instance；找到外观、整体与预配置功能节点|不背全部节点类型，不讲引擎对象模型|
|M 必须掌握 · KN02/KN05|移动整个模块；知道只移动 Visual 是另一件事|不算变换矩阵；父轴/自身轴详解留给 A07|
|M 必须掌握 · KN20 入门|让 AI 只改指定对象，检查改动并恢复一个错误|不考 Git 命令记忆或实现复杂测试框架|
|K 理解即可 · KN22|统一尺寸和网格吸附有助于拼接|一句话说出用途即可，不考模块化资产管线|

今天不学 Layer/Mask、碰撞算法、角色控制、材质理论、脚本语法。StaticBody3D 和 CollisionShape3D 已经准备好；本课只认职责，具体检测在 A04。

## 打开什么

在 Godot 导入 `game/project.godot`。打开 `res://lessons/b02/starter.tscn`，按 F6，只运行这一课。F5 会运行完整星星参考解，不是本课。

先把 starter 场景另存为 `res://lessons/b02/my_practice.tscn`。不要在主场景、参考解或其他课里试改。运行场景是只供观察的固定镜头，不含玩家；不要把“不能走”当故障。

默认练习目标是桌面窗口与 Compatibility 渲染器。只记录你实际使用的系统、Godot 版本和渲染器，不要求此刻选择所有平台。

## 先看懂这棵树

```text
B02Starter
├── Stage                 已搭好的地面、相机与灯光
└── ModuleA               module.tscn 的一个实例；移动整体选它
    ├── Visual            负责外观
    ├── CollisionShape3D  预配置阻挡形状，A04再详细练
    └── Label             跟随模块的标牌
```

Node 是一项职责；Scene 保存一组节点；Instance 是把保存的场景放到当前关卡中使用。不是把整个项目复制一遍。[官方实例化教程](https://docs.godotengine.org/en/stable/getting_started/step_by_step/instancing.html)

## 实验一｜放入第二个模块

先预测：移动第二个实例，会不会把第一个一起移动？用一句话写下理由。

从 FileSystem 将 `module.tscn` 拖入练习场景，命名为 ModuleB；也可以复制 ModuleA 实例再重命名。设置 ModuleA 的 Position=(-2,0,0)，ModuleB=(2,0,0)。运行看两块是否都在镜头里。只修改 ModuleB 的 Position X，确认 A 不跟随，再恢复 B 的 X=2。

这里检验实例的独立位置，不检验材质共享；共享材质到 B04 单独实验，不能从位置独立推出所有资源都独立。

## 实验二｜为什么要选整体

先预测：只改 Visual 的 Position X，标牌和碰撞形状是否跟着走？

在临时副本上允许编辑 ModuleA 的子节点（右键实例，Editable Children／可编辑子节点），只将 Visual 的 X 从0改为1。观察模型与标牌的位置关系；在编辑器选中形状，可观察外观和预配置形状不再对齐。恢复 Visual 的 X=0，再把 ModuleA 的 X增加1；此时整个模块应一起移动。最后恢复原值。

本课只需要“改父节点影响一组孩子，改孩子只改那项职责”的操作直觉。Node3D 变换通常相对父节点，详细轴向讨论不在这一课。[官方 Node3D 说明](https://docs.godotengine.org/en/stable/classes/class_node3d.html)

## 实验三｜修复一个可恢复故障

打开 `broken.tscn` 并另存副本。现在外观与 MODULE 标牌明显错开。先不要看答案。

写一个假设，选中相关节点查看 Position。只改你认为导致故障的那一项；用“改前→改后”两张图验证。不要通过挪相机、隐藏标牌或删除功能节点掩盖问题。

恢复单个属性可使用 Inspector 的还原按钮。彻底恢复则重新从 `broken.tscn` 或 `starter.tscn` 建立副本。无需先学 Git 底层。

## 迁移｜换外观，不改职责

用另一个练习副本，把 ModuleB/Visual 的 Mesh 换成高1、半径0.5的 CylinderMesh，保留根节点位置、Label 和预配置 CollisionShape3D。只检查外观换了、位置没漂、功能节点还在。

盒形碰撞与圆柱外观不会完全重合，这是有意保留的简化形状；本课不宣称这种形状适合所有玩法，A04再比较它的取舍。不要以“外观变圆”为理由在本课实现精准网格碰撞。

## AI 协作限制

```text
在 Godot 当前练习场景里，只处理 ModuleB 的 Visual 外观。
保留 ModuleA、模块根节点变换、Label 和 CollisionShape3D。
先说明预计修改哪个节点，再给最小改动。
不要增加脚本、相机控制、材质系统或编辑其他课程。
我会检查修改范围和运行结果，代码与菜单位置可以由你查询。
```

学员先说预期影响范围，再让 AI 做。判断被 AI 提示过的练习记“有提示”，之后换对象再核对，不以禁止使用 AI 为学习目标。

## 如何结束

做完 [本课考核](assessment.md)。只提交一份简短证据：预测一句话、操作前后截图、一次错误修复、迁移后的节点树。没有必要每个术语写一份报告。

先保存自己的结果，再看 `reference.tscn` 和 [参考答案](answer-key.md)。通过后下一课是 A04 碰撞，再做 A05 移动；课号是固定索引，学习顺序以入口为准。

检索视频关键词：`Godot 4 场景实例化`、`Godot 4 场景树 父子节点`、`Godot 4 Editable Children`。视频只用于解决当前操作卡点，不要求整套看完。
