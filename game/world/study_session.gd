extends Node
## In-memory study handoff. No automatic disk writes or learner-history access.
const Store = preload("res://world/save_store.gd")
var suspended: Dictionary = {}
var panel: HBoxContainer
var resume_button: Button
var leave_dialog: ConfirmationDialog
var pending_quit := false

func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	get_tree().auto_accept_quit = false
	var canvas := CanvasLayer.new()
	canvas.layer = 80
	add_child(canvas)
	panel = HBoxContainer.new()
	panel.set_anchors_and_offsets_preset(Control.PRESET_TOP_RIGHT)
	panel.position = Vector2(-350, 12)
	panel.add_theme_constant_override("separation", 8)
	canvas.add_child(panel)
	var font := SystemFont.new()
	font.font_names = PackedStringArray(["Noto Sans CJK SC", "Microsoft YaHei", "PingFang SC"])
	var theme := Theme.new()
	theme.default_font = font
	theme.default_font_size = 17
	panel.theme = theme
	resume_button = _button("继续刚才的游戏", resume_world)
	_button("实验目录", func(): get_tree().change_scene_to_file("res://labs/lab_hub.tscn"))
	leave_dialog = ConfirmationDialog.new()
	leave_dialog.title = "游戏暂存尚未写入磁盘"
	leave_dialog.dialog_text = "暂存中有未保存的游戏变化。保存失败会留在这里。"
	leave_dialog.ok_button_text = "保存游戏后退出"
	leave_dialog.cancel_button_text = "取消"
	leave_dialog.add_button("不保存并退出", false, "discard")
	leave_dialog.dialog_hide_on_ok = false
	leave_dialog.confirmed.connect(_save_and_quit)
	leave_dialog.custom_action.connect(func(action):
		if action == "discard": get_tree().quit())
	leave_dialog.canceled.connect(func(): pending_quit = false)
	leave_dialog.theme = theme
	canvas.add_child(leave_dialog)
	# Only explicit automated delivery arguments activate the packaged test harness.
	for mode in ["write", "read", "render"]:
		if OS.get_cmdline_user_args().has("--delivery-check=" + mode):
			var probe = preload("res://tests/delivery_probe.gd").new()
			add_child(probe)
			probe.call_deferred("run", mode)
			break

func _button(caption: String, callback: Callable) -> Button:
	var button := Button.new()
	button.text = caption
	button.custom_minimum_size.y = 36
	button.pressed.connect(callback)
	panel.add_child(button)
	return button

func _process(_delta: float) -> void:
	var scene := get_tree().current_scene
	panel.visible = scene != null and not scene.is_in_group("production_world")
	resume_button.visible = not suspended.is_empty()

func retain(world: Node) -> void:
	suspended = {"scene": world.scene_file_path, "data": world.snapshot().duplicate(true),
		"baseline": world.saved_snapshot.duplicate(true), "save_path": world.store.file_path}

func restore(world: Node) -> bool:
	if suspended.is_empty() or world.scene_file_path != suspended.scene: return false
	if not world.apply_snapshot(suspended.data): return false
	world.saved_snapshot = suspended.baseline.duplicate(true)
	world.store.file_path = suspended.save_path
	suspended.clear()
	return true

func resume_world() -> void:
	if suspended.is_empty(): return
	get_tree().paused = false
	# Clear the handoff only after the target world has restored it successfully.
	var error := get_tree().change_scene_to_file(suspended.scene)
	if error != OK:
		leave_dialog.dialog_text = "无法打开暂存对应的场景，暂存仍保留。"
		leave_dialog.popup_centered(Vector2i(550, 190))

func has_unsaved() -> bool:
	return not suspended.is_empty() and suspended.data != suspended.baseline

func save_suspended() -> bool:
	if suspended.is_empty(): return true
	var store := Store.new()
	store.file_path = suspended.save_path
	var result: Dictionary = store.write_snapshot(suspended.data)
	if result.ok:
		suspended.baseline = suspended.data.duplicate(true)
	else:
		leave_dialog.dialog_text = result.message + "\n未退出；暂存仍保留。"
	return result.ok

func _save_and_quit() -> void:
	if pending_quit and save_suspended(): get_tree().quit()

func _notification(what: int) -> void:
	if what != NOTIFICATION_WM_CLOSE_REQUEST: return
	var scene := get_tree().current_scene
	if scene != null and scene.is_in_group("production_world"):
		scene.request_action("quit")
	elif has_unsaved():
		pending_quit = true
		leave_dialog.dialog_text = "暂存中有未保存的游戏变化。保存失败会留在这里。"
		leave_dialog.popup_centered(Vector2i(550, 190))
	else:
		get_tree().quit()
