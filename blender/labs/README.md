# Blender 概念实验室

这些文件用于“拖参数看效果”，不是正式项目资产。

## transform_origin_lab.blend

练习：

- `Door_Center` / `Door_Hinge` 的 Rotation Z。
- Origin 改变为什么会改变旋转轨迹。
- `Scale_Unapplied` / `Scale_Applied` 的 Object Scale 与 Dimensions。

重点：知道什么时候要检查 Origin / Scale，不把 `Apply Transform` 当万能修复。

## kitbash_style_lab.blend

练习：

- `Variant_Roof` 的比例。
- 门窗/雨棚/烟囱模块保留或隐藏。
- `Wall_Variant`、`Roof_Variant` 材质的 Base Color / Roughness。
- 在相同 Camera/Light 下比较 BASE 与 VARIANT。

重点：套装二开不是“越改越多”，而是先保留合格部分，只改影响固定机位观感的关键关系。

## 可重建源

`build_labs.py` 是 `.blend` 的可重建源。课程固定用 Blender 5.2 LTS 系列；二进制文件生成时记录具体 patch 版本。

运行示例：

```bash
blender --background --python blender/labs/build_labs.py -- --output-dir blender/labs
```

学员不需要学习这段 Python；它用于维护者确保实验可重建。
