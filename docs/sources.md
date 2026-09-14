# 技术与教学依据

核对日期：2026-09-14。示例目标基线：Godot 4.7.2 standard/GDScript，Compatibility 渲染器；不是对所有Godot4版本作运行保证。Blender操作按4.x/5.x通用概念设计，具体菜单和导出选项须以本机版本为准。

## Godot 官方

- [Node3D](https://docs.godotengine.org/en/stable/classes/class_node3d.html)：position 与 transform 的父节点空间，global_position，角度/弧度。用于 C01/C02/C03。
- [CharacterBody3D](https://docs.godotengine.org/en/stable/classes/class_characterbody3d.html)：velocity、move_and_slide、is_on_floor、斜坡。用于 C05/C07/C08。
- [Area3D](https://docs.godotengine.org/en/stable/classes/class_area3d.html)：body_entered、monitoring 和 layer/mask。用于 C06/C15。
- [SpringArm3D](https://docs.godotengine.org/en/stable/classes/class_springarm3d.html)：相机距离与碰撞检测。用于 C09。
- [StandardMaterial3D 工作流](https://docs.godotengine.org/en/stable/tutorials/3d/standard_material_3d.html)：Roughness、Emission、Normal Map、透明模式。用于 C12–C14。
- [3D导入格式](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/available_formats.html)：glTF/GLB 与 .blend 导入依赖。用于 C11。
- [性能总览](https://docs.godotengine.org/en/stable/tutorials/performance/index.html)：测量先于优化。用于 C19/C26。
- [Resource](https://docs.godotengine.org/en/stable/classes/class_resource.html)：共享、复制、本地场景资源。用于 C04/C22。
- [Godot 4.7.2发行资产](https://github.com/godotengine/godot-builds/releases/tag/4.7.2-stable)：测试使用固定发行版而非自动追踪 latest。

## Blender 官方

- [Object Origin](https://docs.blender.org/manual/en/latest/scene_layout/object/origin.html)
- [Pivot Point](https://docs.blender.org/manual/en/latest/editors/3dview/controls/pivot_point/index.html)
- [Apply Transform](https://docs.blender.org/manual/en/latest/scene_layout/object/editing/apply.html)
- [glTF导出](https://docs.blender.org/manual/en/latest/addons/import_export/scene_gltf2.html)

文档链接是查证入口，版本变化时须再次核对；不能因为一个链接存在就宣称本机导出已经测试。

## OpenMAIC 官方

- [README](https://github.com/THU-MAIC/OpenMAIC)
- [生成流程](https://github.com/THU-MAIC/OpenMAIC/blob/main/skills/openmaic/references/generate-flow.md)

本课程的Markdown是教学规格，不是OpenMAIC承诺支持的专有文件格式。本版不实现自动调用，不需要把任何访问码提交到仓库。

## 学习设计依据与边界

- Roediger & Karpicke (2006), *Test-enhanced learning: taking memory tests improves long-term retention*. DOI: 10.1111/j.1467-9280.2006.01693.x；[PubMed](https://pubmed.ncbi.nlm.nih.gov/16507066/)。该研究支持在学习中加入主动检索，但不是对本套3D实操课程的直接验证。
- Cepeda et al. (2008), *Spacing effects in learning: a temporal ridgeline of optimal retention*. DOI: 10.1111/j.1467-9280.2008.02209.x；[PubMed](https://pubmed.ncbi.nlm.nih.gov/19076480/)。间隔和保持目标有关，不能据此断言1/3/7/21天对所有人最优。

本项目据此采用检索与间隔复现；“预测—操作—解释—迁移”、评分0–3、每课小范围和关卡门槛是教学设计选择，需要试学检验。不得把课程设计建议写成已证明的效果提升或替代人工评价的能力。
