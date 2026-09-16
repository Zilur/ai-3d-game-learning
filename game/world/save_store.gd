extends RefCounted
## Bounded, schema-checked and recoverable local snapshots. Never reads other saves.
const VERSION := 2
const MAX_BYTES := 65536
const CHECKPOINTS := ["courtyard", "forest", "lookout"]
const STAR_IDS := ["courtyard_0", "courtyard_1", "courtyard_2", "forest_0", "forest_1", "forest_2", "forest_3", "lookout_0", "lookout_1", "lookout_2"]
var file_path := "user://starlight_village_v1/save.json"

func invalid(message: String) -> Dictionary:
	return {"ok": false, "message": message, "data": {}}

func validate_snapshot(raw: Variant) -> Dictionary:
	if not raw is Dictionary: return invalid("存档不是对象；当前游戏未改变。")
	var data: Dictionary = raw.duplicate(true)
	if not data.has("version"): return invalid("没有版本信息。")
	if not (data.version is int or data.version is float) or not is_finite(float(data.version)) or float(data.version) != floorf(float(data.version)): return invalid("存档版本类型错误。")
	var migrated := false
	if data.version == 1:
		# Deliberate v1 fixture: same stable IDs, no settings yet.
		if not data.has_all(["collected", "checkpoint", "has_key", "gate_open"]): return invalid("旧存档字段不完整。")
		data.merge({"training_enabled": true, "training_hits": 0, "low_motion": true, "volume": 0.6}, false)
		data.version = VERSION
		migrated = true
	if data.version != VERSION: return invalid("不支持此存档版本；不会清空或覆盖它。")
	if not data.has_all(["collected", "checkpoint", "has_key", "gate_open", "training_enabled", "training_hits", "low_motion", "volume"]): return invalid("存档缺少必要字段。")
	if not data.collected is Array or data.collected.size() > STAR_IDS.size(): return invalid("收集记录不合法。")
	var unique := {}
	for id in data.collected:
		if not id is String or not STAR_IDS.has(id) or unique.has(id): return invalid("存在未知或重复的物品ID。")
		unique[id] = true
	if not data.checkpoint is String or not CHECKPOINTS.has(data.checkpoint): return invalid("检查点不合法。")
	for key in ["has_key", "gate_open", "training_enabled", "low_motion"]:
		if not data[key] is bool: return invalid("布尔字段类型错误：" + key)
	for key in ["training_hits", "volume"]:
		if not (data[key] is float or data[key] is int) or not is_finite(float(data[key])): return invalid("数值字段错误：" + key)
	if float(data.training_hits) < 0 or float(data.training_hits) > 1000000 or float(data.training_hits) != floorf(float(data.training_hits)): return invalid("训练计数越界。")
	if float(data.volume) < 0 or float(data.volume) > 1: return invalid("音量越界。")
	if data.gate_open and not data.has_key: return invalid("开门状态缺少钥匙前提。")
	if data.checkpoint == "lookout" and not data.gate_open: return invalid("观景台检查点与关门状态冲突。")
	var clean := {"version": VERSION, "collected": data.collected.duplicate(), "checkpoint": data.checkpoint,
		"has_key": data.has_key, "gate_open": data.gate_open, "training_enabled": data.training_enabled,
		"training_hits": int(data.training_hits), "low_motion": data.low_motion, "volume": float(data.volume)}
	return {"ok": true, "data": clean, "message": "已迁移v1；仅下次主动保存时写入v2。" if migrated else "已校验存档。", "migrated": migrated}

func _read(path: String) -> Dictionary:
	if not FileAccess.file_exists(path): return invalid("没有该存档；当前进度保持不变。")
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null: return invalid("无法读取存档。")
	if file.get_length() > MAX_BYTES:
		file.close()
		return invalid("存档过大；拒绝读取。")
	var text := file.get_as_text()
	file.close()
	var json := JSON.new()
	if json.parse(text) != OK: return invalid("存档损坏；可在暂停菜单尝试备份。")
	return validate_snapshot(json.data)

func read_snapshot(backup: bool = false) -> Dictionary:
	return _read(file_path + ".bak" if backup else file_path)

func write_snapshot(raw: Dictionary) -> Dictionary:
	var checked := validate_snapshot(raw)
	if not checked.ok: return checked
	var absolute := ProjectSettings.globalize_path(file_path)
	if DirAccess.make_dir_recursive_absolute(absolute.get_base_dir()) != OK: return invalid("无法创建存档目录。")
	var temp := absolute + ".tmp"
	var file := FileAccess.open(temp, FileAccess.WRITE)
	if file == null: return invalid("无法写入临时存档。")
	file.store_string(JSON.stringify(checked.data, "\t"))
	file.flush()
	var error := file.get_error()
	file.close()
	if error != OK or not _read(temp).ok:
		DirAccess.remove_absolute(temp)
		return invalid("临时文件未通过检查，旧存档保持不变。")
	var rotated := ""
	if FileAccess.file_exists(absolute):
		# A corrupt primary must never replace the last valid backup.
		rotated = absolute + (".bak" if _read(absolute).ok else ".rejected")
		if FileAccess.file_exists(rotated) and DirAccess.remove_absolute(rotated) != OK:
			DirAccess.remove_absolute(temp)
			return invalid("无法轮换备份；取消保存。")
		if DirAccess.rename_absolute(absolute, rotated) != OK:
			DirAccess.remove_absolute(temp)
			return invalid("无法备份旧存档；取消保存。")
	if DirAccess.rename_absolute(temp, absolute) != OK:
		if not rotated.is_empty(): DirAccess.rename_absolute(rotated, absolute)
		DirAccess.remove_absolute(temp)
		return invalid("无法替换存档，已尝试恢复旧文件。")
	return {"ok": true, "message": "进度已保存。继续时从最近到达的安全检查点恢复。", "data": checked.data}
