extends Node3D
## Main production reference. Old scenes/main.tscn remains a stable teaching fixture.
const SaveStore = preload("res://world/save_store.gd")
const STAR = preload("res://scenes/star.tscn")
const ASSET_ROOT := "res://assets/village/"
const STAR_POSITIONS := [Vector3(0,1,2), Vector3(-2,1,-3), Vector3(2,1,-8), Vector3(-1,1,-15), Vector3(-3,1,-19), Vector3(3,1,-23), Vector3(0,1,-27), Vector3(0,1,-34), Vector3(2,1,-39), Vector3(0,1,-44)]
const SPAWNS := {"courtyard": Vector3(0,0.95,4), "forest": Vector3(0,0.95,-15), "lookout": Vector3(0,0.95,-34)}
const Creation = preload("res://world/creation_settings.gd")
@export var creation: Resource = preload("res://world/creation.tres")
var saved_snapshot: Dictionary = {}
var pending_action := ""
var guard: ConfirmationDialog
var guard_discard: Button
var guard_was_paused := false
var design_notice := ""
var store = SaveStore.new()
var seen_ids: Dictionary = {}
var has_key := false
var gate_open := false
var checkpoint := "courtyard"
var training_enabled := true
var training_hits := 0
var low_motion := true
var volume := 0.6
var completed := false
var player: CharacterBody3D
var world: Node3D
var stars: Node3D
var camera: Camera3D
var gate: Node3D
var gate_shape: CollisionShape3D
var key_visual: Node3D
var key_label: Label3D
var training_label: Label3D
var dummy: Node3D
var banner: Label
var objective: Label
var message: Label
var help: Label
var pause_panel: PanelContainer
var training_toggle: CheckButton
var motion_toggle: CheckButton
var volume_slider: HSlider
var confirmation: ConfirmationDialog
var asset_cache := {}
var asset_instances := {}
var status_time := 0.0
var play_time := 0.0
var hit_pulse := 0.0
var tones: Array[AudioStreamPlayer] = []
var scenic: Node3D

func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	add_to_group("production_world")
	world = $Gameplay
	get_viewport().msaa_3d = Viewport.MSAA_2X
	player = $Gameplay/Player
	player.strike_window.connect(_try_hit)
	player.get_node("Orbit/SpringArm3D/Camera3D").current = false
	_hide_layout_preview()
	_apply_creation()
	_build_environment()
	_build_map()
	_build_ui()
	_build_audio()
	spawn_stars()
	_update_progress()
	camera_snap()
	saved_snapshot = snapshot().duplicate(true)
	var resumed: bool = get_node("/root/StudySession").restore(self)
	show_message("已继续刚才的游戏，回到区域安全点。未写盘的变化仍需保存。" if resumed else "欢迎来到星光小庭院。收集十颗星星；林路上的钥匙能打开观景台。", 7)
	if not design_notice.is_empty(): show_message(design_notice, 12)

func _build_environment() -> void:
	var we := WorldEnvironment.new()
	we.environment = Environment.new()
	we.environment.background_mode = Environment.BG_COLOR
	we.environment.background_color = Color("aac7c3")
	we.environment.tonemap_mode = Environment.TONE_MAPPER_FILMIC
	we.environment.tonemap_exposure = 0.95
	we.environment.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	we.environment.ambient_light_color = Color.WHITE
	we.environment.ambient_light_energy = 0.20
	world.add_child(we)
	var sun := DirectionalLight3D.new()
	sun.rotation_degrees = Vector3(-52,-32,0)
	sun.light_color = Color.WHITE
	sun.light_energy = 0.20
	sun.shadow_enabled = true
	sun.directional_shadow_max_distance = 70
	world.add_child(sun)
	camera = Camera3D.new()
	camera.fov = 43
	camera.far = 160
	camera.current = true
	add_child(camera)

