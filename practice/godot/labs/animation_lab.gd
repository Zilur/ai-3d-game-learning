extends "res://labs/lab_shell.gd"
## Imported skin and clips + real AnimationTree. Original block rig, not commercial art.
var model: Node3D
var player: AnimationPlayer
var tree: AnimationTree
var skeleton: Skeleton3D
var blend := 0.0
var target_blend := 0.0
var transition := 0.3
var strike_time := -1.0
var hit_once := false
var hits := 0
var target_in_range := true
var dummy: MeshInstance3D
var library_names: Dictionary = {}

func _ready() -> void:
	setup("C03 / C04 / D05 / D06｜动作", "已备好原创骨架、蒙皮和三段动作。先调待机/行走融合，再比较动作播放与有效命中。")
	camera.position = Vector3(4, 3, 6)
	camera.fov = 42
	camera.look_at(Vector3(-0.9, 1.0, 0))
	model = load("res://assets/practice_robot.gltf").instantiate()
	stage.add_child(model)
	player = find_type(model, "AnimationPlayer") as AnimationPlayer
	skeleton = find_type(model, "Skeleton3D") as Skeleton3D
	if player == null or skeleton == null:
		status.text = "导入缺少动画或骨架，请停止；不能假装成功"
		return
	for animation_name in player.get_animation_list():
		for key in ["Idle", "Walk", "Attack"]:
			if str(animation_name).ends_with(key):
				library_names[key] = animation_name
	if library_names.size() != 3:
		status.text = "没有找到三段所需动作，请检查导入"
		return
	for key in ["Idle", "Walk"]:
		player.get_animation(library_names[key]).loop_mode = Animation.LOOP_LINEAR
	var locomotion := AnimationNodeBlendSpace1D.new()
	locomotion.min_space = 0
	locomotion.max_space = 1
	for index in range(2):
		var node := AnimationNodeAnimation.new()
		node.animation = library_names["Idle" if index == 0 else "Walk"]
		locomotion.add_blend_point(node, float(index), -1, "Idle" if index == 0 else "Walk")
	var attack := AnimationNodeAnimation.new()
	attack.animation = library_names["Attack"]
	var one := AnimationNodeOneShot.new()
	one.fadein_time = 0.08
	one.fadeout_time = 0.15
	var graph := AnimationNodeBlendTree.new()
	graph.add_node("Locomotion", locomotion)
	graph.add_node("Attack", attack)
	graph.add_node("OneShot", one)
	graph.connect_node("OneShot", 0, "Locomotion")
	graph.connect_node("OneShot", 1, "Attack")
	graph.connect_node("output", 0, "OneShot")
	tree = AnimationTree.new()
	model.add_child(tree)
	tree.anim_player = tree.get_path_to(player)
	tree.tree_root = graph
	tree.active = true
	dummy = box(stage, "TrainingTarget", Vector3(1.1, 0.7, 0), Vector3(0.5, 1.4, 0.5), Color("a78054"))
	slider("blend", "待机0 ←→ 行走1（不移动控制器）", 0, 1, 0, 0.1, func(v): target_blend = v)
	slider("transition", "到达目标融合值的时间", 0, 1, transition, 0.1, func(v): transition = v)
	toggle("range", "目标在有效距离内", true, func(v): target_in_range = v; dummy.position.x = 1.1 if v else 4.0)
	button("attack", "播放一次攻击（不连点叠加）", attack_once)
	button("interrupt", "中断并恢复融合", interrupt_attack)
	text("观察：播Walk并不会自动产生控制器位移。命中在明确窗口只计一次。这个原创骨架不证明其他角色可直接复用；未做通用重定向。")

func find_type(node: Node, kind: String) -> Node:
	if node.is_class(kind):
		return node
	for child in node.get_children():
		var found := find_type(child, kind)
		if found != null:
			return found
	return null

func _process(delta: float) -> void:
	if not is_instance_valid(tree):
		return
	blend = move_toward(blend, target_blend, delta / maxf(transition, 0.001))
	tree.set("parameters/Locomotion/blend_position", blend)
	if strike_time >= 0:
		strike_time += delta
		if strike_time >= 0.25 and strike_time <= 0.65 and not hit_once and Vector2(model.global_position.x, model.global_position.z).distance_to(Vector2(dummy.global_position.x, dummy.global_position.z)) <= 1.5:
			hit_once = true
			hits += 1
		if strike_time > 1.0:
			strike_time = -1.0
	status.text = "骨骼 %d | 融合 %.2f\n动作时间 %.2f | 有效命中 %d\n正在动作 %s" % [skeleton.get_bone_count(), blend, strike_time, hits, str(strike_time >= 0)]

func attack_once() -> void:
	if strike_time >= 0 or not is_instance_valid(tree):
		return
	strike_time = 0
	hit_once = false
	tree.set("parameters/OneShot/request", AnimationNodeOneShot.ONE_SHOT_REQUEST_FIRE)

func interrupt_attack() -> void:
	strike_time = -1
	tree.set("parameters/OneShot/request", AnimationNodeOneShot.ONE_SHOT_REQUEST_ABORT)
