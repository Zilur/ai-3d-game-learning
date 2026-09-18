"""Read-only course source contract. Markdown is authoritative; no generator writes it.
Metadata uses JSON flow syntax (a YAML subset) between --- fences, so stdlib suffices.
"""
from __future__ import annotations
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
ORDER = [f'{group}{i:02}' for group, count in [('A',8),('B',13),('C',12),('D',7),('E',7)] for i in range(1,count+1)]
MAX_TEXT = 1_000_000


def require(ok, message):
    if not ok:
        raise ValueError(message)


def _unique(pairs):
    result = {}
    for k,v in pairs:
        require(k not in result, '重复JSON键：'+k)
        result[k] = v
    return result


def json_text(text):
    return json.loads(text, object_pairs_hook=_unique,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError('非JSON值：'+x)))


def read_text(path: Path) -> str:
    require(path.is_file() and not path.is_symlink() and path.stat().st_size <= MAX_TEXT,
            '文件缺失、过大或为符号链接：'+str(path))
    return path.read_text(encoding='utf-8')


def split_document(text: str):
    require(text.startswith('---\n'), '教案必须有元数据头')
    head, sep, body = text[4:].partition('\n---\n')
    require(bool(sep), '元数据没有结束')
    data = json_text(head)
    require(isinstance(data, dict), '元数据必须为对象')
    return data, body


def field(text: str, label: str) -> str:
    match = re.search(r'^\*\*'+re.escape(label)+r'：\*\* (.+)$', text, re.M)
    require(match is not None, '缺少字段：'+label)
    return match.group(1)


def section(text: str, heading: str, level: int = 2) -> str:
    match = re.search(r'^'+('#'*level)+r' '+re.escape(heading)+r'\n(.*?)(?=^#{1,'+str(level)+r'} |\Z)',text,re.M|re.S)
    require(match is not None, '缺少章节：'+heading)
    return match.group(1).strip()


def experience_only(text: str) -> str:
    """Project tasks are removed, not just hidden by HTML. Nested details supported."""
    pieces=[]; pos=0
    for start in list(re.finditer(r'<details\s+data-purpose="project"\s*>',text)):
        if start.start()<pos: continue
        pieces.append(text[pos:start.start()]);depth=1;end=None
        for tag in re.finditer(r'<details\b[^>]*>|</details>',text[start.end():]):
            depth += -1 if tag.group()=='</details>' else 1
            if depth==0:
                end=start.end()+tag.end();break
        require(end is not None,'作品段落未闭合')
        pos=end
    pieces.append(text[pos:])
    return ''.join(pieces)


def read_lesson(ident: str, root: Path = ROOT) -> dict:
    require(ident in ORDER, '未知课号：'+str(ident))
    path=root/'course/lessons'/f'{ident}.md'
    raw=read_text(path);meta,body=split_document(raw)
    require(set(meta)=={'id','prerequisites','revisit','memory','labs'},'课头字段不一致：'+ident)
    require(meta['id']==ident,'文件名与课号不一致')
    for key in ('prerequisites','revisit','memory','labs'):
        require(isinstance(meta[key],list) and all(isinstance(x,str) for x in meta[key]),'列表不合法：'+key)
        require(len(set(meta[key]))==len(meta[key]),'列表重复：'+key)
    for dep in meta['prerequisites']+meta['revisit']:
        require(dep in ORDER and ORDER.index(dep)<ORDER.index(ident),'未知前置／前置在后：'+dep)
    for name in meta['labs']:
        p=Path(name)
        require(not p.is_absolute() and '..' not in p.parts and name.startswith(('practice/godot/','practice/blender/','practice/web/')), '非法实验路径')
        require((root/p).is_file() and not (root/p).is_symlink(),'实验不存在：'+name)
    title=re.match(r'^# '+ident+r'｜([^\n]+)',body)
    require(title is not None, '标题与课号不一致')
    objectives={}
    for match in re.finditer(r'^- `('+ident+r'\.([MK])\d+)` (.+)$',body,re.M):
        key,level,desc=match.groups();require(key not in objectives,'重复能力ID')
        objectives[key]={'lesson':ident,'level':level,'text':desc}
    m=[k for k,v in objectives.items() if v['level']=='M'];ks=[k for k,v in objectives.items() if v['level']=='K']
    require(len(m)==(0 if ident=='E06' else 2) and 1<=len(ks)<=2,'知识深度变化：'+ident)
    require(m==([] if ident=='E06' else [ident+'.M1',ident+'.M2']),'M能力ID变化')
    qids=re.findall(r'^### ('+ident+r'-[PDTK]\d+)\s*$',body,re.M)
    expected=[ident+'-'+kind+str(i+1) for i,kind in enumerate('KKKK' if ident=='E06' else 'PDTK')]
    require(qids==expected,'逐课题号／类型变化：'+ident)
    require(body.count('## 讲给爸爸听')==1,'伙伴分享应恰有一个')
    require('不必背稿、打分或填表' in body and '不影响继续自学' in body,'伙伴分享不能成为门槛')
    share=section(body,'讲给爸爸听')
    # The share section is followed by a project details block: don't include it in the card.
    share=share.split('<details',1)[0].strip()
    match=re.search(r'用自己的话讲讲：(.+?)。',share)
    require(match is not None,'缺少伙伴分享的概念')
    cards=(match.group(1),field(share,'给他演示'),field(share,'你们一起问'))
    production=re.search(r'^\*\*生产阶段：\*\* (.+)$',body,re.M)
    binding=(meta['labs'],field(body,'从哪里开始'),field(body,'材料边界'),production.group(1) if production else '用途讨论')
    require(ident!='E06' or not meta['labs'],'全K课程不要求软件实验')
    return dict(meta=meta,body=body,raw=raw,title=title.group(1),goal=field(body,'今天做什么'),
                objectives=objectives,questions=qids,card=cards,binding=binding,
                entry=field(body,'先从这里开始'))