func box(at: Vector3, size: Vector3, color: Color, collision: bool = false, parent: Node3D = null) -> Node3D:
	var holder: Node3D = StaticBody3D.new() if collision else Node3D.new()
	(parent if parent != null else world).add_child(holder)
	holder.position = at
	var mesh := MeshInstance3D.new()
	var resource := BoxMesh.new()
	resource.size = size
	mesh.mesh = resource
	var mat := StandardMaterial3D.new()
	mat.albedo_color = color
	mat.roughness = 0.96
	mesh.material_override = mat
	holder.add_child(mesh)
	if collision:
		var cs := CollisionShape3D.new()
		var bs := BoxShape3D.new()
		bs.size = size
		cs.shape = bs
		holder.add_child(cs)
	return holder

func asset(kind: String, at: Vector3, yaw: float = 0, scale_value: float = 1) -> Node3D:
	if not asset_cache.has(kind): asset_cache[kind] = load(ASSET_ROOT + kind + ".glb")
	var instance: Node3D = asset_cache[kind].instantiate()
	scenic.add_child(instance)
	instance.position = at
	instance.rotation.y = yaw
	instance.scale = Vector3.ONE * scale_value
	asset_instances[kind] = int(asset_instances.get(kind, 0)) + 1
	return instance

func label3d(value: String, at: Vector3, color: Color = Color.WHITE) -> Label3D:
	var node := Label3D.new()
	node.text = value
	node.position = at
	node.font_size = 44
	node.pixel_size = 0.008
	node.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	node.modulate = color
	node.outline_size = 8
	var font := SystemFont.new()
	font.font_names = PackedStringArray(["Noto Sans CJK SC", "Microsoft YaHei", "PingFang SC"])
	node.font = font
	world.add_child(node)
	return node

