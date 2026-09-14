extends SceneTree
## Structure/behavior checks for the supplied B02 references, not learner grading.

var checks: int = 0
var failures: Array[String] = []

func _initialize() -> void:
	call_deferred("_run")

func _check(condition: bool, message: String) -> void:
	checks += 1
	if not condition:
		failures.append(message)
		push_error("B02 FAILED: " + message)

func _run() -> void:
	for filename in ["starter", "reference", "broken"]:
		var packed := load("res://lessons/b02/%s.tscn" % filename) as PackedScene
		_check(packed != null, filename + " loads")
		if packed == null:
			continue
		var scene := packed.instantiate()
		root.add_child(scene)
		await process_frame
		var module := scene.get_node("ModuleA") as StaticBody3D
		var visual := module.get_node("Visual") as MeshInstance3D
		var collision := module.get_node("CollisionShape3D") as CollisionShape3D
		_check(module.scene_file_path == "res://lessons/b02/module.tscn", "reuses a scene, not loose copied nodes")
		_check(module.scale.is_equal_approx(Vector3.ONE), "module has unit scale")
		_check(collision.shape != null and not collision.disabled, "preconfigured shape remains enabled")
		if filename == "broken":
			_check(not visual.global_position.is_equal_approx(collision.global_position), "fault actually separates visual and shape")
			visual.position = Vector3(0, 0.5, 0)
			_check(visual.global_position.is_equal_approx(collision.global_position), "minimal repair restores alignment")
		else:
			_check(visual.global_position.is_equal_approx(collision.global_position), "visual and shape are aligned")
		if filename == "reference":
			var other := scene.get_node("ModuleB") as StaticBody3D
			_check(other != module and other.scene_file_path == module.scene_file_path, "two independent scene instances")
			var old_visual: Vector3 = visual.global_position
			var old_shape: Vector3 = collision.global_position
			var old_other: Vector3 = other.global_position
			module.position.x += 1.0
			_check((visual.global_position - old_visual).is_equal_approx(Vector3.RIGHT), "root moves visual")
			_check((collision.global_position - old_shape).is_equal_approx(Vector3.RIGHT), "root moves shape")
			_check(other.global_position.is_equal_approx(old_other), "moving A does not move B")
			var shape_before := collision.shape
			var replacement := CylinderMesh.new()
			replacement.height = 1.0
			replacement.top_radius = 0.5
			replacement.bottom_radius = 0.5
			visual.mesh = replacement
			_check(collision.shape == shape_before and not collision.disabled, "appearance replacement retains function nodes")
			_check(module.get_node_or_null("Label") != null, "appearance replacement retains label")
		if filename == "starter":
			_check(scene.get_node_or_null("ModuleB") == null, "starter does not contain the completed task")
		scene.queue_free()
		await process_frame
	if failures.is_empty():
		print("B02 PASS: %d assertions" % checks)
		quit(0)
	else:
		print("B02 FAILED: %d of %d" % [failures.size(), checks])
		quit(1)
