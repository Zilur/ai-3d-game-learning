# Godot 示例与概念实验

目标版本：**Godot 4.7.2 standard / GDScript，Compatibility**。工程使用基础几何，不需要第三方插件、C#、账号或API密钥。验证情况见 [验证记录](../docs/validation.md)。

## 打开

在Godot项目管理器选择Import，选择这里的`project.godot`。等待首次OBJ导入完成，F5启动星星关卡。

在文件系统打开`scenes/lab.tscn`，F6只运行实验场景；也可在游戏中按Esc，再点Concept labs。界面使用英文短词，中文讲义按同名控件说明，不打包字体。

## 操作

WASD移动，Shift跑，Space跳；鼠标转镜头；Esc释放鼠标，左键重新捕获；R或Restart重开。释放鼠标不等于暂停游戏。摔落会回到出生点，已收集进度保留；R是整局重开。

主场景Root的`star_count`可设0–10，供边界测试。星星由main.gd生成：编辑器中Stars初始为空，运行后在Remote场景树查看，不能误以为资源丢失。

默认输入由player.gd在运行时补入InputMap；已在Project Settings配置的同名Action不会被覆盖。要永久改键，先在Project Settings → Input Map创建这些Action并配置，而不是只改一次运行内存。

## 每课只看对应位置

| 内容 | 打开什么 | 只动哪些东西 |
|---|---|---|
| B01 C01–C03 | lab.tscn → Transform / Door pivot | 位置、Yaw、Scale、父旋转、门轴 |
| B03 C07 | player.gd / Player Inspector | walk_speed、run_speed |
| B04 C05/C06 | main.tscn 的Wall；player.tscn | Visual.visible、Shape.disabled、layer/mask |
| B05 C08 | Player Inspector | gravity、jump_velocity |
| B06 C09 | Orbit/SpringArm3D/Camera3D | spring_length、FOV、mouse_sensitivity |
| B08 C12/C13 | lab.tscn → Material | roughness、metallic、emission、独立灯 |
| B09 C11 | star.tscn的Visual | 换自己的GLB外观，保留Area/脚本 |
| B10 C15 | star.gd | consumed锁与事件顺序 |
| B12 C16 | main.gd | state→UI、实际总数、重开 |
| B14 C19 | Debugger/Profiler | 固定条件测量，不改完所有效果才测 |

## 场景结构

`Player`负责运动；`Visual`只负责外观朝向；`Orbit/SpringArm3D`控制镜头。地面、墙与坡是StaticBody+简单Shape。`Star`是Area，不阻挡人物；先标记consumed，再发事件，再释放。`Main`拥有计数与完成状态。

世界在第1物理层，玩家在第2层；玩家检测第1层，星星Area检测第2层。相机臂检测世界并排除玩家。

## 实验约定

先在Prediction字段写预测，再操作；解释默认隐藏，操作后再揭示。这个字段只在本次运行内保存，不是评分系统，退出前复制到本地证据单。按Reset恢复实验物体，不把结果截图当独立掌握证明。

Transform模式提供World/Parent/Object +X对照；对照前Reset，并保持Scale=1。物体带有+X方向的鼻部，避免对称球体看不出朝向。Door模式的两种轴在关门时应有同一可见门板位置。

Material模式固定相机和主光。独立的邻近光源是用来区分“自己亮”和“照亮邻物”，不是Emission自动照明的证明。本项目不预置GI或Glow效果。

## 当前边界

不是通用商业角色控制器：没有自动爬阶、复杂移动平台、土狼时间、输入缓冲、手柄映射或全平台适配。音效/粒子作为B11扩展练习，参考工程只含旋转、浮动和文字反馈。中级动画、导航、存档尚未实现。

## 测试

安装目标Godot后，在仓库根目录执行：

```sh
python3 tools/validate_course.py
godot --headless --path game --editor --import
godot --headless --path game --script res://tests/smoke.gd
```

若命令名不是`godot`，替换成实际可执行文件路径。headless检查能验证导入、脚本、部分物理/事件，不验证画面审美、鼠标手感或目标设备性能。人工回归见 [验证记录](../docs/validation.md)。
