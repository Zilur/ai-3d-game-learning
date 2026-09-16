extends "res://labs/lab_shell.gd"
## Teaching lab for units/second speed and jump/gravity tuning.

var runner: MeshInstance3D
var jumper: MeshInstance3D
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

	camera = Camera3D.new()
	camera.position = Vector3(0, 5.5, 10.5)
	add_child(camera)
	camera.fov = 52
	camera.look_at(Vector3(-2, 0.7, 0))
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
	setup_ui("A05 / A06｜速度与跳跃", "先改一个参数，预测同样时间走多远、跳多高，再重播对比。这是简化运动模型。")
	speed_slider = slider("speed", "速度（单位/秒）", 1, 10, speed, 0.5, _set_speed)
	jump_slider = slider("jump", "起跳速度", 2, 12, jump_velocity, 0.5, _set_jump_velocity)
	gravity_slider = slider("gravity", "重力", 5, 35, gravity, 1, _set_gravity)
	button("run", "跑过同一段路", _start_run)
	button("jump_now", "跳跃（空中不能再次起跳）", _jump)
	button("replay", "仅回到起点，保留参数", _replay_lab)
	text("上方“恢复全部初值”也恢复三个参数。要验证真实角色落地、墙边与不同帧率，请再到主游戏试，不把小球模型当完整控制器。")

func reset_lab() -> void:
	_reset_lab()

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

func _replay_lab() -> void:
	running = false
	airborne = false
	jump_vy = 0.0
	runner.position = Vector3(RUN_START, GROUND_Y, -1.3)
	jumper.position = Vector3(2.5, GROUND_Y, 1.7)
	_refresh()

func _refresh(delta: float = 1.0 / 60.0) -> void:
	if not is_instance_valid(status):
		return
	status.text = "速度 %.1f 单位/秒\n本物理步位移约 %.3f\n起跳 %.1f | 重力 %.1f\n当前高度 %.2f" % [
		speed, speed * delta, jump_velocity, gravity, jumper.position.y if is_instance_valid(jumper) else GROUND_Y]

func _reset_lab() -> void:
	speed = 4.0
	jump_velocity = 7.0
	gravity = 20.0
	speed_slider.set_value_no_signal(speed)
	jump_slider.set_value_no_signal(jump_velocity)
	gravity_slider.set_value_no_signal(gravity)
	_replay_lab()
