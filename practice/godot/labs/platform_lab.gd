extends "res://labs/lab_shell.gd"
## Real AnimatableBody3D + CharacterBody3D contact, not a parented fake rider.
var platform: AnimatableBody3D
var rider: CharacterBody3D
var phase := 0.0
var moving := true
var ride_enabled := true
var direction := 0.0

func _ready() -> void:
	setup("C06｜站上移动平台", "观察角色是否被平台带走，再试离开、跳起和恢复。角色不是平台的子节点。")
	platform = AnimatableBody3D.new()
	platform.name = "MovingPlatform"
	platform.collision_layer = 1
	platform.sync_to_physics = false
	stage.add_child(platform)
	platform.position = Vector3(0, 0.6, 0)
	shape(platform, Vector3(3, 0.3, 2.4))
	box(platform, "Visual", Vector3.ZERO, Vector3(3, 0.3, 2.4), Color("bb9361"))
	var floor_body := StaticBody3D.new()
	stage.add_child(floor_body)
	floor_body.position.y = -0.1
	shape(floor_body, Vector3(13, 0.2, 9))
	rider = CharacterBody3D.new()
	rider.name = "Rider"
	stage.add_child(rider)
	rider.position = Vector3(0, 1.8, 0)
	shape(rider, Vector3(0.6, 0.9, 0.6))
	box(rider, "Visual", Vector3.ZERO, Vector3(0.6, 0.9, 0.6), Color("e3bd48"))
	toggle("moving", "平台移动", true, func(v): moving = v)
	toggle("ride", "接受平台速度", true, func(v): ride_enabled = v; rider.platform_floor_layers = 1 if v else 0)
	slider("direction", "角色自身横向速度（0是站着）", -3, 3, 0, 0.5, func(v): direction = v)
	button("jump", "落地时跳起", jump)
	button("back", "回到平台上方（保留设置）", func(): rider.position = platform.position + Vector3(0, 1.2, 0); rider.velocity = Vector3.ZERO)
	text("支持平移平台的接触与离开对照；复杂挤压、旋转平台、多平台和你的正式控制器仍需另测。")

func _physics_process(delta: float) -> void:
	if not is_instance_valid(rider):
		return
	if moving:
		phase += delta
		platform.position.x = sin(phase) * 2.5
	rider.velocity.x = direction
	rider.velocity.z = 0
	if not rider.is_on_floor():
		rider.velocity.y -= 18 * delta
	elif rider.velocity.y < 0:
		rider.velocity.y = 0
	rider.move_and_slide()
	if absf(rider.position.x) > 6 or rider.position.y < -4:
		rider.position = platform.position + Vector3(0, 1.3, 0)
		rider.velocity = Vector3.ZERO
	status.text = "平台X %.2f | 角色X %.2f\n落地 %s | 平台速度 %s" % [platform.position.x, rider.position.x, str(rider.is_on_floor()), rider.get_platform_velocity()]

func jump() -> void:
	if rider.is_on_floor():
		rider.velocity.y = 6
