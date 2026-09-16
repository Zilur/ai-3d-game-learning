# Godot共享实验目录

[统一入口与分工](../../LABS-START.md) · [逐课核对](../../curriculum/practical-resource-audit.md)

打开`lab_hub.tscn`按F6；新主游戏按Esc选择概念实验；旧参考`Concept labs`按钮也进入此目录。相邻课共享实验，只看当前任务。新增侧栏中文、可滚动，固定相机避免不必要的镜头控制。

新增navigation：真实导航与碰撞半径；shader：已编译空间Shader；effects：雾/辉光/景深；large_scene：MultiMesh/LOD/遮挡/驻留与真实异步请求。

camera：真实透视/正交和方向；event：按钮注入的条件/状态/反馈/重开；interaction：实际Area/门条件/专用存档及异常；platform：真实物理承载；animation：已导入原创骨架、蒙皮、三动作与AnimationTree。

collision补真实Layer/Mask与装饰对照，Reset同时恢复开关；motion区分恢复参数和保参重播；material支持真实共享/独立及Emission/实际光源。现有空间、视觉和A03起点保留。

多数实验在运行时构建节点；Remote场景树可观察，不需要在编辑器里重建。完整恢复重置当前实验，门的持久化文件另有专用删除按钮。脚本实现与实验结果不是学员已掌握的证明。
