"""Two explicit purposes; the default never reconstructs a ready lab."""
from pathlib import Path
import re
import runpy

ROOT = Path(__file__).resolve().parents[2]
BINDINGS = runpy.run_path(str(ROOT / 'curriculum/authoring/novice_learning.py'))['BINDINGS']
PROJECT_OPEN = '<details data-purpose="project">\n<summary>作品模式：明确要改自己的工作副本时才展开</summary>\n\n'
PROJECT_CLOSE = '\n</details>\n'


def experience_plan(ident):
    paths, first, limit, _stage = BINDINGS[ident]
    return first, '先作预测，再提供一项实际对照和解释；未覆盖的能力留待验证。', '在现成材料覆盖范围内选择一个参数或条件作变式，再恢复；不为了凑题重造系统。'


def experience_only(text):
    """Physically exclude project commands from the AI's default session input."""
    return re.sub(r'<details data-purpose="project">.*?</details>\s*', '', text, flags=re.S)


def project_note(first, second):
    return PROJECT_OPEN + ('当前默认是体验模式，以下任务不自动执行。只有学员明确说“我要改自己的作品”，并提供工作副本与本次验收，才一次选一项。不要复制第二套作业。\n\n'
        + '**作品实现候选一：** ' + first + '\n\n**作品实现候选二：** ' + second
        + '\n\n先核对已有对象；能局部修改就不重新创建。实现可交给AI，目标、保持项和验收由学员提出。\n') + PROJECT_CLOSE
