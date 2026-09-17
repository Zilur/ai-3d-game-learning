extends SceneTree
## Render-only audit capture; use a real graphics driver (e.g. xvfb), not --headless.
func _initialize() -> void:
	call_deferred("run")
func run() -> void:
	var directory := OS.get_environment("LAB_CAPTURE_DIR")
	if directory.is_empty():
		push_error("LAB_CAPTURE_DIR must be an explicit audit destination")
		quit(1)
		return
	DirAccess.make_dir_recursive_absolute(directory)
	root.size = Vector2i(1280, 720)
	for path in ["res://labs/lab_hub.tscn", "res://labs/camera_lab.tscn", "res://labs/material_lab.tscn", "res://labs/event_lab.tscn", "res://labs/interaction_lab.tscn", "res://labs/platform_lab.tscn", "res://labs/animation_lab.tscn", "res://labs/collision_roles_lab.tscn", "res://labs/motion_lab.tscn"]:
		change_scene_to_file(path)
		for i in range(12): await process_frame
		await RenderingServer.frame_post_draw
		var image := root.get_texture().get_image()
		image.save_png(directory.path_join(path.get_file().get_basename() + ".png"))
	print("LAB CAPTURE: representative rendered frames, not human classroom evidence")
	quit()
