extends "res://labs/lab_shell.gd"
## A small observable system, not a quiz engine. Requests are injected, not collisions.
const HISTORY_LIMIT := 12
var count := 0
var taken := false
var guard_enabled := true
var feedback_enabled := true
var counter_visible := true
var visual_hidden := false
var mechanism_visible := false
var request_number := 0
var history: Array[Dictionary] = []
var token: MeshInstance3D
var feedback: MeshInstance3D
var counter_view: Label
var mechanism_view: Label
var message := "尚无请求。先选一个你想确认的问题。"

func _ready() -> void:
	setup("B06–B08｜物品、请求与记录", "规则：一枚物品，本局只允许角色领取一次。你可以先预测，再改变一个条件；解释不必一次说完整。")
	camera.position = Vector3(4, 4, 6)
	camera.fov = 42
	camera.look_at(Vector3(-1.4, 0.6, 0))
	token = box(stage, "Collectible", Vector3(0, 1.2, 0), Vector3(1.1, 1.1, 1.1), Color("f0c44c"))
	feedback = box(stage, "Feedback", Vector3(0, 0.12, 0), Vector3(2.5, 0.2, 2.5), Color("479776"))
	counter_view = text("")
	button("collect", "角色发出一次收集请求", func(): request_collect(true))
	button("double", "同一时刻连续请求两次", func(): request_collect(true); request_collect(true))
	button("wrong", "装饰球发出请求", func(): request_collect(false))
	toggle("counter", "显示计数", true, func(v): counter_visible = v; refresh())
	toggle("feedback", "显示成功反馈", true, func(v): feedback_enabled = v; refresh())
	toggle("visual", "暂时隐藏物品外观", false, func(v): visual_hidden = v; refresh())
	button("restart", "重开这局（保留实验设置）", restart_round)
	text("只选一个开关比较，不必全部试完。按钮明确注入请求，不代表Area碰撞。真实接近与拾取回到庭院验证。")
	toggle("mechanism", "查看内部记录与故障对照", false, func(v): mechanism_visible = v; refresh())
	toggle("guard", "一次性状态保护（关掉造故障）", true, func(v): guard_enabled = v; refresh())
	mechanism_view = text("")
	refresh()

func request_collect(is_player: bool) -> void:
	var before_count := count
	var before_taken := taken
	var accepted := false
	var reason: String
	if not is_player:
		reason = "不是允许的对象"
	elif taken and guard_enabled:
		reason = "本物品已经收集"
	else:
		taken = true
		count += 1
		accepted = true
		reason = "条件通过；先更新状态，再刷新表现"
	request_number += 1
	history.append({"number": request_number, "actor": "角色" if is_player else "装饰球",
		"before_count": before_count, "after_count": count,
		"before_taken": before_taken, "after_taken": taken,
		"accepted": accepted, "reason": reason, "guard": guard_enabled})
	if history.size() > HISTORY_LIMIT:
		history.pop_front()
	message = "请求已处理。把你看到的变化和预期比较；需要时展开内部记录。"
	refresh()

func restart_round() -> void:
	count = 0
	taken = false
	request_number = 0
	history.clear()
	message = "已重开，实验开关保留。预测下一次请求；恢复全部初值会同时恢复开关。"
	refresh()

func refresh() -> void:
	token.visible = not taken and not visual_hidden
	feedback.visible = taken and feedback_enabled
	counter_view.visible = counter_visible
	counter_view.text = "计数 %d" % count
	status.text = message
	controls["guard"].visible = mechanism_visible
	mechanism_view.visible = mechanism_visible
	var lines: PackedStringArray = ["当前实际状态：count=%d；taken=%s" % [count, str(taken)],
		"以下来自本次运行，最近%d条请求；开关本身不添加请求。" % HISTORY_LIMIT]
	for entry in history:
		lines.append("#%d %s：%s\ncount %d→%d；taken %s→%s；保护=%s\n%s" % [
			entry["number"], entry["actor"], "接受" if entry["accepted"] else "拒绝",
			entry["before_count"], entry["after_count"], str(entry["before_taken"]), str(entry["after_taken"]),
			str(entry["guard"]), entry["reason"]])
	mechanism_view.text = "\n\n".join(lines)
