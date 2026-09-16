"""Install pinned official Godot on a GitHub-hosted desktop runner; verify digest."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import tempfile
import urllib.request
import zipfile

VERSION = '4.7.2'
BASE = f'https://api.github.com/repos/godotengine/godot-builds/releases/tags/{VERSION}-stable'


def request(url: str):
    return urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'starlight-course-ci'}), timeout=120)


def main() -> None:
    if not os.environ.get('RUNNER_TEMP') or not os.environ.get('GITHUB_ENV'):
        raise RuntimeError('CI only; install the editor normally on a family computer')
    system = platform.system()
    suffix = {'Linux': 'linux.x86_64.zip', 'Windows': 'win64.exe.zip', 'Darwin': 'macos.universal.zip'}[system]
    asset_name = f'Godot_v{VERSION}-stable_{suffix}'
    with request(BASE) as f:
        release = json.load(f)
    asset = next(a for a in release['assets'] if a['name'] == asset_name)
    digest = asset.get('digest', '')
    if not digest.startswith('sha256:'):
        raise RuntimeError('No official asset SHA-256 digest')
    destination = Path(os.environ['RUNNER_TEMP']) / 'starlight-godot-desktop'
    destination.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as temp:
        archive = Path(temp) / 'godot.zip'
        with request(asset['browser_download_url']) as f, archive.open('wb') as out:
            shutil.copyfileobj(f, out)
        with archive.open('rb') as f:
            actual = hashlib.file_digest(f, 'sha256').hexdigest()
        if actual != digest.removeprefix('sha256:'):
            raise RuntimeError('Official Godot checksum mismatch')
        with zipfile.ZipFile(archive) as z:
            for name in z.namelist():
                target = (destination / name).resolve()
                if destination.resolve() not in target.parents and target != destination.resolve():
                    raise RuntimeError('Unsafe archive path')
            if system != 'Darwin':
                z.extractall(destination)
        if system == 'Darwin':
            subprocess.run(['ditto', '-xk', str(archive), str(destination)], check=True)
    if system == 'Darwin':
        binary = destination / 'Godot.app/Contents/MacOS/Godot'
    elif system == 'Windows':
        binary = destination / f'Godot_v{VERSION}-stable_win64_console.exe'
        if not binary.is_file():
            binary = destination / f'Godot_v{VERSION}-stable_win64.exe'
    else:
        binary = destination / f'Godot_v{VERSION}-stable_linux.x86_64'
    if not binary.is_file():
        raise RuntimeError('Expected engine executable missing')
    binary.chmod(0o755)
    with open(os.environ['GITHUB_ENV'], 'a', encoding='utf-8') as f:
        f.write('GODOT_BINARY=' + str(binary) + '\n')
    print('OFFICIAL DESKTOP ENGINE:', system, VERSION, asset_name, digest, binary)


if __name__ == '__main__':
    main()
