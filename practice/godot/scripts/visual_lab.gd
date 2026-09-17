extends Node3D
## A small A/B lab for fixed-camera visual judgment. It is not a benchmark.

@onready var camera: Camera3D = $Camera3D
@onready var sun: DirectionalLight3D = $Sun
@onready var clutter: Node3D = $Clutter
@onready var status: Label = $HUD/Panel/VBox/Status
@onready var fov_slider: HSlider = $HUD/Panel/VBox/FOV
@onready var light_slider: HSlider = $HUD/Panel/VBox/Light

func _ready() -> void:
	fov_slider.value = camera.fov
	light_slider.value = sun.light_energy
	clutter.visible = false
	_refresh()

func _set_fov(value: float) -> void:
	camera.fov = clampf(value, 35.0, 70.0)
	_refresh()

func _set_light(value: float) -> void:
	sun.light_energy = clampf(value, 0.4, 2.0)
	_refresh()

func _set_clutter(enabled: bool) -> void:
	clutter.visible = enabled
	_refresh()

func _refresh() -> void:
	var density := "dense / noisy" if clutter.visible else "clean / breathing space"
	status.text = "FOV %.0f° | light %.1f | %s" % [camera.fov, sun.light_energy, density]

func _back() -> void:
	get_tree().change_scene_to_file("res://scenes/main.tscn")

func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		_back()
