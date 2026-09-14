extends Node3D
## Reference laboratory. Learners adjust controls, not this UI-building code.

var _experiment: Node3D
var _controls: VBoxContainer
var _status: Label
var _prediction: LineEdit
var _instruction: Label
var _explanation: Label
var _reveal: CheckButton
var _mode: int = 0
var _subject: Node3D
var _parent_space: Node3D
var _door_board: MeshInstance3D
var _material: StandardMaterial3D
var _neighbor_light: OmniLight3D
var _door_angle: float = 0.0
var _position_sliders: Array[HSlider] = []

func _ready() -> void:
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	_build_stage()
	_build_ui()
	_switch_mode(0)

func _build_stage() -> void:
	_box(self, "Floor", Vector3(10, 0.1, 10), Vector3(0, -0.1, 0), Color(0.3, 0.34, 0.38))
	var environment := Environment.new()
	environment.background_mode = Environment.BG_SKY
	var sky := Sky.new()
	sky.sky_material = ProceduralSkyMaterial.new()
	environment.sky = sky
	var world_environment := WorldEnvironment.new()
	world_environment.environment = environment
	add_child(world_environment)
	var sun := DirectionalLight3D.new()
	sun.rotation_degrees = Vector3(-45, -30, 0)
	sun.light_energy = 1.2
	sun.shadow_enabled = true
	add_child(sun)
	var camera := Camera3D.new()
	camera.position = Vector3(7, 5.5, 9)
	camera.current = true
	add_child(camera)
	camera.look_at(Vector3(0, 1, 0), Vector3.UP)
	_experiment = Node3D.new()
	_experiment.name = "Experiment"
	add_child(_experiment)

func _build_ui() -> void:
	var canvas := CanvasLayer.new()
	add_child(canvas)
	var panel := PanelContainer.new()
	panel.position = Vector2(12, 12)
	panel.size = Vector2(350, 696)
	canvas.add_child(panel)
	var scroll := ScrollContainer.new()
	panel.add_child(scroll)
	var layout := VBoxContainer.new()
	layout.custom_minimum_size.x = 320
	layout.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	scroll.add_child(layout)
	var heading := Label.new()
	heading.text = "PREDICT -> CHANGE -> EXPLAIN"
	layout.add_child(heading)
	var modes := OptionButton.new()
	for title in ["Transform", "Door pivot", "Material"]:
		modes.add_item(title)
	modes.item_selected.connect(_switch_mode)
	layout.add_child(modes)
	_instruction = _text_label(layout, "")
	_prediction = LineEdit.new()
	_prediction.placeholder_text = "Write your prediction before changing..."
	layout.add_child(_prediction)
	_controls = VBoxContainer.new()
	layout.add_child(_controls)
	var reset := Button.new()
	reset.text = "Reset experiment (keep prediction)"
	reset.pressed.connect(func(): _switch_mode(_mode))
	layout.add_child(reset)
	_status = _text_label(layout, "")
	_reveal = CheckButton.new()
	_reveal.text = "Reveal explanation AFTER trying"
	layout.add_child(_reveal)
	_explanation = _text_label(layout, "")
	_explanation.visible = false
	_reveal.toggled.connect(func(enabled: bool): _explanation.visible = enabled)
	var back := Button.new()
	back.text = "Back to star demo (new game)"
	back.pressed.connect(func(): get_tree().change_scene_to_file("res://scenes/main.tscn"))
	layout.add_child(back)

func _text_label(parent: Node, text: String) -> Label:
	var label := Label.new()
	label.text = text
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	label.custom_minimum_size.x = 310
	parent.add_child(label)
	return label

func _switch_mode(index: int) -> void:
	_mode = index
	_position_sliders.clear()
	for parent in [_experiment, _controls]:
		for child in parent.get_children():
			parent.remove_child(child)
			child.queue_free()
	_subject = null
	_parent_space = null
	_reveal.button_pressed = false
	_explanation.visible = false
	if index == 0:
		_build_transform()
	elif index == 1:
		_build_door()
	else:
		_build_material()