func _build_map() -> void:
	scenic = Node3D.new()
	scenic.name = "ProductionAssets"
	world.add_child(scenic)
	_build_distant_landscape()
	# Three continuous safe floor areas; shallow rivers are scenery, not false hazards.
	box(Vector3(0,-0.45,-21), Vector3(19,0.9,58), Color("776e54"), true)
	for segment in [[0.0,"91ae75"],[-20.0,"799666"],[-40.0,"9aae7d"]]:
		box(Vector3(0,0.01,segment[0]), Vector3(18.5,0.03,19.7), Color(segment[1]))
	for x in [-9.1,9.1]:
		var edge := box(Vector3(x,0.65,-21), Vector3(0.45,1.3,58), Color("879887"), true)
		edge.get_child(0).scale.y = 0.3
		edge.get_child(0).position.y = -0.43
	for z in [7.7,-49.7]:
		var edge := box(Vector3(0,0.65,z),Vector3(18,1.3,0.45),Color("879887"),true)
		edge.get_child(0).scale.y = 0.3
		edge.get_child(0).position.y = -0.43
	# Warm winding ribbon instead of placing detail uniformly.
	var points: Array[Vector3] = [Vector3(0,0.05,6),Vector3(0,0.05,-3),Vector3(2,0.05,-8),Vector3(0,0.05,-13),Vector3(-2,0.05,-19),Vector3(1,0.05,-25),Vector3(0,0.05,-33),Vector3(1,0.05,-41),Vector3(0,0.05,-46)]
	build_path(points, 2.6)
	build_path([Vector3(-2,0.055,-19),Vector3(4,0.055,-22)],1.5)
	build_path([Vector3(0,0.055,-3),Vector3(4,0.055,-5)],1.4)
	for z in [-12.5,-30.0]:
		box(Vector3(0,0.04,z),Vector3(18,0.06,2.4),Color("69a4a1"))
		asset("bridge",Vector3(0,0.08,z))
		box(Vector3(0,0.15,z),Vector3(3.3,0.25,3.1),Color("b58b60"),true)
		for side in [-1.0,1.0]:
			var ramp := box(Vector3(0,0.10,z+side*1.95),Vector3(3.3,0.10,1.3),Color("b58b60"),true)
			ramp.rotation.x = side * 0.20
	asset("cottage",Vector3(-5,0,-2),0.15)
	box(Vector3(-5,1.4,-2),Vector3(3.2,2.8,2.9),Color("eadbb6"),true).get_child(0).hide()
	asset("cottage",Vector3(5.4,0,-18),-0.3,0.78)
	box(Vector3(5.4,1.05,-18),Vector3(2.5,2.1,2.5),Color("eadbb6"),true).get_child(0).hide()
	for at in [Vector3(-3.2,0,3),Vector3(3,0,-10),Vector3(-3.3,0,-16),Vector3(3,0,-26),Vector3(-2.8,0,-35),Vector3(3,0,-43)]: asset("lantern",at)
	for at in [Vector3(2.5,0,3),Vector3(-3.2,0,-14),Vector3(3.3,0,-28),Vector3(-2.8,0,-37)]:asset("signpost",at)
	# Deliberate clusters; no foliage on the central travel corridor.
	var placements := [Vector3(-7,0,4),Vector3(-6,0,6),Vector3(6.6,0,5),Vector3(7.2,0,-2),Vector3(-6.5,0,-8),Vector3(5.5,0,-9),Vector3(-6.4,0,-15),Vector3(-7.1,0,-18),Vector3(-5.8,0,-22),Vector3(6.7,0,-25),Vector3(7.2,0,-28),Vector3(-6.5,0,-29),Vector3(-7,0,-36),Vector3(6.4,0,-36),Vector3(-6.6,0,-44),Vector3(6,0,-46)]
	for i in range(placements.size()):
		asset("pine" if i >= 6 and i <= 11 else "broadleaf", placements[i], i*0.71, 0.8 + (i%3)*0.13)
		if i%2 == 0: asset("rock_cluster",placements[i]+Vector3(1.0,0,0.6), i*0.4,0.7)
		asset("flower_patch",placements[i]+Vector3(-0.8,0,1.4), i*0.37,1.1)
	for z in [3.0,0.0,-5.5]: asset("fence",Vector3(-6.8,0,z),PI/2)
	for x in [-4.0,-2.0,2.0,4.0]: asset("fence",Vector3(x,0,-47))
	asset("lookout_deck",Vector3(0,0,-43))
	# Low platform collider; its stepped entrance is deliberately traversable.
	box(Vector3(0,0.22,-43),Vector3(4.1,0.44,4.1),Color("a9ada0"),true).get_child(0).hide()
	var approach := box(Vector3(0,0.20,-40.1),Vector3(5.2,0.12,2.4),Color("a9ada0"),true)
	approach.rotation.x = 0.19
	asset("beacon",Vector3(0,0.56,-43.7))
	label3d("出发",Vector3(2.5,1.8,3),Color("fff0cc"))
	label3d("林路",Vector3(-3.2,1.8,-14),Color("fff0cc"))
	label3d("星光终点",Vector3(0,2.8,-46.5),Color("fff0cc"))
	dummy = asset("training_dummy",Vector3(4,0,-5))
	training_label = label3d("可选训练 · J",Vector3(4,2.5,-5),Color("fff0cc"))
	# Gate separates traversal but does not make optional combat mandatory.
	for x in [-5.7,5.7]:box(Vector3(x,1.5,-32),Vector3(7.5,3,0.55),Color("7f9180"),true)
	var gate_body := StaticBody3D.new()
	world.add_child(gate_body)
	gate_body.position = Vector3(0,1.3,-32)
	gate_shape = CollisionShape3D.new()
	var gs := BoxShape3D.new()
	gs.size = Vector3(3.9,2.6,0.4)
	gate_shape.shape = gs
	gate_body.add_child(gate_shape)
	gate = Node3D.new()
	gate_body.add_child(gate)
	gate.position = Vector3(-1.9,0,0)
	box(Vector3(1.9,0,0),Vector3(3.8,2.5,0.23),Color("b09564"),false,gate)
	for y in [-0.9,0.9]:box(Vector3(1.9,y,0.15),Vector3(3.6,0.1,0.1),Color("79533c"),false,gate)
	label3d("观景门 · E",Vector3(0,3,-32),Color("ffe1a0"))
	key_visual = asset("beacon",Vector3(4,0,-22),0,0.7)
	key_label = label3d("钥匙 · 靠近按 E",Vector3(4,2,-22),Color("ffdf73"))
	stars = Node3D.new()
	stars.name = "Stars"
	world.add_child(stars)

