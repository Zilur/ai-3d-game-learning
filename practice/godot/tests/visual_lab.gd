extends SceneTree
## Structural/behavior smoke for the visual A/B lab. This does not judge artistic quality.

var failures: Array[String] = []
var checks := 0

func _initialize() -> void:
	call_deferred("_run")

func _check(condition: bool, message: String) -> void:
	checks += 1
	if not condition:
		failures.append(message)
		push_error("VISUAL LAB TEST FAILED: " + message)

func _run() -> void:
	var packed := load("res://scenes/visual_lab.tscn") as PackedScene
	_check(packed != null, "visual lab scene loads")
	if packed == null:
		quit(1)
		return
	var lab = packed.instantiate()
	root.add_child(lab)
	current_scene = lab
	await process_frame

	var camera: Camera3D = lab.get_node("Camera3D")
	var sun: DirectionalLight3D = lab.get_node("Sun")
	var clutter: Node3D = lab.get_node("Clutter")
	var status: Label = lab.get_node("HUD/Panel/VBox/Status")
	_check(is_equal_approx(camera.fov, 50.0), "lab starts from documented FOV baseline")
	_check(not clutter.visible, "lab starts in clean comparison state")

	lab._set_fov(62.0)
	_check(is_equal_approx(camera.fov, 62.0), "FOV control changes the actual camera")
	lab._set_fov(100.0)
	_check(is_equal_approx(camera.fov, 70.0), "FOV method clamps extreme values")

	lab._set_light(1.7)
	_check(is_equal_approx(sun.light_energy, 1.7), "light control changes the actual key light")
	lab._set_clutter(true)
	_check(clutter.visible, "clutter toggle changes comparison geometry")
	_check("dense / noisy" in status.text, "status describes the active comparison")
	lab._set_clutter(false)
	_check(not clutter.visible and "clean / breathing space" in status.text, "clean baseline can be restored")

	lab.queue_free()
	await process_frame
	if failures.is_empty():
		print("VISUAL LAB PASS: %d assertions" % checks)
		quit(0)
	else:
		print("VISUAL LAB FAILED: %d / %d assertions" % [failures.size(), checks])
		quit(1)
