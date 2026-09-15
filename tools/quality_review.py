"""Apply authored quality review to the canonical course; no LLM or engine calls.
The check proves editorial consistency only, not teaching effectiveness or tool execution.
"""
from __future__ import annotations
import re
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUTHOR = ROOT / 'curriculum/authoring'
REVIEW_FILES = ('review_beginner.py', 'review_intermediate.py', 'review_art.py', 'review_optional.py')
REVIEWS = {}
for filename in REVIEW_FILES:
    part = runpy.run_path(str(AUTHOR / filename))['REVIEWS']
    if set(part) & set(REVIEWS):
        raise ValueError('Repeated reviewed lesson: ' + filename)
    REVIEWS.update(part)
QDATA = runpy.run_path(str(AUTHOR / 'review_question_edits.py'))
EDITS, P_TARGET, T_TARGET = (QDATA[k] for k in ('EDITS', 'P_TARGET', 'T_TARGET'))
# This lesson's second M is UI layout, not another state-machine objective.
REVIEWS['B08']['proof'] = [
    '隐藏UI仍更新权威进度；收齐后重开并再次拾取，实际状态为1/10且未完成。',
    '缩窄窗口后进度与重开按钮仍可见、可操作，选择布局调整并保存后重新运行。'
]
REVIEWS['B08']['target'] = 1
VERSION = 'Audited Collaboration v7｜2026-09-15'
FIELD_SET = {'finding', 'decision', 'ai', 'proof', 'diagnostic', 'target'}


def validate_review(by_id, records=None):
    records = REVIEWS if records is None else records
    if set(records) != set(by_id) or len(records) != 47:
        raise ValueError('Review must cover exactly the 47 current lessons')
    if set(P_TARGET) != set(by_id) or set(T_TARGET) != set(by_id):
        raise ValueError('Assessment target mapping is incomplete')
    questions = set()
    for ident, rec in records.items():
        if set(rec) != FIELD_SET:
            raise ValueError(ident + ': incomplete review schema')
        count = len(by_id[ident]['m'])
        if len(rec['proof']) != count:
            raise ValueError(ident + ': each M needs its own bounded practical evidence')
        if count != (0 if ident == 'E06' else 2):
            raise ValueError(ident + ': original M/K boundary changed')
        if rec['target'] not in (range(1, count + 1) if count else [0]):
            raise ValueError(ident + ': diagnostic maps to unknown M')
        if any(n < 1 or n > count for n in P_TARGET[ident] + T_TARGET[ident]):
            raise ValueError(ident + ': P/T maps outside declared M')
        if not count and (P_TARGET[ident] or T_TARGET[ident] or rec['proof']):
            raise ValueError('K-only topic acquired a practical gate')
        if len(rec['diagnostic']) != 4 or any(not isinstance(s, str) or not s.strip() for s in rec['diagnostic']):
            raise ValueError(ident + ': needs case, answer, hint and specific scoring anchor')
        if any(not isinstance(rec[k], str) or not rec[k].strip() for k in ('finding', 'decision', 'ai')):
            raise ValueError(ident + ': needs distinct roles and an actual review finding')
        if rec['diagnostic'][0] in questions:
            raise ValueError('Duplicated diagnostic case: ' + ident)
        questions.add(rec['diagnostic'][0])
        if any(not p.strip() for p in rec['proof']):
            raise ValueError('Empty evidence task: ' + ident)
    return True


