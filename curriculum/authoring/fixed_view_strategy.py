"""Project-specific fixed/limited-camera and kitbash strategy.
This changes teaching emphasis only; it does not implement runtime camera, art or combat features.
"""

STYLE_BASELINE = (
    '本项目默认面向固定或有限镜头的风格化3D小游戏：温暖、唯美、卡通、低写实、配色清楚。'
    '镜头是构图工具，不要求玩家持续自由环绕；美术生产以优质资产套装的选择、拼装、二开和统一为主，'
    '从零建模与原创复杂动画不是主线门槛。'
)


def _row_map(lessons):
    return {row['id']: row for row in lessons}


def _append_unique(row, field, text):
    values = row[field]
    if text not in values:
        values.append(text)


def apply_fixed_view_strategy(lessons, scenarios, plans, diagrams, reviews, starts, sources):
    by_id = _row_map(lessons)
    required = {'A01','A08','C01','C02','C03','C04','C07','D01','D02','D03','D04','D05','D06'}
    if not required <= set(by_id):
        raise ValueError('Fixed-view strategy missing canonical lessons')

    sources.update({
        'fixed_camera': ('Godot Camera3D：投影、FOV与相机属性', 'https://docs.godotengine.org/en/stable/classes/class_camera3d.html'),
        'asset_library': ('Blender Asset Libraries：资产复用入口', 'https://docs.blender.org/manual/en/latest/files/asset_libraries/introduction.html'),
    })

    # Project-wide art direction appears at the beginning, without turning taste into a universal rule.
    _append_unique(by_id['A01'], 'body', STYLE_BASELINE + 'A01仍训练把个人偏好拆成可观察规则；默认风格只是本项目的起始方向，可被实际参考图修正。')
    _append_unique(by_id['A01'], 'remember', '本项目先固定“温暖、风格化、低写实”的方向，再用实际参考细化，不靠抽卡决定画风。')

    # A08 is no longer a free-orbit camera course. It becomes the fixed/limited camera foundation.
    a08 = by_id['A08']
    a08.update(
        title='固定/有限镜头：构图舒服，移动清楚',
        goal='确定一个稳定的固定或有限镜头基线，让角色移动方向、落点和画面构图都清楚。',
        m=['选择固定镜头的位置、角度与投影/视野基线，并用实际玩家画面说明取舍。','让地面移动在固定镜头下方向一致；需要分区切镜时检查进入、退出和边界稳定。'],
        k=['Perspective/Orthographic是两种投影选择；按画面目标比较，不背投影数学。','Camera Zone、SpringArm/RayCast是按需处理切镜或遮挡的工具。'],
        stop='不推投影矩阵，不要求自由环绕镜头、头部晃动、动态FOV或复杂相机框架；舒适度必须真人复核。',
        body=[
            '固定镜头不是“少做一个功能”，而是先决定最终画面再制作世界。角色仍在3D空间移动，但玩家不必持续转相机。透视镜头可用位置/角度/FOV组织画面；正交镜头可用Orthographic Size组织范围。两者都要在实际角色尺度下比较。',
            '移动必须明确参考：固定三分之四镜头下，屏幕上方/下方、左/右与世界轴不一定相同。课程只要求建立一种一致规则并实走验证。若地图分为多个镜头区域，切换点要可预测，避免边界反复切换；默认不把强震动、头部晃动、频繁动态FOV和运动模糊当必要效果。',
        ],
        initial='能走跳的角色、一个低平台与墙角；固定三分之四机位A，备用机位B只用于切镜对照。默认无需鼠标持续转镜头。',
        controls='镜头高度/俯角、Perspective FOV或Orthographic Size二选一、屏幕相对移动示意、机位A/B切换；不同时开放所有参数。',
        steps=['先锁定机位A，固定角色尺度，只调整一项镜头角度或视野/尺寸，观察路线、角色和落点。','在同一机位测试四向移动和跳跃，确认输入不会因镜头俯角混入竖直移动。','只在确有第二构图需求时加入机位B；从两个方向跨过切换边界，检查不抖动、不连续反转。'],
        feedback='始终显示当前机位、投影方式/视野参数和角色地面方向；镜头美术选择与移动正确性分别记录。',
        failure='故障：AI自动加自由Orbit、头部晃动或频繁切镜来“更3D”，却破坏固定构图或舒适基线；恢复项目镜头约束，只保留有证据的变化。',
        reset='恢复机位A、角色起点、移动映射和切镜状态；不通过改角色速度掩盖构图或方向问题。',
        ui=['Godot常用：Camera3D Transform、Projection、FOV或Size；只亲调项目实际采用的一组。','会定位：当前Camera3D、区域切镜触发和运行时相机状态。','按需查：SpringArm/RayCast、复杂平滑和电影相机系统；自由Orbit不是本项目基础门槛。'],
        questions=[
            ('P','固定视角游戏是否必须再加鼠标自由转镜头，才算真正3D？','不必；3D空间与自由相机是不同选择。先按构图、可读性和舒适目标决定镜头控制。','先分清世界维度和镜头交互。'),
            ('D','角色从机位A进入机位B边界后，按住同一个方向键在边界来回反向；AI建议把移动速度降一半。你先检查什么？','先检查切镜阈值/滞回和移动参考是否随相机瞬间重映射；速度不修方向反复。固定一侧机位基线，再双向跨边界验证。','问题是走得太快，还是参考方向不断变化？'),
            ('T','把室外庭院改成室内小房间，应该直接沿用原机位吗？','不一定；保留一致的输入规则，重新按遮挡、可见范围和构图选机位/投影参数，再实走入口与交互点。','哪些规则应该保持，哪些取决于空间？'),
            ('K','正交与透视现在要掌握到什么程度？','知道两者画面空间感不同，会在固定角色和场景下比较并选择；不需要推投影公式。','看实际画面，而不是背矩阵。'),
        ],
        remember=['Camera先决定玩家实际会看到什么。','固定镜头仍要实走验证移动方向与落点。','不把“更会动的相机”自动当成更高级。'],
        practice='后续真机以固定或有限镜头运行；目标是构图、方向和舒适基线，不要求自由鼠标Orbit。切镜仅在地图确有需要时加入。',
    )
    if 'fixed_camera' not in a08['sources']:
        a08['sources'].append('fixed_camera')

    reviews['A08'].update(
        finding='原课程以自由第三人称镜头为默认，与本项目固定/有限镜头和低晕动目标不一致。',
        decision='先锁定玩家实际看到的构图，选择机位/投影并定义一致移动规则；只在地图确有需要时加切镜。',
        ai='搭固定机位A/B、显示移动参考和切换状态；不自动加入Orbit、头晃、动态FOV或震屏。',
        proof=['固定角色和场景，选择一组机位与投影/视野参数，说明路线、角色和落点为何清楚。','四向实走并双向穿过一个可选切镜边界，移动方向稳定且切镜不反复；无第二机位需求时说明不做。'],
        diagnostic=('角色跨入第二机位时方向正常，但站在边界附近会不断A/B切换，输入方向也来回改变。AI建议降低角色速度。你先检查什么设计条件，怎样验证不是速度问题？','先检查相机区域边界、滞回/一次性切换条件和移动参考规则。固定角色速度，从两侧多次跨边界；只有真正进入另一侧才切换，不能靠降速掩盖边界抖动。','如果角色不移动，镜头是否仍可能在边界反复改变？','定位切镜条件与参考方向；保持速度基线，双向跨界可重复验证。'),
        target=2,
    )
    a08['questions'][1] = ('D', '【教学构造情境，不是真实测量或某模型故障统计】' + reviews['A08']['diagnostic'][0], reviews['A08']['diagnostic'][1], reviews['A08']['diagnostic'][2])

    scenarios['A08'].update(
        place='P02｜固定三分之四镜头下跑跳与看落点',
        before='自由转镜头或边界切镜让方向不稳定，画面也难按设计构图。',
        after='固定/有限机位下路线、角色和落点清楚；移动方向稳定，必要切镜不抖动。',
        task='锁定主机位，只调一项位置/角度/投影参数；再实走四向和跳跃。只有第二构图确有价值时才加机位B并测试边界。',
        keep='角色速度、跳跃、碰撞与关卡尺度保持；默认不新增Orbit、头晃、动态FOV或强镜头震动。',
        tweaks=[('Camera3D Transform（内置）','固定其他条件，只小幅改高度或俯角','角色、主路、落点和遮挡是否更清楚'),('Camera3D FOV或Orthographic Size（内置，二选一）','只调项目采用的投影参数','画面范围、角色大小和空间层次是否符合目标')],
        accept=['能说明为什么选择当前固定机位/投影，并在玩家画面看清路线与落点。','四向与跳跃实际方向稳定；选用第二机位时双向跨界不反复切换。'],
        regress='走跑跳、碰撞和目标可达保持；镜头变化不能靠改角色速度补偿。',
        transfer='换一个更窄的室内区域，保留输入规则但重新选构图；可以得出“单机位已够，不新增切镜”。',
        risk='检查AI是否擅自加入Orbit、头晃、动态FOV、频繁震屏或在区域边界反复切镜。',
    )
    plans['A08'] = ('先锁定一个三分之四固定机位，只暴露高度/俯角和项目采用的FOV或Size；不加入鼠标Orbit。', '我能在主机位看清路线、角色和低平台落点，且四向移动稳定。', '只有第二构图确有价值时再加机位B，双向跨界检查切换与方向；没价值就保留单机位。', 'fixed_camera')
    diagrams['fixed_camera'] = 'flowchart LR\n  W["3D世界与可玩路线"] --> C["固定/有限Camera"]\n  C --> F["最终构图与可见范围"]\n  I["输入方向规则"] --> M["角色地面移动"]\n  C --> I\n  Z["可选Camera Zone"] --> C\n  F --> V["路线/落点可读与舒适验收"]\n  M --> V'
    starts['A08'] = ('engine', '已能走跳的角色、低平台和墙角；默认固定三分之四机位，无需鼠标持续控制镜头。')

    # World lessons: each area is designed as a playable composition, not a generic 360-degree set.
    c01 = by_id['C01']
    c01['title'] = '小地图扩展：用固定镜头串起可探索路线'
    c01['goal'] = '保留原庭院，增加林间路和观景台；按固定/有限镜头把入口、地标、落点和回程串成小路线。'
    _append_unique(c01, 'body', '本项目扩图按“镜头画面”而不是“开放世界面积”思考。每个区域先确认玩家机位、入口、出口和一个主要地标；看不到也到不了的区域不需要同等制作成本。')
    c01['k'] = ['Blockout、Landmark、Sightline用于灰盒、地标与视线沟通。','Camera Zone只在不同区域确有构图需求时使用，不为技术展示而增加。']
    c01['stop'] = '不制作开放世界、流送、自由相机或程序化大地图；不靠提高移动速度掩盖空跑。'
    scenarios['C01'].update(
        place='P06a｜三个固定/有限镜头区域串成可跑小地图',
        task='先为庭院、林路、观景台各画一个玩家机位和入口/出口，再只扩一段灰盒；用角色实走而不是俯视图证明连通。',
        keep='原走跑跳、固定镜头输入规则、十星总数和庭院基线保持。',
        risk='检查AI是否只放大地面、增加无目的支路，或为了扩图擅自恢复自由相机。',
    )
    plans['C01'] = ('先只为庭院、林路、观景台标三个玩家机位和入口/出口，再连接一条主路；不先做装饰。', '我能从实际玩家画面说清下一步去哪里并走通主路/回程。', '再移开一个遮挡或调整一个地标；只有跨区确有必要才加入稳定切镜。', 'fixed_world')
    diagrams['fixed_world'] = 'flowchart LR\n  C1["镜头画面1：入口/主路"] --> R["可玩路线"]\n  C2["镜头画面2：转折/地标"] --> R\n  C3["镜头画面3：目标/回程"] --> R\n  R --> S["套装拼装与Set Dressing"]\n  S --> V["实走可读性与统一风格"]'
    starts['C01'] = ('engine', '已经验证的庭院与固定/有限镜头基线；新增林路和观景台先用灰盒，每区先标一个玩家机位。')

    c02 = by_id['C02']
    c02['title'] = '世界美化：镜头决定世界，套装统一风格'
    c02['goal'] = '从一个样板转角开始，用资产套装、配色、材质和留白统一三段固定视角小世界，同时保持路线可读。'
    c02['k'] = ['Set dressing、Focal point、Negative space用于场景布置、焦点与留白。','Facade/Shell、Billboard、Forced Perspective是固定视角下的背景制作手段；玩家可达处仍按玩法验收。']
    c02['stop'] = '不追写实和360度完整世界；不把所有背面、远景都做成Hero精度，也不让装饰破坏玩法。'
    _append_unique(c02, 'body', '固定镜头允许“Camera决定World”：先做好一个玩家真的会看到的转角样板，再扩到其他区域。背景不可达建筑可以只认真做可见面，远树可用低成本表现，远景比例可为构图服务；一旦玩家能接近、切镜会看到或阴影/反射会暴露，就不能按背景规则偷懒。')
    _append_unique(c02, 'body', '资产分Hero、Gameplay、Background三档投入。Hero做明显二开形成身份；Gameplay优先套装复用并保证碰撞/交互；Background以目标镜头成立为准。视觉Mesh和Collision分开，简化碰撞不能改变路线、落点和命中。')
    scenarios['C02'].update(
        place='P06b｜按三个玩家机位统一世界而不是堆满模型',
        task='先选一个风格接近的主资产套装，在入口转角只统一大形、色盘和材质层级；通过后才让AI帮助扩展到林路/观景台。',
        keep='已验证路线、固定镜头、十星可达和交互净空保持；背景作弊不得进入玩家可达/关键阴影范围造成穿帮。',
        risk='检查AI是否混用多个互不相干的风格包、全场高饱和发光，或为了360度完整性浪费不可见区域成本。',
    )
    plans['C02'] = ('先固定入口玩家机位，用主资产套装只做一个样板转角：统一比例、色盘和一种表面规则，不铺满地图。', '同机位下样板像同一个世界，主路/星星/落点仍一眼可读。', '再把规则扩到另一区域；背景不可达部分按目标镜头简化，玩家可达部分继续按玩法验收。', 'fixed_world')
    starts['C02'] = ('engine', '已跑通的三段灰盒、固定/有限镜头基线、风格卡和一个来源清楚的主资产套装；先只做入口样板。')

    # Reuse and assembly are the default art-production skill, not a fallback.
    _append_unique(by_id['C03'], 'body', '本项目优先接入来源清楚、风格接近的现成角色；角色“原创性”不靠从零建模证明，而靠选择、配色/材质、比例校准、动画与整个世界的统一。')
    _append_unique(by_id['C04'], 'body', '动画同样采用资源包思路：先验证待机/走跑/跳等最小片段，再组合状态；复杂原创武打不是主线。')
    _append_unique(by_id['C07'], 'body', '模块化套件就是环境Kitbash的基础：直墙、转角、门窗、屋顶等接口统一后，可以通过组合和少量变体快速生成自己的场景，而不是逐栋从零建模。')

    d01 = by_id['D01']
    d01['title'] = '资产套装二开：从基底拼装成自己的道具'
    d01['goal'] = '从风格接近的可编辑套装中选择基底，通过比例、模块替换和有限细修做出属于当前项目的变体。'
    _append_unique(d01, 'body', '把资产包当乐高积木：先保留它优秀的视觉基因，再改最影响身份的大形、比例和部件组合。可以换屋顶/门窗/招牌/附件，或把多个兼容模块Kitbash成新道具；不需要为“原创”把已合格结构全部重做。')
    d01['stop'] = '不做全套雕刻、复杂角色重拓扑或从Cube重造整件资产；只改玩家镜头真正看得到且能提升统一性的部分。'
    if 'asset_library' not in d01['sources']:
        d01['sources'].append('asset_library')
    scenarios['D01'].update(
        place='P07｜把通用套装里的基底二开成庭院自己的道具',
        before='现成资产单独好看，但直接放入场景像别的游戏；或为了原创从零重做浪费时间。',
        after='保留优秀基底，用比例、部件组合和有限表面修改形成项目变体，可回退也可复用。',
        task='从同一资产套装挑一件基底，先列保留/修改/不做三栏；只改大形或一组模块组合，再决定是否值得细修。',
        risk='检查AI是否为了“原创”重做整件模型、破坏接口/原点，或把看不到的小细节当质量核心。',
    )
    plans['D01'] = ('先选一件套装基底，写保留/修改/不做三栏；只改大比例或替换一组部件，不先雕细节。', '固定玩家机位能看出它已更符合风格，同时原点/接口/用途仍可用。', '再加一处有限倒角、厚度或附件；收益不明显就停止，不从零重做。', 'kitbash')
    diagrams['kitbash'] = 'flowchart LR\n  R["参考与风格规则"] --> K["选择主资产套装/基底"]\n  K --> B["保留可用结构"]\n  B --> M["比例/部件/模块二开"]\n  M --> P["配色/材质统一"]\n  P --> G["Godot玩家机位验收"]\n  G --> L["保存为可追溯变体"]'
    starts['D01'] = ('asset', '一件来源和修改条件明确的可编辑套装基底、风格卡、固定玩家机位和只读原件；从二开开始，不从零建模。')

    d02 = by_id['D02']
    d02['title'] = '风格统一：配色、材质、边缘与细节密度'
    d02['goal'] = '把两三件可能来自同套或不同套的资产，统一成同一个游戏的色彩与表面语言，并验证Godot实际画面。'
    _append_unique(d02, 'body', '风格统一优先改“关系”而不是改每个模型：有限色盘、相似的边缘语言、受控粗糙层级和一致细节密度，比让所有资产使用同一个材质数值更重要。不同套装先各取一件做小样，统一成功再批量。')
    scenarios['D02'].update(
        before='两三套资产各自漂亮，但配色、反射、边缘和细节密度不同，放一起像拼贴。',
        after='用同一风格卡统一色盘和表面层级，同时保留木/布/金属必要差异。',
        task='固定玩家机位和灯光，只统一一类关系：先配色，再粗糙/金属层级，再决定是否需要边缘/细节改造；每步都能恢复。',
        risk='检查AI是否用同一个Roughness/Metallic数值抹平所有材料，或同时改灯光和材质导致无法归因。',
    )
    plans['D02'] = ('先固定同一玩家机位/灯光，让两三件资产只做色盘归一，不改几何。', '它们像来自同一世界，但不同材料仍能分辨。', '再只统一粗糙层级或细节密度一项；最后到Godot同机位确认，不以Blender展示图代替。', 'kitbash')
    starts['D02'] = ('asset', '两三件来自套装的道具、风格卡、固定玩家机位与中性对照；先做配色/材质统一，不要求原创贴图。')

    d03 = by_id['D03']
    d03['title'] = '长期资产库：主套装、基底、变体与组合规则'
    _append_unique(d03, 'body', '资产库重点保存“怎么继续二开”：主套装来源、基底、允许共享的材质、模块接口、推荐色盘、已验证镜头和可用变体。目标是下次直接拿来组装，不是囤几百个互不一致的模型。')
    if 'asset_library' not in d03['sources']:
        d03['sources'].append('asset_library')
    plans['D03'] = ('先登记一个主套装基底与一个二开变体：来源、尺度、接口、色盘/材质规则和验证状态。', '换一个场景仍能找到源文件，并知道改基底会影响哪些变体。', '再增加一个部件组合或配色变体，测试有意共享保留、个体变化不串改。', 'kitbash')
    starts['D03'] = ('data', '少量真实资产：至少一个主套装基底和一两个二开变体，带来源/尺度/接口/材质与验证信息；不以数量评分。')

    d04 = by_id['D04']
    d04['title'] = '美术结业：用套装二开拼出自己的童话场景'
    d04['goal'] = '用主资产套装和少量二开变体，完成一个固定视角下统一、可辨路、能说明取舍的小型童话场景。'
    _append_unique(d04, 'body', '结业不要求六件资产全部原创。重点是你能选择主套装、建立统一规则、做少量有身份的Hero变体，并在固定玩家机位把它们组合成一个完整视觉世界。')
    scenarios['D04'].update(
        place='P07｜用套装与少量Hero二开完成一个固定视角场景',
        task='选择主套装作为视觉基因，只对一两件焦点物做明显二开；其余通过组合、配色、材质与摆放统一，在实际玩家镜头验收。',
        keep='主路、交互净空、固定镜头和来源记录保持；不以原创网格比例作为质量分。',
        risk='检查AI是否为了显得高级把每件资产都重做、把场景填满，或让背景细节抢走玩法焦点。',
    )
    plans['D04'] = ('先在固定玩家机位摆主套装的六件以内资产，只解决整体比例、主次和留白；暂不精修单件。', '一眼能读出主路/焦点，资产像同一个世界而不是素材展台。', '只选择一两件Hero做明显二开，其余靠组合、配色和材质统一；最后隐藏参考换一个道具检验规则。', 'fixed_world')
    starts['D04'] = ('observe', '一个已可玩的固定视角转角/小场景、主资产套装、风格卡和一两件二开变体；没有整图也可只做样板。')

    # Motion follows the same reuse mindset.
    d05 = by_id['D05']
    d05['title'] = '动作资源复用：动作包兼容、重定向与融合'
    _append_unique(d05, 'body', '动作包也是“套装”：优先选择骨架/参考姿态/根位移说明清楚的一组，先试待机或单次动作，再决定是否批量融合。复杂坏动作可以换资源，不把手工清理每帧作为程序员主线能力。')
    plans['D05'] = ('先比较两份动作资源说明，只选来源与骨架/姿态/根位移信息更清楚的一段做最小试用。', '动作可播、脚底/位移来源可解释，且我知道为什么保留或淘汰另一份。', '再加第二片段做最小融合；若适配成本高于换包，就记录理由并换资源。', 'action_reuse')
    diagrams['action_reuse'] = 'flowchart LR\n  P["角色/动作包信息"] --> C["兼容与许可筛选"]\n  C --> T["只试一个片段"]\n  T --> R["重定向/根位移/脚底检查"]\n  R --> B["状态融合或换资源"]\n  B --> G["游戏节奏与反馈验收"]'
    starts['D05'] = ('optional', '一个已选角色、两份来源清楚的动作包/说明卡；先试一个片段，不要求自己制作武打动作。')

    d06 = by_id['D06']
    _append_unique(d06, 'body', '轻战斗仍沿用资源复用原则：现成动作负责表演，玩法命中和反馈由游戏规则负责。只需把一个兼容攻击片段“套进”已有角色和木桩测试，不为证明能力从零做武打动画。')
    plans['D06'] = ('先用D05已验证的一段原地攻击，只确认动作能回到待机；不先加连招或敌人AI。', '动作播放后控制能恢复，主线移动/收集仍正常。', '再接一个有效窗口和木桩命中；空挥、同击一次、原地第二击与中断分别验证。', 'action_reuse')
    starts['D06'] = ('optional', 'D05已验证的一段原地攻击、现有控制器和一个木桩测试副本；动作来自资源复用，不要求原创。')

    # A compact validation contract for the authored strategy.
    if len(a08['m']) != 2 or len(a08['k']) != 2:
        raise ValueError('A08 fixed-camera depth must stay bounded')
    if 'Orbit' not in a08['stop'] or '套装' not in d01['title'] or '配色' not in d02['title']:
        raise ValueError('Fixed-view/kitbash emphasis did not apply')
    if 'Facade' not in c02['k'][1] or 'action_reuse' not in diagrams:
        raise ValueError('Fixed-view visual cheats or action reuse diagram missing')
    return lessons


