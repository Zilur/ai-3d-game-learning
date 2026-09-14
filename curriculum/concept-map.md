# 概念分级与复现地图

M = 必须掌握：预测 + 实操/排错 + 迁移。K = 应该了解：用途 + 风险 + 查询入口。

一个编号代表一个可以验收的概念簇，而不是要求把所有相关 API 背下来。初级只学习 C01–C20 的 M；C21–C26 在初级均为 K，在对应中级课升为 M。K01–K12 本版始终是 K。

每个 C 编号对应 [题库](../assessment/question-bank.md) 的 `-P` 预测、`-R` 实操排错、`-T` 迁移题。K 编号各有一道用途判断题。答案在独立文件中。

## 核心概念

| ID | 概念 / 专业词 | 初级→中级 | 可验收的能力 | 首次→复现→综合 |
|---|---|---|---|---|
| C01 | Axis、Position/Location、Rotation、Scale、Transform、尺寸/单位 | M→M | 把物体移动、转向、拉长分别对应到参数；不把 Scale=1 当成一米 | B01→B07/B09→B15 |
| C02 | Parent Space、Object Local、Global/World、父子变换 | M→M | 区分父节点坐标、自己朝向和世界方向，解释同一个数字的不同位移 | B01/B02→B06→B10/B16 |
| C03 | Origin、Pivot、Object Mode、Edit Mode | M→M | 比较门绕中心/铰链；分清改对象变换与改几何；知道 Origin≠任意操作中心 | B01→B07→I04 |
| C04 | Node、Scene、Node3D、MeshInstance3D、Instance、节点职责 | M→M | 读懂场景树，把显示、碰撞、逻辑分开；复制实例不等于新建完全独立资源 | B02→B10→I03 |
| C05 | Mesh≠Collision、StaticBody3D、CharacterBody3D、CollisionShape3D | M→M | 看得见但穿过去时检查物理；选择简单 Box/Capsule 等形状 | B04→B05→B15 |
| C06 | Collision Layer/Mask、检测方向 | M→M | 说明“我在哪层”和“我要检测谁”；检查 Area 的 mask 与玩家的 layer | B04→B10→I04 |
| C07 | Input Action/InputMap、Velocity、Speed、Delta、physics tick | M→M | 预测速度/时间关系；防对角加速；不把 Godot 4 move_and_slide 的 velocity 再乘 delta | B03→B05→B14 |
| C08 | Gravity、Grounded、Jump、Slope、Floor | M→M | 区分起跳速度与持续加速度；证明落地判断；不把普通角色控制器当自动爬楼梯 | B05→B06→B15 |
| C09 | Camera3D、FOV、Yaw/Pitch、SpringArm3D、相机阻挡 | M→M | 固定位置比较 FOV；检查近墙遮挡、灵敏度和眩晕反馈 | B06→B13→B16 |
| C10 | Mesh 的 Vertex/Edge/Face、Normal、Bevel、平滑着色 | M→M | 用轮廓和受光区分几何与着色；低成本修法线而非盲加面 | B07→B09→B15 |
| C11 | glTF/GLB、Import/Reimport、Apply Scale、源资产与运行资产 | M→M | 用尺度参照物验导入；重导保留游戏逻辑；不盲目 Apply All 到绑定角色 | B07/B09→B15→I11 |
| C12 | Material、PBR、Base Color/Albedo、Metallic、Roughness | M→M | 固定光照改变粗糙度；区分粗糙与暗；均一金属/非金属优先理解端点 | B08→B13→B16 |
| C13 | Emission、灯光、Glow/Bloom、GI 的边界 | M→M | 区分自己亮、出现光晕、照亮邻物；不承诺只有 Emission 就全实现 | B08→B11/B13→B15 |
| C14 | Texture、UV、Normal Map、贴图尺寸 | M→M | 用格子发现拉伸；说明法线贴图不增加轮廓/碰撞；识别大纹理成本 | B08/B09→I05→B15 |
| C15 | Area3D、Signal、Group、事件、queue_free、一次性拾取 | M→M | 把触发与阻挡区分；让重复回调也只计数一次 | B10→B12→B16 |
| C16 | State、HUD/Control/Label、单一事实来源、Reset | M→M | UI 从游戏状态更新；证明最后一个拾取和重开没有残留 | B12→B15→B16 |
| C17 | Feedback、Audio、Tween、Particles、生命周期 | M→M | 做视觉/声音互补反馈；避免拾取物删除时把声音一起截断 | B11→B12→B16 |
| C18 | Light、WorldEnvironment、Shadow、Exposure、Fog、可读性 | M→M | 一次改一个画面变量；区分客观可读性与个人偏好 | B13→B14→I06 |
| C19 | FPS、Frame Time、Profiler、CPU/GPU、目标设备与预算 | M→M | 同机同路径 A/B 测量；知道60 FPS≈16.7ms；不拿截图估性能 | B03/B14→I07→I11 |
| C20 | 最小复现、版本回退、范围控制、资产授权、密钥安全 | M→M | 保存基线再修改；报告可复现证据；发布前检查来源和秘密信息 | B02→B09/B15→I11 |
| C21 | Rig/Armature、Bone、Skin/Weight、Skeleton、动画状态与 Blend | K→M | 导入角色并区分碰撞移动、模型朝向、动画播放；检查穿插/滑步 | I01→I02→I12 |
| C22 | PackedScene、Resource、共享资源、Composition、职责边界 | K→M | 证明改一个实例不会意外改变全部；用事件解耦而不过度架构 | I03→I09→I12 |
| C23 | Modular Asset、Grid/Snap、门/机关状态、RayCast | K→M | 统一接缝与碰撞；用明确状态限制机关重复触发 | I04→I05→I12 |
| C24 | NavigationMesh、NavigationAgent3D、路径与物理障碍 | K→M | 区分可走导航区域与碰撞；复现不可达目标并处理 | I08→I09→I12 |
| C25 | Save、Settings、Input Remap、Export、目标平台验收 | K→M | 设置可恢复，存档有版本；在非开发环境验证一个发布包 | I10→I11→I12 |
| C26 | LOD、Occlusion Culling、MultiMesh/绘制实例化 | K→M | 为大量对象选择一种经测量有效的优化，并说明裁剪/灵活性代价 | I07→I11→I12 |

