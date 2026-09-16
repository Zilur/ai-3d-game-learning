extends Node3D
## Shared presentation only. Actual experiments live in the subclasses.
var camera: Camera3D
var sun: DirectionalLight3D
var stage: Node3D
var rows: VBoxContainer
var status: Label
var controls: Dictionary = {}

func setup(title: String, task: String) -> void:
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	stage = Node3D.new()
	stage.name = "Experiment"
	add_child(stage)
	var environment := WorldEnvironment.new()
	environment.environment = Environment.new()
	environment.environment.background_mode = Environment.BG_COLOR
	environment.environment.background_color = Color("d2dfe2")
	environment.environment.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	environment.environment.ambient_light_color = Color.WHITE
	environment.environment.ambient_light_energy = 0.30
	add_child(environment)
	sun = DirectionalLight3D.new()
	sun.rotation_degrees = Vector3(-48, -32, 0)
	sun.shadow_enabled = true
	sun.light_energy = 0.85
	add_child(sun)
	camera = Camera3D.new()
	camera.position = Vector3(6, 5, 8)
	camera.fov = 50
	camera.current = true
	add_child(camera)
	camera.look_at(Vector3(-1.8, 0.8, 0))
	box(stage, "Ground", Vector3(0, -0.15, 0), Vector3(13, 0.3, 9), Color("89a575"))
	setup_ui(title, task)

func setup_ui(title: String, task: String) -> void:
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	var layer := CanvasLayer.new()
	layer.name = "Instructions"
	add_child(layer)
	var panel := PanelContainer.new()
	panel.set_anchors_and_offsets_preset(Control.PRESET_LEFT_WIDE)
	panel.offset_left = 12
	panel.offset_top = 12
	panel.offset_right = 342
	panel.offset_bottom = -12
	layer.add_child(panel)
	var font := SystemFont.new()
	font.font_names = PackedStringArray(["Noto Sans CJK SC", "Microsoft YaHei", "PingFang SC", "WenQuanYi Zen Hei"])
	var theme := Theme.new()
	theme.default_font = font
	theme.default_font_size = 17
	panel.theme = theme
	var scroll := ScrollContainer.new()
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	panel.add_child(scroll)
	rows = VBoxContainer.new()
	rows.custom_minimum_size.x = 302
	rows.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	rows.add_theme_constant_override("separation", 9)
	scroll.add_child(rows)
	text(title).add_theme_font_size_override("font_size", 22)
	text(task)
	text("先预测 → 只改一项 → 观察 → 讲给爸爸。\n不需要先搭建节点或抄写实现。")
	status = text("")
	button("reset", "恢复本实验全部初值", reset_lab)
	button("hub", "返回实验目录", func(): get_tree().change_scene_to_file("res://labs/lab_hub.tscn"))

func text(value: String) -> Label:
	var label := Label.new()
	label.text = value
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	label.custom_minimum_size.x = 300
	rows.add_child(label)
	return label

func button(id: String, value: String, callback: Callable) -> Button:
	var result := Button.new()
	result.text = value
	result.custom_minimum_size.y = 36
	result.pressed.connect(callback)
	rows.add_child(result)
	controls[id] = result
	return result

func toggle(id: String, value: String, initial: bool, callback: Callable) -> CheckButton:
	var result := CheckButton.new()
	result.text = value
	result.button_pressed = initial
	result.toggled.connect(callback)
	rows.add_child(result)
	controls[id] = result
	return result

func slider(id: String, caption: String, low: float, high: float, initial: float, step: float, callback: Callable) -> HSlider:
	text(caption)
	var result := HSlider.new()
	result.min_value = low
	result.max_value = high
	result.step = step
	result.value = initial
	result.custom_minimum_size = Vector2(280, 28)
	result.value_changed.connect(callback)
	rows.add_child(result)
	controls[id] = result
	return result

func box(parent: Node3D, id: String, at: Vector3, dimensions: Vector3, color: Color) -> MeshInstance3D:
	var result := MeshInstance3D.new()
	result.name = id
	var mesh := BoxMesh.new()
	mesh.size = dimensions
	result.mesh = mesh
	var material := StandardMaterial3D.new()
	material.albedo_color = color
	material.roughness = 0.85
	result.material_override = material
	parent.add_child(result)
	result.position = at
	return result

func shape(parent: CollisionObject3D, dimensions: Vector3) -> CollisionShape3D:
	var node := CollisionShape3D.new()
	var resource := BoxShape3D.new()
	resource.size = dimensions
	node.shape = resource
	parent.add_child(node)
	return node

func reset_lab() -> void:
	# Reload clears controls, timers and state together; persistent lab files are kept.
	get_tree().reload_current_scene()