func _build_distant_landscape() -> void:
	# Non-playable low-contrast silhouettes communicate a valley, not more reachable map.
	box(Vector3(0,-1.4,-25),Vector3(90,0.15,140),Color("8aafaa"))
	for i in range(9):
		var hill := MeshInstance3D.new()
		var sphere := SphereMesh.new()
		sphere.radius = 1
		sphere.height = 2
		sphere.radial_segments = 12
		sphere.rings = 6
		hill.mesh = sphere
		var material := StandardMaterial3D.new()
		material.albedo_color = Color("8ea99d") if i % 2 == 0 else Color("829e96")
		material.roughness = 1
		hill.material_override = material
		hill.position = Vector3(-25+i*6.5,-2,-59-float(i%3)*5)
		hill.scale = Vector3(7.8,5.5+float(i%3)*1.4,9)
		hill.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		world.add_child(hill)

func build_path(points: Array[Vector3], width: float) -> void:
	var sampled: Array[Vector3] = []
	for i in range(points.size()-1):
		for j in range(8):
			sampled.append(points[i].cubic_interpolate(points[i+1], points[maxi(0,i-1)], points[mini(points.size()-1,i+2)], j/8.0))
	sampled.append(points[-1])
	var left: Array[Vector3] = []
	var right: Array[Vector3] = []
	for i in range(sampled.size()):
		var tangent := (sampled[mini(i+1,sampled.size()-1)]-sampled[maxi(i-1,0)]).normalized()
		var side := tangent.cross(Vector3.UP)*width/2
		left.append(sampled[i]+side)
		right.append(sampled[i]-side)
	var surface := SurfaceTool.new()
	surface.begin(Mesh.PRIMITIVE_TRIANGLES)
	for i in range(sampled.size()-1):
		for p in [left[i],right[i+1],right[i],left[i],left[i+1],right[i+1]]:surface.add_vertex(p)
	surface.generate_normals()
	var node := MeshInstance3D.new()
	node.mesh = surface.commit()
	var mat := StandardMaterial3D.new()
	mat.albedo_color = creation.path_color
	mat.roughness = 1
	mat.cull_mode = BaseMaterial3D.CULL_DISABLED
	node.material_override = mat
	world.add_child(node)

func spawn_stars() -> void:
	for child in stars.get_children():
		stars.remove_child(child)
		child.queue_free()
	for i in range(STAR_POSITIONS.size()):
		var id: String = SaveStore.STAR_IDS[i]
		if seen_ids.has(id): continue
		var star = STAR.instantiate()
		star.pickup_id = id
		star.name = id
		var marker := get_node_or_null("StarLayout/" + id) as Marker3D
		star.position = marker.position if marker != null else STAR_POSITIONS[i]
		star.collected.connect(collect_star)
		stars.add_child(star)

func collect_star(id: String) -> bool:
	if not SaveStore.STAR_IDS.has(id) or seen_ids.has(id): return false
	seen_ids[id] = true
	_update_progress()
	play_tone(0)
	show_message("星光已收集 %d / 10" % seen_ids.size(),2)
	return true

func flat_distance(a: Vector3, b: Vector3) -> float:
	return Vector2(a.x,a.z).distance_to(Vector2(b.x,b.z))

func interact() -> bool:
	if get_tree().paused: return false
	if not has_key and flat_distance(player.position,Vector3(4,0,-22)) <= 2.1:
		has_key = true
		key_visual.hide()
		key_label.hide()
		_update_progress()
		show_message("获得观景门钥匙。到门前按 E 打开。",4)
		play_tone(0)
		return true
	if flat_distance(player.position,Vector3(0,0,-32)) <= 2.4:
		if gate_open:
			show_message("门已经打开。",2)
			return false
		if not has_key:
			show_message("门还锁着。钥匙在林路右侧的小信标。",4)
			return false
		gate_open = true
		apply_gate()
		_update_progress()
		show_message("观景门已打开。最后三颗星星就在前方。",4)
		play_tone(0)
		return true
	show_message("附近没有可操作对象。留意钥匙和观景门。",2)
	return false

func apply_gate() -> void:
	gate.rotation.y = -PI/2 if gate_open else 0
	gate_shape.set_deferred("disabled",gate_open)

