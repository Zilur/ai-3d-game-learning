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

## 接收产物和检查

```sh
python3 tools/openmaic.py attach A04 <run-id> /path/to/A04.maic.zip
python3 tools/openmaic.py inspect A04 <run-id>
```

attach复制你提供的原生ZIP并核对基本容器结构、路径与校验值，不执行其中HTML/脚本，不改上游格式。它不证明控件可用、声音正确或课堂已验收。工具不解析任意上游未来格式；遇未知版本明确停下核查。

按review.md实际检查：范围、互动、复位、答案时机、一次伙伴分享、资源依赖和隐私许可。重新导入导出包，检查断网或缺失资源时的真实行为。已检查的条目才改为`[x]`，并写实际环境；这是你的声明，不是自动审计结论。

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

改课只改`course/lessons/`，反馈只改teacher-notes，通用术语只改memory。inspect按实际选中内容的hash识别变化；不因修改无关文档就让47课全重生成，更不会自动付费重生成。

新版本另建运行目录，不覆盖旧验收版。纯排版可用上游编辑；概念、题目或边界变化要同步回教案。输入快照不可覆盖重写来源；重新准备并重新验收再切catalog。共享Godot／Blender工程独立交付，不塞进每一节课。

优先用用户Skill入口，不复制上游通用Skill。`OPENMAIC_AGENT_SKILLS_DIR`在已核查版本中替换扫描根，不是追加路径；不要用只有我们一个Skill的目录覆盖上游内置技能。

公开跟踪项[#57](https://github.com/THU-MAIC/OpenMAIC/issues/57)、[#999](https://github.com/THU-MAIC/OpenMAIC/issues/999)、[#1413](https://github.com/THU-MAIC/OpenMAIC/issues/1413)只作路线线索，不是交付承诺。升级前查实际实现，在副本测试一课；上游能接管的功能验证后替换，不保留两套主数据源。

## 学情与隐私分离

OpenMAIC课堂文档不是完整学员运行记录备份；本地state也不会自动接收OpenMAIC成绩。仅需私人补漏上下文时，可运行`python3 tools/openmaic.py context A04`预览；加`--confirm`才在`.learning/family/`另存附件，不混进公开output或可复用Skill。

复习清单是需要逐渐熟练的概念与思维模式，不只由错题产生。课堂作答、个人自述和软件实操是不同证据；不自动推断独立性或记忆永久稳定。

## 清理边界

build是临时缓存；**output不是缓存**；dist是交付包；.learning是私人资料。通用清理只碰build。output和旧发布要确认已有备份且明确淘汰后才能删除。

[上游原生ZIP类型](https://github.com/THU-MAIC/OpenMAIC/blob/f7b8769e7fff49a083a5f655ed84cf800ab0b135/lib/export/classroom-zip-types.ts) · [官方仓库](https://github.com/THU-MAIC/OpenMAIC)。本工具是本项目的本地维护封装，不是新增或冒称官方API。
