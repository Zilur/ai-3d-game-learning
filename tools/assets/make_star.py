"""Rebuild the dependency-free, flat-shaded glTF star. Python 3.10+.
Run from the repository root: python tools/assets/make_star.py
Asset size: 0.9511 x 0.9045 x 0.20 model units; origin at radial centre.
No external textures, no third-party model or generative image service.
"""
from pathlib import Path
import base64
import json
import math
import struct

ROOT = Path(__file__).resolve().parents[2]

def build():
    ring = []
    for i in range(10):
        angle = math.pi / 2 + i * math.pi / 5
        r = 0.5 if i % 2 == 0 else 0.23
        ring.append((r * math.cos(angle), r * math.sin(angle)))
    positions, normals = [], []
    def triangle(a, b, c):
        u = [b[k] - a[k] for k in range(3)]
        v = [c[k] - a[k] for k in range(3)]
        n = [u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]]
        length = math.sqrt(sum(x*x for x in n))
        assert length > 1e-8, 'Degenerate triangle'
        for p in (a, b, c):
            positions.extend(p)
            normals.extend(x / length for x in n)
    for i in range(10):
        x,y = ring[i]; u,v = ring[(i+1)%10]
        a,b,c,d = (x,y,0.1),(u,v,0.1),(x,y,-0.1),(u,v,-0.1)
        triangle((0,0,0.1),a,b)
        triangle((0,0,-0.1),d,c)
        triangle(a,c,d)
        triangle(a,d,b)
    # glTF front faces are CCW. Exporter/importer handles engine convention changes.
    p = struct.pack('<'+'f'*len(positions), *positions)
    n = struct.pack('<'+'f'*len(normals), *normals)
    doc = {'asset':{'version':'2.0','generator':'AI 3D learning / make_star.py'},
        'scene':0,'scenes':[{'nodes':[0]}],'nodes':[{'name':'StarMesh','mesh':0}],
        'meshes':[{'primitives':[{'attributes':{'POSITION':0,'NORMAL':1},'material':0}]}],
        'materials':[{'name':'Gold','pbrMetallicRoughness':{'baseColorFactor':[1,0.65,0.08,1],
            'metallicFactor':0.15,'roughnessFactor':0.35},'emissiveFactor':[0.15,0.07,0]}],
        'buffers':[{'byteLength':len(p+n),'uri':'data:application/octet-stream;base64,'+base64.b64encode(p+n).decode()}],
        'bufferViews':[{'buffer':0,'byteOffset':0,'byteLength':len(p),'target':34962},
            {'buffer':0,'byteOffset':len(p),'byteLength':len(n),'target':34962}],
        'accessors':[{'bufferView':0,'componentType':5126,'count':len(positions)//3,'type':'VEC3',
            'min':[min(positions[k::3]) for k in range(3)],'max':[max(positions[k::3]) for k in range(3)]},
            {'bufferView':1,'componentType':5126,'count':len(normals)//3,'type':'VEC3'}]}
    path = ROOT/'practice/godot/assets/star.gltf'
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return path

if __name__ == '__main__':
    print(build())
