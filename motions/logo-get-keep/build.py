"""Preserve all uploaded contours and generate a standalone SMIL logo motion."""
from pathlib import Path
import xml.etree.ElementTree as ET
import hashlib,json
ROOT=Path(__file__).resolve().parent
NS='{http://www.w3.org/2000/svg}'
original=ROOT/'original.svg';root=ET.fromstring(original.read_text())
for el in root.iter():
 assert el.tag.rsplit('}',1)[-1] in {'svg','defs','style','g','path'},'Unexpected SVG element'
 assert not any(k.lower().startswith('on') or 'href' in k.lower() for k in el.attrib),'External or executable SVG attribute'
paths=root.findall('.//'+NS+'path');assert len(paths)==15
colors={'cls-1':'#30d949','cls-2':'#fff'}
def plain(p):
 attrs={'d':p.attrib['d'],'fill':colors[p.attrib['class']]}
 return ET.tostring(ET.Element('path',attrs),encoding='unicode')
def anim(typ,keys,values,splines=None):
 if splines is None:splines=['0.2 0.8 0.2 1']*(len(keys)-1)
 return f'<animateTransform attributeName="transform" type="{typ}" dur="10s" begin="0s" fill="freeze" calcMode="spline" keyTimes="{";".join(str(k/10) for k in keys)}" values="{";".join(values)}" keySplines="{";".join(splines)}"/>'
def opacity(keys,values):
 return f'<animate attributeName="opacity" dur="10s" begin="0s" fill="freeze" keyTimes="{";".join(str(k/10) for k in keys)}" values="{";".join(map(str,values))}"/>'
# Original path strings and fills are carried through unchanged.
parts=[]
groups=[('R',[0],(73,220)),('U',[1],(235,220)),('N-upper',[9,10,11],(420,220)),('N-lower',[12,13,14],(250,412)),('I',[2],(383,414)),('N-green',[3],(498,414)),('G',[4],(675,414))]
for i,(name,ids,(cx,cy)) in enumerate(groups):
 delay=i*.045;entry=.08+delay;end=.64+delay
 k=[0,entry,end,end+.11,2.35+delay,2.52+delay,2.78+delay,4.55,5.45,6.6+delay,6.78+delay,7.08+delay,8.2,10]
 vals=['-42 16','-42 16','5 -2','0 0','0 0','14 -4','0 0','0 0','0 0','0 0','5 -1','0 0','0 0','0 0']
 rotkeys=[0,entry,end,end+.11,2.35+delay,2.52+delay,2.78+delay,6.6+delay,6.78+delay,7.08+delay,8.2,10]
 rotvals=['-8','-8','0.6','0','0','-2','0','0','-1.6','0','0','0']
 scaleKeys=[0,end+.11,2.35+delay,2.52+delay,2.78+delay,6.6+delay,6.78+delay,7.08+delay,8.2,10]
 scaleVals=['1','1','1','1.04 0.99','1','1','1.02 0.99','1','1','1']
 shape=''.join(plain(paths[j]) for j in ids)
 parts.append(f'<g id="{name}">'+opacity([0,entry,end,10],[0,0,1,1])+f'<g transform="translate({cx} {cy})"><g>'+anim('translate',k,vals)+'<g>'+anim('rotate',rotkeys,rotvals)+'<g>'+anim('scale',scaleKeys,scaleVals)+f'<g transform="translate({-cx} {-cy})">{shape}</g></g></g></g></g></g>')
