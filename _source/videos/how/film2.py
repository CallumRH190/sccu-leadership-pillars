import asyncio, time, os, subprocess, numpy as np, soundfile as sf
from playwright.async_api import async_playwright
from kokoro_onnx import Kokoro
URL='file:///home/claude/build/index.html'; OUT='frames'; F=1/30
os.makedirs(OUT,exist_ok=True)
L={
 't':"This is Leadership Pillars. Here's how to run one session, start to finish.",
 '1a':"Click your name, top right. This menu switches who you are.",
 '1b':"Choose Elena Marsh, to become a head.",
 '2a':"Press Start scoring.",
 '2b':"Drag the marker, and watch the description change underneath. Stop where it sounds like your month.",
 '2c':"Then type one real example, and add its date. No example, no score.",
 '2d':"Do that for all six pillars, check them on the review page, and press Submit. The scores are now locked.",
 '3a':"Now switch back to yourself.",
 '3b':"Open Session, and pick Elena. Her scores are in, but hidden from you.",
 '3c':"Score each pillar yourself, with your own example and date. We'll skip ahead through the other five.",
 '3d':"When all six are done, press Lock my scores.",
 '4a':"Now, with Elena beside you, press Reveal.",
 '4b':"Both sets appear together, with the widest gap at the top. Green is Elena. Pink is you.",
 '5a':"Click that pillar. Her example and yours sit side by side,",
 '5b':"with the questions to ask underneath.",
 '5c':"Talk it through, then click the score you both agree. Never just the average.",
 '5d':"Repeat for all six, then move on.",
 '6a':"Pick one focus pillar. The tool suggests one.",
 '6b':"Choose an assignment, or write your own, and set a due date.",
 '6c':"Press Finish, and you both get a one page summary.",
 '7':"To start again, click your name, and choose Reset the demo.",
 '8':"That's the whole session. Switch person, self-score, score blind, reveal, agree, and focus. Try one yourself before Tuesday.",
}
k=Kokoro('/home/claude/tts/kokoro-v1.0.onnx','/home/claude/tts/voices-v1.0.bin')
A={}; SR=24000
for key,t in L.items():
    s,SR=k.create(t,voice='bm_george',speed=1.03,lang='en-gb'); A[key]=s
