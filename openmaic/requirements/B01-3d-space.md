# OpenMAIC Generation Requirement — B01 3D 空间与 Transform

请生成一节中文沉浸式互动课堂，主题为：

> **3D 空间与 Transform：第一次真正看懂 Position、Rotation、Scale、Local/Global 与 Pivot**

## 学习者

学习者没有 3D 美术背景，但会使用 AI 辅助编程，目标是使用 Godot 4 + Blender + AI 开发 3D 游戏。

本课不是数学课，也不是软件功能百科。

核心目标是让学习者：

- 能看懂常见 3D 空间术语
- 能亲自拖动关键参数观察效果
- 能判断简单的空间 / Transform 问题
- 能使用正确专业词向 AI 描述问题
- 学完后立刻去 Godot / Blender 完成真机练习

## 必须覆盖的核心词

只重点教授以下概念：

- X / Y / Z Axis
- Position
- Rotation
- Scale
- Transform
- Local Space
- Global / World Space
- Origin / Pivot

补充认识：

- Gizmo
- Translation
- Apply Transform

不要深入：

- Transform Matrix
- Quaternion
- 欧拉角数学推导
- 三角函数
- Godot Transform3D API 完整接口

## 教学风格

请遵循：

**先看到效果 → 再给名字 → 亲自操作 → 看错误案例 → 判断问题 → 去真实软件实战**

不要用大量幻灯片讲定义。

减少文字，优先使用互动 3D 可视化、滑块、开关、对比状态和场景题。

## 必须包含的互动场景

### 1. Transform 三连演示

显示 Cube：

- 从左移动到右
- 旋转约 45°
- 沿 Y 轴拉高

先让学习者判断三次变化分别属于 Position、Rotation 还是 Scale，再解释术语。

### 2. X / Y / Z 可视化

提供可旋转视角的 3D 场景和清晰坐标轴。

点击或操作 X / Y / Z 时让 Cube 沿对应轴移动，并同步显示 Position 数值。

### 3. Position / Rotation / Scale 参数实验

给 Cube 提供即时滑块：

- Position X/Y/Z
- Rotation X/Y/Z
- Scale X/Y/Z

提供 Reset。

让学习者完成：

- 把 Cube 移到右上方
- 绕竖直方向旋转约 45°
- 把 Cube 拉成长方体

### 4. Local vs Global

不要使用对称球体，使用有明显朝向的箭头、汽车或机器人。

先将对象旋转约 45°，然后允许切换 Local / Global Gizmo。

让学习者观察：

- Global 轴保持世界方向
- Local 轴随对象旋转

提出判断题：

“一辆已经转弯的汽车继续沿自己的车头方向前进，更接近 Local 还是 Global？”

### 5. Origin / Pivot 门轴实验

使用一扇简单门。

两个状态：

- Pivot 在门中心
- Pivot 在门侧边铰链

播放同样的 90° Rotation，让学习者直接比较。

必须总结：

“很多看起来像动画或代码问题的 Bug，其实只是 Pivot / Origin 放错了。”

### 6. 错误诊断小游戏

至少包含：

- 模型大 100 倍 → 优先想到 Scale / 单位 / 导入
- 门绕中心旋转 → Pivot / Origin
- 已转向角色却沿世界固定方向移动 → Local / Global
- 只是想移动物体却去改 Mesh 顶点 → Object Transform 与 Mesh 编辑混淆

## Quiz

6–8 题即可。

不要主要考定义，要考场景判断。

至少两题为开放题，可由 AI 老师评分：

1. Blender 中模型看起来正常，但进入游戏后尺寸异常，你首先会检查哪些事情？
2. AI 建议“把 Scale 设成 100 就能解决模型太小”，你会直接接受吗？请说明你还应该检查什么。

## AI 同学

AI 同学最多主动插话两次，且必须提出真正有价值的新手问题：

1. “Position 和在 Blender Edit Mode 里移动顶点，不都是移动吗？”
2. “Pivot 让 AI 帮我改不就行了吗，我为什么还要懂？”

老师回答时强调“识别问题类别与验收 AI 结果”的能力。

## 本课结束页

不要继续扩展理论。

明确布置两个真实软件任务：

### Godot 4

创建 Node3D + MeshInstance3D(Cube)，在 Inspector 修改 Position / Rotation / Scale，并观察 3D Gizmo。

### Blender

使用默认 Cube，在 Transform 面板重复 Position / Rotation / Scale 操作；观察 Object Origin 与旋转中心的关系。

最后提醒：

> OpenMAIC 负责理解和互动，真正的游戏开发能力必须在 Godot 与 Blender 中完成。

## 最终验收

学习者应能自然说出类似：

- “这个 Mesh 可能没问题，更像是 Transform 或导入 Scale 有问题。”
- “门的 Rotation 没问题，但 Pivot 在中心，所以转法不对。”
- “角色转向后如果沿自己的前方移动，我需要确认使用 Local 方向，而不是固定 Global 方向。”

课程整体控制在 30–45 分钟的学习量，不要为了完整而加入高级数学内容。