func _build_transform() -> void:
	_instruction.text = "Change ONE value. For direction tests: reset, keep Scale=1, then rotate parent and object. Nose points along object +X."
	_explanation.text = "position is parent-relative. World +X uses fixed world X. Object +X follows the object's rotated axis. Scale=1 is not a size in meters."
	_axes(_experiment, 3.0, "W")
	_parent_space = Node3D.new()
	_parent_space.name = "ReferenceParent"
	_experiment.add_child(_parent_space)
	_axes(_parent_space, 2.0, "P")
	_subject = Node3D.new()
	_subject.name = "Subject"
	_subject.position = Vector3(0, 1, 0)
	_parent_space.add_child(_subject)
	_box(_subject, "Body", Vector3(1.3, 0.6, 0.6), Vector3.ZERO, Color(0.15, 0.6, 0.8))
	_box(_subject, "Nose", Vector3(0.4, 0.3, 0.3), Vector3(0.8, 0, 0), Color(0.95, 0.4, 0.1))
	_axes(_subject, 1.2, "O")
	for axis in range(3):
		var axis_name: String = ["X", "Y", "Z"][axis]
		var control := _slider("Position " + axis_name, -3.0, 3.0, _subject.position[axis], 0.0, _set_component.bind("position", axis))
		_position_sliders.append(control)
	_slider("Object Yaw", -180, 180, 0, 5, _set_component.bind("rotation_degrees", 1))
	for axis in range(3):
		var axis_name: String = ["X", "Y", "Z"][axis]
		_slider("Scale " + axis_name, 0.25, 3, 1, 0.25, _set_component.bind("scale", axis))
	_slider("Parent Yaw", -180, 180, 0, 5, _set_parent_yaw)
	_button("World +X", _move_world_x)
	_button("Parent +X", _move_parent_x)
	_button("Object +X", _move_object_x)

func _set_component(value: float, property: String, axis: int) -> void:
	var vector: Vector3 = _subject.get(property)
	vector[axis] = value
	_subject.set(property, vector)

func _set_parent_yaw(value: float) -> void:
	_parent_space.rotation_degrees.y = value

func _move_world_x() -> void:
	_subject.global_position += Vector3.RIGHT
	_sync_position_controls()

func _move_parent_x() -> void:
	_subject.position += Vector3.RIGHT
	_sync_position_controls()

func _move_object_x() -> void:
	# Normalize so each click travels one WORLD unit despite visual scale.
	_subject.global_position += _subject.global_basis.x.normalized()
	_sync_position_controls()

func _sync_position_controls() -> void:
	for axis in range(_position_sliders.size()):
		var control := _position_sliders[axis]
		var value: float = _subject.position[axis]
		# Expand the range if a button moved outside the original slider range.
		control.min_value = minf(-3.0, value)
		control.max_value = maxf(3.0, value)
		control.set_value_no_signal(value)
		var label: Label = control.get_meta("value_label")
		label.text = "Position %s: %.2f" % [["X", "Y", "Z"][axis], value]

func _build_door() -> void:
	_instruction.text = "Predict which edge stays fixed. Compare center and side pivots at the SAME angle. Reset before comparing."
	_explanation.text = "The parent provides the hinge axis. The child board is offset from it. In Blender the object Origin and the selected operation Pivot can differ."
	_subject = Node3D.new()
	_subject.name = "Hinge"
	_experiment.add_child(_subject)
	_door_board = _box(_subject, "Board", Vector3(2, 2.5, 0.15), Vector3.ZERO, Color(0.55, 0.28, 0.12))
	_box(_subject, "AxisMarker", Vector3(0.06, 3, 0.06), Vector3.ZERO, Color(0.95, 0.8, 0.2))
	_door_angle = 0.0
	_set_side_pivot(false)
	_slider("Open angle (degrees)", 0, 120, 0, 5, _set_door_angle)
	_toggle("Use SIDE hinge instead of CENTER", _set_side_pivot)

func _set_door_angle(value: float) -> void:
	_door_angle = value
	_subject.rotation_degrees.y = value

func _set_side_pivot(enabled: bool) -> void:
	# At angle=0, the board has the same world position in BOTH modes.
	_subject.position = Vector3(-1 if enabled else 0, 1.25, 0)
	_door_board.position = Vector3(1 if enabled else 0, 0, 0)
	_subject.rotation_degrees.y = _door_angle

