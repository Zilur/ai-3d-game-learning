extends Node3D
## B10/B12: UI is a view of the counter, not the source of game state.
var collected_count: int = 0
var total: int = 0
@onready var counter: Label = $HUD/Panel/Rows/Counter
@onready var stats: Label = $HUD/Panel/Rows/Stats

func _ready() -> void:
    for star in $Stars.get_children():
        star.connect("collected", _on_star_collected)
        total += 1
    _refresh_ui()

func _on_star_collected(_star: Area3D) -> void:
    collected_count += 1
    _refresh_ui()

func _refresh_ui() -> void:
    counter.text = "Stars: %d / %d" % [collected_count, total]
    if total > 0 and collected_count == total:
        counter.text += "   COMPLETE! Press R to restart."

func _process(_delta: float) -> void:
    var fps: float = Engine.get_frames_per_second()
    # This is reciprocal FPS, NOT GPU time or a measurement of an individual effect.
    var approx_ms: float = 1000.0 / maxf(fps, 1.0)
    stats.text = "FPS %.0f | 1000/FPS ~ %.1f ms (not GPU time)" % [fps, approx_ms]

func _unhandled_input(event: InputEvent) -> void:
    if event is InputEventKey and event.pressed and not event.echo and event.keycode == KEY_R:
        get_tree().reload_current_scene()
