extends Area3D
## C06/C07/C16: a trigger detects; it does not block. Exactly one event per star.
signal collected(star: Area3D)
@export_range(0.0, 180.0, 1.0) var spin_degrees_per_second: float = 65.0
var taken: bool = false

func _ready() -> void:
    body_entered.connect(try_collect)

func _process(delta: float) -> void:
    $Visual.rotate_y(deg_to_rad(spin_degrees_per_second) * delta)

func try_collect(body: Node3D) -> void:
    if taken or not body.is_in_group("player"):
        return
    taken = true
    set_deferred("monitoring", false)
    collected.emit(self)
    queue_free()
