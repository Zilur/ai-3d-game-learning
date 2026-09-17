extends SceneTree
var checks := 0
var failures: Array[String] = []
const STORE = preload("res://world/save_store.gd")
const ACTIONS = ["move_left","move_right","move_forward","move_back","sprint","jump","attack"]
func _initialize()->void:call_deferred("run")
func check(ok: bool, detail: String)->void:
	checks+=1
	if not ok:
		failures.append(detail)
		push_error("PRODUCTION CHECK FAILED: "+detail)
func steps(n: int)->void:
	for i in range(n):await physics_frame
	await process_frame
func clear_inputs()->void:
	for a in ACTIONS:
		if InputMap.has_action(a):Input.action_release(a)
func open_scene(path: String)->Node:
	paused=false
	clear_inputs()
	if is_instance_valid(current_scene):
		var old:=current_scene
		current_scene=null
		old.queue_free()
		await process_frame
		await process_frame
	var scene: PackedScene=load(path)
	check(scene!=null,"load "+path)
	var node:=scene.instantiate()
	root.add_child(node)
	current_scene=node
	await steps(8)
	return node
func walk_to(w: Node, to: Vector3, limit: int=260)->bool:
	for i in range(limit):
		var delta: Vector3=to-w.player.position
		delta.y=0
		if delta.length()<0.35:
			clear_inputs()
			await steps(3)
			return true
		var dir:=delta.normalized()
		clear_inputs()
		Input.action_press("move_right",maxf(0,dir.x))
		Input.action_press("move_left",maxf(0,-dir.x))
		Input.action_press("move_back",maxf(0,dir.z))
		Input.action_press("move_forward",maxf(0,-dir.z))
		await physics_frame
	clear_inputs()
	print("Walk stopped at ",w.player.position," target ",to)
	return false
func fixture()->Dictionary:
	return {"version":2,"collected":["courtyard_0"],"checkpoint":"forest","has_key":true,"gate_open":false,"training_enabled":true,"training_hits":2,"low_motion":true,"volume":0.5}
