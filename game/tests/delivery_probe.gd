extends Node
## Explicit opt-in release-package smoke check; only dedicated disposable test saves.
const ACTIONS := ["move_left", "move_right", "move_forward", "move_back", "sprint", "jump", "attack"]
var failures: Array[String] = []
var checks := 0
func check(ok: bool, detail: String) -> void:
	checks += 1
	if not ok:
		failures.append(detail)
		push_error("DELIVERY FAILED: " + detail)
func wait_frames(n: int = 12) -> void:
	for i in range(n): await get_tree().physics_frame
	await get_tree().process_frame
func clear_inputs() -> void:
	for action in ACTIONS:
		if InputMap.has_action(action): Input.action_release(action)
func walk_to(world: Node, target: Vector3) -> bool:
	for i in range(300):
		var delta: Vector3 = target - world.player.position
		delta.y = 0
		if delta.length() < 0.35:
			clear_inputs(); await wait_frames(3); return true
		var direction := delta.normalized()
		clear_inputs()
		Input.action_press("move_right", maxf(0, direction.x))
		Input.action_press("move_left", maxf(0, -direction.x))
		Input.action_press("move_back", maxf(0, direction.z))
		Input.action_press("move_forward", maxf(0, -direction.z))
		await get_tree().physics_frame
	clear_inputs()
	return false
func capture(name: String) -> void:
	if DisplayServer.get_name() == "headless": return
	for i in range(15): await get_tree().process_frame
	await RenderingServer.frame_post_draw
	var folder := OS.get_environment("DELIVERY_CAPTURE_DIR")
	if folder.is_empty(): return
	DirAccess.make_dir_recursive_absolute(folder)
	check(get_viewport().get_texture().get_image().save_png(folder.path_join(name + ".png")) == OK, "rendered " + name)
func run(mode: String) -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	await wait_frames()
	check(not OS.has_feature("editor"), "running actual export template, not the editor")
	var w = get_tree().current_scene
	check(w != null and w.is_in_group("production_world"), "package starts integrated world")
	if w == null or not w.is_in_group("production_world"):
		get_tree().quit(1); return
	var token := OS.get_environment("DELIVERY_CASE")
	if token.is_empty() or not token.is_valid_identifier():
		push_error("DELIVERY_CASE must be an anonymous identifier"); get_tree().quit(1); return
	w.store.file_path = "user://delivery_smoke_only/" + token + "/save.json"
	check(w.asset_instances.size() == 12, "12 production assets present in PCK")
	check(w.banner.get_theme_font("font").has_char(26143), "CJK glyph for star available")
	if mode == "read":
		check(w.load_game(), "read persisted file from separate process")
		check(w.completed and w.seen_ids.size() == 10 and w.gate_open and w.has_key, "restored completed route")
		check(not w.training_enabled and w.low_motion and is_equal_approx(w.volume, 0.25), "restored user settings")
	elif mode == "render":
		await capture("release-courtyard")
		w.volume = 0.25
		w.request_action("labs")
		check(w.guard.visible, "real confirmation visible")
		await capture("release-save-guard")
		w.cancel_action()
	else:
		var route := [Vector3(0,0,2),Vector3(-2,0,-3),Vector3(2,0,-8),Vector3(0,0,-12.5),Vector3(-1,0,-15),Vector3(-3,0,-19),Vector3(4,0,-22)]
		for point in route:check(await walk_to(w,point), "physical walk " + str(point))
		check(w.interact() and w.has_key, "key found by actual route")
		for point in [Vector3(3,0,-23),Vector3(0,0,-27),Vector3(0,0,-30.5)]:check(await walk_to(w,point), "forest " + str(point))
		check(w.interact() and w.gate_open, "key opens gate in range")
		for point in [Vector3(0,0,-34),Vector3(2,0,-39),Vector3(0,0,-44)]:check(await walk_to(w,point), "lookout " + str(point))
		check(w.completed and w.seen_ids.size()==10, "full release walkthrough without injected pickups")
		w.set_training(false); w.volume=0.25; w.low_motion=true
		check(w.save_game(), "release package writes save")
		w.open_labs(); await wait_frames()
		var hub = get_tree().current_scene
		check(hub.scene_file_path.contains("lab_hub"), "menu reaches packed lab hub")
		var paths: Array = hub.LABS.duplicate(true)
		for entry in paths:
			if entry[1] == "res://world/exploration.tscn":continue
			check(get_tree().change_scene_to_file(entry[1]) == OK, "open packed " + entry[1])
			await wait_frames()
			check(get_tree().current_scene.scene_file_path == entry[1], "instantiated " + entry[1])
		get_node("/root/StudySession").resume_world(); await wait_frames()
		w=get_tree().current_scene
		check(w.completed and w.seen_ids.size()==10, "release lab return preserves play")
		w.volume=0.4; w.request_action("quit")
		check(w.guard.visible, "dirty exit intercepted in release")
		w.cancel_action(); w.volume=0.25
	clear_inputs()
	if failures.is_empty():print("EXPORTED DELIVERY ",mode.to_upper()," PASS: ",checks," checks")
	get_tree().paused=false
	get_tree().quit(0 if failures.is_empty() else 1)
