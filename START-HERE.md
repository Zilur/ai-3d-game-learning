# 从这里开始｜只打开今天需要的东西

唯一学习入口是本仓库 `main`。不需要挑选历史分支，不需要先读完题库或所有打印卡。

## 今天学哪一课

首次学习：先用 [B01生成输入](openmaic/requirements/B01-3d-space.md) 生成课堂，或直接打开 [空间实验](web/space-lab.html)（下载后浏览器打开）。先完成B01A的位置、旋转、缩放，父/自身/世界轴和门轴可留B01B。

已完成B01A：进入 [B02灰盒课包](curriculum/beginner/02-scene-node/lesson.md)。只学场景、节点、实例与改动范围；当前不读完整角色脚本。

接下来按 **B01A → B02 → B04 → B03 → B05 → B01B → B06 → B07–B16**。稳定课号方便引用，实际先后由前置知识决定。[后续路线](curriculum/roadmap.md)

## 软件与入口

下载仓库ZIP并解压，或clone main；不要只下载单个.tscn。使用标准Godot（GDScript，不要求.NET），本仓库自动测试固定Godot4.7.2、Compatibility；其他版本需要重新验证。Blender到B07再准备，本地OpenMAIC部署不是开始学习的前提。

在Godot项目管理器导入 `game/project.godot`：

|本次目的|打开后运行|
|---|---|
|B02起始练习|`res://lessons/b02/starter.tscn`，F6|
|B02故障诊断|`res://lessons/b02/broken.tscn`，F6|
|空间/门轴/材质参数实验|`res://scenes/lab.tscn`，F6|
|B08双球对照|`res://labs/material_lab.tscn`，F6|
|完整星星参考解（默认10颗）|F5；WASD、Shift、Space，鼠标控制镜头，Esc释放，R重开|

B02没有玩家，是固定镜头的小实验。F5是完整参考解，不能当成从B02开始的必读源码。网页HTML在GitHub文件页面不能直接播放，下载后本地打开；目前未开启GitHub Pages，不能把仓库链接当已部署游戏。

## 一次学习只留下四样东西

先用一句话预测→亲手操作→解释一个错误→换对象再做。对应本课M能力，不逐词写长报告。

M必须掌握：做得出、判断得对、解释得清。K理解即可：知道用途和什么时候查，不需要深入实现。参见 [学习深度合同](curriculum/learning-contract.md)。打印只打印 [当前阶段要点](print/必须牢记.md)，不要先背全书。

截图与日志保存在自己电脑。可以使用 [记录模板](assessments/learning-log.md)，不要把姓名、私密学习记录、模型密钥或课堂访问码传入公开仓库。

## 卡住时

只有场景看不到：先确认运行的是哪一个场景、有当前Camera、节点没有隐藏，而不是立即重写项目。

AI给了大量改动：保留副本，先列出允许改的节点/文件，只应用最小变更；重新运行已有功能。答案可以查，独立判断仍需在另一个变式中验证。

“有大纲”“有源码”“测试通过”“课堂已生成”“学员已掌握”是不同状态，查看 [交付进度](curriculum/delivery-status.md) 和 [验证记录](docs/validation.md)。
