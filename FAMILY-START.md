# 亲子学习入口：今天我来当小老师

做一个固定视角的3D小世界；每次只完成一件小事，再把自己的发现讲给爸爸或另一位陪伴者。

**家长先读：[开始使用](learning-system/README.md)。** 孩子不用看作者规格、评分JSON或整本软件文档。

我们的课堂：一个创作挑战 → 先预测 → 做一次对照 → 自己作选择、AI辅助实现 → 给爸爸讲并演示 → 换一个例子 → 下次短复习。

这是一层接在原47课上的亲子学习工具，不是另一套课号，也不替代现有Godot/Blender练习。现有固定/有限镜头、干净的风格化自然世界、资产套装二开主线不变。

[设计理念与研究边界](learning-system/design.md) · [爸爸怎样陪](learning-system/parent-guide.md) · [数据与提醒](learning-system/data-and-reminders.md) · [审查与后续工作](learning-system/audit-and-next.md)

**[先打开现成实验，不从零搭场景](LABS-START.md)**。每课0A列出实际文件、首步与局限。

## 今天只做这三件事

先让AI给一个小挑战，不一次讲完整课。完成后，让孩子用自己的话说“是什么、我改了什么、为什么这样判断”，并让爸爸试一下。最后由成人记录真实观察；没有观察到的就留待验证，不宣布已经掌握。

有一天忘记了，不需要补完所有旧题。下次最多取一至两项，重新找回即可。

## 第一件小作品之后

家长按需查看[从入门到小型商业级游戏的成长指南](learning-system/commercial-growth.md)与[知识深度/学习方法地图](learning-system/growth-knowledge-map.md)。不是要求孩子现在学完或必须收费发布。

运行`python3 tools/growth_workshop.py plan`选择当前阶段；`python3 tools/growth_workshop.py session independent --cycle first-small-game`生成一轮本地任务。仍然是先预测、补必要知识、做小实验、讲给爸爸、真实验证，再决定下一步。

[本轮项目复查与下一项工作](learning-system/project-review-2026-09-16.md)

## 现成主游戏与专项实验

[主游戏操作](WORLD-START.md)与[实验入口](LABS-START.md)已经接通。F5运行三段参考；先体验和解释，再在副本中作局部改动，不必从空场景准备。OpenMAIC课堂按家庭安排稍后生成。

## 把自己的改变留下来

需要改游戏时，在完整仓库运行`python3 tools/workspace.py create my-world`，只维护这一份工作副本。每课不重新建场景；在Inspector或已给标记上改一项、保存、重开、解释。

家庭会话默认生成给孩子的`TODAY-课号.md`和给AI的`SESSION-课号.md`，两份用途不同。爸爸用`observe 课号`生成短观察单，记录真实发现；新记录仍需确认，不自动打分。

[保存保护、工作副本、学习接续与独立运行](docs/usability-closeout.md)
