"""One-time controlled publication of validated public teaching sources.
Remove after the approved source/assets and generated course pages are published.
Never reads learner records, never stages arbitrary files, never force-pushes.
"""
from __future__ import annotations
import argparse
import base64
import bz2
import hashlib
import json
import os
from pathlib import Path
import subprocess
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
REPO = 'Zilur/ai-3d-game-learning'
DIGEST = '058ec1d620f78a0d61387ffcb35c3c267b459f1267b3de39a03933285fe20e5e'
CHUNKS = [
    '6781a817528e40e6934917557d25ff76400f0e57',
    '655a52097d208fa093ae4f9075727ee8d4136ddd',
    '81cb21c88567d0aa08943f7f8080ead7849ef0cd',
    '82daa98d771c908bafa42c2f61b84d5b54dd2a24',
    '143569f9c2004d8ef6d40385be1f7564eaf0519d',
    'c881ab39604aadf3d99ad7358459fed91f803bc3',
    '16ef8bcf29fcbb06e871dd4015fc6cedb2375979',
    '00d8efe974c82ed9b4c6fd7e371661fb213c1fda',
]
ASSETS = {
    'game/assets/practice_robot.gltf',
    'game/assets/practice_robot_roundtrip.glb',
    'blender/labs/uv_material_lab.blend',
    'blender/labs/animation_fixture.blend',
}

def checked_path(name):
    path = Path(name)
    assert not path.is_absolute() and '..' not in path.parts
    assert not any(part.startswith('.') for part in path.parts)
    assert path.suffix.lower() not in ('.ttf', '.otf', '.woff', '.woff2')
    assert ROOT in (ROOT / path).resolve().parents
    return ROOT / path

def payload():
    token = os.environ.get('GH_TOKEN')
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'ready-lab-publisher'}
    if token:
        headers['Authorization'] = 'Bearer ' + token
    parts = []
    for sha in CHUNKS:
        req = urllib.request.Request('https://api.github.com/repos/' + REPO + '/git/blobs/' + sha, headers=headers)
        with urllib.request.urlopen(req, timeout=60) as response:
            item = json.load(response)
        assert item['encoding'] == 'base64'
        data = base64.b64decode(item['content'])
        assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == sha
        parts.append(data)
    data = bz2.decompress(b''.join(parts))
    assert len(data) == 153494 and hashlib.sha256(data).hexdigest() == DIGEST
    sources = json.loads(data)
    assert isinstance(sources, dict) and len(sources) == 31
    for name, text in sources.items():
        checked_path(name)
        assert isinstance(text, str)
        assert name == 'FAMILY-START.md' or name.startswith(('curriculum/authoring/', 'game/labs/', 'game/tests/', 'game/assets/', 'game/scripts/', 'tools/', 'learning-system/', 'blender/labs/', 'docs/'))
    return sources

def git(*args, env=None):
    return subprocess.check_output(['git', *args], cwd=ROOT, env=env, text=True).strip()

def apply(sources):
    for name, text in sources.items():
        path = checked_path(name)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')
    print('APPLIED VERIFIED PUBLIC SOURCES:', len(sources), DIGEST)

def publish(sources):
    assert os.environ['GITHUB_REPOSITORY'] == REPO
    assert os.environ['GITHUB_REF'] == 'refs/heads/main'
    expected = os.environ['GITHUB_SHA']
    assert git('rev-parse', 'HEAD') == expected
    manifest = json.loads((ROOT / 'curriculum/materials-manifest.json').read_text(encoding='utf-8'))
    allowed = set(sources) | set(manifest['sha256']) | ASSETS | {'curriculum/materials-manifest.json'}
    for name in allowed:
        assert checked_path(name).is_file(), name
    for name, digest in manifest['sha256'].items():
        assert hashlib.sha256(checked_path(name).read_bytes()).hexdigest() == digest, name
    changed = set(git('-c', 'core.quotepath=false', 'diff', '--name-only').splitlines())
    assert changed <= allowed, 'Unexpected tracked changes: ' + repr(changed - allowed)
    token = os.environ['GH_TOKEN']
    env = dict(os.environ)
    env.update(GIT_CONFIG_COUNT='1', GIT_CONFIG_KEY_0='http.https://github.com/.extraheader',
               GIT_CONFIG_VALUE_0='AUTHORIZATION: basic ' + base64.b64encode(('x-access-token:' + token).encode()).decode())
    assert git('ls-remote', 'origin', 'refs/heads/main', env=env).split()[0] == expected, 'main moved; stop without overwriting'
    subprocess.run(['git', 'add', '--', *sorted(allowed)], cwd=ROOT, check=True)
    staged = set(git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines())
    assert staged and staged <= allowed
    git('config', 'user.name', 'github-actions[bot]')
    git('config', 'user.email', '41898282+github-actions[bot]@users.noreply.github.com')
    git('commit', '-m', 'feat: ship ready native labs and synchronize all 47 lesson routes')
    subprocess.run(['git', 'push', 'origin', 'HEAD:refs/heads/main'], cwd=ROOT, env=env, check=True)
    print('PUBLISHED VALIDATED COMMIT:', git('rev-parse', 'HEAD'), 'paths:', len(staged))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['apply', 'publish'])
    args = parser.parse_args()
    assert os.environ.get('GITHUB_ACTIONS') == 'true', 'one-time CI helper only'
    sources = payload()
    apply(sources) if args.action == 'apply' else publish(sources)
