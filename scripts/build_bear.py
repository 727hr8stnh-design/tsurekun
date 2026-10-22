"""Photo-guided, stylized white bear. Pure Python GLB generator, Y-up."""
import math, json, struct, random, sys
outfit=sys.argv[1] if len(sys.argv)>1 else "vest"
if outfit not in ("vest","sweater","shirt","bare"):raise SystemExit("Unknown outfit")
from pathlib import Path
random.seed(18)
buf=bytearray();views=[];acc=[];meshes=[];nodes=[]
def data(vals,typ,n,component=5126):
 while len(buf)%4:buf.append(0)
 offset=len(buf);flat=[v for row in vals for v in row] if n>1 else vals
 raw=struct.pack('<'+('f' if component==5126 else 'I')*len(flat),*flat);buf.extend(raw)
 views.append({'buffer':0,'byteOffset':offset,'byteLength':len(raw)})
 a={'bufferView':len(views)-1,'componentType':component,'count':len(vals),'type':typ}
 if typ=='VEC3':a.update(min=[min(x[i] for x in vals) for i in range(3)],max=[max(x[i] for x in vals) for i in range(3)])
 acc.append(a);return len(acc)-1
materials=[]
for name,c,rough in [('ivory',[.88,.865,.79,1],.96),('cream',[.98,.965,.9,1],1),('ear',[.73,.69,.59,1],1),('eyes',[.018,.013,.01,1],.16),('nose',[.012,.016,.018,1],.22),('mouth',[.20,.13,.10,1],.95),('shine',[1,1,1,1],.1)]:
 materials.append({'name':name,'pbrMetallicRoughness':{'baseColorFactor':c,'metallicFactor':0,'roughnessFactor':rough}})
def ell(name,center,scale,mat=0,fur=False,parent=None):
 pos=[];norm=[];idx=[];segs=40;rings=28
 for j in range(rings+1):
  p=math.pi*j/rings
  for i in range(segs+1):
   t=2*math.pi*i/segs;x=math.sin(p)*math.cos(t);y=math.cos(p);z=math.sin(p)*math.sin(t)
   noise=1+(.008*math.sin(i*13+j*17)+.004*math.sin(i*23-j*11) if fur else 0)
   pos.append([x*scale[0]*noise,y*scale[1]*noise,z*scale[2]*noise]);n=[x/scale[0],y/scale[1],z/scale[2]];l=math.sqrt(sum(v*v for v in n));norm.append([v/l for v in n])
 for j in range(rings):
  for i in range(segs):
   a=j*(segs+1)+i;b=a+segs+1;idx.extend([a,a+1,b,a+1,b+1,b])
 pa=data(pos,'VEC3',3);no=data(norm,'VEC3',3);ind=data(idx,'SCALAR',1,5125)
 meshes.append({'name':name,'primitives':[{'attributes':{'POSITION':pa,'NORMAL':no},'indices':ind,'material':mat}]})
 node={'name':name,'mesh':len(meshes)-1,'translation':center};nodes.append(node);ni=len(nodes)-1
 if parent is not None:nodes[parent].setdefault('children',[]).append(ni)
 return ni
nodes.append({'name':'Bear_Y_up','children':[]});root=0
body=ell('pear_shaped_body',[0,.79,-.025],[.535,.65,.485],0,True,root)
# Open knitted vest shell follows the fuller torso, with side armholes.
for name,color in [('cocoa_knit',[.27,.145,.075,1]),('oat_knit',[.89,.81,.62,1])]:
 materials.append({'name':name,'doubleSided':True,'pbrMetallicRoughness':{'baseColorFactor':color,'metallicFactor':0,'roughnessFactor':1}})
vp=[];vn=[];groups=[[],[]];rows=160;cols=192
for j in range(rows+1):
 y=.31+j/rows*1.035
 radius=math.sqrt(max(.001,1-((y-.79)/.65)**2))
 for i in range(cols+1):
  a=i/cols*2*math.pi
  # Scoop the front neckline rather than ending at a horizontal cut.
  y=.31+j/rows*(1.035-.13*max(0,math.sin(a))**2)
  radius=math.sqrt(max(.001,1-((y-.79)/.65)**2))
  knit=.0028*math.cos(i*math.pi)*math.cos(j*math.pi)+.0015*math.sin(i*2+j*2)
  x=(.552*radius+knit)*math.cos(a);z=(.502*radius+knit)*math.sin(a)
  vp.append([x,y,z-.025]);n=[x/.552**2,(y-.79)/.65**2,z/.502**2];l=math.sqrt(sum(v*v for v in n));vn.append([v/l for v in n])
