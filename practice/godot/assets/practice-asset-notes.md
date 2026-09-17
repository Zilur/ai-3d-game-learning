# 原创教学角色与回导样本

`practice_robot.gltf`由`tools/assets/make_practice_robot.py`用原创方块几何生成；没有使用第三方角色、动作捕捉或参考作品的资产。含5个关节、明确权重和Idle/Walk/Attack三段原创参数动作。随本课程允许学习、修改与复用；不要把它宣传成专业美术或通用人体骨架。

`practice_robot_roundtrip.glb`是同一模型通过Blender5.2.0导入后再导出的样本。编辑源是`practice/blender/animation_fixture.blend`，可对照骨骼、蒙皮、NLA片段；不要编辑Godot的`.godot`缓存。

尺寸、轴向、片段和共享状态由实际导入检查。没有承诺这些骨骼能直接接受任意外部动作；正式角色/动作来源和许可仍由使用者核对。没有把原地Walk当成控制器位移，也没有把一张静态图当成动作成功。
