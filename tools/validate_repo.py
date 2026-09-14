"""Dependency-free content/geometry checks; NOT a Godot runtime test."""
from pathlib import Path
from collections import Counter
from urllib.parse import unquote
import base64
import json
import math
import re
import struct
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []
def check(ok, message):
    if not ok:
        errors.append(message)

for path in ROOT.rglob('*.md'):
    text = path.read_text(encoding='utf-8')
    for link in re.findall(r'\[[^\]]*\]\(([^\s)]+)\)', text):
        if '://' in link or link.startswith(('#', 'mailto:')):
            continue
        target = unquote(link.split('#')[0])
        check((path.parent/target).exists(), f'Broken link: {path.relative_to(ROOT)} -> {target}')

concepts = (ROOT/'curriculum/concept-map.md').read_text(encoding='utf-8')
ids = set(re.findall(r'^### (C\d{2})', concepts, re.M))
questions = (ROOT/'assessments/question-bank.md').read_text(encoding='utf-8')
qids = re.findall(r'\*\*(C\d{2}-[PT])', questions)
check(len(ids) == 32, 'Expected 32 concepts')
check(len(qids) == len(set(qids)) == 64, 'Expected 64 unique questions')
check(set(qids) == {f'{c}-{t}' for c in ids for t in ('P', 'T')}, 'Concept/question coverage mismatch')
answers = (ROOT/'assessments/answer-key.md').read_text(encoding='utf-8')
check(set(re.findall(r'^## (C\d{2})', answers, re.M)) == ids, 'Answer coverage mismatch')
for c in ids:
    check(c in (ROOT/'print/必须牢记.md').read_text(encoding='utf-8'), f'Missing print card {c}')

for path in (ROOT/'game').rglob('*'):
    if path.suffix not in ('.gd', '.tscn', '.godot'):
        continue
    text = path.read_text(encoding='utf-8')
    for resource in re.findall(r'res://([^"\s]+)', text):
        check((ROOT/'game'/resource).exists(), f'Missing resource {resource}')
    if path.suffix == '.tscn':
        # Resource identifiers must be unique within a scene, even before engine import.
        declarations = re.findall(r'\[(?:ext|sub)_resource[^\n]* id="([^"]+)"', text)
        check(len(declarations) == len(set(declarations)), f'Duplicate resource IDs: {path.name}')

mesh = json.loads((ROOT/'game/assets/star.gltf').read_text(encoding='utf-8'))
buf = base64.b64decode(mesh['buffers'][0]['uri'].split(',',1)[1], validate=True)
check(len(buf) == mesh['buffers'][0]['byteLength'], 'glTF buffer length')
v = mesh['bufferViews'][0]
pos = list(struct.iter_unpack('<fff', buf[v['byteOffset']:v['byteOffset']+v['byteLength']]))
v = mesh['bufferViews'][1]
norm = list(struct.iter_unpack('<fff', buf[v['byteOffset']:v['byteOffset']+v['byteLength']]))
check(len(pos) == len(norm) == 120, 'Expected 40 triangles, 120 flat-shaded vertices')
edges = Counter()
for i in range(0,len(pos),3):
    a,b,c = pos[i:i+3]
    u = [b[k]-a[k] for k in range(3)];w = [c[k]-a[k] for k in range(3)]
    n = [u[1]*w[2]-u[2]*w[1],u[2]*w[0]-u[0]*w[2],u[0]*w[1]-u[1]*w[0]]
    check(sum(n[k]*norm[i][k] for k in range(3)) > 1e-8, 'Winding/normal mismatch')
    for x,y in ((a,b),(b,c),(c,a)):
        edge = tuple(sorted((tuple(round(z,6) for z in x),tuple(round(z,6) for z in y))))
        edges[edge] += 1
check(all(n == 2 for n in edges.values()), 'Star mesh is not watertight after welding')
check(all(abs(sum(x*x for x in n)-1) < 1e-5 for n in norm), 'Non-unit normals')

if errors:
    print('\n'.join(errors));sys.exit(1)
print('PASS: links, 32 concepts / 64 questions, answer/print coverage, Godot resource paths, star geometry.')
print('NOT TESTED: GDScript parser, Godot import/runtime/rendering, Blender, target hardware, OpenMAIC generation.')
