# AI 时代 3D 游戏学习

**从 [START-HERE.md](START-HERE.md) 开始。统一使用 main，不需要选择历史分支。**

Godot + Blender 是真实实验室，OpenMAIC 是互动课堂生成器，AI负责重复实现；学员负责目标、判断、手感、审美、性能取舍和验收。

学习闭环：**先预测 → 亲手操作 → 解释结果 → 修复一个错误 → 换场景应用 → 隔次复测**。不以背API、题量、观看时长或生成代码量代表掌握。

## 学什么、学到哪里

|路线|目标|当前状态|
|---|---|---|
|初级 B01–B16|小型星星收集游戏；建立空间、玩法、资产和验收能力|路线与深度齐全；B01样板、B02课包、B04/B08/B10工作坊；其余逐课包待补|
|中级 I01–I12|角色动画、复用、模块化、简单交互、存档和交付|路线和考核设计已有，不是全部课件/游戏已经完成|
|高级 A01–A06|按实际瓶颈选择专项|不作为做小游戏的全套必修要求|

**M 必须掌握：** 能选方案、操作、解释、排错；关键能力需要迁移验证。**K 理解即可：** 知道用途和何时查询即可，不深入实现。每课都有停止线，考试不得超出当前阶段。[学习深度合同](curriculum/learning-contract.md)

## 只看你当前需要的入口

|用途|入口|
|---|---|
|今天打开什么|[学习入口](START-HERE.md)|
|整体安排|[路线](curriculum/roadmap.md) · [32组概念的分阶段深度](curriculum/concept-map.md)|
|B02实际操作|[课包](curriculum/beginner/02-scene-node/lesson.md) · [本课题目](curriculum/beginner/02-scene-node/assessment.md)|
|生成课堂|[使用规则](openmaic/generation-guide.md) · [B01输入](openmaic/requirements/B01-3d-space.md) · [B02输入](openmaic/requirements/B02-scene-node.md)|
|后续工作坊|[B04碰撞 / B08材质 / B10事件](curriculum/workshop-recipes.md)|
|题库与考核|[考核蓝图](assessments/exam-blueprint.md) · [题库](assessments/question-bank.md) · [评分](assessments/mastery.md)|
|纸面复习|[必须牢记](print/必须牢记.md)，只复习已学阶段|
|运行示例|[Godot工程](game/README.md) · [Blender素材](blender/README.md)|
|做到哪了|[交付进度](curriculum/delivery-status.md) · [测试边界](docs/validation.md)|

## 开发与内容统一规则

概念编号以 `curriculum/concept-map.md` 为准，题库统一在 `assessments/`，不再并列两套C编号和0–2/0–3评分。源码来自整合后的单一工程，完整参考关卡默认10颗星，可用Inspector的star_count做0/1边界实验。

只更新main；使用小提交便于回退。确实需要临时分支时只保留一条，验证合并后清理，不长期维护平行教材。[AI协作规则](AGENTS.md)

大纲齐全不等于全部课堂生成、全部源码实测或学习效果已验证。技术测试和真人操作/延迟复测分别记录。

[本次整合说明](docs/consolidation.md) · [剩余优先事项](docs/improvements.md)
