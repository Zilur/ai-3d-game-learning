# 维护与验证

## 分支与维护范围

只保留`main`和`dev`：main保存稳定基线，日常课程与工具维护在dev。2026-10-02已比较两个旧课程分支的完整文件树，确认内容分别进入main的`039464e`和`c949048`，以`4e199b0`保留合并历史后删除旧分支，再从main建立dev。后续不为每次小修改长期留分支。

按实际需要做小范围维护：修一处内容、核对关联材料、运行相应检查即可；软件补丁先验证兼容，再更新说明。没有需求不新增管理系统，不批量重做素材，也不为版本号变化重新生成全部课堂。

## 哪些文件是源

`course/lessons/*.md`是47课唯一正文；教师答案在`course/teacher-notes.md`；术语、判断和思维模式在`course/memory.md`。修改相应正文即可，不再运行旧Python作者生成器。元数据用JSON流式YAML；保留课号、前置、复现课号、记忆ID和仓库相对实验路径。

新题或教案变化同时检查本课反馈与记忆引用；不把先前学过的公开题冒充盲测。课程索引标题与前置由检查器核对，不自动覆盖正文。147个既有能力ID仍可用于读取旧学习记录。

## 一条检查入口

```sh
python3 tools/check.py
python3 tools/check.py --godot /path/to/godot
python3 tools/check.py --blender /path/to/blender
python3 tools/check.py --web
```

默认检查教案／路径／资产结构及Python单元测试；未加原生参数不宣称软件实测。Godot运行八组行为测试和两个进程间的存档检查。Blender只重新打开已提交四个文件，禁止先重建再验。Web选项需要Playwright和Chromium，环境缺失时明确失败而不是伪称通过。

`.github/workflows/check.yml`负责课程、工具、Mac/Windows原生检查与内部Linux图形/Blender检查；`release.yml`负责Mac/Windows独立release导出与脱离源码运行。内部Linux不提供用户体验包。

最近一次目录迁移的真实执行结果随对应交付说明提供；CI定义存在不等于已运行。Headless行为测试不代表儿童试学、听感或所有目标显卡表现。

2026-10-02本机复核：默认检查156项测试通过；Godot 4.7.2八组原生行为及跨进程存档通过；Blender 5.2.1重开四文件通过，哈希未变。三段场景的实际Compatibility画面已查看，原生日志和截图在`build/audit-20261002/`，属于可重做的验证证据。完整质量边界见[课程设计](design.md#一条主线)。

## 生成与发布

见[OpenMAIC接入](../openmaic/README.md)。代码不会调用模型、上传或付费生成。仅准备输入并保存操作者提供的原生导出，课堂互动必须实际检查。

```sh
python3 tools/release.py source
python3 tools/release.py desktop --godot /path/to/godot
python3 tools/release.py classroom A04 <run-id> --version v1
```

源码包只包含五个源目录、README、AGENTS和必要Git配置；排除私人目录、OpenMAIC产物、缓存、安装程序与字体文件。桌面导出需在Mac／Windows使用匹配4.7.2模板；不制作Linux用户包。成品默认写dist，拒绝覆盖。

发布前核对资源许可与私人信息。未签名／未公证的教学包不是商店发行；不要关闭系统安全保护来绕过警告。

## 什么能清理

```sh
python3 tools/check.py --clean
python3 tools/check.py --clean --confirm
```

第一条只预览`build/`；第二条才删除其中真正可重做的缓存。拒绝任何符号链接，不读取或删除`.learning/`、`openmaic/output/`、`dist/`、引擎源资产。不得使用全仓`git clean -fdx`。`.godot`是引擎缓存，可在关闭编辑器后人工删除，但不在通用自动清理范围。

**被Git忽略不等于可以删除。** 课堂生成有成本且不保证重复生成相同结果；output应正式备份。dist中只有另有可靠副本的旧交付才人工删除。

## 私人数据与旧版本

本轮不移动`.learning/family/state.md`，也不改已有工作副本的路径。轻量入口只保存自述；原评分报告的校验、作废、去重和调度只作为兼容读写内核保留，没有旧家长CLI。未观察不是零分，也不从一句“我懂了”产生分数。

state.md仍是唯一数据源，带独占锁、原子替换和最近一次备份。损坏或未知版本会停止，不会静默初始化。恢复先保留坏文件、确认无写入，再从备份恢复；`.gitignore`不等于访问控制或磁盘加密。

已有`.learning/growth`等私人笔记不删除；课程更新不会自动覆盖或升级孩子的工作副本。下载新版请解压到新目录，备份私人记录后由自己决定继续旧副本还是另建。

旧资料清理前保留最终自学版基线；历史不在活跃树另设archive。修改保留版本记录，不在文件名堆final-final或过期日期。

## 素材复建仅供维护者

`tools/assets/`包含原创模型和Blender复建脚本；学员直接打开`practice/`的现成文件。复建先输出到临时目录比较，不悄悄修复已损坏资产来让检查通过。

Godot内部资源根仍是res://；只把原A03节点样本从旧课号目录改为`labs/scene_nodes/`。旧收集参考仍被基础课程使用，不删除。
