"""Fixed-view visual effects, parallax and impact-feedback teaching overlay.
This is authored curriculum only; it does not claim effects are implemented in the game.
"""


def _append_unique(row, field, text):
    if text not in row[field]:
        row[field].append(text)


def apply_fixed_view_effects(lessons, scenarios, plans, diagrams, reviews, starts, sources):
    by_id = {row['id']: row for row in lessons}
    required = {'A08', 'B07', 'C02', 'C08', 'D06'}
    if not required <= set(by_id):
        raise ValueError('Fixed-view effects overlay missing required lessons')

    sources.update({
        'environment_fx': ('Godot Environment 与后处理', 'https://docs.godotengine.org/en/stable/tutorials/3d/environment_and_post_processing.html'),
        'renderer_fx': ('Godot 渲染器功能差异', 'https://docs.godotengine.org/en/stable/tutorials/rendering/renderers.html'),
    })

    # A08: define FOV in plain language and make camera effects optional, not forbidden.
    a08 = by_id['A08']
    a08['k'] = [
        'Perspective/Orthographic是两种投影选择；FOV（Field of View，视野角）只用于透视镜头，正交镜头主要调Size。',
        'Camera Zone、短促Camera impulse/Shake、轻微Dynamic FOV或Size Pulse都是按需镜头语言；先懂用途，再决定是否使用。',
    ]
    a08['stop'] = ('不推投影矩阵，不要求自由环绕镜头或复杂相机框架。动态FOV、镜头冲击、震屏不是禁用，'
                   '但只作为短促可选强调：先小幅、短时、可恢复，并提供降低/关闭镜头运动的方案；舒适度必须真人复核。')
    _append_unique(a08, 'body',
        'FOV是Field of View，中文可理解为“相机一次能看多宽”。在Godot的透视Camera3D里它是角度：更大通常看得更宽、透视感也更强；更小看得更窄、视觉上更像拉近。正交镜头不靠FOV控制范围，而主要用Size。所谓Dynamic FOV，就是事件发生时短暂改变FOV后再恢复，例如冲刺或重击强调；固定视角同样能用，只是不应让它持续漂移。')
    _append_unique(a08, 'body',
        '固定视角的“镜头不自由转”不等于“镜头完全不动”。可在强事件上使用很短的Camera impulse、轻微位移/旋转、透视FOV Pulse，或正交Size Pulse；普通拾取、走路不必每次震屏。对容易晕3D的玩家，低运动模式应能关闭或显著降低Shake、FOV/Size Pulse、运动模糊和频繁切镜，同时保留闪光、粒子、声音和目标反应等非镜头反馈。')
    scenarios['A08']['keep'] = ('角色速度、跳跃、碰撞与关卡尺度保持；先建立静态镜头基线。事件型FOV/Size Pulse或Shake若后续采用，'
                                 '必须短促、能恢复且不能改变输入/碰撞规则。')
    scenarios['A08']['risk'] = ('检查AI是否把局部强调做成持续镜头漂移、频繁动态FOV、强烈震屏或头晃；'
                                 '同时避免另一极端——误以为固定视角绝不能有任何镜头反馈。')
    if 'fixed_camera' not in a08['sources']:
        a08['sources'].append('fixed_camera')

    # B07: teach feedback layers early, with low-motion alternatives.
    b07 = by_id['B07']
    if len(b07['k']) == 1:
        b07['k'].append('短促Camera impulse、轻微FOV/Size Pulse属于可选强调；静音与低镜头运动时仍应能读懂结果。')
    _append_unique(b07, 'body',
        '固定视角特别适合“局部效果清楚、镜头效果克制”的反馈分层：先有目标本身的缩放/闪光/消失，再加少量粒子与声音；重要事件才考虑一次很短的镜头冲击。镜头效果是加分层，不是成功状态本身。')

    # C02: explicit fixed-view style families and parallax/depth vocabulary.
    c02 = by_id['C02']
    c02['k'] = [
        'Set dressing、Focal point、Negative space用于场景布置、焦点与留白。',
        'Facade/Shell、Billboard、Forced Perspective、Parallax（视差）与Atmospheric Perspective（空气透视）是固定视角常用的深度/背景手段；玩家可达处仍按玩法验收。',
    ]
    _append_unique(c02, 'body',
        '固定视角常见的视觉方向可以先认识而不要求全做：①温暖绘本/童话Storybook；②柔和Low Poly；③玩具/黏土/微缩Diorama；④Toon/Cel Shading卡通渲染；⑤Hand-painted手绘感低写实；⑥Paper-craft/Cutout纸艺剪贴感；⑦Pastel/Cozy柔和粉彩；⑧Stylized Fantasy风格化幻想。风格不是滤镜名字，仍要落到比例、剪影、色盘、材质、边缘、光影与细节密度。')
    _append_unique(c02, 'body',
        'Parallax（视差）就是观察位置变化时，近处和远处在画面里的相对位移不同，从而增强深度。透视3D在相机平移/移动时天然更容易出现这种深度差；纯正交镜头不会靠远近自动缩小物体，因此若想要明显层次，常通过前景/中景/背景分层、人工不同速度偏移、遮挡、阴影、雾与色彩层次来“设计视差”。固定镜头完全不移动时，不要为了视差强行晃相机，仍可用遮挡、透视比例、空气透视和前中后景建立深度。')
    _append_unique(c02, 'body',
        '常用固定视角构图手段还包括：Foreground framing前景框景、Silhouette层次、Landmark地标、Forced Perspective强制透视、远景Facade/Shell、Billboard/Cross-plane植被、局部DOF营造微缩感，以及不可达背景的夸张比例。每一种都以玩家实际机位“不穿帮、不挡玩法”为验收。')
    if 'environment_fx' not in c02['sources']:
        c02['sources'].append('environment_fx')

    # C08: rendering/post effects catalogue, renderer-aware and bounded.
    c08 = by_id['C08']
    c08['k'] = [
        'Lightmap/GI/反射探针知道用途即可。',
        'Tonemapping/Exposure、Color Adjustments、Glow、Fog、SSAO、DOF与自定义后处理知道各自解决什么；先核对渲染器支持，不要求全开。',
    ]
    _append_unique(c08, 'body',
        '固定视角风格化游戏常见的“先试低成本、再按需加”渲染工具：①Tonemapping/Exposure控制整体亮度与高光压缩；②Color Adjustments或LUT思路统一色调；③Glow/Bloom让星星、魔法和灯有柔和光晕；④Fog/高度雾分离前中后景；⑤SSAO/接触阴影帮助物体贴地；⑥DOF在微缩/静态构图中突出焦点；⑦描边/Rim Light增强卡通轮廓；⑧粒子、Trail和局部Emission负责事件效果。不要一次全开，先按“画面问题→一种工具→同机位对照”验证。')
    _append_unique(c08, 'body',
        '渲染器能力不同：Fog、Tonemapping、Glow和颜色调整较普遍；Volumetric Fog、SSR、SSIL等更依赖具体渲染器，SSAO也并非所有目标都支持。课程因此不把某个高级效果当必修；先确定目标设备与渲染器，再让AI核对当前版本支持并提供可回退方案。屏幕空间效果还会受“画面外/被遮挡信息不可见”等限制，不能只凭一张截图判断稳定。')
    _append_unique(c08, 'body',
        '对本项目推荐的优先顺序是：先相机与构图→主光/环境→色盘/材质→Tonemapping/Exposure→少量Glow/Fog→需要时再试AO、DOF、描边或自定义后处理。漂亮不是“特效越多”，而是焦点、层次、配色和玩法可读性一起成立。')
    if 'environment_fx' not in c08['sources']:
        c08['sources'].append('environment_fx')
    if 'renderer_fx' not in c08['sources']:
        c08['sources'].append('renderer_fx')

    # D06: fixed-view combat impact stack, with low-motion alternative.
    d06 = by_id['D06']
    d06['k'] = [
        'Hitbox/Hurtbox、方法事件轨道、Hit stop和Root Motion知道用途，不要求全部采用。',
        'Hit flash、Impact particles、Trail、目标反应、短促Camera impulse/Shake，以及透视FOV Pulse或正交Size Pulse是可组合的打击感层；不要求每层都上。',
    ]
    _append_unique(d06, 'body',
        '固定视角的打击感可以非常强，不需要自由相机。建议按层叠加而不是只靠震屏：第一层是玩法命中真的成立；第二层是目标反应（姿态、轻微后坐/位移、Squash等）；第三层是Hit flash、冲击粒子、武器Trail与声音；第四层才是很短的Hit stop、Camera impulse/Shake；透视镜头可选轻微FOV Pulse，正交镜头可用Size Pulse或极小镜头位移。每次只加一层做A/B。')
    _append_unique(d06, 'body',
        '“强震屏”不是禁用，而是不该成为所有攻击的默认。普通攻击可主要靠Hit stop、目标反应、粒子/Trail和声音；重击/Boss事件才提高镜头冲击。为容易晕3D的玩家保留低运动版本：关闭或降低Shake和FOV/Size Pulse后，命中仍应靠目标闪光、粒子、声音和动作停顿被清楚感知。')
    scenarios['D06']['risk'] = ('检查AI是否用更大攻击距离、持续强Shake或大幅动态FOV掩盖命中时序问题；'
                                  '也检查镜头效果结束后是否恢复基线，低运动设置下反馈是否仍清楚。')

    diagrams['fixed_view_effects'] = ('flowchart LR\n'
        '  B["固定镜头与构图基线"] --> D["深度：前/中/后景 + 视差/遮挡/雾"]\n'
        '  D --> W["世界：光照 + 色调 + Glow/Fog/AO/DOF按需"]\n'
        '  W --> G["事件：Flash/Particle/Trail/Sound"]\n'
        '  G --> C["强事件：Hit stop + 短促Camera impulse/FOV或Size Pulse"]\n'
        '  C --> V["实际玩家机位 + 低运动模式验收"]')

    # Bounded validation: effects vocabulary must not silently become new M requirements.
    for ident in required:
        row = by_id[ident]
        if ident != 'E06' and len(row['m']) != 2:
            raise ValueError(ident + ': effects overlay changed M depth')
        if not (1 <= len(row['k']) <= 2):
            raise ValueError(ident + ': effects overlay exceeded K depth')
    if 'FOV（Field of View' not in '\n'.join(a08['body']):
        raise ValueError('FOV plain-language explanation missing')
    if 'Parallax' not in '\n'.join(c02['body']) or 'Glow' not in '\n'.join(c08['body']):
        raise ValueError('Fixed-view depth or rendering catalogue missing')
    if 'Camera impulse' not in '\n'.join(d06['body']):
        raise ValueError('Combat camera feedback catalogue missing')
    return lessons