def apply_review(lessons, scenarios, sources):
    by_id = {row['id']: row for row in lessons}
    validate_review(by_id)
    for row in lessons:
        ident = row['id']
        rec = REVIEWS[ident]
        if ident != 'E06':
            old = list(row['questions'])
            case, answer, hint, _anchor = rec['diagnostic']
            old[1] = ('D', '【教学构造情境，不是真实测量或某模型故障统计】' + case, answer, hint)
            for index, (kind, _q, _a, _h) in enumerate(old):
                if kind in EDITS.get(ident, {}):
                    old[index] = (kind, *EDITS[ident][kind])
            row['questions'] = old
            # The operation stations are the SAME objectives, not additional exams.
            scenarios[ident]['accept'] = list(rec['proof'])
        if ident == 'A07':
            row['k'] = ['Origin是对象原点；工具Pivot可临时选择别处，二者不必一致。']
        if ident == 'B05':
            scenarios[ident].update(
                place='P03｜更新静态外观并保留当前包装职责',
                task='只对当前静态视觉和已有包装/形状做一次源文件修改与重导入；记录四层来源和覆盖范围。当前尚未制作拾取、完成或重开，不提前创建这些功能。',
                keep='已有尺度、包装层、形状与标记保留；未实现的拾取/计数/重开不属于本次验收。',
                regress='重导入前后核对当前已有外观、尺寸、包装和形状；到B06/B08再补拾取/重开回归。',
                transfer='把箱子视觉换成路牌，保留当前包装和形状并再次重导入；不要求尚未学习的计数系统。')
            row['practice'] = '后续使用同一庭院中当前已有的静态资产包装，改源并重导入两次。核对尺寸/材质/已有形状和标记；拾取、计数、重开到对应课再验。本轮课件没有新增真机资产包。'
        if ident == 'B06':
            row['failure'] = '教学故障明确为通知监听者同步重入，唯一防重写在通知之后；普通顺序调用两次不一定重现。多层防重时分别观察接受/拒绝记录，不捏造重计结果。'
        if ident == 'D02':
            row['k'] = ['手绘感、渐变、描边、烘焙是可选手段。', 'Look development用于在固定条件下建立和验证外观规则，不要求复杂Shader。']
    sources.update({
        'review_body': ('Godot CharacterBody3D：velocity与物理delta', 'https://docs.godotengine.org/en/stable/classes/class_characterbody3d.html'),
        'review_area': ('Godot Area3D：重叠列表的物理更新时机', 'https://docs.godotengine.org/en/stable/classes/class_area3d.html'),
        'review_resource': ('Godot Resources：实例与共享引用', 'https://docs.godotengine.org/en/stable/tutorials/scripting/resources.html'),
        'review_tracks': ('Godot动画事件轨道：编辑器预览与运行不同', 'https://docs.godotengine.org/en/stable/tutorials/animation/animation_track_types.html'),
    })
    for ident, key in [('A05','review_body'), ('B04','review_resource'), ('C05','review_resource'), ('D06','review_area'), ('D06','review_tracks')]:
        if key not in by_id[ident]['sources']:
            by_id[ident]['sources'].append(key)
    return lessons


def target_text(ident, kind):
    if kind == 'K':
        return 'K｜理解用途即可；不要求实现'
    indices = P_TARGET[ident] if kind == 'P' else T_TARGET[ident] if kind == 'T' else [REVIEWS[ident]['target']]
    return '、'.join('M' + str(n) for n in indices) + '的限定子能力；不是整项真机通过证明'


def role_card(row):
    ident = row['id']
    rec = REVIEWS[ident]
    if not row['m']:
        return ('### 本课人和AI分别负责什么\n\n'
                '**我决定：** ' + rec['decision'] + '\n\n'
                '**AI协助：** ' + rec['ai'] + '\n\n'
                '**结束线：** 说明用途与本项目取舍即可；不运行软件、不做M评分。\n\n')
    return ('### 本课人和AI分别负责什么\n\n'
            '|责任|这课具体做什么|\n|---|---|\n'
            '|我必须作出的判断|' + rec['decision'] + '|\n'
            '|可以交给AI的制作|' + rec['ai'] + '|\n'
            '|我检查AI交付物|看修改对象/前后差异、实际执行记录及未验证项；先核对是否保留本课约束，再决定是否接入。|\n\n'
            '**不是手工熟练考试：** 重复劳动与代码可委托；常用可见参数适合亲调时先调一项，无障碍需要可由AI按已选值执行。必须能说明选择、观察和恢复，不要求机械地拖每个滑杆。\n\n'
            '**两种模式：** 练习时可问根因、看示范；独立验收时先由我提出选择/假设，AI只协助执行与记录。已透露本题根因或目标值，就记录“有提示”，再换未揭示答案的变式。\n\n')


def alignment_card(row):
    ident = row['id']
    rec = REVIEWS[ident]
    lines = ['## 1A. 必学内容、实操与题目如何对应', '',
             'M1/M2只是本课任务卡的两项能力序号，不是新的技术概念。查菜单/API不扣独立判断分。', '']
    if not row['m']:
        return '\n'.join(lines + ['本课全K。选一道用途情境即可结束；四道认识题是候选，不需要完成网络实现或全部考试。', ''])
    lines += ['|必须掌握到这里|本课实操题：做什么算有证据|可选配套题|', '|---|---|---|']
    for n, (objective, proof) in enumerate(zip(row['m'], rec['proof']), 1):
        qids = []
        if n in P_TARGET[ident]: qids.append(ident + '-P1')
        if n == rec['target']: qids.append(ident + '-D2')
        if n in T_TARGET[ident]: qids.append(ident + '-T3')
        lines.append(f'|M{n}：{objective}|{proof}|{", ".join(qids) or "直接用本行实操题取证，不另加术语测验"}|')
    lines += ['', '**最低学习路径：** 一次预测 → 一个能覆盖上述两项M的小实验/项目改动 → 一次结果解释。普通M做到即可；关键薄弱处再选一题诊断或隔次迁移，不把P/D/T全套加到每个术语上。',
              '**理解即可与停止线：** 任务卡中的K只检用途；按需查的界面、API、高级实现不进入本课操作门槛。只有已学且已存在的项目功能需要回归。', '']
    return '\n'.join(lines)


