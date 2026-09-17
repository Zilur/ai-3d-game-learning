extends "res://labs/lab_shell.gd"
## Teaching lab: visible mesh, blocking collision and trigger detection are separate roles.

var switches: Dictionary = {}
var decoration: CharacterBody3D
var decoration_overlap := false
var decor_tween: Tween

var wall: StaticBody3D
var wall_visual: MeshInstance3D
var wall_shape: CollisionShape3D
var trigger: Area3D
var probe: CharacterBody3D
var target_slider: HSlider
var target_x: float = -3.0
var move_speed: float = 3.0
var trigger_overlap: bool = false

func _ready() -> void:
	_build_world()
	_build_ui()
	_refresh()

func _physics_process(_delta: float) -> void:
	if not is_instance_valid(probe):
		return
	var dx := target_x - probe.position.x
	probe.velocity = Vector3.ZERO
	if absf(dx) > 0.03:
		probe.velocity.x = signf(dx) * move_speed
		probe.move_and_slide()
	else:
		probe.position.x = target_x
	if trigger.monitoring:
		trigger_overlap = probe in trigger.get_overlapping_bodies()
	else:
		trigger_overlap = false
	decoration_overlap = decoration in trigger.get_overlapping_bodies() if trigger.monitoring else false
	_refresh()

func _build_world() -> void:
	var environment := WorldEnvironment.new()
	var env := Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color(0.74, 0.82, 0.84)
	environment.environment = env
	add_child(environment)

	var sun := DirectionalLight3D.new()
	sun.rotation_degrees = Vector3(-48, -35, 0)
	sun.light_energy = 1.1
	sun.shadow_enabled = true
	add_child(sun)

	camera = Camera3D.new()
	camera.position = Vector3(0, 5.2, 9.5)
	add_child(camera)
	camera.fov = 52
	camera.look_at(Vector3(-2.0, 0.6, 0))
	camera.current = true

	var floor_mesh := MeshInstance3D.new()
	var floor_box := BoxMesh.new()
	floor_box.size = Vector3(10, 0.2, 5)
	floor_mesh.mesh = floor_box
	var floor_mat := StandardMaterial3D.new()
	floor_mat.albedo_color = Color(0.48, 0.64, 0.42)
	floor_mat.roughness = 0.95
	floor_mesh.material_override = floor_mat
	floor_mesh.position.y = -0.1
	add_child(floor_mesh)

	wall = StaticBody3D.new()
	wall.name = "Wall"
	wall.collision_layer = 1
	add_child(wall)
	wall_visual = MeshInstance3D.new()
	var wall_mesh := BoxMesh.new()
	wall_mesh.size = Vector3(0.45, 1.8, 4.0)
	wall_visual.mesh = wall_mesh
	var wall_mat := StandardMaterial3D.new()
	wall_mat.albedo_color = Color(0.70, 0.48, 0.31)
	wall_mat.roughness = 0.9
	wall_visual.material_override = wall_mat
	wall_visual.position.y = 0.9
	wall.add_child(wall_visual)
	wall_shape = CollisionShape3D.new()
	var wall_box := BoxShape3D.new()
	wall_box.size = Vector3(0.45, 1.8, 4.0)
	wall_shape.shape = wall_box
	wall_shape.position.y = 0.9
	wall.add_child(wall_shape)

	trigger = Area3D.new()
	trigger.name = "Trigger"
	trigger.position = Vector3(2.2, 0.6, 0)
	trigger.collision_layer = 0
	trigger.collision_mask = 2
	trigger.monitoring = true
	add_child(trigger)
	var trigger_visual := MeshInstance3D.new()
	var trigger_mesh := BoxMesh.new()
	trigger_mesh.size = Vector3(1.4, 1.2, 2.4)
	trigger_visual.mesh = trigger_mesh
	var trigger_mat := StandardMaterial3D.new()
	trigger_mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	trigger_mat.albedo_color = Color(0.25, 0.70, 0.86, 0.28)
	trigger_mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	trigger_visual.material_override = trigger_mat
	trigger.add_child(trigger_visual)
	var trigger_shape := CollisionShape3D.new()
	var trigger_box := BoxShape3D.new()
	trigger_box.size = Vector3(1.4, 1.2, 2.4)
	trigger_shape.shape = trigger_box
	trigger.add_child(trigger_shape)

	probe = CharacterBody3D.new()
	probe.name = "Probe"
	probe.position = Vector3(-3.0, 0.45, 0)
	probe.collision_layer = 2
	probe.collision_mask = 1
	add_child(probe)
	var probe_visual := MeshInstance3D.new()
	var probe_mesh := SphereMesh.new()
	probe_mesh.radius = 0.38
	probe_mesh.height = 0.76
	probe_visual.mesh = probe_mesh
	var probe_mat := StandardMaterial3D.new()
	probe_mat.albedo_color = Color(0.95, 0.72, 0.18)
	probe_mat.roughness = 0.75
	probe_visual.material_override = probe_mat
	probe.add_child(probe_visual)
	var probe_shape := CollisionShape3D.new()
	var sphere := SphereShape3D.new()
	sphere.radius = 0.38
	probe_shape.shape = sphere
	probe.add_child(probe_shape)

	decoration = CharacterBody3D.new()
	decoration.name = "DecorationLayer3"
	decoration.collision_layer = 4
	decoration.collision_mask = 0
	decoration.position = Vector3(4.0, 0.35, 0.8)
	add_child(decoration)
	var decor_mesh := MeshInstance3D.new()
	var sphere_mesh := SphereMesh.new()
	sphere_mesh.radius = 0.25
	sphere_mesh.height = 0.5
	decor_mesh.mesh = sphere_mesh
	decoration.add_child(decor_mesh)
	var decor_shape := CollisionShape3D.new()
	var sphere_shape := SphereShape3D.new()
	sphere_shape.radius = 0.25
	decor_shape.shape = sphere_shape
	decoration.add_child(decor_shape)

