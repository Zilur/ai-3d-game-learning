# 技术来源与学习边界

核对日期：2026-09-14。优先官方资料；stable/latest会变化，试教应记录实际软件版本与渲染器。这里是查证入口，不是必读书单。

|编号|概念|官方来源|核对用途|
|---|---|---|---|
|S01|C03/C04|[Godot Node3D](https://docs.godotengine.org/en/stable/classes/class_node3d.html)|父空间、自身方向、世界位置不同；不把学习目标扩大为矩阵推导|
|S02|C08/C09|[CharacterBody3D](https://docs.godotengine.org/en/stable/classes/class_characterbody3d.html)|velocity是速度；不要重复乘delta；落地来自物理移动结果|
|S03|C06/C07/C16|[Area3D](https://docs.godotengine.org/en/stable/classes/class_area3d.html)|monitoring、Mask、body_entered与检测更新|
|S04|C10|[SpringArm教程](https://docs.godotengine.org/en/stable/tutorials/3d/spring_arm.html)|第三人称镜头障碍检测，不需自己实现完整算法|
|S05|C12/C13/C14|[StandardMaterial3D](https://docs.godotengine.org/en/stable/tutorials/3d/standard_material_3d.html)|常用参数、Emission与表面细节的实际含义|
|S06|C15|[Blender glTF](https://docs.blender.org/manual/en/latest/addons/scene_gltf2.html)|格式支持不等于Blender任意节点树原样导出|
|S07|C02/C15|[Blender Apply](https://docs.blender.org/manual/en/latest/scene_layout/object/editing/apply.html)|变换应用与对象关系，静态小资产不能代表所有角色流程|
|S08|C04|[Object Origin](https://docs.blender.org/manual/en/latest/scene_layout/object/origin.html)|对象原点与操作支点的区别|
|S09|C19/C32|[优化与测量](https://docs.godotengine.org/en/stable/tutorials/performance/general_optimization.html)|识别瓶颈、对照和再测，不盲目优化所有内容|
|S10|OpenMAIC输入|[官方生成流程](https://github.com/THU-MAIC/OpenMAIC/blob/main/skills/openmaic/references/generate-flow.md)|内容要求与API字段分开，提交任务不等于成功|
|S11|版本|[Godot archive](https://godotengine.org/download/archive/)|固定实际使用版本，不要求追开发版|
|S12|C17|[Godot Resources](https://docs.godotengine.org/en/stable/tutorials/scripting/resources.html)|资源共享是日常参数修改必须验收的影响范围，不需学习缓存源码|

本轮重点重新核对S01/S02/S09/S12来界定“必须懂的行为”和“不必深入的实现”。其余为既有官方参考入口，不声称本轮全部逐条重新验证。

这些资料支持技术事实，不证明教学效果。M90/K10、M至少72分和微单元大小是本项目试教选择，不是普适研究定律。所有技术学习停止线见[学习合同](../curriculum/learning-contract.md)。

Godot工程仍是参考源码，不据文档可查就宣称本分支已在全部Godot4版本运行。不同分支的引擎测试结果不能混用；具体状态见[validation.md](validation.md)。