func _build_material() -> void:
	_instruction.text = "Keep camera and sun fixed. Compare one slider at a time. Watch BOTH the sphere and the neighbor cube."
	_explanation.text = "Roughness is not darkness. Metallic is not a general brightness control. Emission makes this surface bright; the separate light illuminates neighbors. This setup has no GI or glow."
	var sphere := MeshInstance3D.new()
	sphere.name = "Sample"
	var mesh := SphereMesh.new()
	mesh.radius = 0.8
	mesh.height = 1.6
	sphere.mesh = mesh
	sphere.position = Vector3(0, 1, 0)
	_material = StandardMaterial3D.new()
	_material.albedo_color = Color(0.9, 0.5, 0.12)
	_material.roughness = 0.5
	_material.emission_enabled = true
	_material.emission = Color(1, 0.5, 0.1)
	_material.emission_energy_multiplier = 0.0
	sphere.material_override = _material
	_experiment.add_child(sphere)
	_subject = sphere
	_box(_experiment, "Neighbor", Vector3(1, 1, 1), Vector3(2, 0.5, 0), Color(0.6, 0.6, 0.6))
	_neighbor_light = OmniLight3D.new()
	_neighbor_light.position = Vector3(0.7, 1.7, 1)
	_neighbor_light.light_energy = 2.0
	_neighbor_light.omni_range = 5.0
	_neighbor_light.visible = false
	_experiment.add_child(_neighbor_light)
	_slider("Roughness", 0, 1, 0.5, 0.05, _set_material_parameter.bind("roughness"))
	_slider("Metallic", 0, 1, 0, 0.05, _set_material_parameter.bind("metallic"))
	_slider("Emission", 0, 3, 0, 0.1, _set_material_parameter.bind("emission_energy_multiplier"))
	_toggle("Separate light ON (not emission)", func(enabled: bool): _neighbor_light.visible = enabled)

func _set_material_parameter(value: float, property: String) -> void:
	_material.set(property, value)

func _process(_delta: float) -> void:
	if not is_instance_valid(_subject):
		return
	if _mode == 0:
		_status.text = "Parent position: %s\nWorld position: %s\nPosition sliders follow actual parent-relative coordinates." % [_subject.position, _subject.global_position]
	elif _mode == 1:
		_status.text = "Angle: %.0f degrees\nHinge world position: %s" % [_door_angle, _subject.global_position]
	else:
		_status.text = "Roughness %.2f | Metallic %.2f\nEmission %.2f" % [_material.roughness, _material.metallic, _material.emission_energy_multiplier]

func _button(title: String, callback: Callable) -> void:
	var button := Button.new()
	button.text = title
	button.pressed.connect(callback)
	_controls.add_child(button)

func _toggle(title: String, callback: Callable) -> void:
	var button := CheckButton.new()
	button.text = title
	button.toggled.connect(callback)
	_controls.add_child(button)

func _slider(title: String, minimum: float, maximum: float, initial: float, step: float, callback: Callable) -> HSlider:
	var label := Label.new()
	label.text = "%s: %.2f" % [title, initial]
	_controls.add_child(label)
	var slider := HSlider.new()
	slider.min_value = minimum
	slider.max_value = maximum
	slider.step = step
	slider.value = initial
	slider.set_meta("value_label", label)
	slider.value_changed.connect(_slider_changed.bind(label, title, callback))
	_controls.add_child(slider)
	return slider

func _slider_changed(value: float, label: Label, title: String, callback: Callable) -> void:
	label.text = "%s: %.2f" % [title, value]
	callback.call(value)

func _box(parent: Node, title: String, size: Vector3, location: Vector3, color: Color) -> MeshInstance3D:
	var instance := MeshInstance3D.new()
	instance.name = title
	var mesh := BoxMesh.new()
	mesh.size = size
	instance.mesh = mesh
	var material := StandardMaterial3D.new()
	material.albedo_color = color
	material.roughness = 0.7
	instance.material_override = material
	instance.position = location
	parent.add_child(instance)
	return instance

func _axes(parent: Node3D, length: float, prefix: String) -> void:
	var directions: Array[Vector3] = [Vector3.RIGHT, Vector3.UP, Vector3.BACK]
	var colors: Array[Color] = [Color(0.9, 0.15, 0.15), Color(0.2, 0.8, 0.2), Color(0.2, 0.4, 1)]
	for axis in range(3):
		var size := Vector3(0.018, 0.018, 0.018)
		size[axis] = length
		_box(parent, prefix + "Axis%d" % axis, size, directions[axis] * length / 2.0, colors[axis])
		var label := Label3D.new()
		label.text = prefix + ":" + ["X", "Y", "Z"][axis]
		label.position = directions[axis] * (length + 0.15)
		label.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		label.pixel_size = 0.004
		label.font_size = 32
		parent.add_child(label)
