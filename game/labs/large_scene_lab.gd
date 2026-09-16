extends "res://labs/lab_shell.gd"
## Bounded actual residency and render batching experiment, not a huge-world benchmark.
var chunks: Dictionary = {}
var travel := 0.0
var batching := true
var streaming := true
var lod_enabled := false
var high: SphereMesh
var low: SphereMesh
var material: StandardMaterial3D
var samples: Array[float] = []
var old_occlusion := false
var occluder: OccluderInstance3D
var object_count := 0
var pending_load := false
var streamed_piece: Node3D
var load_note := "未请求磁盘区块"
const PIECE := "res://world/stream_piece.tscn"
const CHUNKS := 9
const PER_CHUNK := 48
const SPACING := 14.0
func _ready() -> void:
	setup("E02 / E05｜批量、LOD与分块", "同一分布和机位，分别改变批量绘制、几何细节、驻留范围或遮挡剔除。不要把四种技术混作一个优化。")
	high = SphereMesh.new()
	high.radius = 0.45
	high.height = 1.4
	high.radial_segments = 24
	high.rings = 12
	low = SphereMesh.new()
	low.radius = 0.45
	low.height = 1.4
	low.radial_segments = 6
	low.rings = 3
	material = StandardMaterial3D.new()
	material.albedo_color = Color("568565")
	material.roughness = 0.95
	high.material = material
	low.material = material
	old_occlusion = get_viewport().use_occlusion_culling
	occluder = OccluderInstance3D.new()
	var resource := BoxOccluder3D.new()
	resource.size = Vector3(5, 3, 0.4)
	occluder.occluder = resource
	occluder.position = Vector3(3, 1.5, 2)
	stage.add_child(occluder)
	box(occluder, "OpaqueWall", Vector3.ZERO, resource.size, Color("a1a69b"))
	toggle("batch", "同一网格使用MultiMesh", true, func(v): batching = v; rebuild_all())
	toggle("lod", "远处切低细节网格（几何LOD）", false, func(v): lod_enabled = v; update_residency())
	toggle("stream", "只驻留当前与相邻区块", true, func(v): streaming = v; update_residency())
	toggle("occlusion", "视口真实遮挡剔除", old_occlusion, func(v): get_viewport().use_occlusion_culling = v)
	slider("travel", "沿区块移动相机", 0, 8 * SPACING, 0, 2, set_travel)
	button("measure", "清空帧间隔采样，再作同条件对照", func(): samples.clear())
	button("request_chunk", "异步请求真实场景文件", request_piece)
	button("release_chunk", "卸下异步示例区块", release_piece)
	text("每区48个物体，总共9区。驻留开关实际创建/释放节点；下方按钮另用ResourceLoader异步读真实场景。共享资源可能仍缓存，不宣称全部显存释放。LOD改变几何，不改变数量；MultiMesh按整批剔除。帧间隔不是纯GPU计时，首次加载/编译要另外记录。")
	set_travel(0)
func set_travel(value: float) -> void:
	travel = value
	camera.position = Vector3(value + 6, 7, 12)
	camera.look_at(Vector3(value - 2, 0.4, 0))
	occluder.position.x = value + 3
	update_residency()
func rebuild_all() -> void:
	for key in chunks:
		stage.remove_child(chunks[key])
		chunks[key].queue_free()
	chunks.clear()
	update_residency()
func update_residency() -> void:
	var center := clampi(roundi(travel / SPACING), 0, CHUNKS - 1)
	for key in chunks.keys():
		if streaming and absi(key - center) > 1:
			stage.remove_child(chunks[key])
			chunks[key].queue_free()
			chunks.erase(key)
	for i in range(CHUNKS):
		if streaming and absi(i - center) > 1: continue
		if not chunks.has(i): chunks[i] = build_chunk(i)
		var mesh: Mesh = low if lod_enabled and absf(i * SPACING - travel) > 10 else high
		for child in chunks[i].get_children():
			if child is MultiMeshInstance3D: child.multimesh.mesh = mesh
			elif child is MeshInstance3D: child.mesh = mesh
	object_count = chunks.size() * PER_CHUNK
func build_chunk(index: int) -> Node3D:
	var chunk := Node3D.new()
	chunk.position.x = index * SPACING
	stage.add_child(chunk)
	var multi: MultiMeshInstance3D
	if batching:
		multi = MultiMeshInstance3D.new()
		multi.multimesh = MultiMesh.new()
		multi.multimesh.transform_format = MultiMesh.TRANSFORM_3D
		multi.multimesh.mesh = high
		multi.multimesh.instance_count = PER_CHUNK
		chunk.add_child(multi)
	for i in range(PER_CHUNK):
		var t := Transform3D(Basis.IDENTITY, Vector3((i % 8) * 1.25 - 4, 0.7, floori(i / 8.0) * 1.25 - 4))
		if batching: multi.multimesh.set_instance_transform(i, t)
		else:
			var m := MeshInstance3D.new()
			m.mesh = high
			m.transform = t
			chunk.add_child(m)
	return chunk
func _process(delta: float) -> void:
	if not is_instance_valid(high): return
	if pending_load:
		var state := ResourceLoader.load_threaded_get_status(PIECE)
		if state == ResourceLoader.THREAD_LOAD_LOADED:
			var resource := ResourceLoader.load_threaded_get(PIECE) as PackedScene
			streamed_piece = resource.instantiate()
			streamed_piece.position = Vector3(travel + 2, 0, 4)
			stage.add_child(streamed_piece)
			pending_load = false
			load_note = "真实文件已读取、实例已加入场景"
		elif state == ResourceLoader.THREAD_LOAD_FAILED or state == ResourceLoader.THREAD_LOAD_INVALID_RESOURCE:
			pending_load = false
			load_note = "请求失败，原实验未改变"
			controls.request_chunk.disabled = false
	samples.append(delta * 1000)
	if samples.size() > 240: samples.pop_front()
	var sorted := samples.duplicate()
	sorted.sort()
	var median: float = sorted[sorted.size() / 2]
	var p95: float = sorted[mini(sorted.size()-1, int(sorted.size() * 0.95))]
	status.text = "驻留 %d / %d 区｜测试物体 %d\n测试Mesh节点 %d｜实测draw calls %.0f\n帧间隔 中位 %.1f / P95 %.1f ms\n%s；不代表目标设备收益" % [chunks.size(), CHUNKS, object_count, chunks.size() if batching else object_count, Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME), median, p95, RenderingServer.get_current_rendering_method()] + "\n" + load_note
func _exit_tree() -> void:
	if is_inside_tree(): get_viewport().use_occlusion_culling = old_occlusion

func request_piece() -> void:
	if pending_load or is_instance_valid(streamed_piece): return
	var error := ResourceLoader.load_threaded_request(PIECE, "PackedScene", false, ResourceLoader.CACHE_MODE_IGNORE)
	pending_load = error == OK
	controls.request_chunk.disabled = pending_load
	load_note = "异步读取中；不阻塞等待结果" if pending_load else "请求未接受"
func release_piece() -> void:
	if is_instance_valid(streamed_piece):
		stage.remove_child(streamed_piece)
		streamed_piece.queue_free()
		streamed_piece = null
	if not pending_load:
		controls.request_chunk.disabled = false
		load_note = "示例节点已卸下；缓存不承诺随之释放"
