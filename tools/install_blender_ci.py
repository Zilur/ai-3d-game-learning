"""CI-only official Blender 5.2.0 installer; verify SHA-256 before extraction."""
from __future__ import annotations
import hashlib
import os
from pathlib import Path
import shutil
import tarfile
import tempfile
import urllib.request

VERSION = '5.2.0'
BASE = 'https://download.blender.org/release/Blender5.2/'
ARCHIVE = f'blender-{VERSION}-linux-x64.tar.xz'

def request(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'course-lab-audit'}), timeout=180)

def main():
    if not os.environ.get('RUNNER_TEMP'):
        raise RuntimeError('CI-only installer; learners open ready .blend files in their installed Blender.')
    dest = Path(os.environ['RUNNER_TEMP']) / 'blender-verified'
    dest.mkdir(parents=True, exist_ok=True)
    with request(BASE + f'blender-{VERSION}.sha256') as response:
        rows = response.read().decode().splitlines()
    matches = [line.split()[0] for line in rows if line.split() and line.split()[-1].lstrip('*') == ARCHIVE]
    if len(matches) != 1:
        raise RuntimeError('Expected exactly one official Blender checksum')
    with tempfile.TemporaryDirectory(dir=dest) as td:
        package = Path(td) / ARCHIVE
        with request(BASE + ARCHIVE) as response, package.open('wb') as target:
            shutil.copyfileobj(response, target)
        with package.open('rb') as stream:
            digest = hashlib.file_digest(stream, 'sha256').hexdigest()
        if digest.lower() != matches[0].lower():
            raise RuntimeError('Blender checksum mismatch')
        with tarfile.open(package) as bundle:
            bundle.extractall(dest, filter='data')
    binary = dest / f'blender-{VERSION}-linux-x64' / 'blender'
    if not binary.is_file():
        raise RuntimeError('Official archive has unexpected structure')
    with open(os.environ['GITHUB_PATH'], 'a', encoding='utf-8') as stream:
        stream.write(str(binary.parent) + '\n')
    print('BLENDER VERIFIED:', VERSION, digest)

if __name__ == '__main__':
    main()
