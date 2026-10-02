# OpenMAIC｜教案输入、真实产物、验收与发布

使用官方OpenMAIC，不维护分叉课堂系统。我们的差异Skill在[ai3d-self-study](skills/ai3d-self-study/SKILL.md)：自学、现成实验、孩子作判断、一次伙伴分享与真实软件证据。通用费曼／回忆／螺旋学习优先使用实际部署里的上游能力。

**本仓库没有已经生成的课堂。** `catalog.json`起初为空；Skill文件也不会自动安装到托管站点。固定核查来源见[upstream.json](upstream.json)，源码阅读不是已部署验证。

## 最简单的生成流程

```sh
python3 tools/openmaic.py prepare A04
```

只创建本次目录和输入，不发起生成。命令显示实际运行ID；需要固定ID可用`--run-id <名称>`，已有目录拒绝覆盖。默认只体验现成实验；明确为自己的项目制作时才加`--purpose project`。

输入由**本课正文＋本课教师反馈＋实际引用的记忆项＋差异Skill**组装；不用手拼多份稿，不含个人记录。把`input.md`交给实际OpenMAIC工作台，用其官方方式生成，生成后导出原生`.maic.zip`。

```text
openmaic/output/A04/<run-id>/
  input.md        当次实际输入快照，不手改代替教案
  run.json        来源hash、用途、版本、状态与产物定位
  A04.maic.zip    真实导出后才出现
  review.md      实际验收，没有做过的不能勾选
```

可以用`--upstream-ref <版本或提交>`记录实际部署；不知道就保持null，不拿核查提交假冒实际运行版本。

`practice/...`和`res://...`是本地路径，上传input不会把3D工程送进云端。生成课堂应把这些内容标为“在Godot/Blender打开”，只在课堂里做解释或明确标注的示意；不能生成一个按钮后声称已经运行了本地工程。

## 接收产物和检查

```sh
python3 tools/openmaic.py attach A04 <run-id> /path/to/A04.maic.zip
python3 tools/openmaic.py inspect A04 <run-id>
```

attach复制你提供的原生ZIP并核对基本容器结构、路径与校验值，不执行其中HTML/脚本，不改上游格式。它不证明控件可用、声音正确或课堂已验收。工具不解析任意上游未来格式；遇未知版本明确停下核查。

按review.md实际检查：范围、互动、复位、答案时机、一次伙伴分享、资源依赖和隐私许可。重新导入导出包，检查断网或缺失资源时的真实行为。已检查的条目才改为`[x]`，并写实际环境；这是你的声明，不是自动审计结论。

## 代表课堂的引导验收

源文件通过后，实际生成一课仍需检查：开场是否只给当前问题而不是全部解释；求助或直接请求解释时能否及时帮助；连续无进展是否缩小步骤；已经理解时是否停止重复追问。用构造回应分别试“完全陌生、已有解释、只缺入口、明确求解释、想暂停”，并标为教师走查，不冒充儿童记录。

再看学习者有没有一处真实选择、一次可见结果，以及把发现用回作品的机会。喜欢的颜色不当作标准答案；不要求表演惊奇、不把分享变考核。可以指认、画图或演示，阅读与表达方式不是固定能力标签。

本地CURRENT卡现在先呈现教案中的开场，操作帮助、伙伴分享与旧问题按需展开；公开生成输入仍不自动带入私人历史。每次实际生成结果都要检查，源码中出现这些要求不等于模型已经执行。

## 正式交付与索引

```sh
python3 tools/release.py classroom A04 <run-id> --version v1
```

只在导出hash一致、来源未变化且验收声明完整时打包到`dist/openmaic/`；本地打包不是上传或发布。包装ZIP保留原生`.maic.zip`及来源记录；学习时解压并导入其中的`.maic.zip`。将这个版本的包装ZIP保存到你选定的正式分发／备份位置后，再登记它的公开下载地址：

```sh
python3 tools/openmaic.py register A04 <run-id> --version v1 --url <公开HTTPS地址>
python3 tools/openmaic.py register A04 <run-id> --version v1 --url <公开HTTPS地址> --confirm
```

先预览，再确认更新catalog。只放版本、来源hash、下载包装ZIP的sha256、内部原生课堂的classroom_sha256和公开地址，不保存大文件或令牌链接；工具不验证远端链接是否可下载。正式成品不能只留在会过期的CI附件里。

## 维护与升级