for j in range(rows):
 y=.31+(j+.5)/rows*1.035
 # Cocoa base with broad cream horizontal stripes and cream lower edging.
 mat=1 if y<.35 or .49<y<.57 or .76<y<.84 or 1.02<y<1.10 else 0
 for i in range(cols):
  a=(i+.5)/cols*2*math.pi
  # Open armholes on both sides, below the shoulder straps.
  yy=.31+(j+.5)/rows*(1.035-.13*max(0,math.sin(a))**2)
  side_angle=math.atan2(math.sin(a),abs(math.cos(a)))
  if outfit in ('vest','bare') and ((yy-1.075)/.195)**2+(side_angle/.66)**2<1:continue
  n=j*(cols+1)+i;m=n+cols+1
  groups[mat].extend([n,m,n+1,n+1,m,m+1])
pa=data(vp,'VEC3',3);no=data(vn,'VEC3',3);pr=[]
for k,indices in enumerate(groups):pr.append({'attributes':{'POSITION':pa,'NORMAL':no},'indices':data(indices,'SCALAR',1,5125),'material':7+k})
meshes.append({'name':'brown_and_cream_knitted_vest','primitives':pr});nodes.append({'name':'striped_sleeveless_vest','mesh':len(meshes)-1});nodes[root]['children'].append(len(nodes)-1)
# Rounded knitted binding follows the actual curved openings.
def shell_point(a,y):
 r=math.sqrt(max(.001,1-((y-.79)/.65)**2))
 return [.556*r*math.cos(a),y,.506*r*math.sin(a)-.025]
def binding(name,path,radius,material):
 pos=[];norm=[];indices=[];N=len(path)
 for i,c in enumerate(path):
  prev=path[(i-1)%N];nxt=path[(i+1)%N];t=[nxt[k]-prev[k] for k in range(3)];l=math.sqrt(sum(x*x for x in t));t=[x/l for x in t]
  ref=[0,1,0] if abs(t[1])<.9 else [0,0,1]
  u=[t[1]*ref[2]-t[2]*ref[1],t[2]*ref[0]-t[0]*ref[2],t[0]*ref[1]-t[1]*ref[0]];l=math.sqrt(sum(x*x for x in u));u=[x/l for x in u]
  v=[t[1]*u[2]-t[2]*u[1],t[2]*u[0]-t[0]*u[2],t[0]*u[1]-t[1]*u[0]]
  for j in range(10):
   a=j/10*2*math.pi;n=[math.cos(a)*u[k]+math.sin(a)*v[k] for k in range(3)]
   pos.append([c[k]+radius*n[k] for k in range(3)]);norm.append(n)
 for i in range(N):
  for j in range(10):
   a=i*10+j;b=((i+1)%N)*10+j;c=i*10+(j+1)%10;d=((i+1)%N)*10+(j+1)%10
   indices.extend([a,b,c,c,b,d])
 meshes.append({'name':name,'primitives':[{'attributes':{'POSITION':data(pos,'VEC3',3),'NORMAL':data(norm,'VEC3',3)},'indices':data(indices,'SCALAR',1,5125),'material':material}]})
 nodes.append({'name':name,'mesh':len(meshes)-1});nodes[root]['children'].append(len(nodes)-1)
for side in [0,math.pi]:
 path=[]
 for i in range(160):
  t=i/160*2*math.pi;a=side+.66*math.cos(t);y=1.075+.195*math.sin(t)
  path.append(shell_point(a,y))
 binding('rounded_armhole_binding',path,.018,7)
path=[]
for i in range(192):
 a=i/192*2*math.pi;path.append(shell_point(a,1.345-.13*max(0,math.sin(a))**2))
binding('round_scooped_neckline',path,.022,8)
head=ell('round_head',[0,1.73,.015],[.59,.54,.43],1,True,root)
for side in [-1,1]:
 ell('round_ear',[side*.46,.35,-.025],[.15,.16,.105],1,True,head)
 ell('inner_ear',[side*.46,.35,.073],[.08,.09,.035],2,False,head)
 ell('black_eye',[side*.225,.038,.391],[.061,.079,.039],3,False,head)
 ell('eye_glint',[side*.225-.014,.065,.425],[.014,.018,.008],6,False,head)
 ell('muzzle_cheek',[side*.108,-.13,.388],[.19,.155,.16],1,True,head)
 # The shoulder is the pivot; arm geometry extends down from it.
 shoulder=len(nodes)
 nodes.append({'name':'arm_left' if side<0 else 'arm_right','translation':[side*.47,1.105,-.045],'children':[]})
 nodes[root]['children'].append(shoulder)
 ell('continuous_soft_arm',[side*.025,-.245,0],[.18,.35,.19],1,True,shoulder)
 # Short legs tuck into the lower body; feet overlap the leg volume.
 leg=ell('short_leg',[side*.225,.31,.015],[.22,.30,.235],0,True,root)
 foot=ell('foot',[0,-.18,.13],[.22,.145,.275],1,True,leg)
 for toe in [-1,1]:
  ell('toe_seam',[toe*.057,.012,.264],[.006,.047,.008],2,False,foot)
 # curved stitched smile segments
 for k in range(9):
  t=k/8;x=side*(.012+t*.11);y=-.225-.027*math.sin(t*math.pi)
  ell('smile_stitch',[x,y,.524-.018*t],[.012,.009,.008],5,False,head)
