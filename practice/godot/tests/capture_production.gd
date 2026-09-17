extends SceneTree
func _initialize()->void: call_deferred("run")
func open_scene(path: String)->Node:
	paused=false
	if is_instance_valid(current_scene):
		current_scene.queue_free()
		await process_frame
	var s: PackedScene=load(path)
	var node:=s.instantiate()
	root.add_child(node)
	current_scene=node
	return node
func capture(name: String)->void:
	for i in range(20):await process_frame
	await RenderingServer.frame_post_draw
	var dest:=OS.get_environment("PRODUCTION_CAPTURE_DIR")
	if dest.is_empty():dest="/tmp/production-captures"
	DirAccess.make_dir_recursive_absolute(dest)
	var result:=root.get_texture().get_image().save_png(dest.path_join(name+".png"))
	print("CAPTURE ",name," ",result)
	if result != OK:push_error("Failed to write native capture");quit(1)
func run()->void:
	root.size=Vector2i(1280,720)
	print("ACTUAL RENDERER: ",RenderingServer.get_current_rendering_method()," | ",RenderingServer.get_video_adapter_name())
	var args:=OS.get_cmdline_user_args()
	if args.has("require-forward") and RenderingServer.get_current_rendering_method() != "forward_plus":
		push_error("Requested Forward+ verification fell back to another renderer")
		quit(1);return
	if args.has("effects-only"):
		var fx=await open_scene("res://labs/effects_lab.tscn")
		await capture("effects-baseline")
		fx.controls.fog.button_pressed=true
		await capture("effects-fog")
		fx.baseline();fx.controls.glow.button_pressed=true
		await capture("effects-glow")
		fx.baseline()
		if fx.dof_supported:fx.controls.dof.button_pressed=true
		await capture("effects-dof")
	else:
		var w=await open_scene("res://world/exploration.tscn")
		await capture("courtyard")
		w.player.position=Vector3(0,0.95,-21);w.player.velocity=Vector3.ZERO;w.camera_snap()
		await capture("forest")
		w.gate_open=true;w.has_key=true;w.apply_gate();w.player.position=Vector3(0,0.95,-40);w.camera_snap()
		await capture("lookout")
		w.pause_game(true)
		await capture("pause-menu")
		for name in ["navigation","shader","large_scene"]:
			var lab=await open_scene("res://labs/"+name+"_lab.tscn")
			if name=="shader":lab.controls.stripe.button_pressed=true;lab.controls.wind.value=0.2
			if name=="navigation":
				for i in range(8):await physics_frame
				lab.depart()
			await capture(name)
	quit()
