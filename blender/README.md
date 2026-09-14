# Blender：先做小资产，不学整本软件百科

## 第一次使用

打开一个新的练习文件，切到Object Mode。在Scripting工作区打开`create_star.py`，阅读顶部说明后Run Script。脚本只添加LearningStar，不清场景、不保存、不导出、不覆盖同名对象。再次运行会提示同名对象已存在；这不是需要删除整个场景的错误。

在Outliner选LearningStar，使用Frame Selected（聚焦所选）观察。另存自己的.blend副本；不要把默认Cube、灯和相机一起当成星星导出。

## 练习路线

B01：默认Cube的Location/Rotation/Scale；Object Mode与Edit Mode的区别。

B07：观察星星的Mesh、Origin和Dimensions；材质只用简单Principled BSDF。

B09：选中星星，File → Export → glTF 2.0，选GLB和仅导出选中对象。具体菜单名称以安装版本为准。在Godot保存一层独立拾取场景，将导入模型作为外观，Area与脚本留在Godot层。

## 尺度与轴

本脚本采用Blender默认+Z向上。外半径0.5，厚度0.16，宽约0.951、高约0.905，不是“Scale=1所以尺寸就是1米”。改变尺寸前后记录Dimensions，导入后用已知尺寸Box比较。

静态网格需要时可按工作流Apply Scale；不要对已有骨骼、约束、动画的资产不加检查地Apply All。Origin是对象原点，Pivot可以另选；不把两者合并背成一个词。

## 素材边界

这是无UV的低多边形形状素材，适合常量颜色材质，不作为纹理展开完成品。UV练习使用默认Cube和格子诊断；增加倒角后需重新观察轮廓和面数。没有提供真人角色、骨骼、音效或第三方贴图包。

脚本语法可以由AI维护，学习者必须亲自检查结果。Blender实际执行/导出仍需按 [验证记录](../docs/validation.md)在本机完成，不把脚本存在当成已验证导出。
