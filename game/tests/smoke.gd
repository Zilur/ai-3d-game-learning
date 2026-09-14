extends SceneTree
## Run after --editor --import. No visual, human-learning or performance claims.

var failures: Array[String] = []
var checks: int = 0
var main_scene: PackedScene

func _initialize() -> void:
	call_deferred("_run")

func _check(condition: bool, message: String) -> void:
	checks += 1
	if not condition:
		failures.append(message)
		push_error("TEST FAILED: " + message)

func _physics_steps(count: int) -> void:
	for index in range(count):
		await physics_frame
	await process_frame

func _spawn_main(count: int = 10):
	var world = main_scene.instantiate()
	world.star_count = count
	world.get_node("Player").capture_mouse_on_start = false
	root.add_child(world)
	current_scene = world
	return world

func _release_inputs() -> void:
	for action in ["move_left", "move_right", "move_forward", "move_back", "sprint", "jump"]:
		Input.action_release(action)

func _discard_current() -> void:
	_release_inputs()
	if is_instance_valid(current_scene):
		var previous := current_scene
		current_scene = null
		previous.queue_free()
	await process_frame
	await process_frame

func _run() -> void:
	print("Godot version: ", Engine.get_version_info().get("string"))
	main_scene = load("res://scenes/main.tscn") as PackedScene
	_check(main_scene != null, "main scene loads")
	if main_scene == null:
		quit(1)
		return
	await _test_movement_and_collision()
	await _discard_current()
	await _test_collection_and_reset()
	await _discard_current()
	await _test_zero_and_one()
	await _test_labs()
	_release_inputs()
	if failures.is_empty():
		print("SMOKE PASS: %d assertions" % checks)
		quit(0)
	else:
		print("SMOKE FAILED: %d / %d assertions" % [failures.size(), checks])
		quit(1)

func _test_movement_and_collision() -> void:
	var world = _spawn_main()
	var player = world.get_node("Player")
	_check(player.collision_layer == 2 and player.collision_mask == 1, "player layer/mask")
	await _physics_steps(50)
	_check(player.is_on_floor(), "player settles on floor")
	_check(absf(player.global_position.y - 0.9) < 0.12, "capsule stands at correct height")
	var start: Vector3 = player.global_position
	Input.action_press("move_forward")
	await _physics_steps(30)
	Input.action_release("move_forward")
	var walk_distance: float = start.z - player.global_position.z
	_check(walk_distance > 1.8 and walk_distance < 2.3, "walking is approximately speed x time")
	player.respawn()
	await _physics_steps(10)
	start = player.global_position
	Input.action_press("move_forward")
	Input.action_press("move_right")
	await _physics_steps(30)
	_release_inputs()
	var diagonal_delta: Vector3 = player.global_position - start
	diagonal_delta.y = 0.0
	_check(absf(diagonal_delta.length() - walk_distance) < 0.25, "diagonal input is normalized")
	player.respawn()
	await _physics_steps(10)
	start = player.global_position
	Input.action_press("sprint")
	Input.action_press("move_forward")
	await _physics_steps(30)
	_release_inputs()
	_check(start.z - player.global_position.z > walk_distance * 1.5, "sprint is faster than walking")
	player.respawn()
	await _physics_steps(15)
	Input.action_press("jump")
	await _physics_steps(2)
	Input.action_release("jump")
	await _physics_steps(8)
	_check(player.global_position.y > 1.3 and not player.is_on_floor(), "jump leaves floor")
	var vertical_before: float = player.velocity.y
	Input.action_press("jump")
	await _physics_steps(2)
	Input.action_release("jump")
	_check(player.velocity.y <= vertical_before + 0.01, "airborne jump does not reset vertical speed")
	await _physics_steps(80)
	_check(player.is_on_floor(), "player lands after jump")
	player.global_position = Vector3(-5.5, 1.0, 3.0)
	player.velocity = Vector3.ZERO
	await _physics_steps(10)
	Input.action_press("move_left")
	await _physics_steps(40)
	_check(player.global_position.x > -6.5 and player.global_position.x < -6.2, "wall blocks player")
	world.get_node("Wall/Visual").visible = false
	await _physics_steps(15)
	_check(player.global_position.x > -6.5, "invisible wall still blocks")
	world.get_node("Wall/CollisionShape3D").set_deferred("disabled", true)
	await _physics_steps(15)
	Input.action_release("move_left")
	_check(player.global_position.x < -6.8, "disabled wall shape allows passage")
	player.global_position.y = -20.0
	await _physics_steps(3)
	_check(player.global_position.distance_to(player.spawn_position) < 0.3, "falling respawns player")

