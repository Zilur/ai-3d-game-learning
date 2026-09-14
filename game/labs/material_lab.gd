extends Node3D
## C12/C13. A: adjustable material. B: fixed reference. No GI or glow is enabled.
var material := StandardMaterial3D.new()
var readout := Label.new()
var point_light := OmniLight3D.new()

func _ready() -> void:
    var camera := Camera3D.new()
    add_child(camera)
    camera.position = Vector3(0, 3.2, 7)
    camera.look_at(Vector3(0, 0.8, 0))
    camera.current = true
    var environment := WorldEnvironment.new()
    environment.environment = Environment.new()
    var sky := Sky.new()
    sky.sky_material = ProceduralSkyMaterial.new()
    environment.environment.background_mode = Environment.BG_SKY
    environment.environment.sky = sky
    add_child(environment)
    var sun := DirectionalLight3D.new()
    add_child(sun)
    sun.rotation_degrees = Vector3(-45, -30, 0)
    sun.shadow_enabled = true
    material.albedo_color = Color(0.9, 0.48, 0.12)
    material.roughness = 0.4
    material.emission_enabled = true
    material.emission = Color(1, 0.5, 0.1)
    material.emission_energy_multiplier = 0.0
    for i in range(2):
        var ball := MeshInstance3D.new()
        var mesh := SphereMesh.new()
        mesh.radius = 0.7
        mesh.height = 1.4
        ball.mesh = mesh
        ball.material_override = material if i == 0 else (material.duplicate() as StandardMaterial3D)
        add_child(ball)
        ball.position = Vector3(-1.3 + 2.6 * i, 0.8, 0)
    var floor_mesh := MeshInstance3D.new()
    var box := BoxMesh.new()
    box.size = Vector3(8, 0.1, 6)
    floor_mesh.mesh = box
    add_child(floor_mesh)
    add_child(point_light)
    point_light.position = Vector3(-1.3, 1.8, 0)
    point_light.light_color = Color(1, 0.5, 0.1)
    point_light.omni_range = 4.0
    point_light.visible = false
    var layer := CanvasLayer.new()
    add_child(layer)
    var panel := PanelContainer.new()
    layer.add_child(panel)
    panel.position = Vector2(16, 16)
    var rows := VBoxContainer.new()
    panel.add_child(rows)
    rows.add_child(readout)
    _slider(rows, "roughness", 0, 1, 0.4)
    _slider(rows, "metallic", 0, 1, 0)
    _slider(rows, "emission_energy_multiplier", 0, 4, 0)
    var light_switch := CheckButton.new()
    light_switch.text = "Add actual OmniLight (not emission)"
    rows.add_child(light_switch)
    light_switch.toggled.connect(func(value: bool): point_light.visible = value)
    var note := Label.new()
    note.text = "Left: variable | Right: fixed reference\nEmission != glow != lighting the floor.\nNo GI / glow in this lab. Reset: stop and press F6."
    rows.add_child(note)
    _update_text()

func _slider(parent: VBoxContainer, property: String, low: float, high: float, initial: float) -> void:
    var label := Label.new()
    label.text = property
    parent.add_child(label)
    var slider := HSlider.new()
    slider.min_value = low
    slider.max_value = high
    slider.step = 0.05
    slider.value = initial
    slider.custom_minimum_size = Vector2(370, 28)
    parent.add_child(slider)
    slider.value_changed.connect(func(value: float):
        material.set(property, value)
        _update_text())

func _update_text() -> void:
    readout.text = "A: rough %.2f / metal %.2f / emission %.2f" % [material.roughness,
        material.metallic, material.emission_energy_multiplier]