func _try_hit() -> void:
	if not training_enabled or player.hit_confirmed: return
	var to_target: Vector3 = dummy.global_position-player.global_position
	to_target.y = 0
	var forward: Vector3 = -player.visual.global_basis.z
	if to_target.length() > 1.9 or (to_target.length()>0.01 and forward.dot(to_target.normalized()) < 0.3): return
	player.hit_confirmed = true
	training_hits = mini(training_hits + 1, 1000000)
	hit_pulse = 0.2
	show_message("有效命中 %d 次 · 同一次挥击只计一次" % training_hits,2)
	play_tone(1)

func set_training(value: bool) -> void:
	training_enabled = value
	player.training_enabled = value
	player.cancel_attack()
	dummy.visible = value
	training_label.visible = value
	if training_toggle != null:training_toggle.set_pressed_no_signal(value)

func snapshot() -> Dictionary:
	return {"version":2,"collected":seen_ids.keys(),"checkpoint":checkpoint,"has_key":has_key,"gate_open":gate_open,"training_enabled":training_enabled,"training_hits":training_hits,"low_motion":low_motion,"volume":volume}

func save_game() -> bool:
	var result: Dictionary = store.write_snapshot(snapshot())
	show_message(result.message,5)
	if result.ok: saved_snapshot = snapshot().duplicate(true)
	return result.ok

func load_game(backup: bool = false) -> bool:
	var result: Dictionary = store.read_snapshot(backup)
	if not result.ok:
		show_message(result.message,5)
		return false
	if not apply_snapshot(result.data): return false
	saved_snapshot = snapshot().duplicate(true)
	show_message(("已恢复备份。" if backup else "继续游戏。")+result.message,5)
	return true

func apply_snapshot(data: Dictionary) -> bool:
	var result: Dictionary = store.validate_snapshot(data)
	if not result.ok: return false
	var valid: Dictionary = result.data
	seen_ids.clear()
	for id in valid.collected:seen_ids[id]=true
	has_key=valid.has_key
	gate_open=valid.gate_open
	checkpoint=valid.checkpoint
	training_hits=valid.training_hits
	low_motion=valid.low_motion
	volume=valid.volume
	set_training(valid.training_enabled)
	apply_gate()
	key_visual.visible=not has_key
	key_label.visible=not has_key
	player.spawn_position=SPAWNS[checkpoint]
	player.respawn()
	spawn_stars()
	_update_progress()
	motion_toggle.set_pressed_no_signal(low_motion)
	volume_slider.set_value_no_signal(volume)
	camera_snap()
	return true

func _process(delta: float) -> void:
	if get_tree().paused:return
	play_time += delta
	status_time=maxf(0,status_time-delta)
	if status_time==0:message.text=""
	var next_checkpoint := "lookout" if player.position.z < -33 and gate_open else "forest" if player.position.z < -14 else "courtyard"
	if next_checkpoint != checkpoint:
		checkpoint=next_checkpoint
		player.spawn_position=SPAWNS[checkpoint]
		_update_progress()
	var focus := Vector3(clampf(player.position.x * 0.25,-1.6,1.6),0,clampf(player.position.z-3,-44,1))
	camera.position = camera.position.lerp(focus+Vector3(0,16,15),minf(1,delta*5))
	camera.rotation_degrees=Vector3(-46.85,0,0)
	if hit_pulse>0:
		hit_pulse=maxf(0,hit_pulse-delta)
		dummy.scale=Vector3.ONE*(1+hit_pulse*0.25 if not low_motion else 1)
	else:dummy.scale=Vector3.ONE
	if not has_key and flat_distance(player.position,Vector3(4,0,-22))<2.1:help.text="按 E 拿起钥匙"
	elif flat_distance(player.position,Vector3(0,0,-32))<2.4:help.text="按 E 操作观景门"
	elif training_enabled and flat_distance(player.position,dummy.position)<2.3:help.text="面向木桩按 J · 训练为选修，不影响通关"
	else:help.text="WASD 移动 · Shift 跑 · 空格跳 · E 交互 · J 训练 · Esc 菜单"

func camera_snap() -> void:
	var focus := Vector3(clampf(player.position.x*0.25,-1.6,1.6),0,clampf(player.position.z-3,-44,1))
	camera.position=focus+Vector3(0,16,15)
	camera.rotation_degrees=Vector3(-46.85,0,0)

