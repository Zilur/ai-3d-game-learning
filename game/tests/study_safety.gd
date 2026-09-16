extends SceneTree
const STORE = preload("res://world/save_store.gd")
const CREATION = preload("res://world/creation_settings.gd")
var count := 0
var failures: Array[String] = []
class FailingStore extends "res://world/save_store.gd":
	func write_snapshot(_data: Dictionary) -> Dictionary:
		return invalid("构造磁盘写入失败")
func _initialize() -> void: call_deferred("run")
func check(value: bool, label: String) -> void:
	count += 1
	if not value:
		failures.append(label)
		push_error("STUDY SAFETY FAILED: " + label)
func settle() -> void:
	for i in range(12): await process_frame
func run() -> void:
	var session := root.get_node("StudySession")
	session.suspended.clear()
	change_scene_to_file("res://world/exploration.tscn")
	await settle()
	var w = current_scene
	w.store.file_path = "user://study_safety_only/snapshot.json"
	check(not auto_accept_quit, "window manager close intercepted")
	check(not w.has_unsaved_changes(), "fresh world is clean")
	check(w.get_node("StarLayout/courtyard_0") is Marker3D, "persistent layout marker")
	check(not w.get_node("StarLayout/LayoutPreview").visible, "editor guides hidden at runtime")
	check(w.collect_star("courtyard_0") and w.has_unsaved_changes(), "new progress makes dirty")
	w.request_action("labs")
	check(w.guard.visible and paused, "dirty lab transition asks")
	w.guard.canceled.emit()
	check(not paused and w.pending_action == "" and w.seen_ids.size() == 1, "cancel preserves unpaused game")
	var original_store = w.store
	var failing := FailingStore.new()
	failing.file_path = original_store.file_path
	w.store = failing
	w.request_action("quit")
	check(not w.resolve_action(true), "failed save blocks quit")
	check(current_scene == w and w.guard.visible and w.has_unsaved_changes(), "failed save stays dirty with dialog")
	w.cancel_action()
	w.store = original_store
	check(w.save_game() and not w.has_unsaved_changes(), "successful manual save establishes baseline")
	w.collect_star("courtyard_1")
	var primary := FileAccess.get_file_as_string(w.store.file_path)
	w.request_action("load")
	check(w.guard.ok_button_text.contains("保护"), "load offers separate rescue copy")
	check(w.resolve_action(true), "save rescue then load")
	check(w.seen_ids.size() == 1 and not w.has_unsaved_changes(), "requested old primary restored")
	check(FileAccess.get_file_as_string(w.store.file_path) == primary, "save-before-load did not overwrite target")
	var rescue := STORE.new()
	rescue.file_path = w.store.file_path + ".before-load"
	check(rescue.read_snapshot().data.collected.size() == 2, "preload progress is recoverable")
	w.request_action("recover")
	check(w.seen_ids.size() == 2 and w.has_unsaved_changes(), "recovered rescue stays unsaved relative to primary")
	w.request_action("labs")
	check(w.resolve_action(false), "enter without disk save retains in memory")
	await settle()
	check(current_scene.scene_file_path == "res://labs/lab_hub.tscn", "arrived in hub")
	check(session.has_unsaved() and session.suspended.data.collected.size() == 2, "handoff carries dirty progress")
	current_scene.open_lab("res://labs/collision_roles_lab.tscn")
	await settle()
	check(current_scene.scene_file_path.contains("collision_roles") and session.panel.visible, "lab has global return")
	session._notification(Node.NOTIFICATION_WM_CLOSE_REQUEST)
	check(session.pending_quit and session.leave_dialog.visible, "close in lab protects suspended game")
	session.leave_dialog.canceled.emit(); session.leave_dialog.hide()
	check(not session.pending_quit and session.has_unsaved(), "cancel lab quit retains handoff")
	session.resume_world()
	await settle()
	w = current_scene
	check(w.seen_ids.size() == 2 and w.has_unsaved_changes(), "return restores count and dirty baseline")
	check(session.suspended.is_empty(), "handoff consumed only after restore")
	check(w.player.position.distance_to(w.SPAWNS.courtyard) < 2, "return uses safe checkpoint")
	w.pause_game(true)
	w.request_action("new"); w.cancel_action()
	check(paused and w.pause_panel.visible, "cancel from menu restores menu")
	w.request_action("labs"); check(w.resolve_action(true), "saved transition succeeds")
	await settle()
	check(not session.has_unsaved(), "saved handoff clean")
	# Legacy scene also gets a return route; do not rely on F6/editor.
	change_scene_to_file("res://scenes/lab.tscn")
	await settle()
	check(session.resume_button.visible, "legacy reference supports resume")
	session.resume_world(); await settle(); w=current_scene
	check(not w.has_unsaved_changes() and w.seen_ids.size() == 2, "legacy roundtrip preserves saved progress")
	w.motion_toggle.button_pressed = not w.low_motion
	check(w.has_unsaved_changes(), "settings included in dirty tracking")
	session._notification(Node.NOTIFICATION_WM_CLOSE_REQUEST)
	check(w.pending_action == "quit" and w.guard.visible, "world titlebar routes through same guard")
	w.cancel_action()
	# Real ResourceSaver/load roundtrip, never mutate the reference creation file.
	var before := FileAccess.get_sha256("res://world/creation.tres")
	var design := CREATION.new()
	design.walk_speed=5.5; design.path_color=Color("b0ba88")
	check(design.problem().is_empty(), "legal creative parameters")
	check(ResourceSaver.save(design, "user://study_safety_only/design.tres") == OK, "creation resource written")
	var loaded = ResourceLoader.load("user://study_safety_only/design.tres", "", ResourceLoader.CACHE_MODE_IGNORE)
	check(is_equal_approx(loaded.walk_speed, 5.5) and loaded.path_color == design.path_color, "saved parameters reopen unchanged")
	loaded.run_speed=1
	check(not loaded.problem().is_empty(), "invalid run/walk relation rejected")
	check(FileAccess.get_sha256("res://world/creation.tres") == before, "reference design untouched")
	# Separate primary: missing-load must not destroy current state.
	w.store.file_path="user://study_safety_only/no-parent-yet/never-created.json"
	w.request_action("load")
	check(not w.resolve_action(true) and w.guard.visible and w.seen_ids.size()==2, "missing requested save stays put")
	w.cancel_action(); paused=false
	if failures.is_empty(): print("STUDY SAFETY PASS: ",count," assertions; constructed tests, not a child trial")
	quit(0 if failures.is_empty() else 1)
