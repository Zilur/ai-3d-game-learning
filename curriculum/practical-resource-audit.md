# 逐课配套核对：47课共用少量真实实验

[直接打开现成实验](../LABS-START.md)。此表与各课0A、对话1及家庭会话共用一个BINDINGS源；不另造课号。

本表是材料与路径审查，不是所有M已通过、所有课已试教或游戏已完成。实验只覆盖明确切片；真实工程迁移按原M检查。

|课号/主题|建议主要环境|现成文件|先做的一件事|仍须注意的边界|
|---|---|---|---|---|
|[A01 美术对话：把唯美、卡通说具体](lessons/A01.md)|参考/概念讨论；所选专项另备实际样本|本课不需要专用3D文件，或专项按需|从自己提供的参考中选一个可见特征，说出借鉴与不借鉴什么。|参考分析，无软件Lab门槛；没有图不捏造作品内容。|
|[A02 空间入门：位置、旋转、缩放](lessons/A02.md)|OpenMAIC先理解；Godot真实对照|[lab.tscn](../game/scenes/lab.tscn)|固定父空间，只改对象Position的一个轴，再恢复。|空间子实验；不一次操作所有模式。|
|[A03 场景、节点与实例：先搭灰盒](lessons/A03.md)|OpenMAIC先理解；Godot真实对照|[starter.tscn](../game/lessons/b02/starter.tscn)、[broken.tscn](../game/lessons/b02/broken.tscn)|打开现成starter，选中模块整体和外观子节点分别观察；再另存副本改一项。|这是A03的真实起点与故障对照；历史目录名b02不代表当前B02，不先读reference答案。|
|[A04 看得见、挡得住、能检测是三回事](lessons/A04.md)|OpenMAIC先理解；Godot真实对照|[collision_roles_lab.tscn](../game/labs/collision_roles_lab.tscn)|把角色目标移到墙另一侧，分别切换外观和阻挡；复位后再切检测角色/装饰。|真实Area与物理；改Mask后让角色或白色装饰重新进入，分别验证谁被检测。不是只由M1替M2。|
|[A05 走与跑：输入、速度和时间](lessons/A05.md)|OpenMAIC先理解；Godot真实对照|[motion_lab.tscn](../game/labs/motion_lab.tscn)、[main.tscn](../game/scenes/main.tscn)|在现成运动Lab只改速度，比较相同时间位移；再在主游戏检查直走/斜走。|Lab是简化运动模型；真实控制器、帧率差异与碰撞在提供的主游戏副本和实际运行条件中检查。|
|[A06 跳跃：调手感而不是背公式](lessons/A06.md)|OpenMAIC先理解；Godot真实对照|[motion_lab.tscn](../game/labs/motion_lab.tscn)、[main.tscn](../game/scenes/main.tscn)|固定重力只改起跳速度，按跳跃观察；用“仅回到起点”重播对照。|恢复全部初值会复位参数和控件，重播保留参数；边缘/墙边真实落地仍在主游戏检查。|
|[A07 相对谁：父空间、自身方向和门轴](lessons/A07.md)|OpenMAIC先理解；Godot/Blender各验相关部分|[lab.tscn](../game/scenes/lab.tscn)、[transform_origin_lab.blend](../blender/labs/transform_origin_lab.blend)|任选门轴实验，闭门位置相同，再分别观察中心/侧边旋转。|Godot与Blender坐标轴不同，按文件实际轴观察，不背同一个轴名。|
|[A08 固定/有限镜头：构图舒服，移动清楚](lessons/A08.md)|OpenMAIC先理解；Godot真实对照|[camera_lab.tscn](../game/labs/camera_lab.tscn)、[main.tscn](../game/scenes/main.tscn)|在镜头Lab保持其他条件，只切透视/正交，分别比较FOV/Size；再试向右移动。|真实Camera3D投影和地面方向；没有完整分区切镜或事件镜头，未选这些增强不增加作业。|
|[B01 训练眼睛一：剪影、比例和细节层级](lessons/B01.md)|Blender现成副本|[kitbash_style_lab.blend](../blender/labs/kitbash_style_lab.blend)|固定视图先比较Base与Variant大形，不先画纹理。|小屋比例示例，不是商业品质标杆。|
|[B02 Blender静态资产：先会验收，再谈从零造型](lessons/B02.md)|Blender现成副本|[transform_origin_lab.blend](../blender/labs/transform_origin_lab.blend)、[kitbash_style_lab.blend](../blender/labs/kitbash_style_lab.blend)|直接打开现成静态样本，在副本中比较对象变换与网格编辑；再选小屋轮廓。|原点/缩放样本已给；平滑/倒角局部对照可在副本用现有方块作一次设置，不要求从零搭模型。|
|[B03 训练眼睛二：明度、色相、饱和度与焦点](lessons/B03.md)|Blender现成副本|[kitbash_style_lab.blend](../blender/labs/kitbash_style_lab.blend)|固定机位光照，只调整变体一处颜色，先看焦点和大色块。|原生材质参数练习，不自带自动色彩评分器。|
|[B04 材质四个判断：颜色、粗糙、金属、共享](lessons/B04.md)|OpenMAIC先理解；Godot/Blender各验相关部分|[material_lab.tscn](../game/labs/material_lab.tscn)、[uv_material_lab.blend](../blender/labs/uv_material_lab.blend)|保持灯光不动，先只改左球粗糙度；复位后切换共享材质，再改一次。|双球可切真实共享/独立资源，自发光与实际光源可分开；不把自发光球当环境照明或Glow已实现。|
|[B05 资产往返：源文件改了，游戏别被改坏](lessons/B05.md)|OpenMAIC先理解；Godot/Blender各验相关部分|[kitbash_style_lab.blend](../blender/labs/kitbash_style_lab.blend)、[main.tscn](../game/scenes/main.tscn)|在副本中选一个静态部件导出，再接到自己的游戏视觉包装。|给出源样本与参考工程；学员GLB往返、原点与功能保持仍须实际做。|
|[B06 拾取只算一次：事件、条件与状态](lessons/B06.md)|OpenMAIC先理解；Godot真实对照|[event_lab.tscn](../game/labs/event_lab.tscn)、[main.tscn](../game/scenes/main.tscn)|在事件Lab先发一次正确对象请求，再发错误对象和同帧双请求，比较计数。|按钮注入事件用于时序与状态实验，不伪称鼠标点击就是Area碰撞；真实拾取在主游戏，故障开关不带到成品。|
|[B07 反馈：让玩家知道刚才成功了](lessons/B07.md)|OpenMAIC先理解；Godot真实对照|[event_lab.tscn](../game/labs/event_lab.tscn)、[main.tscn](../game/scenes/main.tscn)|在事件Lab切换可见反馈，比较成功计数和显示；再观察主游戏真实拾取。|现成反馈与规则分离；本Lab未提供完整音频/粒子/打击感库，不以反馈关掉判规则失败。|
|[B08 UI、完成和重开：状态只有一个来源](lessons/B08.md)|OpenMAIC先理解；Godot真实对照|[event_lab.tscn](../game/labs/event_lab.tscn)、[main.tscn](../game/scenes/main.tscn)|先在事件Lab完成、重开并再次请求，再在主游戏改变窗口检查布局。|事件Lab有独立状态和显示、可重复重开；主游戏的完整十星与窗口布局仍分别实测。|
|[B09 柔和光照：先让目标被看见](lessons/B09.md)|OpenMAIC先理解；Godot真实对照|[visual_lab.tscn](../game/scenes/visual_lab.tscn)|固定FOV，只改主光强度，对照亮面、暗部和目标。|光强样例，不包含所有环境光/阴影配置。|
|[B10 看大师不只收藏：从参考到观察再到变式](lessons/B10.md)|OpenMAIC先理解；Godot真实对照|[visual_lab.tscn](../game/scenes/visual_lab.tscn)|将一条参考规则用于同机位对照，解释为什么不继续加细节。|参考来源由学员提供；Lab是原创示意，不是假大师截图。|
|[B11 性能入门：先测，再判断要不要优化](lessons/B11.md)|已有游戏参考/自己的工程/目标设备|[main.tscn](../game/scenes/main.tscn)|记录实际设备/分辨率/路线，再测一次基线，不先盲目优化。|不自带已验证性能收益；结果来自你的设备。|
|[B12 验收AI改动：小假设、小修改、可回退](lessons/B12.md)|OpenMAIC先理解；Godot真实对照|[broken.tscn](../game/lessons/b02/broken.tscn)、[event_lab.tscn](../game/labs/event_lab.tscn)、[main.tscn](../game/scenes/main.tscn)|先在现成故障副本说明实际现象，再提出一个可能原因和最小验证，不先读答案。|可用A03故障或事件防重故障练排查；工程diff/版本恢复仍用自己的修改记录，不能自动判会。|
|[B13 初级结业：把星星换成另一种可用物品](lessons/B13.md)|已有游戏参考/自己的工程/目标设备|[main.tscn](../game/scenes/main.tscn)|沿本课任务换一种可用物品，先写允许改与必须保留项。|完整参考用于比较；检查使用自己的快照和未揭示变式。|
|[C01 小地图扩展：用固定镜头串起可探索路线](lessons/C01.md)|已有游戏参考/自己的工程/目标设备|[main.tscn](../game/scenes/main.tscn)|先画主路与返回路径，用代理块在副本扩一个区域。|当前主场景不是已完成的庭院/林路/观景台三段地图。|
|[C02 世界美化：镜头决定世界，套装统一风格](lessons/C02.md)|OpenMAIC先理解；Godot真实对照|[visual_lab.tscn](../game/scenes/visual_lab.tscn)|只切换Clutter，指出焦点、路径和留白变化。|密度样例；不包含全套视差/背景层实现。|
|[C03 接入现成角色：会选、会替换、会验收](lessons/C03.md)|OpenMAIC先理解；Godot/Blender各验相关部分|[animation_lab.tscn](../game/labs/animation_lab.tscn)、[animation_fixture.blend](../blender/labs/animation_fixture.blend)、[main.tscn](../game/scenes/main.tscn)|先打开原创动作样本查看骨架、蒙皮、三段片段，再比较角色大小与控制器职责。|原创教学角色与实际动画现成可用；不是正式美术选型或通用骨架兼容保证，替换自己的角色还需验证。|
|[C04 动画状态：动作片段如何接起来](lessons/C04.md)|OpenMAIC先理解；Godot/Blender各验相关部分|[animation_lab.tscn](../game/labs/animation_lab.tscn)、[animation_fixture.blend](../blender/labs/animation_fixture.blend)|在动作Lab只调待机到行走的融合值和过渡时间，观察肢体而非读源码。|真实AnimationTree与导入片段；Walk原地播放，主游戏移动/动画同步和脚滑验收仍需接到自己的控制器。|
|[C05 复用与资源：共享什么、独立什么](lessons/C05.md)|OpenMAIC先理解；Godot/Blender各验相关部分|[material_lab.tscn](../game/labs/material_lab.tscn)、[uv_material_lab.blend](../blender/labs/uv_material_lab.blend)、[starter.tscn](../game/lessons/b02/starter.tscn)|先切Godot材质共享/独立，再在Blender检查Shared_A/B与Independent_C的数据引用。|提供真实材质和网格共享对照；动画引用及独立运行状态在实际角色实例中另验，不用一个静态图包办。|
|[C06 门与移动平台：复用已会的空间和状态](lessons/C06.md)|OpenMAIC先理解；Godot真实对照|[interaction_lab.tscn](../game/labs/interaction_lab.tscn)、[platform_lab.tscn](../game/labs/platform_lab.tscn)|先在门实验观察靠近与开门；需要平台变式时，打开平台实验比较站立跟随和起跳离开。|门与平台均已可交互；平台是实际独立CharacterBody与AnimatableBody，完整机关阻挡/关卡集成仍需实际项目验证。|
|[C07 模块拼接与简单UV：统一尺度和纹理密度](lessons/C07.md)|Blender现成副本|[uv_material_lab.blend](../blender/labs/uv_material_lab.blend)、[kitbash_style_lab.blend](../blender/labs/kitbash_style_lab.blend)|打开UV样本，上排几何和光照相同，先观察棋盘格；只调整中间板的UV，不改几何尺寸。|纹理已打包，正常/拉伸/密度样本现成；模块连接用小屋部件，复杂角色UV不列入当前必修。|
|[C08 风格化光照方案：效果必须能进游戏](lessons/C08.md)|OpenMAIC先理解；Godot真实对照|[visual_lab.tscn](../game/scenes/visual_lab.tscn)、[material_lab.tscn](../game/labs/material_lab.tscn)、[camera_lab.tscn](../game/labs/camera_lab.tscn)|在现成同机位样本中先比较光照、材质或投影的一项，再核对实际渲染器。|提供实际渲染基线；Fog/Glow/DOF等候选仍按目标渲染器另试，不假装全套效果控件已配齐。|
|[C09 优化入口：知道什么时候该停](lessons/C09.md)|已有游戏参考/自己的工程/目标设备|[main.tscn](../game/scenes/main.tscn)|对同一构建/机位选择一项真实测量，不改多种设置。|基准由目标设备提供，headless不代表GPU画面性能。|
|[C10 可交互对象：提示、条件和结果](lessons/C10.md)|OpenMAIC先理解；Godot真实对照|[interaction_lab.tscn](../game/labs/interaction_lab.tscn)|拖动角色接近蓝区，先不拿钥匙尝试开门，再只改变钥匙条件。|真实检测/允许条件/门状态/提示分离，重复开门可验证；不含背包或完整正式关卡系统。|
|[C11 存档与设置：能恢复比能写入更重要](lessons/C11.md)|OpenMAIC先理解；Godot真实对照|[interaction_lab.tscn](../game/labs/interaction_lab.tscn)|在门实验先保存门进度与偏好，再改临时位置、门或偏好，按读取观察哪些恢复。|真实专用本地文件，可准备缺失/坏档/v0旧档；恢复初值不删文件，只能删除本实验档，不代表正式游戏存档已接入。|
|[C12 交付：别人电脑上第一次运行](lessons/C12.md)|已有游戏参考/自己的工程/目标设备|[main.tscn](../game/scenes/main.tscn)|核对目标平台和当前导出条件，再生成自己的可运行包。|有项目源码不等于已给出跨平台成品包。|
|[D01 资产套装二开：从基底拼装成自己的道具](lessons/D01.md)|Blender现成副本|[kitbash_style_lab.blend](../blender/labs/kitbash_style_lab.blend)|先另存副本，选Variant_Roof只改一项比例，比较Base。|原创几何二开样例，不是已购买的完整资产套装。|
|[D02 风格统一：配色、材质、边缘与细节密度](lessons/D02.md)|OpenMAIC先理解；Godot/Blender各验相关部分|[kitbash_style_lab.blend](../blender/labs/kitbash_style_lab.blend)、[material_lab.tscn](../game/labs/material_lab.tscn)|固定光照，先统一一件变体色彩，再单独调粗糙度。|支持局部材质观察，不等于整库风格已经统一。|
|[D03 长期资产库：主套装、基底、变体与组合规则](lessons/D03.md)|Blender现成副本|[kitbash_style_lab.blend](../blender/labs/kitbash_style_lab.blend)|为一件变体记录源、用途、版本、引用和预览机位。|样例不自带完整商业资产库，按本地实际资源建立。|
|[D04 美术结业：用套装二开拼出自己的童话场景](lessons/D04.md)|OpenMAIC先理解；Godot/Blender各验相关部分|[kitbash_style_lab.blend](../blender/labs/kitbash_style_lab.blend)、[main.tscn](../game/scenes/main.tscn)|挑一个小区域组合已合格部件，固定机位做减法。|当前文件只是起点，不是已验收美术结业作品。|
|[D05 动作资源复用：动作包兼容、重定向与融合](lessons/D05.md)|OpenMAIC先理解；Godot/Blender各验相关部分|[animation_fixture.blend](../blender/labs/animation_fixture.blend)、[animation_lab.tscn](../game/labs/animation_lab.tscn)|先直接播放原创角色的三段现成片段，观察骨骼/网格关系，再到Godot比较导入和融合。|有真实骨架、蒙皮与动作；不是外部动作库或通用重定向，新角色仍先做一段兼容小试。|
|[D06 轻战斗融入：现成攻击动作与可重复训练木桩](lessons/D06.md)|OpenMAIC先理解；Godot真实对照|[animation_lab.tscn](../game/labs/animation_lab.tscn)、[main.tscn](../game/scenes/main.tscn)|先播放一次攻击并中断，比较目标在内/在外与重复输入下的命中次数。|现成窗口/距离/一次性规则实验；未把攻击接入主游戏控制器，关闭训练角后的十星回归仍要自己集成后验证。|
|[D07 精致Demo结业：完整探索关卡与可选训练角](lessons/D07.md)|已有游戏参考/自己的工程/目标设备|[main.tscn](../game/scenes/main.tscn)|按已选范围检查自己的完整构建和真实试玩，不增新玩法。|现有参考不代表精致三段地图已完成。|
|[E01 导航选修：画得出路径还要走得到](lessons/E01.md)|参考/概念讨论；所选专项另备实际样本|本课不需要专用3D文件，或专项按需|有真实寻路需要时，先分清可画路径与角色能通过。|导航选修无专用Lab，不阻塞基础版。|
|[E02 高级测量：用证据决定技术投入](lessons/E02.md)|已有游戏参考/自己的工程/目标设备|[main.tscn](../game/scenes/main.tscn)|先固定实际设备与构建，定义要解决的一个性能问题。|参考场景不是通用性能测试集。|
|[E03 Shader选修：能控制效果，不必重造渲染器](lessons/E03.md)|参考/概念讨论；所选专项另备实际样本|本课不需要专用3D文件，或专项按需|有明确视觉缺口时准备隔离样例和可关闭的单效果。|Shader专项无预置完整效果库。|
|[E04 复杂旋转选修：轨迹对，比公式背得熟重要](lessons/E04.md)|OpenMAIC先理解；Godot真实对照|[lab.tscn](../game/scenes/lab.tscn)|先用现有门轴说明预期轨迹，再定义复杂旋转问题。|基础Lab不能代替复杂旋转专项验证。|
|[E05 大场景选修：批量、剔除与加载各治什么](lessons/E05.md)|参考/概念讨论；所选专项另备实际样本|本课不需要专用3D文件，或专项按需|先以测量确认批量/加载问题，再选择专项，不先扩大地图。|大场景无完整样例，基础项目无需强做。|
|[E06 多人认识专题：先知道为什么会复杂](lessons/E06.md)|OpenMAIC/对话即可，全K|本课不需要专用3D文件，或专项按需|只解释联网增加了哪类协调问题，以及本项目是否需要。|全K，只理解用途，不要求实操或背诵。|
|[E07 高级专项结业：一个问题，一份可信决策](lessons/E07.md)|参考/概念讨论；所选专项另备实际样本|本课不需要专用3D文件，或专项按需|选一个真实专项问题，整理已测、未测和采用理由。|用自己的专项证据，不凭目录存在宣布通过。|

## 不把缺材料当孩子不会

A01/B10的参考必须真实可查看；没拿到图片先用文字/原创体块表达，不虚构大师画面。E01导航、E03专项Shader、E05大场景等没有完整专用包；未选不阻塞主线，选定后围绕实际需求由成人/AI补最小样本，不强迫孩子先重造系统。

C01/C02/D04/D07的三段地图、正式资产统一与最终试玩是孩子作品的生产任务，参考场景和实验不能代替该作品交付。C08并未提供Fog/Glow/DOF全套开关；非当前必要效果不为凑课强加。

需要亲手理解的是选择、预测、改变条件、观察、恢复和验收；不是把生成器已经能完成的空场景搭建逐步抄一遍。构建关系本身是学习目标时，在现成副本做一次局部修改即可。
