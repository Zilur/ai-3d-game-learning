"""Create an original, tiny skinned glTF teaching fixture; standard library only.
No third-party model or motion. Not an anatomy, retargeting or production-art benchmark.
"""
from __future__ import annotations
import base64
import json
import math
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[1]

def build() -> dict:
    data = bytearray(); views = []; accessors = []
    def accessor(values, fmt, component, kind, count, bounds=False):
        while len(data) % 4: data.append(0)
        offset = len(data)
        for value in values: data.extend(struct.pack('<'+fmt, *value))
        views.append({'buffer': 0, 'byteOffset': offset, 'byteLength': len(data)-offset})
        item = {'bufferView': len(views)-1, 'componentType': component, 'count': count, 'type': kind}
        if bounds:
            item['min'] = [min(v[i] for v in values) for i in range(len(values[0]))]
            item['max'] = [max(v[i] for v in values) for i in range(len(values[0]))]
        accessors.append(item)
        return len(accessors)-1
    positions=[]; normals=[]; joints=[]; weights=[]; indices=[]
    # Rigidly weighted cubes are enough to expose a genuine skin/bone relationship.
    pieces=[((0,1.1,0),(.65,.75,.4),0),((0,1.8,0),(.5,.5,.5),0),
            ((-.57,1.17,0),(.22,.68,.25),1),((.57,1.17,0),(.22,.68,.25),2),
            ((-.2,.4,0),(.25,.8,.28),3),((.2,.4,0),(.25,.8,.28),4)]
    faces=[((1,0,0),[(1,-1,-1),(1,1,-1),(1,1,1),(1,-1,1)]),
           ((-1,0,0),[(-1,-1,1),(-1,1,1),(-1,1,-1),(-1,-1,-1)]),
           ((0,1,0),[(-1,1,-1),(-1,1,1),(1,1,1),(1,1,-1)]),
           ((0,-1,0),[(-1,-1,1),(-1,-1,-1),(1,-1,-1),(1,-1,1)]),
           ((0,0,1),[(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]),
           ((0,0,-1),[(1,-1,-1),(-1,-1,-1),(-1,1,-1),(1,1,-1)])]
    for center, size, joint in pieces:
        for normal, corners in faces:
            start=len(positions)
            for c in corners:
                positions.append(tuple(center[i]+c[i]*size[i]/2 for i in range(3)))
                normals.append(normal); joints.append((joint,0,0,0)); weights.append((1,0,0,0))
            indices.extend([(start,),(start+1,),(start+2,),(start,),(start+2,),(start+3,)])
    attrs={'POSITION':accessor(positions,'3f',5126,'VEC3',len(positions),True),
           'NORMAL':accessor(normals,'3f',5126,'VEC3',len(normals)),
           'JOINTS_0':accessor(joints,'4H',5123,'VEC4',len(joints)),
           'WEIGHTS_0':accessor(weights,'4f',5126,'VEC4',len(weights))}
    index=accessor(indices,'H',5123,'SCALAR',len(indices))
    centers=[(0,1.1,0),(-.57,1.5,0),(.57,1.5,0),(-.2,.8,0),(.2,.8,0)]
    inverse=[]
    for x,y,z in centers: inverse.append((1,0,0,0,0,1,0,0,0,0,1,0,-x,-y,-z,1))
    bind=accessor(inverse,'16f',5126,'MAT4',5)
    nodes=[{'name':'LearningRig','children':[1]},
           {'name':'Hip','translation':[0,1.1,0],'children':[2,3,4,5]},
           {'name':'Arm_L','translation':[-.57,.4,0]},
           {'name':'Arm_R','translation':[.57,.4,0]},
           {'name':'Leg_L','translation':[-.2,-.3,0]},
           {'name':'Leg_R','translation':[.2,-.3,0]},
           {'name':'RobotMesh','mesh':0,'skin':0}]
    animations=[]
    for name in ['Idle','Walk','Attack']:
        times=[(i/12,) for i in range(13)]
        ai=accessor(times,'f',5126,'SCALAR',13,True)
        samplers=[]; channels=[]
        for node in [2,3,4,5]:
            values=[]
            for i in range(13):
                if name=='Walk': angle=math.sin(i/12*math.tau)*.6*(1 if node in (2,5) else -1)
                elif name=='Attack': angle=(-1.7*math.sin(i/12*math.pi) if node==3 else 0)
                else: angle=math.sin(i/12*math.tau)*.035
                values.append((math.sin(angle/2),0,0,math.cos(angle/2)))
            out=accessor(values,'4f',5126,'VEC4',13)
            samplers.append({'input':ai,'output':out,'interpolation':'LINEAR'})
            channels.append({'sampler':len(samplers)-1,'target':{'node':node,'path':'rotation'}})
        animations.append({'name':name,'samplers':samplers,'channels':channels})
    return {'asset':{'version':'2.0','generator':'AI3D original teaching fixture v1'},
            'scene':0,'scenes':[{'name':'PracticeRobot','nodes':[0,6]}],'nodes':nodes,
            'skins':[{'name':'LearningSkin','inverseBindMatrices':bind,'joints':[1,2,3,4,5],'skeleton':1}],
            'meshes':[{'name':'WeightedBlocks','primitives':[{'attributes':attrs,'indices':index,'material':0}]}],
            'materials':[{'name':'LearningBlue','pbrMetallicRoughness':{'baseColorFactor':[.23,.52,.68,1],'metallicFactor':0,'roughnessFactor':.82}}],
            'animations':animations,'bufferViews':views,'accessors':accessors,
            'buffers':[{'byteLength':len(data),'uri':'data:application/octet-stream;base64,'+base64.b64encode(data).decode()}]}

if __name__ == '__main__':
    path=ROOT/'game/assets/practice_robot.gltf'
    path.write_text(json.dumps(build(),separators=(',',':'))+'\n',encoding='utf-8')
    print('Original rig fixture generated:',path)