func _unhandled_input(event: InputEvent) -> void:
	if not event is InputEventKey or not event.pressed or event.echo:return
	if event.physical_keycode==KEY_ESCAPE:
		if not pending_action.is_empty():
			cancel_action()
			get_viewport().set_input_as_handled()
			return
		pause_game(not get_tree().paused)
		get_viewport().set_input_as_handled()
	elif not get_tree().paused:
		match event.physical_keycode:
			KEY_E:interact()
			KEY_F9:save_game()
			KEY_F10:request_action("load")
			KEY_R: request_action("new")

func pause_game(value: bool) -> void:
	get_tree().paused=value
	pause_panel.visible=value
	for action in ["move_left","move_right","move_forward","move_back","sprint","jump","attack"]:Input.action_release(action)
	if value:
		player.cancel_attack()
		player.velocity=Vector3.ZERO

func _notification(what: int) -> void:
	if what == NOTIFICATION_APPLICATION_FOCUS_OUT and is_instance_valid(pause_panel):pause_game(true)

func new_game() -> void:
	pause_game(false)
	get_tree().reload_current_scene()

func open_labs() -> void:
	request_action("labs")

func _build_ui() -> void:
	var canvas:=CanvasLayer.new()
	canvas.process_mode=Node.PROCESS_MODE_ALWAYS
	add_child(canvas)
	var root:=Control.new()
	root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	root.mouse_filter=Control.MOUSE_FILTER_IGNORE
	canvas.add_child(root)
	var theme:=Theme.new()
	var font:=SystemFont.new()
	font.font_names=PackedStringArray(["Noto Sans CJK SC","Microsoft YaHei","PingFang SC"])
	theme.default_font=font
	theme.default_font_size=18
	root.theme=theme
	var top:=PanelContainer.new()
	top.position=Vector2(18,16)
	top.custom_minimum_size=Vector2(495,0)
	root.add_child(top)
	var rows:=VBoxContainer.new()
	rows.add_theme_constant_override("separation",5)
	top.add_child(rows)
	banner=ui_label(rows,"星光小庭院",26)
	objective=ui_label(rows,"",18)
	message=ui_label(rows,"",16)
	message.autowrap_mode=TextServer.AUTOWRAP_WORD_SMART
	message.custom_minimum_size.x=475
	var bottom:=PanelContainer.new()
	bottom.set_anchors_and_offsets_preset(Control.PRESET_BOTTOM_WIDE)
	bottom.offset_left=18
	bottom.offset_right=-18
	bottom.offset_top=-66
	bottom.offset_bottom=-12
	root.add_child(bottom)
	var bottom_rows:=VBoxContainer.new()
	bottom.add_child(bottom_rows)
	help=ui_label(bottom_rows,"",17)
	ui_label(bottom_rows,"F9 保存 · F10 继续存档 · R 重新开始（先确认） · 固定朝向镜头",14)
	pause_panel=PanelContainer.new()
	pause_panel.anchor_left=0.5
	pause_panel.anchor_right=0.5
	pause_panel.anchor_top=0.1
	pause_panel.anchor_bottom=0.9
	pause_panel.offset_left=-215
	pause_panel.offset_right=215
	root.add_child(pause_panel)
	var scroll:=ScrollContainer.new()
	scroll.horizontal_scroll_mode=ScrollContainer.SCROLL_MODE_DISABLED
	pause_panel.add_child(scroll)
	var menu:=VBoxContainer.new()
	menu.custom_minimum_size.x=408
	menu.size_flags_horizontal=Control.SIZE_EXPAND_FILL
	menu.add_theme_constant_override("separation",8)
	scroll.add_child(menu)
	ui_label(menu,"暂停 · 进度由你决定何时保存",22)
	ui_button(menu,"返回游戏",func():pause_game(false))
	ui_button(menu,"保存当前进度",save_game)
	ui_button(menu,"继续主存档",func():request_action("load"))
	ui_button(menu,"主存档损坏时：尝试备份",func():request_action("backup"))
	ui_button(menu,"恢复读取前保护副本",func():request_action("recover"))
	training_toggle=CheckButton.new()
	training_toggle.text="开启可选木桩训练（不影响十星）"
	training_toggle.button_pressed=true
	training_toggle.toggled.connect(set_training)
	menu.add_child(training_toggle)
	motion_toggle=CheckButton.new()
	motion_toggle.text="低运动反馈（关闭命中缩放）"
	motion_toggle.button_pressed=true
	motion_toggle.toggled.connect(func(v):low_motion=v)
	menu.add_child(motion_toggle)
	ui_label(menu,"反馈音量（静音仍有文字反馈）",16)
	volume_slider=HSlider.new()
	volume_slider.min_value=0
	volume_slider.max_value=1
	volume_slider.step=0.1
	volume_slider.value=volume
	volume_slider.value_changed.connect(func(v):volume=v)
	menu.add_child(volume_slider)
	ui_button(menu,"进入实验（保留本次暂存）",open_labs)
	ui_button(menu,"重新开始（保留磁盘存档）",func():request_action("new"))
	ui_button(menu,"退出游戏",func():request_action("quit"))
	pause_panel.hide()
	_build_guard(root)
	confirmation=ConfirmationDialog.new()
	confirmation.title="重新开始？"
	confirmation.dialog_text="当前未保存的进度会丢失。已有磁盘存档保留，除非你之后主动保存覆盖。"
	confirmation.confirmed.connect(new_game)
	root.add_child(confirmation)

