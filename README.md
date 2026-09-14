# AI 时代 3D 游戏学习

这是一个以 **Godot 4 + Blender + AI + OpenMAIC** 为核心的实战学习项目。

目标不是把学习者训练成传统意义上的“纯程序员”或“纯 3D 美术”，而是建立 AI 时代真正重要的能力：

- 能把游戏目标拆成清晰任务
- 能使用正确的 3D / 游戏开发术语与 AI 沟通
- 能判断 AI 生成的代码、模型、材质、灯光和交互是否合理
- 能识别性能、资产导入、碰撞、尺度、动画等外行常忽略的问题
- 能在 Godot 与 Blender 中亲自调节关键参数并做最终审美与工程判断

---

## 第一个实战目标

完成一个小型 **3D 星星收集 Demo**：

**走路 → 跑步 → 跳跃 → 第三人称镜头 → 碰撞 → 拾取星星 → UI → 音效 / 特效 → 基础场景美化 → 第一次性能检查**

复杂战斗、背包、任务、多人等系统暂时不进入初级阶段。

---

# 学习方式

本项目不是“看完一套课再开始做游戏”。

每课遵循：

```text
明确今天要做成什么
        ↓
学习最少必要概念
        ↓
OpenMAIC 互动课堂
        ↓
Godot / Blender 真机操作
        ↓
自己拖参数、看效果
        ↓
故意制造一个错误
        ↓
Debug + 验收
        ↓
Git Commit
```

OpenMAIC 负责帮助理解；Godot / Blender 才是真正的实验室。

---

# 从这里开始

## 1｜先看完整路线

[`curriculum/roadmap.md`](curriculum/roadmap.md)

包含：

- 初级 B01–B16
- 中级 I01–I12
- 每阶段实战目标
- 真正需要掌握的关键词
- 性能与工程意识

## 2｜理解这套课程为什么这样设计

[`curriculum/course-design-principles.md`](curriculum/course-design-principles.md)

核心原则：

> 不追求“没有 AI 能不能背着写出来”，而追求“AI 做出来以后能不能判断它对不对”。

## 3｜第一课：3D 空间与 Transform

完整教学设计：

[`curriculum/beginner/01-3d-space/openmaic-spec.md`](curriculum/beginner/01-3d-space/openmaic-spec.md)

可直接交给 OpenMAIC 的生成要求：

[`openmaic/requirements/B01-3d-space.md`](openmaic/requirements/B01-3d-space.md)

上完课后的 Godot / Blender 真机练习：

[`curriculum/beginner/01-3d-space/practice.md`](curriculum/beginner/01-3d-space/practice.md)

## 4｜不知道专业词时

[`glossary/core-3d.md`](glossary/core-3d.md)

不要背词汇表。遇到词 → 知道用途 → 调一次参数 → 用它向 AI 描述一次问题。

---

# OpenMAIC 在这里负责什么？

我们把课程内容分成两层。

## 课程源代码

本仓库维护：

- 学习目标
- 知识边界
- 必学 / 认识 / 暂不学习内容
- 互动场景设计
- Quiz
- 常见错误
- 性能意识
- Godot / Blender 真机任务
- 验收标准

统一模板：

[`openmaic/lesson-template.md`](openmaic/lesson-template.md)

## 课堂生成器

OpenMAIC 负责将这些规格生成：

- AI 老师讲解
- Slides
- Quiz
- 3D / Simulation / Game 等互动内容
- AI 同学讨论
- 白板

使用方法：

[`openmaic/generation-guide.md`](openmaic/generation-guide.md)

---

# 项目目录

```text
ai-3d-game-learning/
│
├── curriculum/              # 课程路线、教学设计、真机练习
│   ├── roadmap.md
│   ├── course-design-principles.md
│   └── beginner/
│
├── openmaic/                # OpenMAIC 模板与生成输入
│   ├── lesson-template.md
│   ├── generation-guide.md
│   └── requirements/
│
├── glossary/                # 3D / Godot / Blender / 性能专业词
│
├── game/                    # 真正的 Godot 4 游戏项目
│
└── blender/                 # Blender 原始资产与实验
```

---

# 当前状态

**课程阶段：Foundation v1**

当前优先级不是批量生成全部课程，而是：

1. 验证 B01 的 OpenMAIC 生成效果
2. 实际完成 B01 Godot / Blender 练习
3. 找出过度讲解、互动不足、术语过多等问题
4. 修改课程模板
5. 模板稳定后继续 B02 / B03

这是一个持续迭代的学习工程，而不是一次写完的教材。
