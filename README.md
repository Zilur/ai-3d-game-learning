# AI时代3D游戏学习 · Focus v3

用Godot与Blender做一个小型单机游戏。AI减少重复实现；学习者把精力放在目标、参数、因果判断、手感、美术取舍和验收。

**路线齐全不等于课程全部完成。** 初级B01–B16、中级I01–I12、高级A01–A06已有路线和学习深度；目前完整样板是B01，B04/B08/B10有详细工作坊，其余尚待逐课交付和试教。下一份完整课包应做B02，不是直接进入中级。

## 先看这三个入口

|问题|入口|
|---|---|
|现在做完了什么、下一步做什么？|[交付进度](curriculum/delivery-status.md)|
|每课必须会什么、哪些只要理解？|[逐课路线](curriculum/roadmap.md)、[学习深度合同](curriculum/learning-contract.md)|
|重点如何详考、理解项如何轻考？|[考核蓝图](assessments/exam-blueprint.md)、[评分规则](assessments/mastery.md)|

M＝必须掌握限定的判断/操作/验收能力；K＝理解用途即可。不考API记忆或底层算法。64道P/T为跨阶段题库，不是初级作业清单；K不做深题，未选高级专项不进入毕业条件。

## 学员路径

B01A → B02 → B04 → B03 → B05 → B01B → B06，再到B07–B16。每课只先看一个产物、2–3项M目标、必要的K提示和停止线。

使用[B01生成输入](openmaic/requirements/B01-3d-space.md)或离线网页 `web/space-lab.html`，再做[真机练习](curriculum/beginner/01-3d-space/practice.md)。按阶段抽[题目](assessments/question-bank.md)，最后查看[答案](assessments/answer-key.md)。不需要先读完所有源码和术语。

## 资料导航

[概念地图](curriculum/concept-map.md)限定32组能力的具体深度；[打印卡](print/必须牢记.md)只复习当前重点；[课程原则](curriculum/course-design-principles.md)规定AI与人的分工；[学习记录](assessments/learning-log.md)保留最少必要证据。

[B04/B08/B10工作坊](curriculum/workshop-recipes.md)、[Godot参考工程](game/README.md)、[Blender素材说明](blender/README.md)、[术语检索](glossary/core-3d.md)、[OpenMAIC模板](openmaic/lesson-template.md)、[生成验收](openmaic/generation-guide.md)、[技术来源](docs/sources.md)、[运行验证边界](docs/validation.md)。

## 工程与版本边界

本轮继续使用 **PR #1 / course/foundation-v1** 的三级课程。PR #2是另一套并行实现，题号和目录不相同，不要混读；本轮没有合并或删除任何分支。

本分支Godot源码含走跑跳、镜头、墙/平台、5颗星、计数/完成/重开和坠落复位，另有材质实验；不是每课独立起始/完成包，不含正式角色动画、自动爬楼梯或音效粒子成品。本分支引擎运行与Blender验证仍按验证记录待办，不能套用另一分支的测试通过。

B01首版有用户正向反馈；新版课堂未重新生成，整套方法未完成延迟学习效果验证。内容和题量不代表教学效果。本轮仅校准重点、难度和进度，不生成收费课堂、不部署网站、不合并main。
