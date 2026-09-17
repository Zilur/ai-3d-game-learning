# 星光小庭院：打开就能玩的三段参考

**使用平台：仅 macOS 与 Windows。** 独立体验包和桌面导出仅面向这两个平台；上课与修改作品使用完整工程。

这是已实现的生产参考，不是孩子已完成的作业或最终商业美术签收。固定高角度朝向，镜头沿路线平移；素材复用与局部二开策略不变。

## 开始

用Godot **4.7.2**导入`game/project.godot`，等待首次资源导入完成，按F5。默认启动`game/world/exploration.tscn`。
旧`game/scenes/main.tscn`仍是原十星教学参考；不要用旧场景判断新功能是否存在。

中文界面使用电脑已有的中文系统字体，例如苹方、微软雅黑或Noto Sans CJK SC。不随工程打包字体。极简或全新系统出现缺字/字体加载报错时，由成人先检查中文字体安装并重启Godot；macOS的干净测试环境已补装中文字体后通过运行检查。

|操作|作用|
|---|---|
|WASD / Shift / 空格|移动 / 跑 / 跳；斜向不额外增速|
|E|在对象附近取得林路钥匙、打开观景门|
|J|面向庭院木桩进行可选训练；一次动作只计一次有效命中|
|Esc|暂停、保存、继续、训练开关、低运动反馈、音量、实验、退出|
|F9 / F10|主动保存 / 从主存档继续|
|R|确认后重新开始；已有磁盘存档不删除|

庭院三颗星 → 林路四颗星和钥匙 → 门前按E → 观景台三颗星。桥和观景台入口有可步行坡道；无需靠跳跃掩盖地形接缝。木桩训练可关闭，不影响十星通关。

## 存档与恢复

存档只在主动保存时写入。继续会恢复已收集星星、钥匙、门、训练计数/开关、音量/低运动设置，并在最近所在区域的安全检查点重生，不保存跳跃或攻击中间帧。

专用位置为`user://starlight_village_v1/save.json`；与旧交互实验文件和私人学习记录分离。临时文件写入并校验后再替换，保留上一份有效`.bak`。损坏主档不覆盖有效备份，暂停菜单有“尝试备份”。读取失败不改变当前游戏。未来版本不认识时拒绝而不自动清空。原v1示例格式有明确迁移；不声称兼容任意旧游戏存档或任何断电故障。

换机器请由成人备份这个目录。有未保存变化时，退出、打开实验、重新开始和读取旧档先提供确认；保存失败会留在原处。实验右上角可以继续刚才的暂存游戏。暂存只在本次程序运行中有效，强制结束进程不受正常退出确认保护。测试脚本只用`production_test_only`，不使用个人唯一存档。

## 先创建自己的副本，再改一个参数

在完整仓库运行`python3 tools/workspace.py create my-world`，打开生成的`.learning/projects/my-world/game/project.godot`。只调`world/creation.tres`的一个参数，或移动`world/exploration.tscn`里StarLayout的一个标记，Ctrl+S保存，再重开验证。编辑定位示意运行时隐藏；原参考不会被改坏。详见[工作副本与使用收尾](docs/usability-closeout.md)。

读取旧档前的保护副本保存在`.before-load`，不覆盖待读取的主档/备份；菜单提供恢复入口。

## 原创资产如何二开

`game/assets/village/`含12类真实GLB：小屋、树、松树、石、花、桥、围栏、灯、路牌、木桩、平台、信标；全数接入三段地图。
每个GLB都能直接在Blender导入和修改。无需购买、下载角色或运行构建器才开始玩。新几何的来源、许可、摘要在同目录README、LICENSE和manifest。

这是本轮采用的原创生产参考套件，不假称已采购此前提及的外部商品包。角色使用已验证的原创骨架加外观包装；不是任意商业角色的通用动作重定向。最终美术风格是否满意仍由人看真实玩家画面决定。

## 新选修实验

按Esc进入实验，或F6运行`game/labs/lab_hub.tscn`。E01导航、E03 Shader、E02/E05批量/LOD/分块/异步读取及C08 Fog/Glow/景深全部有现成场景。
景深只在Forward+或Mobile可用；Compatibility中明确禁用。渲染器切换需重启，具体场景的状态栏显示**实际**渲染器，不能只相信启动参数。保留低配默认Compatibility，不为了景深让全课变成高配置门槛。

原生命令行示例（Godot已在PATH中）：

```sh
godot --path game --rendering-method forward_plus res://labs/effects_lab.tscn
```

OpenMAIC课堂成品由家庭稍后自行生成，本轮不运行生成服务。已同步的Markdown是教师输入和课程索引，不是课堂导出。

[47课资源映射](curriculum/practical-resource-audit.md) · [操作实验](LABS-START.md) · [本轮验证](docs/production-validation.md) · [未来商业成长](learning-system/commercial-growth.md)
