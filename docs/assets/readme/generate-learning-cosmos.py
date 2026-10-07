"""Deterministic conceptual trajectory animation. Run with Python 3."""
from pathlib import Path
from math import sin,cos,pi,tanh,sqrt
import random,xml.etree.ElementTree as ET
from html import escape
R=random.Random(71); P=Path(__file__).parent
S=[('EXPERIENCE → INTELLIGENCE','Every path tells a story.','Trace actions, observations and outcomes.','Turn completed work into learning signals.'),('TRAJECTORY MEMORY','Remember the whole journey.','Capture the route, not just the final answer.','Recall useful episodes when context returns.'),('CONTRASTIVE AI','Learn from the difference.','Bring positive examples closer in embedding space.','Separate negatives with a contrastive objective.'),('OUTCOME FEEDBACK','Success is a signal.','Score trajectories against explicit task criteria.','Retain corrections alongside useful patterns.'),('LOCAL INTELLIGENCE','No LLM required.','Local vector retrieval and contrastive updates.','Embeddings and learning modules still required.'),('RECALL → ROUTE → ACT','Let experience guide the route.','Use relevant memory to inform the next decision.','Agent execution may still use an LLM.'),('EVALUATE → RETAIN → REPEAT','Close the loop.','Evaluate fresh outcomes before retaining changes.','Learning depends on feedback and configuration.')]
O=['<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="960" height="900" viewBox="0 0 960 900" role="img" aria-labelledby="title desc"><title id="title">Ruflo trajectory learning and contrastive AI</title><desc id="desc">A conceptual seven scene learning loop. Branching trajectories capture actions and outcomes. Contrastive learning draws positive examples closer and separates negatives. Local retrieval and contrastive updates do not require an LLM; embedding models and configured learning modules are required. Agent execution can still use LLM providers. Illustration, not live telemetry.</desc><defs><radialGradient id="bg"><stop stop-color="#0c2033"/><stop offset="1" stop-color="#020409"/></radialGradient><linearGradient id="route" x1="0" y1="1" x2="0" y2="0"><stop stop-color="#69baff"/><stop offset=".45" stop-color="#edf5ff"/><stop offset="1" stop-color="#ff914e"/></linearGradient><filter id="glow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="5"/></filter>']
# Radial tree with 1,093 vertices in a shallow perspective dome.
points=[(480,694)]; parents=[-1]; levels=[[0]]; angles={0:(-pi+.12,-.12)}
for depth in range(1,7):
 level=[]
 for par in levels[-1]:
  lo,hi=angles[par]
  for j in range(3):
   a=lo+(hi-lo)*(j+.5)/3;rad=depth/6
   x=480+432*rad*cos(a); y=694-455*rad*(-sin(a))**.62-42*rad
   x+=R.uniform(-4,4);y+=R.uniform(-4,4)
   idx=len(points);points.append((x,y));parents.append(par);angles[idx]=(lo+(hi-lo)*j/3,lo+(hi-lo)*(j+1)/3);level.append(idx)
 levels.append(level)
def path(ids):
 s=f'M{points[ids[0]][0]:.1f} {points[ids[0]][1]:.1f}'
 for a,b in zip(ids,ids[1:]):
  x,y=points[a];xx,yy=points[b];s+=f' Q{x:.1f} {(y+yy)/2:.1f} {xx:.1f} {yy:.1f}'
 return s
base_points=points[:]
view_paths=[]
view_names=['BRANCHING TRAJECTORIES','HYPERBOLIC POINCARE DISK','CONTRASTIVE CLUSTERS','GRADIENT VECTOR FIELD','NEAREST NEIGHBOR GRAPH','HELICAL MEMORY MANIFOLD','TOROIDAL FEEDBACK']
def linepath(ids,pts):
 return 'M'+'L'.join(f'{pts[i][0]:.1f} {pts[i][1]:.1f}' for i in ids)
def projected(x,y,z):
 yy=y*.78-z*.55;zz=y*.55+z*.78;scale=800/(800+zz)
 return 480+x*scale,450+yy*scale
def geo(a,b):
 p=complex((a[0]-480)/242,(a[1]-450)/242);q=complex((b[0]-480)/242,(b[1]-450)/242)
 w=(q-p)/(1-p.conjugate()*q);out=[]
 for j in range(13):
  v=w*j/12;z=(p+v)/(1+p.conjugate()*v);out.append((480+242*z.real,450+242*z.imag))
 return 'M'+'L'.join(f'{x:.1f} {y:.1f}' for x,y in out)
