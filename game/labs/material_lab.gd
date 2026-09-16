extends "res://labs/lab_shell.gd"
## B04 / C05 / D02: real shared resources, independent state, emission vs light.
var material := StandardMaterial3D.new()
var reference: StandardMaterial3D
var left: MeshInstance3D
var right: MeshInstance3D
var point_light := OmniLight3D.new()
var shared := false

func _ready() -> void:
	setup("B04 / C05｜材质与共享", "先固定光照只调左球，再切换共享。预测右球会不会改变。")
	camera.position = Vector3(5, 4, 7)
	camera.fov = 45
	camera.look_at(Vector3(-1.2, 0.8, 0))
	material.albedo_color = Color("dca55f")
	material.roughness = 0.4
	material.emission_enabled = true
	material.emission = Color("ffc155")
	material.emission_energy_multiplier = 0
	reference = material.duplicate() as StandardMaterial3D
	left = ball(Vector3(-1.2, 1, 0), material)
	right = ball(Vector3(1.5, 1, 0), reference)
	stage.add_child(point_light)
	point_light.position = Vector3(-1.2, 2, 0)
	point_light.omni_range = 4
	point_light.light_color = Color("ffc155")
	point_light.visible = false
	slider("roughness", "粗糙度 Roughness", 0, 1, 0.4, 0.05, func(v): material.roughness = v; refresh())
	slider("metallic", "金属度 Metallic", 0, 1, 0, 0.05, func(v): material.metallic = v; refresh())
	slider("emission", "自发光 Emission", 0, 4, 0, 0.1, func(v): material.emission_energy_multiplier = v; refresh())
	toggle("shared", "两球使用同一份材质", false, set_shared)
	toggle("light", "另开真实灯光（不是自发光）", false, func(v): point_light.visible = v; refresh())
	button("color", "只改左球所引用材质的颜色", func(): material.albedo_color = Color("689bb8"); refresh())
	text("关闭共享：右球恢复固定参考。球的位置始终独立。这里不启用GI/Glow，不把表面发亮说成照亮地面。")
	refresh()

func ball(at: Vector3, mat: StandardMaterial3D) -> MeshInstance3D:
	var result := MeshInstance3D.new()
	var mesh := SphereMesh.new()
	mesh.radius = 0.8
	mesh.height = 1.6
	result.mesh = mesh
	result.material_override = mat
	stage.add_child(result)
	result.position = at
	return result

func set_shared(value: bool) -> void:
	shared = value
	right.material_override = material if value else reference
	refresh()

func refresh() -> void:
	status.text = "左球：粗糙 %.2f / 金属 %.2f\n同一资源 %s | 灯光 %s\n右球粗糙 %.2f" % [material.roughness, material.metallic, str(left.material_override == right.material_override), str(point_light.visible), right.material_override.roughness]
