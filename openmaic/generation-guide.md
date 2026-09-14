# OpenMAIC生成与验收 · Focus v3

课程规格不是已生成课堂，Markdown路径也不是平台自动可读的附件。当前交付见[进度](../curriculum/delivery-status.md)。

## 输入前先锁定学习深度

按[路线](../curriculum/roadmap.md)、[概念停止线](../curriculum/concept-map.md)和[考核蓝图](../assessments/exam-blueprint.md)填写[模板](lesson-template.md)。一个requirement只处理一个课或微单元，包含产物、M、K、不展开、实验和对应题目。

M考判断/操作/验收；K只问用途；未引入和未选方向不生成考题。不得把完整跨阶段题库直接当作初级考试，也不因平台能生成更复杂模拟就增加本课要求。

## 最小流程

先用 `requirements/B01-3d-space.md`，默认只生成B01A。附加材料显式上传或提供平台可访问内容。其他工作坊尚需整理为独立requirement，不能说它们都已有生成成品。

检查大纲的M/K和停止线，再生成；逐一操作控件、Reset、问答和真机出口。记录课程输入版本、实际模型/平台版本、日期、真实课堂链接和验收，不记录Key。

## 生成验收

- 初始数值/单位/轴向/简化假设明确，单变量对照可重置。
- 首次回答前隐藏答案；不是只有动画播放，能亲自操作并解释。
- K不要求实现；M评具体能力；关键任务有一次排错/迁移。
- 不把网页说成Godot运行时，不伪造PBR效果或性能数字。
- 运行、生成、实操和学习效果分开记录；失败不能用流畅旁白掩盖。

## 接口边界

参考已读取的官方generate-flow：`POST /api/generate-classroom`的requirement是文本要求，其他字段需遵守所部署版本的文档。自定义“M/K”“实验”“题目”属于正文规格，不臆造API参数。

先检查 `GET /api/health` 和可用能力；供应商/密钥配置留服务端，不进入本仓库或HTML。提交得到jobId不代表已生成成功；查询原任务，不因短暂失败重复计费。只有真正成功的课堂URL才登记。

本轮没有部署、调用生成接口或安排自动任务。实际使用前仍须核对所安装版本：[官方生成流程](https://github.com/THU-MAIC/OpenMAIC/blob/main/skills/openmaic/references/generate-flow.md)。

## 试学

B01首版得到用户正向体验反馈；新版及整套课程未完成延迟验证。按重点能力记录提示程度和新情境表现，不用观看次数或题量代替掌握。