func ui_label(parent: Node,value: String,size_value: int)->Label:
	var label:=Label.new()
	label.text=value
	label.add_theme_font_size_override("font_size",size_value)
	parent.add_child(label)
	return label
func ui_button(parent: Node,value: String,callback: Callable)->Button:
	var button:=Button.new()
	button.text=value
	button.custom_minimum_size.y=32
	button.pressed.connect(callback)
	parent.add_child(button)
	return button
func _update_progress()->void:
	completed=seen_ids.size()==SaveStore.STAR_IDS.size()
	if not is_instance_valid(banner):return
	banner.text="星光小庭院  ·  %s" % {"courtyard":"01 庭院","forest":"02 林路","lookout":"03 观景台"}[checkpoint]
	objective.text="星光 %d / 10  ·  钥匙 %s" % [seen_ids.size(),"已取得" if has_key else "未取得"]
	if completed:objective.text="十颗星光已点亮！可以继续探索、保存，或在菜单重新开始。"
func show_message(value: String,duration: float)->void:
	if is_instance_valid(message):message.text=value
	status_time=duration
func _build_audio()->void:
	for freq in [660.0,220.0]:
		var stream:=AudioStreamWAV.new()
		stream.format=AudioStreamWAV.FORMAT_16_BITS
		stream.mix_rate=22050
		var bytes:=PackedByteArray()
		for i in range(4410):
			var sample:=int(sin(TAU*freq*i/22050.0)*exp(-i/1200.0)*7000)
			bytes.append(sample & 255)
			bytes.append((sample >> 8)&255)
		stream.data=bytes
		var audio:=AudioStreamPlayer.new()
		audio.stream=stream
		world.add_child(audio)
		tones.append(audio)
func play_tone(index: int)->void:
	if tones.size()<=index or volume<=0 or DisplayServer.get_name()=="headless":return
	tones[index].volume_db=linear_to_db(volume)
	tones[index].play()

func _exit_tree() -> void:
	for tone in tones:
		if is_instance_valid(tone):
			tone.stop()
			tone.stream = null

func _apply_creation() -> void:
	if creation == null or creation.get_script() != Creation or not creation.problem().is_empty():
		design_notice = "创作配置无效；本次使用原基线，请检查world/creation.tres。"
		creation = Creation.new()
	player.walk_speed = creation.walk_speed
	player.run_speed = creation.run_speed
	player.jump_velocity = creation.jump_velocity
	player.gravity = creation.gravity

func has_unsaved_changes() -> bool:
	return snapshot() != saved_snapshot