先保持现在这条简单链路：**改源文件 → 检查 → prepare → 官方工作台生成/编辑 → 原生导出 → attach/inspect → 实际验收 → 本地打包**。不另建课程数据库或生成后台，也不一次生成47课。先用A04试通；后续遇到美术与动作需求时，再用B02、C04检查对应材料，B13检查答案是否提前泄露。

|内容|固定位置|怎么更新|
|---|---|---|
|课程、教师反馈、记忆|`course/`|在dev修改并检查，稳定后合入main|
|共享3D源与实验|`practice/`|保留.blend/.glb/.gltf和必要导入元数据；按改动重跑原生验证|
|每次输入、导出、验收|`openmaic/output/<课号>/<run-id>/`|新建运行，不覆盖旧版；与源仓库分开备份|
|可交付ZIP|`dist/`|用新版本名，保留当前可用版；备份到现有可靠存储即可|
|当前可下载版本|`openmaic/catalog.json`|真实交付且有公开地址后才register；未交付保持空|
|学习记录和个人作品|`.learning/`|保持私人，不随课程更新自动迁移|

共享工程独立打一个源码包即可，不复制47份。课堂与实践包一起交付时，保留相同运行记录中的`practice.sha256`；它是素材版本指纹。`prepare`记录整个可分发实践包，`inspect`列出改变的文件；动态加载难以仅凭课内链接追踪，所以采取整包保守核对。缓存、字体和Blender备份不参与。实践包改变不等于必须重新调用模型：先看关联演示是否受影响，必要时修课堂，另建运行并重新验收。旧运行没有素材指纹时标为`untracked`，仍可读取，但不能直接按新版素材再打包。

实际部署、会话和模型设置由OpenMAIC自己维护。正式生成后在该运行的`review.md`记公开版本、模型/媒体设置、课堂定位和实测问题；密钥不入库。`output`和`dist`不受Git备份保护，应另存一份；课堂导出也不能代替上游会话/数据库的备份。回退时继续使用留存的旧课堂与匹配实践包，不覆盖孩子的工程。

改课只改`course/lessons/`，反馈只改teacher-notes，通用术语只改memory。inspect按实际选中内容的hash识别变化；不因修改无关文档就让47课全重生成，更不会自动付费重生成。

新版本另建运行目录，不覆盖旧验收版。纯排版可用上游编辑；概念、题目或边界变化要同步回教案。输入快照不可覆盖重写来源；重新准备并重新验收再切catalog。共享Godot／Blender工程独立交付，不塞进每一节课。

2026-10-02核对[官方README](https://github.com/THU-MAIC/OpenMAIC)：已列出9月28日的v1.1.2及后续主分支运行说明；这是文档核对，不表示本项目已部署或验证该版本。需要升级时读所选版本变更，在副本里导入一课、试交互并重导出，再更新实际部署记录。没有当前需求就维持已验证版本，不追着每个新功能改课程。

优先用用户Skill入口，不复制上游通用Skill。`OPENMAIC_AGENT_SKILLS_DIR`在已核查版本中替换扫描根，不是追加路径；不要用只有我们一个Skill的目录覆盖上游内置技能。

公开跟踪项[#57](https://github.com/THU-MAIC/OpenMAIC/issues/57)、[#999](https://github.com/THU-MAIC/OpenMAIC/issues/999)、[#1413](https://github.com/THU-MAIC/OpenMAIC/issues/1413)只作路线线索，不是交付承诺。升级前查实际实现，在副本测试一课；上游能接管的功能验证后替换，不保留两套主数据源。

## 学情与隐私分离

OpenMAIC课堂文档不是完整学员运行记录备份；本地state也不会自动接收OpenMAIC成绩。仅需私人补漏上下文时，可运行`python3 tools/openmaic.py context A04`预览；加`--confirm`才在`.learning/family/`另存附件，不混进公开output或可复用Skill。

复习清单是需要逐渐熟练的概念与思维模式，不只由错题产生。课堂作答、个人自述和软件实操是不同证据；不自动推断独立性或记忆永久稳定。

## 清理边界

build是临时缓存；**output不是缓存**；dist是交付包；.learning是私人资料。通用清理只碰build。output和旧发布要确认已有备份且明确淘汰后才能删除。

[上游原生ZIP类型](https://github.com/THU-MAIC/OpenMAIC/blob/f7b8769e7fff49a083a5f655ed84cf800ab0b135/lib/export/classroom-zip-types.ts) · [官方仓库](https://github.com/THU-MAIC/OpenMAIC)。本工具是本项目的本地维护封装，不是新增或冒称官方API。
