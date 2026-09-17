#!/usr/bin/env python3
"""Build local source/classroom packages or native Mac/Windows releases. No uploading."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import os
import shutil
import sys
import zipfile
from lib.course import ROOT, require
from lib.learning_state import atomic_write
from workspace import clean_path, console

SOURCE_DIRS={'course','practice','openmaic','tools','docs','.github'}
ROOT_FILES={'README.md','AGENTS.md','.gitignore','.gitattributes'}
SKIP={'.godot','.git','.learning','__pycache__','.export','exports','build','dist','node_modules'}
FONT_EXTS={'.ttf','.otf','.woff','.woff2','.ttc','.otc'}


def source_files(root: Path=ROOT):
    for path in sorted(root.rglob('*')):
        rel=path.relative_to(root)
        if any(x in SKIP for x in rel.parts) or rel.parts[:2]==('openmaic','output'):continue
        if rel.parts[0] not in SOURCE_DIRS and rel.as_posix() not in ROOT_FILES:continue
        require(not path.is_symlink(),'源码包不能包含符号链接：'+str(rel))
        if not path.is_file():continue
        if path.suffix in FONT_EXTS or path.suffix in {'.pyc','.log','.tmp','.blend1','.blend2'}:continue
        if path.name.startswith('.env') or path.name in {'export_credentials.cfg','server-providers.yml','.DS_Store','Thumbs.db'}:continue
        yield path


def output_path(path: Path,root: Path=ROOT):
    p=clean_path(path);base=clean_path(root/'dist')
    require(base in p.parents and p!=base,'交付只能写入本仓库dist子目录')
    require(not p.exists(),'交付已存在；选择新名称，不覆盖')
    return p


def source_archive(path:Path,root:Path=ROOT):
    path=output_path(path,root);files=list(source_files(root))
    require(files and (root/'practice/godot/project.godot') in files,'源工程不完整')
    path.parent.mkdir(parents=True,exist_ok=True)
    # mode x prevents overwriting a concurrent build's package.
    with zipfile.ZipFile(path,'x',zipfile.ZIP_DEFLATED) as z:
        for f in files:z.write(f,Path('ai-3d-game-learning')/f.relative_to(root))
    return path,len(files)


def classroom_archive(lesson,run_id,version,root=ROOT):
    from openmaic import require_publishable,digest
    import re
    require(re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]{0,39}',version),'非法版本名')
    path,record=require_publishable(lesson,run_id,root)
    out=output_path(root/'dist/openmaic'/lesson/(version+'.zip'),root)
    out.parent.mkdir(parents=True,exist_ok=True)
    # No private context, state, recordings, or cookies are included.
    with zipfile.ZipFile(out,'x',zipfile.ZIP_DEFLATED) as z:
        for name in ('input.md','run.json','review.md',lesson+'.maic.zip'):
            f=path/name;require(f.is_file() and not f.is_symlink(),'运行记录不完整');z.write(f,name)
    return out


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
    q=sub.add_parser('source');q.add_argument('--name',default='ai3d-source.zip')
    q=sub.add_parser('classroom');q.add_argument('lesson');q.add_argument('run_id');q.add_argument('--version',required=True)
    q=sub.add_parser('desktop');q.add_argument('--godot',default=os.environ.get('GODOT_BINARY','godot'));q.add_argument('--out',type=Path,default=ROOT/'dist/desktop')
    a=p.parse_args(argv)
    if a.command=='source':
        require(Path(a.name).name==a.name and a.name.endswith('.zip'),'只指定.zip文件名，不传路径')
        path,count=source_archive(ROOT/'dist'/a.name);console(f'已打包{count}个源文件：{path}；未上传。')
    elif a.command=='classroom':console(str(classroom_archive(a.lesson,a.run_id,a.version))+'；仅本地打包，未上传。')
    else:
        # Native export still uses official matching templates and detached smoke tests.
        from lib import desktop_export
        dest=clean_path(a.out);require(ROOT/'dist' in dest.parents,'桌面输出必须在dist下')
        sys.argv=['desktop_export','--godot',a.godot,'--out',str(dest)]
        desktop_export.main()
    return 0


if __name__=='__main__':
    try:raise SystemExit(main())
    except (ValueError,OSError,KeyError,TypeError) as exc:
        console('未完成：'+str(exc),stream=sys.stderr);raise SystemExit(2)