ell('nose',[0,-.047,.539],[.085,.053,.045],4,False,head)
ell('nose_highlight',[-.021,-.029,.576],[.024,.008,.006],6,False,head)
ell('philtrum',[0,-.16,.536],[.009,.057,.008],5,False,head)
ell('little_tail',[0,.41,-.43],[.135,.14,.13],1,True,root)
# Fine short tufts around silhouette; restrained geometry keeps mobile rendering light.
for k in range(0):
 t=random.uniform(0,2*math.pi);p=random.uniform(.1,math.pi-.1);x=math.sin(p)*math.cos(t);y=math.cos(p);z=math.sin(p)*math.sin(t)
 ell('plush_tuft',[x*.59,y*.54,z*.43],[.016,.025,.015],1,False,head)
# Animation clips: gentle sway and hello, based on actual node transforms.
times=[i/12 for i in range(49)];ti=data(times,'SCALAR',1);animations=[]
for clip,amp in [('01_Sway_4s',.065),('02_Hello_4s',.10)]:
 sam=[];channels=[]
 for ni in [root]+[i for i,n in enumerate(nodes) if n['name'] in ['arm_left','arm_right']]:
  values=[]
  for t in times:
   base=0 if ni==root else (-.10 if nodes[ni]['name']=='arm_left' else .10)
   angle=base+(.025 if ni==root else .055)*math.sin(t*math.pi)
   if clip.startswith('02') and nodes[ni]['name']=='arm_left':angle=-.26+.12*math.sin(2*math.pi*t)
   values.append([0,0,math.sin(angle/2),math.cos(angle/2)])
  ai=data(values,'VEC4',4);sam.append({'input':ti,'output':ai,'interpolation':'LINEAR'});channels.append({'sampler':len(sam)-1,'target':{'node':ni,'path':'rotation'}})
 animations.append({'name':clip,'samplers':sam,'channels':channels})
mouth=ell('talking_mouth',[0,-.245,.538],[.065,.012,.012],5,False,head)
values=[[1,1+4*max(0,math.sin(t*math.pi*6)),1] for t in times]
animations.append({'name':'03_Talk_4s','samplers':[{'input':ti,'output':data(values,'VEC3',3),'interpolation':'LINEAR'}],'channels':[{'sampler':0,'target':{'node':mouth,'path':'scale'}}]})
# Wardrobe changes garment geometry, leaving the same animated bear intact.
if outfit=='bare':
 hidden={'striped_sleeveless_vest','rounded_armhole_binding','round_scooped_neckline'}
 nodes[root]['children']=[n for n in nodes[root]['children'] if nodes[n]['name'] not in hidden]
elif outfit in ('sweater','shirt'):
 materials[7]['pbrMetallicRoughness']['baseColorFactor']=([.52,.19,.26,1] if outfit=='sweater' else [.10,.28,.46,1])
 nodes[root]['children']=[n for n in nodes[root]['children'] if nodes[n]['name']!='rounded_armhole_binding']
 for ni,node in list(enumerate(nodes)):
  if node['name'] not in ('arm_left','arm_right'):continue
  side=-1 if node['name']=='arm_left' else 1
  long=outfit=='sweater'
  ell('long_sleeve' if long else 'short_sleeve',[side*.025,-.19 if long else -.07,0],[.205,.31 if long else .15,.215],7,False,ni)
  ell('knit_cuff' if long else 'shirt_cuff',[side*.025,-.445 if long else -.175,0],[.20,.035,.21],8,False,ni)
g={'asset':{'version':'2.0','generator':'Photo-guided stylized bear v1'},'scene':0,'scenes':[{'nodes':[0]}],'nodes':nodes,'meshes':meshes,'materials':materials,'animations':animations,'buffers':[{'byteLength':len(buf)}],'bufferViews':views,'accessors':acc}
j=json.dumps(g,separators=(',',':')).encode();j+=b' '*(-len(j)%4);buf.extend(b'\0'*(-len(buf)%4));total=12+8+len(j)+8+len(buf)
Path('docs/bear').mkdir(exist_ok=True)
Path('docs/bear/'+('model' if outfit=='vest' else outfit)+'.glb').write_bytes(struct.pack('<4sII',b'glTF',2,total)+struct.pack('<II',len(j),0x4e4f534a)+j+struct.pack('<II',len(buf),0x004e4942)+buf)
print('GLB',total,'bytes',len(nodes),'nodes; 3 animation clips')
