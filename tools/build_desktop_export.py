"""Export a real release, test it detached from sources, retain notices and checksums."""
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
import uuid
import zipfile

ROOT=Path(__file__).resolve().parents[1]
ERROR=re.compile(r'SCRIPT ERROR|Parse Error|ERROR:|DELIVERY FAILED|ObjectDB instances leaked')


def run(args, cwd, log, env=None, marker=None):
    result=subprocess.run([str(x) for x in args],cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace',timeout=420)
    log.parent.mkdir(parents=True,exist_ok=True);log.write_text(result.stdout,encoding='utf-8')
    print(result.stdout)
    if result.returncode or ERROR.search(result.stdout) or marker and marker not in result.stdout:raise RuntimeError('Failed: '+log.name)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--godot',required=True);p.add_argument('--output',type=Path,default=ROOT/'build/desktop');p.add_argument('--render',action='store_true')
    a=p.parse_args();system=platform.system();preset={'Linux':'Linux','Windows':'Windows','Darwin':'macOS'}[system]
    out=a.output.resolve()/preset
    if out.exists():raise RuntimeError('Output exists; choose a new folder, never overwrite a delivered build.')
    out.mkdir(parents=True);logs=out/'evidence';logs.mkdir()
    package=out/'package';package.mkdir()
    filename={'Linux':'Starlight.x86_64','Windows':'Starlight.exe','Darwin':'Starlight.zip'}[system]
    editor=Path(a.godot).resolve()
    run([editor,'--version'],ROOT,logs/'version.log',marker='4.7.2.stable')
    run([editor,'--headless','--path',ROOT/'game','--editor','--import'],ROOT,logs/'import.log')
    run([editor,'--headless','--path',ROOT/'game','--export-release',preset,package/filename],ROOT,logs/'export.log')
    env=os.environ.copy();env['EXPORT_NOTICE_PATH']=str(package/'ENGINE-NOTICES.txt')
    run([editor,'--headless','--path',ROOT/'game','--script','res://tests/write_notices.gd'],ROOT,logs/'notices.log',env)
    shutil.copy2(ROOT/'game/assets/village/LICENSE',package/'ASSET-LICENSE.txt')
    (package/'README.txt').write_text('星光小庭院｜独立体验包\n无需安装Godot；请完整解压目录，不单独移动可执行文件。\nWASD移动、Shift跑、空格跳、E交互、J可选训练、Esc菜单。F9保存、F10继续。\n实验可暂存接续，关闭进程前仍要保存。需要系统中文字体。\n这是未签名的教学测试包，不是商店发行；系统拦截时请由成人核对来源或从源工程自行构建，不关闭系统安全保护。\n学习记录不在本游戏包中。\n',encoding='utf-8')
    if system=='Darwin':
        subprocess.run(['ditto','-xk',str(package/filename),str(package)],check=True);(package/filename).unlink()
    executables=list(package.glob('*.app/Contents/MacOS/*')) if system=='Darwin' else [package/filename]
    binary=next(x for x in executables if x.is_file() and not x.name.startswith('.'))
    binary.chmod(0o755)
    # Actual exported executable/PCK alone in a temporary directory: no --path back to the repo.
    with tempfile.TemporaryDirectory(prefix='starlight-detached-') as d:
        detached=Path(d)/'package';shutil.copytree(package,detached,symlinks=True)
        executable=detached/binary.relative_to(package)
        env=os.environ.copy();env['DELIVERY_CASE']='case_'+uuid.uuid4().hex
        for mode in ['write','read']:
            run([executable,'--headless','--audio-driver','Dummy','--fixed-fps','60','--','--delivery-check='+mode],detached,logs/('detached-'+mode+'.log'),env,'EXPORTED DELIVERY '+mode.upper()+' PASS')
        if a.render:
            if system!='Linux':raise RuntimeError('--render requires Linux Xvfb in this runner')
            env['LIBGL_ALWAYS_SOFTWARE']='1';env['DELIVERY_CAPTURE_DIR']=str(logs/'captures')
            run(['xvfb-run','-a',executable,'--audio-driver','Dummy','--rendering-method','gl_compatibility','--','--delivery-check=render'],detached,logs/'detached-render.log',env,'EXPORTED DELIVERY RENDER PASS')
    hashes={x.relative_to(package).as_posix():hashlib.sha256(x.read_bytes()).hexdigest() for x in package.rglob('*') if x.is_file()}
    (out/'SHA256.json').write_text(json.dumps(hashes,indent=2),encoding='utf-8')
    # zipfile cannot retain macOS framework symlinks; use ditto for that platform.
    archive=out/('Starlight-'+preset+'.zip')
    if system=='Darwin':subprocess.run(['ditto','-c','-k','--sequesterRsrc','--keepParent',str(package),str(archive)],check=True)
    else:
        with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
            for file in package.rglob('*'):
                if file.is_file():z.write(file,Path('Starlight')/file.relative_to(package))
    print('DETACHED RELEASE PASS:',preset,archive)

if __name__=='__main__':main()
