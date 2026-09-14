# Blender素材练习｜到B07再做

`create_star.py` 在Blender中生成简单星星，保留脚本的非破坏性约定；它是实现工具，不要求学员背Python或手工完成所有建模步骤。运行前保存自己的场景副本。

本阶段M：检查模型尺寸、原点、朝向、法线与导入结果；选择是否需要应用对象变换。K：顶点/边/面、UV用途等按当前课要求学习，不从静态星星扩展到完整手工绑定。

工作流：Blender运行脚本或手动建星星→检查尺寸和原点→选中导出GLB→Godot包装场景中挂视觉→保留触发/碰撞节点→改源素材再导出一次，确认功能没被覆盖。不要盲目Apply全部变换到已经绑定的角色；角色管线留中级。

参考工程用 `game/assets/star.obj`，另外保留 `game/assets/star.gltf` 作静态资产往返材料；glTF生成脚本在 `tools/make_star.py`。这是两种教学格式，不应推断OBJ携带完整骨骼动画。

Blender实际脚本执行、GLB往返及视觉仍需本机验收。Python语法检查与Godot模型导入都不能代替Blender验证。[素材记录](../docs/assets-manifest.md)
