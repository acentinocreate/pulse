"""Build ten-second transparent motion from the two exact supplied SVG assets."""
from pathlib import Path
import xml.etree.ElementTree as ET
import re,json,hashlib
from fontTools.svgLib.path import parse_path
from fontTools.pens.boundsPen import BoundsPen
ROOT=Path(__file__).resolve().parent;NS='{http://www.w3.org/2000/svg}'
ET.register_namespace('',NS[1:-1]);W,H=1920,1080

def anim(typ,keys,values):
 assert len(keys)==len(values) and all(a<b for a,b in zip(keys,keys[1:]))
 return f'<animateTransform attributeName="transform" type="{typ}" dur="10s" begin="0s" fill="freeze" calcMode="spline" keyTimes="{";".join(str(k/10) for k in keys)}" values="{";".join(values)}" keySplines="{";".join(["0.16 0.85 0.18 1"]*(len(keys)-1))}"/>'
def opacity(keys,values):
 return f'<animate attributeName="opacity" dur="10s" begin="0s" fill="freeze" keyTimes="{";".join(str(k/10) for k in keys)}" values="{";".join(map(str,values))}"/>'
assets=[];manifest=[]
for number,color in [(1,'#30d949'),(2,'#e5e1cf')]:
 p=ROOT/f'vector-{number}.svg';r=ET.fromstring(p.read_text())
 for el in r.iter():
  assert el.tag.rsplit('}',1)[-1] in {'svg','defs','style','g','path'}
  assert not any(k.lower().startswith('on') or 'href' in k.lower() for k in el.attrib)
 assert len(r.findall('.//'+NS+'text'))==0
 declared=re.findall(r'fill:\s*(#[a-fA-F0-9]+)',r.find(NS+'defs').find(NS+'style').text);assert declared==[color]
 box=list(map(float,r.attrib['viewBox'].split()));tx=(W-box[2])/2;ty=(H-box[3])/2
 paths=r.findall('.//'+NS+'path');groups=[]
 neutral='' # Static contour layers below provide exact raster endpoints.
 for i,p in enumerate(paths):
  assert not any(k not in {'d','class'} for k in p.attrib)
  pen=BoundsPen(None);parse_path(p.attrib['d'],pen);x0,y0,x1,y1=pen.bounds;cx=(x0+x1)/2;cy=(y0+y1)/2
  plain=ET.tostring(ET.Element('path',{'d':p.attrib['d'],'fill':color}),encoding='unicode')
  delay=i*.024
  if number==1:
   k=[0,.06+delay,.52+delay,.67+delay,1.65+delay,1.79+delay,2.04+delay,2.85+delay,3.00+delay,3.24+delay,4.42+delay,4.60+delay,5.20,10]
   v=['165 -58','165 -58','-10 4','0 0','0 0','32 -28','0 0','0 0','-22 18','0 0','0 0','-48 -16','-48 -16','-48 -16']
   rk=[0,.06+delay,.52+delay,.67+delay,1.65+delay,1.79+delay,2.04+delay,2.85+delay,3+delay,3.24+delay,4.42+delay,4.60+delay,5.20,10]
   rv=['-14','-14','2','0','0','-8','0','0','5','0','0','-9','-9','-9']
   op=opacity([0,.06+delay,.22+delay,4.75,5.1,10],[0,0,1,1,0,0])
  else:
   k=[0,5+delay,5.38+delay,5.53+delay,6.35+delay,6.50+delay,6.77+delay,7.38+delay,7.54+delay,7.80+delay,8.3,10]
   v=['120 54','120 54','-8 -4','0 0','0 0','27 -31','0 0','0 0','-18 17','0 0','0 0','0 0']
   rk=k;rv=['-12','-12','2','0','0','-7','0','0','5','0','0','0']
   op=opacity([0,5+delay,5.15+delay,10],[0,0,1,1])
  groups.append(f'<g id="v{number}-glyph-{i}">'+op+f'<g transform="translate({cx} {cy})">'+neutral+'<g>'+anim('translate',k,v)+'<g>'+anim('rotate',rk,rv)+f'<g transform="translate({-cx} {-cy})">{neutral}{plain}</g></g></g></g></g>')
 if number==1:
  camkeys=[0,1.1,2.50,2.64,2.92,3.45,3.60,3.91,4.65,4.92,5.20,10]
  camv=['0 0','0 0','0 0','66 -38','0 0','0 0','-55 30','0 0','0 0','-620 -18','-2140 -45','-2140 -45']
  rotv=['0','0','0','-4','0','0','3','0','0','-7','-7','-7']
  scalev=['1','1','1','1.15','1','1','1.10','1','1','0.85 1.08','0.85 1.08','0.85 1.08']
 else:
  camkeys=[0,5,5.45,5.70,6.12,6.29,6.58,7.02,7.18,7.43,8.3,10]
  camv=['1040 20','1040 20','-14 -3','0 0','0 0','-48 -20','0 0','0 0','45 30','0 0','0 0','0 0']
  rotv=['-6','-6','1','0','0','-3','0','0','2','0','0','0']
  scalev=['1.08','1.08','1.02','1','1','1.065','1','1','1.05','1','1','1']
 hide='<set attributeName="display" to="none" begin="1.08s" dur="0.54s" fill="remove"/>' if number==1 else '<set attributeName="display" to="none" begin="8.3s" fill="freeze"/>'
 assets.append(f'<g id="vector-{number}" transform="translate({tx} {ty})">'+hide+f'<g transform="translate({box[2]/2} {box[3]/2})">'+neutral+'<g>'+anim('translate',camkeys,camv)+'<g>'+anim('rotate',camkeys,rotv)+'<g>'+anim('scale',camkeys,scalev)+f'<g transform="translate({-box[2]/2} {-box[3]/2})">'+neutral+''.join(groups)+'</g></g></g></g></g></g>')
 show='<set attributeName="display" to="inline" begin="1.08s" dur="0.54s" fill="remove"/>' if number==1 else '<set attributeName="display" to="inline" begin="8.3s" fill="freeze"/>'
 rest=''.join(ET.tostring(ET.Element('path',{'d':p.attrib['d'],'fill':color}),encoding='unicode') for p in paths)
 assets.append(f'<g id="rest-{number}" display="none" transform="translate({tx} {ty})">'+show+rest+'</g>')
 manifest.append({'file':f'vector-{number}.svg','sha256':hashlib.sha256((ROOT/f'vector-{number}.svg').read_bytes()).hexdigest(),'path_count':len(paths),'viewbox':box,'placement':[tx,ty],'fill':color})