func _build_guard(parent: Node) -> void:
	guard = ConfirmationDialog.new()
	guard.title = "先保护当前进度"
	guard.cancel_button_text = "取消，留在这里"
	guard.dialog_hide_on_ok = false
	guard_discard = guard.add_button("不保存继续", false, "discard")
	guard.confirmed.connect(func(): resolve_action(true))
	guard.custom_action.connect(func(action):
		if action == "discard": resolve_action(false))
	guard.canceled.connect(cancel_action)
	parent.add_child(guard)

func request_action(action: String) -> void:
	if not ["labs", "quit", "new", "load", "backup", "recover"].has(action): return
	if not pending_action.is_empty(): return
	guard_was_paused = get_tree().paused
	pending_action = action
	pause_game(true)
	if not has_unsaved_changes() and action != "new":
		_perform_action()
		return
	var reading := ["load", "backup", "recover"].has(action)
	guard.ok_button_text = "另存保护副本后读取" if reading else "保存后继续"
	guard_discard.text = "暂不写盘，进入实验" if action == "labs" else "不保存当前变化，继续"
	guard.dialog_text = ("读取会替换当前进度。保护副本与要读取的旧档分开，原主档与备份不会被覆盖。" if reading else
		"进入实验会暂存本次进度；可从右上角返回。暂存只在本次程序运行中有效。" if action == "labs" else
		"继续会结束当前这次游戏。未保存的变化会丢失；磁盘存档不删除。")
	guard.dialog_text += "\n保存失败会留在这里；可取消。"
	guard.popup_centered(Vector2i(620, 220))

func cancel_action() -> void:
	pending_action = ""
	guard.hide()
	pause_game(guard_was_paused)

func resolve_action(save_first: bool) -> bool:
	if pending_action.is_empty(): return false
	if save_first:
		if ["load", "backup", "recover"].has(pending_action):
			# Preserve the selected old snapshot BEFORE writing the separate rescue copy.
			var chosen: Dictionary = _read_target(pending_action)
			if not chosen.ok:
				guard.dialog_text = chosen.message + "\n尚未写入保护副本；仍留在这里。"
				return false
			var rescue := SaveStore.new()
			rescue.file_path = store.file_path + ".before-load"
			var result: Dictionary = rescue.write_snapshot(snapshot())
			if not result.ok:
				guard.dialog_text = result.message + "\n保护失败，未读取旧档。"
				return false
			return _finish_read(chosen)
		elif not save_game():
			guard.dialog_text = message.text + "\n保存失败，未离开。可重试或取消。"
			return false
	return _perform_action()

func _read_target(action: String) -> Dictionary:
	if action == "recover":
		var rescue := SaveStore.new()
		rescue.file_path = store.file_path + ".before-load"
		return rescue.read_snapshot()
	return store.read_snapshot(action == "backup")

func _finish_read(result: Dictionary) -> bool:
	if not result.ok:
		show_message(result.message, 8)
		cancel_action()
		return false
	var reading := pending_action
	if not apply_snapshot(result.data): return false
	# Main save matches disk. Backup/recovery may differ from the primary: keep it dirty.
	if reading == "load": saved_snapshot = snapshot().duplicate(true)
	else: saved_snapshot = {}
	pending_action = ""
	guard.hide()
	pause_game(guard_was_paused)
	show_message("已读取。" + ("保护副本保留了读取前的进度。" if FileAccess.file_exists(store.file_path + ".before-load") else ""), 8)
	return true

func _perform_action() -> bool:
	var action := pending_action
	if ["load", "backup", "recover"].has(action): return _finish_read(_read_target(action))
	pending_action = ""
	guard.hide()
	match action:
		"labs":
			get_node("/root/StudySession").retain(self)
			pause_game(false)
			var error := get_tree().change_scene_to_file("res://labs/lab_hub.tscn")
			if error != OK:
				pause_game(true)
				show_message("实验未能打开，游戏仍在这里。", 8)
				return false
		"new": new_game()
		"quit": get_tree().quit()
	return true

func _hide_layout_preview() -> void:
	var layout := get_node_or_null("StarLayout")
	if layout == null: return
	for child in layout.get_children():
		if child is Marker3D:
			for visual in child.get_children():
				if visual is Node3D: visual.hide()
		elif child is Node3D: child.hide()
