extends Area3D
## C15: a disappearing object is not, by itself, an exactly-once reward.

signal collected(pickup_id: String)
@export var pickup_id: String = ""
@export var spin_speed: float = 1.5
var consumed: bool = false
var elapsed: float = 0.0
@onready var visual: MeshInstance3D = $Visual

func _ready() -> void:
	if pickup_id.is_empty():
		pickup_id = str(name)
	body_entered.connect(_on_body_entered)

func _process(delta: float) -> void:
	elapsed += delta
	visual.rotation.y += spin_speed * delta
	# Animate the visual, not the detection region.
	visual.position.y = sin(elapsed * 2.0) * 0.12

func _on_body_entered(body: Node3D) -> void:
	try_collect(body)

func try_collect(body: Node) -> bool:
	if consumed or not is_instance_valid(body) or not body.is_in_group("player"):
		return false
	# Lock synchronously BEFORE notifying listeners.
	consumed = true
	set_deferred("monitoring", false)
	$CollisionShape3D.set_deferred("disabled", true)
	collected.emit(pickup_id)
	queue_free()
	return true
