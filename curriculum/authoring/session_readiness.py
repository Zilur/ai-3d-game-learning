"""Minimum starting materials, not a claim that practical lesson packs exist.
These records extend the existing 47 lessons, not a new course or scoring scale.
"""
STARTS = {
 'A01': ('observe', '一张你确实能查看的参考图，或一段自己的偏好描述；没有图也可先练表达，但不能凭空评价画面。'),
 'A02': ('engine', '一个可选中的方块、带文字的世界轴、可观察的视口；还不需要玩家、物理或完整关卡。'),
 'A03': ('engine', '一个模块根节点、一个外观子节点和功能位置标记；不需要先有移动脚本。'),
 'A04': ('engine', '一堵外观与碰撞分开的墙、可用于测试的物理角色、一个检测区；移动能力可由提供的测试器承担，本课不考编写控制器。'),
 'A05': ('engine', '已经能碰撞的地面与测试角色、可编辑控制脚本或明确的局部操作入口；计时/距离记录可由AI准备。'),
 'A06': ('engine', '已有走跑、地面和一块已知高度低平台；能观察起跳与落地，不要求正式角色动画。'),
 'A07': ('engine', '可选中的父子物体、门板与支点；比较时有同一关闭位置和不变的尺度。'),
 'A08': ('engine', '已能走跳的角色和简单墙角；能够运行、停止并释放鼠标，不要求新美术素材。'),
 'B01': ('observe', '确实可查看的同一道具轮廓或形体变式，以及统一的观察大小；没有图先用标明的简化形状。'),
 'B02': ('asset', '一件来源明确、允许本次使用的可编辑静态道具副本；没有角色也能学，不在唯一源文件上修改。'),
 'B03': ('observe', '同一布局的主体、背景及可控颜色样本；固定轮廓与观察机位。'),
 'B04': ('engine', '两个可独立调材质的球、固定相机灯光和邻近灰箱；共享实验单独切换，不能假设已有参考场景全部实现。'),
 'B05': ('asset', '可编辑静态源文件、交换文件和当前已有的Godot包装；只验现有尺寸、材质与功能标记，不提前要求拾取和重开。'),
 'B06': ('engine', '已能移动的玩家、一颗有检测形状的星星及计数观察入口；防重和通知是本课逐步接入的部分，不必课前全部实现。'),
 'B07': ('engine', '已经有证据确认的拾取成功事件和计数；不需要预先具备声音、粒子或整套特效。'),
 'B08': ('engine', '已有有效拾取和明确进度来源；能改变运行窗口大小，本课再接完成、重开和布局。'),
 'B09': ('engine', '可运行的小场地、角色/目标、主光与环境；已有相机、材质及曝光基线可以记录。'),
 'B10': ('observe', '一件实际可查看且来源可追溯的作品，以及一个能够画简图或摆体块的练习位置；不自动下载原图。'),
 'B11': ('data', '约定的目标设备/画质/路线与一小段帧时间记录；没有真实数据时使用标明的合成样本，只评分析而非性能结果。'),
 'B12': ('data', '一处明确的预期/实际差异、最近修改和可回退版本；无真实故障时用教学修改卡，不假装读过个人项目。'),
 'B13': ('engine', '已有可完成并重开的收集小循环，以及一种新拾取物的需求；不以完整美术包作为前置。'),
 'C01': ('engine', '已经验证的初级小庭院与走跑跳/镜头参数基线；新增两段路用灰盒，不要求地形插件。'),
 'C02': ('engine', '已能跑通的庭院、林路、观景台，以及风格卡和三个观察点；先有一个入口转角可作样板。'),
 'C03': ('asset', '现有控制器和占位外观，以及实际提供的候选角色与来源说明；没有可用角色时只做资源卡选择。'),
 'C04': ('engine', '一个已验过基本兼容的角色与确实存在的动作片段；没有跑/跳片段不编造名称，先做可支持的最小状态。'),
 'C05': ('engine', '至少两个同类实例、可检查的资源引用和独立状态；不用一上来复制整个资源库。'),
 'C06': ('engine', '已有支点、碰撞、触发或交互测试入口；主任务只选一种门/机关，平台是可选变式。'),
 'C07': ('asset', '两三件简单模块、统一尺寸参照及棋盘格诊断材质；不要求人物UV或高分辨率素材包。'),
 'C08': ('engine', '真实目标设备/渲染器、一个静态样本及会移动的对象；不强制两个候选方案都已实现。'),
 'C09': ('data', '一个明确运行症状、条件记录和对照；无实测就分析合成案例，不给优化收益保证。'),
 'E01': ('optional', '已选择导航路线、可移除的测试场景、一个通道与巡逻对象；纯机关路线跳过。'),
 'C10': ('engine', '一个已有机关或可交互对象、输入意图、距离/目标可观察入口；不需要背包。'),
 'C11': ('data', '最小需要保存的进度/设置，以及正常、缺失、损坏的测试数据副本；不用真实玩家唯一存档。'),
 'C12': ('engine', '选定目标平台的可运行项目、资源来源清单和测试数据；没有实际导出包时只能准备交付检查，不能宣称发布通过。'),
 'D07': ('engine', '已完成的基础版可探索小关卡、来源与实际测试记录；仅选择增强版者再准备训练角证据。'),
 'D01': ('asset', '一件许可适用的可编辑基底、风格卡、游戏距离机位和只读原件；坏基底允许换，不强迫从零建模。'),
 'D02': ('asset', '两三件道具及中性对照环境；只有Blender预览时先记录引擎验证未做。'),
 'D03': ('data', '少量真实或明确标为示意的资产卡、源/变体关系和来源信息；不以资产数量作为成绩。'),
 'D04': ('observe', '一个实际可查看的场景样本或转角、自己的风格卡和资产信息；没有完整地图不声称整图已完成。'),
 'D05': ('optional', '已选动作复用路线、一个角色及真实动作文件或说明卡；无许可清楚的片段时只做选型判断。'),
 'D06': ('optional', '已试过兼容的一段原地攻击、可恢复的控制器和木桩测试副本；没有真实动作只做时间线模拟。'),
 'E02': ('optional', '一个实际需要进一步测量的问题、对应构建和基线；没有问题可不选本课。'),
 'E03': ('optional', '一个明确视觉目标、效果对照样本及渲染器约束；先选一种效果，不要求全套着色器。'),
 'E04': ('optional', '发生旋转问题的对象/父子关系，或带标签的170至-170度示意；先给路径目标。'),
 'E05': ('optional', '一个已有证据的重复物体或加载问题及固定观察路线；小世界不为完成本课强行扩建。'),
 'E06': ('decision', '两人同时请求一件物品的教学时间线即可；不需要网络项目、服务器或软件操作。'),
 'E07': ('optional', '一个已选专项的目标、基线和实际证据；未完成专项时先选择范围，不把实验计划当实验成功。'),
}
# File existence is checked by CI. A reference is not a complete, validated lesson starter.
REFERENCES = {
 'A02': ('game/scenes/lab.tscn', '已有综合实验参考；需核对本课参数，不能等同于整堂课的起点已验收。'),
 'A07': ('game/scenes/lab.tscn', '已有空间/门轴参考；真实导出原点仍另验。'),
 'A03': ('game/lessons/b02/starter.tscn', '已有起始场景；本课无玩家，打开当前场景，不把主游戏误当练习。'),
 'B04': ('game/labs/material_lab.tscn', '已有双球参考；共享/独立切换并非该场景默认配齐，缺少部分先标未实现。'),
}
for _id in ('A05','A04','A06','A08','B06','B07','B08','B09','B11','B12','B13'):
    REFERENCES[_id] = ('game/scenes/main.tscn', '已有完整收集参考解，只用于观察/排错；逐课隔离起点与全部新验收项仍待核验。')

