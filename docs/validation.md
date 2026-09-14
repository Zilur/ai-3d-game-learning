> v4仅新增/修订课件与作者工具，未修改game/、blender/或web/实现。旧引擎结果属于其原提交；新课堂均未逐课生成和试教。课件验证另见 [审核记录](../curriculum/lesson-review.md)。

# 统一主线验证记录

日期：2026-09-14。所有测试以对应提交的真实Actions日志为准，不把历史分支结果自动继承到main。

## 合并前状态与重新验证入口

原PR #2提交a8e2c166949d7d1dd021303dc2476f5acd1d2136曾通过Godot4.7.2导入及50项无界面行为测试。当前整合以c06a0db763ab3c32d7200ce6c7ae51af41b957a2的工程为基础，保留原PR #1双球实验并新增B02，必须重新测试。

[当前工作流运行列表](https://github.com/Zilur/ai-3d-game-learning/actions/workflows/validate.yml) 的绿色结果对应具体提交；查看日志中的COURSE VALIDATION PASS、SMOKE PASS与B02 PASS。添加工作流文件不是通过证据。

|层次|检查内容|边界|
|---|---|---|
|课程静态检查|Markdown文件链接、32概念/64P-T题与答案、单一目录/评分、B02材料入口|不证明所有教学事实正确或学员已掌握|
|素材与源码|Python语法、资源路径、OBJ闭边、glTF缓冲区边界|不等于Blender执行和材质视觉验收|
|引擎导入|Godot4.7.2实际解析、资源导入|不是运行全部学习者设备|
|参考关卡|50项移动、跳跃、碰撞、检测、重复拾取、重开与实验参数测试|不是帧率评测或图形界面验收|
|B02|三个场景加载、实例/职责、整体移动、故障修复、外观替换|测试提供的参考解，不读取/评分个人作业|
|双球材质场景|无界面启动、无脚本运行错误|不是像素、光效和交互控件人工验收|

编辑会话本地没有Godot/Blender且无法直接clone；引擎验证使用GitHub Actions真实运行，不声称本机游玩过。

## 仍需人工完成

- [ ] B02在实际窗口可看清两个模块，Camera正确，字体/标牌/子节点操作无障碍。
- [ ] 玩家贴墙/进角落镜头可用；10颗星全可达；运动手感由人判断。
- [ ] 双球及单球实验每次只改一个参数；画面变化与讲义一致。
- [ ] Blender脚本运行、保存副本、导出GLB、修改源文件后重导入。
- [ ] 新OpenMAIC输入真实生成、控件有效、K没有被扩大考核。
- [ ] 学员首次独立判断、操作、换情境与隔次复测有证据。

这些状态分开记录；自动测试绿灯不能全部勾选。当前未部署OpenMAIC、未开启GitHub Pages、未生成收费课堂、未完成新课真人试教。

## 可重复执行

```sh
python3 tools/validate_repo.py
godot --headless --path game --editor --import
godot --headless --audio-driver Dummy --path game --fixed-fps 60 --script res://tests/smoke.gd
godot --headless --audio-driver Dummy --path game --script res://tests/b02.gd
```

任何Parse Error、SCRIPT ERROR、非零退出或没有PASS标记都不能算通过。main合并后也重新运行相同检查。清理旧分支只在该次main检查通过、分支头确认在main历史中时执行。
