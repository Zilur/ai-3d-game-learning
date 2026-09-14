# 技术事实校核与版本边界

核对日期：2026-09-14。优先官方文档，不从AI生成的课件反推API事实。stable/latest页面会变化，正式试教要记录实际安装版本与渲染器。

|编号|对应概念|官方来源|核对重点|
|---|---|---|---|
|S01|C03/C04|[Godot Node3D](https://docs.godotengine.org/en/stable/classes/class_node3d.html)|父空间与object-local不同；position/global_position；角度API注意弧度|
|S02|C08/C09|[CharacterBody3D](https://docs.godotengine.org/en/stable/classes/class_characterbody3d.html)|velocity为速度，move_and_slide使用物理delta；落地来自上次移动|
|S03|C06/C07/C16|[Area3D](https://docs.godotengine.org/en/stable/classes/class_area3d.html)|monitoring、Mask、body_entered和重叠更新|
|S04|C10|[Spring arm tutorial](https://docs.godotengine.org/en/stable/tutorials/3d/spring_arm.html)|第三人称镜头检测与相机父子结构|
|S05|C12/C13/C14|[StandardMaterial3D教程](https://docs.godotengine.org/en/stable/tutorials/3d/standard_material_3d.html)|金属/粗糙度、Emission、Normal Map不改几何|
|S06|C15|[Blender glTF](https://docs.blender.org/manual/en/latest/addons/scene_gltf2.html)|glTF材质支持不是Blender任意节点树等价导出|
|S07|C02/C15|[Blender Apply](https://docs.blender.org/manual/en/latest/scene_layout/object/editing/apply.html)|应用变换的语义，动画/关系影响需检查|
|S08|C04|[Blender Object Origin](https://docs.blender.org/manual/en/latest/scene_layout/object/origin.html)|对象原点与操作支点区别|
|S09|C19/C29/C30/C32|[Godot性能文档索引](https://docs.godotengine.org/en/stable/tutorials/performance/index.html)|测量和瓶颈意识；高级具体方案须再查对应章节|
|S10|平台输入|[OpenMAIC generate-flow](https://github.com/THU-MAIC/OpenMAIC/blob/main/skills/openmaic/references/generate-flow.md)|requirement、支持字段、能力检测、任务提交不等于成功|
|S11|版本|[Godot archive](https://godotengine.org/download/archive/)|选择正式版本，而不是把开发版当必需条件|

本次不做模型排名、不锁定某API供应商、不要求最新版独有渲染特性。Godot源码以4.5+的4.x API为目标，但未在本轮执行引擎，不据此宣称所有4.x均兼容。

课程中的复习间隔、7/8晋级规则、每段概念数量是本项目试教策略，不是已验证的普适阈值。与“市面上没有”有关的市场唯一性未调查，因此不作此断言。
