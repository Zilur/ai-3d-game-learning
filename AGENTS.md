# AI 协作约定

唯一交付版本为main；用户要求减少分支。日常小修改直接提交main并运行检查。不自行增加长期平行分支、重复题库或另一套概念ID。

权威文档顺序：curriculum/learning-contract.md → curriculum/concept-map.md → assessments/exam-blueprint.md → 本课材料。M/K是具体能力深度，不能把整个学科强制升级成M。所有评分使用assessments/mastery.md的0–2规则。

每课交付起始材料、完成参考、可恢复故障、匹配深度的题目、独立OpenMAIC输入、验证记录。禁止把课纲/源码/生成课堂/试教/掌握混为一谈。答案与学员任务分开；API可查，学员必须自行作关键判断。

修改代码后执行tools/validate_repo.py，并在固定Godot版本跑工程导入、game/tests/smoke.gd、game/tests/b02.gd。无引擎环境就使用GitHub Actions实际结果，不声称本地运行过。不把历史分支测试结果当成新提交的结果。

只修改本次任务范围。源资产不破坏覆盖；不提交API Key、访问码、个人学习记录。无明确授权，不部署OpenMAIC、不启动收费生成、不选择项目许可证、不上传第三方素材或字体文件。

合并分支保留原始历史，按内容解决冲突而不是把两套目录一股脑复制。删除分支前确认其提交已在main历史中；有新未合并提交就停止删除。
