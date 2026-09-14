# 学习路线图

## 项目目标

这不是传统的“先学完 Blender，再学 Godot”课程。

课程围绕一个持续成长的真实项目推进：

> **3D 星星收集 Demo → 可玩的中型 3D 原型**

学习顺序遵循：

**需求 → 必要概念 → 互动理解 → 真机实战 → 验收 → 常见坑 → 性能意识 → Git 留档**

---

# 初级阶段：做出一个完整可玩的 3D Demo

初级阶段的目标不是“学完 Godot / Blender”，而是建立完整的 3D 游戏开发闭环。

## B01｜3D 空间与 Transform

**实战结果：** 能在 Godot / Blender 中移动、旋转、缩放物体，并理解 Local / Global、Origin / Pivot。

核心词：

- X / Y / Z
- Position
- Rotation
- Scale
- Transform
- Local / Global
- Origin / Pivot
- Apply Transform

AI 时代重点：知道 AI 所说的“位置、朝向、轴、原点、局部坐标”具体对应什么。

---

## B02｜Scene、Node 与灰盒场景

**实战结果：** 用 Cube / Plane 搭出一个可以测试移动的灰盒关卡。

核心词：

- Scene
- Node
- Node3D
- MeshInstance3D
- Instance
- Parent / Child
- Graybox / Blockout
- Grid / Snap

AI 时代重点：能看懂 Godot 场景树，并判断一个功能应该属于哪个节点。

---

## B03｜玩家走路与跑步

**实战结果：** 玩家可以 WASD 移动、Shift 跑步。

核心词：

- CharacterBody3D
- InputMap
- Velocity
- Speed
- Delta Time
- move_and_slide

只需理解用途，不要求背 API。

---

## B04｜碰撞与地面

**实战结果：** 玩家不会穿墙或掉穿地面。

核心词：

- Collision
- CollisionShape3D
- StaticBody3D
- Capsule / Box / Convex
- Layer / Mask
- Visual Mesh ≠ Collision Mesh

性能重点：碰撞体应尽量简单，不要默认拿高模网格直接做复杂碰撞。

---

## B05｜重力、跳跃、斜坡与楼梯

**实战结果：** 玩家能稳定跳跃、落地、走斜坡。

核心词：

- Gravity
- Grounded
- Floor Normal
- Slope
- Step
- Jump Velocity

重点不是公式，而是知道常见手感问题来自哪里。

---

## B06｜第三人称 Camera

**实战结果：** 鼠标旋转镜头，镜头围绕玩家工作。

核心词：

- Camera3D
- Pivot
- FOV
- Pitch / Yaw
- Mouse Sensitivity
- Spring Arm / Raycast 思路

视觉重点：亲自拖动 FOV、距离、灵敏度来建立手感。

---

## B07｜Blender：制作第一个游戏资产

**实战结果：** 在 Blender 中制作一个简单低多边形星星。

核心词：

- Mesh
- Vertex / Edge / Face
- Edit Mode
- Extrude
- Bevel
- Shade Smooth
- Normal
- Origin
- Apply Scale

重点：不是学习复杂建模，而是完成一个“能进入游戏”的资产。

---

## B08｜PBR 材质与视觉参数

**实战结果：** 星星具备金属感、粗糙度和自发光效果。

核心词：

- Material
- Principled BSDF
- Base Color
- Metallic
- Roughness
- Normal Map
- Emission

互动重点：大量拖参数，看结果，不做图形学公式推导。

---

## B09｜Blender → Godot 资产导入

**实战结果：** GLB / glTF 资产正确进入 Godot。

核心词：

- GLB / glTF
- Import
- Scale
- Orientation
- Normal
- UV
- Material
- Reimport

外行高频坑：尺寸、坐标轴、Origin、未 Apply Transform、材质差异。

---

## B10｜拾取星星

**实战结果：** 玩家碰到星星后触发拾取。

核心词：

- Area3D
- Signal
- body_entered
- Group
- Queue Free
- Trigger

重点：理解“物理碰撞”和“触发区域”不是同一个用途。

---

## B11｜反馈：音效、粒子、旋转、发光

**实战结果：** 拾取开始有游戏感。

核心词：

- AudioStreamPlayer3D
- GPUParticles3D
- Tween
- AnimationPlayer
- Emission
- Feedback / Juice

