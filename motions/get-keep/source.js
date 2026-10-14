'use strict';
const lettering=LETTERING_DATA;
const $=id=>document.getElementById(id),ctx=$('canvas').getContext('2d'),W=1080,H=1920,DURATION=10000;
const GREEN=lettering.color,WHITE='#ffffff',BLACK='#102515';
const glyphs=Object.fromEntries(Object.entries(lettering.glyphs).map(([ch,g])=>[ch,{...g,shape:new Path2D(g.path)}]));
const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x)),out=x=>1-Math.pow(1-clamp(x),4),inOut=x=>{x=clamp(x);return x<.5?8*x*x*x*x:1-Math.pow(-2*x+2,4)/2},lerp=(a,b,p)=>a+(b-a)*p;
function wordWidth(word,gap=34){return [...word].reduce((v,ch)=>v+glyphs[ch].width,0)+(word.length-1)*gap}
function text(s,x,y,size=25,color=BLACK,align='left'){ctx.fillStyle=color;ctx.font=`${size}px ui-monospace,monospace`;ctx.textAlign=align;ctx.fillText(s,x,y)}
function line(x,y,xx,yy,color,width=2){ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(xx,yy);ctx.lineWidth=width;ctx.strokeStyle=color;ctx.stroke()}
function arrow(x,y,n,color,width=8){line(x,y+n,x+n,y,color,width);line(x,y,x+n,y,color,width);line(x+n,y,x+n,y+n,color,width)}
function ring(x,y,r,color,width=2){ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);ctx.strokeStyle=color;ctx.lineWidth=width;ctx.stroke()}
function fill(color){ctx.fillStyle=color;ctx.fillRect(0,0,W,H)}
function letter(ch,x,y,scale,color=GREEN,angle=0){ctx.save();ctx.translate(x,y);ctx.scale(scale,scale);ctx.rotate(angle);ctx.fillStyle=color;ctx.fill(glyphs[ch].shape,'evenodd');ctx.restore()}
function word(str,x,y,width,color=GREEN,{gap=34,enter=1,t=0,slant=0,stagger=false,trail=0}={}){
 const scale=width/wordWidth(str,gap);let dx=0;
 for(let i=0;i<str.length;i++){
  const local=stagger?out((enter-i*.075)/.62):out(enter),offset=(1-local)*1250;
  if(trail){ctx.save();ctx.globalAlpha=.09;for(let j=3;j>0;j--)letter(str[i],x+dx-j*trail,y,scale,color,slant);ctx.restore()}
  letter(str[i],x+dx+offset,y+(1-local)*45,scale,color,slant*(1-local));dx+=(glyphs[str[i]].width+gap)*scale;
 }
 return lettering.height*scale;
}
function lockup(t,color=GREEN,{x=64,y=650,width=952,enter=1,drift=0,trail=0,slant=0}={}){
 const h=word('RUN',x+drift,y,width,color,{enter,t,stagger:enter<1,trail,slant});
 const lowerWidth=width*.98;
 word('NING',x+width-lowerWidth-drift*.5,y+h+34,lowerWidth,color,{enter:enter-.08,t,stagger:enter<1,trail,slant});
}
function header(t,fg=BLACK,phase='START / 01'){
 text('RUN CULTURE',64,94,25,fg);text(phase,1016,94,22,fg,'right');line(64,125,1016,125,fg,2);
}
function footer(t,fg=BLACK,tag='COMECE. ENCONTRE SEU RITMO.'){
 line(64,1750,1016,1750,fg,2);line(64,1750,64+952*clamp(t/10),1750,fg,8);
 text(tag,64,1810,23,fg);text((t.toFixed(2)+' S').padStart(7,'0'),1016,1870,23,fg,'right');
 text(t<5?'01 / GET RUNNING':'02 / KEEP RUNNING',64,1870,21,fg);
}
function lanes(t,color=GREEN,alpha=.16){ctx.save();ctx.globalAlpha=alpha;const offset=(t*650)%260;for(let i=-5;i<13;i++)line(-200+i*220-offset,1920,680+i*220-offset,80,color,3);for(let j=0;j<8;j++){const y=(j*250+t*1050)%2200;ctx.fillStyle=color;ctx.fillRect(920,y-200,60,8)}ctx.restore()}
function speed(t,color=GREEN,alpha=1){ctx.save();ctx.globalAlpha=alpha;for(let i=0;i<13;i++){const x=((t*(780+i*17)+i*139)%1500)-350,y=280+i*99,len=70+(i%4)*35;line(x,y,x+len,y,color,i%3===0?7:2)}ctx.restore()}
function chevrons(t,color=GREEN){ctx.save();const offset=(t*420)%220;for(let i=-1;i<6;i++){const x=i*220-offset;line(x,1598,x+83,1515,color,15);line(x+83,1515,x,1432,color,15)}ctx.restore()}
function smallMark(t,color=GREEN){ctx.save();ctx.translate(941,222);ctx.rotate(-.12+Math.sin(t*3)*.06);arrow(-42,-42,84,color,11);ctx.restore()}
function startScene(t){
 fill(WHITE);header(t,BLACK,t<.9?'READY / 01':'GO / 01');
 const topEntry=out((t-.12)/.65);ctx.save();ctx.beginPath();ctx.rect(0,208,1080,420);ctx.clip();word('GET',64+(1-topEntry)*1000,270,745,GREEN,{enter:1});ctx.restore();
 smallMark(t);lockup(t,GREEN,{y:690,enter:clamp((t-.1)/1.12),slant:-.12});
 ctx.save();ctx.globalAlpha=.08;speed(t,GREEN);ctx.restore();
 chevrons(t,GREEN);footer(t,BLACK);text('DÊ O PRIMEIRO PASSO.',64,1640,34,BLACK);
}
function accelerate(t){
 const local=t-1.65,p=out(local/.3);fill(GREEN);header(t,WHITE,'PACE / 02');
 lanes(t,WHITE,.28);speed(t,WHITE,.35);
 word('GET',64-(1-p)*1050,265,745,WHITE);smallMark(t,WHITE);
 const pulse=Math.sin(local*6)*7;lockup(t,WHITE,{y:685,drift:pulse,trail:local>.7?23:0,enter:1});
 chevrons(t,WHITE);text('MAIS RITMO. MAIS RUA.',64,1640,34,WHITE);footer(t,WHITE);
}
function macro(t){
 fill(WHITE);const local=t-3.15,p=clamp(local/1.1),zoom=1+Math.sin(p*Math.PI)*1.35;
 ctx.save();ctx.translate(540,940);ctx.scale(zoom,zoom);ctx.translate(-540,-940);word('GET',64,265,745,GREEN);lockup(t,GREEN,{y:685,drift:Math.sin(p*Math.PI*2)*70,trail:15});ctx.restore();
 ctx.save();ctx.globalAlpha=.65;speed(t,GREEN);ctx.restore();
 header(t,BLACK,'PUSH / 03');footer(t,BLACK);text('NÃO É SÓ COMEÇAR.',64,1640,34,BLACK);
 ctx.fillStyle=WHITE;ctx.fillRect(0,129,1080,52);
}
function exchange(t){
 fill(GREEN);const local=t-4.35;lanes(t,WHITE,.25);header(t,WHITE,t<5?'GET → KEEP':'KEEP / 04');
 const exit=inOut((t-4.6)/.4);ctx.save();ctx.beginPath();ctx.rect(40,250,1000,330);ctx.clip();
 if(t<5){word('GET',64-exit*80,270-exit*460,745,WHITE,{trail:exit*30})}
 else{const enter=out((t-5)/.38);word('KEEP',64+(1-enter)*220,272+(1-enter)*440,952,WHITE,{trail:(1-enter)*35})}
 ctx.restore();smallMark(t,WHITE);
 lockup(t,WHITE,{y:685,drift:Math.sin(local*9)*6,trail:t<5?15:8});chevrons(t,WHITE);
 text(t<5?'O PRIMEIRO PASSO É O COMEÇO.':'CONTINUAR É A ESCOLHA.',64,1640,30,WHITE);footer(t,WHITE,t<5?'ARRANQUE.':'MANTENHA O MOVIMENTO.');
}
function keepScene(t){
 fill(WHITE);const local=t-5.7;header(t,BLACK,'KEEP / 04');
 ctx.save();ctx.globalAlpha=.07;word('KEEP',64+((local*230)%1400)-800,210,1300,GREEN);word('KEEP',64-((local*230)%1400)+600,1350,1300,GREEN);ctx.restore();
 lanes(t,GREEN,.11);word('KEEP',64,275,952,GREEN,{trail:local>.8?12:0});
 const bump=Math.sin(local*8)*6;lockup(t,GREEN,{y:685,drift:bump,trail:12});smallMark(t,GREEN);chevrons(t,GREEN);
 text('PASSO APÓS PASSO.',64,1640,34,BLACK);footer(t,BLACK,'SEU RITMO. SEM PARAR.');
}
function finish(t){
 const local=t-7.7,p=out(local/.4);fill(GREEN);header(t,WHITE,'FINISH / 05');
 ctx.save();ctx.globalAlpha=.22;for(let i=0;i<5;i++){ctx.save();ctx.translate(540,1100);ctx.scale(1+i*.16,1+i*.16);ctx.translate(-540,-1100);ctx.beginPath();ctx.roundRect(90,780,900,580,290);ctx.strokeStyle=WHITE;ctx.lineWidth=2;ctx.stroke();ctx.restore()}ctx.restore();
 word('KEEP',64+(1-p)*1050,270,952,WHITE);lockup(t,WHITE,{y:685,enter:1,drift:(1-p)*-100});
 smallMark(t,WHITE);chevrons(t,WHITE);text('COMECE. CONTINUE. REPITA.',64,1640,33,WHITE);footer(t,WHITE,'O PRIMEIRO PASSO É SÓ O COMEÇO.');
}
let position=0,playing=false,raf=0,start=0;
function draw(ms){position=clamp(ms,0,DURATION);const t=position/1000;
 ctx.save();ctx.clearRect(0,0,W,H);
 if(t<1.65)startScene(t);else if(t<3.15)accelerate(t);else if(t<4.35)macro(t);else if(t<5.7)exchange(t);else if(t<7.7)keepScene(t);else finish(t);
 ctx.restore();$('timeline').value=position;$('time').textContent=(position/1000).toFixed(1).replace('.',',')+' / 10,0 s';
}
function pause(){playing=false;cancelAnimationFrame(raf);$('play').textContent=position>=DURATION?'Rever':'Reproduzir'}
function tick(now){if(!playing)return;const ms=now-start;if(ms>=DURATION){draw(DURATION);if($('loop').checked){start=now;draw(0)}else{pause();$('status').textContent='Animação concluída.';return}}else draw(ms);raf=requestAnimationFrame(tick)}
function play(){if(position>=DURATION)draw(0);playing=true;start=performance.now()-position;$('play').textContent='Pausar';$('status').textContent='Reproduzindo.';raf=requestAnimationFrame(tick)}
$('play').onclick=()=>playing?pause():play();$('timeline').oninput=()=>{pause();draw(Number($('timeline').value))};document.addEventListener('visibilitychange',()=>{if(document.hidden&&playing)pause()});
window.Pulso={duration:DURATION,seek(t){pause();draw(t)},play,pause,get position(){return position},get playing(){return playing},get word(){return position<5000?'GET':'KEEP'},get lettering(){return lettering}};
if(typeof ctx.roundRect!=='function')ctx.roundRect=function(x,y,w,h,r){this.moveTo(x+r,y);this.arcTo(x+w,y,x+w,y+h,r);this.arcTo(x+w,y+h,x,y+h,r);this.arcTo(x,y+h,x,y,r);this.arcTo(x,y,x+w,y,r);return this};
draw(0);if(matchMedia('(prefers-reduced-motion: reduce)').matches)draw(DURATION);else play();
