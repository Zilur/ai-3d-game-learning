"""One-time exact-anchor activation of the reviewed authoring data. No engine/model calls."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def once(path, old, new):
    text = path.read_text(encoding='utf-8')
    if new in text:
        return
    if text.count(old) != 1:
        raise RuntimeError('Unexpected source anchor in ' + str(path) + ': ' + repr(old))
    path.write_text(text.replace(old, new, 1), encoding='utf-8')


def main():
    builder = ROOT / 'tools/build_course_materials.py'
    once(builder, 'from demo_coach import prepare_lessons, enrich_demo, validate_coaching\n',
         'from demo_coach import prepare_lessons, enrich_demo, validate_coaching\nfrom quality_review import apply_review, enrich_review\n')
    once(builder, '    lessons = prepare_lessons(lessons, sources)\n',
         '    lessons = prepare_lessons(lessons, sources)\n    lessons = apply_review(lessons, ROWS, sources)\n')
    once(builder, '    enrich_demo(output, by_id, ORDER, ROWS, DISPLAY)\n',
         '    enrich_demo(output, by_id, ORDER, ROWS, DISPLAY)\n    enrich_review(output, by_id, ORDER, ROWS, DISPLAY)\n')
    once(builder, "manifest = {'version':'v6-guided-demo'", "manifest = {'version':'v7-audited-collaboration'")
    # Preserve the existing 0-2 rubric and thresholds; clarify unobserved vs wrong.
    mastery = ROOT / 'assessments/mastery.md'
    once(mastery, '|预测|错误或无证据|', '|预测|已显示错误或违背题干条件|')
    once(mastery, '## 统一0–2评分锚点\n',
         '## 统一0–2评分锚点\n\n未提交或无法观察的证据先记“待验证”，不自动等于不会。文字推理与真机应用分别记录；下表只评分已呈现的表现。具体例子见[评分校准](grading-calibration.md)。\n')
    # Keep the same clarification inside all generated teacher inputs.
    source = ROOT / 'tools/quality_review.py'
    once(source, "    text = text.replace('版本：Guided Demo v6｜2026-09-15', '版本：' + VERSION)\n",
         "    text = text.replace('版本：Guided Demo v6｜2026-09-15', '版本：' + VERSION)\n    text = text.replace('0=缺证据或错误', '0=已显示错误；无证据另记待验证')\n")
    # Retain all existing validation; add an independent consistency/corruption check.
    validator = ROOT / 'tools/validate_repo.py'
    once(validator, '    if errors:\n',
         '    reviewed = subprocess.run([sys.executable, str(ROOT / "tools/check_quality_review.py")], cwd=ROOT, check=False)\n    check(reviewed.returncode == 0, "AI collaboration/evidence review inconsistent")\n    if errors:\n')
    print('QUALITY ACTIVATION PASS: exact hooks; unchanged runtime and grade thresholds')


if __name__ == '__main__':
    main()
