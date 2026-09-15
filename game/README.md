# Godot工程｜统一参考解与独立小实验

导入 `project.godot`（从仓库根目录看是game/project.godot）。测试版本固定Godot4.7.2，Compatibility，标准GDScript版。不要只复制单个.tscn。其他版本/设备需重新验证。

## 按课程打开

|目的|场景|运行|
|---|---|---|
|A03起始练习|lessons/b02/starter.tscn|F6|
|A03完成参考|lessons/b02/reference.tscn|F6|
|A03故障|lessons/b02/broken.tscn|F6|
|空间/门轴/单球参数实验|scenes/lab.tscn|F6|
|B04双球固定参考对照|labs/material_lab.tscn|F6|
|完整星星收集参考解|scenes/main.tscn|F5|

F5运行项目主场景，F6运行当前场景。A03没有玩家，先学整体、外观和实例职责；不能把完整代码全部视为当前必修。[A03讲义](../curriculum/beginner/02-scene-node/lesson.md)

## 参考关卡

默认10颗星；WASD移动，Shift跑，Space跳，鼠标转镜头，Esc释放鼠标，点击场景重新捕获，R重开。主场景根节点的star_count允许0–10，测试0/1边界不靠硬编码计数。

Player在layer2（脚本位值2）查询环境layer1（位值1）；星星Area的mask=2检查玩家。不要把层编号和位值的所有情况当成同一个数字。Visual只负责显示，CollisionShape3D负责形状，事件和状态在脚本中；KN概念编号以主线概念地图为准。

源码分工：player.gd管输入/运动/镜头；star.gd管有效对象和一次性拾取；main.gd持有进度，HUD只显示；lab.gd构造实验界面（非学员必读）。可调参数暴露到Inspector。

参考工程不是成熟游戏框架，不包含正式角色动画、完整反馈音效/粒子、通用自动爬楼梯、存档、导航或手机输入。

## 材质实验说明

scenes/lab.tscn的Material页有可调球和邻近立方体，单独开灯来区分Emission与照明；labs/material_lab.tscn是双球A/B版本。两者目的不同，不要求一课都做。B04采用双球；共享材质的专门实验需要按讲义另做，不假称所有参考球默认共享。

## 自动验证

```sh
python3 tools/validate_repo.py
# 下列从仓库根目录执行
godot --headless --path game --editor --import
godot --headless --audio-driver Dummy --path game --fixed-fps 60 --script res://tests/smoke.gd
godot --headless --audio-driver Dummy --path game --script res://tests/b02.gd
```

自动测试检查参考程序，不给学员打分，也不证明画面、手感或目标硬件性能。真实执行结果与人工待验收项见[验证记录](../docs/validation.md)。
