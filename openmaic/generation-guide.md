# 从Markdown到真正的互动课

本仓库维护教学目标、实验约束、题目和真实软件任务；OpenMAIC负责生成课堂表现。生成结果需要审核，不能保证逐字逐项实现。

## 当前四种输入

| 输入 | 验证什么教学形式 | 真机出口 |
|---|---|---|
| [B01空间](requirements/B01-3d-space.md) | 空间预测与门轴对照 | lab.tscn → Transform / Door pivot |
| [B04碰撞](requirements/B04-collision.md) | 控制变量与排错 | main.tscn → Wall |
| [B08材质](requirements/B08-material.md) | 视觉参数与因果区分 | lab.tscn → Material |
| [B10拾取](requirements/B10-pickup.md) | 事件顺序与重复触发 | star.gd / main.gd |

## 使用步骤

复制一份输入的完整正文，作为课程要求提交给已可用的OpenMAIC。不要只提交GitHub链接并假设它一定读取，也不把文件路径当已上传的文件。

先看生成大纲是否守住范围，再生成正文/互动。实际拖动每个滑块，测试Reset和错误分支，核对答案。平台功能不满足某项时，应标记缺失并改用Godot实操，不用“看起来能点”的页面冒充实现。

生成课堂通过 [审核清单](review-checklist.md) 后，完成对应真机任务，并用 [证据单](../assessment/evidence-template.md)记录。涉及评分的答案只在作答后揭示。

## 要不要一次生成全部课

不需要。已有B01体验反馈，下一轮先验证碰撞、材质、事件这三种不同形式，再按验证过的模板扩展。路线设计完整不代表每节生成课堂已经测试。

## 记录可复现条件

课程规格的提交号、OpenMAIC版本（已知才填）、模型/提供商（已知才填）、开关、生成日期、匿名试学记录。不要猜在线演示站使用了哪个模型。

只分享不包含访问码的课堂地址；API Key、模型提供商配置、原始学习者记录不要提交公共仓库。GitHub授权和OpenMAIC服务/API授权是两件事。

## 本版不自动调用服务

本地部署或API自动生成以后单独实现。本版没有调用OpenMAIC生成新课堂，也没有消耗生成服务额度。Markdown规范不依赖把OpenMAIC源码复制进课程仓库。
