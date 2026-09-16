#!/usr/bin/env python3
"""Author tool: deterministic original GLB village kit, standard library only.
Learners open the committed assets, not this generator. Units metres; +Y up.
No third-party meshes/textures, no network, no writes outside game/assets/village.
"""
from __future__ import annotations
import hashlib
import json
import math
from pathlib import Path
import random
import struct

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'game/assets/village'
COLORS = {'plaster':'eadbb6','roof':'ad604b','roof_dark':'82483d','timber':'79533c',
          'wood':'b58b60','door':'377c7c','glass':'b3dcce','stone':'a9ada0',
          'stone_dark':'7b897d','leaves':'58894d','leaves_light':'78a55c',
          'pine':'3f7662','flower':'ebc16a','petal':'e8bfb3','metal':'3b595b',
          'lamp':'ffe2a1','water':'67acaf'}

def sub(a,b): return tuple(a[i]-b[i] for i in range(3))
def add(a,b): return tuple(a[i]+b[i] for i in range(3))
def mul(a,n): return tuple(v*n for v in a)
def cross(a,b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def norm(a): return mul(a, 1/max(1e-9,math.sqrt(sum(v*v for v in a))))

class Model:
    def __init__(self): self.parts={}
    def tri(self,a,b,c,color):
        n=norm(cross(sub(b,a),sub(c,a)))
        positions,normals=self.parts.setdefault(color,([],[]))
        positions.extend((*a,*b,*c)); normals.extend((*n,*n,*n))
    def quad(self,a,b,c,d,color): self.tri(a,b,c,color); self.tri(a,c,d,color)
    def box(self,at,size,color, angle=0):
        x,y,z=at; w,h,d=(v/2 for v in size)
        def p(a,b,c): return (x+a*math.cos(angle)-c*math.sin(angle),y+b,z+a*math.sin(angle)+c*math.cos(angle))
        v=[p(a,b,c) for a,b,c in [(-w,-h,-d),(w,-h,-d),(w,h,-d),(-w,h,-d),(-w,-h,d),(w,-h,d),(w,h,d),(-w,h,d)]]
        for a,b,c,d in [(0,3,2,1),(4,5,6,7),(0,4,7,3),(1,2,6,5),(3,7,6,2),(0,1,5,4)]: self.quad(v[a],v[b],v[c],v[d],color)
    def cone(self,at,height,radius,top,color,segments=10):
        x,y,z=at
        for i in range(segments):
            a=i*math.tau/segments; b=(i+1)*math.tau/segments
            p=(x+math.cos(a)*radius,y,z+math.sin(a)*radius); q=(x+math.cos(b)*radius,y,z+math.sin(b)*radius)
            r=(x+math.cos(b)*top,y+height,z+math.sin(b)*top); s=(x+math.cos(a)*top,y+height,z+math.sin(a)*top)
            self.quad(q,p,s,r,color)
            self.tri((x,y,z),p,q,color)
            if top: self.tri((x,y+height,z),r,s,color)
    def ellipsoid(self,at,scale,color,seed=0,segments=10,rings=6):
        rng=random.Random(seed)
        offsets=[[rng.uniform(.93,1.07) for _ in range(segments)] for _ in range(rings+1)]
        offsets[0]=[1.0]*segments; offsets[-1]=[1.0]*segments
        def p(j,i):
            theta=j*math.pi/rings; phi=(i%segments)*math.tau/segments
            k=offsets[j][i%segments]
            return tuple(at[c]+scale[c]*k*v for c,v in enumerate((math.sin(theta)*math.cos(phi),math.cos(theta),math.sin(theta)*math.sin(phi))))
        for j in range(rings):
            for i in range(segments):
                a,b,c,d=p(j,i),p(j,i+1),p(j+1,i+1),p(j+1,i)
                if j>0: self.tri(a,b,d,color); self.parts[color][1][-9:] = [v for q in (a,b,d) for v in norm(tuple((q[k]-at[k])/(scale[k]*scale[k]) for k in range(3)))]
                if j<rings-1: self.tri(b,c,d,color); self.parts[color][1][-9:] = [v for q in (b,c,d) for v in norm(tuple((q[k]-at[k])/(scale[k]*scale[k]) for k in range(3)))]
    def beam(self,a,b,width,color):
        axis=norm(sub(b,a)); right=norm(cross(axis,(0,1,0) if abs(axis[1])<.99 else (1,0,0)))
        up=norm(cross(axis,right)); w=width/2
        aa=[add(a,add(mul(right,i*w),mul(up,j*w))) for i,j in [(-1,-1),(1,-1),(1,1),(-1,1)]]
        bb=[add(p,sub(b,a)) for p in aa]
        self.quad(*aa[::-1],color);self.quad(*bb,color)
        for i in range(4): self.quad(aa[i],aa[(i+1)%4],bb[(i+1)%4],bb[i],color)
    def roof(self,at,w,h,d):
        x,y,z=at
        a=(x-w/2,y,z-d/2);b=(x+w/2,y,z-d/2);c=(x,y+h,z-d/2)
        e=(x-w/2,y,z+d/2);f=(x+w/2,y,z+d/2);g=(x,y+h,z+d/2)
        self.tri(a,c,b,'roof_dark');self.tri(e,f,g,'roof_dark')
        self.quad(a,e,g,c,'roof');self.quad(c,g,f,b,'roof');self.quad(a,b,f,e,'roof_dark')
        for t in [0,.33,.66,1]:
            zz=z-d/2+t*d
            self.beam((x-w/2-.02,y+.025,zz),(x,y+h+.025,zz),.055,'roof_dark')
            self.beam((x,y+h+.025,zz),(x+w/2+.02,y+.025,zz),.055,'roof_dark')
    def save(self,name):
        blob=bytearray();views=[];accessors=[];primitives=[];materials=[]
        def accessor(values,kind='VEC3'):
            # Canonical micrometre precision removes irrelevant libm differences across desktop OSes.
            values=[round(v,6) if abs(v)>=1e-6 else 0.0 for v in values]
            while len(blob)%4: blob.append(0)
            offset=len(blob);blob.extend(struct.pack('<'+'f'*len(values),*values))
            views.append({'buffer':0,'byteOffset':offset,'byteLength':len(values)*4,'target':34962})
            item={'bufferView':len(views)-1,'componentType':5126,'count':len(values)//3,'type':kind,
                  'min':[min(values[i::3]) for i in range(3)],'max':[max(values[i::3]) for i in range(3)]}
            accessors.append(item);return len(accessors)-1
        for color,(p,n) in self.parts.items():
            rgb=[int(COLORS[color][i:i+2],16)/255 for i in (0,2,4)]
            linear=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in rgb]
            mat={'name':color,'pbrMetallicRoughness':{'baseColorFactor':linear+[1], 'metallicFactor':0,'roughnessFactor':.9}}
            if color=='lamp': mat['emissiveFactor']=[.45,.25,.08]
            materials.append(mat)
            primitives.append({'attributes':{'POSITION':accessor(p),'NORMAL':accessor(n)},'material':len(materials)-1,'mode':4})
        doc={'asset':{'version':'2.0','generator':'Original Starlight Village Kit v1'},'scene':0,'scenes':[{'nodes':[0]}],
             'nodes':[{'name':name,'mesh':0}],'meshes':[{'name':name,'primitives':primitives}],
             'materials':materials,'buffers':[{'byteLength':len(blob)}],'bufferViews':views,'accessors':accessors}
        data=json.dumps(doc,separators=(',',':')).encode()
        data+=b' '*((-len(data))%4);blob+=b'\0'*((-len(blob))%4)
        result=struct.pack('<III',0x46546c67,2,12+8+len(data)+8+len(blob))+struct.pack('<II',len(data),0x4e4f534a)+data+struct.pack('<II',len(blob),0x004e4942)+blob
        (DEST/(name+'.glb')).write_bytes(result)
        return {'file':name+'.glb','sha256':hashlib.sha256(result).hexdigest(),'triangles':sum(len(v[0])//9 for v in self.parts.values())}

def models():
    out={}
    m=Model();m.box((0,.15,0),(3.5,.3,3),'stone');m.box((0,1.35,0),(3.1,2.4,2.7),'plaster');m.roof((0,2.55,0),3.8,1.3,3.4)
    for x in [-1.5,1.5]: m.box((x,1.4,1.39),(.13,2.3,.14),'timber')
    m.box((0,1,1.39),(.85,1.7,.16),'door');m.box((.27,1.03,1.51),(.07,.07,.08),'flower')
    for x in [-1,1]:
        m.box((x,1.7,1.4),(.61,.71,.1),'timber');m.box((x,1.72,1.47),(.45,.53,.055),'glass');m.box((x,1.72,1.51),(.045,.56,.04),'wood')
        m.box((x,1.72,1.51),(.49,.04,.04),'wood');m.box((x,1.28,1.6),(.76,.12,.35),'wood')
    m.box((0,.16,1.85),(1.35,.22,.8),'stone');m.box((1.0,3.4,-.65),(.45,1.25,.5),'stone');m.box((1.0,4.02,-.65),(.58,.12,.62),'stone_dark');out['cottage']=m
    for name,pine in [('broadleaf',False),('pine',True)]:
        m=Model();m.cone((0,0,0),2.4,.25,.14,'timber',8)
        if pine:
            for y,r in [(1.0,1.25),(1.8,1.05),(2.55,.75)]:m.cone((0,y,0),1.45,r,0,'pine',10)
        else:
            for j,(at,sz) in enumerate([((0,2.65,0),(1.2,1.2,1.12)),((-.8,2.1,.2),(.85,.9,.84)),((.75,2.25,-.2),(.83,.9,.91))]):m.ellipsoid(at,sz,'leaves_light' if j==1 else 'leaves',j)
        out[name]=m
    m=Model();m.ellipsoid((0,.45,0),(1.0,.65,.76),'stone',5);m.ellipsoid((.6,.22,.3),(.48,.34,.43),'stone_dark',7);out['rock_cluster']=m
    m=Model()
    for j,(x,z) in enumerate([(-.4,0),(.25,.22),(0,-.25),(.5,-.2),(-.15,.4)]):
        m.cone((x,0,z),.42,.035,.018,'leaves',5)
        for a in range(5):m.ellipsoid((x+.105*math.cos(a*math.tau/5),.43,z+.105*math.sin(a*math.tau/5)),(.12,.045,.09),'flower' if j%2 else 'petal',j+a,6,3)
        m.ellipsoid((x,.47,z),(.06,.04,.06),'flower',j,6,3)
    out['flower_patch']=m
    m=Model()
    for z in [-.9,0,.9]:m.box((0,.12,z),(3.4,.24,.86),'wood')
    for x in [-1.65,1.65]:
        for z in [-1.3,0,1.3]:m.box((x,.7,z),(.14,1.4,.14),'timber')
        m.box((x,1.18,0),(.13,.13,2.8),'wood')
    out['bridge']=m
    m=Model()
    for x in [-1,1]:m.box((x,.62,0),(.14,1.24,.14),'timber');m.box((x,1.26,0),(.23,.07,.23),'wood')
    for y in [.4,.9]:m.box((0,y,0),(2,.12,.1),'wood')
    out['fence']=m
    m=Model();m.box((0,1.05,0),(.12,2.1,.12),'timber');m.box((.23,2.02,0),(.58,.12,.12),'wood');m.box((.44,1.78,0),(.35,.47,.35),'metal');m.box((.44,1.8,0),(.28,.29,.37),'lamp');m.roof((.44,2.02,0),.48,.21,.48);out['lantern']=m
    m=Model();m.box((0,.62,0),(.14,1.24,.14),'timber');m.box((0,1.23,0),(1.3,.43,.13),'door')
    for x in [-.25,0,.25]:m.box((x,1.23,.08),(.07,.15,.015),'lamp')
    out['signpost']=m
    m=Model();m.cone((0,0,0),.3,.52,.45,'stone',12);m.box((0,.9,0),(.2,1.35,.2),'wood');m.cone((0,1.2,0),.5,.4,.38,'wood',10);m.box((0,1.27,.4),(.37,.38,.08),'door');m.box((0,1.27,.45),(.19,.2,.03),'flower');m.box((0,1.1,0),(1.3,.13,.13),'timber');out['training_dummy']=m
    m=Model();m.cone((0,0,0),.3,2.4,2.4,'stone',24);m.cone((0,.3,0),.18,2.1,2.1,'stone_dark',24);m.cone((0,.48,0),.08,1.95,1.95,'stone',24);out['lookout_deck']=m
    m=Model();m.cone((0,0,0),.3,.62,.55,'stone',10);m.cone((0,.3,0),1.0,.33,.26,'stone_dark',8);m.ellipsoid((0,1.4,0),(.42,.42,.42),'lamp',3,10,5);out['beacon']=m
    return out

def main():
    DEST.mkdir(parents=True,exist_ok=True)
    records=[model.save(name) for name,model in models().items()]
    manifest={'version':1,'origin':'Original geometry authored for this repository; no third-party asset pack.',
              'units':'metres','up_axis':'+Y','license':'CC0-1.0 for newly authored village geometry; separate inherited robot terms remain in practice-asset-notes.md',
              'scope':'Reusable production reference kit, not a claim of final commercial visual acceptance.', 'assets':records}
    (DEST/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('WORLD ASSETS:',len(records),'GLB files,',sum(r['triangles'] for r in records),'triangles')
if __name__=='__main__':main()
