# OpenMAIC与本课程的学习闭环：能力核查

核查日期：2026-09-17。上游读取固定到 `THU-MAIC/OpenMAIC@2cbd011c1f08d963c94e7b4478c44c750ea6ed6e`。这是官方源码/教学技能核查，不是已部署站点、实际孩子或生成课堂的端到端试验。仓库内旧的官方生成Skill引用仍固定在原提交，不静默更新vendor，不运行生成或收费服务。

## 结论

OpenMAIC不是仅仅生成几页可点击的课件。核查版本具备多智能体授课与讨论、测验作答和评分反馈、课堂运行记录、项目制学习的过程记录与统计，以及可选的学习方法Skill。但“提供这些模块”不等于“为每个孩子自动维护跨课掌握模型并按日程复习”。

本课程也不只有内容：有四轴能力记录、具体错因、复测和本地复习队列。不过目前它是与OpenMAIC配合的本地学习伴侣，不是OpenMAIC内部已经安装、自动运行的学情插件。两边还没有自动双向同步。

## 逐项核对

|问题|上游核查结果|本课程实际状态|
|---|---|---|
|互动课堂和讨论|支持幻灯片、测验、HTML交互、PBL与多智能体讨论 [S1]|47课教师输入已备好；课堂成品由家庭稍后生成|
|作答是否能留下|Quiz有草稿/提交/已反馈状态，记录answers/results、attemptId、stageId/sceneId及learnerKey [S2–S3]|不会直接从上游数据库读取或自动导入本地成绩|
|记录存在哪里|默认浏览器RuntimeStore；配置持久化后可使用HTTP存储通路，不能笼统说“只在浏览器”或“自动跨设备同步” [S4–S5]|自己的学习数据默认在`.learning/family/state.md`；游戏存档另存|
|PBL能否观察学情|有概念事件、错误次数、提交、阶段回顾等统计；指标依赖已记录的事件，不是客观认证的长期掌握程度 [S6]|软件应用还需要Godot/Blender实际证据；不把课堂项目自动判作游戏实操通过|
|学习理论是否引入|有learning-to-learn、feynman-learning、spiral-curriculum等可选运行时Skill [S7–S10]|已把预测、解释、亲子讲回、提示渐撤、延迟复测等写进教练协议和逐课要求；不是每次加载所有方法|
|具体哪里不懂|讨论/测验/PBL可产生诊断线索；费曼Skill要求留下解释变化与下一轮目标，并明确预生成页面不能逐句动态诊断 [S8]|成人核对实际证据后记录basis/next_question/next_task/recheck；不是读到“我懂了”就记掌握|
|跨课概念成长|螺旋Skill安排重访并要求概念记忆，但明确平台不会替Skill自动维护概念模型，需在工作台对话记录和回读 [S9]|本地能力ID与四轴记录跨课保留；不是通用知识追踪算法或全学科画像|
|自动排期和提醒|本轮未核实到可直接承担本课程每日弱项队列/定时推送的通用闭环；不能凭学习法文字或存储模块宣称已实现|本地程序计算到期项，运行时刷新；ICS需成人导入日历；没有常驻后台或自动通知|
|OpenMAIC结果会自动进本地吗|上游runtime记录有接入基础，但不是本项目的桥接器|没有；当前是人工/AI整理草稿→成人核对→record --confirm|

上表判断以所读实现为界。没有搜索到某模块不等于证明任何版本都不存在；特别是托管站点、不同部署配置或后续版本，需要另查，不能套用本结论。

## 学习方法怎样用，而不是写一页“学习法介绍”

普通概念课优先采用`learning-to-learn`：围绕当前概念只选一两种学习动作，如先预测后验证、用自己的话解释、隔次回想。学生看到的是“先猜一下”“给爸爸演示”，不是内部教学术语。

需要专门检查某个弱项时，再采用`feynman-learning`：先讲→定位一两个缺口→适量提示→重新解释→换情境。全新且没有前置知识时可以先给最小示范，不让孩子猜空白概念；不因为采用费曼法就把每课扩成七至九份作业。爸爸是懂行的共创教练，不必装作什么都不懂；独立检查与共同探究分开记。

跨课进深使用`spiral-curriculum`的“这次新增什么关系/边界/迁移”原则。螺旋进深与隔天防遗忘的短复习是两回事。课程已有编号、M/K和前置，不授权生成器自行重排整套47课。

Skill文件存在或已进入工作台目录不代表每次默认启用，更不能证明生成后每个组件都遵循要求。使用实际版本的工作台选择/加载相应Skill；版本不具备时仍以本课程明文协议作为输入。不把斜杠名称当成所有托管界面都支持的API。

## 两套记录和一条尚未自动化的连接

课堂原始事实（题目/回答/反馈/讨论/项目过程）由OpenMAIC运行层保存。跨课教学判断（掌握哪一项、给过什么提示、具体混淆、下一次怎么查）由本地学习伴侣保存。它们用途不同，不应把一方分数直接拷贝成另一方掌握结论。

目前可用流程：

`公开教师输入 → OpenMAIC课堂 → 取本次必要作答/反馈＋爸爸观察 → 整理报告草稿 → 成人核对record --confirm → state.md → today/下一课摘要`