D={key:len(s)/SR for key,s in A.items()}
print('voice total',round(sum(D.values()),1))
frames=[]; scenes=[0]; marks={}; n=0; mouse=[640,360]; over=[]
total=lambda: sum(d for _,d in frames)
OVERLAY=r'''
(()=>{const s=document.createElement('style');s.textContent=`
#app{transition:transform .55s cubic-bezier(.3,.7,.2,1);will-change:transform}
#ring{position:fixed;z-index:97;display:none;pointer-events:none;border:3px solid #fff;box-shadow:0 0 0 4px rgba(195,46,129,.9),0 0 34px 6px rgba(195,46,129,.55)}
#ring.spot{box-shadow:0 0 0 4px rgba(195,46,129,.9),0 0 0 4000px rgba(9,16,22,.66)}
#ring span{position:absolute;left:-3px;top:-44px;white-space:nowrap;padding:7px 14px;border-radius:10px;background:#fff;color:#182833;font-family:'Nunito Sans';font-weight:800;font-size:16px;box-shadow:0 8px 24px rgba(0,0,0,.4)}
#ring.below span{top:auto;bottom:-44px}
#ring.right span{left:auto;right:-3px}
#step{position:fixed;left:22px;bottom:20px;z-index:99;display:none;align-items:center;gap:12px;padding:9px 20px 9px 9px;border-radius:999px;background:#0f1a22;box-shadow:0 0 0 2px rgba(255,255,255,.18),0 14px 40px rgba(0,0,0,.5);font-family:'Nunito Sans';font-weight:800;font-size:16px;color:#fff}
#step b{width:34px;height:34px;border-radius:50%;display:grid;place-items:center;background:linear-gradient(90deg,#6c3481,#c32e81);font-family:'Comfortaa';font-size:16px}
#step i{display:flex;gap:5px;margin-left:6px}#step i u{width:18px;height:4px;border-radius:4px;background:rgba(255,255,255,.2)}#step i u.on{background:#53baab}
#cur{position:fixed;z-index:100;width:30px;height:30px;margin:-15px 0 0 -15px;border-radius:50%;background:rgba(255,255,255,.3);border:2.5px solid #fff;pointer-events:none;transition:transform .12s;box-shadow:0 2px 10px rgba(0,0,0,.4)}
#cur.dn{transform:scale(.55);background:rgba(83,186,171,.9)}
#card{position:fixed;inset:0;z-index:98;background:radial-gradient(ellipse at 50% 0%,rgba(195,46,129,.3),transparent 62%),#182833;display:none;place-items:center;text-align:center}
#card small{display:block;font-family:'Nunito Sans';font-weight:800;letter-spacing:.3em;font-size:14px;color:rgba(255,255,255,.55);margin-bottom:20px}
#card h1{font-family:'Comfortaa';font-size:60px;line-height:1.1;margin-bottom:20px;color:#fff}
#card p{font-family:'Nunito Sans';font-size:23px;color:rgba(255,255,255,.75);max-width:760px;margin:0 auto}
#card em{display:block;width:120px;height:4px;border-radius:4px;margin:0 auto 26px;background:linear-gradient(90deg,#6c3481,#c32e81)}
#card ol{list-style:none;display:grid;grid-template-columns:repeat(3,250px);gap:14px;margin:8px auto 30px;padding:0;justify-content:center}
#card li{display:flex;align-items:center;gap:12px;padding:14px 16px;border-radius:14px;background:#1f3340;border:1px solid rgba(255,255,255,.12);font-family:'Nunito Sans';font-weight:800;font-size:18px;color:#fff;text-align:left}
#card li b{flex:none;width:32px;height:32px;border-radius:50%;display:grid;place-items:center;background:linear-gradient(90deg,#6c3481,#c32e81);font-family:'Comfortaa';font-size:15px}
`;document.head.appendChild(s);
for(const id of ['ring','step','cur','card']){const d=document.createElement('div');d.id=id;document.body.appendChild(d)}
addEventListener('mousemove',e=>{const c=document.getElementById('cur');c.style.left=e.clientX+'px';c.style.top=e.clientY+'px'},true);
addEventListener('mousedown',()=>document.getElementById('cur').classList.add('dn'),true);
addEventListener('mouseup',()=>document.getElementById('cur').classList.remove('dn'),true);
window.ringEl=(el,tag,spot,rad)=>{const g=document.getElementById('ring');if(!el){g.style.display='none';return}
 const r=el.getBoundingClientRect(),p=spot?10:7;
 Object.assign(g.style,{display:'block',left:r.left-p+'px',top:r.top-p+'px',width:r.width+2*p+'px',height:r.height+2*p+'px',borderRadius:(rad||Math.min(999,r.height))+'px'});
 g.className=(spot?'spot ':'')+(r.top<70?'below ':'')+(r.left>900?'right':'');g.innerHTML=tag?'<span>'+tag+'</span>':''};
window.camEl=(el,z)=>{const app=document.getElementById('app');if(!el){app.style.transform='none';return}
 const prevT=app.style.transform,prevO=app.style.transformOrigin;app.style.transition='none';app.style.transform='none';
 const r=el.getBoundingClientRect(),cx=r.left+r.width/2,cy=r.top+r.height/2;
 app.style.transformOrigin=prevO;app.style.transform=prevT;void app.offsetWidth;app.style.transition='';
 let tx=640-cx,ty=360-cy;tx=Math.min(cx*(z-1),Math.max((1280-cx)*(1-z),tx));ty=Math.min(cy*(z-1),ty);
 app.style.transformOrigin=cx+'px '+(cy+scrollY)+'px';app.style.transform='translate('+tx+'px,'+ty+'px) scale('+z+')'};
window.stepSet=(n,t)=>{const s=document.getElementById('step');if(!n){s.style.display='none';return}s.style.display='flex';
 s.innerHTML='<b>'+n+'</b><span>'+t+'</span><i>'+[1,2,3,4,5,6].map(i=>'<u class="'+(i<=n?'on':'')+'"></u>').join('')+'</i>'};
window.cardSet=(html)=>{const c=document.getElementById('card');c.style.display=html?'grid':'none';c.innerHTML=html||''};
})()'''
async def main():
    global n
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox','--lang=en-GB'],env={**os.environ,'LANG':'en_GB.UTF-8','LANGUAGE':'en_GB'})
        ctx=await b.new_context(viewport={'width':1280,'height':720},device_scale_factor=1.5,locale='en-GB')
        pg=await ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(800); await pg.evaluate(OVERLAY)
        async def snap(d):
            global n; n+=1; path=f'{OUT}/f{n:05d}.jpg'
            await pg.screenshot(path=path,type='jpeg',quality=92); frames.append([path,d])
        still=snap
        async def live(sec):
            t0=time.time(); last=t0; i0=len(frames)
            while True:
                await snap(0); now=time.time()
                if len(frames)-i0>1: frames[-2][1]=now-last
                last=now
                if now-t0>=sec: frames[-1][1]=0.07; break
        def say(key): marks[key]=total()
        async def end(key,gap=0.28):
            el=total()-marks[key]; need=D[key]+0.12+gap
            if el<need: await still(need-el)
            else: over.append((key,round(el-need,2)))
        async def move(x,y,steps=13):
            x0,y0=mouse
            for i in range(1,steps+1):
                q=i/steps; q=q*q*(3-2*q); await pg.mouse.move(x0+(x-x0)*q,y0+(y-y0)*q); await snap(F)
            mouse[0]=x; mouse[1]=y
        async def scroll_to(y,steps=14):
            y0=await pg.evaluate('scrollY')
            if abs(y-y0)<2: return
            for i in range(1,steps+1):
                q=i/steps; q=q*q*(3-2*q); await pg.evaluate(f'scrollTo(0,{y0+(y-y0)*q})'); await snap(F)
        async def bring(sel,top=300):
            bx=await pg.locator(sel).first.bounding_box()
            if bx['y']<80 or bx['y']+bx['height']>640:
                y=await pg.evaluate('scrollY'); await scroll_to(max(0,y+bx['y']-top))
        async def ring(sel,tag='',spot=False,rad=0):
            if sel is None: await pg.evaluate('ringEl(null)')
            else: await pg.locator(sel).first.evaluate('(el,a)=>ringEl(el,a[0],a[1],a[2])',[tag,spot,rad])
        async def cam(sel,z=1.25):
            if sel is None: await pg.evaluate('camEl(null)')
            else: await pg.locator(sel).first.evaluate('(el,z)=>camEl(el,z)',z)
            await live(0.6)
        async def click(sel,tag='',after=0.4,rad=0):
            await bring(sel); await ring(sel,tag,False,rad)
            bx=await pg.locator(sel).first.bounding_box(); x=bx['x']+bx['width']/2; y=bx['y']+bx['height']/2
            await move(x,y); await still(0.22); await pg.mouse.down(); await snap(0.1); await pg.mouse.up(); await ring(None); await live(after)
        async def typ(sel,text):
            bx=await pg.locator(sel).first.bounding_box(); x=bx['x']+bx['width']/2; y=bx['y']+bx['height']/2
            await move(x,y,9); await pg.mouse.click(x,y)
            for i in range(0,len(text),5):
                await pg.keyboard.type(text[i:i+5]); await snap(F*2)
        async def drag(sel,vals):
            tr=await pg.locator(sel).first.locator('.sl-track').bounding_box(); X=lambda v: tr['x']+tr['width']*(v-1)/9; Y=tr['y']+tr['height']/2
            await move(X(5.5),Y,10); await pg.mouse.down(); await snap(0.08)
            for v,h in vals:
                await move(X(v),Y,10); await live(0.3)
                if h: await still(h)
            await pg.mouse.up(); await snap(0.06)
        def scene(): scenes.append(len(frames))
        async def step(nn,t): await pg.evaluate('([n,t])=>stepSet(n,t)',[nn,t])
        cur=lambda v: pg.evaluate(f"document.getElementById('cur').style.display='{v}'")

        # title
        await cur('none'); await pg.evaluate("""cardSet('<div><small>SCCU GROUP</small><h1>Leadership Pillars</h1><em></em><p>How to run one session, start to finish.</p></div>')""")
        say('t'); await still(0.5); await end('t',0.2)
        # 1 switch person
        scene(); await pg.evaluate('cardSet("")'); await cur('block'); await pg.mouse.move(640,360); await step(1,'Switch person')
        say('1a'); await cam('[data-a=menu]',1.35); await click('[data-a=menu]','Click your name',0.35); await end('1a')
        say('1b'); await click('[data-a=role][data-id=elena]','Elena Marsh',0.3,12); await cam(None); await end('1b')
        # 2 self-score
        scene(); await step(2,'Self-score as a head')
        say('2a'); await click('[data-a=ss-go][data-id="0"]','Start scoring',0.3); await pg.evaluate('scrollTo(0,0)'); await live(0.2); await end('2a',0.15)
        say('2b'); await cam('.sl',1.22); await drag('.sl',[(3,0.9),(5,0.9),(7,0)]); await end('2b')
        say('2c'); await cam('.evi',1.22); await ring('textarea[data-k=ex]','One real example',False,14)
        await typ('textarea[data-k=ex]','Two learners withdrew in the same week. I kept every session running and nothing slipped.')
        await ring('input[data-k=d]','And its date',False,14); await pg.fill('input[data-k=d]','2026-11-03'); await live(0.3); await end('2c')
        await ring(None); await cam(None)
        await pg.evaluate("""()=>{const h=S.heads.elena;const d={decisiveness:[5,'Took four days to choose the new assessor when I had what I needed on day one.','2026-11-05'],ingenuity:[7,'Changed the induction from one long day to three short sessions when drop-off showed it was not working.','2026-11-04'],assertiveness:[7,'Told a team member the same day that their handover was not good enough, and why.','2026-11-06'],communication:[5,'Sent the timetable change by email and found out a week later half the group had missed it.','2026-11-02'],enthusiasm:[7,'Picked up the open evening that nobody owned and ran it myself.','2026-11-09']};for(const k in d)h.cur.self[k]={s:d[k][0],ex:d[k][1],d:d[k][2],over:false};h.cur.step=6;save();render();scrollTo(0,0)}""")
        scene(); say('2d'); await live(0.3); await still(1.3); await scroll_to(await pg.evaluate('document.body.scrollHeight-720'),40)
        print('DBG2',await pg.evaluate("JSON.stringify([S.heads.elena.cur.self.resilience,S.heads.elena.cur.step,document.querySelector('[data-a=ss-submit]').disabled,P.map(p=>full(S.heads.elena.cur.self[p.id]))])")); await click('[data-a=ss-submit]','Submit and lock',0.3); print('DBG3',await pg.evaluate('S.heads.elena.cur.selfAt')); await pg.evaluate('scrollTo(0,0)'); await live(0.2); await end('2d')
        # 3 James scores blind
        scene(); await step(3,'Score blind as James')
        say('3a'); await click('[data-a=menu]','Click your name',0.3); await click('[data-a=role][data-id=james]','James Pease',0.3,12); await end('3a',0.15)
        say('3b'); await click('a[href="#session"]','Session',0.4); await click('[data-a=head][data-id=elena]','Pick the head',0.3); await ring('.hidden-note','Hidden until yours are locked',True,16); await end('3b')
        await ring(None)
        say('3c'); await cam('.jrow',1.18); await drag('.jrow .sl',[(5,0)])
        await typ('#jex-resilience','That week the team told me they were tiptoeing around her. The work held, the room was tense.')
        await pg.fill('#jd-resilience','2026-11-04'); await live(0.3); await end('3c')
        await cam(None)
        await pg.evaluate("""()=>{const h=S.heads.elena;const d={decisiveness:[6,'Chose the assessor and closed it. Slower than it needed to be, but she owned the call.','2026-11-05'],ingenuity:[7,'The three short induction sessions were her idea. Drop-off fell the next week.','2026-11-04'],assertiveness:[7,'Dealt with the poor handover herself, the same day. It never reached me.','2026-11-06'],communication:[6,'The timetable email was missed by half the group. She phoned round once she knew.','2026-11-09'],enthusiasm:[7,'Ran the open evening herself when nobody else picked it up.','2026-11-09']};for(const k in d)h.cur.james[k]={s:d[k][0],ex:d[k][1],d:d[k][2],over:false};save();render()}""")
        say('3d'); await scroll_to(await pg.evaluate('document.body.scrollHeight-720'),30); await click('[data-a=j-lock]','Lock my scores',0.3); print('DBG',await pg.evaluate("JSON.stringify([S.role,S.headId,S.heads.elena.cur.selfAt,S.heads.elena.cur.jamesAt,S.heads.elena.cur.james.resilience,location.hash])")); await pg.evaluate('scrollTo(0,0)'); await live(0.2); await end('3d',0.15)
        # 4 reveal
        scene(); await step(4,'Reveal together')
        say('4a'); await click('[data-a=reveal]','Reveal both sets',0.1); await live(1.2); await end('4a',0.0)
        say('4b'); await live(1.6); await cam('.rv-row',1.22); await ring('.rv-row','Widest gap first',False,14); await end('4b')
        await ring(None); await cam(None)
        # 5 explore and agree
        scene(); await step(5,'Explore and agree')
        say('5a'); await click('.xc-h','Open the pillar',0.3,16); y=await pg.evaluate("document.querySelector('.xc').getBoundingClientRect().top+scrollY-100"); await scroll_to(y,14); await ring('.xc .two','Both examples',True,16); await end('5a',0.1)
        say('5b'); await ring(None); await bring('.xc .qs',200); await ring('.xc .qs','Questions to ask',True,16); await end('5b')
        await ring(None)
        say('5c'); await bring('.xc .agree',330); await cam('.xc .agree',1.3); await click('.xc [data-a=agree][data-id="6"]','The score you both agree',0.4,12); await end('5c')
        await cam(None)
        await pg.evaluate("""()=>{const c=S.heads.elena.cur;Object.assign(c.agreed,{decisiveness:6,ingenuity:7,assertiveness:7,communication:6,enthusiasm:7});ui.open=null;save();render()}""")
        say('5d'); await scroll_to(await pg.evaluate('document.body.scrollHeight-720'),22); await click('[data-a=stage][data-id=focus]','Next',0.3); await pg.evaluate('scrollTo(0,0)'); await live(0.2); await end('5d',0.15)
        # 6 focus and assignment
        scene(); await step(6,'Focus and assignment')
        say('6a'); await click('.ft:has(small:text-is("Suggested"))','Suggested focus',0.35,14); await end('6a')
        say('6b'); await scroll_to(300,14); await click('[data-a=asg][data-id="0"]','One real assignment',0.3,14); await bring('#due',300); y=await pg.evaluate('scrollY'); await scroll_to(y+140,10); await ring('#due','Due date',False,14); await pg.fill('#due','2026-12-09'); await live(0.3); await end('6b')
        await ring(None)
        say('6c'); await click('[data-a=finish]','Finish',0.4); await pg.evaluate('scrollTo(0,0)'); await live(0.3); await still(0.6); await scroll_to(330,40); await end('6c',0.5)
        # 7 reset
        scene(); await pg.evaluate('stepSet(0)'); await pg.evaluate('scrollTo(0,0)')
        say('7'); await click('[data-a=menu]','Click your name',0.4); await ring('[data-a=reset]','Reset the demo',True,12); bx=await pg.locator('[data-a=reset]').bounding_box(); await move(bx['x']+120,bx['y']+bx['height']/2); await end('7',0.5)
        await ring(None); await cam(None)
        # 8 recap
        scene(); await cur('none')
        await pg.evaluate("""cardSet('<div><small>ONE SESSION, SIX STEPS</small><ol>'+['Switch person','Self-score','Score blind','Reveal','Explore and agree','Focus and assignment'].map((t,i)=>'<li><b>'+(i+1)+'</b>'+t+'</li>').join('')+'</ol><p>Try one yourself before Tuesday.</p></div>')""")
        say('8'); await still(0.5); await end('8',0.9)
        print('page errors',errs); await b.close()
    # encode
    scenes.append(len(frames)); files=[]
    for i in range(len(scenes)-1):
        fr=frames[scenes[i]:scenes[i+1]]
        if not fr: continue
        lst=f's{i}.txt'
        with open(lst,'w') as f:
            for path,d in fr: f.write(f"file '{os.path.abspath(path)}'\nduration {max(d,0.02):.4f}\n")
            f.write(f"file '{os.path.abspath(fr[-1][0])}'\n")
        r=subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',lst,'-vf','fps=30,scale=1920:1080,format=yuv420p','-c:v','libx264','-crf','18','-preset','veryfast','-pix_fmt','yuv420p',f's{i}.tmp.mp4']); assert r.returncode==0
        os.rename(f's{i}.tmp.mp4',f's{i}.mp4'); files.append(os.path.abspath(f's{i}.mp4'))
    open('all.txt','w').write(''.join(f"file '{x}'\n" for x in files))
    r=subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i','all.txt','-c','copy','joined.mp4']); assert r.returncode==0
    T=total(); track=np.zeros(int((T+0.5)*SR),dtype=np.float32)
    for key,s in A.items():
        o=int((marks[key]+0.12)*SR); track[o:o+len(s)]+=s[:len(track)-o]
    sf.write('voice.wav',track,SR)
    r=subprocess.run(['ffmpeg','-y','-loglevel','error','-i','joined.mp4','-i','voice.wav','-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','160k','-af','loudnorm=I=-16:TP=-1.5','-shortest','-movflags','+faststart','out.tmp.mp4']); assert r.returncode==0
    os.rename('out.tmp.mp4','SCCU-Leadership-Pillars-How-To-Run-A-Session.mp4')
    print('total',round(T,1),'overruns',over)
    import json; json.dump({'marks':marks,'dur':D},open('marks.json','w'))
asyncio.run(main())
