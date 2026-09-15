# 单一作者源和构建顺序

学员直接看课程索引，不需要读这些Python数据。

1. beginner_a/b、intermediate、advanced、art、motion中的LESSONS是原始逐课内容。
2. demo_extension.py在构建时明确应用v6修订：新增I13/I14、替换X02、补I12/R08；它是当前这些修改的权威源，不改旧稳定ID。
3. application_*.py描述原应用场景，demo_extension.py的SCENARIOS给新增/修改场景。
4. conversation_plans.py逐课定义首步、证据门、下一步和概念图；不是统一套一句话。
5. site_*.py为原页面；demo_pages.py与tools/demo_coach.py产生当前导航/状态和对话页。后者在同一构建末尾覆盖旧页面，不并列两个权威入口。

运行 `python3 tools/build_course_materials.py` 后，再运行 `python3 tools/build_course_materials.py --check`、`python3 tools/check_lesson_delivery.py` 和 `python3 tools/validate_repo.py`。源和所有输出一次提交，不只改生成MD。检查失败不得绕过或删除测试。

构建仅把作者已写的内容排成Markdown，不调用LLM，不生成课堂，不操作Godot/Blender，不给个人学习打分。运行与学习证据必须另记。
