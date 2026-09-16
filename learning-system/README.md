# 亲子AI学习伴侣 v1

**目标不是让AI带着孩子更快“做完”，而是让孩子能决定、能验证、能解释，隔一段时间还会用。** 第一版保留47课与全部项目约束，只增加学习过程、亲子讲解、个人弱项与复习调度。无需数据库，不调用付费接口，不自动上传个人数据。

## 1. 孩子实际怎样上一课

先给一个看得见的小任务，例如“发现庭院里的隐形墙”。孩子猜结果，动手试一个变量，再决定采用什么。AI只解释当前用得上的部分，卡住时给小线索或短示范，不连续拷问。

结束前留约3分钟：孩子给爸爸、同学或其他陪伴者讲概念并演示；听的人根据解释先猜一次，再试一次。一次演示可以同时覆盖两项M，不再重复写一套作业。

早晨或下一次见面，先回想一至两项，再看资料。晚间只是可选的短回想，不强迫每天做两套复习，不推迟睡觉。

首次默认`supported`陪伴模式：可口述、画图、指着屏幕解释，成人可以代打字和操作鼠标。`independent`模式只是减少提示，不按年龄、识字速度或打字速度给能力贴标签。

## 2. 成人一次准备

在完整仓库的根目录运行，需Python 3.10或更新版本。Windows可把`python3`换成已配置的`python`或`py -3`。先由成人确认所用AI服务的年龄、账户和数据条款；工具不会替孩子注册账户。

```sh
python3 tools/family_learning.py init --timezone Asia/Tokyo
python3 tools/family_learning.py session A01
```

打开生成的`.learning/family/SESSION-A01.md`，由成人检查后交给AI开始这一课。AI只读本课学生稿、亲子任务及最少必要的学习摘要；不默认收到整份个人历史。

孩子最开始只需要说：“我们来做今天的小挑战。一次问我一个问题，不要先告诉我答案。”

## 3. 使用OpenMAIC

```sh
python3 tools/family_learning.py session A04 --openmaic
```

生成的`.learning/family/OPENMAIC-A04.md`是**教师生成输入**，由本课原OpenMAIC规格和亲子教学协议组合而成，不含个人记录。它包含教师答案，不能直接发给孩子阅读，也不能把答案渲染在初始课堂里。

原`openmaic/lessons/`与学生稿保持各自作者源的一致性；新模式通过组装器接入所有47课，不手工复制修改141份派生稿。单独复制旧输入不会自动带上本次的新协议；亲子模式从本入口生成组合输入。

## 4. 结束后怎样记录

```sh
python3 tools/family_learning.py template A04
```

生成`.learning/family/report-A04.json`，所有成绩初始都是`null`。AI或成人根据实际作答整理证据；没有看过就不填。沿用原有`learning_review.py`的四个维度、0–2锚点、提示级别和证据类型。

```sh
python3 tools/family_learning.py record .learning/family/report-A04.json
python3 tools/family_learning.py record .learning/family/report-A04.json --confirm
python3 tools/family_learning.py today
```

第一条只校验，不写入；第二条表示陪伴者已核对并确认保存。参数不是身份认证，也不能证明证据真实。孩子不用编辑JSON；成人可以把[手工观察单](templates/manual-record.md)上的简短观察交给AI整理，再核对。

**缺证据不是0分。** 图像、代码、自动测试、孩子的判断和最终项目验收是不同证据。用纸片演示能支持解释，但不能伪称完成Godot操作。看过答案后复述不能记作独立迁移。

同一报告重复保存不会重复计数。误记时使用`void`保留旧记录及更正原因，再用新会话ID提交修正版，详见[数据说明](data-and-reminders.md)。

## 5. 本地复习与提醒

```sh
python3 tools/family_learning.py today
python3 tools/family_learning.py cards
python3 tools/family_learning.py reminders --morning 07:30 --evening 19:30 --days 30
```

`today`根据实际记录更新`TODAY.md`；`cards`生成47张本地逐课亲子卡。最后一条中的时间只是可修改示例，默认从次日开始导出30天提醒。晚间参数可以省略。

**生成ICS不等于通知已经开启。** 成人需要把`.learning/family/reminders.ics`导入日历，并检查通知权限。日历只提醒打开本地复习清单，不读取弱项，也不会在云端自动更新清单。电脑关闭时，Python脚本不运行；聊天AI也不能直接读取你电脑里的新进度。

## 6. 怎么判断这一版真的有用

先使用A04、A05、B04、C02中的已具备前置条件的代表课，不要求孩子为了试验跳过必要基础。记第一处卡点、孩子能否独立解释、隔天是否记得、是否愿意再做，以及成人记录花费的时间。没有孩子的真实试学记录前，不称为最优教学模式。

[爸爸陪伴脚本](parent-guide.md) · [教学理念](design.md) · [AI教练协议](coach.md) · [后续优先级](audit-and-next.md)

## 7. 学完入门之后：走向商业作品，但不换学习方法

[未来商业成长指南](commercial-growth.md)讲六个阶段：独立小作品、玩法原型、目标品质样段、受控生产、候选发布、发布后维护；[知识成长地图](growth-knowledge-map.md)讲每阶段要深入什么、怎样学、何时停。商业化是未来选择，不是儿童毕业要求。

```sh
python3 tools/growth_workshop.py plan
python3 tools/growth_workshop.py session independent --cycle first-small-game
python3 tools/growth_workshop.py session prototype --cycle route-test --openmaic
```

无需先init家庭记录。只生成`.learning/growth/<cycle>.md`，同名文件拒绝覆盖。普通模式是当前阶段的AI工作坊任务；`--openmaic`是生成一个短互动课的教师输入，不是已经生成课堂。两者均不读取私人历史、不评分、不修改游戏、不启用提醒。Windows可按本机配置用`python`或`py -3`。

一轮只选一个问题，不把整本成长指南投喂成孩子的必读课。阶段标识不是新增课号；原M/K不变。任意新专题先用自由MD写观察与下次复测，不假称旧调度器已经支持自动追踪。发布前另用[发布检查单](templates/release-readiness.md)，产品质量和孩子理解分别看。

[项目复查与工作优先级](project-review-2026-09-16.md)区分了已写好的设计/工具、尚缺的工程与必须真实执行的试学。
