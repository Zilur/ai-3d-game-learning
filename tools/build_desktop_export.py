"""Export a native release, then test a copied package without editor or source path.
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
ROOT=Path(__file__).resolve().parents[1]
ERRORS=re.compile(r'SCRIPT ERROR|Parse Error|ERROR:|ObjectDB instances leaked|resources still in use')


def run(command,log,cwd,env=None,marker=None,timeout=300):
    result=subprocess.run(command,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace',timeout=timeout)
    log.parent.mkdir(parents=True,exist_ok=True); log.write_text(result.stdout,encoding='utf-8'); print(result.stdout)
    if result.returncode or ERRORS.search(result.stdout) or marker and marker not in result.stdout:
        raise RuntimeError('Export/runtime check failed: '+str(log))


def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--godot',default=os.environ.get('GODOT_BINARY','godot'));p.add_argument('--out',type=Path,default=Path('build/desktop'));p.add_argument('--render',action='store_true');a=p.parse_args()
    system=platform.system(); preset={'Linux':'Linux','Windows':'Windows','Darwin':'macOS'}[system]
    out=a.out.resolve()/preset
    if out.exists():raise ValueError('Output exists; choose a new folder, never overwrite a package.')
    package=out/'package';package.mkdir(parents=True);evidence=out/'evidence';evidence.mkdir()
    run([a.godot,'--version'],evidence/'version.log',ROOT,marker='4.7.2.stable')
    base=[a.godot,'--headless','--audio-driver','Dummy','--path',str(ROOT/'game')]
    run(base+['--editor','--import'],evidence/'import.log',ROOT)
    target=package/({'Linux':'Starlight.x86_64','Windows':'Starlight.exe','Darwin':'Starlight-macOS.zip'}[system])
    run(base+['--export-release',preset,str(target)],evidence/'export.log',ROOT)
    if system=='Darwin':
        subprocess.run(['ditto','-x','-k',str(target),str(package)],check=True);target.unlink()
    env=os.environ.copy();env['NOTICES_OUT']=str(package/'GODOT-THIRD-PARTY-NOTICES.txt')
    run(base+['--script','res://tests/write_notices.gd'],evidence/'notices.log',ROOT,env)
    shutil.copy2(ROOT/'game/assets/village/LICENSE.txt',package/'ASSET-LICENSE.txt')
    shutil.copy2(ROOT/'game/assets/practice-asset-notes.md',package/'PRACTICE-ASSET-NOTES.md')
    (package/'README.txt').write_text('星光小庭院｜亲子课程独立体验包\n\n解压整个目录，不要只移动exe或pck。Windows运行Starlight.exe；Linux运行Starlight.x86_64；macOS打开.app。\n需要操作系统提供中文字体；不随包分发字体。WASD移动，Shift跑，空格跳，E交互，J训练，Esc暂停，F9保存，F10读档。\n窗口关闭和实验往返已有保存保护；内存暂存不是磁盘存档。仅教学试玩，未经商店签名/公证，不建议绕过系统安全机制；遇拦截由成人核对来源并使用源码项目。\n行为自动测试不等于所有设备、听感、儿童学习或商业品质已验收。\n',encoding='utf-8')
    if system=='Darwin':
        apps=list(package.glob('*.app'));assert len(apps)==1
        binaries=[x for x in (apps[0]/'Contents/MacOS').iterdir() if x.is_file()]
        assert len(binaries)==1;binary=binaries[0]
    else:binary=target
    if os.name!='nt':binary.chmod(binary.stat().st_mode|0o111)
    with tempfile.TemporaryDirectory(prefix='detached-starlight-') as temporary:
        detached=Path(temporary)/'package';shutil.copytree(package,detached)
        exe=detached/binary.relative_to(package)
        runtime_env=os.environ.copy();runtime_env['DELIVERY_CASE']=preset.lower()+'-'+os.urandom(4).hex()
        for phase in ('write','read'):
            run([str(exe),'--headless','--audio-driver','Dummy','--fixed-fps','60','--','--delivery-check='+phase],evidence/(phase+'.log'),detached,runtime_env,'EXPORTED DELIVERY '+phase.upper()+' PASS')
        if a.render and system=='Linux':
            runtime_env['DELIVERY_CAPTURE']=str(evidence)
            run(['xvfb-run','-a','-s','-screen 0 1280x720x24',str(exe),'--audio-driver','Dummy','--rendering-method','gl_compatibility','--','--delivery-check=render'],evidence/'render.log',detached,runtime_env,'EXPORTED DELIVERY RENDER PASS')
    files={str(x.relative_to(package)):hashlib.sha256(x.read_bytes()).hexdigest() for x in sorted(package.rglob('*')) if x.is_file()}
    (out/'SHA256.json').write_text(json.dumps(files,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    archive=out/('Starlight-'+preset+'.zip')
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for file in sorted(package.rglob('*')):
            if file.is_file():z.write(file,Path('Starlight-'+preset)/file.relative_to(package))
    print('STANDALONE EXPORT VERIFIED:',archive)
if __name__=='__main__':main()
