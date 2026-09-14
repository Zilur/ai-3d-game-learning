# AI 时代 3D 游戏学习 · Foundation v2

用 Godot + Blender 做星星收集游戏；用 AI 减少机械劳动；用预测、实验、诊断和迁移证明自己真的懂。

**这是一套待持续验证的课程设计，不宣称“全球首创”或已被证明优于所有教程。** 学习者对 B01 首版反馈良好；新版学习效果仍需通过延迟测验和真机任务验证。

## 从哪里开始

1. 看 [三阶段路线图](curriculum/roadmap.md)，先只读初级。
2. 用 [B01 生成要求](openmaic/requirements/B01-3d-space.md) 生成互动课；或离线打开 `web/space-lab.html` 先实验。
3. 按 [真机练习单](curriculum/beginner/01-3d-space/practice.md) 操作，不要一开始阅读全部源码。
4. 做 [题目](assessments/question-bank.md)，再查 [答案与补练](assessments/answer-key.md)，记录 [学习证据](assessments/learning-log.md)。

## 导航

| 要找什么 | 入口 |
|---|---|
| 初级 / 中级 / 高级、每课交付物 | [roadmap.md](curriculum/roadmap.md) |
| 每个概念必须掌握还是应该了解 | [concept-map.md](curriculum/concept-map.md) |
| 学习方法与AI使用边界 | [课程原则](curriculum/course-design-principles.md) |
| 必记要点，可打印 | [必须牢记.md](print/必须牢记.md) |
| 64题与能力验收 | [assessments](assessments/mastery.md) |
| 完整互动课范例 | [B01](curriculum/beginner/01-3d-space/openmaic-spec.md)、[B04/B08/B10](curriculum/workshop-recipes.md) |
| Godot 游戏与材质实验 | [game/README.md](game/README.md) |
| 原创星星素材、Blender练习 | [blender/README.md](blender/README.md) |
| OpenMAIC生成与人工验收 | [generation-guide.md](openmaic/generation-guide.md) |
| 技术事实与版本边界 | [sources.md](docs/sources.md) |
| 已测 / 未测、改版记录 | [validation.md](docs/validation.md) |

## 直接体验

下载本分支 ZIP 后，双击 `web/space-lab.html`：离线空间实验，无账号、无CDN、无API。GitHub文件页只展示源码，不会直接运行HTML。

Godot 项目：在 Godot 4 标准版导入 `game/project.godot`，F6运行单个实验，F5运行收集游戏。游戏示例包含走、跑、跳、镜头、墙、平台、5颗星、计数、完成与重开；**不含角色动画、楼梯自动攀爬、音效或粒子成品**。这些是后续任务，不伪装成已实现。

## 当前交付与边界

已编写：三阶段课程设计、32概念分级、64训练题、独立答案、复习与实操评分、打印卡、4节详细教学规格、网页空间实验、Godot源码和原创glTF素材。

完整路线不等于每课已生成/试教。除用户体验过的B01首版外，新版OpenMAIC课堂尚未生成。Godot/Blender真机与目标硬件验证状态见验证记录。`main` 不自动合并；课程继续在PR中审查。

没有把OpenMAIC平台源码复制进学习仓库，没有上传API Key，也没有启用收费生成或自动部署。
