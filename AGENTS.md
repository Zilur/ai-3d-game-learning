# 维护约定

先读README。只维护当前五个主目录：course、practice、openmaic、tools、docs。

- 教案正文唯一来源是`course/lessons/<ID>.md`；元数据采用JSON（YAML子集）放在`---`内。只保留课号、前置、复现、记忆与实验关联；目标和能力写正文，不复制为Python字符串。
- 教师答案只在`course/teacher-notes.md`，共享术语／思路只在`course/memory.md`。调用时用`tools/openmaic.py prepare`组装，不能改input快照代替源。
- 保持A01—E07、原有能力ID、前置和M/K边界；E06仍全K选修。爸爸只有一次非阻塞分享，不恢复家长评分系统。
- OpenMAIC已有能力优先用上游。不复制上游源码、改其数据库或静默升级；本次重构不授权收费生成。
- `.learning/`、`openmaic/output/`、`dist/`不是缓存；禁止全仓`git clean -fdx`，不迁移或覆盖私人历史。可清理范围只有`build/`，且必须先预览。
- 现成.blend/.glb/.gltf及必要.import/.uid是教学源资产或导入/标识元数据，保留许可；.godot等引擎缓存不得打包。不分发字体文件、密钥或个人记录。
- 改动后运行`python3 tools/check.py`；涉及软件路径再跑原生验证，不能用旧测试结论代替。删除过时CLI测试时，要把仍有效的行为约束迁到新入口测试。
- 源码清理不等于重置学习数据或发布课堂；提交和生成是否完成必须如实写明。
