extends SceneTree
## Behavior checks for small concept labs. These do not judge visual quality or learner mastery.

var failures: Array[String] = []
var checks := 0

func _initialize() -> void:
	call_deferred("_run")

func _check(condition: bool, message: String) -> void:
	checks += 1
	if not condition:
		failures.append(message)
		push_error("CONCEPT LAB TEST FAILED: " + message)

func _physics_steps(count: int) -> void:
	for _i in range(count):
		await physics_frame
	await process_frame

func _discard() -> void:
	if is_instance_valid(current_scene):
		var old := current_scene
		current_scene = null
		old.queue_free()
	await process_frame
	await process_frame

func _run() -> void:
	await _test_collision_roles()
	await _discard()
	await _test_motion()
	await _discard()
	if failures.is_empty():
		print("CONCEPT LAB PASS: %d assertions" % checks)
		quit(0)
	else:
		print("CONCEPT LAB FAILED: %d / %d assertions" % [failures.size(), checks])
		quit(1)

func _test_collision_roles() -> void:
	var packed := load("res://labs/collision_roles_lab.tscn") as PackedScene
	_check(packed != null, "collision roles lab loads")
	if packed == null:
		return
	var lab = packed.instantiate()
	root.add_child(lab)
	current_scene = lab
	await _physics_steps(3)
	_check(lab.wall_visual.visible, "wall starts visible")
	_check(not lab.wall_shape.disabled, "wall starts blocking")
	_check(lab.trigger.monitoring, "trigger starts monitoring")

	lab._set_target_x(3.0)
	await _physics_steps(90)
	_check(lab.probe.position.x < -0.45, "blocking collision stops probe before wall")
	lab._set_visual_enabled(false)
	_check(not lab.wall_visual.visible and not lab.wall_shape.disabled, "invisible wall can still block")

	lab._set_collision_enabled(false)
	await _physics_steps(3)
	lab._set_target_x(2.2)
	await _physics_steps(100)
	_check(lab.probe.position.x > 1.7, "disabled collision lets probe cross wall")
	_check(lab.trigger_overlap, "probe can enter trigger after crossing wall")

	lab._set_trigger_enabled(false)
	await _physics_steps(3)
	_check(not lab.trigger.monitoring and not lab.trigger_overlap, "trigger detection can be disabled separately")
	lab._reset_lab()
	await _physics_steps(3)
	_check(absf(lab.probe.position.x + 3.0) < 0.05, "collision lab reset restores start")
	_check(lab.wall_visual.visible and not lab.wall_shape.disabled and lab.trigger.monitoring,
		"collision lab reset restores all three roles")

func _test_motion() -> void:
	var packed := load("res://labs/motion_lab.tscn") as PackedScene
	_check(packed != null, "motion lab loads")
	if packed == null:
		return
	var lab = packed.instantiate()
	root.add_child(lab)
	current_scene = lab
	await _physics_steps(3)
	lab._set_speed(6.0)
	_check(is_equal_approx(lab.speed, 6.0), "speed slider changes units-per-second parameter")
	lab._start_run()
	await _physics_steps(30)
	var moved := lab.runner.position.x - lab.RUN_START
	_check(moved > 2.7 and moved < 3.3, "runner moves approximately speed x half-second")

	lab._set_jump_velocity(8.0)
	lab._set_gravity(20.0)
	lab._jump()
	await _physics_steps(12)
	_check(lab.jumper.position.y > lab.GROUND_Y + 0.6, "jump velocity lifts jumper")
	await _physics_steps(80)
	_check(absf(lab.jumper.position.y - lab.GROUND_Y) < 0.02 and not lab.airborne,
		"gravity returns jumper to ground")
	lab._reset_lab()
	_check(absf(lab.runner.position.x - lab.RUN_START) < 0.01, "motion lab reset restores runner")