func _build_ui() -> void:
	setup_ui("A04｜外观、阻挡与检测", "把黄色角色移向蓝色检测区。先猜：只隐藏墙，能不能通过？")
	target_slider = slider("target", "角色的目标位置 X", -3, 3.4, -3, 0.1, _set_target_x)
	switches["visual"] = toggle("visual", "墙的外观可见", true, _set_visual_enabled)
	switches["collision"] = toggle("collision", "墙的物理阻挡", true, _set_collision_enabled)
	switches["trigger"] = toggle("trigger", "检测区启用", true, _set_trigger_enabled)
	switches["player_mask"] = toggle("player_mask", "检测角色（第2层）", true, _set_mask_bit.bind(2))
	switches["decor_mask"] = toggle("decor_mask", "检测装饰（第3层）", false, _set_mask_bit.bind(4))
	button("decor_enter", "让白色装饰重新进入检测区", _replay_decoration)
	text("改变检测范围后，让对象退出再进入。蓝框是检测区的示意外观；是否命中以真实Area重叠记录为准。")

func reset_lab() -> void:
	_reset_lab()

func _set_target_x(value: float) -> void:
	target_x = clampf(value, -3.0, 3.4)

func _set_visual_enabled(enabled: bool) -> void:
	wall_visual.visible = enabled
	_refresh()

func _set_collision_enabled(enabled: bool) -> void:
	wall_shape.set_deferred("disabled", not enabled)
	_refresh()

func _set_trigger_enabled(enabled: bool) -> void:
	trigger.monitoring = enabled
	if not enabled:
		trigger_overlap = false
	_refresh()

func _replay_decoration() -> void:
	if decor_tween:
		decor_tween.kill()
	decoration.position.x = 4.0
	decor_tween = create_tween()
	decor_tween.set_process_mode(Tween.TWEEN_PROCESS_PHYSICS)
	decor_tween.tween_interval(0.1)
	decor_tween.tween_property(decoration, "position:x", 2.2, 0.5)

func _set_mask_bit(enabled: bool, bit: int) -> void:
	trigger.collision_mask = (trigger.collision_mask | bit) if enabled else (trigger.collision_mask & ~bit)

func _reset_lab() -> void:
	if decor_tween:
		decor_tween.kill()
	decoration.position = Vector3(4, 0.35, 0.8)
	for key in ["visual", "collision", "trigger", "player_mask"]:
		switches[key].set_pressed_no_signal(true)
	switches["decor_mask"].set_pressed_no_signal(false)
	trigger.collision_mask = 2
	decoration_overlap = false
	target_x = -3.0
	if is_instance_valid(target_slider):
		target_slider.value = -3.0
	probe.position = Vector3(-3.0, 0.45, 0)
	probe.velocity = Vector3.ZERO
	wall_visual.visible = true
	wall_shape.set_deferred("disabled", false)
	trigger.monitoring = true
	trigger_overlap = false
	_refresh()

func _refresh() -> void:
	if not is_instance_valid(status) or not is_instance_valid(probe):
		return
	status.text = "角色X %.2f\n外观 %s | 阻挡 %s | 检测 %s\n检测到角色 %s | 装饰 %s" % [
		probe.position.x, "开" if wall_visual.visible else "关",
		"关" if wall_shape.disabled else "开", "开" if trigger.monitoring else "关",
		"是" if trigger_overlap else "否", "是" if decoration_overlap else "否"]
