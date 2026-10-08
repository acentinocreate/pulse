from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import threading, subprocess, json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*a): pass
server=ThreadingHTTPServer(('127.0.0.1',8092),partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
checks={};errors=[];requests=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1336,'height':920},device_scale_factor=1)
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.on('request',lambda r:requests.append(r.url))
 page.goto('http://127.0.0.1:8092/index.html');page.wait_for_function('window.Pulso')
 checks['HTTP startup']=True
 page.evaluate('Pulso.seek(4800)');checks['4.8 second duration']=page.evaluate('Pulso.duration===4800&&Pulso.position===4800')
 page.click('#play');page.wait_for_timeout(150);checks['Replay from final frame']=page.evaluate('Pulso.playing&&Pulso.position>0&&Pulso.position<1000')
 page.click('#play');checks['Pause']=page.evaluate('!Pulso.playing')
 page.evaluate('Pulso.seek(0);document.querySelector("#loop").checked=false;Pulso.play()');page.wait_for_timeout(5050);checks['Playback stops after 4.8 seconds']=page.evaluate('!Pulso.playing&&Pulso.position===4800')
 page.evaluate('document.querySelector("#loop").checked=true;Pulso.play()');page.wait_for_timeout(4950);checks['Loop restarts']=page.evaluate('Pulso.playing&&Pulso.position<1000');page.evaluate('Pulso.pause()')
 stage=page.locator('#stage');page.evaluate('Pulso.seek(3020)');stage.screenshot(path=str(ROOT/'assets/preview.png'))
 process=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','image2pipe','-vcodec','png','-framerate','30','-i','-','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(ROOT/'assets/pulso-demo.mp4')],stdin=subprocess.PIPE)
 for i in range(144):
  page.evaluate('(t)=>Pulso.seek(t)',i*1000/30)
  process.stdin.write(stage.screenshot())
 process.stdin.close();checks['MP4 rendering']=process.wait()==0
 page.set_viewport_size({'width':390,'height':844});page.evaluate('Pulso.seek(3020)');checks['Mobile overflow']=page.evaluate('document.documentElement.scrollWidth<=innerWidth')
 page.emulate_media(reduced_motion='reduce');page.reload();page.wait_for_function('window.Pulso');checks['Reduced motion static frame']=page.evaluate('!Pulso.playing&&Pulso.position===4800')
 local=browser.new_page()
 try:
  local.goto((ROOT/'index.html').as_uri(),timeout=10000);local.wait_for_function('window.Pulso',timeout=3000);checks['file startup']='Passed'
 except Exception as e: checks['file startup']='Not executed successfully: '+str(e).splitlines()[0]
 checks['No page errors']=not errors;checks['No remote network calls']=all(u.startswith('http://127.0.0.1:8092/') for u in requests)
 browser.close()
server.shutdown()
probe=json.loads(subprocess.check_output(['ffprobe','-v','quiet','-show_format','-show_streams','-of','json',str(ROOT/'assets/pulso-demo.mp4')]))
v=probe['streams'][0];checks['MP4 dimensions and duration']=v['width']==1280 and v['height']==720 and abs(float(probe['format']['duration'])-4.8)<.01
(ROOT/'tests/results.json').write_text(json.dumps({'checks':checks,'errors':errors,'video':{'width':v['width'],'height':v['height'],'duration':probe['format']['duration']}},indent=2,ensure_ascii=False))
print(json.dumps(checks,indent=2,ensure_ascii=False))
assert all(v for v in checks.values())