func run()->void:
	var lab=await open_scene("res://labs/navigation_lab.tscn")
	check(lab.region.navigation_mesh.get_polygon_count()>0,"nav polygons actually exist")
	lab.controls.query.pressed.emit()
	check(lab.route_reaches_goal,"small agent route reaches goal")
	await steps(210)
	check(lab.reached,"small body passes physical door")
	lab.controls.body_radius.value=0.8
	lab.depart()
	await steps(210)
	check(lab.route_reaches_goal and not lab.reached,"path/physical clearance mismatch is observable")
	lab.controls.nav_radius.value=0.8
	await steps(8)
	lab.depart()
	check(not lab.route_reaches_goal,"large nav clearance rejects narrow gate")
	lab.controls.physical_wall.button_pressed=false
	lab.controls.nav_wall.button_pressed=false
	await steps(8)
	lab.depart()
	await steps(210)
	check(lab.reached,"no wall in both systems allows large actor")
	lab.controls.reset.pressed.emit()
	await steps(10)
	lab=current_scene
	check(is_equal_approx(lab.body_shape.radius,0.2) and lab.include_wall,"nav full reset restores parameters/physics")
	lab=await open_scene("res://labs/shader_lab.tscn")
	check(lab.material.shader.code.contains("void vertex"),"real shader resource")
	lab.controls.wind.value=0.2
	check(is_equal_approx(lab.material.get_shader_parameter("wind_amount"),0.2),"wind control wired")
	lab.controls.rim.value=1.2
	check(is_equal_approx(lab.material.get_shader_parameter("rim_amount"),1.2),"rim control wired")
	check(lab.reference.material_override != lab.material,"reference independent")
	lab.controls.freeze.button_pressed=true
	var clock: float=lab.clock
	await steps(8)
	check(is_equal_approx(clock,lab.clock),"freeze holds uniform clock")
	lab.controls.enabled.button_pressed=false
	check(lab.subject.material_override is StandardMaterial3D,"disable really restores material")
	lab=await open_scene("res://labs/effects_lab.tscn")
	check(not lab.env.fog_enabled and not lab.env.glow_enabled,"effects off baseline")
	lab.controls.fog.button_pressed=true
	lab.controls.density.value=0.06
	check(lab.env.fog_enabled and is_equal_approx(lab.env.fog_density,0.06),"native fog toggles and density")
	lab.controls.glow.button_pressed=true
	check(lab.env.glow_enabled,"native glow enabled")
	check(lab.controls.dof.disabled == not lab.dof_supported,"unsupported DOF explicitly disabled")
	lab.set_effect(true,"dof")
	check(lab.attributes.dof_blur_near_enabled==lab.dof_supported,"DOF respects renderer")
	lab.set_focus(18)
	check(lab.attributes.dof_blur_near_distance==15 and lab.attributes.dof_blur_far_distance==21,"focus plane updates")
	lab.baseline()
	check(not lab.env.glow_enabled and not lab.attributes.dof_blur_far_enabled,"baseline clears all native effects")
	lab=await open_scene("res://labs/large_scene_lab.tscn")
	check(lab.chunks.size()==2 and lab.object_count==96,"initial residency bounded")
	var first: Node=lab.chunks[0]
	lab.set_travel(70)
	await steps(3)
	check(not is_instance_valid(first) and lab.chunks.size()==3,"departed chunks freed, neighbours resident")
	lab.controls.stream.button_pressed=false
	check(lab.chunks.size()==9 and lab.object_count==432,"disable streaming instantiates all")
	lab.controls.batch.button_pressed=false
	await steps(3)
	check(lab.chunks[0].get_child_count()==48,"unbatched independent render nodes")
	lab.controls.lod.button_pressed=true
	check(lab.chunks[0].get_child(0).mesh==lab.low,"far geometry LOD")
	lab.controls.batch.button_pressed=true
	check(lab.chunks[0].get_child(0) is MultiMeshInstance3D,"actual MultiMesh")
	lab.controls.occlusion.button_pressed=true
	check(lab.get_viewport().use_occlusion_culling,"native occlusion state")
	lab.controls.request_chunk.pressed.emit()
	for i in range(600):
		if is_instance_valid(lab.streamed_piece): break
		await process_frame
	check(is_instance_valid(lab.streamed_piece),"async PackedScene loaded and instantiated")
	lab.controls.release_chunk.pressed.emit()
	check(not is_instance_valid(lab.streamed_piece),"async chunk can be released")
	var w=await open_scene("res://world/exploration.tscn")
	w.store.file_path="user://production_test_only/snapshot.json"
	check(w.asset_instances.size()==12,"all 12 production asset types integrated")
	check(w.stars.get_child_count()==10 and not w.completed,"ten stable stars")
	check(w.player.animation_tree.active,"skinned player AnimationTree active")
	check(not w.collect_star("invalid"),"unknown pickup ID rejected")
	check(not w.interact(),"remote interaction rejected")
	w.player.position=Vector3(0,0.95,-30)
	w.player.velocity=Vector3.ZERO
	await steps(8)
	check(not w.interact() and not w.gate_open,"locked gate rejects keyless interaction")
	Input.action_press("move_forward")
	await steps(75)
	clear_inputs()
	check(w.player.position.z > -31.6,"locked gate blocks actual movement")
	w.player.spawn_position=w.SPAWNS.courtyard
	w.player.respawn()
	await steps(12)
	check(w.tones.size()==2,"two original audio cues prepared, playback not judged headless")
	# Genuine walk-through route: no teleports, no injected pickups, no forced gate state.
	var route: Array[Vector3]=[Vector3(0,0,2),Vector3(-2,0,-3),Vector3(2,0,-8),Vector3(0,0,-12.5),Vector3(-1,0,-15),Vector3(-3,0,-19),Vector3(4,0,-22)]
	for point in route:check(await walk_to(w,point),"walk route "+str(point))
	check(w.interact() and w.has_key,"real route obtains key at actual position")
	for point in [Vector3(3,0,-23),Vector3(0,0,-27),Vector3(0,0,-30.5)]:check(await walk_to(w,point),"forest path "+str(point))
	check(w.interact() and w.gate_open,"key unlocks main gate in range")
	check(not w.interact(),"repeated gate interaction is idempotent")
	await steps(5)
	check(w.gate_shape.disabled,"open gate removes real blocking shape")
	for point in [Vector3(0,0,-34),Vector3(2,0,-39),Vector3(0,0,-44)]:check(await walk_to(w,point),"lookout path "+str(point))
	check(w.completed and w.seen_ids.size()==10,"all ten collected by actual walking")
	check(w.checkpoint=="lookout","actual checkpoint reached")
	check(not w.collect_star("courtyard_0"),"duplicate stable ID rejected")
	check(w.save_game(),"main game writes verified save")
	w.player.position=Vector3(4,0.95,-3.5)
	w.player.velocity=Vector3.ZERO
	w.player.visual.rotation.y=0
	await steps(20)
	var hits: int=w.training_hits
	check(w.player.begin_attack(),"grounded attack starts")
	check(not w.player.begin_attack(),"same attack cannot stack")
	await steps(60)
	check(w.training_hits==hits+1,"one window records exactly one in-range frontal hit")
	check(w.player.attack_time<0,"attack ends and control returns")
	w.player.visual.rotation.y=PI
	w.player.begin_attack()
	await steps(60)
	check(w.training_hits==hits+1,"target behind player not hit")
	w.player.visual.rotation.y=0
	w.player.begin_attack()
	w.player.cancel_attack()
	await steps(40)
	check(w.training_hits==hits+1,"interruption before window cancels hit")
	w.set_training(false)
	check(not w.player.begin_attack() and not w.dummy.visible,"optional combat can be fully disabled")
	check(w.completed,"combat toggle cannot revoke ten-star completion")
	w.pause_game(true)
	var before: Vector3=w.player.position
	Input.action_press("move_forward")
	await steps(20)
	check(w.player.position.is_equal_approx(before),"pause stops movement")
	w.pause_game(false)
	check(not Input.is_action_pressed("move_forward"),"resume clears held input")
	check(w.load_game(),"load original saved progress")
	check(w.player.position.distance_to(w.SPAWNS.lookout)<0.15 and w.completed,"load restores safe checkpoint and completion")
	check(w.stars.get_child_count()==0,"load does not respawn collected stars")
	check(w.player.attack_time<0,"load cancels transient combat")
	var bad: Dictionary=w.snapshot()
	bad.collected=["invented"]
	check(not w.apply_snapshot(bad) and w.completed,"invalid apply is transactional")
	var state:=fixture()
	var store=STORE.new()
	store.file_path="user://production_test_only/validation.json"
	check(store.write_snapshot(state).ok,"store valid fixture")
	state.training_hits=3
	check(store.write_snapshot(state).ok,"rotate backup")
	check(store.read_snapshot(true).data.training_hits==2,"backup contains previous valid state")
	var f:=FileAccess.open(store.file_path,FileAccess.WRITE)
	f.store_string("broken json");f.close()
	check(not store.read_snapshot().ok,"corrupt JSON rejected")
	check(store.read_snapshot(true).ok,"backup available explicitly")
	state.training_hits=4
	check(store.write_snapshot(state).ok,"can save new state without clobbering valid backup with corruption")
	check(store.read_snapshot(true).data.training_hits==2,"valid backup survives corrupt primary")
	var cases: Array[Dictionary]=[]
	for change in [{"version":true},{"version":2.1},{"version":"2"},{"version":99},{"collected":["courtyard_0","courtyard_0"]},{"checkpoint":"outside"},{"gate_open":true,"has_key":false},{"training_hits":-1},{"training_hits":2.5},{"training_hits":"2"},{"volume":2},{"low_motion":"false"},{"checkpoint":"lookout","gate_open":false}]:
		var c:=fixture();c.merge(change,true);cases.append(c)
	for i in range(cases.size()):check(not store.validate_snapshot(cases[i]).ok,"negative schema "+str(i))
	var old:=fixture();old.version=1;old.erase("volume");old.erase("low_motion")
	check(store.validate_snapshot(old).ok and store.validate_snapshot(old).migrated,"explicit v1 fixture migrates")
	store.file_path="user://production_test_only/missing.json"
	check(not store.read_snapshot().ok,"missing save is not false success")
	clear_inputs()
	paused=false
	if failures.is_empty():print("PRODUCTION SUITE PASS: %d assertions; not human learning or commercial acceptance"%checks)
	else:print("PRODUCTION SUITE FAIL: ",failures)
	quit(0 if failures.is_empty() else 1)
