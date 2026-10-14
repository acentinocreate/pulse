"""Check exact supplied vector endpoints, sporty transforms and transparent video."""
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
import threading,subprocess,json,xml.etree.ElementTree as ET,io,sys
from PIL import Image,ImageChops
from playwright.sync_api import sync_playwright
ET.register_namespace('', 'http://www.w3.org/2000/svg')
ROOT=Path(__file__).resolve().parents[1];checks={};errors=[];requests=[];manifest=json.loads((ROOT/'motions/never-give-up/manifest.json').read_text())
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=ThreadingHTTPServer(('127.0.0.1',8097),partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start()
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=b.new_page(viewport={'width':1600,'height':1100},device_scale_factor=1)
 page.on('pageerror',lambda e:errors.append(str(e)));page.on('request',lambda r:requests.append(r.url))
 page.goto('http://127.0.0.1:8097/motions/never-give-up/index.html');page.wait_for_function('window.PhraseMotion');checks['HTTP startup']=True
 page.evaluate('PhraseMotion.seek(1350)');page.screenshot(path=str(ROOT/'assets/never-give-up-inspection.png'))
 style=page.add_style_tag(content='html,body{background:transparent!important}main{max-width:none;width:1920px;padding:0;margin:0}header,.controls,input,p{display:none!important}.board{width:1920px;height:1080px;background:none!important;border-radius:0}.board svg{width:1920px;height:1080px}')
 page.set_viewport_size({'width':1920,'height':1080});svg=page.locator('#logo svg')
 native=ET.fromstring((ROOT/'motions/never-give-up/motion.svg').read_text());ns='{http://www.w3.org/2000/svg}'
 for number,t in [(1,1350),(2,9000)]:
  asset=manifest['assets'][number-1];original=ET.fromstring((ROOT/'motions/never-give-up'/asset['file']).read_text());orig_paths=[n.attrib['d'] for n in original.findall('.//'+ns+'path')]
  target=native.find(f'.//{ns}g[@id="vector-{number}"]');actual=[n.attrib['d'] for n in target.findall('.//'+ns+'path')]
  checks[f'Vector {number} every original contour unchanged']=actual==orig_paths
  checks[f'Vector {number} color unchanged']=all(n.attrib.get('fill')==asset['fill'] for n in target.findall('.//'+ns+'path'))
  page.evaluate('(t)=>PhraseMotion.seek(t)',t);png=svg.screenshot(omit_background=True);(ROOT/f'assets/never-give-up-vector-{number}-transparent.png').write_bytes(png)
  tx,ty=asset['placement'];original.tag=ns+'g';original.attrib={'transform':f'translate({tx} {ty})'}
  ref=b.new_page(viewport={'width':1920,'height':1080});ref.set_content('<style>html,body{margin:0;background:transparent}svg{display:block}</style><svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">'+ET.tostring(original,encoding='unicode')+'</svg>');reference=ref.locator('svg').screenshot(omit_background=True)
  aa=Image.open(io.BytesIO(png)).convert('RGBA');bb=Image.open(io.BytesIO(reference)).convert('RGBA');checks[f'Vector {number} resting frame RGBA pixel exact']=all(ImageChops.difference(aa,bb).getchannel(ch).getbbox() is None for ch in 'RGBA');print('RGBA difference',number,ImageChops.difference(aa,bb).getextrema(),flush=True);Path(f'/tmp/phrase-reference-{number}.png').write_bytes(reference);ref.close()
  checks[f'Vector {number} background really transparent']=aa.getpixel((0,0))[3]==0 and aa.getchannel('A').getextrema()==(0,255)
 page.evaluate('PhraseMotion.seek(2700)');moving=svg.screenshot(omit_background=True);still=Image.open(ROOT/'assets/never-give-up-vector-1-transparent.png').convert('RGBA');different=ImageChops.difference(still,Image.open(io.BytesIO(moving)).convert('RGBA'))
 checks['Sporty transform changes the actual raster']=different.getchannel('A').getbbox() is not None
 page.evaluate('PhraseMotion.seek(4700)');checks['First vector before transition']=page.evaluate("[...document.querySelectorAll('#vector-2 > g [id^=v2-glyph]')].every(g=>getComputedStyle(g).opacity==='0')")
 page.evaluate('PhraseMotion.seek(5900)');checks['Second vector after transition']=page.evaluate("[...document.querySelectorAll('[id^=v1-glyph]')].every(g=>getComputedStyle(g).opacity==='0')&&[...document.querySelectorAll('[id^=v2-glyph]')].every(g=>getComputedStyle(g).opacity==='1')")
 checks['Only the 25 supplied contours, in animated and exact-rest copies']=page.locator('#logo path').count()==50 and page.locator('#logo rect,#logo circle,#logo image,#logo text').count()==0
 if '--reuse-exports' not in sys.argv:
  proc=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','image2pipe','-vcodec','png','-framerate','30','-i','-','-an','-c:v','libvpx-vp9','-deadline','good','-cpu-used','4','-row-mt','1','-threads','4','-b:v','0','-crf','20','-pix_fmt','yuva420p','-auto-alt-ref','0',str(ROOT/'assets/never-give-up-transparent.webm')],stdin=subprocess.PIPE)
  for i in range(300):
   page.evaluate('(t)=>PhraseMotion.seek(t)',i*1000/30);proc.stdin.write(svg.screenshot(omit_background=True))
  proc.stdin.close();checks['Transparent WebM rendering']=proc.wait()==0
 else:checks['Transparent WebM rendering']=(ROOT/'assets/never-give-up-transparent.webm').is_file()
 style.evaluate('(el)=>el.remove()');page.set_viewport_size({'width':1600,'height':1100});page.evaluate('PhraseMotion.seek(9000)');page.select_option('#backdrop','dark');page.screenshot(path=str(ROOT/'assets/nunca-desista-inspection.png'))
 page.set_viewport_size({'width':390,'height':844});checks['Mobile has no horizontal overflow']=page.evaluate('document.documentElement.scrollWidth<=innerWidth')
 page.evaluate('PhraseMotion.seek(10000)');checks['Ten-second timeline']=page.evaluate('PhraseMotion.position===10000&&PhraseMotion.duration===10000')
 page.click('#play');page.wait_for_timeout(120);checks['Replay']=page.evaluate('PhraseMotion.playing&&PhraseMotion.position<1000');page.click('#play');checks['Pause']=page.evaluate('!PhraseMotion.playing')
 page.evaluate('PhraseMotion.seek(9800);document.querySelector("#loop").checked=false;PhraseMotion.play()');page.wait_for_timeout(400);checks['Playback stops']=page.evaluate('!PhraseMotion.playing&&PhraseMotion.position===10000')
 page.evaluate('PhraseMotion.seek(9800);document.querySelector("#loop").checked=true;PhraseMotion.play()');page.wait_for_timeout(400);checks['Loop restarts']=page.evaluate('PhraseMotion.playing&&PhraseMotion.position<1000');page.evaluate('PhraseMotion.pause()')
 page.emulate_media(reduced_motion='reduce');page.reload();page.wait_for_function('window.PhraseMotion');checks['Reduced motion pauses at final vector']=page.evaluate('!PhraseMotion.playing&&PhraseMotion.position===10000')
 independent=b.new_page();independent.goto('http://127.0.0.1:8097/motions/never-give-up/motion.svg');checks['Standalone animated SVG']=independent.evaluate('typeof document.documentElement.setCurrentTime==="function"');independent.evaluate('document.documentElement.pauseAnimations();document.documentElement.setCurrentTime(10)');checks['Standalone finishes on vector 2']=independent.evaluate("getComputedStyle(document.getElementById('rest-2')).display==='inline'&&[...document.querySelectorAll('[id^=v2-glyph]')].every(g=>getComputedStyle(g).opacity==='1')&&[...document.querySelectorAll('[id^=v1-glyph]')].every(g=>getComputedStyle(g).opacity==='0')")
 local=b.new_page()
 try:local.goto((ROOT/'motions/never-give-up/index.html').as_uri(),timeout=5000);local.wait_for_function('window.PhraseMotion',timeout=2000);file_status='Passed'
 except Exception as e:file_status='Blocked: '+str(e).splitlines()[0]
 checks['No JavaScript errors']=not errors;checks['No ordinary remote requests']=all(r.startswith('http://127.0.0.1:8097/') for r in requests);b.close()
server.shutdown()
video=ROOT/'assets/never-give-up-transparent.webm';pr=json.loads(subprocess.check_output(['ffprobe','-v','quiet','-show_format','-show_streams','-of','json',str(video)]));stream=pr['streams'][0]
checks['Native 1920x1080 and ten-second duration']=stream['width']==1920 and stream['height']==1080 and abs(float(pr['format']['duration'])-10)<.01
checks['Native alpha metadata']=stream.get('tags',{}).get('alpha_mode')=='1'
frame=subprocess.check_output(['ffmpeg','-loglevel','error','-c:v','libvpx-vp9','-ss','9','-i',str(video),'-frames:v','1','-f','image2pipe','-vcodec','png','-pix_fmt','rgba','-']);im=Image.open(io.BytesIO(frame)).convert('RGBA');checks['Native decoded alpha is real']=im.getpixel((0,0))[3]==0 and im.getchannel('A').getextrema()==(0,255)
portrait=ROOT/'assets/never-give-up-transparent-9x16.webm'
if '--reuse-exports' not in sys.argv:
 checks['Portrait transparent render']=subprocess.call(['ffmpeg','-y','-loglevel','error','-c:v','libvpx-vp9','-i',str(video),'-vf','format=yuva420p,scale=1080:-2:flags=lanczos,pad=1080:1920:0:(oh-ih)/2:color=black@0','-an','-c:v','libvpx-vp9','-deadline','good','-cpu-used','4','-row-mt','1','-threads','4','-b:v','0','-crf','20','-pix_fmt','yuva420p','-auto-alt-ref','0',str(portrait)])==0
else:checks['Portrait transparent render']=portrait.is_file()
pp=json.loads(subprocess.check_output(['ffprobe','-v','quiet','-show_format','-show_streams','-of','json',str(portrait)]));s=pp['streams'][0];checks['Portrait 9:16 ten seconds']=s['width']==1080 and s['height']==1920 and abs(float(pp['format']['duration'])-10)<.01
frame=subprocess.check_output(['ffmpeg','-loglevel','error','-c:v','libvpx-vp9','-ss','9','-i',str(portrait),'-frames:v','1','-f','image2pipe','-vcodec','png','-pix_fmt','rgba','-']);im=Image.open(io.BytesIO(frame)).convert('RGBA');checks['Portrait decoded background transparent']=im.getpixel((540,100))[3]==0 and im.getchannel('A').getextrema()==(0,255)
result={'checks':checks,'file_startup':file_status,'exports_reused':'--reuse-exports' in sys.argv,'errors':errors,'native_video':{'width':stream['width'],'height':stream['height'],'duration':pr['format']['duration'],'alpha':stream.get('tags',{}).get('alpha_mode')}}
(ROOT/'tests/phrase-motion-results.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');print(json.dumps(result,indent=2,ensure_ascii=False));assert all(checks.values())