此前`family_learning.py session A04 --openmaic`**有意不包含私人学情**。普通`session A04`会携带少量本地摘要。这意味着教学方法已进入OpenMAIC输入，但个体旧错因不会仅凭`--openmaic`自动传进去。

本轮新增了单独的可选私人附件，见下节。这只补“把最少必要学情交给下一堂课”的手动通路，没有伪称自动拉取上游记录。

## 当前可以怎样使用

先按原工具生成不含私人历史的教师输入：

```sh
python3 tools/family_learning.py session A04 --openmaic
```

生成`.learning/family/OPENMAIC-A04.md`。使用私人课堂并确实需要带上旧错因时，再预览：

```sh
python3 tools/openmaic_handoff.py A04
```

成人读过摘要、确认使用范围后，再生成独立附件：

```sh
python3 tools/openmaic_handoff.py A04 --confirm
```

它只写`.learning/family/OPENMAIC-CONTEXT-A04.md`；已有同名附件不覆盖。需要更新时由成人保留/移走旧附件再生成，避免误用过期摘要。程序不上传、不评分、不改state.md，也不连接OpenMAIC。把该附件作为工作台对话上下文，而不是公开课堂内容；共享课堂不附带个人历史。Windows使用`py -3 -X utf8`代替`python3`。

课后用既有`observe`和空白`template`整理本次证据。没观察的软件应用留null；看过答案、跟提示完成、自己独立完成分开记。成人确认后才`record --confirm`，再运行`today`或生成下一课会话。不能用导出PPT/HTML/课堂ZIP代替学员运行记录。

## 真正自动化下一步要接什么（尚未实现）

应复用OpenMAIC现有runtime，而不是另造授课器。一个小适配器需要关联本地lesson/objective与上游stage/scene/attempt、本人学习者标识和版本；只读取成人授权的最小事实，保留时间、原答、反馈来源、提示/答案揭示情况。缺少“有没有提示”的数据就记未知，不能假定独立。

适配器先生成待确认报告，不直接宣布掌握；按稳定事件ID去重、允许更正/作废，错误不能覆盖旧档。确认记录后本地调度器更新队列，下次再提供少量摘要。软件证据依旧从Godot/Blender与家长观察取得，PBL统计不能包办。到时通知仍依赖明确选择的日历/后台执行器。

自动闭环的验收用同一名虚拟测试学员跨两课、关闭重开验证：旧错因能回读，重复事件不重复计数，有提示不记独立，失败不丢档，未授权数据不导出，到期任务能生成。上述上游端到端试验本轮没有运行，也不影响家庭稍后生成课堂。

## 可复核来源（官方固定提交）

- [S1 README-zh](https://github.com/THU-MAIC/OpenMAIC/blob/2cbd011c1f08d963c94e7b4478c44c750ea6ed6e/README-zh.md)
- [S2 Quiz runtime](https://github.com/THU-MAIC/OpenMAIC/blob/2cbd011c1f08d963c94e7b4478c44c750ea6ed6e/lib/quiz/runtime.ts)
- [S3 Quiz view state](https://github.com/THU-MAIC/OpenMAIC/blob/2cbd011c1f08d963c94e7b4478c44c750ea6ed6e/lib/quiz/view-state.ts)
- [S4 Runtime store](https://github.com/THU-MAIC/OpenMAIC/blob/2cbd011c1f08d963c94e7b4478c44c750ea6ed6e/lib/runtime/store.ts)
- [S5 Persistence bootstrap](https://github.com/THU-MAIC/OpenMAIC/blob/2cbd011c1f08d963c94e7b4478c44c750ea6ed6e/lib/persistence/bootstrap.ts)
- [S6 PBL completion stats](https://github.com/THU-MAIC/OpenMAIC/blob/2cbd011c1f08d963c94e7b4478c44c750ea6ed6e/lib/pbl/v2/operations/runtime/completion-stats.ts)
- [S7 Learning to Learn](https://github.com/THU-MAIC/OpenMAIC/blob/2cbd011c1f08d963c94e7b4478c44c750ea6ed6e/skills/agent-runtime/learning-to-learn/SKILL.md)
- [S8 Feynman learning](https://github.com/THU-MAIC/OpenMAIC/blob/2cbd011c1f08d963c94e7b4478c44c750ea6ed6e/skills/agent-runtime/feynman-learning/SKILL.md)
- [S9 Spiral curriculum](https://github.com/THU-MAIC/OpenMAIC/blob/2cbd011c1f08d963c94e7b4478c44c750ea6ed6e/skills/agent-runtime/spiral-curriculum/SKILL.md)
- [S10 Runtime skill registration tests](https://github.com/THU-MAIC/OpenMAIC/blob/2cbd011c1f08d963c94e7b4478c44c750ea6ed6e/tests/agent-runtime/skills.test.ts)

本课程实现：`tools/family_learning.py`、`tools/openmaic_handoff.py`、`learning-system/design.md`、`learning-system/data-and-reminders.md`。这些依据证明源码与规则的存在，不证明孩子已掌握、模型评分可靠或每次生成都符合教学设计。
