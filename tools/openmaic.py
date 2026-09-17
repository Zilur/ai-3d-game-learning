#!/usr/bin/env python3
"""Prepare and track local OpenMAIC artifacts. Never generates classrooms or calls a service."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import sys
import zipfile
from urllib.parse import urlsplit
from lib.course import ROOT, ORDER, build_input, json_text, require, read_text
from lib.learning_state import atomic_write, locked
from workspace import clean_path, console

CHECKS = ('scope','interaction','reset','answers','partner','resources','privacy')
DESCRIPTIONS = (
 '课号、M/K和停止线保持，没有把候选题全加成作业',
 '在实际课堂中操作控件，结果真实改变，不是假按钮',
 '实验能恢复；模拟与Godot/Blender实测明确区分',
 '参考答案在首次作答后反馈，不提前展示',
 '只有一次轻量伙伴分享，爸爸不在不阻塞',
 '导出后重新导入检查媒体与依赖，需联网之处有说明',
 '无密钥、私人对话和学情；素材授权与分享范围已核对')


def digest(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()


def run_path(lesson: str, run_id: str, root: Path=ROOT) -> Path:
    require(lesson in ORDER,'未知课号')
    require(re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,63}',run_id) is not None,'运行ID限字母数字、短横线和下划线')
    return clean_path(root/'openmaic/output'/lesson/run_id)


def load_run(lesson, run_id, root=ROOT):
    path=run_path(lesson,run_id,root)
    row=json_text(read_text(path/'run.json'))
    require(row.get('schema_version')==1 and row.get('lesson')==lesson and row.get('run_id')==run_id,'运行记录不匹配')
    require(digest(path/'input.md')==row['input_sha256'],'输入快照被改动；建立新运行，不覆盖来源')
    require(row.get('purpose') in ('experience','project'),'未知用途')
    require(row.get('status') in ('prepared','export-attached'),'未知运行状态')
    return path,row


def prepare(lesson: str, run_id: str | None=None, *, purpose='experience', upstream_ref=None, root=ROOT):
    text,hashes=build_input(lesson,purpose=purpose,root=root)
    require(upstream_ref is None or re.fullmatch(r'[A-Za-z0-9._/-]{1,100}',upstream_ref),'上游版本使用公开版本号或提交，不填URL/密钥')
    if run_id is None:
        prefix=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
        run_id=prefix+'-'+os.urandom(3).hex()
    path=run_path(lesson,run_id,root)
    require(not path.exists(),'运行已存在，不覆盖')
    path.parent.mkdir(parents=True,exist_ok=True)
    path.mkdir() # exclusive; competing writers cannot overwrite the same run
    row={'schema_version':1,'lesson':lesson,'run_id':run_id,'purpose':purpose,
         'created_at':datetime.now(timezone.utc).isoformat(), 'upstream_ref':upstream_ref,
         'source_hashes':hashes,'input_sha256':hashlib.sha256(text.encode()).hexdigest(),
         'status':'prepared','export':None}
    try:
        atomic_write(path/'input.md',text)
        atomic_write(path/'run.json',json.dumps(row,ensure_ascii=False,indent=2)+'\n')
        review='# '+lesson+'｜本次实际验收\n\n未生成、未检查的项目保持未勾选，不凭工具通过替代课堂体验。\n\n'
        review+='\n'.join('- [ ] '+key+': '+desc for key,desc in zip(CHECKS,DESCRIPTIONS))
        review+='\n\n## 实际环境与发现\n\n写明实际OpenMAIC版本、导入环境、已发现问题和需要联网的部分；不要填私人资料。\n'
        atomic_write(path/'review.md',review)
    except Exception:
        # Only the newly created run is ours. Preserve it for diagnosis, never pretend success.
        raise
    return path


def check_export(path: Path) -> dict:
    """Container sanity only; never execute HTML/JS or claim instructional validation."""
    path=clean_path(path)
    require(path.name.endswith('.maic.zip') and path.is_file(),'需要实际导出的.maic.zip文件')
    require(0<path.stat().st_size<=512*1024*1024,'课堂包为空或大于512MiB')
    with zipfile.ZipFile(path) as z:
        infos=z.infolist();require(0<len(infos)<=20000,'ZIP条目过多或为空')
        require(sum(x.file_size for x in infos)<=1024**3,'ZIP解压大小超过1GiB')
        seen=set()
        for i in infos:
            # ZIP readers normalize platform separators and truncate at NUL.
            # Reject altered raw member names before checking the normalized path.
            require(i.orig_filename == i.filename and '\0' not in i.orig_filename,'ZIP含被规范化的不安全路径')
            n=PurePosixPath(i.filename)
            require(not n.is_absolute() and '..' not in n.parts and '\\' not in i.filename and ':' not in i.filename,'ZIP含不安全路径')
            require(i.filename not in seen,'ZIP含重复文件名');seen.add(i.filename)
            require(not stat.S_ISLNK(i.external_attr>>16),'ZIP不能含符号链接')
            require(not (i.flag_bits & 1),'不支持加密ZIP')
        require('manifest.json' in seen,'未找到原生manifest.json')
        info=z.getinfo('manifest.json');require(info.file_size<=8*1024*1024,'清单过大')
        data=json_text(z.read('manifest.json').decode('utf-8'))
        require(isinstance(data,dict) and type(data.get('formatVersion')) is int and data['formatVersion']==1,'未验证的上游导出格式；先核查，不猜测转换')
        require(isinstance(data.get('stage'),dict) and isinstance(data.get('scenes'),list) and data['scenes'],'缺课堂结构')
        require(isinstance(data.get('agents'),list) and isinstance(data.get('mediaIndex'),dict),'缺角色或媒体索引')
        require(all(isinstance(s,dict) and s.get('type') in ('slide','quiz','interactive','pbl') for s in data['scenes']),'未知课堂场景类型')
        require(z.testzip() is None,'ZIP校验失败')
        missing=sum(isinstance(v,dict) and v.get('missing') is True for v in data['mediaIndex'].values())
    return {'file':path.name,'sha256':digest(path),'bytes':path.stat().st_size,
            'format_version':1,'scenes':len(data['scenes']),'reported_missing_media':missing,
            'validation':'container-only; classroom not executed'}


def attach_export(lesson,run_id,source:Path,root=ROOT):
    path,row=load_run(lesson,run_id,root)
    facts=check_export(source)
    with locked(path):
        path,row=load_run(lesson,run_id,root)
        require(row['export'] is None,'本次已有产物；重新生成请另建运行')
        dest=path/(lesson+'.maic.zip')
        # exclusive byte copy: no extraction and no runtime execution
        with dest.open('xb') as out,source.open('rb') as src:
            shutil.copyfileobj(src,out);out.flush();os.fsync(out.fileno())
        require(digest(dest)==facts['sha256'],'复制中源文件变化；未登记产物')
        facts['file']=dest.name;row.update(status='export-attached',export=facts)
        atomic_write(path/'run.json',json.dumps(row,ensure_ascii=False,indent=2)+'\n')
    return facts


def inspect(lesson,run_id,root=ROOT):
    path,row=load_run(lesson,run_id,root)
    _text,hashes=build_input(lesson,purpose=row['purpose'],root=root)
    changed=[k for k in hashes if hashes[k]!=row['source_hashes'].get(k)]
    export=row['export'];export_ok=False
    if export:
        require(export['file']==lesson+'.maic.zip','非法产物定位')
        p=path/export['file'];export_ok=p.is_file() and not p.is_symlink() and digest(p)==export['sha256']
    checked=set(re.findall(r'^- \[[xX]\] ('+'|'.join(CHECKS)+r'): ',read_text(path/'review.md'),re.M))
    return {'lesson':lesson,'run_id':run_id,'status':row['status'],'source_changed':changed,
            'export_matches':export_ok,'review_complete':checked==set(CHECKS),
            'note':'勾选是操作者的验收声明，不是自动证明；未调用OpenMAIC。'}


def require_publishable(lesson,run_id,root=ROOT):
    report=inspect(lesson,run_id,root)
    require(not report['source_changed'],'教案或输入依赖已改变，先重新核查并建立新运行')
    require(report['export_matches'],'没有匹配的实际课堂包')
    require(report['review_complete'],'课堂实际验收尚未完成')
    path,row=load_run(lesson,run_id,root)
    require(not row['export'].get('reported_missing_media'),'上游报告缺失媒体，先修复再打包')
    return path,row


def register(lesson,run_id,version,url,*,confirm=False,root=ROOT):
    path,row=require_publishable(lesson,run_id,root)
    require(re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]{0,39}',version),'版本号格式错误')
    u=urlsplit(url)
    require(u.scheme=='https' and u.hostname and not (u.username or u.password or u.query or u.fragment),'只能登记不带令牌/查询参数的公开HTTPS链接')
    bundle=clean_path(root/'dist/openmaic'/lesson/(version+'.zip'))
    require(bundle.is_file(),'先用release.py classroom生成这个版本的交付包，再登记其公开地址')
    names=('input.md','run.json','review.md',lesson+'.maic.zip')
    with zipfile.ZipFile(bundle) as z:
        require(len(z.infolist())==len(names) and set(z.namelist())==set(names),'交付包文件不一致')
        for name in names:
            require(z.read(name)==(path/name).read_bytes(),'交付包与验收运行不同；不要登记过期包')
    record={'version':version,'run_id':run_id,'input_sha256':row['input_sha256'],
            'sha256':digest(bundle),'classroom_sha256':row['export']['sha256'],
            'url':url,'upstream_ref':row['upstream_ref']}
    if confirm:
        directory=clean_path(root/'openmaic')
        with locked(directory):
            target=directory/'catalog.json';data=json_text(read_text(target))
            require(data.get('schema_version')==1 and isinstance(data.get('courses'),dict),'索引格式错误')
            data['courses'][lesson]=record
            atomic_write(target,json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    return record


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
    q=sub.add_parser('prepare');q.add_argument('lesson');q.add_argument('--run-id');q.add_argument('--purpose',choices=['experience','project'],default='experience');q.add_argument('--upstream-ref')
    q=sub.add_parser('attach');q.add_argument('lesson');q.add_argument('run_id');q.add_argument('file',type=Path)
    q=sub.add_parser('inspect');q.add_argument('lesson');q.add_argument('run_id')
    q=sub.add_parser('register');q.add_argument('lesson');q.add_argument('run_id');q.add_argument('--version',required=True);q.add_argument('--url',required=True);q.add_argument('--confirm',action='store_true')
    q=sub.add_parser('context',help='单独预览可选私人摘要，不放进公开运行目录');q.add_argument('lesson');q.add_argument('--home',type=Path,default=ROOT/'.learning/family');q.add_argument('--confirm',action='store_true')
    a=p.parse_args(argv)
    if a.command=='prepare': console(str(prepare(a.lesson,a.run_id,purpose=a.purpose,upstream_ref=a.upstream_ref))+'；只准备输入，未生成课堂。')
    elif a.command=='attach':console(json.dumps(attach_export(a.lesson,a.run_id,a.file),ensure_ascii=False,indent=2))
    elif a.command=='inspect':console(json.dumps(inspect(a.lesson,a.run_id),ensure_ascii=False,indent=2))
    elif a.command=='register':console(json.dumps(register(a.lesson,a.run_id,a.version,a.url,confirm=a.confirm),ensure_ascii=False,indent=2)+'\n仅登记；未上传也未核实远端下载。')
    else:
        from lib.private_context import export_context
        text,path=export_context(a.home,a.lesson,confirm=a.confirm)
        console(str(path) if path else text)
    return 0


if __name__=='__main__':
    try:raise SystemExit(main())
    except (ValueError,OSError,KeyError,TypeError,zipfile.BadZipFile) as exc:
        console('未完成：'+str(exc),stream=sys.stderr);raise SystemExit(2)
