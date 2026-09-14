extends CharacterBody3D
## C08/C09/C10: velocity is units/second; learners judge motion and camera behavior.

@export_range(0.1, 20.0, 0.1) var walk_speed: float = 4.0
@export_range(0.1, 30.0, 0.1) var run_speed: float = 7.0
@export_range(0.1, 30.0, 0.1) var jump_velocity: float = 8.0
@export_range(0.1, 80.0, 0.1) var gravity: float = 24.0
@export_range(0.0001, 0.02, 0.0001) var mouse_sensitivity: float = 0.002
@export var capture_mouse_on_start: bool = true

@onready var orbit: Node3D = $Orbit
@onready var arm: SpringArm3D = $Orbit/SpringArm3D
@onready var visual: Node3D = $Visual
var spawn_position: Vector3

func _enter_tree() -> void:
	# Preserve actions the learner has configured in Project Settings.
	var bindings := {
		"move_left": KEY_A, "move_right": KEY_D,
		"move_forward": KEY_W, "move_back": KEY_S,
		"sprint": KEY_SHIFT, "jump": KEY_SPACE
	}
	for action in bindings:
		if not InputMap.has_action(action):
			InputMap.add_action(action)
			var key := InputEventKey.new()
			key.physical_keycode = bindings[action]
			InputMap.action_add_event(action, key)

func _ready() -> void:
	add_to_group("player")
	spawn_position = global_position
	arm.add_excluded_object(get_rid())
	if capture_mouse_on_start and DisplayServer.get_name() != "headless":
		Input.mouse_mode = Input.MOUSE_MODE_CAPTURED

func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	elif event is InputEventMouseButton:
		if event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
			Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
	elif event is InputEventMouseMotion and Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
		orbit.rotate_y(-event.relative.x * mouse_sensitivity)
		arm.rotation.x = clampf(
			arm.rotation.x - event.relative.y * mouse_sensitivity,
			deg_to_rad(-65.0), deg_to_rad(35.0)
		)

func _physics_process(delta: float) -> void:
	var axes := Input.get_vector("move_left", "move_right", "move_forward", "move_back")
	# Only yaw affects movement: looking up must not make the player fly.
	var direction := orbit.global_basis * Vector3(axes.x, 0.0, axes.y)
	direction.y = 0.0
	direction = direction.limit_length(1.0)
	var speed := run_speed if Input.is_action_pressed("sprint") else walk_speed
	velocity.x = direction.x * speed
	velocity.z = direction.z * speed
	if not is_on_floor():
		velocity.y -= gravity * delta
	elif velocity.y < 0.0:
		velocity.y = 0.0
	if Input.is_action_just_pressed("jump") and is_on_floor():
		velocity.y = jump_velocity
	if direction.length_squared() > 0.001:
		visual.rotation.y = atan2(-direction.x, -direction.z)
	# Godot 4 handles the physics timestep inside this method.
	move_and_slide()
	if global_position.y < -12.0:
		respawn()

func respawn() -> void:
	global_position = spawn_position
	velocity = Vector3.ZERO

func _notification(what: int) -> void:
	if what == NOTIFICATION_APPLICATION_FOCUS_OUT:
		Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
		for action in ["move_left", "move_right", "move_forward", "move_back", "sprint", "jump"]:
			if InputMap.has_action(action):
				Input.action_release(action)
