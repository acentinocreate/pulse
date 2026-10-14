"""Verify original vector fidelity, transparent rendering and real VP9 alpha decoding."""
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
import threading, subprocess,json,xml.etree.ElementTree as ET,io,sys
from PIL import Image,ImageChops
from playwright.sync_api import sync_playwright
ET.register_namespace('', 'http://www.w3.org/2000/svg')
ROOT=Path(__file__).resolve().parents[1];checks={};errors=[];requests=[]
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=ThreadingHTTPServer(('127.0.0.1',8094),partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=b.new_page(viewport={'width':1600,'height':1200},device_scale_factor=1)
 page.on('pageerror',lambda e:errors.append(str(e)));page.on('request',lambda r:requests.append(r.url))
 page.goto('http://127.0.0.1:8094/motions/logo-get-keep/index.html');page.wait_for_function('window.LogoMotion')
 checks['HTTP startup']=True
 page.evaluate('LogoMotion.seek(1500)');page.screenshot(path=str(ROOT/'assets/logo-motion-inspection.png'))
 export=page.add_style_tag(content='html,body{background:transparent!important}main{max-width:none;width:1518px;padding:0;margin:0}header,.controls,input,p{display:none!important}.board{width:1518px;height:1010px;border-radius:0;background:none!important}.board svg{width:1518px;height:1010px}')
 svg=page.locator('#logo svg');original_frame=svg.screenshot(omit_background=True)
 original=ET.fromstring((ROOT/'motions/logo-get-keep/original.svg').read_text());ns='{http://www.w3.org/2000/svg}'
 expected=[p.attrib['d'] for p in original.findall('.//'+ns+'path')]
 delivered=ET.fromstring((ROOT/'motions/logo-get-keep/logo-animated.svg').read_text());actual=[p.attrib['d'] for p in delivered.findall('.//'+ns+'path')]
 checks['Every original path retained verbatim']=all(d in actual for d in expected) and len(expected)==15
 checks['Original green and white fills preserved']=page.evaluate("[...document.querySelectorAll('#logo path')].filter(p=>!p.closest('#KEEP')).every(p=>['#30d949','#fff'].includes(p.getAttribute('fill')))")
 original.attrib.update({'viewBox':'-50 -50 858.5 604.83','width':'1518','height':'1010'})
 ref=b.new_page(viewport={'width':1518,'height':1010});ref.set_content('<style>html,body{margin:0;background:transparent}svg{display:block}</style>'+ET.tostring(original,encoding='unicode'));ref_frame=ref.locator('svg').screenshot(omit_background=True)
 a=Image.open(io.BytesIO(original_frame)).convert('RGBA');z=Image.open(io.BytesIO(ref_frame)).convert('RGBA')
 checks['Resting GET logo matches supplied SVG pixel for pixel']=all(ImageChops.difference(a,z).getchannel(c).getbbox() is None for c in 'RGBA')
 checks['Transparent background and visible logo']=a.getpixel((0,0))[3]==0 and a.getchannel('A').getextrema()==(0,255)
 page.evaluate('LogoMotion.seek(4850)');checks['GET visible before midpoint']=page.evaluate("getComputedStyle(document.getElementById('GET')).opacity>0.1 && getComputedStyle(document.getElementById('KEEP')).opacity==='0'")
 page.evaluate('LogoMotion.seek(5400)');checks['KEEP replaces GET after midpoint']=page.evaluate("getComputedStyle(document.getElementById('GET')).opacity==='0' && Number(getComputedStyle(document.getElementById('KEEP')).opacity)>0.99")
 # RUNNING has no active transforms during the swap: its contour placement stays fixed.
 page.evaluate('LogoMotion.seek(4800)');before=page.evaluate("[...document.querySelectorAll('#R,#U,#N-upper,#N-lower,#I,#N-green,#G')].map(g=>g.getBBox().toJSON?g.getBBox().toJSON():[g.getBBox().x,g.getBBox().y,g.getBBox().width,g.getBBox().height])")
 page.evaluate('LogoMotion.seek(5400)');after=page.evaluate("[...document.querySelectorAll('#R,#U,#N-upper,#N-lower,#I,#N-green,#G')].map(g=>g.getBBox().toJSON?g.getBBox().toJSON():[g.getBBox().x,g.getBBox().y,g.getBBox().width,g.getBBox().height])")
 checks['RUNNING placement preserved through word exchange']=before==after
 page.evaluate('LogoMotion.seek(10000)');checks['Duration ten seconds']=page.evaluate('LogoMotion.position===10000&&LogoMotion.duration===10000')
 final=svg.screenshot(omit_background=True);(ROOT/'assets/keep-running-transparent.png').write_bytes(final)
 checks['Final still has alpha']=Image.open(io.BytesIO(final)).convert('RGBA').getchannel('A').getextrema()==(0,255)
 if '--reuse-exports' not in sys.argv:
  proc=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','image2pipe','-vcodec','png','-framerate','30','-i','-','-an','-c:v','libvpx-vp9','-deadline','good','-cpu-used','4','-row-mt','1','-threads','4','-b:v','0','-crf','22','-pix_fmt','yuva420p','-auto-alt-ref','0',str(ROOT/'assets/get-keep-logo-transparent.webm')],stdin=subprocess.PIPE)
  for i in range(300):
   page.evaluate('(t)=>LogoMotion.seek(t)',i*1000/30);proc.stdin.write(svg.screenshot(omit_background=True))
  proc.stdin.close();checks['Transparent WebM rendering']=proc.wait()==0
 else: checks['Transparent WebM rendering']=(ROOT/'assets/get-keep-logo-transparent.webm').is_file()
 export.evaluate('(e)=>e.remove()');page.set_viewport_size({'width':390,'height':844});page.evaluate('LogoMotion.seek(9000)');checks['Mobile no horizontal overflow']=page.evaluate('document.documentElement.scrollWidth<=innerWidth')
 page.evaluate('LogoMotion.seek(10000)');page.click('#play');page.wait_for_timeout(120);checks['Replay']=page.evaluate('LogoMotion.playing&&LogoMotion.position<1000')
 page.click('#play');checks['Pause']=page.evaluate('!LogoMotion.playing')
 page.evaluate('LogoMotion.seek(9800);document.querySelector("#loop").checked=false;LogoMotion.play()');page.wait_for_timeout(400);checks['Playback completion']=page.evaluate('!LogoMotion.playing&&LogoMotion.position===10000')
 page.evaluate('document.querySelector("#loop").checked=true;LogoMotion.seek(9800);LogoMotion.play()');page.wait_for_timeout(400);checks['Repeat']=page.evaluate('LogoMotion.playing&&LogoMotion.position<1000');page.evaluate('LogoMotion.pause()')
 page.emulate_media(reduced_motion='reduce');page.reload();page.wait_for_function('window.LogoMotion');checks['Reduced motion pauses on final logo']=page.evaluate('!LogoMotion.playing&&LogoMotion.position===10000')
 # Standalone SVG runs natively, without the HTML controller.
 standalone=b.new_page();standalone.goto('http://127.0.0.1:8094/motions/logo-get-keep/logo-animated.svg');checks['Standalone animated SVG loads']=standalone.evaluate('typeof document.documentElement.setCurrentTime==="function"');standalone.evaluate('document.documentElement.pauseAnimations();document.documentElement.setCurrentTime(10)');checks['Standalone SVG finishes with KEEP']=standalone.evaluate("Number(getComputedStyle(document.getElementById('KEEP')).opacity)>.99&&getComputedStyle(document.getElementById('GET')).opacity==='0'")
 local=b.new_page()
 try:local.goto((ROOT/'motions/logo-get-keep/index.html').as_uri(),timeout=5000);local.wait_for_function('window.LogoMotion',timeout=2000);file_status='Passed'
 except Exception as e:file_status='Blocked: '+str(e).splitlines()[0]
 checks['No JavaScript errors']=not errors;checks['No ordinary remote requests']=all(r.startswith('http://127.0.0.1:8094/') for r in requests)
 b.close()
server.shutdown()
video=ROOT/'assets/get-keep-logo-transparent.webm'
probe=json.loads(subprocess.check_output(['ffprobe','-v','quiet','-show_format','-show_streams','-of','json',str(video)]));v=probe['streams'][0]
checks['WebM dimensions and duration']=v['width']==1518 and v['height']==1010 and abs(float(probe['format']['duration'])-10)<.01
checks['WebM alpha signaling']=v.get('tags',{}).get('alpha_mode')=='1'
# Explicit libvpx decoder is required: FFmpeg's native VP9 decoder can discard alpha.
frame=subprocess.check_output(['ffmpeg','-loglevel','error','-c:v','libvpx-vp9','-ss','1.5','-i',str(video),'-frames:v','1','-f','image2pipe','-vcodec','png','-pix_fmt','rgba','-'])
rgba=Image.open(io.BytesIO(frame)).convert('RGBA');checks['Decoded WebM has real transparent pixels']=rgba.getpixel((0,0))[3]==0 and rgba.getchannel('A').getextrema()==(0,255)
cmd=['ffmpeg','-y','-loglevel','error','-c:v','libvpx-vp9','-i',str(video),'-vf','format=yuva420p,scale=1080:-2:flags=lanczos,pad=1080:1920:0:(oh-ih)/2:color=black@0','-an','-c:v','libvpx-vp9','-deadline','good','-cpu-used','4','-row-mt','1','-threads','4','-b:v','0','-crf','22','-pix_fmt','yuva420p','-auto-alt-ref','0',str(ROOT/'assets/get-keep-logo-transparent-9x16.webm')]
checks['Portrait transparent render']=subprocess.call(cmd)==0 if '--reuse-exports' not in sys.argv else (ROOT/'assets/get-keep-logo-transparent-9x16.webm').is_file()
portrait=ROOT/'assets/get-keep-logo-transparent-9x16.webm';pr=json.loads(subprocess.check_output(['ffprobe','-v','quiet','-show_format','-show_streams','-of','json',str(portrait)]));s=pr['streams'][0]
checks['Portrait 9:16 dimensions and duration']=s['width']==1080 and s['height']==1920 and abs(float(pr['format']['duration'])-10)<.01
f=subprocess.check_output(['ffmpeg','-loglevel','error','-c:v','libvpx-vp9','-ss','1.5','-i',str(portrait),'-frames:v','1','-f','image2pipe','-vcodec','png','-pix_fmt','rgba','-']);im=Image.open(io.BytesIO(f)).convert('RGBA');checks['Portrait padding really transparent']=im.getpixel((540,100))[3]==0 and im.getchannel('A').getextrema()==(0,255)
result={'exports_reused':'--reuse-exports' in sys.argv,'checks':checks,'file_startup':file_status,'errors':errors,'video':{'width':v['width'],'height':v['height'],'duration':probe['format']['duration'],'codec':v['codec_name'],'alpha':v.get('tags',{}).get('alpha_mode')}}
(ROOT/'tests/logo-motion-results.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(result,indent=2,ensure_ascii=False));assert all(checks.values())
