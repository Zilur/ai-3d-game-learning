# Blender共享起始文件

[直接打开与操作说明](../../LABS-START.md) · [逐课对应](../../curriculum/practical-resource-audit.md)

直接打开现成`.blend`，先另存副本。运行基线Blender5.2 LTS；本轮作者检查固定5.2.0。无需插件、密钥或另找网络模型。

- `transform_origin_lab.blend`：中心/侧边门轴、静态变换与尺度。
- `kitbash_style_lab.blend`：Base/Variant小屋、比例、部件、风格统一；不要求从零建模。
- `uv_material_lab.blend`：内嵌棋盘格，正常/拉伸/密度对照，真实共享/独立网格和材质。
- `animation_fixture.blend`：原创5骨骼蒙皮小人，Idle/Walk/Attack片段与NLA；不要求先绑骨架。

新文件有中文说明文本。原有场景的英文对象名是定位标记，不考记忆。按实际软件轴向观察；Blender预览或渲染不等同于Godot成品效果。

`build_labs.py`与`build_practical_labs.py`是**作者复建/验证工具**，不是孩子开始课程的步骤。新增构建器会将同一原创角色导出`game/assets/practice_robot_roundtrip.glb`，为往返检查提供已完成样本；真正改动后的项目仍由学员验收。所有样本保留源，软件课程完成不代表正式美术库已完成。