def decorate_review(text, row, teacher=False, dialogue=False):
    ident = row['id']
    rec = REVIEWS[ident]
    if '### 本课人和AI分别负责什么' in text:
        raise ValueError(ident + ': double application of review')
    anchor = '### 复制第1框开始；以后每次只发当前一步'
    if text.count(anchor) != 1:
        raise ValueError(ident + ': missing copyable-dialogue anchor')
    text = text.replace(anchor, role_card(row) + anchor, 1)
    # Embed responsibilities IN the first copied prompt, not only outside it.
    prompt_anchor = '先读取我已提供的进度和材料，只问真正缺失的一项。'
    if text.count(prompt_anchor) != 1:
        raise ValueError(ident + ': unexpected first prompt')
    text = text.replace(prompt_anchor,
        '本课由我负责：' + rec['decision'] + '\n可以交给你：' + rec['ai'] + '\n'
        '请标明建议/已执行/已验证的区别。练习可提示；验收先等我作判断，已提示根因则如实记有提示。\n' + prompt_anchor, 1)
    text = text.replace('版本：Guided Demo v6｜2026-09-15', '版本：' + VERSION)
    text = text.replace('0=缺证据或错误', '0=已显示错误；无证据另记待验证')
    if not dialogue:
        a = '## 2. 必要讲解：先看现象，再给术语'
        if text.count(a) != 1:
            raise ValueError(ident + ': missing teaching anchor')
        text = text.replace(a, alignment_card(row) + '\n' + a, 1)
        for index, (kind, _q, _a, _h) in enumerate(row['questions'], 1):
            qid = f'{ident}-{kind}{index}'
            heading = '### ' + qid + '\n'
            if text.count(heading) != 1:
                raise ValueError(ident + ': missing question ' + qid)
            evidence_type = '一句用途解释即可。' if kind == 'K' else '先给判断与理由；要求操作时再提供过程/对照。仅答对文字不自动等于实际应用通过。'
            text = text.replace(heading, heading + '**考察范围：** ' + target_text(ident, kind) + '。' + evidence_type + '\n\n', 1)
        text = text.replace('## 6. 训练：先作答，再看反馈',
            '## 6. 训练：先作答，再看反馈\n\n题干中的日志、数值与AI建议均为标明的教学情境，除非另附运行证据，不是本项目实测。可以有多个合理假设：先给能区分它们的验证，而不是猜老师心中的唯一原因。', 1)
        if teacher:
            extra = ['## 11A. 本课诊断题的具体评分锚点', '']
            if not row['m']:
                extra += ['本课没有D题和M成绩。只核对用途解释；不生成深度排错或工具执行门槛。', '']
            else:
                extra += [f'**{ident}-D2｜{target_text(ident, "D")}**',
                    '**2：** ' + rec['diagnostic'][3],
                    '**1：** 方向合理但缺区分性验证/结果解释，或得到目标根因提示后才完成；继续一次最小补练。',
                    '**0：** 已给出的选择违背题干约束、以无关补偿代替原因检查，且不能用证据解释。尚未提交/无法观察的部分另记“待验证”，不能假定学员不会。',
                    '**可接受替代：** 不要求使用参考答案的术语或唯一路径；其他符合条件、可检验且可恢复的方案同样可得分。真实软件表现须另有对应过程证据。',
                    '**迁移安排：** D题已讲解时不拿原题重复作独立考试。换本课T题的对象/一个约束，先不给目标参数和根因；实现代码仍可由AI执行已由学员选定的方案。', '']
            a = '## 12. 生成后的验收清单'
            if text.count(a) != 1:
                raise ValueError(ident + ': missing teacher acceptance heading')
            text = text.replace(a, '\n'.join(extra) + '\n' + a, 1)
            text += ('\n- [ ] 本课M到实操题、P/D/T和项目证据可追溯，K未扩大成实现。\n'
                     '- [ ] AI先等学员判断；提示后的表现没有冒充独立掌握；同一题不反复凑分。\n'
                     '- [ ] 教学情境/模拟日志与真实运行分开，替代方案按证据评分，不按关键词或个人审美。\n')
    return text


