# Godot 实战工程：星光小庭院

固定 Godot 4.7.2。这里不再只是概念测试；从本阶段开始，它也是课程主项目的可运行参考实现。

## 当前主场景

`scenes/main.tscn`

目标视觉：**干净的高角度风格化自然世界**。

当前使用原创原生几何搭建第一版：

- 暖土主路。
- 草地与留白。
- 模块小屋。
- 树/石/花的少量簇。
- 柔和暖主光与冷填充。
- 偏高 Roughness 的克制材质。
- 十星收集闭环。
- 固定高角度跟随镜头。

这些几何是“视觉规则验证母体”，后续会被合法购买/自制/二开的真实资产逐步替换。

## 操作

- WASD：移动
- Shift：跑
- Space：跳
- R：重开
- HUD `Visual A/B lab`：打开视觉实验室

当前主线不要求鼠标自由转镜头。

## 视觉 A/B 实验室

`scenes/visual_lab.tscn`

现在先比较三个变量：

- Perspective FOV。
- 主光强度。
- Clean vs extra clutter。

原则：**一次只改一个变量。** 先描述看到什么，再决定保留哪个版本。

后续可逐步加 Fog、Glow、DOF、色彩调整、Hit Stop/Camera impulse 等，但每个效果必须有明确问题和恢复路径。

## 工程边界

当前没有引入第三方美术资源，也没有复制参考游戏的独特内容。参考作品只用于提炼构图、色彩、材质、密度和镜头语言。

课程实战说明：[实战Demo搭建](../curriculum/practical-demo-build.md)

AI协作：[实战AI指挥手册](../curriculum/ai-build-playbook.md)

采购：[素材包采购指南](../art/asset-pack-buying-guide.md)
