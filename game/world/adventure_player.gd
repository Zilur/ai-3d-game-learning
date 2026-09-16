extends "res://scripts/player.gd"
signal strike_window
var rig: Node3D
var animator: AnimationPlayer
var animation_tree: AnimationTree
var attack_time := -1.0
var hit_confirmed := false
var training_enabled := true
var controls_enabled := true
var attack_count := 0

func _enter_tree() -> void:
	super._enter_tree()
	if not InputMap.has_action("attack"):
		InputMap.add_action("attack")
		var key := InputEventKey.new()
		key.physical_keycode = KEY_J
		InputMap.action_add_event("attack", key)

func _ready() -> void:
	super._ready()
	for node in visual.get_children(): node.hide()
	rig = preload("res://assets/practice_robot.gltf").instantiate()
	rig.position.y = -0.9
	visual.add_child(rig)
	# Accessories follow the actual Hip bone; the weighted source is unchanged.
	var skeleton := find_class(rig, "Skeleton3D") as Skeleton3D
	var attachment := BoneAttachment3D.new()
	attachment.bone_name = "Hip"
	skeleton.add_child(attachment)
	accessory(attachment, Vector3(0,1.07,0), Vector3(0.52,0.18,0.46), Color("d6be85"))
	accessory(attachment, Vector3(0,0.96,0), Vector3(0.72,0.065,0.65), Color("d6be85"))
	accessory(attachment, Vector3(0,0.05,0.27), Vector3(0.34,0.38,0.2), Color("ab7250"))
	for x in [-0.1,0.1]: accessory(attachment, Vector3(x,0.74,-0.265), Vector3(0.045,0.045,0.025), Color("25474b"))
	animator = find_class(rig, "AnimationPlayer") as AnimationPlayer
	var names := {}
	for name in animator.get_animation_list():
		for key in ["Idle", "Walk", "Attack"]:
			if str(name).ends_with(key): names[key] = name
	for key in ["Idle", "Walk"]: animator.get_animation(names[key]).loop_mode = Animation.LOOP_LINEAR
	var graph := AnimationNodeBlendTree.new()
	var locomotion := AnimationNodeBlendSpace1D.new()
	locomotion.min_space = 0
	locomotion.max_space = 1
	for i in range(2):
		var clip := AnimationNodeAnimation.new()
		clip.animation = names["Idle" if i == 0 else "Walk"]
		locomotion.add_blend_point(clip, float(i), -1, "Idle" if i == 0 else "Walk")
	var attack := AnimationNodeAnimation.new()
	attack.animation = names.Attack
	var one_shot := AnimationNodeOneShot.new()
	one_shot.fadein_time = 0.06
	one_shot.fadeout_time = 0.15
	graph.add_node("Locomotion", locomotion)
	graph.add_node("Attack", attack)
	graph.add_node("Strike", one_shot)
	graph.connect_node("Strike", 0, "Locomotion")
	graph.connect_node("Strike", 1, "Attack")
	graph.connect_node("output", 0, "Strike")
	animation_tree = AnimationTree.new()
	rig.add_child(animation_tree)
	animation_tree.anim_player = animation_tree.get_path_to(animator)
	animation_tree.tree_root = graph
	animation_tree.active = true

func find_class(node: Node, kind: String) -> Node:
	if node.is_class(kind): return node
	for child in node.get_children():
		var found := find_class(child, kind)
		if found != null: return found
	return null

func begin_attack() -> bool:
	if not training_enabled or not controls_enabled or attack_time >= 0 or not is_on_floor(): return false
	attack_time = 0
	hit_confirmed = false
	attack_count += 1
	animation_tree.set("parameters/Strike/request", AnimationNodeOneShot.ONE_SHOT_REQUEST_FIRE)
	return true

func cancel_attack() -> void:
	attack_time = -1
	hit_confirmed = false
	if is_instance_valid(animation_tree): animation_tree.set("parameters/Strike/request", AnimationNodeOneShot.ONE_SHOT_REQUEST_ABORT)

func _physics_process(delta: float) -> void:
	if not controls_enabled:
		velocity = Vector3.ZERO
		return
	if Input.is_action_just_pressed("attack"): begin_attack()
	if attack_time >= 0:
		var previous := attack_time
		attack_time += delta
		velocity.x = 0
		velocity.z = 0
		if not is_on_floor(): velocity.y -= gravity * delta
		move_and_slide()
		if not hit_confirmed and previous <= 0.52 and attack_time >= 0.23: strike_window.emit()
		if attack_time >= 0.85: attack_time = -1
	else:
		super._physics_process(delta)
	if is_instance_valid(animation_tree):
		animation_tree.set("parameters/Locomotion/blend_position", clampf(Vector2(velocity.x, velocity.z).length() / walk_speed, 0, 1))

func respawn() -> void:
	cancel_attack()
	super.respawn()

func accessory(parent: Node3D, at: Vector3, size: Vector3, color: Color) -> void:
	var mesh := MeshInstance3D.new()
	var box := BoxMesh.new()
	box.size = size
	mesh.mesh = box
	var material := StandardMaterial3D.new()
	material.albedo_color = color
	material.roughness = 0.95
	mesh.material_override = material
	parent.add_child(mesh)
	mesh.position = at
