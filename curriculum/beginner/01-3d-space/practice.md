# B01：第一次真正操纵3D

只需Godot。Blender部分可下一次做，不要求第一天同时熟悉两个软件。

## 0. 打开能运行的实验

Godot项目管理器Import → 选择`game/project.godot` → 等导入完成 → 打开`scenes/lab.tscn` → F6。

找不到物体时先检查运行场景和窗口；不要立刻改相机或删节点。实验UI由lab.gd生成，运行时在Remote场景树查看；本课不用读这段界面辅助代码。

复制 [证据单](../../../assessment/evidence-template.md)到本地。界面Prediction只临时保存文字，关闭前自行记录。

## 1. 位置、朝向、比例（C01）

选择Transform。先填预测，再把Position Y从1改2；Reset后把Object Yaw改45；再Reset，把Scale X从1改2。其它值不动。

分别记录：原点移动了吗？鼻部朝向变了吗？轮廓变了吗？不要把旋转时看到的屏幕宽度变化当真实尺寸变化。

答C01-P/R。做到这一步可以结束本次学习。

## 2. 相对谁（C02）

Reset，Scale全部为1；Parent Yaw=90，Object Yaw=45。先写下三个+X按钮的预测方向。

点World +X，记录前后世界坐标。Reset并恢复相同旋转，点Parent +X；再次重复，点Object +X。

不要直接连续点三个按钮再凭印象比较。position是父空间的数值，global_position是世界数值。操作器上物体自己的轴又可能与父轴不同。

答C02-P/R；下次用C02-T复测。能说出“Local/Global”但不能预测方向，还没完成。

## 3. 门轴（C03）

选择Door pivot。保持0度，切换侧轴开关，确认关门时门板位置一致；再分别旋转90度，观察哪条边保持不动。

记录“父轴在哪、门板相对父轴偏移多少”。不是背“Pivot=Origin”，而是理解参考点怎样影响运动。

答C03-P/R；翻页是之后的迁移题。

## 4. Blender对照（可分次）

新练习文件，默认Cube。Object Mode移动对象：观察Location与Origin。撤销；Edit Mode全选顶点再移动：观察几何变了，但对象原点和对象变换不是同一种改动。

选择Pivot为3D Cursor并旋转，观察“操作中心变化”并不自动把对象Origin搬过去。将设置恢复后再保存，避免下一课继承不明状态。

只使用副本，不对已有绑定角色做Apply All。

## 5. 给AI的任务，不给它你的首次答案

```text
我在Godot 4.7.2学习C02。请只帮我检查实验条件：父节点Yaw=90度，
对象自身Yaw=45度，Scale=1。不要先告诉我三个方向的答案。
等我提交预测、前后坐标和解释后，指出我的参照系是否混淆。
如需提示，先提示观察哪里，不直接写修复代码。
```

## 验收

三个微单元分别保存P/R证据；下一次抽一个T。不要求一次全部满分。

还应做到：知道Reset恢复什么；不会用Scale=100掩盖不明导入问题；能把“位置错/朝向错/尺寸错/轴错”区分开。

打印复习：[必须牢记](../../../print/must-remember.md)。技术依据：[sources](../../../docs/sources.md)。
