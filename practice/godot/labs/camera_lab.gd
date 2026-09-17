extends "res://labs/lab_shell.gd"
## Real Camera3D projection and input basis. No simulated FOV arithmetic.
var actor: MeshInstance3D
var orthographic := false
var view_fov := 50.0
var view_size := 12.0
var yaw := 25.0
var camera_relative := true
var fov_control: HSlider
var size_control: HSlider

func _ready() -> void:
	setup("A08｜固定镜头实验", "同一场景切换透视/正交，只调当前投影的视野。再比较按‘向右’时的方向。")
	for z in [-3.0, 0.0, 3.0]:
		box(stage, "SameSize", Vector3(0, 0.75, z), Vector3(1.5, 1.5, 1.5), Color("d6a55d"))
	actor = box(stage, "Probe", Vector3(3, 0.35, 0), Vector3(0.5, 0.7, 0.5), Color("448bba"))
	toggle("projection", "正交 Orthographic", false, set_projection_mode)
	fov_control = slider("fov", "透视 FOV（度）", 35, 70, view_fov, 1, func(v): view_fov = v; apply_view())
	size_control = slider("size", "正交 Size（单位）", 8, 18, view_size, 0.5, func(v): view_size = v; apply_view())
	slider("yaw", "固定机位预设角度（非自由环绕）", -35, 45, yaw, 5, func(v): yaw = v; apply_view())
	toggle("relative", "按镜头的地面方向移动", true, func(v): camera_relative = v; apply_view())
	button("right", "让蓝块向右走一步", func(): move_probe(Vector2.RIGHT))
	button("forward", "让蓝块向前走一步", func(): move_probe(Vector2(0, -1)))
	button("home", "只让蓝块回到起点", func(): actor.position = Vector3(3, 0.35, 0); apply_view())
	text("三块黄色方块尺寸相同。机位、投影、移动基准分开观察；本场景不包含切镜区域系统。")
	apply_view()

func set_projection_mode(value: bool) -> void:
	orthographic = value
	apply_view()

func apply_view() -> void:
	camera.position = Vector3(sin(deg_to_rad(yaw)) * 13, 7, cos(deg_to_rad(yaw)) * 13)
	camera.look_at(Vector3(-1.8, 0.6, 0))
	camera.projection = Camera3D.PROJECTION_ORTHOGONAL if orthographic else Camera3D.PROJECTION_PERSPECTIVE
	camera.fov = view_fov
	camera.size = view_size
	if is_instance_valid(fov_control):
		fov_control.editable = not orthographic
	if is_instance_valid(size_control):
		size_control.editable = orthographic
	status.text = "%s | FOV %.0f | Size %.1f\n蓝块位置：%s" % ["正交：调Size" if orthographic else "透视：调FOV", camera.fov, camera.size, actor.position]

func movement(axes: Vector2) -> Vector3:
	if not camera_relative:
		return Vector3(axes.x, 0, axes.y).limit_length(1)
	var right := camera.global_basis.x
	var back := camera.global_basis.z
	right.y = 0
	back.y = 0
	return (right.normalized() * axes.x + back.normalized() * axes.y).limit_length(1)

func move_probe(axes: Vector2) -> void:
	actor.position += movement(axes)
	actor.position.x = clampf(actor.position.x, -5, 5)
	actor.position.z = clampf(actor.position.z, -4, 4)
	apply_view()
