extends SceneTree
## Run AFTER import: godot --headless --path game --script res://tests/smoke.gd
var errors: int = 0

func _initialize() -> void:
    run_tests.call_deferred()

func check(ok: bool, message: String) -> void:
    if not ok:
        errors += 1
        push_error(message)

func run_tests() -> void:
    var packed := load("res://scenes/main.tscn") as PackedScene
    if packed == null:
        quit(1)
        return
    var level := packed.instantiate()
    root.add_child(level)
    current_scene = level
    await process_frame
    var player := level.get_node("Player") as CharacterBody3D
    for i in range(120):
        await physics_frame
    check(player.is_on_floor(), "Player should land on Ground")
    check(absf(player.global_position.y) < 0.2, "Feet should be near y=0")
    check(level.get("total") == 5, "Expected five collectibles")
    var star := level.get_node("Stars/Star1") as Area3D
    check(star.collision_mask == 2, "Area must scan Player layer")
    var outsider := Node3D.new()
    star.call("try_collect", outsider)
    check(level.get("collected_count") == 0, "Non-player body must not collect")
    outsider.free()
    # Actual overlap, not just calling the event handler directly.
    player.global_position = Vector3(0, 0.05, 1)
    player.velocity = Vector3.ZERO
    for i in range(5):
        await physics_frame
    check(level.get("collected_count") == 1, "Area overlap should increment once")
    var next_star := level.get_node("Stars/Star2")
    next_star.call("try_collect", player)
    next_star.call("try_collect", player)
    check(level.get("collected_count") == 2, "Duplicate callback must not double count")
    var before: Vector3 = player.global_position
    Input.action_press("back")
    for i in range(30):
        await physics_frame
    Input.action_release("back")
    check(player.global_position.z > before.z + 0.5, "Input must move player")
    print("SMOKE errors=", errors)
    quit(1 if errors > 0 else 0)
