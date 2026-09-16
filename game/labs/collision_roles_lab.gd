extends Node3D
## Teaching lab: visible mesh, blocking collision and trigger detection are separate roles.

var wall: StaticBody3D
var wall_visual: MeshInstance3D
var wall_shape: CollisionShape3D
var trigger: Area3D
var probe: CharacterBody3D
var status: Label
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

	var camera := Camera3D.new()
	camera.position = Vector3(0, 5.2, 9.5)
	add_child(camera)
	camera.look_at(Vector3(0, 0.6, 0))
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

func _build_ui() -> void:
	var layer := CanvasLayer.new()
	add_child(layer)
	var panel := PanelContainer.new()
	panel.position = Vector2(14, 14)
	layer.add_child(panel)
	var rows := VBoxContainer.new()
	panel.add_child(rows)

	var title := Label.new()
	title.text = "Visual / Collision / Trigger lab"
	rows.add_child(title)
	status = Label.new()
	rows.add_child(status)

	var target_label := Label.new()
	target_label.text = "Target X: move the yellow probe across the wall toward the blue Trigger"
	rows.add_child(target_label)
	target_slider = HSlider.new()
	target_slider.min_value = -3.0
	target_slider.max_value = 3.4
	target_slider.step = 0.1
	target_slider.value = -3.0
	target_slider.custom_minimum_size = Vector2(430, 28)
	target_slider.value_changed.connect(_set_target_x)
	rows.add_child(target_slider)

	var visual_toggle := CheckButton.new()
	visual_toggle.text = "Wall visual visible"
	visual_toggle.button_pressed = true
	visual_toggle.toggled.connect(_set_visual_enabled)
	rows.add_child(visual_toggle)

	var collision_toggle := CheckButton.new()
	collision_toggle.text = "Wall collision enabled"
	collision_toggle.button_pressed = true
	collision_toggle.toggled.connect(_set_collision_enabled)
	rows.add_child(collision_toggle)

	var trigger_toggle := CheckButton.new()
	trigger_toggle.text = "Trigger detection enabled"
	trigger_toggle.button_pressed = true
	trigger_toggle.toggled.connect(_set_trigger_enabled)
	rows.add_child(trigger_toggle)

	var reset := Button.new()
	reset.text = "Reset"
	reset.pressed.connect(_reset_lab)
	rows.add_child(reset)

	var note := Label.new()
	note.text = "Try: hide the wall but keep collision; then disable collision and enter the Trigger.\nVisible != blocking != event detection."
	rows.add_child(note)

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

func _reset_lab() -> void:
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
	status.text = "probe x %.2f | visual %s | collision %s | trigger %s | overlap %s" % [
		probe.position.x,
		"ON" if wall_visual.visible else "OFF",
		"OFF" if wall_shape.disabled else "ON",
		"ON" if trigger.monitoring else "OFF",
		"YES" if trigger_overlap else "NO"
	]
