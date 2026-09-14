# 专业词怎么查

本版不再维护另一套可能与课程分级冲突的词典。术语、中文解释、学习深度和复现课次统一放在 [概念分级与复现地图](../curriculum/concept-map.md)。

## 最容易混淆的九组

| 容易混淆 | 应该怎样区分 | 练习 |
|---|---|---|
| Position / Scale / Dimensions | 位置、相对倍数、实际尺寸不是一回事 | C01 |
| Parent / Object-local / World | 父节点坐标、物体自己的轴、世界轴分别识别；position 通常相对父节点 | C02 |
| Origin / Pivot | 对象原点与一次操作选定的中心可能不同；Godot 可用父 Node3D 做门轴 | C03 |
| Scene Instance / 绘制实例化 | 复用场景结构不等于用一次绘制高效画很多物体 | C04/C22/C26 |
| Mesh / Collision | 显示形状和物理形状分开检查 | C05 |
| Layer / Mask | 我属于哪组；我检查哪组。Area 检测有方向 | C06 |
| Roughness / Metallic / 暗色 | 粗糙度不是亮度；金属不是“所有高光都开1” | C12 |
| Emission / Glow / Light | 自己亮、光晕、照亮旁物要分别验证 | C13 |
| FPS / 帧时间 / CPU与GPU工作耗时 | 不是同一种计量；同条件测量，不用总帧时间猜唯一瓶颈 | C19 |

技术查证入口见 [sources](../docs/sources.md)。背不出 API 名称时可以查询；说不清正在改什么、为什么改、怎么验收时，应返回对应实验。
