# Godot 实战工程：星光小庭院

固定 Godot 4.7.2。这里同时保留两种东西，但用途不同：

1. **概念实验室**：小场景、滑杆、A/B，用来理解参数和因果。
2. **正式项目**：`scenes/main.tscn`，按真实生产阶段逐步成长。

详细规则：[概念实验室与正式项目](../curriculum/lab-production-workflow.md)。

## 正式项目当前主场景

`scenes/main.tscn`

目标视觉：**干净的高角度风格化自然世界**。

当前第一版：

- 暖土主路。
- 草地与留白。
- 模块小屋。
- 树/石/花的少量簇。
- 柔和暖主光与冷填充。
- 偏高 Roughness 的克制材质。
- 十星收集闭环。
- 固定高角度跟随镜头。

这些原生几何是代理资产和视觉基线。真实工作流程是：灰盒/逻辑先稳定 → 做一个美术竖切片 → 锁素材母体 → Blender 二开 → 分批替换 → 统一风格 → Set Dressing → 灯光/VFX/动作 → 性能交付。

完整流程：[正式 Demo 搭建](../curriculum/practical-demo-build.md)。

## 操作

- WASD：移动
- Shift：跑
- Space：跳
- R：重开
- HUD `Visual A/B lab`：打开视觉实验室

正式主线不要求鼠标自由转镜头。

## 概念实验室

### `scenes/lab.tscn`
Transform、父/自身/世界空间、门轴等基础概念。

### `labs/collision_roles_lab.tscn`
拖动目标位置并分别关闭：Visual / Collision / Trigger。直观看到：**看得见、挡得住、触发事件是三种不同职责。**

### `labs/motion_lab.tscn`
拖 Speed / Jump Velocity / Gravity；看每秒位移、单步位移和跳跃高度/落地时间。

### `labs/material_lab.tscn`
Roughness / Metallic / Emission 对照；区分材质自发光和真实光源。

### `scenes/visual_lab.tscn`
FOV、主光和 Clean / Clutter 对照。用来训练固定视角构图和干净度判断。

实验目录说明：[labs/README](labs/README.md)。

## 工程边界

当前没有把商业参考的独特角色、关卡或资产复制进仓库。参考只用于提炼构图、色彩、材质、密度和镜头语言。

AI协作：[实战AI指挥手册](../curriculum/ai-build-playbook.md) · 采购：[素材包采购指南](../art/asset-pack-buying-guide.md)
