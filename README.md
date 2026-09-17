# AI 时代 3D 游戏自学

**孩子自学，AI辅助；爸爸是一起看、一起问的陪学伙伴。** 做一个固定／有限视角、风格统一的小世界，不必先从零建模或搭全部场景。使用平台：**macOS、Windows**。

## 从这里开始

|现在要做什么|入口|
|---|---|
|开始或继续一课|[47课目录](course/README.md)|
|把关键词和思考方式练熟|[记在脑海里的清单](course/memory.md)|
|打开现成实验或主游戏|[Godot／Blender实践包](practice/README.md)|
|以后做更完整的作品|[从入门到商业游戏](course/growth.md)|

一课一个小任务：先观察或预测，动手改一个条件，说清发现；关键处或结束时给爸爸讲几个点，一起看题、一起问。爸爸还有问题就自由聊，不评分、不签字；爸爸暂时不在也能继续。

**记忆不是晨晚打卡。** 按已学范围遮住清单里的解释，自己说词义、举例、换情境使用；下次选一两项再想起来。API与菜单可查，重要概念和思维模式要逐渐熟练。

## 需要保存自己的改变时

上课直接读教案、开现成实验即可。制作自己的作品时，只创建一份工作副本，不每课重建：

```sh
python3 tools/workspace.py create my-world
```

打开 `.learning/projects/my-world/game/project.godot`。可选轻量笔记：`python3 tools/learn.py start A04` 或 `python3 tools/learn.py note A04 "检测对象这里还不清楚"`。这些命令不评分、不调用AI，也不要求先初始化。

Windows可把`python3`换成`py -3 -X utf8`；Python 3.10以上。软件首次安装和账户／分享由成人协助。

## 维护者入口

[从教案生成OpenMAIC课堂](openmaic/README.md) · [课程设计](docs/design.md) · [维护、验证与安全清理](docs/maintenance.md) · [来源与许可](docs/sources.md)。

源文件在`course / practice / openmaic / tools / docs`。实际课堂产物在`openmaic/output/`，临时缓存在`build/`，交付包在`dist/`，个人记录与作品在`.learning/`；它们互不混用。当前没有生成的OpenMAIC课堂，索引保持空。