## 应该了解的补充概念

| ID | 概念 | 认识到什么程度 | 何处出现 / 查证入口 |
|---|---|---|---|
| K01 | Gizmo、Translation、Transform orientation | 看懂操作器，知道 Translation 指平移；方向设置不等于旋转中心设置 | B01；Blender/Godot 空间文档 |
| K02 | Euler、Quaternion、Basis、Matrix | 知道复杂旋转需要专门表示；不手推公式，不把度直接塞进弧度参数 | B01/B06；Node3D |
| K03 | Convex/Concave Collision、RigidBody3D | 分清动态刚体和角色控制；高精度网格碰撞不是默认答案 | B04；Godot 物理文档 |
| K04 | BRDF、Principled BSDF、Shader | 知道是表面光照/材质实现，不作为初级推导内容 | B08；材质文档 |
| K05 | AO、GI、Lightmap、Reflection Probe | 知道阴影、间接光和反射不是同一个效果；支持范围依赖渲染器 | B13/I06；渲染文档 |
| K06 | Draw Calls、Triangle Count、VRAM | 能把它们当线索，而非凭某个固定上限给所有游戏判死刑 | B14；Profiler/渲染文档 |
| K07 | Texel Density、Decal、Trim Sheet | 知道用于清晰度一致/局部细节/重复贴图，不要求初级搭完整管线 | I05；资产管线资料 |
| K08 | Root Motion、Retargeting | 识别动画驱动位移与骨架重定向；不是加一段移动代码就完成 | I02；动画文档 |
| K09 | HLOD、Streaming、分块 | 知道处理大范围资源与可见性；小房间不先做开放世界架构 | I07；优化资料 |
| K10 | Anti-aliasing、MSAA、色彩管理 | 能识别锯齿/色彩显示差异；不把两个软件默认画面当严格同条件比较 | B09/B13；渲染设置 |
| K11 | Accessibility、Readability、对比度 | 知道反馈不能只靠一种颜色或声音；先能玩懂再加装饰 | B11/B13；用户测试 |
| K12 | License、Attribution、API Provider | 能找到许可证/署名要求；知道本地平台调用云模型仍会发送请求内容 | B02/B09；原始服务与素材条款 |

## 复现不是重播

使用首次对象之外的对象、不同数值或不同症状。`C02-P` 答对后，后续应做 `C02-R/T`，而不是连续重复同一句定义。复现安排按 [掌握规则](../assessment/mastery-policy.md)记录。

本表不等于“整门 3D 学科的所有概念”。新增战斗、网络或复杂绑定前，应另立范围与分级，不悄悄塞入初级。