svg='<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080" role="img" aria-label="Never give up. transiciona para Nunca desista. Motion de dez segundos, transparente."><title>Never give up. → Nunca desista.</title>'+''.join(assets)+'</svg>'
(ROOT/'motion.svg').write_text(svg)
(ROOT/'manifest.json').write_text(json.dumps({'duration_seconds':10,'transition_seconds':5,'canvas':[1920,1080],'assets':manifest,'all_original_paths_unchanged':True},indent=2)+'\n')
# Reuse the tested player shell; controls stay outside the transparent SVG.
base=(ROOT/'shell.html').read_text().replace('SVG_SLOT',svg)
base=base.replace('GET → KEEP / Logo original','Never give up. → Nunca desista.').replace('<h1>GET → KEEP RUNNING</h1>','<h1>Never give up. → Nunca desista.</h1>')
base=base.replace('GET e RUNNING usam os contornos fornecidos; KEEP foi desenhado para acompanhar o estilo do GET.','Os dois vetores enviados são preservados. Somente os contornos das frases são animados.')
base=base.replace('href="logo-animated.svg"','href="motion.svg"').replace('<a href="keep-running.svg" download>Logo KEEP vetorial</a>','<a href="vector-2.svg" download>Vetor final original</a>').replace('get-keep-logo-transparent.webm','never-give-up-transparent.webm').replace('window.LogoMotion','window.PhraseMotion')
if (ROOT/'never-give-up-transparent.webm').is_file():base=base.replace('../../assets/never-give-up-transparent.webm','never-give-up-transparent.webm')
(ROOT/'index.html').write_text(base)