重点：学习“动作发生后，玩家如何感知到”。

---

## B12｜UI 与游戏完成条件

**实战结果：** 显示 `3 / 10`，全部收集后显示完成。

核心词：

- Control
- Label
- HUD
- Counter
- Game State
- Signal

---

## B13｜基础灯光与 Environment

**实战结果：** 灰盒场景第一次变得“像游戏”。

核心词：

- DirectionalLight3D
- WorldEnvironment
- Shadow
- Ambient
- Exposure
- Fog
- Tone Mapping

视觉重点：自己拖动亮度、曝光、雾和颜色。

---

## B14｜第一次性能体检

**实战结果：** 会看性能数据，而不是只凭感觉。

核心词：

- FPS
- Frame Time
- Draw Call
- Triangle
- VRAM
- Profiler
- LOD
- Occlusion
- Instancing

初级验收：知道“哪里贵”，不要求立即掌握所有优化技术。

---

## B15｜Debug：故意把项目搞坏

**实战结果：** 能定位问题属于模型、材质、碰撞、脚本、灯光还是导入。

练习：

- Scale 异常
- Origin 偏移
- Collision Layer 错误
- Signal 没连接
- Normal 异常
- 材质过亮
- Camera 穿墙

---

## B16｜综合挑战

在不照抄教程的前提下，新增一种拾取物，例如：

- 蓝色能量球
- 钥匙
- 金币
- 临时加速道具

需要自己决定：

- 使用什么节点
- 使用什么材质参数
- 是否需要 Area3D
- 如何给玩家反馈
- 是否存在性能风险

完成后，初级阶段结束。

---

# 中级阶段：从 Demo 走向真正的小型 3D 游戏

## I01｜角色模型、骨骼与蒙皮

- Armature
- Bone
- Rig
- Skin
- Weight
- Skeleton3D

目标：能使用现成角色，并理解 AI / 资产库返回的角色是否可用。

## I02｜动画状态系统

- Idle / Walk / Run / Jump
- AnimationPlayer
- AnimationTree
- Blend
- State Machine
- Root Motion（先理解用途）

## I03｜可复用场景与组件化思维

- PackedScene
- Resource
- Composition
- Signal
- Interface 思维

目标：不把整个游戏写成一团脚本。

## I04｜门、机关、移动平台、陷阱

- Trigger
- State
- Tween
- RayCast
- Layer / Mask

## I05｜模块化环境资产

- Modular Asset
- Grid
- Snap
- Texel Density
- Decal
- Trim Sheet（理解用途即可）

## I06｜更完整的光照与画面

- Key / Fill / Rim
- GI
- Lightmap
- AO
- Reflection
- Tone Mapping

## I07｜大场景与性能

- LOD / HLOD
- Occlusion Culling
- Instancing
- MultiMesh
- Shadow Cost
- Transparency Cost
- Streaming 思维

## I08｜导航与简单敌人

- NavigationMesh
- NavigationAgent3D
- Detection
- State Machine
- Chase / Patrol

## I09｜基础交互系统

- Interaction Raycast
- Prompt
- Item Data
- Inventory 基础

## I10｜存档、设置、输入映射

- Save Data
- Config
- Input Remap
- Audio Bus
- Graphics Settings

## I11｜工程质量与发布

- Git 分支
- Debug Build
- Release Build
- Export
- Profiling
- Asset License
- Target Hardware

## I12｜中级综合项目

将星星收集 Demo 扩展成一个 10–20 分钟可完成的小型 3D 游戏原型。

至少包含：

- 正式角色
- 动画
- 一个简单敌人或机关系统
- 一个完整目标
- UI / 音效 / 视觉反馈
- 一轮性能检查
- 可导出的可玩版本

---

# 学习完成的判断标准

不是“看完多少课程”，而是是否具备以下能力：

1. 能把玩法拆成节点、资产、数据、状态和反馈。
2. 能使用专业关键词向 AI 描述需求。
3. 能在 Inspector / Blender 面板里亲自调整关键参数。
4. 能看出 AI 结果明显哪里不对。
5. 遇到问题时，能先判断问题属于哪一类。
6. 在添加视觉效果前，会想到性能成本。
7. 知道什么时候应该继续让 AI 做，什么时候必须自己做审美或工程判断。
