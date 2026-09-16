"""CI-only install of exact official export templates, with digest verification."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import tempfile
import zipfile
from install_godot_desktop_ci import request, BASE, VERSION


def main():
    if not os.environ.get('RUNNER_TEMP'): raise RuntimeError('CI only; adults install matching export templates normally.')
    with request(BASE) as stream: release=json.load(stream)
    asset=next(a for a in release['assets'] if a['name']==f'Godot_v{VERSION}-stable_export_templates.tpz')
    digest=asset.get('digest','')
    if not digest.startswith('sha256:'):raise RuntimeError('Missing official SHA-256')
    system=platform.system()
    base={'Linux':Path.home()/'.local/share/godot', 'Windows':Path(os.environ.get('APPDATA',''))/'Godot', 'Darwin':Path.home()/'Library/Application Support/Godot'}[system]
    destination=base/'export_templates'/(VERSION+'.stable')
    destination.mkdir(parents=True,exist_ok=True)
    required={'Linux':['linux_release.x86_64'], 'Windows':['windows_release_x86_64.exe'], 'Darwin':['macos.zip']}[system]
    with tempfile.TemporaryDirectory() as temp:
        archive=Path(temp)/'templates.tpz'
        with request(asset['browser_download_url']) as src,archive.open('wb') as dst:shutil.copyfileobj(src,dst)
        with archive.open('rb') as src:actual=hashlib.file_digest(src,'sha256').hexdigest()
        if actual != digest[7:]:raise RuntimeError('Export template checksum mismatch')
        with zipfile.ZipFile(archive) as z:
            for name in required:
                with z.open('templates/'+name) as src,(destination/name).open('wb') as dst:shutil.copyfileobj(src,dst)
                (destination/name).chmod(0o755)
    print('VERIFIED EXPORT TEMPLATES:', VERSION, system, digest)

if __name__=='__main__':main()
