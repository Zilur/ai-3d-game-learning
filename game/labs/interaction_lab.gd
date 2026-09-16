extends "res://labs/lab_shell.gd"
## Real Area3D detection, conditional interaction and bounded local teaching save file.
const SAVE_PATH := "user://teaching_interaction_lab_v1.json"
var actor: CharacterBody3D
var area: Area3D
var hinge: Node3D
var door_shape: CollisionShape3D
var has_key := false
var opened := false
var volume := 0.7
var target_x := -3.0
var message := "移动到蓝色检测区，再尝试开门"
var x_control: HSlider

func _ready() -> void:
	setup("C06 / C10 / C11｜门与存档", "先区分靠近、允许开门、门的状态；再体验保存、读取和损坏文件。所有写入只在本实验专用文件。")
	actor = CharacterBody3D.new()
	actor.name = "Actor"
	actor.collision_layer = 2
	actor.collision_mask = 1
	stage.add_child(actor)
	actor.position = Vector3(-3, 0.5, 0)
	shape(actor, Vector3(0.6, 1, 0.6))
	box(actor, "Visual", Vector3.ZERO, Vector3(0.6, 1, 0.6), Color("e7ba4b"))
	area = Area3D.new()
	area.name = "DoorSensor"
	area.collision_layer = 0
	area.collision_mask = 2
	stage.add_child(area)
	area.position = Vector3(0.3, 0.6, 0)
	shape(area, Vector3(2.4, 1.8, 2.2))
	box(stage, "SensorFloor", Vector3(0.3, 0.02, 0), Vector3(2.4, 0.05, 2.2), Color("75bfd0"))
	hinge = Node3D.new()
	hinge.name = "DoorPivot"
	stage.add_child(hinge)
	hinge.position = Vector3(1.5, 0, -0.9)
	box(hinge, "DoorVisual", Vector3(0, 1, 0.9), Vector3(0.2, 2, 1.8), Color("a57649"))
	var wall := StaticBody3D.new()
	wall.collision_layer = 1
	wall.collision_mask = 0
	stage.add_child(wall)
	wall.position = Vector3(1.5, 1, 0)
	door_shape = shape(wall, Vector3(0.2, 2, 1.8))
	x_control = slider("position", "角色目标位置", -3, 3, -3, 0.1, func(v): target_x = v)
	toggle("key", "拥有钥匙", false, func(v): has_key = v; refresh())
	button("open", "尝试开门", try_open)
	slider("volume", "偏好示意值（不播放声音）", 0, 1, volume, 0.1, func(v): volume = v; refresh())
	button("save", "保存门进度和偏好", save_state)
	button("load", "读取：先检查数据，再改变场景", load_state)
	button("corrupt", "制造本实验坏档（不是你的游戏存档）", func(): write_fixture("broken"))
	button("old", "制造可迁移的v0旧档", func(): write_fixture("old"))
	button("missing", "仅删除本实验文件，测试缺档", func(): write_fixture("missing"))
	text("临时位置、靠近提示不保存。钥匙/门属于进度，偏好值单独分类。恢复初值不删除本实验文件。正式产品还需迁移、备份和多设备验证。")
	refresh()

func _physics_process(_delta: float) -> void:
	if not is_instance_valid(actor):
		return
	var difference := target_x - actor.position.x
	actor.velocity = Vector3(signf(difference) * minf(3, absf(difference) * 20), 0, 0)
	actor.move_and_slide()
	refresh()

func nearby() -> bool:
	return actor in area.get_overlapping_bodies()

func try_open() -> void:
	if opened:
		message = "已经打开；重复操作不重复执行"
	elif not nearby():
		message = "还未检测到角色靠近"
	elif not has_key:
		message = "已靠近，但缺少钥匙"
	else:
		opened = true
		message = "条件满足，门打开"
		apply_door()
	refresh()

func apply_door() -> void:
	hinge.rotation.y = -PI / 2 if opened else 0.0
	door_shape.set_deferred("disabled", opened)

func save_state() -> bool:
	var data := {"version": 1, "progress": {"key": has_key, "door": opened}, "preferences": {"volume": volume}}
	var file := FileAccess.open(SAVE_PATH + ".tmp", FileAccess.WRITE)
	if file == null:
		message = "写入失败，旧文件未改"
		refresh()
		return false
	file.store_string(JSON.stringify(data))
	file.flush()
	file.close()
	var result := DirAccess.rename_absolute(SAVE_PATH + ".tmp", SAVE_PATH)
	message = "保存完成：进度/偏好分开，临时位置不保存" if result == OK else "替换失败，保留现状"
	refresh()
	return result == OK

func load_state() -> bool:
	if not FileAccess.file_exists(SAVE_PATH):
		message = "没有本实验存档：保持当前场景，可以继续"
		refresh()
		return false
	var file := FileAccess.open(SAVE_PATH, FileAccess.READ)
	if file == null or file.get_length() > 4096:
		message = "文件不可读或过大：不应用"
		refresh()
		return false
	var decoder := JSON.new()
	var parse_result := decoder.parse(file.get_as_text())
	file.close()
	if parse_result != OK:
		message = "坏档：拒绝应用，当前状态不变"
		refresh()
		return false
	var data = decoder.data
	var migrated := false
	if data is Dictionary and version_is(data, 0) and data.get("door") is bool:
		data = {"version": 1, "progress": {"key": data["door"], "door": data["door"]}, "preferences": {"volume": 0.7}}
		migrated = true
	if not valid_data(data):
		message = "坏档或未知版本：拒绝应用，当前状态不变"
		refresh()
		return false
	has_key = data["progress"]["key"]
	opened = data["progress"]["door"]
	volume = float(data["preferences"]["volume"])
	controls["key"].set_pressed_no_signal(has_key)
	controls["volume"].set_value_no_signal(volume)
	apply_door()
	message = "已迁移v0；可重新保存成v1" if migrated else "读取成功；临时位置未被覆盖"
	refresh()
	return true

func version_is(data: Dictionary, expected: int) -> bool:
	var version = data.get("version")
	return (version is float or version is int) and is_finite(float(version)) and version == expected

func valid_data(data: Variant) -> bool:
	if not data is Dictionary or not version_is(data, 1):
		return false
	var progress = data.get("progress")
	var preferences = data.get("preferences")
	if not progress is Dictionary or not preferences is Dictionary:
		return false
	if not progress.get("key") is bool or not progress.get("door") is bool:
		return false
	var value = preferences.get("volume")
	return (value is float or value is int) and is_finite(float(value)) and value >= 0 and value <= 1

func write_fixture(kind: String) -> void:
	if kind == "missing":
		if FileAccess.file_exists(SAVE_PATH):
			var result := DirAccess.remove_absolute(SAVE_PATH)
			if result != OK:
				message = "删除失败：原文件仍保留"
				refresh()
				return
	else:
		var file := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
		if file == null:
			message = "无法准备本实验文件"
			refresh()
			return
		file.store_string("{bad json" if kind == "broken" else '{"version":0,"door":true}')
		file.close()
	message = "已准备 %s；请先预测再点读取" % kind
	refresh()

func refresh() -> void:
	status.text = "靠近 %s | 钥匙 %s | 门开 %s\n偏好 %.1f | 临时X %.2f\n%s" % [str(nearby()), str(has_key), str(opened), volume, actor.position.x, message]
