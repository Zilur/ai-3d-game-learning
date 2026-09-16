extends Node3D
## Teaching lab for units/second speed and jump/gravity tuning.

var runner: MeshInstance3D
var jumper: MeshInstance3D
var status: Label
var speed_slider: HSlider
var jump_slider: HSlider
var gravity_slider: HSlider

var speed: float = 4.0
var jump_velocity: float = 7.0
var gravity: float = 20.0
var running: bool = false
var airborne: bool = false
var jump_vy: float = 0.0
const RUN_START := -4.0
const RUN_END := 4.0
const GROUND_Y := 0.42

func _ready() -> void:
	_build_world()
	_build_ui()
	_refresh()

func _physics_process(delta: float) -> void:
	if running:
		runner.position.x += speed * delta
		if runner.position.x >= RUN_END:
			runner.position.x = RUN_END
			running = false
	if airborne:
		jump_vy -= gravity * delta
		jumper.position.y += jump_vy * delta
		if jumper.position.y <= GROUND_Y:
			jumper.position.y = GROUND_Y
			jump_vy = 0.0
			airborne = false
	_refresh(delta)

func _build_world() -> void:
	var environment := WorldEnvironment.new()
	var env := Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color(0.72, 0.82, 0.84)
	environment.environment = env
	add_child(environment)

	var sun := DirectionalLight3D.new()
	sun.rotation_degrees = Vector3(-52, -35, 0)
	sun.light_energy = 1.15
	sun.shadow_enabled = true
	add_child(sun)

	var camera := Camera3D.new()
	camera.position = Vector3(0, 5.5, 10.5)
	add_child(camera)
	camera.look_at(Vector3(0, 0.7, 0))
	camera.current = true

	var track := MeshInstance3D.new()
	var track_mesh := BoxMesh.new()
	track_mesh.size = Vector3(9.5, 0.18, 1.8)
	track.mesh = track_mesh
	var track_mat := StandardMaterial3D.new()
	track_mat.albedo_color = Color(0.71, 0.60, 0.43)
	track_mat.roughness = 0.95
	track.material_override = track_mat
	track.position = Vector3(0, -0.09, -1.3)
	add_child(track)

	var jump_pad := MeshInstance3D.new()
	var pad_mesh := BoxMesh.new()
	pad_mesh.size = Vector3(3.0, 0.18, 2.2)
	jump_pad.mesh = pad_mesh
	var pad_mat := StandardMaterial3D.new()
	pad_mat.albedo_color = Color(0.45, 0.62, 0.39)
	pad_mat.roughness = 0.95
	jump_pad.material_override = pad_mat
	jump_pad.position = Vector3(2.5, -0.09, 1.7)
	add_child(jump_pad)

	runner = MeshInstance3D.new()
	runner.name = "Runner"
	var runner_mesh := SphereMesh.new()
	runner_mesh.radius = 0.38
	runner_mesh.height = 0.76
	runner.mesh = runner_mesh
	var runner_mat := StandardMaterial3D.new()
	runner_mat.albedo_color = Color(0.22, 0.64, 0.80)
	runner_mat.roughness = 0.72
	runner.material_override = runner_mat
	runner.position = Vector3(RUN_START, GROUND_Y, -1.3)
	add_child(runner)

	jumper = MeshInstance3D.new()
	jumper.name = "Jumper"
	var jumper_mesh := SphereMesh.new()
	jumper_mesh.radius = 0.42
	jumper_mesh.height = 0.84
	jumper.mesh = jumper_mesh
	var jumper_mat := StandardMaterial3D.new()
	jumper_mat.albedo_color = Color(0.94, 0.55, 0.18)
	jumper_mat.roughness = 0.76
	jumper.material_override = jumper_mat
	jumper.position = Vector3(2.5, GROUND_Y, 1.7)
	add_child(jumper)

func _build_ui() -> void:
	var layer := CanvasLayer.new()
	add_child(layer)
	var panel := PanelContainer.new()
	panel.position = Vector2(14, 14)
	layer.add_child(panel)
	var rows := VBoxContainer.new()
	panel.add_child(rows)

	var title := Label.new()
	title.text = "Motion lab: speed / jump / gravity"
	rows.add_child(title)
	status = Label.new()
	rows.add_child(status)

	speed_slider = _slider(rows, "Speed (units / second)", 1.0, 10.0, 0.5, speed, _set_speed)
	jump_slider = _slider(rows, "Jump velocity", 2.0, 12.0, 0.5, jump_velocity, _set_jump_velocity)
	gravity_slider = _slider(rows, "Gravity", 5.0, 35.0, 1.0, gravity, _set_gravity)

	var buttons := HBoxContainer.new()
	rows.add_child(buttons)
	var run_button := Button.new()
	run_button.text = "Run across track"
	run_button.pressed.connect(_start_run)
	buttons.add_child(run_button)
	var jump_button := Button.new()
	jump_button.text = "Jump"
	jump_button.pressed.connect(_jump)
	buttons.add_child(jump_button)
	var reset_button := Button.new()
	reset_button.text = "Reset"
	reset_button.pressed.connect(_reset_lab)
	buttons.add_child(reset_button)

	var note := Label.new()
	note.text = "Speed is distance per second; physics uses speed * delta each frame.\nChange one slider at a time, predict first, then compare."
	rows.add_child(note)

func _slider(parent: VBoxContainer, label_text: String, low: float, high: float, step: float, initial: float, callback: Callable) -> HSlider:
	var label := Label.new()
	label.text = label_text
	parent.add_child(label)
	var slider := HSlider.new()
	slider.min_value = low
	slider.max_value = high
	slider.step = step
	slider.value = initial
	slider.custom_minimum_size = Vector2(430, 28)
	slider.value_changed.connect(callback)
	parent.add_child(slider)
	return slider

func _set_speed(value: float) -> void:
	speed = clampf(value, 1.0, 10.0)
	_refresh()

func _set_jump_velocity(value: float) -> void:
	jump_velocity = clampf(value, 2.0, 12.0)
	_refresh()

func _set_gravity(value: float) -> void:
	gravity = clampf(value, 5.0, 35.0)
	_refresh()

func _start_run() -> void:
	runner.position.x = RUN_START
	running = true

func _jump() -> void:
	if not airborne:
		jump_vy = jump_velocity
		airborne = true

func _reset_lab() -> void:
	running = false
	airborne = false
	jump_vy = 0.0
	runner.position = Vector3(RUN_START, GROUND_Y, -1.3)
	jumper.position = Vector3(2.5, GROUND_Y, 1.7)
	_refresh()

func _refresh(delta: float = 1.0 / 60.0) -> void:
	if not is_instance_valid(status):
		return
	status.text = "speed %.1f u/s | this physics-step displacement ≈ %.3f | jump %.1f | gravity %.1f | jumper y %.2f" % [
		speed, speed * delta, jump_velocity, gravity, jumper.position.y if is_instance_valid(jumper) else GROUND_Y
	]
