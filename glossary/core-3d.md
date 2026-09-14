# 术语索引：遇到再查，不逐页背诵

完整分级、易混区别、题目与实验见[32概念地图](../curriculum/concept-map.md)。以下只是检索入口。

|看到这个词|先去看|现在先问什么|
|---|---|---|
|Axis / Gizmo / Transform / Scale|C01–C02|是改对象还是网格？相对谁？单位是什么？|
|Local / Global / position / Basis|C03、C28|父空间、自身空间还是世界空间？|
|Origin / Pivot / Hinge|C04|哪个点应保持不动？工具Pivot是否真的改变了对象Origin？|
|Scene / Node / Instance / Resource|C05、C17|节点职责是什么？实例内部资源是否共享？|
|Mesh / Collision / Area / Mask|C06–C07|只负责显示、阻挡还是检测？谁扫描谁？|
|Velocity / Delta / Gravity|C08–C09|这是每秒速度、每帧位移，还是加速度？|
|Camera / FOV / SpringArm|C10|改变观察还是改变世界？镜头会碰到什么？|
|Normal / Bevel / Shade Smooth|C11|改了几何、轮廓还是着色？|
|PBR / Roughness / Metallic|C12|固定光照了吗？是不是拿Metallic当亮度？|
|Emission / Glow / GI / Light|C13、C25|表面亮、光晕还是照亮邻居？|
|UV / Texture / Texel Density|C14、C22|是映射错误还是分辨率不足？|
|glTF / GLB / Import|C15|源资产与导入生成文件，哪里才是编辑源？|
|Signal / State / queue_free|C16|事件和状态属于谁？能否重复触发？|
|Feedback / HUD / Particles|C18|静音、低对比度下还能理解结果吗？|
|FPS / Frame Time / Draw Call / VRAM|C19、C32|实测是什么？条件一致吗？慢帧在哪里？|
|Armature / Skin / AnimationTree|C21|形变、状态还是位移归属出了问题？|
|Navigation / Save / Version|C23–C24|路径是否真的可达？旧数据还能读取吗？|
|Shader / Quaternion / MultiMesh / LOD|C27–C30|当前项目真的遇到这个问题了吗？|
|Authority / Latency|C31|谁决定状态？是否真的需要多人？|

视频搜索方式：`Godot 4 + 精确类名 + 实验目标`，例如“Godot 4 SpringArm3D 相机碰撞”“Blender Object Origin 3D Cursor 区别”。先核对教程版本，避免把Godot 3的Spatial/KinematicBody写法套进4.x。
