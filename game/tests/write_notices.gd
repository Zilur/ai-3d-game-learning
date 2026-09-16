extends SceneTree
func _initialize() -> void:
	var dest := OS.get_environment("EXPORT_NOTICE_PATH")
	if dest.is_empty():quit(1);return
	var file := FileAccess.open(dest, FileAccess.WRITE)
	if file == null:quit(1);return
	file.store_string("Godot Engine and bundled third-party notices\n\n" + Engine.get_license_text() + "\n\n")
	file.store_string(JSON.stringify(Engine.get_copyright_info(), "\t") + "\n\n")
	var licenses := Engine.get_license_info()
	for key in licenses: file.store_string(str(key)+"\n"+str(licenses[key])+"\n\n")
	file.close()
	quit()
