# B01 真机练习｜3D 空间与 Transform

> 目标：把 OpenMAIC 里看到的概念，在真实 Godot / Blender 中亲手做一遍。

本练习不要求写复杂代码。

---

# Part A｜Godot 4

## 任务 1：创建最小 3D 场景

创建：

```text
Node3D
├── MeshInstance3D   # BoxMesh
├── Camera3D
└── DirectionalLight3D
```

要求：运行后能看见 Cube。

## 任务 2：只改 Transform

选中 Cube，在 Inspector 中依次修改：

- Position X
- Position Y
- Position Z
- Rotation Y
- Scale X
- Scale Y
- Scale Z

每次只改一个参数，观察结果。

不要一次乱改所有值。

## 任务 3：建立三个明显状态

让 Cube 依次变成：

1. 位于原点附近的正常 Cube
2. 向右移动、旋转 45° 的 Cube
3. 一个很高、很窄的长方体

重点不是记数值，而是能判断该改哪个属性。

## 任务 4：观察 Local / Global Gizmo

将 Cube 旋转约 45°。

切换局部 / 全局坐标操作方式，观察 Gizmo 方向是否跟随物体。

用自己的话回答：

> 为什么一个已经转弯的角色如果继续沿“自己的前方”走，Local 思维会更自然？

---

# Part B｜Blender

## 任务 1：使用默认 Cube

不要删除默认 Cube。

打开 Transform 面板，分别修改：

- Location
- Rotation
- Scale

观察 Blender 中的术语和 Godot 的对应关系：

| Blender | Godot | 人话 |
|---|---|---|
| Location | Position | 在哪里 |
| Rotation | Rotation | 朝向 / 旋转 |
| Scale | Scale | 相对大小 |

## 任务 2：Object Transform vs Edit Mode

做两次实验：

### A

Object Mode 中移动整个 Cube。

### B

恢复后进入 Edit Mode，全选顶点，再移动 Mesh。

观察两种情况下：

- 可见模型位置
- Object Origin
- Transform 数值

然后回答：

> “移动对象”和“移动对象内部的 Mesh 顶点”为什么不是一回事？

## 任务 3：Pivot / Origin

创建一个长方体，想象它是一扇门。

先让 Origin 保持在中心并旋转。

然后尝试把 Origin / 几何关系调整到更像“门铰链”的位置，再旋转。

只需要看到明显区别，不要求掌握所有 Origin 工具。

---

# Part C｜故意搞坏

## 实验 1：夸张 Scale

把 Cube 的某个轴 Scale 改成 10 或 100。

观察：

- 视觉上发生什么
- 相机是否还舒服
- 如果以后有碰撞，可能出现什么连锁问题

恢复正常。

## 实验 2：错误 Pivot

让“门”围绕错误位置旋转。

看到症状后，不要第一反应怀疑动画代码。

先说出：

> “我应该检查 Origin / Pivot。”

---

# Part D｜和 AI 沟通

尝试用下面这种方式描述问题，而不是只说“它不对”：

```text
我在 Godot 4 中有一个 MeshInstance3D。
Mesh 外观看起来正常，但物体尺寸明显异常。
请优先帮我检查 Transform / Scale / 导入尺寸相关原因，
不要先建议我重新建模。
```

再尝试描述门的问题：

```text
这扇门的 Rotation 数值看起来正常，
但旋转时绕模型中心转，而不是绕侧边铰链。
请帮我从 Pivot / Origin 的角度分析，
并告诉我应该在 Blender 还是 Godot 修正更合理。
```

---

# 验收

完成后确认：

- [ ] 我能在 Godot 中主动修改 Position / Rotation / Scale。
- [ ] 我知道 Blender 的 Location 对应“位置”。
- [ ] 我看过一次 Local / Global 的实际差异。
- [ ] 我看过一次错误 Pivot 的实际效果。
- [ ] 我知道 Object Transform 和 Edit Mode 改 Mesh 不是同一件事。
- [ ] 我能用 Transform / Scale / Pivot / Local / Global 等词向 AI 描述问题。

建议 Commit：

```text
lesson-01: practice 3d transform basics
```
