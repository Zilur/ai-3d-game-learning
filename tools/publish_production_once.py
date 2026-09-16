"""One-time integrity-checked publication of approved native teaching code.
Never reads learner data; stages exact source/derived files; never force-pushes.
Remove this file and its one-time workflow after publication.
"""
from __future__ import annotations
import argparse
import base64
import hashlib
import json
import lzma
import os
from pathlib import Path
import subprocess
import urllib.request

REPO = 'Zilur/ai-3d-game-learning'
BASE = 'https://api.github.com/repos/' + REPO
PARTS = (
    'f1606ca8e8b2c8cb4e8311cec61f19de07397678',
    'dfa2360eca21042c30fe1657e1f5e155d51ea712',
    'fe67fe97df030951015e97b8e72977503062d273',
    '0ecdf484f35312b261549524695a1a077a01b299',
    '0fc3bea4e29f4dc6b1358e7e7abb77929c610efe',
    '908396defdb7258c8a093d337b2ee1d1cf9f9e0a',
)
DIGEST = '7c99b652c93dd6a53f4aa18a253025765c1765c281da3d1e2217d7a8cf24df6b'
SOURCES = set('''FAMILY-START.md
WORLD-START.md
curriculum/authoring/novice_learning.py
curriculum/authoring/ready_lab_pages.py
docs/production-validation.md
game/assets/village/LICENSE.txt
game/assets/village/README.md
game/labs/effects_lab.gd
game/labs/effects_lab.tscn
game/labs/lab_hub.gd
game/labs/large_scene_lab.gd
game/labs/large_scene_lab.tscn
game/labs/navigation_lab.gd
game/labs/navigation_lab.tscn
game/labs/shader_lab.gd
game/labs/shader_lab.tscn
game/project.godot
game/shaders/learning_surface.gdshader
game/tests/capture_production.gd
game/tests/practical_labs.gd
game/tests/production_suite.gd
game/tests/save_roundtrip.gd
game/world/adventure_player.gd
game/world/exploration.gd
game/world/exploration.tscn
game/world/save_store.gd
game/world/stream_piece.tscn
learning-system/README.md
tools/build_world_assets.py
tools/check_effect_captures.py
tools/check_production.py
tools/install_godot_desktop_ci.py
tools/run_production_checks.py'''.splitlines())
ASSETS = {'game/assets/village/' + name + '.glb' for name in (
    'cottage', 'broadleaf', 'pine', 'rock_cluster', 'flower_patch', 'bridge',
    'fence', 'lantern', 'signpost', 'training_dummy', 'lookout_deck', 'beacon')}


def request(path: str) -> dict:
    req = urllib.request.Request(BASE + path, headers={
        'Authorization': 'Bearer ' + os.environ['GH_TOKEN'],
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28'})
    with urllib.request.urlopen(req, timeout=45) as response:
        return json.load(response)


def check_path(name: str) -> None:
    p = Path(name)
    assert not p.is_absolute() and '..' not in p.parts and not any(x.startswith('.') for x in p.parts), name
    assert p.is_file() and not p.is_symlink(), name
    assert p.suffix in ('.py', '.md', '.json', '.txt', '.gd', '.tscn', '.tres', '.godot', '.gdshader', '.glb'), name


def apply() -> None:
    data = b''
    for sha in PARTS:
        blob = request('/git/blobs/' + sha)
        assert blob['encoding'] == 'base64'
        part = base64.b64decode(blob['content'])
        assert hashlib.sha1(b'blob ' + str(len(part)).encode() + b'\0' + part).hexdigest() == sha
        data += part
    assert len(data) == 40620 and hashlib.sha256(data).hexdigest() == DIGEST, 'payload digest mismatch'
    decoder = lzma.LZMADecompressor()
    raw = decoder.decompress(data, max_length=200001)
    assert decoder.eof and not decoder.unused_data and len(raw) == 129442, 'payload size mismatch'
    text = raw.decode('utf-8')
    targets = [line[6:] for line in text.splitlines() if line.startswith('+++ b/')]
    assert len(targets) == len(SOURCES) and set(targets) == SOURCES, 'unexpected patch paths'
    origins = [line[4:] for line in text.splitlines() if line.startswith('--- ')]
    assert len(origins) == len(SOURCES) and all(x == '/dev/null' or x.startswith('a/') and x[2:] in SOURCES for x in origins)
    patch = Path(os.environ['RUNNER_TEMP']) / 'approved-production.patch'
    patch.write_bytes(raw)
    subprocess.run(['git', 'apply', '--check', str(patch)], check=True)
    subprocess.run(['git', 'apply', str(patch)], check=True)
    print('APPLIED: 33 integrity-checked public source files; no generated classroom or personal data')


def publish() -> None:
    manifest_path = 'curriculum/materials-manifest.json'
    manifest = json.loads(Path(manifest_path).read_text(encoding='utf-8'))
    assert manifest['lesson_count'] == 47
    generated = set(manifest['sha256'])
    allowed = SOURCES | ASSETS | generated | {manifest_path, 'game/assets/village/manifest.json'}
    for name in allowed:
        check_path(name)
    for name, digest in manifest['sha256'].items():
        assert hashlib.sha256(Path(name).read_bytes()).hexdigest() == digest, name
    changed = set(subprocess.check_output(['git', 'diff', '--name-only'], text=True).splitlines())
    assert changed <= allowed, 'unexpected tracked modification: ' + repr(changed - allowed)
    assert request('/git/ref/heads/main')['object']['sha'] == os.environ['GITHUB_SHA'], 'main moved; refusing stale publish'
    subprocess.run(['git', 'add', '--'] + sorted(allowed), check=True)
    staged = set(subprocess.check_output(['git', 'diff', '--cached', '--name-only'], text=True).splitlines())
    assert staged and staged <= allowed
    subprocess.run(['git', 'diff', '--cached', '--check'], check=True)
    subprocess.run(['git', 'config', 'user.name', 'Course Builder'], check=True)
    subprocess.run(['git', 'config', 'user.email', 'course-builder@users.noreply.github.com'], check=True)
    subprocess.run(['git', 'commit', '-m', 'feat: integrate three-zone game, persistent saves, combat and four native electives'], check=True)
    env = os.environ.copy()
    auth = base64.b64encode(('x-access-token:' + os.environ['GH_TOKEN']).encode()).decode()
    env.update(GIT_CONFIG_COUNT='1', GIT_CONFIG_KEY_0='http.https://github.com/.extraheader',
               GIT_CONFIG_VALUE_0='AUTHORIZATION: basic ' + auth)
    subprocess.run(['git', 'push', 'origin', 'HEAD:refs/heads/main'], check=True, env=env)
    print('PUBLISHED:', subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip())


if __name__ == '__main__':
    assert os.environ.get('GITHUB_REPOSITORY') == REPO and os.environ.get('GITHUB_REF') == 'refs/heads/main'
    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=('apply', 'publish'))
    args = parser.parse_args()
    {'apply': apply, 'publish': publish}[args.phase]()
