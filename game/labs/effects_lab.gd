extends "res://labs/lab_shell.gd"
## Real native settings; DOF is explicitly unavailable on Compatibility.
var env: Environment
var attributes: CameraAttributesPractical
var dof_supported := false
var effect_state := {"fog": false, "glow": false, "dof": false}
func _ready() -> void:
	setup("C08｜雾、辉光与景深", "看近、中、远三排物体。保留全关基线，一次只启用一种效果，检查焦点与代价。")
	for child in get_children():
		if child is WorldEnvironment: env = child.environment
	env.background_color = Color("718c91")
	env.fog_light_color = Color("adc9c4")
	env.fog_density = 0.035
	env.glow_bloom = 0.15
	env.glow_intensity = 0.8
	env.glow_hdr_threshold = 1.0
	attributes = CameraAttributesPractical.new()
	attributes.dof_blur_near_distance = 10.0
	attributes.dof_blur_far_distance = 16.0
	attributes.dof_blur_near_transition = 2
	attributes.dof_blur_far_transition = 3
	attributes.dof_blur_amount = 0.2
	camera.attributes = attributes
	camera.position = Vector3(4, 3.4, 9)
	camera.look_at(Vector3(-1.8, 1, -5))
	camera.far = 100
	dof_supported = RenderingServer.get_current_rendering_method() != "gl_compatibility"
	box(stage, "LongGround", Vector3(1, -0.2, -10), Vector3(12, 0.2, 26), Color("7f927a"))
	for z in [0.0, -6.0, -14.0]:
		for x in [0.0, 3.0, 5.0]:
			box(stage, "Pillar", Vector3(x, 0.9, z), Vector3(0.6, 1.8, 0.6), Color("ddb986"))
			var top := box(stage, "Emitter", Vector3(x, 2, z), Vector3(0.7, 0.4, 0.7), Color("ffcd65"))
			var m := top.material_override as StandardMaterial3D
			m.emission_enabled = true
			m.emission = Color("ffbf50")
			m.emission_energy_multiplier = 4.0
	button("baseline", "全部效果关闭（保留数值）", baseline)
	for key in ["fog", "glow", "dof"]:
		var t := toggle(key, {"fog": "Fog 普通深度雾", "glow": "Glow 高亮辉光", "dof": "景深：近远失焦"}[key], false, set_effect.bind(key))
		if key == "dof": t.disabled = not dof_supported
	slider("density", "雾密度", 0, 0.1, 0.035, 0.005, func(v): env.fog_density = v)
	slider("glow_intensity", "辉光强度", 0, 2, 0.8, 0.1, func(v): env.glow_intensity = v)
	var focus := slider("focus", "焦点距离（米）", 5, 24, 13, 0.5, set_focus)
	var blur := slider("blur", "景深模糊强度", 0, 0.5, 0.2, 0.05, func(v): attributes.dof_blur_amount = v)
	focus.editable = dof_supported
	blur.editable = dof_supported
	text("Compatibility可看普通雾与本版本辉光；景深必须用Forward+或Mobile，当前不支持时控件禁用。切换渲染器需要重启场景；不以假模糊代替。体积雾是另一项技术，不混作普通雾。")
	refresh_status()
func set_effect(value: bool, key: String) -> void:
	if key == "dof" and not dof_supported: value = false
	effect_state[key] = value
	env.fog_enabled = effect_state.fog
	env.glow_enabled = effect_state.glow
	attributes.dof_blur_near_enabled = effect_state.dof
	attributes.dof_blur_far_enabled = effect_state.dof
	refresh_status()
func baseline() -> void:
	for key in effect_state:
		controls[key].set_pressed_no_signal(false)
		set_effect(false, key)
func set_focus(value: float) -> void:
	attributes.dof_blur_near_distance = maxf(0, value - 3)
	attributes.dof_blur_far_distance = value + 3
func refresh_status() -> void:
	status.text = "实际渲染器：%s\n雾 %s / 辉光 %s / 景深 %s\n景深支持：%s" % [RenderingServer.get_current_rendering_method(), str(effect_state.fog), str(effect_state.glow), str(effect_state.dof), str(dof_supported)]
