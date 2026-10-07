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
O.append('<g id="forest">')
for i,(x,y) in enumerate(points[1:],1):
 p=parents[i];O.append(f'<path d="{path([p,i])}" fill="none" stroke="#b8d9f1" stroke-width="{.7 if i>120 else 1}" opacity="{.22 if i>120 else .4}"/>')
 if i%5==0 and i>365:
  xx,yy=points[i-1];O.append(f'<path d="M{x:.1f} {y:.1f}L{xx:.1f} {yy:.1f}" stroke="#7fadd5" opacity=".14"/>')
for i,(x,y) in enumerate(points):O.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{max(.9,3.5-i/160):.1f}" fill="{"#ffae78" if i%31==0 else "#e0f2ff"}" opacity="{.55+R.random()*.45:.2f}"/>')
O.append('</g>')
paths=[]
for leaf in [800,660,990,450,875,550,1070]:
 ids=[leaf]
 while parents[ids[-1]]>=0:ids.append(parents[ids[-1]])
 ids.reverse();paths.append(path(ids));O.append(f'<path id="route{len(paths)-1}" d="{paths[-1]}"/>')
O.append('</defs>')
css='text{font-family:Arial,Helvetica,sans-serif}.scene{opacity:0;animation:scene 49s linear infinite}.drift{transform-origin:480px 470px;animation:drift 14s ease-in-out infinite}.trace{stroke-dasharray:1200;stroke-dashoffset:1200;animation:trace 7s ease-in-out infinite}.pulse{transform-origin:480px 694px;animation:pulse 3s ease-out infinite}@keyframes pulse{0%{transform:scale(.5);opacity:.8}100%{transform:scale(2.5);opacity:0}}@keyframes drift{0%,100%{transform:perspective(900px) rotateY(-6deg) rotateZ(-1deg)}50%{transform:perspective(900px) rotateY(6deg) rotateZ(1deg)}}@keyframes trace{0%{stroke-dashoffset:1200}60%,90%{stroke-dashoffset:0}100%{stroke-dashoffset:-1200}}@keyframes scene{0%,13.1%{opacity:1}14.28%,100%{opacity:0}}'
for k in range(7):css+=f'.s{k}{{animation-delay:-{49-k*7}s}}'
css+='@media(prefers-reduced-motion:reduce){.scene{animation:none;opacity:0}.s4{opacity:1}.drift,.trace,.pulse{animation:none}.trace{stroke-dashoffset:0}.motion{display:none}}'
O+=['<style>'+css+'</style>','<rect width="960" height="900" rx="24" fill="#020409"/><rect x="1" y="1" width="958" height="898" rx="23" fill="none" stroke="#26384b"/><ellipse cx="480" cy="470" rx="450" ry="320" fill="url(#bg)"/>']
for i in range(125):
 x=R.randrange(28,934);y=R.randrange(170,726);O.append(f'<circle cx="{x}" cy="{y}" r=".7" fill="#759bb5" opacity=".3"/>')
O.append('<path d="M26 92V26H105M855 26H934V92M26 810V874H105M855 874H934V810" stroke="#527088" fill="none"/><text x="44" y="51" fill="#95adc4" font-size="18" letter-spacing="4">RUFLO / LEARNING ENGINE</text><text x="916" y="51" text-anchor="end" fill="#647f95" font-size="15">CONCEPTUAL</text><g class="drift"><use xlink:href="#forest"/></g>')
for r in [20,47,78]:O.append(f'<circle cx="480" cy="694" r="{r}" fill="none" stroke="#82baff" stroke-dasharray="2 7" opacity=".3"/>')
O.append('<circle class="pulse" cx="480" cy="694" r="28" fill="none" stroke="#75baff"/><circle cx="480" cy="694" r="12" fill="#030817" stroke="#d2eaff" stroke-width="3"/><circle cx="480" cy="694" r="6" fill="#78bdff"/>')
for k,(label,title,l1,l2) in enumerate(S):
 O.append(f'<g class="scene s{k}"><text x="44" y="96" fill="#ffab70" font-size="20" letter-spacing="3">{escape(label)}</text><text x="44" y="151" fill="#f5f8ff" font-size="44" font-weight="700" letter-spacing="-1">{escape(title)}</text><g class="drift">')
 for route in [k,(k+2)%7]:
  d=paths[route];O.append(f'<path class="trace" d="{d}" stroke="url(#route)" stroke-width="10" opacity=".75" fill="none" filter="url(#glow)"/><path class="trace" d="{d}" stroke="url(#route)" stroke-width="2.7" fill="none"/>')
  for delay in [0,1.5,3]:O.append(f'<circle class="motion" r="4" fill="#fff3df"><animateMotion dur="5s" begin="-{delay}s" repeatCount="indefinite" path="{d}"/></circle>')
 O.append('</g>')
 if k==2:
  O.append('<rect x="176" y="372" width="608" height="144" rx="20" fill="#030914" fill-opacity=".94" stroke="#485a72"/><path d="M320 435H640" stroke="#637c94" stroke-dasharray="4 7"/>')
  for x,c,t,vals in [(350,'#54efc0','POSITIVE','300;400;300'),(480,'#e9f5ff','ANCHOR','480;480;480'),(650,'#ff925d','NEGATIVE','580;690;580')]:
   O.append(f'<circle cx="{x}" cy="425" r="12" fill="{c}"><animate class="motion" attributeName="cx" values="{vals}" dur="5s" repeatCount="indefinite"/></circle><text x="{x}" y="483" text-anchor="middle" fill="{c}" font-size="19">{t}</text>')
 O.append(f'<rect x="32" y="744" width="896" height="114" rx="16" fill="#09111c" stroke="#293c50"/><text x="480" y="788" text-anchor="middle" fill="#edf4fd" font-size="27">{escape(l1)}</text><text x="480" y="829" text-anchor="middle" fill="#a9bfd2" font-size="25">{escape(l2)}</text>')
 for j in range(7):O.append(f'<rect x="{347+j*39}" y="875" width="28" height="4" rx="2" fill="{"#ff9e64" if j==k else "#2b3e51"}"/>')
 O.append('</g>')
O.append('</svg>');svg=''.join(O);ET.fromstring(svg);(P/'learning-trajectories-cosmos.svg').write_text(svg);print(len(points),'nodes;',len(svg),'bytes; XML valid')
