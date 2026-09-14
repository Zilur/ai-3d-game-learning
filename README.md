# AI时代的3D游戏与风格化美术学习

**当前主线：先完成课程Markdown，再验证OpenMAIC课堂，最后统一完善Godot/Blender配套。**

我们训练的是：能说清需求、看懂关键参数、预测结果、选择方案、验收AI改动。不是软件功能百科，也不要求不用AI手写所有代码。

## 从哪里开始

- 学员从 [START-HERE](START-HERE.md) 进入。
- 教师直接打开 [45份课件索引](curriculum/lesson-index.md)，每课都提供**学生讲义**和**可整份复制给OpenMAIC的教师输入**。
- 先看学习安排：[路线](curriculum/roadmap.md) · [两轮大纲审核](curriculum/outline-review.md) · [逐课自审](curriculum/lesson-review.md)。
- 看美术：[参考作品与艺术家](art/reference-gallery.md) · [美术词汇](art/visual-vocabulary.md) · [长期资产库思路](art/style-and-library.md)。

## 课程结构

|系列|内容|本轮课件数量|是否所有人必修|
|---|---|---:|---|
|B 初级|空间、场景、走跑跳、镜头、资产、材质、拾取、反馈、性能与排错|17|主线；B01分A/B两次学习|
|I 中级|角色与动画接入、资源复用、机关、UV、光照、交互、恢复与交付|12|按原型目标；I08导航可跳过|
|R 审美与美术|基础美术对话、训练眼睛、看作品，再到基底打磨和资产库|8|R01–R04穿插主线；R05–R08作为Blender美术进阶|
|X 动作复用|现成动作筛选、适配、武打表现节奏|2|选修；不从零做复杂动画|
|A 高级|测量、Shader、复杂旋转、大场景、多人认识、专项验收|6|按实际问题选修，不阻塞小游戏|

**45是独立课件输入数量，不是要求新手一次完成45堂课。** B01保留原编号但拆成A/B；原技术C01–C32编号与`assessments/`继续保留，美术新词使用ART编号，不制造第二套技术编号。

## 学习深度与考核

**M 必须掌握**：针对本课具体需求，会选、会调、会说明、会验收。关键M再做排错、换情境与隔次复测。**K 理解即可**：知道用途和需要时去哪里查，一道轻量情境题即可。按需查询的API、菜单和快捷键不做记忆考试。

每课有：任务卡 → 必要讲解 → 界面深度 → 互动实验 → 一项故障/反例 → 训练和反馈 → 必记要点 → 延迟变式。完整规则见 [学习合同](curriculum/learning-contract.md)、[考核蓝图](assessments/exam-blueprint.md)。

## 已完成与未完成

本轮完成45份教师课件输入及45份对应学生讲义的内容编写、结构校验与作者自审；新课堂尚未逐课调用OpenMAIC生成、运行和试教。已有游戏/网页/Blender材料保留，但**没有宣称每课都具备完整配套**。具体状态以 [交付进度](curriculum/delivery-status.md) 为准。

## OpenMAIC参考与维护

[官方Skill参考说明](openmaic/upstream-reference.md)保留固定上游提交、原文、许可证与摘要；参考文件不自动执行。它规定部署/生成流程，不替代课程教学设计。课件入口统一为`openmaic/lessons/`，旧`requirements/`仅作迁移入口。

人工编写的单课内容存于`curriculum/authoring/`；运行`python3 tools/build_course_materials.py`展开Markdown，`--check`确认两份输出没有漂移。这只是文档展开，**不调用大模型、不生成课堂、不改游戏实现**。学员无需学习这些工具。

[打印技术要点](print/必须牢记.md) · [打印美术要点](print/art-must-remember.md) · [下一阶段清单](docs/improvements.md)
