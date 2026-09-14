#!/usr/bin/env python3
"""Copy the user-requested official Skill as a pinned, verified reference. Never execute it."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'openmaic/vendor/THU-MAIC-OpenMAIC'
COMMIT = 'ee7a7b64df9abbccf939e109ae850e63bc075392'
FILES = {
 'skills/openmaic/SKILL.md':'7b5346d6a92b1265b62b22e5adddd6fcf7733d8f',
 'skills/openmaic/references/clone.md':'783b16b10429c397c2c6fe2585c503e588e2e294',
 'skills/openmaic/references/extend-cookbook.md':'9c61133a1791f9c3f8c911730eaaf541f7a0a829',
 'skills/openmaic/references/extend-sdk.md':'beb09694f8d4ae78192f48a2866453d61d447da7',
 'skills/openmaic/references/extend.md':'d0f23ea92c36a81d57b6dc834646bf00a6b14d18',
 'skills/openmaic/references/generate-flow.md':'209e48621706a715d83ed30bf6aa977a7ce39387',
 'skills/openmaic/references/live-demo.md':'88dfb662583f0c931b42b04b7188c12ddbd5ad7f',
 'skills/openmaic/references/provider-keys.md':'d971611fb03058bd91378f4bc4b562df5e61380c',
 'skills/openmaic/references/startup-modes.md':'d9cd30131c86bb22f56dbc1d669ad6b4718a314f',
 'LICENSE':'76abc5f13261e94fc0382b33ac8c101555288083',
}

def blob_sha(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

def main():
    metadata = {'repository':'THU-MAIC/OpenMAIC','commit':COMMIT,'license':'MIT (this subtree only)', 'files':[]}
    for source, expected in FILES.items():
        rel = source.removeprefix('skills/openmaic/')
        target = DEST / rel
        url = f'https://raw.githubusercontent.com/THU-MAIC/OpenMAIC/{COMMIT}/{source}'
        if target.exists() and blob_sha(target.read_bytes()) == expected:
            data = target.read_bytes()
        else:
            request = urllib.request.Request(url, headers={'User-Agent':'ai-3d-course-reference-vendor'})
            with urllib.request.urlopen(request, timeout=45) as response:
                data = response.read(200000)
            if blob_sha(data) != expected:
                raise RuntimeError(f'Upstream reference hash mismatch: {source}')
            data.decode('utf-8')
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        metadata['files'].append({'path':rel,'source':url,'git_blob_sha':expected,'sha256':hashlib.sha256(data).hexdigest()})
    DEST.mkdir(parents=True, exist_ok=True)
    (DEST / 'UPSTREAM.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('VENDOR PASS: 10 original files verified; not executed; project license unchanged')

if __name__ == '__main__':
    main()
