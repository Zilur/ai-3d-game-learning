extends SceneTree
## Two independent process invocations; uses only this dedicated test directory.
const STORE = preload("res://world/save_store.gd")
func _initialize()->void: call_deferred("run")
func run()->void:
	var args:=OS.get_cmdline_user_args()
	var store=STORE.new()
	store.file_path="user://production_test_only/cross_process.json"
	if args.has("write"):
		var data={"version":2,"collected":["courtyard_0","forest_2"],"checkpoint":"forest","has_key":true,"gate_open":false,"training_enabled":false,"training_hits":3,"low_motion":true,"volume":0.25}
		var result:Dictionary=store.write_snapshot(data)
		if not result.ok: push_error(result.message);quit(1);return
		print("SAVE ROUNDTRIP WRITE PASS")
	elif args.has("read"):
		var result:Dictionary=store.read_snapshot()
		if not result.ok: push_error(result.message);quit(1);return
		var data:Dictionary=result.data
		if data.collected!=["courtyard_0","forest_2"] or data.checkpoint!="forest" or not data.has_key or data.gate_open or data.training_enabled or data.training_hits!=3 or not is_equal_approx(data.volume,0.25):
			push_error("Cross-process save did not preserve the expected fields")
			quit(1);return
		print("SAVE ROUNDTRIP READ PASS: actual file from previous process")
	else:
		push_error("Use -- write and then -- read in separate invocations")
		quit(1);return
	quit()
