extends "res://labs/lab_shell.gd"
## Explicit teaching NavMesh, queried by NavigationServer; physics remains independent.
var nav_map: RID
var region: NavigationRegion3D
var actor: CharacterBody3D
var body_shape: SphereShape3D
var path := PackedVector3Array()
var waypoint := 0
var moving := false
var nav_radius := 0.2
var physics_radius := 0.2
var include_wall := true
var wall_shapes: Array[CollisionShape3D] = []
var markers: Node3D
var reached := false
var start := Vector3(-3, 0.4, 0)
var goal := Vector3(4, 0.4, 0)
var route_reaches_goal := false
var rebuilding := false
var rebuild_serial := 0

func _ready() -> void:
	setup("E01｜导航与真实通行", "门洞宽1.3米。导航半径与真实球半径可以不同：先预测路径存在时，角色是否一定能通过。")
	camera.position = Vector3(5, 9, 11)
	camera.look_at(Vector3(-1.5, 0, 0))
	for side in [-1.0, 1.0]:
		var wall := StaticBody3D.new()
		wall.position = Vector3(0.5, 0.7, side * 1.825)
		stage.add_child(wall)
		wall_shapes.append(shape(wall, Vector3(0.5, 1.4, 2.35)))
		box(wall, "VisibleWall", Vector3.ZERO, Vector3(0.5, 1.4, 2.35), Color("9a775a"))
	actor = CharacterBody3D.new()
	actor.collision_layer = 2
	actor.collision_mask = 1
	stage.add_child(actor)
	var cs := CollisionShape3D.new()
	body_shape = SphereShape3D.new()
	body_shape.radius = physics_radius
	cs.shape = body_shape
	actor.add_child(cs)
	var visual := MeshInstance3D.new()
	visual.name = "Body"
	var sphere := SphereMesh.new()
	sphere.radius = 1
	sphere.height = 2
	visual.mesh = sphere
	var mat := StandardMaterial3D.new()
	mat.albedo_color = Color("ffd46b")
	visual.material_override = mat
	actor.add_child(visual)
	visual.scale = Vector3.ONE * physics_radius
	actor.position = start
	box(stage, "Goal", goal - Vector3(0, 0.3, 0), Vector3(0.6, 0.1, 0.6), Color("30afa5"))
	region = NavigationRegion3D.new()
	stage.add_child(region)
	nav_map = NavigationServer3D.map_create()
	NavigationServer3D.map_set_active(nav_map, true)
	NavigationServer3D.map_set_use_async_iterations(nav_map, false)
	NavigationServer3D.region_set_use_async_iterations(region.get_rid(), false)
	region.set_navigation_map(nav_map)
	markers = Node3D.new()
	stage.add_child(markers)
	slider("nav_radius", "导航预留半径（米）", 0.1, 0.8, nav_radius, 0.05, func(v): nav_radius = v; rebuild())
	slider("body_radius", "真实碰撞球半径（米）", 0.1, 0.8, physics_radius, 0.05, set_body_radius)
	toggle("nav_wall", "导航网格考虑墙体", true, func(v): include_wall = v; rebuild())
	toggle("physical_wall", "墙体实际阻挡", true, func(v):
		for cs2 in wall_shapes: cs2.set_deferred("disabled", not v))
	button("query", "查询真实路径并出发", depart)
	button("replay", "回到起点（保留参数）", replay)
	text("蓝点来自NavigationServer3D，不是预写轨迹。网格由课程预制规则生成，非自动烘焙。大球可能卡门；导航不考虑墙时，路径也可能穿墙。未实现动态避障和敌人AI。")
	rebuild()

func set_body_radius(value: float) -> void:
	physics_radius = value
	body_shape.radius = value
	actor.get_node("Body").scale = Vector3.ONE * value
	replay()

func rebuild() -> void:
	rebuild_serial += 1
	var serial := rebuild_serial
	rebuilding = true
	replay()
	var mesh := NavigationMesh.new()
	var vertices := PackedVector3Array()
	# Shared vertices make contiguous polygons one connected surface.
	for z in range(25):
		for x in range(41): vertices.append(Vector3(-4 + x * 0.25, 0, -3 + z * 0.25))
	mesh.vertices = vertices
	for z in range(24):
		for x in range(40):
			var center := Vector3(-4 + (x + 0.5) * 0.25, 0, -3 + (z + 0.5) * 0.25)
			var touches_wall := absf(center.x - 0.5) < 0.25 + nav_radius + 0.125 and absf(center.z) > 0.65 - nav_radius - 0.125
			if include_wall and touches_wall: continue
			var i := z * 41 + x
			mesh.add_polygon(PackedInt32Array([i, i + 41, i + 42, i + 1]))
	region.navigation_mesh = mesh
	NavigationServer3D.map_force_update(nav_map)
	if serial == rebuild_serial:
		rebuilding = false
		status.text = "网格已同步。先预测，再点击查询。"

func replay() -> void:
	moving = false
	reached = false
	if is_instance_valid(actor):
		actor.position = start
		actor.velocity = Vector3.ZERO
	if is_instance_valid(markers):
		for node in markers.get_children():
			markers.remove_child(node)
			node.queue_free()
	path.clear()
	route_reaches_goal = false

func depart() -> void:
	if rebuilding: return
	replay()
	NavigationServer3D.map_force_update(nav_map)
	path = NavigationServer3D.map_get_path(nav_map, Vector3(start.x, 0, start.z), Vector3(goal.x, 0, goal.z), true)
	route_reaches_goal = not path.is_empty() and path[-1].distance_to(Vector3(goal.x, 0, goal.z)) < 0.3
	for p in path: box(markers, "PathPoint", p + Vector3(0, 0.08, 0), Vector3(0.16, 0.1, 0.16), Color("3bcec8"))
	waypoint = 0
	moving = path.size() > 0

func _physics_process(delta: float) -> void:
	if moving and waypoint < path.size():
		var target := Vector3(path[waypoint].x, start.y, path[waypoint].z)
		var offset := target - actor.position
		if offset.length() < 0.08:
			waypoint += 1
		else:
			actor.velocity = offset.normalized() * minf(2.6, offset.length() / delta)
			actor.move_and_slide()
		if waypoint >= path.size(): moving = false
	if is_instance_valid(actor):
		reached = Vector2(actor.position.x, actor.position.z).distance_to(Vector2(goal.x, goal.z)) < 0.3
		if not rebuilding:
			status.text = "导航到达目标：%s\n实际到达：%s｜路径点 %d\n导航 %.2f米 / 碰撞 %.2f米" % [str(route_reaches_goal), str(reached), path.size(), nav_radius, physics_radius]

func _exit_tree() -> void:
	if nav_map.is_valid():
		region.set_navigation_map(RID())
		NavigationServer3D.free_rid(nav_map)
