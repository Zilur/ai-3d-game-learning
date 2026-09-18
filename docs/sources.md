# 来源与许可

本页集中当前有效来源，不复制上游源码或旧审查报告。上游手册可能更新，操作前以实际安装版本为准。

## 教学参考

- [Godot Node3D：变换与父空间](https://docs.godotengine.org/en/stable/classes/class_node3d.html)
- [Godot CharacterBody3D：速度、落地与移动](https://docs.godotengine.org/en/stable/classes/class_characterbody3d.html)
- [Godot Area3D：重叠检测与信号](https://docs.godotengine.org/en/stable/classes/class_area3d.html)
- [Godot Resources：共享和引用](https://docs.godotengine.org/en/stable/tutorials/scripting/resources.html)
- [Godot AnimationTree：动画组织](https://docs.godotengine.org/en/stable/tutorials/animation/animation_tree.html)
- [Godot Retargeting 3D Skeletons](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/retargeting_3d_skeletons.html)
- [Godot General optimization：测量与取舍](https://docs.godotengine.org/en/stable/tutorials/performance/general_optimization.html)
- [Blender Principled BSDF：当前手册入口](https://docs.blender.org/manual/en/latest/render/shader_nodes/shader/principled.html)
- [Blender glTF 2.0管线参考（4.0文档，具体新版选项另查）](https://docs.blender.org/manual/en/4.0/addons/import_export/scene_gltf2.html)
- [Blender官方手册：按实际版本查询工具](https://docs.blender.org/manual/en/latest/)
- [Grant Abbitt：Blender造型与图形设计](https://www.gabbitt.co.uk/)
- [Roman Klco / Polygon Runway：风格化3D作品与课程](https://polygonrunway.com/)
- [The Walt Disney Family Museum：Mary Blair展览资料](https://www.waltdisney.org/mary-blair)
- [Eyvind Earle官方作品入口（仅链接，保留版权）](https://eyvindearle.com/)
- [Daniel Merriam官方画廊](https://www.danielmerriam.com/)
- [Adobe Mixamo FAQ：角色、动作及使用条件](https://helpx.adobe.com/creative-cloud/faq/mixamo-faq.html)
- [Kenney Support：资产用途与许可说明](https://kenney.nl/support)
- [Quaternius：基础角色、动作与风格化套件](https://quaternius.com/)
- [Godot运行检查与可见碰撞工具](https://docs.godotengine.org/en/stable/tutorials/scripting/debug/overview_of_debugging_tools.html)
- [Godot动画轨道：方法事件不在编辑器预览执行](https://docs.godotengine.org/en/stable/tutorials/animation/animation_track_types.html)
- [Godot环境与后处理：效果及渲染器边界](https://docs.godotengine.org/en/stable/tutorials/3d/environment_and_post_processing.html)
- [Godot三维性能：先测量，关注透明和绘制成本](https://docs.godotengine.org/en/stable/tutorials/performance/optimizing_3d_performance.html)
- [Blender Link与Append：引用和本地副本](https://docs.blender.org/manual/en/latest/files/linked_libraries/link_append.html)
- [Godot Camera3D：投影、FOV与相机属性](https://docs.godotengine.org/en/stable/classes/class_camera3d.html)
- [Blender Asset Libraries：资产复用入口](https://docs.blender.org/manual/en/latest/files/asset_libraries/introduction.html)
- [Godot 渲染器功能差异](https://docs.godotengine.org/en/stable/tutorials/rendering/renderers.html)

## 资产与授权

[原创村庄资产许可](../practice/godot/assets/village/LICENSE.txt) · [教学角色及资源说明](../practice/godot/assets/practice-asset-notes.md)。
删除固定的OpenMAIC vendor文档副本，保留来源提交在[upstream.json](../openmaic/upstream.json)。本课程未因此取得上游软件或外部图片的所有权。
本仓库未新增一份覆盖全部内容的许可证；已有单项资产许可继续适用，其余内容不能仅因仓库公开就推断可任意再分发。正式分享前逐项核对。

## 学习方法参考与边界

以下沿用原课程的研究出处，用于理解机制，不把它们当作当前自学系统已通过效果试验。


1. **儿童提取练习。** Karpicke、Blunt与Smith（2016）在小学儿童实验中观察到提取练习收益，同时强调初次提取必须有一定成功率。支持“先回忆、困难时给适量支架”，不支持无限要求孩子从零回想。研究材料并非3D工程，不能直接推出本课程的效果。[原始研究](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2016.00350/full)
2. **间隔。** Cepeda等（2008）发现合适的学习间隔与目标保留时长有关，不能据此给所有年龄、所有知识设置统一神奇周期。本课程的复习安排是可调整的设计选择。[原始研究摘要](https://pubmed.ncbi.nlm.nih.gov/19076480/)
3. **自我解释。** Chi等（1994）研究了诱发自我解释如何帮助理解。支持要求解释因果，而不是仅重复术语；并不等于每个孩子必须擅长长篇口述。[原始研究](https://onlinelibrary.wiley.com/doi/10.1207/s15516709cog1803_3)
4. **教别人。** Fiorella与Mayer（2013）比较学习后教学与准备教学等条件。支持将“真的讲并组织解释”作为活动；把它称为费曼学习法只是方便理解，不表示有一个万能四步配方。[原始研究](https://www.sciencedirect.com/science/article/pii/S0361476X13000209)
5. **AI不能只优化眼前表现。** Bastani等（2025）在高中数学场景研究发现，无护栏的生成式AI辅助可能损害之后独立作答表现。支持本项目保留无答案提示的判断检查；研究不等于已经证明儿童游戏开发中同样的效应大小。[原始研究](https://www.pnas.org/doi/10.1073/pnas.2422633122)。该文后续更正涉及作者单位信息，引用时同时保留[更正记录](https://www.pnas.org/doi/10.1073/pnas.2518204122)。
6. **不要假定方法相加必然更好。** Franzoi等（2025）在真实小学课堂研究提取与分散练习；具体实验条件下，不能把多种方法的组合自动当作额外收益。支持把当前整套亲子流程当待验证的设计，而不是用方法数量宣传效果。[原始研究](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2025.1632206/full)

本设计没有宣称睡前或刚醒来是普适的最佳学习时刻；晚间和晨间只是家庭容易记得的可选习惯锚点，不挤占睡眠。


## 产品责任与成长参考


[1] [Collins、Brown、Holum：Cognitive Apprenticeship](https://www.aft.org/ae/winter1991/collins_brown_holum)，教学设计框架，不是本项目效果评估。

[2] [MIT Learning Creative Learning](https://lcl.media.mit.edu/)，项目、创作、分享与反思参考。

[3] [Steamworks Review Process](https://partner.steamgames.com/doc/store/review_process)，发布核对入口。

[4] [Steamworks Content Survey](https://partner.steamgames.com/doc/gettingstarted/contentsurvey)，AI内容与内容调查口径。

[5] [Steamworks Steam Playtest](https://partner.steamgames.com/doc/features/playtest)，封闭测试渠道参考。

[6] [Xbox Accessibility Guidelines](https://learn.microsoft.com/en-us/xbox/accessibility/guidelines)，可用性与无障碍设计参考。

[7] [Godot Scene organization](https://docs.godotengine.org/en/stable/tutorials/best_practices/scene_organization.html)、[General optimization tips](https://docs.godotengine.org/en/stable/tutorials/performance/general_optimization.html)、[Saving games](https://docs.godotengine.org/en/stable/tutorials/io/saving_games.html)，职责、测量、持久化的技术参考。实际项目按仓库固定版本核对；示例教程不等于生产级异常恢复已经完成。

## 本轮学习体验修订的依据与限度

- **示范与解释。** [IES：Organizing Instruction and Study to Improve Student Learning](https://ies.ed.gov/ncee/wwc/PracticeGuide/1)建议交替使用示范与问题练习、连接具体与抽象表示、提出解释性问题，各项证据强度不同。用来支持“先给可理解例子，再渐进提炼”，不是每课必须执行完整提问流程，也不证明本课程已经有效。
- **把思考策略放回学科任务。** [EEF：Metacognition and Self-Regulated Learning，第二版，2025](https://educationendowmentfoundation.org.uk/education-evidence/guidance-reports/metacognition)及[证据汇总](https://educationendowmentfoundation.org.uk/education-evidence/teaching-learning-toolkit/metacognition-and-self-regulation)强调明确教学、示范、支架与学科内应用。课程借鉴其方向，不把汇总中的平均学业增益当成儿童游戏开发的预期收益。
- **自主、胜任与支持关系。** Bureau等的[原始元分析](https://journals.sagepub.com/doi/abs/10.3102/00346543211042426)综合144项研究，考察自主支持、心理需要和学习动机的关系。它支持重视选择与可获得的帮助；不能推断选项越多越好、取消所有规则更好，也不保证每个孩子采用同一种教学节奏。
- **具体帮助不等于泛泛鼓励。** Munshi等的[中学科学因果建模研究](https://arxiv.org/abs/2202.09698)涉及98名学习者，报告不同支架结果并不一致，调试与模型检查的策略提示比部分鼓励提示更有用。课程据此警惕只说“再努力”；该场景不是3D开发，不将其结果直接外推为本系统效果。

以上是设计依据，不是临床诊断、保证孩子惊奇的心理公式或已经完成的真人试验。每课开场、选择数量、提示时机和篇幅是可调整的产品设计；没有把它们宣称为某个年龄的普适最佳值。公开资料核对日期：2026-09-18。
