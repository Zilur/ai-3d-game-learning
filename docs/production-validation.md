# 生产整合与专项实验：验证范围

基线：9708e816611244851ee11d622f8f9971fd211358；固定Godot4.7.2。本文描述已实现对象、可复核测试和未覆盖范围，最终运行结论以当前提交的CI日志及随包报告为准。

## 实现边界

- 默认主游戏：庭院—林路—观景台，连续可走主路和支路、十个稳定物品ID、钥匙门、检查点、暂停/重开、独立版本存档和可选择的备份恢复。
- 战斗：现成骨架/动画树接入主角；J攻击、时机窗口、距离与前方判定、一次性命中、中断与恢复、关闭训练不影响主线。仅训练木桩，不虚构敌人AI、连招或完整战斗系统。
- 资产：12类原创GLB均接入，色盘与尺度统一，树石曲面法线平滑；许可台账与确定性复建工具已备好。不是购买的第三方套装，视觉满意度不由测试自动判定。
- 实验：真实NavigationServer路径与物理通行、可关闭/冻结的空间Shader、普通雾/辉光/景深、MultiMesh/几何LOD/遮挡剔除/节点驻留与另一次真实异步场景读取。不是无限地图或通用渲染框架。

## 复核命令

先在Godot完成资源导入，再在仓库根目录运行：

```sh
python3 tools/build_course_materials.py --check
python3 tools/validate_repo.py
python3 tools/check_practical_labs.py
python3 tools/check_production.py
godot --headless --audio-driver Dummy --path game --fixed-fps 60 --script res://tests/production_suite.gd
```

原smoke、visual_lab、concept_labs、b02、practical_labs全部保留。新增production_suite检查真实输入走完整条主线（不瞬移、不注入拾取计数）、钥匙与门、战斗有效/无效情况、关闭与暂停、加载及异常、备份与v1迁移；还检查新实验的真正对象/状态与复位。测试用专用目录，不能对学员文件运行损坏试验。

`save_roundtrip.gd`分两次进程写入/读取，检查跨应用启动的持久化，避免仅在同一对象里假装存档。
`capture_production.gd`输出三个区域、菜单和实验的真实引擎截图；截图视点有人工设置，不能将视点调整说成玩家已走完。实际走通由独立行为测试取证。

## 平台和渲染证据不能混同

headless测试不提供GPU画面质量或帧率结论。Linux软件OpenGL截图只证明该渲染路径的画面可见；Forward+必须核对实际渲染器未回退，再比较景深开关。Windows/macOS自动运行不代表所有显卡、显示器和输入设备均通过。

C08普通雾、辉光可以在本版本Compatibility对照；景深仅Forward+和Mobile。大场景的帧间隔是当前程序的墙钟采样，不是纯GPU耗时；draw calls包含同一视口的其他对象，不伪造“优化提高多少”。MultiMesh按批剔除、LOD减少几何、驻留改变节点集合、异步加载改变获取资源方式，各自分开观察。

## 本轮实际结果（与条件绑定）

2026-09-16，提交`fae33a65990105e539f66217a64af57537292841`的三个桌面自动运行任务通过：Ubuntu24.04、Windows2025测试镜像、macOS15 ARM64。每种环境均导入固定Godot4.7.2资源，执行六组行为测试（50+9+17+23+76+100，共275项断言），再独立启动两次进程验证存档写入/读取。Mac初次中文字体加载失败后，通过为干净镜像补装真正的中文系统字体解决；没有忽略错误或删除断言。

同一提交的Forward+实际Vulkan渲染与Compatibility截图检查也已通过。核对实际渲染器，比较排除侧栏后的场景像素；景深在Forward+产生近远模糊，Compatibility明确禁用。测试环境为Linux Mesa llvmpipe软件渲染，不能据此推断实际显卡帧率。

[桌面与真实渲染的完整运行记录](https://github.com/Zilur/ai-3d-game-learning/actions/runs/35107488196)。记录是历史证据，后续改动仍由保留的CI继续检查。

## 家庭真实验收（不预填结果）

|项目|需要真实观察|状态|
|---|---|---|
|儿童试教|第一处卡点、预测/解释、提示、隔次变式、是否愿意继续|待家庭进行|
|非作者试玩|没有作者解释也能理解目标、找到钥匙和门，完成或主动重开|待真人试玩|
|最终视觉与声音|实际玩家尺寸、主体/道路/留白、响度与静音提示是否合适|需成人/孩子确认；截图不代替听感|
|目标设备|系统/CPU/GPU/驱动/分辨率/渲染器/构建版本、完整路线、退出恢复|按真实设备逐台记录，不标“全部兼容”|
|正式发行|商店规则、资源来源、页面承诺、维护与数据安全|不在本轮自动上架|

无需为试教上传孩子照片、学校、姓名或完整录音。私人观察继续留`.learning/`。用户已决定稍后自行生成OpenMAIC课堂，本轮没有制作课堂成品，也不会把此项写成工程失败。

## 技术依据

- [Godot NavigationPaths](https://docs.godotengine.org/en/4.7/tutorials/navigation/navigation_using_navigationpaths.html)：导航服务器路径与节点职责。
- [Environment](https://docs.godotengine.org/en/4.7/classes/class_environment.html)与[CameraAttributesPractical](https://docs.godotengine.org/en/4.7/classes/class_cameraattributespractical.html)：原生效果参数与景深渲染边界。
- [MultiMesh](https://docs.godotengine.org/en/stable/tutorials/performance/using_multimesh.html)、[遮挡剔除](https://docs.godotengine.org/en/stable/tutorials/3d/occlusion_culling.html)：批量与可见性不是一回事。
- [ResourceLoader](https://docs.godotengine.org/en/4.7/classes/class_resourceloader.html)：后台请求、状态轮询和已完成读取。

链接用于技术核对，不是学习效果或商业品质的证明。
