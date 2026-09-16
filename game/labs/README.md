# Godot 概念实验室

这里的场景是为了**理解概念和拖参数看因果**，不是正式游戏架构。

原则：

- 每个实验只暴露少量关键变量。
- 必须能复位或重新运行回到基线。
- 允许使用很人工的教学场景。
- 实验结论最终要回正式项目做迁移验证。

当前实验：

- `material_lab.tscn`：Roughness / Metallic / Emission；Emission、Glow、Light 的边界。
- `collision_roles_lab.tscn`：Visual / Collision / Trigger 三种职责，拖目标位置观察角色被墙挡住或进入 Trigger。
- `motion_lab.tscn`：Speed / Jump Velocity / Gravity，直接看每秒位移和跳跃曲线。

另外：

- `../scenes/lab.tscn`：Transform、父/自身/世界空间、门轴和基础材质概念。
- `../scenes/visual_lab.tscn`：FOV、主光和 Clean/Clutter 对照。

**实验通过不等于正式项目完成。** 正式项目流程见 `../../curriculum/lab-production-workflow.md`。
