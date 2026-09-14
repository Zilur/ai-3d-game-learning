# Godot 星星实验工程（参考解，不是第一课必读源码）

目标API为Godot 4.5及以后的4.x标准版GDScript，默认Compatibility渲染器。尚未在本轮环境启动引擎；不能据此宣称跨版本/平台运行已通过。版本记录见[验证状态](../docs/validation.md)。

## 启动

下载含本分支内容的完整仓库，在Godot项目管理器Import选择 `game/project.godot`，等待glTF导入。F5运行游戏。无需插件、API Key、网络图片或第三方模型。

WASD移动，Shift跑，Space跳；单击游戏捕获鼠标，Esc释放；R重新开始。鼠标初始不锁住。没有手柄/触屏输入，暂不宣称支持手机。

运行材质实验：打开 `labs/material_lab.tscn`，F6。左球有Roughness/Metallic/Emission滑条，右球固定；独立开关OmniLight，不启用GI或Glow。

## 节点与职责

`main.tscn`：地面、墙、低平台、5颗星、HUD、完成与重开。

`player.tscn` + `player.gd`：CharacterBody3D、胶囊视觉/形状、CameraPivot→SpringArm3D→Camera3D。角色物理根节点保持Scale=(1,1,1)，修改Shape尺寸而非随意非均匀缩放。

`star.tscn` + `star.gd`：Area3D及SphereShape、glTF视觉。taken防止同一帧重复计分，先发事件再延迟释放。只旋转Visual，不把复杂星形当碰撞体。

输入动作在player的_ready中安装，便于独立复用；正式项目迁移到Project Settings > Input Map。变量暴露在Inspector；你不必从零手写脚本，但要理解状态和单位。

## 可以亲自调的旋钮

Player：walk_speed 4、run_speed 7、jump_speed 6、gravity 18；数值是示例起点，不是最佳手感。Camera FOV 65、SpringArm长度6、鼠标灵敏度0.12。

先猜，再每次只改一项：C08速度；C09固定跳速改变重力；C10固定距离改变FOV；C12/C13材质实验。停止运行后Inspector修改会保存；Remote修改通常只影响当次运行。

## 物理分类

第1层World=位值1；第2层Player=位值2；第3层Collectible=位值4。

玩家Layer2、Mask1；星星Layer4、Mask2；世界使用默认Layer1。注意“第3层”不等于位值3，Inspector勾选第3层对应4。

## 自检与验收

仓库根目录：

```sh
python tools/validate_repo.py
# 下两条需要先安装Godot，并把实际可执行文件名替换为godot。
godot --headless --path game --editor --import
godot --headless --path game --script res://tests/smoke.gd
```

先导入再测试，因为glTF需要导入结果。`smoke.gd`检验落地、Area实际重叠、单次计数、防重入和输入移动；没有替代手感、相机穿墙、视觉或性能验收。

人工：撞墙、绕墙、跳平台、收齐、重开、跌出地面恢复、Esc、俯仰极限；再测错误对象不计分和30/60物理tick相同秒数位移。记录失败，不把存在测试文件当测试通过。

## 已写入与未实现

参考解写入走/跑/跳、镜头、阻挡、拾取、计数、完成/重开、坠落复位。暂不含音效/粒子、坡道或自动爬台阶、正式动画、存档、游戏手柄与生产级角色控制器。

HUD的1000/FPS是平均FPS倒数估计，不是GPU耗时。真正性能证据来自Godot监视器/分析器和目标硬件。
