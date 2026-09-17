"""Export a Mac or Windows release, then test it without editor or source path.
Requires the pinned engine and matching installed export templates. No uploads.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import tempfile
import zipfile
ROOT = Path(__file__).resolve().parents[1]
SUPPORTED_TARGETS = {'Windows': ('Windows', 'Starlight.exe'), 'Darwin': ('macOS', 'Starlight-macOS.zip')}


def release_target(system: str) -> tuple[str, str]:
    if system not in SUPPORTED_TARGETS:
        raise ValueError('Standalone packages support macOS and Windows only.')
    return SUPPORTED_TARGETS[system]

ERRORS = re.compile(r'SCRIPT ERROR|Parse Error|ERROR:|DELIVERY FAILED|ObjectDB instances leaked|resources still in use')


def run(command, log, cwd, env=None, marker=None, timeout=300):
    log.parent.mkdir(parents=True, exist_ok=True)
    try:
        result = subprocess.run(command, cwd=cwd, env=env, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, text=True, encoding='utf-8',
                                errors='replace', timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        partial = exc.stdout or ''
        if isinstance(partial, bytes):
            partial = partial.decode('utf-8', 'replace')
        log.write_text(partial + '\nPROCESS TIMEOUT\n', encoding='utf-8')
        raise
    log.write_text(result.stdout, encoding='utf-8')
    encoding = getattr(__import__('sys').stdout, 'encoding', None) or 'utf-8'
    print(result.stdout.encode(encoding, 'backslashreplace').decode(encoding))
    if result.returncode or ERRORS.search(result.stdout) or marker and marker not in result.stdout:
        raise RuntimeError('Export/runtime check failed: ' + str(log))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--godot', default=os.environ.get('GODOT_BINARY', 'godot'))
    p.add_argument('--out', type=Path, default=Path('build/desktop'))
    a = p.parse_args()
    system = platform.system()
    preset, filename = release_target(system)
    license_path = ROOT / 'game/assets/village/LICENSE.txt'
    if not license_path.is_file():
        raise ValueError('Original asset license is missing; export refused.')
    out = a.out.resolve() / preset
    if out.exists():
        raise ValueError('Output exists; choose a new folder, never overwrite a package.')
    package = out / 'package'; package.mkdir(parents=True)
    evidence = out / 'evidence'; evidence.mkdir()
    run([a.godot, '--version'], evidence / 'version.log', ROOT, marker='4.7.2.stable')
    base = [a.godot, '--headless', '--audio-driver', 'Dummy', '--path', str(ROOT / 'game')]
    run(base + ['--editor', '--import'], evidence / 'import.log', ROOT)
    target = package / filename
    run(base + ['--export-release', preset, str(target)], evidence / 'export.log', ROOT)
    if system == 'Darwin':
        subprocess.run(['ditto', '-x', '-k', str(target), str(package)], check=True)
        target.unlink()
    notice = package / 'GODOT-THIRD-PARTY-NOTICES.txt'
    env = os.environ.copy(); env['EXPORT_NOTICE_PATH'] = str(notice)
    run(base + ['--script', 'res://tests/write_notices.gd'], evidence / 'notices.log', ROOT, env)
    if not notice.is_file() or notice.stat().st_size < 2000:
        raise RuntimeError('Engine notices were not generated; package is incomplete.')
    shutil.copy2(license_path, package / 'ASSET-LICENSE.txt')
    shutil.copy2(ROOT / 'game/assets/practice-asset-notes.md', package / 'PRACTICE-ASSET-NOTES.md')
    (package / 'README.txt').write_text(
        '星光小庭院｜亲子课程独立体验包\n\n'
        '解压整个目录，不要只移动exe或pck。Windows运行Starlight.exe；macOS打开.app。\n'
        '需要操作系统提供中文字体；不随包分发字体。WASD移动，Shift跑，空格跳，E交互，J训练，Esc暂停，F9保存，F10读档。\n'
        '窗口关闭和实验往返已有保存保护；内存暂存不是磁盘存档。仅教学试玩，未经商店签名/公证；遇系统拦截由成人核对来源并使用源码项目，不关闭系统安全保护。\n'
        '行为自动测试不等于所有设备、听感、儿童学习或商业品质已验收。\n', encoding='utf-8')
    if system == 'Darwin':
        apps = list(package.glob('*.app'))
        if len(apps) != 1: raise RuntimeError('Expected one exported app.')
        binaries = [x for x in (apps[0] / 'Contents/MacOS').iterdir() if x.is_file()]
        if len(binaries) != 1: raise RuntimeError('Expected one exported app executable.')
        binary = binaries[0]
    else:
        binary = target
    if os.name != 'nt': binary.chmod(binary.stat().st_mode | 0o111)
    # Only the package is copied. No --path, .godot editor cache, or loose source project.
    with tempfile.TemporaryDirectory(prefix='detached-starlight-') as temporary:
        detached = Path(temporary) / 'package'
        shutil.copytree(package, detached, symlinks=True)
        exe = detached / binary.relative_to(package)
        runtime_env = os.environ.copy()
        runtime_env['DELIVERY_CASE'] = 'case_' + preset.lower() + '_' + os.urandom(4).hex()
        for phase in ('write', 'read'):
            run([str(exe), '--headless', '--audio-driver', 'Dummy', '--fixed-fps', '60', '--', '--delivery-check=' + phase],
                evidence / (phase + '.log'), detached, runtime_env, 'EXPORTED DELIVERY ' + phase.upper() + ' PASS')
    files = {x.relative_to(package).as_posix(): hashlib.sha256(x.read_bytes()).hexdigest()
             for x in sorted(package.rglob('*')) if x.is_file()}
    (out / 'SHA256.json').write_text(json.dumps(files, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    archive = out / ('Starlight-' + preset + '.zip')
    if system == 'Darwin':
        # Preserve framework symlinks and application-bundle metadata.
        subprocess.run(['ditto', '-c', '-k', '--sequesterRsrc', '--keepParent', str(package), str(archive)], check=True)
    else:
        with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
            for file in sorted(package.rglob('*')):
                if file.is_file(): z.write(file, Path('Starlight-' + preset) / file.relative_to(package))
    print('STANDALONE EXPORT VERIFIED:', archive)


if __name__ == '__main__':
    main()
