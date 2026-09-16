# Blender 实验与正式资产二开

这里不把 Blender 教成“从零建模百科”。本项目主要训练：**看懂基底 → 改比例/Origin/模块 → 统一配色和材质 → 导出 → 回 Godot 玩家机位验收。**

## 两类文件

### 1. `labs/`：概念实验室

用于拖参数看现象，可以很教学化。

- `transform_origin_lab.blend`：中心 Origin / 侧边 Origin、旋转门轴、Applied / Unapplied Scale。
- `kitbash_style_lab.blend`：基础小屋和二开变体；练比例、模块替换、材质 Base Color / Roughness 和细节密度。
- `build_labs.py`：两份 `.blend` 的可重建源。学员不需要背 Python。

这些实验文件不是正式项目资产库。

### 2. 正式项目资产

正式资产进入项目时按真实流程：

**来源/许可 → 游戏用途与镜头 → 大形比例 → Origin/尺度/朝向 → Kitbash/模块替换 → 配色 → 材质 → 有限细修 → 导出 GLB → Godot 固定机位验收 → 回归功能。**

不要因为实验里可以随便 Apply Transform，就在绑定角色上盲目 Apply；角色/动作单独走兼容与重定向流程。

## 概念实验怎么用

先预测，再只改一个东西。

### Transform / Origin

打开 `labs/transform_origin_lab.blend`：

- 选择 `Door_Center` 和 `Door_Hinge`，分别拖 `Rotation Z`。
- 看同样的门为什么旋转轨迹不同。
- 比较 `Scale_Unapplied` 与 `Scale_Applied` 的 Object Scale 和 Dimensions。
- 最后用自己的门模块做一次迁移，不把实验场景当正式资产。

### Kitbash / Style

打开 `labs/kitbash_style_lab.blend`：

- 先比较 `Base_*` 与 `Variant_*`。
- 只改一项：屋顶比例、门窗模块、墙体颜色或 Roughness。
- 在相同 Camera 下比较，不同时改灯光和几何。
- 觉得“更精致”时仍要问：缩到游戏距离看得到吗？是不是反而更杂？

## 正式项目怎么替换素材

不要一次导入一整套然后全地图替换。

1. 先导入一棵树、一栋小屋、一块石头。
2. 在 Blender 做第一轮二开。
3. 导出 GLB。
4. 在 Godot 同一机位 A/B。
5. 检查碰撞、路径、星星和材质共享。
6. 三件都能统一后才扩大。

正式工作流见 [概念实验室与正式项目](../curriculum/lab-production-workflow.md) 和 [实战 Demo](../curriculum/practical-demo-build.md)。

## 版本

课程实验文件固定用 **Blender 5.2 LTS** 系列生成；生成脚本记录具体 patch 版本。LTS 的目的不是追最新功能，而是让实验文件和二开流程稳定可复现。

`create_star.py` 仍保留作早期静态资产往返示例；它不是正式项目的最终美术生产方式。