def enrich_review(output, by_id, order, scenarios, display):
    validate_review(by_id)
    for ident in order:
        for folder, teacher, dialogue in [('curriculum/lessons',False,False), ('openmaic/lessons',True,False), ('curriculum/dialogues',False,True)]:
            key = f'{folder}/{ident}.md'
            output[key] = decorate_review(output[key], by_id[ident], teacher, dialogue)
    pages = runpy.run_path(str(AUTHOR / 'review_pages.py'))['PAGES']
    if set(pages) & set(output):
        raise ValueError('Review page collides with another source')
    output.update(pages)
    audit = ['# 逐课审查：AI分工、必要内容、题目与实际证据', '',
             '2026-09-15｜作者逐课审查，不是独立外部评审或学习效果试验。47课不增课时；46道诊断题重写，E06保持全K。其余P/T/K按必要性选择修订，不宣称所有旧题全部重写。', '',
             '|课号|本轮发现与修订理由|人必须作出的判断|实操证据入口|', '|---|---|---|---|']
    trace = {'version':'v7', 'lesson_count':47, 'diagnostic_count':46, 'units':[]}
    for ident in order:
        row, rec = by_id[ident], REVIEWS[ident]
        audit.append(f'|[{display[ident]} / {ident}](lessons/{ident}.md)|{rec["finding"]}|{rec["decision"]}|讲义1A及第8节；' + ('全K不设实操门槛' if not row['m'] else 'M1/M2分别对应本项目证据') + '|')
        qmap = []
        for i, q in enumerate(row['questions'], 1):
            qmap.append({'id':f'{ident}-{q[0]}{i}', 'kind':q[0], 'target':target_text(ident, q[0])})
        trace['units'].append({'id':ident, 'display':display[ident], 'm':row['m'], 'k':row['k'], 'human':rec['decision'], 'ai':rec['ai'], 'project':scenarios[ident]['place'], 'practical_evidence':rec['proof'], 'questions':qmap, 'status':'author-reviewed; classroom-and-learner-not-tested'})
    audit += ['', '## 审查后仍不能断言的事情', '',
              '课程输入能否让OpenMAIC稳定生成有效控件、学员负担是否合适、真机是否完成与隔次迁移是否成立，均需实际试学。结构检查不能证明题目有效性或AI能力上限。', '',
              '## 修正的典型错位', '',
              'A07的K由提前询问四元数改为Origin/Pivot；B05移除未学拾取和重开的硬门槛；B08把状态循环证据放M1、布局证据放M2；B06明确同步重入条件；D06用日志区分范围内重复攻击的两类原因。', '',
              '[AI协作核心与考察](../assessments/ai-collaboration.md) · [评分校准样例](../assessments/grading-calibration.md) · [打印卡](../print/ai-control-card.md)', '']
    output['curriculum/quality-review.md'] = '\n'.join(audit)
    import json
    output['curriculum/quality-trace.json'] = json.dumps(trace, ensure_ascii=False, indent=2) + '\n'
    navigation = ('> v7审查：[逐课检查](curriculum/quality-review.md) · [AI协作能力](assessments/ai-collaboration.md) · [评分校准](assessments/grading-calibration.md)。每课已有具体人/AI分工和M—实操—题目对应；新课实际效果仍待试学。\n\n')
    for key in ('README.md','START-HERE.md'):
        if key in output:
            # Keep the entry compact instead of accumulating old version banners.
            output[key] = re.sub(r'\A(?:> v[456][^\n]*\n\n)+', '', output[key])
            output[key] = navigation + output[key]
    output['curriculum/lesson-index.md'] += '\n[逐课质量审查](quality-review.md) · [AI协作考察](../assessments/ai-collaboration.md) · [必记卡](../print/ai-control-card.md)\n'
    output['curriculum/delivery-status.md'] = ('> v7：47课已核对具体人/AI职责与M操作证据，46道诊断题重写并有评分锚点；部分P/T/K修订。新课堂与新Demo未由本轮执行。[审查记录](quality-review.md)。\n\n' + output['curriculum/delivery-status.md'])
    output['AGENTS.md'] += ('\n## v7质量审查源\n\nreview_*.py保存逐课职责、诊断题、证据与审查说明；tools/quality_review.py在v6课程装配后应用。不得只改生成MD。更新运行build_course_materials.py --check、check_quality_review.py、validate_repo.py。结构检查只证明一致性，不证明教学效果。B05不能提前验B06/B08功能；E06全K不增实操门槛。\n')
    return output
