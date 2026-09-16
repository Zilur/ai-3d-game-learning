"""Check production sources, ready geometry and routes; never grades learners."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import runpy
import struct
import tempfile

ROOT = Path(__file__).resolve().parents[1]
ASSETS = {'cottage', 'broadleaf', 'pine', 'rock_cluster', 'flower_patch', 'bridge',
          'fence', 'lantern', 'signpost', 'training_dummy', 'lookout_deck', 'beacon'}


def require(ok: bool, detail: str) -> None:
    if not ok:
        raise ValueError(detail)


def main() -> None:
    folder = ROOT / 'game/assets/village'
    manifest = json.loads((folder / 'manifest.json').read_text(encoding='utf-8'))
    records = manifest['assets']
    require({Path(r['file']).stem for r in records} == ASSETS and len(records) == 12,
            'exact production inventory required')
    generator = runpy.run_path(str(ROOT / 'tools/build_world_assets.py'))
    # Rebuild only into a temporary directory, never repair a bad ready asset silently.
    with tempfile.TemporaryDirectory() as temp:
        save = generator['Model'].save
        save.__globals__['DEST'] = Path(temp)
        for name, model in generator['models']().items():
            model.save(name)
            require((folder / (name + '.glb')).read_bytes() == (Path(temp) / (name + '.glb')).read_bytes(),
                    'ready GLB differs from deterministic author source: ' + name)
    triangles = 0
    for record in records:
        path = folder / record['file']
        data = path.read_bytes()
        require(hashlib.sha256(data).hexdigest() == record['sha256'], 'asset digest: ' + path.name)
        magic, version, length, jsize, jtype = struct.unpack('<5I', data[:20])
        require((magic, version, length, jtype) == (0x46546C67, 2, len(data), 0x4E4F534A), 'GLB header')
        gltf = json.loads(data[20:20+jsize])
        require(gltf['asset']['version'] == '2.0' and len(gltf['meshes']) == 1, 'ready glTF scene')
        require(all('uri' not in b for b in gltf['buffers']) and 'images' not in gltf, 'no hidden remote texture/buffer dependency')
        for prim in gltf['meshes'][0]['primitives']:
            attrs = prim['attributes']
            require({'POSITION', 'NORMAL'} <= attrs.keys(), 'geometry and normals')
            require(gltf['accessors'][attrs['POSITION']]['count'] % 3 == 0, 'triangle geometry')
        triangles += record['triangles']
    bindings = runpy.run_path(str(ROOT / 'curriculum/authoring/novice_learning.py'))['BINDINGS']
    expected = {'E01': 'navigation_lab', 'E03': 'shader_lab', 'E05': 'large_scene_lab', 'C08': 'effects_lab'}
    for ident, stem in expected.items():
        require('game/labs/' + stem + '.tscn' in bindings[ident][0], ident + ' missing real lab route')
        for suffix in ('.tscn', '.gd'):
            require((ROOT / ('game/labs/' + stem + suffix)).is_file(), stem + ' missing file')
    require('game/world/exploration.tscn' in bindings['D07'][0], 'D07 missing integrated game')
    require(not bindings['E06'][0], 'K-only E06 must not gain software requirement')
    require('run/main_scene="res://world/exploration.tscn"' in (ROOT / 'game/project.godot').read_text(), 'new main not selected')
    for name in ('WORLD-START.md', 'docs/production-validation.md', 'game/shaders/learning_surface.gdshader',
                 'game/world/stream_piece.tscn', 'game/tests/production_suite.gd', 'game/tests/save_roundtrip.gd'):
        require((ROOT / name).is_file(), 'missing production source: ' + name)
    require((ROOT / 'game/scenes/main.tscn').is_file(), 'old reference must remain')
    print(f'PRODUCTION SOURCE PASS: 12 deterministic ready GLBs, {triangles} triangles, four real lab routes, independent save test; not visual/mastery certification')


if __name__ == '__main__':
    main()