func _test_collection_and_reset() -> void:
	var world = _spawn_main()
	var player = world.get_node("Player")
	var star = world.get_node("Stars/Star00")
	_check(world.total_stars == 10 and world.collected_count == 0, "initial total and progress")
	_check(star.collision_layer == 0 and star.collision_mask == 2, "Area detects player layer")
	star.collision_mask = 1
	player.global_position = Vector3(0, 0.95, 1)
	await _physics_steps(8)
	_check(world.collected_count == 0, "wrong Area mask does not collect player")
	player.global_position = Vector3(0, 0.95, 5)
	await _physics_steps(4)
	star.collision_mask = 2
	player.global_position = Vector3(0, 0.95, 1)
	await _physics_steps(8)
	_check(world.collected_count == 1, "real Area overlap collects exactly one star")
	world._on_star_collected("Star00")
	_check(world.collected_count == 1, "level also rejects duplicate event IDs")
	var other := Node3D.new()
	root.add_child(other)
	var second = world.get_node("Stars/Star01")
	_check(not second.try_collect(other), "non-player cannot collect")
	_check(second.try_collect(player), "first valid request is accepted")
	_check(not second.try_collect(player), "second synchronous request is rejected")
	_check(world.collected_count == 2, "duplicate request does not duplicate reward")
	other.queue_free()
	for remaining in world.get_node("Stars").get_children():
		remaining.try_collect(player)
	_check(world.collected_count == 10 and world.completed, "all stars complete level")
	_check(world.get_node("HUD/Panel/VBox/Counter").text == "10 / 10", "HUD mirrors state")
	await process_frame
	await process_frame
	_check(world.get_node("Stars").get_child_count() == 0, "consumed objects are released")
	for iteration in range(3):
		var result := reload_current_scene()
		_check(result == OK, "restart request succeeds")
		await process_frame
		await process_frame
		await _physics_steps(3)
		var fresh = current_scene
		_check(fresh != null, "restart creates a current scene")
		if fresh != null:
			_check(fresh.collected_count == 0 and fresh.total_stars == 10 and not fresh.completed,
				"restart has clean progress")

func _test_zero_and_one() -> void:
	var empty = _spawn_main(0)
	_check(empty.total_stars == 0 and empty.completed, "empty test level has explicit completion state")
	await _discard_current()
	var one = _spawn_main(1)
	one.get_node("Stars/Star00").try_collect(one.get_node("Player"))
	_check(one.total_stars == 1 and one.collected_count == 1 and one.completed, "one-star level completes")
	await _discard_current()

func _test_labs() -> void:
	var packed := load("res://scenes/lab.tscn") as PackedScene
	_check(packed != null, "lab scene loads")
	if packed == null:
		return
	var lab = packed.instantiate()
	root.add_child(lab)
	current_scene = lab
	await process_frame
	lab._set_parent_yaw(90.0)
	lab._set_component(45.0, "rotation_degrees", 1)
	var subject = lab._subject
	var start: Vector3 = subject.global_position
	lab._move_world_x()
	_check((subject.global_position - start).is_equal_approx(Vector3.RIGHT), "World +X uses world axis")
	subject.global_position = start
	var parent_direction: Vector3 = lab._parent_space.global_basis.x
	lab._move_parent_x()
	_check((subject.global_position - start).is_equal_approx(parent_direction), "Parent +X follows parent axis")
	subject.global_position = start
	var object_direction: Vector3 = subject.global_basis.x.normalized()
	lab._move_object_x()
	_check((subject.global_position - start).is_equal_approx(object_direction), "Object +X follows object axis")
	_check(not parent_direction.is_equal_approx(object_direction), "test actually distinguishes axes")
	lab._switch_mode(1)
	var center_position: Vector3 = lab._door_board.global_position
	lab._set_side_pivot(true)
	_check(lab._door_board.global_position.is_equal_approx(center_position), "closed door stays in same place")
	var hinge_edge: Vector3 = lab._door_board.to_global(Vector3(-1, 0, 0))
	lab._set_door_angle(90.0)
	_check(lab._door_board.to_global(Vector3(-1, 0, 0)).is_equal_approx(hinge_edge), "hinge edge stays fixed")
	lab._switch_mode(2)
	lab._set_material_parameter(0.8, "roughness")
	lab._set_material_parameter(1.0, "metallic")
	lab._set_material_parameter(3.0, "emission_energy_multiplier")
	_check(is_equal_approx(lab._material.roughness, 0.8), "roughness control changes material")
	_check(is_equal_approx(lab._material.metallic, 1.0), "metallic control changes material")
	_check(is_equal_approx(lab._material.emission_energy_multiplier, 3.0), "emission control changes material")
	_check(not lab._neighbor_light.visible, "emission does not silently toggle separate light")
	_check(not lab._explanation.visible, "explanation is hidden before reveal")
	lab._switch_mode(0)
	_check(lab._subject.position.is_equal_approx(Vector3(0, 1, 0)), "reset restores initial transform")
	await _discard_current()
