"""Run in Blender's Text Editor, in Object Mode. Adds ONE original star.
No files are saved/exported automatically and no existing objects are deleted.
"""
import math
import bpy

NAME = "LearningStar"
if bpy.context.mode != "OBJECT":
    raise RuntimeError("Switch to Object Mode before running this script.")
if bpy.data.objects.get(NAME) is not None:
    raise RuntimeError("LearningStar already exists. Rename it or use a new file; nothing overwritten.")

vertices = []
for depth in (0.08, -0.08):
    for index in range(10):
        angle = math.pi * index / 5
        radius = 0.5 if index % 2 == 0 else 0.23
        x, y = radius * math.sin(angle), radius * math.cos(angle)
        # Godot-style (x,y,z) -> Blender (x,-z,y): preserve handedness, Z up.
        vertices.append((x, -depth, y))
vertices.extend(((0, -0.08, 0), (0, 0.08, 0)))
faces = []
for index in range(10):
    nxt = (index + 1) % 10
    faces.extend(((20, nxt, index), (21, 10 + index, 10 + nxt),
                  (index, nxt, 10 + nxt), (index, 10 + nxt, 10 + index)))

mesh = bpy.data.meshes.new(NAME + "Mesh")
mesh.from_pydata(vertices, [], faces)
mesh.update()
star = bpy.data.objects.new(NAME, mesh)
bpy.context.collection.objects.link(star)
material = bpy.data.materials.new(NAME + "Paint")
material.use_nodes = True
principled = next(node for node in material.node_tree.nodes if node.type == "BSDF_PRINCIPLED")
principled.inputs["Base Color"].default_value = (1.0, 0.55, 0.08, 1.0)
principled.inputs["Metallic"].default_value = 0.0
principled.inputs["Roughness"].default_value = 0.4
mesh.materials.append(material)
for obj in bpy.context.selected_objects:
    obj.select_set(False)
star.select_set(True)
bpy.context.view_layer.objects.active = star
print("Created LearningStar: 22 vertices, 40 triangles; Z up. Save a copy and export selected GLB manually.")
