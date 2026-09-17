extends "res://labs/lab_shell.gd"
## Buttons inject explicit events, not fake physics observations. One state source drives UI.
var count := 0
var taken := false
var guard_enabled := true
var feedback_enabled := true
var pending_restart := false
var token: MeshInstance3D
var feedback: MeshInstance3D
var message := "尚无请求"

func _ready() -> void:
	setup("B06–B08｜事件与状态", "一枚物品，只允许角色收集一次。预测重复请求、错误对象和重开后的结果。")
	camera.position = Vector3(4, 4, 6)
	camera.fov = 42
	camera.look_at(Vector3(-1.4, 0.6, 0))
	token = box(stage, "Collectible", Vector3(0, 1.2, 0), Vector3(1.1, 1.1, 1.1), Color("f0c44c"))
	feedback = box(stage, "Feedback", Vector3(0, 0.12, 0), Vector3(2.5, 0.2, 2.5), Color("479776"))
	button("collect", "角色发出一次收集请求", func(): request_collect(true))
	button("double", "同一时刻连续请求两次", func(): request_collect(true); request_collect(true))
	button("wrong", "装饰球发出请求", func(): request_collect(false))
	toggle("guard", "一次性状态保护（关掉造故障）", true, func(v): guard_enabled = v; refresh())
	toggle("feedback", "显示成功反馈", true, func(v): feedback_enabled = v; refresh())
	button("restart", "重开这局（保留实验设置）", restart_round)
	text("按钮是明确注入的事件。真实碰撞/重叠到事件的链路在碰撞实验和庭院中检查。隐藏物品本身不是一次性保护。")
	refresh()

func request_collect(is_player: bool) -> void:
	if not is_player:
		message = "拒绝：不是允许的对象"
	elif taken and guard_enabled:
		message = "拒绝：本物品已经收集"
	else:
		taken = true
		count += 1
		message = "接受请求，先改变状态，再刷新表现"
	refresh()

func restart_round() -> void:
	count = 0
	taken = false
	message = "本局重开；预测下一次计数"
	refresh()

func refresh() -> void:
	token.visible = not taken
	feedback.visible = taken and feedback_enabled
	status.text = "计数 %d | 已收集 %s\n%s\n显示来自同一个计数，关闭反馈不改计数。" % [count, str(taken), message]
