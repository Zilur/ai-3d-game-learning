# Godot 游戏项目目录

这里将存放真正可运行的 Godot 4 项目。

## 初级 Demo 目标

最终做出：

- 第三人称玩家
- 走 / 跑 / 跳
- 基础相机
- 灰盒关卡
- 碰撞
- 星星拾取
- UI 计数
- 音效 / 粒子反馈
- 基础灯光与 Environment
- 第一次性能检查

## 推荐目录（项目创建后）

```text
game/
├── project.godot
├── scenes/
│   ├── levels/
│   ├── player/
│   ├── pickups/
│   └── ui/
├── scripts/
├── assets/
│   ├── models/
│   ├── textures/
│   ├── materials/
│   └── audio/
└── resources/
```

## 原则

- 每一课只增加本课需要的功能。
- 不为了“以后可能用”提前建立复杂系统。
- 可调手感参数优先暴露到 Inspector。
- AI 写出的代码必须能说明节点依赖和职责。
- 遇到 Bug 先判断属于：场景结构 / 脚本 / 物理 / 资产 / 渲染 / 导入中的哪一类。
- 每个阶段保留可运行的 Git 节点。