for camera in range(7):
 pts=[];edges=[];routes=[];extra='';hues=[]
 if camera==0:
  pts=base_points;edges=[(parents[i],i) for i in range(1,len(pts))]
  for leaf in [800,990]:
   ids=[leaf]
   while parents[ids[-1]]>=0:ids.append(parents[ids[-1]])
   routes.append(linepath(ids[::-1],pts))
 elif camera==1:
  pts=[(480,450)];intervals=[(0,2*pi)];last=[0]
  for depth in range(1,6):
   nxt=[]
   for par in last:
    lo,hi=intervals[par]
    for j in range(3):
     angle=lo+(j+.5)*(hi-lo)/3;rr=tanh(depth*.37)*242
     idx=len(pts);pts.append((480+rr*cos(angle),450+rr*sin(angle)));intervals.append((lo+j*(hi-lo)/3,lo+(j+1)*(hi-lo)/3));edges.append((par,idx));nxt.append(idx)
   last=nxt
  for leaf in [200,290]:
   ids=[leaf]
   while ids[-1]>0:ids.append((ids[-1]-1)//3)
   ids.reverse();routes.append(''.join(geo(pts[a],pts[b]).replace('M','L',1) if n else geo(pts[a],pts[b]) for n,(a,b) in enumerate(zip(ids,ids[1:]))))
  extra='<circle cx="480" cy="450" r="244" stroke="#7bd9ff" stroke-width="1.5" fill="none"/><circle cx="480" cy="450" r="250" stroke="#38566e" stroke-dasharray="2 8" fill="none"/>'
 elif camera==2:
  for c,(cx,cy) in enumerate([(285,330),(665,330),(480,606)]):
   for j in range(70):
    angle=j*2.399;rr=11*sqrt(j);pts.append((cx+rr*cos(angle),cy+.7*rr*sin(angle)));hues.append(['#55efc1','#ff9869','#a591ff'][c])
   for j in range(c*70+1,(c+1)*70):edges.append((j,c*70+(j-c*70)//2))
  routes=[linepath([20,8,3,0,140,143,153],pts),linepath([100,84,75,70,140,145,160],pts)]
 elif camera==3:
  for row in range(13):
   for col in range(23):
    x=120+col*32;y=242+row*32;pts.append((x,y));angle=.007*(x-480)+.006*(y-450)
    dx=19*cos(angle);dy=19*sin(angle)
    extra+=f'<path d="M{x} {y}l{dx:.1f} {dy:.1f}m{-dx*.3+dy*.2:.1f} {-dy*.3-dx*.2:.1f}l{dx*.3-dy*.2:.1f} {dy*.3+dx*.2:.1f}l{-dx*.3-dy*.2:.1f} {-dy*.3+dx*.2:.1f}" fill="none" stroke="#7bcbe8" opacity=".65"/>'
  routes=['M125 600C230 600 210 350 400 330S690 580 830 350','M130 290C310 220 365 615 550 565S650 330 830 240']
 elif camera==4:
  for j in range(150):
   angle=j*2.399;rr=24*sqrt(j);pts.append((480+rr*cos(angle)*1.25,450+rr*sin(angle)*.72))
  for i,pnt in enumerate(pts):
   ns=sorted(range(len(pts)),key=lambda j:(pts[j][0]-pnt[0])**2+(pts[j][1]-pnt[1])**2)[1:5]
   edges.extend((i,j) for j in ns if j>i)
  for start in [120,138]:
   ids=[start]
   while ids[-1]>8:
    cur=ids[-1];candidates=[j for j in range(cur)];n=min(candidates,key=lambda j:(pts[j][0]-pts[cur][0])**2+(pts[j][1]-pts[cur][1])**2);ids.append(n)
   routes.append(linepath(ids,pts))
 elif camera==5:
  for j in range(70):
   a=j*.16
   for strand in range(3):pts.append(projected(155*cos(a+strand*2*pi/3),(j-35)*6,155*sin(a+strand*2*pi/3)))
  edges=[(j,j+3) for j in range(len(pts)-3)]+[(j,j+1) for j in range(0,len(pts)-2,3)]
  routes=[linepath(list(range(strand,len(pts),3)),pts) for strand in [0,2]]
 else:
  for i in range(40):
   a=2*pi*i/40
   for j in range(10):
    b=2*pi*j/10;rad=205+65*cos(b);pts.append(projected(rad*cos(a),65*sin(b),rad*sin(a)))
  edges=[(i*10+j,((i+1)%40)*10+j) for i in range(40) for j in range(10)]+[(i*10+j,i*10+(j+1)%10) for i in range(40) for j in range(10)]
  routes=[linepath([((i%40)*10+(i//4+offset)%10) for i in range(61)],pts) for offset in [0,5]]
 O.append(f'<g id="forest{camera}">')
 O.append(extra)
 for a,b in edges:
  d=geo(pts[a],pts[b]) if camera==1 else linepath([a,b],pts)
  O.append(f'<path d="{d}" fill="none" stroke="#a9cce8" stroke-width=".8" opacity=".36"/>')
 for i,(x,y) in enumerate(pts):
  color=hues[i] if hues else ('#ffaf75' if i%29==0 else '#cceeff')
  O.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{1 if camera in [0,3] else 2}" fill="{color}" opacity=".85"/>')
 O.append('</g>');view_paths.append(routes)
O.append('</defs>')
css='text{font-family:Arial,Helvetica,sans-serif}.scene{opacity:0;animation:scene 49s linear infinite}.drift{transform-origin:480px 470px;animation:drift 14s ease-in-out infinite}.trace{stroke-dasharray:1200;stroke-dashoffset:1200;animation:trace 7s ease-in-out infinite}.pulse{transform-origin:480px 694px;animation:pulse 3s ease-out infinite}@keyframes pulse{0%{transform:scale(.5);opacity:.8}100%{transform:scale(2.5);opacity:0}}@keyframes drift{0%,100%{transform:perspective(900px) rotateY(-6deg) rotateZ(-1deg)}50%{transform:perspective(900px) rotateY(6deg) rotateZ(1deg)}}@keyframes trace{0%{stroke-dashoffset:1200}60%,90%{stroke-dashoffset:0}100%{stroke-dashoffset:-1200}}@keyframes scene{0%,13.1%{opacity:1}14.28%,100%{opacity:0}}'
for k in range(7):css+=f'.s{k}{{animation-delay:-{49-k*7}s}}'
css+='@media(prefers-reduced-motion:reduce){.scene{animation:none;opacity:0}.s4{opacity:1}.drift,.trace,.pulse{animation:none}.trace{stroke-dashoffset:0}.motion{display:none}}'
O+=['<style>'+css+'</style>','<rect width="960" height="900" rx="24" fill="#020409"/><rect x="1" y="1" width="958" height="898" rx="23" fill="none" stroke="#26384b"/><ellipse cx="480" cy="470" rx="450" ry="320" fill="url(#bg)"/>']
for i in range(125):
 x=R.randrange(28,934);y=R.randrange(170,726);O.append(f'<circle cx="{x}" cy="{y}" r=".7" fill="#759bb5" opacity=".3"/>')
O.append('<path d="M26 92V26H105M855 26H934V92M26 810V874H105M855 874H934V810" stroke="#527088" fill="none"/><text x="44" y="51" fill="#95adc4" font-size="18" letter-spacing="4">RUFLO / LEARNING ENGINE</text><text x="916" y="51" text-anchor="end" fill="#647f95" font-size="15">CONCEPTUAL</text>')
for k,(label,title,l1,l2) in enumerate(S):
 O.append(f'<g class="scene s{k}"><text x="44" y="96" fill="#ffab70" font-size="20" letter-spacing="3">{escape(label)}</text><text x="44" y="151" fill="#f5f8ff" font-size="44" font-weight="700" letter-spacing="-1">{escape(title)}</text><g class="drift">')
 O.append(f'<use xlink:href="#forest{k}"/>')
 paths=view_paths[k]
 for route in range(len(paths)):
  d=paths[route];O.append(f'<path class="trace" d="{d}" stroke="url(#route)" stroke-width="10" opacity=".75" fill="none" filter="url(#glow)"/><path class="trace" d="{d}" stroke="url(#route)" stroke-width="2.7" fill="none"/>')
  for delay in [0,1.5,3]:O.append(f'<circle class="motion" r="4" fill="#fff3df"><animateMotion dur="5s" begin="-{delay}s" repeatCount="indefinite" path="{d}"/></circle>')
 O.append('</g>')
 O.append(f'<text x="916" y="719" text-anchor="end" fill="#87a6bd" font-size="16" letter-spacing="2">{view_names[k]}</text>')
 if k==2:
  O.append('<rect x="176" y="372" width="608" height="144" rx="20" fill="#030914" fill-opacity=".94" stroke="#485a72"/><path d="M320 435H640" stroke="#637c94" stroke-dasharray="4 7"/>')
  for x,c,t,vals in [(350,'#54efc0','POSITIVE','300;400;300'),(480,'#e9f5ff','ANCHOR','480;480;480'),(650,'#ff925d','NEGATIVE','580;690;580')]:
   O.append(f'<circle cx="{x}" cy="425" r="12" fill="{c}"><animate class="motion" attributeName="cx" values="{vals}" dur="5s" repeatCount="indefinite"/></circle><text x="{x}" y="483" text-anchor="middle" fill="{c}" font-size="19">{t}</text>')
 O.append(f'<rect x="32" y="744" width="896" height="114" rx="16" fill="#09111c" stroke="#293c50"/><text x="480" y="788" text-anchor="middle" fill="#edf4fd" font-size="27">{escape(l1)}</text><text x="480" y="829" text-anchor="middle" fill="#a9bfd2" font-size="25">{escape(l2)}</text>')
 for j in range(7):O.append(f'<rect x="{347+j*39}" y="875" width="28" height="4" rx="2" fill="{"#ff9e64" if j==k else "#2b3e51"}"/>')
 O.append('</g>')
O.append('</svg>');svg=''.join(O);ET.fromstring(svg);(P/'learning-vector-geometries.svg').write_text(svg);print(len(points),'nodes;',len(svg),'bytes; XML valid')