def catalog(root: Path = ROOT):
    files={p.stem for p in (root/'course/lessons').glob('*.md')}
    require(files==set(ORDER),'必须恰有47份正式教案')
    objectives={};cards={};bindings={}
    for ident in ORDER:
        row=read_lesson(ident,root);objectives.update(row['objectives']);cards[ident]=row['card'];bindings[ident]=row['binding']
    return objectives,cards,bindings,ORDER.copy()


def partner_text(lesson, cards):
    terms,demo,question=cards[lesson]
    return ('## 讲给爸爸听\n\n可演示一个选择、发现或疑问，不要求完整讲课。用自己的话讲讲：'+terms+'。\n\n**给他演示：** '+demo+
            '\n\n**你们一起问：** '+question+'\n\n爸爸还有问题就接着问，你也可以问爸爸。一起看、一起试，不必背稿、打分或填表。爸爸暂时不在就稍后分享，不影响继续自学。\n')


def short_card(lesson, cards, bindings, purpose='experience', root: Path=ROOT):
    """A learner opening, not a dump of demonstrations, review cues or teacher answers."""
    row=read_lesson(lesson,root)
    paths,first,limits,_=bindings[lesson]
    return ('# '+lesson+'｜今天只做这一小步\n\n**今天先试：** '+row['entry']+
            '\n\n**打开：** '+('、'.join('`'+p+'`' for p in paths) or '讨论，不新建工程')+
            '\n\n可以要线索、看示范或直接请解释；可以短答、指认或演示，也可以暂停。\n\n'+
            '<details>\n<summary>需要时找操作入口与材料边界</summary>\n\n**首步：** '+first+
            '\n\n材料边界：'+limits+'\n\n</details>\n\n'+
            '<details>\n<summary>想分享时再打开</summary>\n\n'+partner_text(lesson,cards)+'\n</details>\n\n'+
            ('全K：只聊用途，不要求软件实操，不强制背诵。' if lesson=='E06' else '备用题按需要选，不必全做。')+
            '\n\n'+('体验现成材料，不重造Lab。' if purpose=='experience' else '只改自己的工作副本。')+'\n')


def memory_sections(root: Path = ROOT) -> dict[str,str]:
    text=read_text(root/'course/memory.md')
    return {m.group(1):m.group(2).strip() for m in re.finditer(r'^### ((?:KN|ART|TH)\d+)｜(.*?)(?=^<a id=|\Z)',text,re.M|re.S)}


def memory_cues(lesson: str, root: Path = ROOT) -> str:
    row=read_lesson(lesson,root);sections=memory_sections(root)
    ids=row['meta']['memory']
    require(all(k in sections for k in ids),'记忆项缺失')
    # show prompts, not memorized answers, and don't infer mastery from opening a lesson.
    selected=ids[:1] if lesson=='E06' else list(dict.fromkeys(ids[:1]+[k for k in ids if k.startswith('TH')]))[:2]
    heading='## 本课用途提示（不背诵）' if lesson=='E06' else '## 本课需要逐渐熟悉的词和思路'
    return heading+'\n\n'+'\n'.join('- `'+k+'` '+field(sections[k],'遮住后自问') for k in selected)+\
        '\n\n完整清单：`course/memory.md`。只练已学部分，不是晨晚打卡；打开本课不表示已掌握。\n'


def teacher_section(lesson: str, root: Path = ROOT) -> str:
    text=read_text(root/'course/teacher-notes.md')
    common=text.partition('\n## ')[0].strip()
    return common+'\n\n## '+lesson+'\n\n'+section(text,lesson)


def build_input(lesson: str, *, purpose: str='experience', root: Path=ROOT) -> tuple[str,dict]:
    require(purpose in ('experience','project'),'未知输入用途')
    row=read_lesson(lesson,root)
    skill=read_text(root/'openmaic/skills/ai3d-self-study/SKILL.md')
    mem=memory_sections(root);selected='\n\n'.join('### '+k+'｜'+mem[k] for k in row['meta']['memory'])
    body=experience_only(row['body']) if purpose=='experience' else row['body']
    body='教案关联信息（教师侧，不是学生页面）：\n```json\n'+json.dumps(row['meta'],ensure_ascii=False,sort_keys=True)+'\n```\n\n'+body
    teacher=teacher_section(lesson,root)
    # These are the actual selected pieces: unrelated lessons do not invalidate this input.
    pieces={'lesson':body,'teacher':teacher,'memory':selected,'skill':skill}
    import hashlib
    hashes={k:hashlib.sha256(v.encode('utf-8')).hexdigest() for k,v in pieces.items()}
    text=('> 教师生成输入，不是已经生成的课堂。不含私人历史；参考答案只能在首次作答之后用于反馈。\n'
          '> 只生成本课，保持课号和M/K；生成后的控件、复位和答案时机需实际检查。\n\n'+
          '# 课程差异要求\n\n'+skill+'\n\n'+body+'\n\n# 本课记忆项（先自问，再核对）\n\n'+selected+
          '\n\n# 教师答案：初始学生页面不可展示\n\n'+teacher+'\n')
    return text,hashes
