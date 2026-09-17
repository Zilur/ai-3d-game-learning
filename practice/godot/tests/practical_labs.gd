extends SceneTree
## Real engine assertions. No grading, classroom, commercial-art or GPU-speed claims.
var failures: Array[String] = []
var checks := 0

func _initialize() -> void:
	call_deferred("run")

func check(ok: bool, detail: String) -> void:
	checks += 1
	if not ok:
		failures.append(detail)
		push_error("PRACTICAL LAB FAILED: " + detail)

func steps(count: int) -> void:
	for i in range(count):
		await physics_frame
	await process_frame

func open_scene(path: String) -> Node:
	if is_instance_valid(current_scene):
		var old := current_scene
		current_scene = null
		old.queue_free()
	await process_frame
	await process_frame
	var scene: PackedScene = load(path)
	check(scene != null, "load " + path)
	var lab := scene.instantiate()
	root.add_child(lab)
	current_scene = lab
	await steps(5)
	return lab

func run() -> void:
	print("Practical suite: ", Engine.get_version_info().get("string"))
	var hub = await open_scene("res://labs/lab_hub.tscn")
	check(hub.LABS.size() == 17, "hub exposes all intended ready scenes")
	var lab = await open_scene("res://labs/camera_lab.tscn")
	check(lab.camera.projection == Camera3D.PROJECTION_PERSPECTIVE, "perspective default")
	lab.controls["projection"].button_pressed = true
	check(lab.camera.projection == Camera3D.PROJECTION_ORTHOGONAL, "UI changes real projection")
	check(not lab.fov_control.editable and lab.size_control.editable, "only active projection control enabled")
	lab.controls["size"].value = 16
	check(is_equal_approx(lab.camera.size, 16), "size control is wired")
	var before: Vector2 = lab.camera.unproject_position(lab.actor.global_position)
	lab.controls["right"].pressed.emit()
	var after: Vector2 = lab.camera.unproject_position(lab.actor.global_position)
	check(after.x > before.x, "camera-relative right moves screen-right")
	lab.controls["relative"].button_pressed = false
	check(lab.movement(Vector2.RIGHT).is_equal_approx(Vector3.RIGHT), "world direction contrasted")
	lab.controls["reset"].pressed.emit()
	await steps(6)
	lab = current_scene
	check(not lab.orthographic and lab.controls["fov"].value == 50, "reset projection and controls together")
	check(lab.actor.position.is_equal_approx(Vector3(3, 0.35, 0)), "reset actor and input mode")

	lab = await open_scene("res://labs/material_lab.tscn")
	check(lab.left.material_override != lab.right.material_override, "independent material default")
	lab.controls["roughness"].value = 0.85
	check(is_equal_approx(lab.reference.roughness, 0.4), "independent right reference unaffected")
	lab.controls["shared"].button_pressed = true
	check(lab.left.material_override == lab.right.material_override, "real shared reference")
	check(is_equal_approx(lab.right.material_override.roughness, 0.85), "right sees previous left material")
	lab.controls["roughness"].value = 0.2
	check(is_equal_approx(lab.right.material_override.roughness, 0.2), "shared edit changes both")
	lab.controls["shared"].button_pressed = false
	check(is_equal_approx(lab.right.material_override.roughness, 0.4), "unshare restores original reference")
	lab.controls["emission"].value = 3
	check(not lab.point_light.visible, "emission does not enable light")
	lab.controls["light"].button_pressed = true
	check(lab.point_light.visible, "actual light separately controlled")
	lab.controls["reset"].pressed.emit()
	await steps(6)
	lab = current_scene
	check(not lab.shared and not lab.point_light.visible and is_equal_approx(lab.material.roughness, 0.4), "material full reset")

	lab = await open_scene("res://labs/collision_roles_lab.tscn")
	check(not lab.decoration_overlap, "non-player initially excluded")
	lab.switches["decor_mask"].button_pressed = true
	lab._replay_decoration()
	await steps(45)
	check(lab.decoration_overlap, "mask now actually detects layer-3 body")
	lab.switches["decor_mask"].button_pressed = false
	lab._set_collision_enabled(false)
	lab._set_target_x(2.2)
	await steps(120)
	check(lab.trigger_overlap and not lab.decoration_overlap, "same area detects player only")
	lab.switches["player_mask"].button_pressed = false
	await steps(5)
	check(not lab.trigger_overlap, "disabling player mask clears detection")
	lab.switches["visual"].button_pressed = false
	lab._reset_lab()
	await steps(5)
	check(lab.switches["visual"].button_pressed and lab.switches["collision"].button_pressed, "reset checkboxes match world")
	check(lab.trigger.collision_mask == 2 and lab.switches["player_mask"].button_pressed, "reset mask and control")
	lab = await open_scene("res://labs/motion_lab.tscn")
	lab.speed_slider.value = 9
	lab.gravity_slider.value = 30
	lab._replay_lab()
	check(lab.speed == 9 and lab.gravity == 30, "replay keeps settings")
	lab._reset_lab()
	check(lab.speed == 4 and lab.gravity == 20 and lab.jump_velocity == 7, "reset restores all values")
	check(lab.speed_slider.value == 4 and lab.gravity_slider.value == 20, "reset sliders agree")

	lab = await open_scene("res://labs/event_lab.tscn")
	lab.controls["wrong"].pressed.emit()
	check(lab.count == 0 and lab.token.visible, "wrong actor rejected")
	lab.controls["double"].pressed.emit()
	check(lab.count == 1 and lab.taken and not lab.token.visible, "duplicate requests only one reward")
	lab.controls["feedback"].button_pressed = false
	check(lab.count == 1 and not lab.feedback.visible, "feedback separate from truth")
	lab.controls["guard"].button_pressed = false
	lab.controls["collect"].pressed.emit()
	check(lab.count == 2, "deliberate missing-state-guard fault reproduces")
	lab.controls["restart"].pressed.emit()
	check(lab.count == 0 and lab.token.visible and not lab.guard_enabled, "round restart keeps experiment setting")
	lab.controls["reset"].pressed.emit()
	await steps(6)
	lab = current_scene
	check(lab.guard_enabled and lab.count == 0 and lab.controls["guard"].button_pressed, "full reset clears fault setting")

	lab = await open_scene("res://labs/interaction_lab.tscn")
	# Test runner uses isolated XDG_DATA_HOME; nevertheless preserve any existing teaching file.
	var had_file := FileAccess.file_exists(lab.SAVE_PATH)
	var old_bytes := FileAccess.get_file_as_bytes(lab.SAVE_PATH) if had_file else PackedByteArray()
	lab.try_open()
	check(not lab.opened and not lab.nearby(), "cannot interact outside Area")
	lab.controls["position"].value = 0.3
	await steps(100)
	check(lab.nearby(), "real overlap establishes nearby")
	lab.try_open()
	check(not lab.opened, "detection is not permission")
	lab.controls["key"].button_pressed = true
	lab.controls["open"].pressed.emit()
	await steps(4)
	check(lab.opened and lab.door_shape.disabled, "valid action changes door and collision")
	lab.try_open()
	check(lab.opened, "repeat interaction stable")
	lab.controls["volume"].value = 0.4
	check(lab.save_state(), "real file save succeeds")
	lab.opened = false
	lab.has_key = false
	lab.volume = 0.1
	lab.apply_door()
	var position: Vector3 = lab.actor.position
	check(lab.load_state(), "real file parses")
	check(lab.opened and lab.has_key and is_equal_approx(lab.volume, 0.4), "persistent and preference state restored")
	check(lab.actor.position == position, "temporary actor position not loaded")
	lab.write_fixture("broken")
	check(not lab.load_state() and lab.opened, "corrupt file rejected without mutation")
	lab.write_fixture("missing")
	check(not lab.load_state() and lab.opened, "missing file leaves world usable")
	lab.write_fixture("old")
	check(lab.load_state() and is_equal_approx(lab.volume, 0.7), "known old version explicitly migrated")
	check(not lab.valid_data({"version":1,"progress":{"key":true,"door":true},"preferences":{"volume":2}}), "out-of-range values rejected")
	check(not lab.valid_data({"version":999}), "unknown version rejected")
	if had_file:
		var restore := FileAccess.open(lab.SAVE_PATH, FileAccess.WRITE)
		restore.store_buffer(old_bytes)
		restore.close()
	else:
		DirAccess.remove_absolute(lab.SAVE_PATH)


	check(not lab.valid_data({"version": true, "progress": {"key": true, "door": true}, "preferences": {"volume": 0.7}}), "boolean version is invalid")
	check(not lab.valid_data({"version": 1, "progress": {"key": true, "door": true}, "preferences": {"volume": 2}}), "out-of-range preference is invalid")
	lab = await open_scene("res://labs/platform_lab.tscn")
	await steps(30)
	var relative_before: float = lab.rider.position.x - lab.platform.position.x
	var rider_before: float = lab.rider.position.x
	await steps(35)
	check(lab.rider.is_on_floor(), "rider makes real platform contact")
	check(absf(lab.rider.position.x - lab.platform.position.x - relative_before) < 0.15 and absf(lab.rider.position.x - rider_before) > 0.4, "rider carried without parenting")
	check(lab.rider.get_parent() != lab.platform, "not a parenting illusion")
	lab.controls["jump"].pressed.emit()
	await steps(10)
	check(not lab.rider.is_on_floor(), "jump leaves platform")
	lab.controls["back"].pressed.emit()
	await steps(30)
	check(lab.rider.is_on_floor(), "can return and land")

	lab = await open_scene("res://labs/animation_lab.tscn")
	check(lab.skeleton != null and lab.skeleton.get_bone_count() >= 5, "real imported skeleton")
	check(lab.library_names.size() == 3 and lab.tree.active, "three imported clips linked to AnimationTree")
	var bone: int = lab.skeleton.find_bone("Arm_R")
	var before_pose: Quaternion = lab.skeleton.get_bone_pose_rotation(bone)
	lab.controls["blend"].value = 1
	await steps(22)
	check(lab.blend > 0.9, "blend transition reaches requested parameter")
	check(not lab.skeleton.get_bone_pose_rotation(bone).is_equal_approx(before_pose), "actual bone pose changes")
	check(lab.model.position == Vector3.ZERO, "animation playback does not silently move actor")
	lab.controls["attack"].pressed.emit()
	lab.controls["attack"].pressed.emit()
	await steps(40)
	check(lab.hits == 1, "one hit within active window, repeated request rejected")
	lab.controls["interrupt"].pressed.emit()
	check(lab.strike_time < 0, "interrupt restores control state")
	lab.controls["range"].button_pressed = false
	lab.attack_once()
	await steps(70)
	check(lab.hits == 1 and lab.strike_time < 0, "miss adds no hit and returns to locomotion")

	# The packaged Blender roundtrip must contain a real skin and three playable clips.
	var packed_roundtrip := load("res://assets/practice_robot_roundtrip.glb") as PackedScene
	check(packed_roundtrip != null, "actual Blender GLB imports")
	var roundtrip := packed_roundtrip.instantiate()
	root.add_child(roundtrip)
	var bones = lab.find_type(roundtrip, "Skeleton3D")
	var animation = lab.find_type(roundtrip, "AnimationPlayer")
	check(bones != null and bones.get_bone_count() >= 5, "Blender roundtrip preserves skeleton")
	check(animation != null and animation.get_animation_list().size() >= 3, "Blender roundtrip preserves clips")
	var round_names: Array[String] = []
	for clip in animation.get_animation_list():
		round_names.append(str(clip))
	check(round_names.any(func(n): return n.ends_with("Walk")), "roundtrip Walk can be selected")
	var motion_clip: String = round_names.filter(func(n): return n.ends_with("Walk"))[0]
	animation.play(motion_clip)
	animation.seek(0.2, true)
	await steps(3)
	check(not bones.get_bone_pose_rotation(2).is_equal_approx(Quaternion.IDENTITY), "roundtrip clip really changes pose")
	roundtrip.queue_free()

	if is_instance_valid(current_scene):
		current_scene.queue_free()
		current_scene = null
	await process_frame
	if failures.is_empty():
		print("PRACTICAL LAB PASS: %d assertions; engine behavior only" % checks)
		quit(0)
	else:
		print("PRACTICAL LAB FAIL: %d / %d" % [failures.size(), checks])
		quit(1)
