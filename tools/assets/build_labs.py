"""Build small Blender concept labs. Run with Blender 5.2 LTS in background mode.

Example:
  blender --background --python tools/assets/build_labs.py -- --output-dir practice/blender

The generated .blend files are teaching artifacts, not final game assets.
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector


def parse_args() -> argparse.Namespace:
    argv = sys.argv
    argv = argv[argv.index("--") + 1 :] if "--" in argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="practice/blender")
    return parser.parse_args(argv)


def reset_scene() -> None:
    bpy.ops.wm.read_factory_settings(use_empty=True)


def make_material(name: str, rgb: tuple[float, float, float], roughness: float = 0.85, metallic: float = 0.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    mat.diffuse_color = (*rgb, 1.0)
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Metallic"].default_value = metallic
    return mat


def link_to_collection(obj, collection) -> None:
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    collection.objects.link(obj)


def add_cube(name, location, dimensions, material=None, collection=None, apply_scale=True):
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dimensions
    if apply_scale:
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if material:
        obj.data.materials.append(material)
    if collection:
        link_to_collection(obj, collection)
    return obj


def add_uv_sphere(name, location, scale, material=None, collection=None):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if material:
        obj.data.materials.append(material)
    if collection:
        link_to_collection(obj, collection)
    return obj


def add_cylinder(name, location, radius, depth, material=None, vertices=16, collection=None):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=location)
    obj = bpy.context.object
    obj.name = name
    if material:
        obj.data.materials.append(material)
    if collection:
        link_to_collection(obj, collection)
    return obj


def add_pyramid_roof(name, location, radius, depth, material=None, collection=None):
    bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=radius, radius2=0.0, depth=depth, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.rotation_euler.z = math.radians(45)
    if material:
        obj.data.materials.append(material)
    if collection:
        link_to_collection(obj, collection)
    return obj


def add_text(body, location, size=0.42, collection=None):
    bpy.ops.object.text_add(location=location, rotation=(math.radians(90), 0, 0))
    obj = bpy.context.object
    obj.data.body = body
    obj.data.align_x = "CENTER"
    obj.data.size = size
    obj.data.extrude = 0.005
    if collection:
        link_to_collection(obj, collection)
    return obj


def point_camera(camera, target):
    direction = Vector(target) - camera.location
    camera.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def setup_camera(target=(0, 0, 1.2), location=(0, -18, 8.5), lens=52.0):
    bpy.ops.object.camera_add(location=location)
    camera = bpy.context.object
    camera.name = "LAB_Camera"
    camera.data.lens = lens
    point_camera(camera, target)
    bpy.context.scene.camera = camera
    return camera


def setup_world():
    world = bpy.context.scene.world or bpy.data.worlds.new("World")
    bpy.context.scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs["Color"].default_value = (0.07, 0.09, 0.10, 1.0)
        bg.inputs["Strength"].default_value = 0.45
    bpy.ops.object.light_add(type="AREA", location=(-4, -6, 9))
    key = bpy.context.object
    key.name = "LAB_Key"
    key.data.energy = 900
    key.data.shape = "DISK"
    key.data.size = 7
    point_camera(key, (0, 0, 1.0))
    bpy.ops.object.light_add(type="AREA", location=(5, -2, 5))
    fill = bpy.context.object
    fill.name = "LAB_Fill"
    fill.data.energy = 280
    fill.data.size = 5
    point_camera(fill, (0, 0, 1.0))


def save(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(path.resolve()))


def build_transform_origin(path: Path):
    reset_scene()
    setup_world()
    setup_camera(target=(0, 0, 1.1), location=(0, -18, 7.5), lens=55)

    wood = make_material("Wood", (0.55, 0.28, 0.13), 0.82)
    accent = make_material("PivotMarker", (0.95, 0.28, 0.12), 0.65)
    cool = make_material("Cool", (0.24, 0.56, 0.72), 0.72)
    warm = make_material("Warm", (0.90, 0.66, 0.22), 0.76)

    add_text("Origin / Pivot: same door, different rotation center", (0, 0.3, 5.0), 0.48)
    add_text("Door_Center: drag Rotation Z", (-4.0, 0.25, 3.8), 0.30)
    add_text("Door_Hinge: drag Rotation Z", (4.0, 0.25, 3.8), 0.30)

    center = add_cube("Door_Center", (-4.0, 0, 1.7), (2.4, 0.22, 3.4), wood)
    center.rotation_euler.z = math.radians(28)
    add_uv_sphere("Center_Pivot_Marker", (-4.0, -0.25, 1.7), (0.12, 0.12, 0.12), accent)

    hinge = add_cube("Door_Hinge", (2.8, 0, 1.7), (2.4, 0.22, 3.4), wood)
    bpy.context.view_layer.objects.active = hinge
    hinge.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.transform.translate(value=(1.2, 0, 0))
    bpy.ops.object.mode_set(mode="OBJECT")
    hinge.rotation_euler.z = math.radians(28)
    add_uv_sphere("Hinge_Pivot_Marker", (2.8, -0.25, 1.7), (0.12, 0.12, 0.12), accent)

    add_text("Applied vs Unapplied Scale", (0, 0.25, -0.1), 0.38)
    unapplied = add_cube("Scale_Unapplied", (-2.4, 0, -1.45), (2, 2, 2), cool, apply_scale=True)
    unapplied.scale = (1.8, 0.55, 0.8)
    applied = add_cube("Scale_Applied", (2.4, 0, -1.45), (2, 2, 2), warm, apply_scale=True)
    applied.scale = (1.8, 0.55, 0.8)
    bpy.context.view_layer.objects.active = applied
    applied.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    add_text("same visible size; inspect Object Scale + Dimensions", (0, 0.25, -2.8), 0.27)

    bpy.context.scene["LAB_INSTRUCTIONS"] = (
        "Select Door_Center and Door_Hinge and drag Rotation Z. Then compare Scale_Unapplied and Scale_Applied. "
        "This lab demonstrates cause/effect only; do not blindly Apply Transform on rigged production assets."
    )
    save(path)


def build_kitbash_style(path: Path):
    reset_scene()
    setup_world()
    setup_camera(target=(0, 0, 1.4), location=(0, -20, 10), lens=58)

    ground_mat = make_material("Ground", (0.34, 0.52, 0.30), 0.94)
    wall_a = make_material("Wall_Base", (0.74, 0.66, 0.49), 0.88)
    wall_b = make_material("Wall_Variant", (0.78, 0.70, 0.51), 0.92)
    roof_a = make_material("Roof_Base", (0.50, 0.23, 0.14), 0.84)
    roof_b = make_material("Roof_Variant", (0.63, 0.27, 0.16), 0.89)
    wood = make_material("Wood", (0.34, 0.20, 0.11), 0.90)
    leaf = make_material("Leaf", (0.27, 0.50, 0.25), 0.96)
    stone = make_material("Stone", (0.47, 0.50, 0.45), 0.93)
    accent = make_material("Accent", (0.93, 0.68, 0.20), 0.78)

    add_cube("Ground", (0, 0, -0.18), (14, 8, 0.35), ground_mat)
    add_text("Kitbash + style lab: keep / modify / do not do", (0, 0.2, 5.2), 0.50)

    base_col = bpy.data.collections.new("BASE_KIT")
    var_col = bpy.data.collections.new("VARIANT_KIT")
    bpy.context.scene.collection.children.link(base_col)
    bpy.context.scene.collection.children.link(var_col)

    x = -3.6
    add_text("BASE", (x, 0.3, 4.1), 0.42, base_col)
    add_cube("Base_Wall", (x, 0, 1.35), (4.2, 3.2, 2.7), wall_a, base_col)
    add_pyramid_roof("Base_Roof", (x, 0, 3.2), 3.0, 1.9, roof_a, base_col)
    add_cube("Base_Door", (x, -1.63, 0.95), (0.9, 0.16, 1.9), wood, base_col)
    add_cube("Base_Window", (x + 1.1, -1.65, 1.65), (0.7, 0.12, 0.7), accent, base_col)

    x = 3.6
    add_text("VARIANT: select pieces and drag Dimensions / Scale", (x, 0.3, 4.1), 0.31, var_col)
    add_cube("Variant_Wall", (x, 0, 1.45), (4.5, 3.4, 2.9), wall_b, var_col)
    roof = add_pyramid_roof("Variant_Roof", (x, 0, 3.5), 3.3, 2.1, roof_b, var_col)
    roof.scale.x = 1.08
    add_cube("Variant_Door", (x - 0.55, -1.73, 1.0), (1.0, 0.16, 2.0), wood, var_col)
    add_cube("Variant_Window", (x + 1.0, -1.75, 1.75), (0.9, 0.12, 0.8), accent, var_col)
    add_cube("Variant_Awning", (x - 0.55, -2.0, 2.15), (1.6, 0.75, 0.18), roof_b, var_col)
    add_cylinder("Variant_Chimney", (x + 1.25, 0.35, 4.1), 0.22, 1.5, stone, 12, var_col)

    for tx, tz, s in [(-5.7, 1.0, 1.0), (5.9, 1.15, 1.15)]:
        add_cylinder("Tree_Trunk", (tx, 0.6, 0.8), 0.18 * s, 1.5 * s, wood, 12)
        add_uv_sphere("Tree_Crown", (tx, 0.6, 2.0), (0.95 * s, 0.82 * s, 0.95 * s), leaf)

    add_text("Try one variable at a time: roof proportion -> module -> Base Color -> Roughness", (0, 0.3, -0.8), 0.28)
    add_text("Keep the same camera/light while comparing. More detail is not automatically better.", (0, 0.3, -1.5), 0.26)

    bpy.context.scene["LAB_INSTRUCTIONS"] = (
        "Compare BASE_KIT and VARIANT_KIT. Change one visible relationship at a time: proportion, module, palette, material. "
        "Return to Godot at real player distance before accepting a change."
    )
    save(path)


def main() -> int:
    args = parse_args()
    out = Path(args.output_dir)
    build_transform_origin(out / "transform_origin_lab.blend")
    build_kitbash_style(out / "kitbash_style_lab.blend")
    print("BLENDER LAB BUILD PASS", bpy.app.version_string)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