get=''.join(plain(paths[j]) for j in [5,6,7,8])
parts.append('<g id="GET">'+opacity([0,.07,.6,4.76,4.96,10],[0,0,1,1,0,0])+'<g>'+anim('translate',[0,.07,.6,.72,4.65,4.84,5,10],['-12 8','-12 8','2 -1','0 0','0 0','9 -8','22 -20','22 -20'])+'<g transform="translate(100 47)"><g>'+anim('scale',[0,.72,4.65,4.89,5,10],['1','1','1','1.1 0.72','1.12 0.65','1.12 0.65'])+f'<g transform="translate(-100 -47)">{get}</g></g></g></g></g>')
keepRoot=ET.fromstring((ROOT/'keep.svg').read_text());keepGroup=ET.tostring(keepRoot.find(NS+'g'),encoding='unicode').replace('ns0:','').replace(' xmlns:ns0="http://www.w3.org/2000/svg"','')
parts.append('<g id="KEEP" opacity="0">'+opacity([0,5,5.055,5.34,10],[0,0,.45,1,1])+'<g>'+anim('translate',[0,5,5.12,5.35,5.47,10],['-18 16','-18 16','5 -2','1 0','0 0','0 0'])+'<g>'+anim('rotate',[0,5,5.12,5.47,10],['-3','-3','.6','0','0'])+keepGroup+'</g></g></g>')
svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="-50 -50 858.5 604.83" width="1518" height="1010" role="img" aria-label="Logo GET RUNNING que muda para KEEP RUNNING em dez segundos. Fundo transparente."><title>GET → KEEP RUNNING — original vector logo motion</title>'+''.join(parts)+'</svg>'
(ROOT/'logo-animated.svg').write_text(svg)
final='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 758.5 504.83">'+''.join(plain(paths[j]) for j in [0,1,2,3,4,9,10,11,12,13,14])+keepGroup+'</svg>'
(ROOT/'keep-running.svg').write_text(final)
js="""'use strict';const $=id=>document.getElementById(id),svg=$('logo').querySelector('svg'),DURATION=10000;let position=0,playing=false,start=0,raf=0;svg.pauseAnimations();function draw(t){position=Math.max(0,Math.min(DURATION,t));svg.setCurrentTime(position/1000);$('timeline').value=position;$('time').textContent=(position/1000).toFixed(1).replace('.',',')+' / 10,0 s'}function pause(){playing=false;cancelAnimationFrame(raf);$('play').textContent=position>=DURATION?'Rever':'Reproduzir'}function tick(now){if(!playing)return;let t=now-start;if(t>=DURATION){draw(DURATION);if($('loop').checked){start=now;draw(0)}else{pause();return}}else draw(t);raf=requestAnimationFrame(tick)}function play(){if(position>=DURATION)draw(0);playing=true;start=performance.now()-position;$('play').textContent='Pausar';raf=requestAnimationFrame(tick)}$('play').onclick=()=>playing?pause():play();$('timeline').oninput=()=>{pause();draw(Number($('timeline').value))};$('backdrop').onchange=()=>{$('logo').dataset.backdrop=$('backdrop').value};document.addEventListener('visibilitychange',()=>{if(document.hidden&&playing)pause()});window.LogoMotion={duration:DURATION,seek(t){pause();draw(t)},play,pause,get position(){return position},get playing(){return playing},get svg(){return svg}};draw(0);if(matchMedia('(prefers-reduced-motion: reduce)').matches)draw(DURATION);else play();"""
html='''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>GET → KEEP / Logo original</title><style>*{box-sizing:border-box}body{background:#121714;color:#fff;margin:0;font-family:Arial,Helvetica,sans-serif}main{max-width:1120px;margin:auto;padding:28px}header{display:flex;justify-content:space-between;gap:20px;align-items:center;margin-bottom:22px}h1{font-size:25px;margin:0;letter-spacing:-1px}header span,p,.controls{font:12px ui-monospace,monospace;line-height:1.6;color:#aab6ae}.board{border-radius:8px;overflow:hidden;background-color:#333;background-image:linear-gradient(45deg,#404740 25%,transparent 25%),linear-gradient(-45deg,#404740 25%,transparent 25%),linear-gradient(45deg,transparent 75%,#404740 75%),linear-gradient(-45deg,transparent 75%,#404740 75%);background-size:32px 32px;background-position:0 0,0 16px,16px -16px,-16px 0}.board[data-backdrop=dark]{background:#121714}.board[data-backdrop=light]{background:#ecefeb}.board svg{width:100%;height:auto;display:block}.controls{display:flex;gap:15px;align-items:center;flex-wrap:wrap;margin-top:20px}button{background:#30d949;color:#102515;border:0;padding:12px 18px;font:inherit;cursor:pointer}label{display:flex;gap:7px;align-items:center}input{accent-color:#30d949}input[type=range]{width:100%;margin-top:18px}output{margin-left:auto}select{font:inherit;background:#29392e;border:1px solid #536759;color:white;padding:7px}a{color:#30d949}button:focus-visible,input:focus-visible,select:focus-visible,a:focus-visible{outline:3px solid white;outline-offset:4px}@media(max-width:600px){main{padding:16px}header{align-items:flex-start;flex-direction:column;gap:8px}h1{font-size:21px}.controls{gap:12px}output{margin-left:0}}</style></head><body><main><header><h1>GET → KEEP RUNNING</h1><span>LOGO ORIGINAL / 10 S / TRANSPARÊNCIA</span></header><div id="logo" class="board" data-backdrop="check">EMBED_SVG</div><div class="controls"><button id="play">Reproduzir</button><label><input id="loop" type="checkbox">Repetir</label><label>Fundo de inspeção<select id="backdrop"><option value="check">Transparência</option><option value="dark">Escuro</option><option value="light">Claro</option></select></label><output id="time">0,0 / 10,0 s</output></div><input id="timeline" type="range" min="0" max="10000" step="1" value="0" aria-label="Posição da animação"><p>O fundo de inspeção pertence apenas ao visualizador. SVG e WebM são transparentes. GET e RUNNING usam os contornos fornecidos; KEEP foi desenhado para acompanhar o estilo do GET.</p><p><a href="logo-animated.svg" download>SVG animado</a> · <a href="keep-running.svg" download>Logo KEEP vetorial</a> · <a href="../../assets/get-keep-logo-transparent.webm" download>WebM com transparência</a></p></main><script>EMBED_SCRIPT</script></body></html>'''
if (ROOT/'get-keep-logo-transparent.webm').is_file():
 html=html.replace('../../assets/get-keep-logo-transparent.webm','get-keep-logo-transparent.webm')
(ROOT/'index.html').write_text(html.replace('EMBED_SVG',svg).replace('EMBED_SCRIPT',js))
(ROOT/'source-manifest.json').write_text(json.dumps({'original_sha256':hashlib.sha256(original.read_bytes()).hexdigest(),'original_path_count':len(paths),'original_colors':colors,'new_word':'KEEP','duration_seconds':10,'swap_seconds':5,'reference_viewbox':root.attrib['viewBox'],'original_contours_preserved':True},indent=2)+'\n')
