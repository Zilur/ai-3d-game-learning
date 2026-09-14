extends Node3D
## C16: the level owns progress; UI only displays it.

const STAR_SCENE: PackedScene = preload("res://scenes/star.tscn")
@export_range(0, 10, 1) var star_count: int = 10
var collected_count: int = 0
var total_stars: int = 0
var completed: bool = false
var seen_ids: Dictionary = {}
@onready var stars: Node3D = $Stars
@onready var counter: Label = $HUD/Panel/VBox/Counter
@onready var status_label: Label = $HUD/Panel/VBox/Status

func _ready() -> void:
	var positions: Array[Vector3] = [
		Vector3(0, 1, 1), Vector3(-2, 1, -1), Vector3(2, 1, -1),
		Vector3(-4, 1, -3), Vector3(0, 1, -3), Vector3(4.5, 1, -1),
		Vector3(3, 1.8, -6), Vector3(-2, 1.5, -5),
		Vector3(-4, 1, -7), Vector3(0, 1, -8)
	]
	for index in range(clampi(star_count, 0, positions.size())):
		var star = STAR_SCENE.instantiate()
		star.name = "Star%02d" % index
		star.pickup_id = str(star.name)
		star.position = positions[index]
		star.collected.connect(_on_star_collected)
		stars.add_child(star)
	total_stars = stars.get_child_count()
	_refresh_ui()

func _on_star_collected(pickup_id: String) -> void:
	# Defensive at the level boundary too; do not trust duplicate events.
	if pickup_id.is_empty() or seen_ids.has(pickup_id):
		return
	seen_ids[pickup_id] = true
	collected_count = seen_ids.size()
	_refresh_ui()

func _refresh_ui() -> void:
	completed = collected_count == total_stars
	counter.text = "%d / %d" % [collected_count, total_stars]
	if total_stars == 0:
		status_label.text = "No stars in this test level. R to restart."
	elif completed:
		status_label.text = "Complete! R to restart."
	elif collected_count > 0:
		status_label.text = "Collected! Find the next star."
	else:
		status_label.text = "Find all stars. Try the ramp and platform."

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		if event.physical_keycode == KEY_R:
			_restart()

func _restart() -> void:
	get_tree().reload_current_scene()

func _open_lab() -> void:
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	get_tree().change_scene_to_file("res://scenes/lab.tscn")
