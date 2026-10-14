from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import threading, subprocess, json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*a): pass
server=ThreadingHTTPServer(('127.0.0.1',8093),partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
checks={};errors=[];requests=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1336,'height':920},device_scale_factor=1)
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.on('request',lambda r:requests.append(r.url))
 page.goto('http://127.0.0.1:8093/motions/get-keep/index.html');page.wait_for_function('window.Pulso')
 checks['HTTP startup']=True
 page.evaluate('Pulso.seek(4999)');checks['GET immediately before midpoint']=page.evaluate('Pulso.word==="GET"')
 page.evaluate('Pulso.seek(5000)');checks['KEEP at midpoint']=page.evaluate('Pulso.word==="KEEP"')
 bounds="""()=>{const c=document.querySelector('canvas').getContext('2d'),d=c.getImageData(40,280,1000,270).data;let min=1000,max=0,count=0;for(let y=0;y<270;y++)for(let x=0;x<1000;x++){const i=(y*1000+x)*4;if(d[i]>250&&d[i+1]>250&&d[i+2]>250){min=Math.min(min,x);max=Math.max(max,x);count++}}return {min,max,count}}"""
 page.evaluate('Pulso.seek(4550)');before=page.evaluate(bounds)
 page.evaluate('Pulso.seek(5500)');after=page.evaluate(bounds)
 checks['Visible KEEP has four-letter width after exchange']=after['max']-before['max']>180 and after['count']>before['count']
 checks['Main lettering uses vector contours']=page.evaluate('Object.keys(Pulso.lettering.glyphs).length===9&&Pulso.lettering.glyphs.K.path.length>0&&Pulso.lettering.glyphs.P.path.length>0')
 page.evaluate('Pulso.seek(10000)');checks['10 second duration']=page.evaluate('Pulso.duration===10000&&Pulso.position===10000')
 page.click('#play');page.wait_for_timeout(150);checks['Replay from final frame']=page.evaluate('Pulso.playing&&Pulso.position>0&&Pulso.position<1000')
 page.click('#play');checks['Pause']=page.evaluate('!Pulso.playing')
 page.evaluate('Pulso.seek(0);document.querySelector("#loop").checked=false;Pulso.play()');page.wait_for_timeout(10200);checks['Playback stops after 10 seconds']=page.evaluate('!Pulso.playing&&Pulso.position===10000')
 page.evaluate('document.querySelector("#loop").checked=true;Pulso.play()');page.wait_for_timeout(10200);checks['Loop restarts']=page.evaluate('Pulso.playing&&Pulso.position<1000');page.evaluate('Pulso.pause()')
 page.set_viewport_size({'width':1080,'height':1920});export_style=page.add_style_tag(content='main{display:block;padding:0;margin:0;max-width:none;min-height:0}.intro,.controls,#timeline{display:none}.player,.stage{width:1080px;max-width:none}body{overflow:hidden}');stage=page.locator('#stage');page.evaluate('Pulso.seek(5500)');stage.screenshot(path=str(ROOT/'assets/get-keep-preview.png'))
 process=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','image2pipe','-vcodec','png','-framerate','30','-i','-','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(ROOT/'assets/get-keep-running.mp4')],stdin=subprocess.PIPE)
 for i in range(300):
  page.evaluate('(t)=>Pulso.seek(t)',i*1000/30)
  process.stdin.write(stage.screenshot())
 process.stdin.close();checks['MP4 rendering']=process.wait()==0
 for i,t in enumerate([1200,2500,4600,5500,9700]):
  page.evaluate('(t)=>Pulso.seek(t)',t);stage.screenshot(path=str(ROOT/f'assets/get-keep-scene-{i+1}.png'))
 export_style.evaluate('(el)=>el.remove()');page.set_viewport_size({'width':390,'height':844});page.evaluate('Pulso.seek(5500)');page.screenshot(path=str(ROOT/'assets/get-keep-mobile.png'));checks['Mobile overflow']=page.evaluate('document.documentElement.scrollWidth<=innerWidth')
 page.emulate_media(reduced_motion='reduce');page.reload();page.wait_for_function('window.Pulso');checks['Reduced motion static frame']=page.evaluate('!Pulso.playing&&Pulso.position===10000')
 local=browser.new_page()
 try:
  local.goto((ROOT/'motions/get-keep/index.html').as_uri(),timeout=10000);local.wait_for_function('window.Pulso',timeout=3000);checks['file startup']='Passed'
 except Exception as e: checks['file startup']='Not executed successfully: '+str(e).splitlines()[0]
 checks['No page errors']=not errors;checks['No remote network calls']=all(u.startswith('http://127.0.0.1:8093/') for u in requests)
 browser.close()
server.shutdown()
probe=json.loads(subprocess.check_output(['ffprobe','-v','quiet','-show_format','-show_streams','-of','json',str(ROOT/'assets/get-keep-running.mp4')]))
v=probe['streams'][0];checks['MP4 dimensions and duration']=v['width']==1080 and v['height']==1920 and abs(float(probe['format']['duration'])-10)<.01
(ROOT/'tests/get-keep-results.json').write_text(json.dumps({'checks':checks,'errors':errors,'video':{'width':v['width'],'height':v['height'],'duration':probe['format']['duration']}},indent=2,ensure_ascii=False))
print(json.dumps(checks,indent=2,ensure_ascii=False))
assert all(v for v in checks.values() if isinstance(v,bool))
