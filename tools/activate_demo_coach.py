"""One-time, exact-anchor activation of the reviewed v6 authoring modules.
Only authoring/build tools change. Never touches game, Blender or web runtimes.
"""
from pathlib import Path
import pprint
import re
import runpy

ROOT = Path(__file__).resolve().parents[1]

def once(text, old, new):
    if text.count(old) != 1:
        raise RuntimeError('Unexpected source anchor: ' + repr(old))
    return text.replace(old, new, 1)

def main():
    builder = ROOT / 'tools/build_course_materials.py'
    scenario = ROOT / 'tools/scenario_sections.py'
    b = builder.read_text(encoding='utf-8')
    s = scenario.read_text(encoding='utf-8')
    if 'from demo_coach import prepare_lessons' in b:
        print('v6 is already activated; no second patch applied')
        return
    order = runpy.run_path(str(ROOT / 'curriculum/authoring/demo_extension.py'))['ORDER']
    b = once(b, 'from scenario_sections import validate_scenarios, decorate_lesson, enrich_output',
        'from scenario_sections import validate_scenarios, decorate_lesson, enrich_output, ROWS, DISPLAY\nfrom demo_coach import prepare_lessons, enrich_demo, validate_coaching')
    b, n = re.subn(r'^ORDER = .*$', 'ORDER = ' + repr(order), b, count=1, flags=re.M)
    if n != 1:
        raise RuntimeError('Missing canonical order')
    b = once(b, "{f'I{i:02}' for i in range(1,13)}", "{f'I{i:02}' for i in range(1,15)}")
    # This renderer contains counts only, not scene dimensions or game formulas.
    b = b.replace('45', '47').replace('180 local questions', '188 local questions')
    b = once(b, '    by_id = validate(lessons, sources)',
        '    lessons = prepare_lessons(lessons, sources)\n    by_id = validate(lessons, sources)\n    validate_coaching(by_id)')
    b = once(b, '    enrich_output(output, by_id, ORDER)',
        '    enrich_output(output, by_id, ORDER)\n    enrich_demo(output, by_id, ORDER, ROWS, DISPLAY)')
    b = b.replace("'version':'v5-application'", "'version':'v6-guided-demo'")
    b = once(b, "'units':[{'id':ident,'prerequisites'", "'units':[{'id':ident,'display':DISPLAY[ident],'dialogue':'curriculum/dialogues/'+ident+'.md','prerequisites'")
    s = once(s, 'import runpy\n', 'import runpy\nfrom demo_coach import dialogue_card, EXT\n')
    s = once(s, "'B13','B14','B16'))", "'B13','B14','B16','I13','I14'))")
    s = once(s, "FIELDS = {'place'", "ROWS.update(EXT['SCENARIOS'])\nFIELDS = {'place'")
    s = s.replace('45', '47')
    s, n = re.subn(r'^def ai_card\(row\):.*?(?=^def completion_card\(row\):)',
        "def ai_card(row):\n    return dialogue_card(row, ROWS[row['id']], DISPLAY)\n\n\n", s, count=1, flags=re.M | re.S)
    if n != 1:
        raise RuntimeError('Missing scenario renderer function')
    s = s.replace('Applied Curriculum v5', 'Guided Demo v6')
    s = once(s, "def mode(ident):\n", "def mode(ident):\n    if ident == 'X02':\n        return '可选轻战斗：隔离验证后并入训练角'\n")
    # Remove the per-lesson mandatory second mechanic that conflicted with the elective route.
    plan_path = ROOT / 'curriculum/authoring/conversation_plans.py'
    p = runpy.run_path(str(plan_path))
    p['PLANS']['I04'] = ('从门或平台中只选一个；先列允许状态和实际运动的对象，不同时做两种机关。',
        '选门时开关位置正确；选平台时站上能按预期运动；当前只验所选机制。',
        '对已选机制检查重复触发、离开或恢复；通过后才讨论另一种机制，不强制实现。', 'space')
    plan_path.write_text('"""Reviewed lesson-specific coaching plans and concept diagrams."""\nPLANS = ' + pprint.pformat(p['PLANS'], width=110, sort_dicts=False) + '\n\nDIAGRAMS = ' + pprint.pformat(p['DIAGRAMS'], width=110, sort_dicts=False) + '\n', encoding='utf-8')
    ext_path = ROOT / 'curriculum/authoring/demo_extension.py'
    e = ext_path.read_text(encoding='utf-8')
    e = once(e, "        if row['id'] == 'I12':", "        if row['id'] == 'B08':\n            row['initial'] = '两个同尺寸且初始独立材质的球、灰箱、固定灯光相机；第二小实验再切为共享，结束时恢复独立。无GI/Glow。'\n            row['steps'] = ['固定右球，只调左球一项材质并作对照。', '切到共享修改范围实验：共享时两球一起变；分离后才恢复右球基线。', '恢复独立材质，分别比较Emission与独立光源对灰箱的影响。']\n        if row['id'] == 'I12':")
    capstone = dict(place='P06c/P07｜精致Demo的基础版与增强版验收', before='局部任务分别通过，但整段探索、风格和交付尚未连起来。', after='基础版三段地图十星循环可靠；增强版额外有可绕过的攻击木桩闭环。', task='先由我选择基础版或增强版，再按项目质量表验收。先跑从启动、三段探索、收齐到重开的完整路径；只修一个阻碍交付的问题，不增加新系统。', keep='基础十星、原角色/相机行为、已选风格与目标平台固定；未选战斗/导航不成为门槛。', tweaks=[('完整路线与三个玩家观察点（验收入口）','固定输入参数跑同一路线，比较一项改动','迷路、遮挡、反馈、完成和重开是否改善'),('训练角启用配置（本项目自定义，仅增强版）','开和关分别回归，不改星星计数','攻击防重/恢复与基础收集互不破坏')], accept=['实际从干净启动走完三段地图、十星、完成和重开，并说明三个视觉观察点的风格规则。','基础版按范围回归；增强版另提供空挥、同次去重、下一次可命中和取消恢复证据，无数据的性能不宣称达标。'], regress='用相同目标设备、分辨率和路线核对原控制、碰撞、资源往返、提示与恢复。', transfer='换一个已学的布局/材质/反馈约束，先说明影响范围再用最小对照验证。', risk='检查AI是否用漂亮截图代替连续游玩、把选修加入通关门槛、隐瞒失败或报告未执行的性能数据。')
    e = once(e, 'def prepare_lessons(lessons, sources):', "SCENARIOS['I12'] = " + repr(capstone) + '\n\ndef prepare_lessons(lessons, sources):')
    ext_path.write_text(e, encoding='utf-8')
    # Add supporting reference to every lesson that mentions runtime inspection.
    e = ext_path.read_text(encoding='utf-8')
    e = once(e, "SOURCES = {", "SOURCES = {\n 'v6_debug': ('Godot运行检查与可见碰撞工具', 'https://docs.godotengine.org/en/stable/tutorials/scripting/debug/overview_of_debugging_tools.html'),")
    e = once(e, '    return rows\n', "    for row in rows:\n        if row['id'] != 'A05' and 'v6_debug' not in row['sources']:\n            row['sources'].append('v6_debug')\n    return rows\n")
    ext_path.write_text(e, encoding='utf-8')
    builder.write_text(b, encoding='utf-8')
    scenario.write_text(s, encoding='utf-8')
    print('ACTIVATION PASS: exact renderer hooks, 47 lessons, single-mechanic and material-baseline fixes')

if __name__ == '__main__':
    main()
