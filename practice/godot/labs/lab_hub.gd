extends "res://labs/lab_shell.gd"
const LABS = [
	["三段世界：探索 / 训练 / 保存", "res://world/exploration.tscn"],
	["C08｜雾、辉光、景深", "res://labs/effects_lab.tscn"],
	["E01｜导航与真实通行", "res://labs/navigation_lab.tscn"],
	["E03｜Shader对照", "res://labs/shader_lab.tscn"],
	["E02 / E05｜批量、LOD与分块", "res://labs/large_scene_lab.tscn"],
	["A02 / A07｜空间与门轴", "res://scenes/lab.tscn"],
	["A03｜节点：现成小起点", "res://labs/scene_nodes/starter.tscn"],
	["A04｜外观、阻挡、检测与Mask", "res://labs/collision_roles_lab.tscn"],
	["A05 / A06｜速度、跳跃、重力", "res://labs/motion_lab.tscn"],
	["A08｜透视、正交、移动方向", "res://labs/camera_lab.tscn"],
	["B04 / C05｜材质与共享资源", "res://labs/material_lab.tscn"],
	["B06–B08｜事件、状态、重开", "res://labs/event_lab.tscn"],
	["B09 / C02｜光照、密度与留白", "res://scenes/visual_lab.tscn"],
	["C06｜真实移动平台", "res://labs/platform_lab.tscn"],
	["C10 / C11｜交互与存档", "res://labs/interaction_lab.tscn"],
	["C03 / C04 / D05 / D06｜动作", "res://labs/animation_lab.tscn"],
	["完整庭院参考：实际走跑收集", "res://scenes/main.tscn"]
]
func _ready() -> void:
	setup("现成实验目录", "只选择当前课需要的实验。多个课程共用场景，不用逐课重新建模或搭节点。")
	controls["hub"].hide()
	controls["reset"].hide()
	status.text = "Godot 4.7.2｜实验不是完整商业成品\n旧场景也可从右上角返回实验目录。"
	for entry in LABS:
		button(entry[1], entry[0], open_lab.bind(entry[1]))
	text("Blender文件在仓库practice/blender：门轴、套装二开、UV材质、动画骨架。直接打开副本即可；不必执行生成脚本。")
	box(stage, "House", Vector3(1.6, 0.9, 0), Vector3(2.4, 1.8, 2), Color("c4a170"))
	box(stage, "Roof", Vector3(1.6, 2, 0), Vector3(2.8, 0.4, 2.4), Color("985b42"))

func open_lab(path: String) -> void:
	var session := get_node("/root/StudySession")
	if path == "res://world/exploration.tscn" and not session.suspended.is_empty():
		session.resume_world()
	else:
		get_tree().change_scene_to_file(path)
