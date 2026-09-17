extends "res://labs/lab_shell.gd"
var material: ShaderMaterial
var subject: MeshInstance3D
var reference: MeshInstance3D
var clock := 0.0
var frozen := false
func _ready() -> void:
	setup("E03｜一个可关闭的Shader", "同一模型左右对照。先只开条纹、边缘强调或风摆其中一项；冻结时间，比较远近与轮廓。")
	for x in [-0.1, 3.0]:
		var node := MeshInstance3D.new()
		var mesh := SphereMesh.new()
		mesh.radius = 0.8
		mesh.height = 2.0
		node.mesh = mesh
		node.position = Vector3(x, 1.0, 0)
		stage.add_child(node)
		if x < 1: reference = node
		else: subject = node
	var ref_mat := StandardMaterial3D.new()
	ref_mat.albedo_color = Color(0.23, 0.56, 0.42)
	ref_mat.roughness = 0.85
	reference.material_override = ref_mat
	material = ShaderMaterial.new()
	material.shader = preload("res://shaders/learning_surface.gdshader")
	subject.material_override = material
	toggle("enabled", "右侧使用Shader", true, func(v): subject.material_override = material if v else ref_mat)
	toggle("stripe", "条纹（表面，不是增加几何）", false, func(v): material.set_shader_parameter("stripe", v))
	slider("wind", "风摆幅度（只影响显示）", 0, 0.25, 0, 0.01, func(v): material.set_shader_parameter("wind_amount", v))
	slider("rim", "边缘强调强度", 0, 2, 0, 0.1, func(v): material.set_shader_parameter("rim_amount", v))
	toggle("freeze", "冻结实验时间", false, func(v): frozen = v)
	slider("distance", "相机距离", 8, 18, 11, 0.5, func(v): camera.position = Vector3(4, 4, v); camera.look_at(Vector3(-0.8, 1, 0)))
	text("这是已编译的空间Shader，左侧永不共享右侧参数。风摆不移动碰撞体；不是万能材质转换器，也不替代Blender材质。效果默认全关，不靠叠满特效达标。")
func _process(delta: float) -> void:
	if not is_instance_valid(material): return
	if not frozen: clock += delta
	material.set_shader_parameter("clock", clock)
	status.text = "渲染器：%s\n实验时间 %.2f｜冻结 %s" % [RenderingServer.get_current_rendering_method(), clock, str(frozen)]