def enrich_fixed_view(output, by_id, order, scenarios):
    page = '''# 项目美术与镜头基线：固定视角 + 套装二开\n\n本项目默认不是自由转镜头的通用3D游戏。目标是固定或有限镜头、角色可在场景中跑跳、风格化卡通、温暖漂亮配色；美术生产以“选优秀套装 → 拼装 → 二开 → 风格统一 → 游戏内验收”为主。完整方法见 [固定视角套装二开工作流](fixed-view-art-workflow.md)。\n\n## 人的长期重点\n\n人负责选择参考与主套装、提炼风格规则、决定镜头、挑出值得二开的资产、判断最终画面与玩法是否成立。AI负责参考拆解、候选组合、批量改色/命名/设置、局部建模或脚本、重复验证。Blender主要用于局部几何/模块/材质修改，Godot是最终玩家机位与交互验收点。\n\n## 课程中最重要的落点\n\nA08改为固定/有限镜头基础；C01按镜头串地图，C02按镜头美化世界；D01–D04集中训练资产套装二开、风格统一、资产库和场景组装；D05–D06训练现成动作包的兼容、融合与一段轻战斗。\n\n这不是要求把所有资产都“骗”成平面。Hero、Gameplay、Background按玩家能否接近、是否交互及镜头能否看到来分配成本；简化不能破坏路线、落点、命中和交互。\n'''
    output['curriculum/fixed-view-direction.md'] = page

    link = '[固定视角 + 套装二开工作流](fixed-view-art-workflow.md)'
    if 'curriculum/lesson-index.md' in output and link not in output['curriculum/lesson-index.md']:
        output['curriculum/lesson-index.md'] += '\n## 本项目的美术生产基线\n\n' + link + '：镜头先定构图；资产以套装复用、拼装和二开为主；动作以资源融合为主。\n'
    if 'START-HERE.md' in output and '固定/有限镜头' not in output['START-HERE.md']:
        output['START-HERE.md'] += '\n## 这个项目默认做什么样的3D\n\n固定或有限镜头、温暖风格化卡通、漂亮但不写实。美术重点是选择一套视觉基因接近的资产，拼装、二开、统一配色/材质，再回Godot玩家机位验收；不是从零建完所有模型。[查看工作流](curriculum/fixed-view-art-workflow.md)。\n'
    if 'README.md' in output and '固定或有限镜头' not in output['README.md']:
        output['README.md'] = output['README.md'].replace('把必要概念、审美判断和AI协作应用到同一个逐步成长的小游戏：', '围绕固定或有限镜头、风格化卡通和资产套装二开，')
        output['README.md'] += '\n[固定视角与套装二开](curriculum/fixed-view-art-workflow.md)\n'
    if 'curriculum/demo-quality.md' in output and '固定/有限镜头基线' not in output['curriculum/demo-quality.md']:
        output['curriculum/demo-quality.md'] = ('> 固定/有限镜头基线：最终Demo默认不要求玩家持续自由转镜头。每个区域按实际玩家画面验收；头晃、动态FOV、强震屏和运动模糊不是默认需求。美术优先套装拼装与二开，而不是从零重做全部网格。\n\n' + output['curriculum/demo-quality.md'])
    if 'curriculum/delivery-status.md' in output:
        output['curriculum/delivery-status.md'] = ('> 项目方向已进一步收敛为固定/有限镜头、风格化卡通、资产套装二开与动作资源融合；这是课件设计更新，不代表新镜头/美术/动作工程已经实现。\n\n' + output['curriculum/delivery-status.md'])
    if 'AGENTS.md' in output:
        output['AGENTS.md'] += ('\n## 固定视角与套装二开基线\n\n本项目默认固定/有限镜头、温暖风格化卡通。A08不恢复为自由Orbit主课；C01/C02按玩家镜头设计地图和世界；D01-D04以资产套装选择、拼装、二开、风格统一和复用为主；D05/D06以现成动作融合为主。不得把“原创”解释成必须从零建模/动画。\n')
    return output
