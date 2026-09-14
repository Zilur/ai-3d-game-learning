# Blender 资产目录

这里保存 Blender 源文件和游戏资产制作说明。

## 初级阶段只学习必要工作流

重点：

- Move / Rotate / Scale
- Origin / Pivot
- Apply Transform
- Mesh / Vertex / Edge / Face
- Extrude / Bevel
- Shade Smooth / Normal
- UV 基础
- Principled BSDF
- Base Color / Metallic / Roughness / Emission
- GLB / glTF 导出

暂时不深入：

- 高级雕刻
- Geometry Nodes 复杂系统
- 高级程序化材质
- 流体 / 布料 / 毛发
- 复杂绑定与角色制作

## 资产进入 Godot 前的基础检查

- 尺寸是否合理
- Origin 是否合理
- Rotation / Scale 是否需要 Apply
- Normal 是否正常
- 材质数量是否必要
- UV 是否存在且合理
- 文件命名是否清楚
- 导出 GLB / glTF 后在 Godot 中是否与预期一致

## 目录建议

```text
blender/
├── props/
├── environment/
├── characters/
└── experiments/
```

课程第一个正式资产将是一个简单的低多边形星星拾取物。
