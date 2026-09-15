> v4学生讲义：[A02](../../lessons/A02.md)、[A07](../../lessons/A07.md)。本操作单保留作后续真机补充，课程生成先用统一规格。

# A02 · 真机练习与证据

先完成A；初学时可把B/C留到A08之前。不开复杂游戏系统，不要求手写完整脚本。

## A：一个可看见的盒子

新建Node3D，子节点MeshInstance3D使用BoxMesh，默认边长1；加DirectionalLight3D。Camera3D位置(4,3,6)，可在视口对准模型后使用“将相机对齐到视图”的菜单。运行前确认Camera current已启用。不要把编辑器看得见当成运行相机一定看得见。

保存 `transform_practice.tscn`，F6运行。停下后选盒子：Position X从0到2；恢复；Rotation Y从0°到45°；恢复；Scale Y从1到2。每次写“预计改变什么/什么不会变”。

**验收：** 能自己重置并完成三种不同目标；指出屏幕方向与世界方向的区别。这里只改视觉盒子，不通过缩放角色物理体示范。

## B：父子关系的数值证据

创建Parent(Node3D)及其子Cube(MeshInstance3D)。Parent位置(5,0,0)，Cube位置(2,0,0)。运行时用Remote Inspector或临时打印查看 `global_position`，应为(7,0,0)。

将Parent绕Y旋转90°再测。现在子节点position仍可为(2,0,0)，世界结果却改变。请先预测再查看，不要求背旋转矩阵。

选择子物体，比较世界/局部Gizmo；注意position仍表示相对父节点。额外给子物体Y旋转45°，分别沿父轴、世界轴、自身轴移动，参考网页实验的三种按钮。

**验收：** 新父节点位置/旋转下仍能解释差异，不能只背“Local跟着转”。

## C：门与风车

Node3D命名Hinge，门Mesh为其子节点。BoxMesh尺寸(2,2,0.2)，门相对Hinge位置(1,1,0)。旋转Hinge的Y角度0→90°，观察左边缘不动。

中心轴版本：轴节点位置(1,0,0)，门相对位置(0,1,0)，保持关闭时几何和前一个版本重合。比较轨迹。不要用同时平移整扇门制造“支点效果”。

**迁移：** 设计风车，说明为什么中心轴反而合理。

## D：Blender对照（本课选做，B02前完成）

保存新文件后，在Object Mode移动默认Cube；重置。再在Edit Mode全选顶点移动，返回Object Mode观察Location与Origin。两种操作看似都移动了几何，但相对对象基准的关系不同。

临时把工具Pivot设为3D Cursor，和真正调整Object Origin对照。不要对有绑定/动画的角色实验Apply All；静态小资产也只应用确认需要的变换。

## 出错先查

看不见：运行相机/位置/朝向/裁剪/可见性；世界位置不对：父节点、top_level和坐标空间；门轴不对：轴节点与几何相对偏移。不要先要求AI重做整个场景。

## 提交证据

课号、概念ID、Godot版本、预测、三组参数、一个错误及恢复过程、一条新情境解释。用[学习日志](../../../assessments/learning-log.md)。示例提交信息：`practice: verify transform and hinge invariants`。

技术校核见[来源表](../../../docs/sources.md)。
