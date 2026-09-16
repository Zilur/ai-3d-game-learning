extends Resource
## Small, saved creative surface. Built-in inspector controls; no editor plugin needed.
@export_range(1.0, 10.0, 0.1) var walk_speed: float = 4.0
@export_range(1.0, 15.0, 0.1) var run_speed: float = 7.0
@export_range(2.0, 14.0, 0.1) var jump_velocity: float = 8.0
@export_range(8.0, 45.0, 0.1) var gravity: float = 24.0
@export_color_no_alpha var path_color: Color = Color("ceaf7d")

func problem() -> String:
	for entry in [[walk_speed, 1.0, 10.0], [run_speed, 1.0, 15.0], [jump_velocity, 2.0, 14.0], [gravity, 8.0, 45.0]]:
		if not is_finite(entry[0]) or entry[0] < entry[1] or entry[0] > entry[2]:
			return "体验参数超出当前练习范围。"
	if run_speed < walk_speed: return "跑速不能低于走速；先明确这次比较的目标。"
	for channel in [path_color.r, path_color.g, path_color.b]:
		if not is_finite(channel) or channel < 0 or channel > 1: return "道路颜色需为普通0–1色值。"
	return ""