def enrich_fixed_view_effects(output, by_id, order, scenarios):
    page = '''# 固定视角3D：镜头、视差、渲染与打击感速查\n\n本页是项目视觉语言目录，不是“全部都要打开”的效果清单。默认目标是固定/有限镜头、温暖唯美、风格化卡通、低眩晕。先保证构图和玩法清楚，再按问题选效果。\n\n## 1. FOV到底是什么\n\n**FOV = Field of View，视野角。** 只对透视相机直接成立。FOV大，通常一次看到更宽，透视感更明显；FOV小，看得更窄，视觉上更像拉近。Godot的正交Camera不用FOV控制范围，主要看`Size`。Dynamic FOV就是事件中短暂改变FOV再恢复；固定视角也可以用，例如冲刺或重击的一次轻微Pulse，但它不是持续运镜。\n\n## 2. 固定视角常见画面方向\n\n- **Storybook / 童话绘本**：柔和形状、暖色关系、哑光材质、清楚焦点。\n- **Soft Low Poly**：简洁大形、低细节噪声、靠光色与剪影成立。\n- **Diorama / Miniature**：微缩场景、强构图，可配少量DOF。\n- **Clay / Toy-like**：圆润、可爱、材质统一但不要全部塑料高光。\n- **Toon / Cel Shading**：明暗分层、描边或Rim可选，轮廓优先。\n- **Hand-painted Stylized**：低写实手绘感，颜色与纹理承担较多风格。\n- **Paper-craft / Cutout**：纸艺、剪贴和层叠感，适合明显前中后景。\n- **Pastel / Cozy Fantasy**：柔和粉彩、低攻击性对比、温暖光照与少量发光点。\n\n## 3. 深度与视差\n\n**Parallax / 视差**：观察位置变化时，近处和远处在画面中相对移动不同，让人感觉“有深度”。透视3D在相机移动时天然容易产生；纯正交不会靠远近自动缩小，所以常用人工分层偏移、遮挡、阴影、雾和色彩层次补深度。\n\n常用手段：前景框景、前/中/后景分层、Landmark、遮挡关系、Forced Perspective、Facade/Shell、Billboard/Cross-plane植被、空气透视/雾、远景降饱和/降对比、必要时少量DOF。固定镜头完全不移动时，不为了“视差”强行晃相机。\n\n## 4. 世界渲染常用工具\n\n|工具|主要解决什么|本项目建议|\n|---|---|---|\n|Tonemapping / Exposure|整体亮度、高光压缩|常用，先于复杂后处理|\n|Color Adjustments / LUT思路|统一色调与对比|常用，但先保证材质/光照本身合理|\n|Glow / Bloom|星星、魔法、灯的柔光|常用少量，防止全场发光|\n|Fog / Height Fog|前中后景分离、氛围|很好用，先低密度|\n|SSAO / 接触阴影|物体贴地、缝隙层次|按渲染器/设备验证|\n|DOF|焦点与微缩感|少量、静态构图优先；玩法中慎用|\n|Outline / Rim Light|卡通轮廓、角色可读性|按风格选择|\n|Particles / Trails|拾取、魔法、攻击事件|高性价比，保持方向/寿命清楚|\n|Custom Post FX|特殊滤镜、局部效果|高级按需，不做基础门槛|\n\nGodot不同渲染器支持并不完全一致；高级效果先核对当前版本、Forward+/Mobile/Compatibility与目标设备，再决定采用。\n\n## 5. 固定视角也可以有很强的打击感\n\n推荐从“非镜头反馈”开始：**命中规则 → 目标反应 → Hit flash → Impact particle → Weapon trail → Sound → 短Hit stop**。只有更重要的重击再追加**短促Camera impulse/Shake**；透视镜头可选很轻的**FOV Pulse**，正交镜头用**Size Pulse**或极小位移替代。\n\n不要把所有攻击都做成全屏大震动。低运动模式关闭Shake/FOV/Size Pulse后，玩家仍应该靠闪光、目标反应、粒子、声音和Hit stop判断命中。\n\n## 6. AI怎么协作\n\n让AI负责：搭A/B版本、暴露1–2个参数、核对Godot版本/渲染器支持、记录原值与恢复路径。人负责：选效果目标、判断强度、看焦点有没有被抢、检查是否晕、确认低运动模式仍成立。AI最容易犯的错误是一次堆太多效果、把漂亮截图当运行稳定、忘记恢复FOV/Size/Shake状态，或推荐当前渲染器不支持的功能。\n\n## 7. 学习顺序\n\nA08先学固定镜头与FOV/Size；B07第一次练反馈分层；C02学习视差/深度与固定视角美术；C08学习实时渲染与后处理选择；D06在真实攻击中组合Hit stop、Flash、粒子、Trail、Sound与可选镜头冲击。\n'''
    output['curriculum/fixed-view-effects.md'] = page

    link = '[固定视角效果/视差/打击感速查](fixed-view-effects.md)'
    if 'curriculum/lesson-index.md' in output and link not in output['curriculum/lesson-index.md']:
        output['curriculum/lesson-index.md'] += '\n## 固定视角视觉语言\n\n' + link + '：FOV、正交/透视、视差、前中后景、Glow/Fog/DOF/AO、描边与固定视角打击感。\n'
    if 'START-HERE.md' in output and 'fixed-view-effects.md' not in output['START-HERE.md']:
        output['START-HERE.md'] += '\n\n想先知道固定视角有哪些视觉手段，可看 [镜头、视差、渲染与打击感速查](curriculum/fixed-view-effects.md)。\n'
    if 'curriculum/demo-quality.md' in output:
        output['curriculum/demo-quality.md'] = output['curriculum/demo-quality.md'].replace(
            '头晃、动态FOV、强震屏和运动模糊不是默认需求。',
            '头晃、持续动态FOV、持续强震屏和运动模糊不是默认需求；重击可用短促、可关闭的FOV/Size Pulse或Camera impulse，并另验低运动模式。')
    if 'AGENTS.md' in output and '固定视角效果语言' not in output['AGENTS.md']:
        output['AGENTS.md'] += ('\n## 固定视角效果语言\n\n固定镜头不等于完全静止。可以用短促Camera impulse/Shake、透视FOV Pulse或正交Size Pulse强化重要事件，但必须恢复基线并提供低运动替代。C02负责视差/深度与固定视角画面语言，C08负责渲染/后处理边界，D06负责打击反馈分层。不得把所有效果同时开启当成高质量。\n')
    return output
