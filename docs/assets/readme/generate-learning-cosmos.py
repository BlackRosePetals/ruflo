"""Deterministic conceptual trajectory animation. Run with Python 3."""
from pathlib import Path
from math import sin,cos,pi
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
views=[]; view_paths=[]
view_names=['FRONTAL CANOPY','ISOMETRIC MEMORY','POLAR EMBEDDINGS','SIDE PROFILE','LOCAL VECTOR SPHERE','TRAJECTORY TUNNEL','ORBITAL FEEDBACK']
for camera in range(7):
 points=[]
 for i,(bx,by) in enumerate(base_points):
  u=(bx-480)/432; v=(694-by)/497
  depth=next(d for d,ids in enumerate(levels) if i in ids)
  lo,hi=angles[i]; theta=(lo+hi)/2; r=depth/6
  if camera==0: x,y=bx,by
  elif camera==1:
   x=480+u*340+v*130; y=650-v*370+u*105
  elif camera==2:
   angle=theta*2; x=480+350*r*cos(angle); y=455+240*r*sin(angle)
  elif camera==3:
   x=130+v*680; y=452+u*210*(.4+.6*v)
  elif camera==4:
   angle=theta*2; latitude=(r-.5)*pi
   xx=cos(latitude)*cos(angle); yy=sin(latitude); zz=cos(latitude)*sin(angle)
   scale=1/(1+.22*zz); x=480+340*xx*scale; y=453+222*yy*scale
  elif camera==5:
   angle=theta*2+depth*.35; radius=40+195*r
   x=480+radius*1.65*cos(angle); y=450+radius*sin(angle)
  else:
   angle=theta*2; ring=125+75*r
   x=480+ring*1.7*cos(angle); y=453+ring*.72*sin(angle)+(r-.5)*210
  points.append((x,y))
 views.append(points[:]); O.append(f'<g id="forest{camera}">')
 for i,(x,y) in enumerate(points[1:],1):
  par=parents[i];O.append(f'<path d="{path([par,i])}" fill="none" stroke="#b8d9f1" stroke-width="{.65 if i>120 else 1}" opacity="{.2 if i>120 else .4}"/>')
 for i,(x,y) in enumerate(points):O.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{max(.8,3.5-i/160):.1f}" fill="{"#ffae78" if i%31==0 else "#e0f2ff"}" opacity="{.55+R.random()*.45:.2f}"/>')
 O.append('</g>'); paths=[]
 for leaf in [800,660,990,450,875,550,1070]:
  ids=[leaf]
  while parents[ids[-1]]>=0:ids.append(parents[ids[-1]])
  ids.reverse();paths.append(path(ids))
 view_paths.append(paths)
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
 for route in [k,(k+2)%7]:
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
O.append('</svg>');svg=''.join(O);ET.fromstring(svg);(P/'learning-vector-perspectives.svg').write_text(svg);print(len(points),'nodes;',len(svg),'bytes; XML valid')
