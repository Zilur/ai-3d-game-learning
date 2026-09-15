# AI协作与课程维护约定

唯一交付分支main。当前先完善课件并验证代表课堂，再补参考素材与Godot/Blender配套。没有明确切换阶段，不扩写game/、blender/、web/运行实现，不调用收费生成或索取密钥。

## 唯一编号

课程唯一编号由tools/course_order.py定义：A01–A08、B01–B13、C01–C12、D01–D07、E01–E07，共47课。ABCDE只是顺序分组，A最基础，不按软件含义归组。文件名、课内标题、前置、练习题号、对话启动框及索引必须一致。不再使用另一套展示号或兼容课号。

作者源中的LESSONS、SCENARIOS、PLANS、REVIEWS和准备材料索引也使用同一课号，不保留一套隐藏旧课程ID。技术概念为KN01–KN32，艺术词用ART；不与C组课号混淆。旧版本映射只保留在docs/numbering-migration.md。

## 内容与生成

curriculum/authoring/维护逐课正文、应用、对话、审核与准备材料；tools/build_course_materials.py生成学生稿、OpenMAIC全文和对话卡。先改源，再构建；不能只改生成MD。tools/numbered_navigation.py负责统一入口，不更改学习内容或评分。

M/K描述限定能力，不把整个学科升级必修。API、菜单、快捷键可查；常用可见参数适合亲调但不以机械拖滑杆证明掌握。学生稿不得包含教师答案。没有过程证据，不将模拟或文字解释标成软件应用通过。

起始材料缺失时明确分支，不让学员临时重建大工程。第一条提示必须自带首步、继续条件、下一步和结束证据；AI根据实际材料说明建议、执行、验证三个状态，不能假称已读电脑或保存进度。

## 校验

运行python3 tools/build_course_materials.py --check、python3 tools/check_course_numbering.py和python3 tools/validate_repo.py。现有质量/准备/对话检查保留；结构检查不证明课堂、视觉或学习效果。运行代码另按实际固定版本验证，区分历史结果与新结果。

openmaic/vendor是固定上游参考，保留原字节、许可证和摘要，不自动执行。参考链接、临摹、公开分发的条件分别核对；密钥、个人日志和未授权原作不进入公开仓库。