SUPPORT_FADE = {'B12','B13','D07','D04','E07'}
FALLBACKS = {
 'observe': '可先作风格/观察决定。没有真实图片或样本时用标明的原创简图，不描述不存在的画面，不记真实作品观察通过。',
 'engine': '先用课内模拟辨清概念。缺起始场景时仅准备最小搭建清单；不要让新手为了上本课先生成整款游戏，真机应用保持待验证。',
 'asset': '先用说明卡判断来源、结构和改造范围。缺可编辑源或适用许可时停止导入/修改，不自动购买、下载或替换成不明资源。',
 'data': '先用明确标注的教学数据作判断；不可把合成数据、计划或AI口头结果填写成真实测量/修复/存档成功。',
 'decision': '只作一次用途与是否需要的决定即可结束；不增加软件执行或M成绩。',
 'optional': '未选择此专题就跳过。已选择但缺材料时先做范围/方案判断，实际应用留待验证，不反过来阻塞基础版。',
}

# Ready-made lab entry points; detailed native/production limits live in BINDINGS.
STARTS['A03'] = (STARTS['A03'][0], '现成实验：game/lessons/b02/starter.tscn、game/lessons/b02/broken.tscn。先做：打开现成starter，选中模块整体和外观子节点分别观察；再另存副本改一项。；不要从空项目重建。')
REFERENCES['A03'] = ('game/lessons/b02/starter.tscn', '这是A03的真实起点与故障对照；历史目录名b02不代表当前B02，不先读reference答案。')
STARTS['A04'] = (STARTS['A04'][0], '现成实验：game/labs/collision_roles_lab.tscn。先做：把角色目标移到墙另一侧，分别切换外观和阻挡；复位后再切检测角色/装饰。；不要从空项目重建。')
REFERENCES['A04'] = ('game/labs/collision_roles_lab.tscn', '真实Area与物理；改Mask后让角色或白色装饰重新进入，分别验证谁被检测。不是只由M1替M2。')
STARTS['A05'] = (STARTS['A05'][0], '现成实验：game/labs/motion_lab.tscn、game/scenes/main.tscn。先做：在现成运动Lab只改速度，比较相同时间位移；再在主游戏检查直走/斜走。；不要从空项目重建。')
REFERENCES['A05'] = ('game/labs/motion_lab.tscn', 'Lab是简化运动模型；真实控制器、帧率差异与碰撞在提供的主游戏副本和实际运行条件中检查。')
STARTS['A06'] = (STARTS['A06'][0], '现成实验：game/labs/motion_lab.tscn、game/scenes/main.tscn。先做：固定重力只改起跳速度，按跳跃观察；用“仅回到起点”重播对照。；不要从空项目重建。')
REFERENCES['A06'] = ('game/labs/motion_lab.tscn', '恢复全部初值会复位参数和控件，重播保留参数；边缘/墙边真实落地仍在主游戏检查。')
STARTS['A08'] = (STARTS['A08'][0], '现成实验：game/labs/camera_lab.tscn、game/scenes/main.tscn。先做：在镜头Lab保持其他条件，只切透视/正交，分别比较FOV/Size；再试向右移动。；不要从空项目重建。')
REFERENCES['A08'] = ('game/labs/camera_lab.tscn', '真实Camera3D投影和地面方向；没有完整分区切镜或事件镜头，未选这些增强不增加作业。')
STARTS['B02'] = (STARTS['B02'][0], '现成实验：blender/labs/transform_origin_lab.blend、blender/labs/kitbash_style_lab.blend。先做：直接打开现成静态样本，在副本中比较对象变换与网格编辑；再选小屋轮廓。；不要从空项目重建。')
STARTS['B04'] = (STARTS['B04'][0], '现成实验：game/labs/material_lab.tscn、blender/labs/uv_material_lab.blend。先做：保持灯光不动，先只改左球粗糙度；复位后切换共享材质，再改一次。；不要从空项目重建。')
REFERENCES['B04'] = ('game/labs/material_lab.tscn', '双球可切真实共享/独立资源，自发光与实际光源可分开；不把自发光球当环境照明或Glow已实现。')
STARTS['B06'] = (STARTS['B06'][0], '现成实验：game/labs/event_lab.tscn、game/scenes/main.tscn。先做：在事件Lab先发一次正确对象请求，再发错误对象和同帧双请求，比较计数。；不要从空项目重建。')
REFERENCES['B06'] = ('game/labs/event_lab.tscn', '按钮注入事件用于时序与状态实验，不伪称鼠标点击就是Area碰撞；真实拾取在主游戏，故障开关不带到成品。')
STARTS['B07'] = (STARTS['B07'][0], '现成实验：game/labs/event_lab.tscn、game/scenes/main.tscn。先做：在事件Lab切换可见反馈，比较成功计数和显示；再观察主游戏真实拾取。；不要从空项目重建。')
REFERENCES['B07'] = ('game/labs/event_lab.tscn', '现成反馈与规则分离；本Lab未提供完整音频/粒子/打击感库，不以反馈关掉判规则失败。')
STARTS['B08'] = (STARTS['B08'][0], '现成实验：game/labs/event_lab.tscn、game/scenes/main.tscn。先做：先在事件Lab完成、重开并再次请求，再在主游戏改变窗口检查布局。；不要从空项目重建。')
REFERENCES['B08'] = ('game/labs/event_lab.tscn', '事件Lab有独立状态和显示、可重复重开；主游戏的完整十星与窗口布局仍分别实测。')
STARTS['B12'] = (STARTS['B12'][0], '现成实验：game/lessons/b02/broken.tscn、game/labs/event_lab.tscn、game/scenes/main.tscn。先做：先在现成故障副本说明实际现象，再提出一个可能原因和最小验证，不先读答案。；不要从空项目重建。')
REFERENCES['B12'] = ('game/lessons/b02/broken.tscn', '可用A03故障或事件防重故障练排查；工程diff/版本恢复仍用自己的修改记录，不能自动判会。')
STARTS['C03'] = (STARTS['C03'][0], '现成实验：game/labs/animation_lab.tscn、blender/labs/animation_fixture.blend、game/scenes/main.tscn。先做：先打开原创动作样本查看骨架、蒙皮、三段片段，再比较角色大小与控制器职责。；不要从空项目重建。')
REFERENCES['C03'] = ('game/labs/animation_lab.tscn', '原创教学角色与实际动画现成可用；不是正式美术选型或通用骨架兼容保证，替换自己的角色还需验证。')
STARTS['C04'] = (STARTS['C04'][0], '现成实验：game/labs/animation_lab.tscn、blender/labs/animation_fixture.blend。先做：在动作Lab只调待机到行走的融合值和过渡时间，观察肢体而非读源码。；不要从空项目重建。')
REFERENCES['C04'] = ('game/labs/animation_lab.tscn', '真实AnimationTree与导入片段；Walk原地播放，主游戏移动/动画同步和脚滑验收仍需接到自己的控制器。')
STARTS['C05'] = (STARTS['C05'][0], '现成实验：game/labs/material_lab.tscn、blender/labs/uv_material_lab.blend、game/lessons/b02/starter.tscn。先做：先切Godot材质共享/独立，再在Blender检查Shared_A/B与Independent_C的数据引用。；不要从空项目重建。')
REFERENCES['C05'] = ('game/labs/material_lab.tscn', '提供真实材质和网格共享对照；动画引用及独立运行状态在实际角色实例中另验，不用一个静态图包办。')
STARTS['C06'] = (STARTS['C06'][0], '现成实验：game/labs/interaction_lab.tscn、game/labs/platform_lab.tscn。先做：先在门实验观察靠近与开门；需要平台变式时，打开平台实验比较站立跟随和起跳离开。；不要从空项目重建。')
REFERENCES['C06'] = ('game/labs/interaction_lab.tscn', '门与平台均已可交互；平台是实际独立CharacterBody与AnimatableBody，完整机关阻挡/关卡集成仍需实际项目验证。')
STARTS['C07'] = (STARTS['C07'][0], '现成实验：blender/labs/uv_material_lab.blend、blender/labs/kitbash_style_lab.blend。先做：打开UV样本，上排几何和光照相同，先观察棋盘格；只调整中间板的UV，不改几何尺寸。；不要从空项目重建。')
STARTS['C08'] = (STARTS['C08'][0], '现成实验：game/scenes/visual_lab.tscn、game/labs/material_lab.tscn、game/labs/camera_lab.tscn。先做：在现成同机位样本中先比较光照、材质或投影的一项，再核对实际渲染器。；不要从空项目重建。')
REFERENCES['C08'] = ('game/scenes/visual_lab.tscn', '提供实际渲染基线；Fog/Glow/DOF等候选仍按目标渲染器另试，不假装全套效果控件已配齐。')
STARTS['C10'] = (STARTS['C10'][0], '现成实验：game/labs/interaction_lab.tscn。先做：拖动角色接近蓝区，先不拿钥匙尝试开门，再只改变钥匙条件。；不要从空项目重建。')
REFERENCES['C10'] = ('game/labs/interaction_lab.tscn', '真实检测/允许条件/门状态/提示分离，重复开门可验证；不含背包或完整正式关卡系统。')
STARTS['C11'] = (STARTS['C11'][0], '现成实验：game/labs/interaction_lab.tscn。先做：在门实验先保存门进度与偏好，再改临时位置、门或偏好，按读取观察哪些恢复。；不要从空项目重建。')
REFERENCES['C11'] = ('game/labs/interaction_lab.tscn', '真实专用本地文件，可准备缺失/坏档/v0旧档；恢复初值不删文件，只能删除本实验档，不代表正式游戏存档已接入。')
STARTS['D05'] = (STARTS['D05'][0], '现成实验：blender/labs/animation_fixture.blend、game/labs/animation_lab.tscn。先做：先直接播放原创角色的三段现成片段，观察骨骼/网格关系，再到Godot比较导入和融合。；不要从空项目重建。')
REFERENCES['D05'] = ('game/labs/animation_lab.tscn', '有真实骨架、蒙皮与动作；不是外部动作库或通用重定向，新角色仍先做一段兼容小试。')
STARTS['D06'] = (STARTS['D06'][0], '现成实验：game/labs/animation_lab.tscn、game/scenes/main.tscn。先做：先播放一次攻击并中断，比较目标在内/在外与重复输入下的命中次数。；不要从空项目重建。')
REFERENCES['D06'] = ('game/labs/animation_lab.tscn', '现成窗口/距离/一次性规则实验；未把攻击接入主游戏控制器，关闭训练角后的十星回归仍要自己集成后验证。')
