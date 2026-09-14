# 验证记录与边界

版本：Interactive Mastery v2。记录日期：2026-09-14。

## 已执行的自动验证

[GitHub Actions 成功运行 #3](https://github.com/Zilur/ai-3d-game-learning/actions/runs/34806032078)，对应代码提交 `a8e2c166949d7d1dd021303dc2476f5acd1d2136`。环境：Ubuntu 24.04，官方 Godot `4.7.2.stable.official.ed1daf0bf`；下载包依据官方发行元数据做SHA-256校验。

日志结果：

```text
OBJ: 22 vertices, 40 triangles, signed volume 0.054076249
COURSE VALIDATION PASS: 138 checks, 90 unique questions
SMOKE PASS: 50 assertions
```

这50条是无图形界面的程序断言，不是50位学习者通过，也不是所有画面/手感已经验收。后续改动应重新看对应提交的CI，不把这次成功自动套用到未来版本。

## 必须分别报告的状态

| 检查层 | 本版提供的检查 | 当前证据状态 |
|---|---|---|
| 课程与文件 | 90题唯一ID、26组P/R/T、12道K、课程覆盖、Markdown本地链接 | 通过上述CI；全仓库内容/资源合计138项检查 |
| 资源 | 场景资源路径、load_steps、Python语法、星星闭合网格 | 通过；22顶点/40三角形、边的闭合性与正有向体积已检查 |
| Godot运行 | 真实导入、移动/跳跃/墙碰撞、Area层检测、重复拾取、0/1边界、三次重开、实验变换 | 官方4.7.2导入通过；50条headless行为断言通过 |
| 视觉与手感 | 三种实验显示、控件位置、近墙镜头、可读性与参数A/B | 待真实图形界面人工验收 |
| Blender | 脚本执行、保存.blend、选中对象导出GLB、修改后重导 | 待本机执行；Python语法检查不等于Blender验证 |
| OpenMAIC | 新四份输入生成并逐项测试 | v1 B01收到正面体验反馈；本版未调用服务生成新课 |
| 学习效果 | 首次独立作答、实操、迁移与延迟复测 | 待试学；不能从喜欢课堂推断掌握率 |

编写环境没有预装Godot/Blender；引擎测试实际通过GitHub Actions运行。没有声称在编写环境完成视觉、鼠标手感或Blender导出测试。

## 一次真实的“AI输出→测试→修复”

[第一轮运行](https://github.com/Zilur/ai-3d-game-learning/actions/runs/34805893260)的课程检查通过，但Godot导入报错：`Input.release_pressed_events()`不存在，行为测试因此没有运行。修复为对本项目输入Action调用官方支持的 `Input.action_release()` 后重新执行，导入和行为测试通过。

查证：[Godot Input 文档](https://docs.godotengine.org/en/stable/classes/class_input.html)。不要因为函数名看起来合理就信任AI；也不要只改测试让错误消失。

另修正了实验按钮移动后位置滑块未同步的问题。程序测试覆盖实际空间变换；界面显示位置和使用体验仍需下面的人工验收。

## 本地重现自动测试

```sh
python3 tools/validate_course.py
godot --headless --path game --editor --import
godot --headless --audio-driver Dummy --path game --fixed-fps 60 --script res://tests/smoke.gd
```

出现Parse Error、SCRIPT ERROR、非零退出码或没有SMOKE PASS，都不能当通过。测试不能替代目标设备性能采样。

## 人工验收清单

- [ ] F5能从项目打开完整关卡；F6能单独打开实验。
- [ ] 1280×720窗口中实验控件可滚动，无遮挡导致无法操作；较小窗口另测。
- [ ] Transform的方向标记清楚，三种空间与数值一致，Reset恢复。
- [ ] Door两种模式在0度门板重合，90度侧边保持不动。
- [ ] Material保持主光不变；Emission和独立光源分开；没有承诺默认GI/Glow。
- [ ] 玩家贴墙、进角落、抬头低头时相机可用；灵敏度可调。
- [ ] 十颗星星可实际走到/跳到；场景总数、最后一颗、R重开一致。
- [ ] Blender脚本只新增对象、不覆盖文件；尺寸/原点/朝向与GLB重导核对。
- [ ] 新OpenMAIC课按review-checklist逐项运行，不只观看。
- [ ] 至少一次无答案迁移与一次延迟复测有记录。

实际执行人/设备/版本/日期/结果：________________

## 不在本次实现范围

正式角色骨骼动画、通用自动爬楼梯、复杂移动平台、音效/粒子成品包、导航/存档/发布包，以及对所有Godot4版本的兼容保证。中级文档是课程设计，不是已经实现的中级项目。
