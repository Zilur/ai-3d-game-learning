"""Author-only: build ready UV/resource and rig/animation labs using Blender 5.2.
Learners open the committed .blend files, not this generator. No external assets.
Run: blender --background --python tools/assets/build_practical_labs.py
"""
from __future__ import annotations
import math
import os
import sys
from pathlib import Path
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'practice/blender'

def material(name, color):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    mat.diffuse_color = (*color, 1)
    node = mat.node_tree.nodes.get('Principled BSDF')
    node.inputs['Base Color'].default_value = (*color, 1)
    node.inputs['Roughness'].default_value = 0.8
    return mat

def cube(name, at, scale, mat):
    bpy.ops.mesh.primitive_cube_add(size=1, location=at)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(mat)
    return obj

def label(value, at, size=0.22):
    curve = bpy.data.curves.new('Label', 'FONT')
    curve.body = value
    curve.align_x = 'CENTER'
    curve.size = size
    obj = bpy.data.objects.new('Label_' + value, curve)
    bpy.context.collection.objects.link(obj)
    obj.location = at
    obj.rotation_euler.x = math.pi / 2
    mat = bpy.data.materials.get('Label_Unlit')
    if mat is None:
        mat = material('Label_Unlit', (1, 1, 1))
        node = mat.node_tree.nodes['Principled BSDF']
        node.inputs['Emission Color'].default_value = (1, 1, 1, 1)
        node.inputs['Emission Strength'].default_value = 1
    obj.data.materials.append(mat)
    return obj

def camera_and_light(at, target, ortho):
    bpy.ops.object.camera_add(location=at)
    cam = bpy.context.object
    cam.name = 'LAB_Camera'
    cam.rotation_euler = (Vector(target) - cam.location).to_track_quat('-Z', 'Y').to_euler()
    cam.data.type = 'ORTHO'
    cam.data.ortho_scale = ortho
    bpy.context.scene.camera = cam
    world = bpy.data.worlds.new('LAB_World')
    world.use_nodes = True
    world.node_tree.nodes['Background'].inputs['Color'].default_value = (0.24, 0.29, 0.31, 1)
    world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.5
    bpy.context.scene.world = world
    bpy.ops.object.light_add(type='AREA', location=(-3, -4, 7))
    lamp = bpy.context.object
    lamp.data.energy = 600
    lamp.data.size = 6
    lamp.rotation_euler = (Vector(target) - lamp.location).to_track_quat('-Z', 'Y').to_euler()
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'CPU'
    scene.cycles.samples = 12
    scene.render.resolution_x = 1000
    scene.render.resolution_y = 650
    scene.render.resolution_percentage = 100
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type == 'VIEW_3D':
                area.spaces.active.region_3d.view_perspective = 'CAMERA'
                area.spaces.active.shading.type = 'MATERIAL'

def help_text(content):
    doc = bpy.data.texts.new('START_HERE_中文说明')
    doc.write(content)
    bpy.context.scene['LAB_INSTRUCTIONS'] = content
    bpy.context.scene['LAB_VERSION'] = 'ready-labs-2026-09-16'

def save_and_render(name):
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT / name), compress=True)
    captures = os.environ.get('LAB_CAPTURE_DIR')
    if captures:
        path = Path(captures)
        path.mkdir(parents=True, exist_ok=True)
        bpy.context.scene.render.filepath = str(path / (Path(name).stem + '.png'))
        bpy.ops.render.render(write_still=True)

