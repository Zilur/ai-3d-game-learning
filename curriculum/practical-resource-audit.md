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
|[C01 小地图扩展：用固定镜头串起可探索路线](lessons/C01.md)|OpenMAIC先理解；Godot真实对照|[exploration.tscn](../game/world/exploration.tscn)|先运行三段路线，指出主路、找钥匙的支路和回程；另存副本只改变一个路口。|三段参考已实现，不等于自己的地图已通过；新路线仍要实走与陌生玩家检验。|
|[C02 世界美化：镜头决定世界，套装统一风格](lessons/C02.md)|OpenMAIC先理解；Godot真实对照|[visual_lab.tscn](../game/scenes/visual_lab.tscn)、[exploration.tscn](../game/world/exploration.tscn)|先在疏密实验作对照，再用实际玩家镜头检查庭院、林路、观景台的焦点。|原生实验与原创资产参考都已备好；视觉选择由真人验收，未冒称商业品质。|
|[C03 接入现成角色：会选、会替换、会验收](lessons/C03.md)|OpenMAIC先理解；Godot/Blender各验相关部分|[animation_lab.tscn](../game/labs/animation_lab.tscn)、[animation_fixture.blend](../blender/labs/animation_fixture.blend)、[main.tscn](../game/scenes/main.tscn)|先打开原创动作样本查看骨架、蒙皮、三段片段，再比较角色大小与控制器职责。|原创教学角色与实际动画现成可用；不是正式美术选型或通用骨架兼容保证，替换自己的角色还需验证。|
|[C04 动画状态：动作片段如何接起来](lessons/C04.md)|OpenMAIC先理解；Godot/Blender各验相关部分|[animation_lab.tscn](../game/labs/animation_lab.tscn)、[animation_fixture.blend](../blender/labs/animation_fixture.blend)|在动作Lab只调待机到行走的融合值和过渡时间，观察肢体而非读源码。|真实AnimationTree与导入片段；Walk原地播放，主游戏移动/动画同步和脚滑验收仍需接到自己的控制器。|
|[C05 复用与资源：共享什么、独立什么](lessons/C05.md)|OpenMAIC先理解；Godot/Blender各验相关部分|[material_lab.tscn](../game/labs/material_lab.tscn)、[uv_material_lab.blend](../blender/labs/uv_material_lab.blend)、[starter.tscn](../game/lessons/b02/starter.tscn)|先切Godot材质共享/独立，再在Blender检查Shared_A/B与Independent_C的数据引用。|提供真实材质和网格共享对照；动画引用及独立运行状态在实际角色实例中另验，不用一个静态图包办。|
|[C06 门与移动平台：复用已会的空间和状态](lessons/C06.md)|OpenMAIC先理解；Godot真实对照|[interaction_lab.tscn](../game/labs/interaction_lab.tscn)、[platform_lab.tscn](../game/labs/platform_lab.tscn)|先在门实验观察靠近与开门；需要平台变式时，打开平台实验比较站立跟随和起跳离开。|门与平台均已可交互；平台是实际独立CharacterBody与AnimatableBody，完整机关阻挡/关卡集成仍需实际项目验证。|
|[C07 模块拼接与简单UV：统一尺度和纹理密度](lessons/C07.md)|Blender现成副本|[uv_material_lab.blend](../blender/labs/uv_material_lab.blend)、[kitbash_style_lab.blend](../blender/labs/kitbash_style_lab.blend)|打开UV样本，上排几何和光照相同，先观察棋盘格；只调整中间板的UV，不改几何尺寸。|纹理已打包，正常/拉伸/密度样本现成；模块连接用小屋部件，复杂角色UV不列入当前必修。|
|[C08 风格化光照方案：效果必须能进游戏](lessons/C08.md)|OpenMAIC先理解；Godot真实对照|[effects_lab.tscn](../game/labs/effects_lab.tscn)|全关基线开始，一次开Fog、Glow或景深；观察实际渲染器和对应参数。|普通雾/辉光已实现；景深需Forward+或Mobile，Compatibility明确禁用；不冒充体积雾。|
|[C09 优化入口：知道什么时候该停](lessons/C09.md)|已有游戏参考/自己的工程/目标设备|[main.tscn](../game/scenes/main.tscn)|对同一构建/机位选择一项真实测量，不改多种设置。|基准由目标设备提供，headless不代表GPU画面性能。|
|[C10 可交互对象：提示、条件和结果](lessons/C10.md)|OpenMAIC先理解；Godot真实对照|[interaction_lab.tscn](../game/labs/interaction_lab.tscn)、[exploration.tscn](../game/world/exploration.tscn)|先用隔离实验区分靠近、允许和结果，再在林路拿钥匙、到门前按E。|门和钥匙已接入主游戏；实验文件与主游戏存档完全隔离。|
|[C11 存档与设置：能恢复比能写入更重要](lessons/C11.md)|OpenMAIC先理解；Godot真实对照|[interaction_lab.tscn](../game/labs/interaction_lab.tscn)、[exploration.tscn](../game/world/exploration.tscn)|先在实验测试缺失/损坏文件，再在主游戏主动保存、退出并继续。|主游戏有独立版本存档和备份；恢复到安全检查点，不保存攻击中间帧；不承诺抗所有断电故障。|
|[C12 交付：别人电脑上第一次运行](lessons/C12.md)|OpenMAIC先理解；Godot真实对照|[exploration.tscn](../game/world/exploration.tscn)|先运行完整三段主线和暂停菜单，再按自己的目标平台实际导出验收。|源码与自动测试不是全部设备体验认证；发布包仍须目标设备检查。|
|[D01 资产套装二开：从基底拼装成自己的道具](lessons/D01.md)|Blender现成副本|[kitbash_style_lab.blend](../blender/labs/kitbash_style_lab.blend)|先另存副本，选Variant_Roof只改一项比例，比较Base。|原创几何二开样例，不是已购买的完整资产套装。|
|[D02 风格统一：配色、材质、边缘与细节密度](lessons/D02.md)|OpenMAIC先理解；Godot/Blender各验相关部分|[kitbash_style_lab.blend](../blender/labs/kitbash_style_lab.blend)、[material_lab.tscn](../game/labs/material_lab.tscn)|固定光照，先统一一件变体色彩，再单独调粗糙度。|支持局部材质观察，不等于整库风格已经统一。|
|[D03 长期资产库：主套装、基底、变体与组合规则](lessons/D03.md)|Blender现成副本|[kitbash_style_lab.blend](../blender/labs/kitbash_style_lab.blend)|为一件变体记录源、用途、版本、引用和预览机位。|样例不自带完整商业资产库，按本地实际资源建立。|
|[D04 美术结业：用套装二开拼出自己的童话场景](lessons/D04.md)|OpenMAIC先理解；Godot/Blender各验相关部分|[kitbash_style_lab.blend](../blender/labs/kitbash_style_lab.blend)、[exploration.tscn](../game/world/exploration.tscn)|用现成原创GLB库替换或调整一处，固定机位作前后对照，再走完整路线。|三段原创生产参考已接入12类静态资产；不是已购买外部套装或最终美术签收。|
|[D05 动作资源复用：动作包兼容、重定向与融合](lessons/D05.md)|OpenMAIC先理解；Godot/Blender各验相关部分|[animation_fixture.blend](../blender/labs/animation_fixture.blend)、[animation_lab.tscn](../game/labs/animation_lab.tscn)|先直接播放原创角色的三段现成片段，观察骨骼/网格关系，再到Godot比较导入和融合。|有真实骨架、蒙皮与动作；不是外部动作库或通用重定向，新角色仍先做一段兼容小试。|
|[D06 轻战斗融入：现成攻击动作与可重复训练木桩](lessons/D06.md)|OpenMAIC先理解；Godot真实对照|[animation_lab.tscn](../game/labs/animation_lab.tscn)、[exploration.tscn](../game/world/exploration.tscn)|先看隔离命中窗口，再在主游戏面对木桩按J；比较远处/背对/关闭训练。|动作、命中、恢复控制已整合；训练可关闭且不影响十星，不是完整敌人/战斗系统。|
|[D07 精致Demo结业：完整探索关卡与可选训练角](lessons/D07.md)|OpenMAIC先理解；Godot真实对照|[exploration.tscn](../game/world/exploration.tscn)|从庭院经过林路拿钥匙到观景台，完成十星；测试保存、继续、重开与训练关闭。|这是可玩的完整参考版本；儿童掌握、商业视觉质量与全部设备兼容仍需独立验收。|
|[E01 导航选修：画得出路径还要走得到](lessons/E01.md)|OpenMAIC先理解；Godot真实对照|[navigation_lab.tscn](../game/labs/navigation_lab.tscn)|保持导航半径，调大真实碰撞球；先猜路径存在是否等于能过窄门。|使用真实NavigationServer与碰撞；网格是预制规则生成，非自动烘焙或动态避障系统。|
|[E02 高级测量：用证据决定技术投入](lessons/E02.md)|OpenMAIC先理解；Godot真实对照|[large_scene_lab.tscn](../game/labs/large_scene_lab.tscn)、[exploration.tscn](../game/world/exploration.tscn)|固定机位与渲染器，单独切批量或LOD，重新采样并记录条件。|界面帧间隔和draw calls是真实当前运行值；无渲染模式不代表GPU性能，不保证每项优化都会更快。|
|[E03 Shader选修：能控制效果，不必重造渲染器](lessons/E03.md)|OpenMAIC先理解；Godot真实对照|[shader_lab.tscn](../game/labs/shader_lab.tscn)|先保持左侧参考不变，只在右侧启用条纹、边缘强调或风摆一项。|真实空间Shader含关闭与冻结；不是完整Shader效果库或材质自动转换。|
|[E04 复杂旋转选修：轨迹对，比公式背得熟重要](lessons/E04.md)|OpenMAIC先理解；Godot真实对照|[lab.tscn](../game/scenes/lab.tscn)|先用现有门轴说明预期轨迹，再定义复杂旋转问题。|基础Lab不能代替复杂旋转专项验证。|
|[E05 大场景选修：批量、剔除与加载各治什么](lessons/E05.md)|OpenMAIC先理解；Godot真实对照|[large_scene_lab.tscn](../game/labs/large_scene_lab.tscn)|只切分块驻留并移动相机，观察远区节点实际创建/释放，再分别对照MultiMesh和LOD。|9区块432物体的有界实验；另有真实场景异步读取按钮；共享资源可能缓存，不等于无限地图或全部显存卸载。|
|[E06 多人认识专题：先知道为什么会复杂](lessons/E06.md)|OpenMAIC/对话即可，全K|本课不需要专用3D文件，或专项按需|只解释联网增加了哪类协调问题，以及本项目是否需要。|全K，只理解用途，不要求实操或背诵。|
|[E07 高级专项结业：一个问题，一份可信决策](lessons/E07.md)|参考/概念讨论；所选专项另备实际样本|本课不需要专用3D文件，或专项按需|选一个真实专项问题，整理已测、未测和采用理由。|用自己的专项证据，不凭目录存在宣布通过。|

## 不把缺材料当孩子不会

A01/B10的参考必须真实可查看；没拿到图片先用文字/原创体块表达，不虚构大师画面。E01导航、E03单效果Shader、E05分块/批量/LOD现在都有真实场景；未选仍不阻塞主线，不要求先重造系统。新的高级需求超出该切片时，再补局部样本。

C01/C02/D04/D07可直接观察已实现的三段原创资产参考，再到自己的副本迁移。C08已有普通Fog、Glow与景深控件，景深按真实渲染器禁用或启用；这些不是儿童掌握、商业美术或所有设备通过的证明。

需要亲手理解的是选择、预测、改变条件、观察、恢复和验收；不是把生成器已经能完成的空场景搭建逐步抄一遍。构建关系本身是学习目标时，在现成副本做一次局部修改即可。
