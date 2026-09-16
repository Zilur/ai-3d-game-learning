"""Check ready-file routing and fixture structure; not runtime or learner grading."""
from __future__ import annotations
import base64
import json
from pathlib import Path
import runpy
import struct
import sys

ROOT = Path(__file__).resolve().parents[1]

def require(ok, detail):
    if not ok:
        raise ValueError(detail)

def validate_mesh(mesh):
    require(mesh.get('asset', {}).get('version') == '2.0', 'glTF version')
    require(len(mesh.get('skins', [])) >= 1, 'missing real skin')
    require(len(mesh['skins'][0]['joints']) >= 5, 'missing teaching bones')
    attrs = mesh['meshes'][0]['primitives'][0]['attributes']
    require({'POSITION','NORMAL','JOINTS_0','WEIGHTS_0'} <= attrs.keys(), 'missing weighted geometry')
    names = {a['name'] for a in mesh.get('animations', [])}
    require({'Idle','Walk','Attack'} <= names, 'three named clips required')
    for skin in mesh['skins']:
        require(all(type(i) is int and 0 <= i < len(mesh['nodes']) for i in skin['joints']), 'bone index invalid')
    return True

def validate_bindings(bindings, order, root=ROOT):
    require(len(order) == 47 and set(bindings) == set(order), '47 canonical IDs required')
    for ident, binding in bindings.items():
        require(len(binding) == 4 and all(binding[i] for i in (1,2,3)), 'missing first/limit/production')
        for name in binding[0]:
            p = Path(name)
            require(not p.is_absolute() and '..' not in p.parts and name.startswith(('game/','blender/')), 'unsafe resource path')
            require((root/p).is_file(), 'ready resource missing: ' + name)
    require(not bindings['E06'][0], 'K-only lesson cannot gain a required software lab')

def main():
    order = runpy.run_path(str(ROOT/'tools/course_order.py'))['ORDER']
    bindings = runpy.run_path(str(ROOT/'curriculum/authoring/novice_learning.py'))['BINDINGS']
    validate_bindings(bindings, order)
    published = json.loads((ROOT/'curriculum/lab-bindings.json').read_text())['bindings']
    for ident, (paths, first, limits, production) in bindings.items():
        require(published[ident] == dict(paths=paths,first=first,limits=limits,production=production), 'stale published binding')
    original = json.loads((ROOT/'game/assets/practice_robot.gltf').read_text())
    validate_mesh(original)
    expected = runpy.run_path(str(ROOT/'tools/make_practice_robot.py'))['build']()
    require(original == expected, 'fixture does not match its original author source')
    raw = base64.b64decode(original['buffers'][0]['uri'].split(',',1)[1], validate=True)
    require(len(raw) == original['buffers'][0]['byteLength'], 'fixture buffer length')
    for view in original['bufferViews']:
        require(0 <= view.get('byteOffset',0) <= view.get('byteOffset',0)+view['byteLength'] <= len(raw), 'fixture buffer bounds')
    glb = (ROOT/'game/assets/practice_robot_roundtrip.glb').read_bytes()
    magic, version, length, json_size, kind = struct.unpack('<5I', glb[:20])
    require(magic == 0x46546C67 and version == 2 and length == len(glb) and kind == 0x4E4F534A, 'invalid Blender roundtrip GLB')
    validate_mesh(json.loads(glb[20:20+json_size]))
    for name in ('transform_origin_lab.blend','kitbash_style_lab.blend','uv_material_lab.blend','animation_fixture.blend'):
        require((ROOT/'blender/labs'/name).stat().st_size > 10_000, 'missing/empty ready blend')
    require('LABS-START.md' in (ROOT/'README.md').read_text(), 'missing main entry')
    require('lab_hub.tscn' in (ROOT/'game/scripts/main.gd').read_text(), 'missing in-game entry')
    require('practical_labs.gd' in (ROOT/'.github/workflows/lab-readiness.yml').read_text(), 'runtime assertions not in CI')
    print('READY LAB MAP PASS: 47 bindings; 4 .blend files; original and Blender-roundtrip skin/animation; no mastery claim')

if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
