#!/usr/bin/env python3
"""One validation entry point. Default: source + asset + Python checks. Native checks are explicit."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import unittest
from urllib.parse import unquote,urlsplit
from lib.course import ROOT,ORDER,catalog,read_lesson,memory_sections,teacher_section,require,build_input
from workspace import clean_path,console


def check_links(root=ROOT):
    """Resolve authored relative Markdown links; don't fetch websites or run fenced examples."""
    problems=[]
    for p in root.rglob('*.md'):
        rel=p.relative_to(root)
        if any(x in {'.git','.learning','build','dist','output','__pycache__','.godot'} for x in rel.parts):continue
        text=p.read_text(encoding='utf-8')
        text=re.sub(r'```.*?```','',text,flags=re.S)
        for value in re.findall(r'\]\(([^)\s]+)(?:\s+"[^"]*")?\)',text):
            if value.startswith(('https:','http:','mailto:','data:')):continue
            url=urlsplit(value);name=unquote(url.path);target=(p.parent/name).resolve() if name else p.resolve()
            if not target.is_relative_to(root.resolve()):problems.append(f'{rel}: escapes root: {value}');continue
            if not target.exists():problems.append(f'{rel}: missing {value}')
            elif url.fragment and target.is_file() and target.suffix=='.md':
                content=target.read_text(encoding='utf-8');fragment=unquote(url.fragment)
                explicit=re.findall(r'<a\s+id="([^"]+)"',content)
                headings=re.findall(r'^#+\s+(.+)$',content,re.M)
                slugs=[re.sub(r'[^\w\-\s\u4e00-\u9fff]','',h.lower()).strip().replace(' ','-') for h in headings]
                if fragment not in explicit+slugs:problems.append(f'{rel}: missing anchor {value}')
    require(not problems,'本地链接错误：\n'+'\n'.join(problems))


def check_course(root=ROOT):
    obj,cards,bindings,order=catalog(root)
    memory=memory_sections(root)
    require(set(memory)=={f'KN{i:02}' for i in range(1,33)}|{f'ART{i:02}' for i in range(1,10)}|{f'TH{i:02}' for i in range(1,7)},'记忆清单缺少已定义概念／思维模式')
    core=[];extras=[]
    index=(root/'course/README.md').read_text(encoding='utf-8')
    for ident in order:
        row=read_lesson(ident,root)
        require(row['title'] in index and f'](lessons/{ident}.md)' in index,'课程索引缺标题／链接：'+ident)
        require(all(x in memory for x in row['meta']['memory']),'缺记忆项：'+ident)
        feedback=teacher_section(ident,root)
        for qid in row['questions']:require('### '+qid+'\n' in feedback,'缺逐课反馈：'+qid)
        core.extend(row['questions'])
        qx=re.findall(r'^### ((?:KN\d+-[PT]|K\d+))｜',row['body'],re.M);extras+=qx
        for qid in qx:require('### '+qid+'\n' in feedback,'缺补充反馈：'+qid)
        require(row['body'].count('<details')==row['body'].count('</details>'),'折叠段落不闭合：'+ident)
        txt,_=build_input(ident,root=root)
        require(txt.count('## 讲给爸爸听')==1,'组装重复伙伴分享')
        require('data-purpose="project"' not in txt,'默认输入泄漏制作步骤')
    require(len(core)==188 and len(set(core))==188,'逐课题覆盖改变')
    require(len(extras)==76 and len(set(extras))==76,'补充题未完整归位')
    require(len(obj)==147,'原能力ID覆盖改变')
    require(not any((root/x).exists() for x in ('curriculum','assessments','learning-system','art','print','glossary','game','blender','web','docs/archive','openmaic/vendor')),'旧活跃目录仍存在')
    data=json.loads((root/'openmaic/catalog.json').read_text(encoding='utf-8'))
    require(data.get('schema_version')==1 and isinstance(data.get('courses'),dict),'发布索引无效')
    check_links(root)
    console(f'COURSE PASS: {len(order)} Markdown sources, {len(obj)} stable objectives, 188 core + 76 supplemental questions, {len(memory)} memory items; no classroom generated')


def clean_build(root=ROOT,confirm=False):
    base=clean_path(root/'build')
    if not base.exists():return []
    require(base.is_dir(),'build不是目录')
    files=list(base.rglob('*'))
    require(not any(p.is_symlink() for p in files),'缓存中有符号链接，拒绝清理')
    listing=[p.relative_to(root).as_posix() for p in files if p.is_file()]
    if confirm:shutil.rmtree(base)
    return listing


def run_native(command):
    r=subprocess.run(command,cwd=ROOT,timeout=600)
    require(r.returncode==0,'原生检查失败：'+str(command))


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--godot');p.add_argument('--blender');p.add_argument('--web',action='store_true')
    p.add_argument('--clean',action='store_true');p.add_argument('--confirm',action='store_true')
    p.add_argument('--source-only',action='store_true',help='仅源码／链接／资产校验；不运行单元测试')
    a=p.parse_args(argv)
    if a.clean:
        console('\n'.join(clean_build(confirm=a.confirm)) or '没有可清理缓存。')
        console('已按白名单清理build。' if a.confirm else '仅预览，未删除。');return 0
    require(not a.confirm,'--confirm只用于--clean')
    check_course()
    from lib.checks import check_practical_labs,check_production
    check_practical_labs.main();check_production.main()
    if not a.source_only:
        suite=unittest.defaultTestLoader.discover(str(ROOT/'tools/tests'),pattern='test_*.py')
        result=unittest.TextTestRunner(verbosity=2).run(suite)
        require(result.wasSuccessful(),'Python测试失败')
    if a.godot:run_native([sys.executable,str(ROOT/'tools/lib/checks/run_production_checks.py'),'--godot',a.godot])
    if a.blender:
        paths=list((ROOT/'practice/blender').glob('*.blend'))
        before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
        run_native([a.blender,'--background','--python-exit-code','1','--python',str(ROOT/'tools/assets/build_practical_labs.py'),'--','--verify-only'])
        require(before=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'验证过程不得重建或修改现成blend')
    if a.web:run_native([sys.executable,str(ROOT/'tools/tests/browser_space.py')])
    console('CHECK PASS。未指定的软件检查未运行；不代表课堂生成、儿童试教或全设备验收。')
    return 0


if __name__=='__main__':
    try:raise SystemExit(main())
    except (ValueError,OSError,KeyError,TypeError,subprocess.SubprocessError) as exc:
        console('未完成：'+str(exc),stream=sys.stderr);raise SystemExit(1)