def uv_lab():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    checker = bpy.data.images.new('Packed_checker_8x8', width=64, height=64)
    pixels = []
    for y in range(64):
        for x in range(64):
            color = (0.84, 0.91, 0.88, 1) if ((x // 8 + y // 8) % 2) else (0.08, 0.21, 0.27, 1)
            pixels.extend(color)
    checker.pixels.foreach_set(pixels)
    checker.pack()
    mat = material('Shared_Checker_Material', (1, 1, 1))
    tex = mat.node_tree.nodes.new('ShaderNodeTexImage')
    tex.image = checker
    tex.interpolation = 'Closest'
    tex.extension = 'REPEAT'
    uv = mat.node_tree.nodes.new('ShaderNodeTexCoord')
    mat.node_tree.links.new(uv.outputs['UV'], tex.inputs['Vector'])
    mat.node_tree.links.new(tex.outputs['Color'], mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'])
    for index, (name, factor) in enumerate([('UV_Reference', (1, 1)), ('UV_Stretched', (3, 1)), ('UV_Dense', (2, 2))]):
        mesh = bpy.data.meshes.new(name + '_Mesh')
        mesh.from_pydata([(-1, 0, 0), (1, 0, 0), (1, 0, 2), (-1, 0, 2)], [], [(0, 1, 2, 3)])
        mesh.uv_layers.new(name='UVMap')
        for item, value in zip(mesh.uv_layers.active.data, [(0, 0), (factor[0], 0), factor, (0, factor[1])]):
            item.uv = value
        obj = bpy.data.objects.new(name, mesh)
        bpy.context.collection.objects.link(obj)
        obj.location.x = (index - 1) * 2.7
        mesh.materials.append(mat)
        label(name.replace('UV_', ''), (obj.location.x, -0.04, 2.25))
    shared = material('Shared_Green', (0.20, 0.54, 0.31))
    a = cube('Shared_A', (-2.7, 0, -0.8), (0.9, 0.8, 0.7), shared)
    b = bpy.data.objects.new('Shared_B', a.data)
    bpy.context.collection.objects.link(b)
    b.location = (0, 0, -0.8)
    c = bpy.data.objects.new('Independent_C', a.data.copy())
    bpy.context.collection.objects.link(c)
    c.location = (2.7, 0, -0.8)
    c.data.materials[0] = shared.copy()
    for x, name in [(-2.7, 'Shared A'), (0, 'Shared B'), (2.7, 'Independent C')]:
        label(name, (x, -0.05, -1.5))
    camera_and_light((0, -12, 5), (0, 0, 0.5), 10)
    bpy.ops.object.select_all(action='DESELECT')
    focus = bpy.data.objects['UV_Stretched']
    focus.select_set(True)
    bpy.context.view_layer.objects.active = focus
    help_text('C07：上排三块板的几何尺寸、材质和光照相同，只是UV不同。先预测，再在UV编辑工作区选UV_Stretched，只缩放UV的U方向，比较棋盘格是否恢复方形；不要改几何尺寸来掩盖问题。\nB04/C05：下排Shared_A与Shared_B共享网格和材质，Independent_C两者独立。先看数据名称/用户数，再只改A的一个顶点或材质；预测谁会一起变化。\n每次先另存副本。文件内纹理已打包，无需下载、脚本或插件。撤销恢复本次改动，或不保存关闭后重开原文件。菜单和快捷键可以查；本文件不是商业材质库。')
    save_and_render('uv_material_lab.blend')

def rig_lab():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(ROOT / 'practice/godot/assets/practice_robot.gltf'))
    rig = next(obj for obj in bpy.context.scene.objects if obj.type == 'ARMATURE')
    rig.show_in_front = True
    rig.data.display_type = 'STICK'
    bpy.context.scene.render.fps = 30
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = 30
    bpy.context.scene.frame_set(12)
    # Export while only the imported teaching rig is present. Keep imported stashed actions.
    bpy.ops.export_scene.gltf(filepath=str(ROOT / 'practice/godot/assets/practice_robot_roundtrip.glb'), export_format='GLB', export_animations=True, export_animation_mode='ACTIONS', export_yup=True)
    camera_and_light((3, -5, 3), (0, 0, 1), 3.8)
    bpy.ops.object.select_all(action='DESELECT')
    rig.select_set(True)
    bpy.context.view_layer.objects.active = rig
    help_text('C03/C04/D05：这是本项目原创的5骨骼方块角色，有真实蒙皮与Idle、Walk、Attack三段动作。无需自己建骨架或绑权重。\n先播放时间轴，再到非线性动画编辑器观察导入的三个NLA轨道，单独Solo一个轨道来切换动作；每次只启用一个，避免叠加。姿态模式可观察骨骼如何带动网格，不要求手工重做绑定。\n模型只演示资产结构与动作复用，不是最终角色、美术成品或通用重定向教程。Walk原地播放，不会自动移动Godot控制器。再打开Godot的animation_lab.tscn比较融合与命中条件。\n先另存副本；撤销或不保存重开恢复。随包GLB是同一原创角色经Blender导出后的回程样本，仍须在自己的工程验证尺寸、资源和功能。')
    save_and_render('animation_fixture.blend')

def verify():
    bpy.ops.wm.open_mainfile(filepath=str(OUT / 'uv_material_lab.blend'), load_ui=False)
    assert bpy.data.objects['Shared_A'].data == bpy.data.objects['Shared_B'].data
    assert bpy.data.objects['Shared_A'].data != bpy.data.objects['Independent_C'].data
    assert bpy.data.objects['Shared_A'].active_material == bpy.data.objects['Shared_B'].active_material
    assert bpy.data.objects['Shared_A'].active_material != bpy.data.objects['Independent_C'].active_material
    assert bpy.data.images['Packed_checker_8x8'].packed_file is not None
    spans = []
    for name in ('UV_Reference', 'UV_Stretched', 'UV_Dense'):
        mesh = bpy.data.objects[name].data
        coords = [item.uv[:] for item in mesh.uv_layers.active.data]
        spans.append((max(uv[0] for uv in coords), max(uv[1] for uv in coords)))
    assert spans == [(1, 1), (3, 1), (2, 2)], spans
    bpy.ops.wm.open_mainfile(filepath=str(OUT / 'animation_fixture.blend'), load_ui=False)
    rig = next(obj for obj in bpy.context.scene.objects if obj.type == 'ARMATURE')
    assert len(rig.data.bones) >= 5
    assert len(bpy.data.actions) >= 3
    meshes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
    assert any(any(mod.type == 'ARMATURE' for mod in obj.modifiers) and len(obj.vertex_groups) >= 5 for obj in meshes)
    for name in ('transform_origin_lab.blend', 'kitbash_style_lab.blend'):
        bpy.ops.wm.open_mainfile(filepath=str(OUT / name), load_ui=False)
        assert bpy.context.scene.camera is not None
        assert any(obj.type == 'MESH' for obj in bpy.context.scene.objects)
    print('BLENDER PRACTICAL PASS: four ready files reopened; UV, packed texture, shared data, bones, weights and clips checked;', bpy.app.version_string)

if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    if "--verify-only" not in sys.argv:
        uv_lab()
        rig_lab()
    verify()
