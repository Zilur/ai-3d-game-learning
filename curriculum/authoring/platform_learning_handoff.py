"""Current supported platforms and explicit OpenMAIC learning-data boundaries."""

PLATFORM_NOTE = '**使用平台：仅 macOS 与 Windows。** 独立体验包和桌面导出仅面向这两个平台；上课与修改作品使用完整工程。\n'

APPEND = {
    'AGENTS.md': '\n## 使用平台与OpenMAIC学情边界\n\n\n用户交付仅macOS与Windows；不得恢复Linux导出预设/体验包。Linux可作内部无窗口/渲染测试，不是支持承诺。OpenMAIC最新能力按openmaic/capability-audit.md所核对版本描述；保留vendor原字节。生成规格、运行事实、能力判断和复习调度分开。公开输入默认无私人历史；可选openmaic_handoff摘要先预览确认，不上传、不评分，不宣称已经实现上游记录自动回传。\n',
    'openmaic/README.md': '\n## 学情与学习方法不是只有生成页面\n\n\n[阅读官方能力核查与本课程接入边界](capability-audit.md)。当前上游有测验/讨论/PBL记录及学习方法Skill，但本课程没有自动读取这些运行记录。公开教师输入默认不带个人历史；个性化可用成人确认的私人摘要附件，课后仍走报告核对与本地复习调度。\n',
    'openmaic/generation-guide.md': '\n## 学习方法与个体记录的分工\n\n\n普通概念课选少量learning-to-learn动作；专门补弱项再用feynman-learning；系列进深参考spiral-curriculum。它们是实际版本工作台中的可选技能，不是所有页面默认运行的功能。保留本课程固定课号/MK和亲子任务，不因加载技能而给孩子增加多套作业。\n\n`family_learning.py session A04 --openmaic`输出教师输入，默认不含私人历史。需要个体摘要时先用`python3 tools/openmaic_handoff.py A04`预览，成人确认后加`--confirm`生成独立私人附件；不放进公开课程或共享课堂。没有自动学情回传和自动打分。详情与源码证据见[能力核查](capability-audit.md)。\n',
}

def enrich(output):
    for path in ("README.md", "game/README.md", "LABS-START.md"):
        title, body = output[path].split("\n", 1)
        output[path] = title + "\n\n" + PLATFORM_NOTE + body
    for path, text in APPEND.items():
        output[path] += text
