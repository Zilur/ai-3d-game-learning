extends CharacterBody3D
## B03/B05/B06. Units: metres, seconds, degrees in the Inspector.
@export_range(0.5, 12.0, 0.1) var walk_speed: float = 4.0
@export_range(0.5, 20.0, 0.1) var run_speed: float = 7.0
@export_range(1.0, 20.0, 0.1) var jump_speed: float = 6.0
@export_range(1.0, 40.0, 0.1) var gravity: float = 18.0
@export_range(0.01, 0.5, 0.01) var mouse_sensitivity: float = 0.12
@onready var pivot: Node3D = $CameraPivot
@onready var arm: SpringArm3D = $CameraPivot/SpringArm3D
var spawn_position: Vector3

func _ready() -> void:
    spawn_position = global_position
    add_to_group("player")
    # Kept here so the sample also runs when player.tscn is reused.
    # For a production game, move these actions to Project Settings > Input Map.
    var keys: Dictionary = {"left": KEY_A, "right": KEY_D, "forward": KEY_W,
        "back": KEY_S, "run": KEY_SHIFT, "jump": KEY_SPACE}
    for action: String in keys:
        if not InputMap.has_action(action):
            InputMap.add_action(action)
            var event := InputEventKey.new()
            event.physical_keycode = keys[action]
            InputMap.action_add_event(action, event)
    arm.add_excluded_object(get_rid())

func _unhandled_input(event: InputEvent) -> void:
    if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
        Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
    if event is InputEventKey and event.pressed and event.keycode == KEY_ESCAPE:
        Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
    if event is InputEventMouseMotion and Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
        pivot.rotate_y(deg_to_rad(-event.relative.x * mouse_sensitivity))
        arm.rotation.x = clampf(arm.rotation.x - deg_to_rad(event.relative.y * mouse_sensitivity),
            deg_to_rad(-65.0), deg_to_rad(25.0))

func _physics_process(delta: float) -> void:
    if not is_on_floor():
        velocity.y -= gravity * delta
    elif Input.is_action_just_pressed("jump"):
        velocity.y = jump_speed
    var input_axis := Input.get_vector("left", "right", "forward", "back")
    # Camera-relative horizontal movement, not camera pitch / flying movement.
    var direction := pivot.global_basis * Vector3(input_axis.x, 0.0, input_axis.y)
    direction.y = 0.0
    direction = direction.normalized() * input_axis.length()
    var speed: float = run_speed if Input.is_action_pressed("run") else walk_speed
    velocity.x = direction.x * speed
    velocity.z = direction.z * speed
    # velocity is m/s. move_and_slide already uses physics delta; do not multiply twice.
    move_and_slide()
    if global_position.y < -12.0:
        respawn()

func respawn() -> void:
    global_position = spawn_position
    velocity = Vector3.ZERO
