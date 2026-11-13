"""Films the trial-version explainer to Callum's recording. James's laptop and the head's phone."""
import asyncio, time, os, subprocess, json, numpy as np, soundfile as sf
from playwright.async_api import async_playwright
SITE = 'https://sccu-leadership-pillars.vercel.app'
TRIAL_HTML = open('/home/claude/build/trial.html').read()
OVERLAY = open('/home/claude/v2/overlay.js').read()
OUT = 'frames_t'; os.makedirs(OUT, exist_ok=True); F = 1 / 30
A = np.load('/home/claude/vo4/clips_trial.npy', allow_pickle=True).item(); SR = 48000
D = {k: len(v) / SR for k, v in A.items()}
frames = []; scenes = [0]; marks = {}; over = []; n = 0; mouse = [640, 360]
total = lambda: sum(d for _, d in frames)
STAGE = '''<!DOCTYPE html><html><head><meta charset="utf-8"><style>FONTS
*{box-sizing:border-box;margin:0;padding:0}html,body{width:1280px;height:720px;overflow:hidden}
body{background:radial-gradient(ellipse at 28% 0%,rgba(195,46,129,.28),transparent 60%),#182833;color:#fff;font-family:'Nunito Sans',sans-serif}
.cap{position:absolute;left:84px;top:210px;width:520px}
.cap small{display:block;font-weight:800;letter-spacing:.24em;font-size:14px;color:#53baab;text-transform:uppercase;margin-bottom:18px}
.cap h1{font-family:'Comfortaa';font-size:46px;line-height:1.12;margin-bottom:18px;transition:opacity .35s}
.cap p{font-size:21px;line-height:1.45;color:rgba(255,255,255,.76);transition:opacity .35s}
.cap em{display:block;width:96px;height:4px;border-radius:4px;margin:0 0 22px;background:linear-gradient(90deg,#6c3481,#c32e81)}
.phone{position:absolute;left:800px;top:18px;width:336px;height:684px;border-radius:44px;background:#0b141a;box-shadow:0 0 0 2px rgba(255,255,255,.16),0 40px 90px rgba(0,0,0,.55);padding:36px 12px 12px}
.phone::before{content:"";position:absolute;left:50%;top:13px;width:70px;height:10px;margin-left:-35px;border-radius:8px;background:#1f2c35;z-index:3}
.scr{width:312px;height:636px;border-radius:12px 12px 34px 34px;overflow:hidden;background:#182833}
iframe{width:390px;height:795px;border:0;transform:scale(.8);transform-origin:0 0}
</style></head><body><div class="cap"><small id="eb"></small><em></em><h1 id="h"></h1><p id="p"></p></div>
<div class="phone"><div class="scr"><iframe id="f" src="/trial?who=head"></iframe></div></div>
<script>window.setCap=(e,h,p)=>{document.getElementById('eb').textContent=e;document.getElementById('h').textContent=h;document.getElementById('p').textContent=p}</script></body></html>'''
fonts = TRIAL_HTML[TRIAL_HTML.index('@font-face'):TRIAL_HTML.index('</style>')]
fonts = '\n'.join(l for l in fonts.split('\n') if l.startswith('@font-face'))
STAGE = STAGE.replace('FONTS', fonts)
EXTRA = r'''(()=>{window.stepSet=(n,t)=>{const s=document.getElementById('step');if(!n){s.style.display='none';return}s.style.display='flex';
 s.innerHTML='<span style="padding-left:12px">'+t+'</span><i>'+[1,2,3].map(i=>'<u class="'+(i<=n?'on':'')+'" style="width:26px"></u>').join('')+'</i>'};})()'''
HEAD_FILL = """()=>{const h=S.heads.me;const d={decisiveness:[8,'Chose the new booking supplier the same day the quotes came in and told the team why.'],ingenuity:[6,'Rebuilt the induction as two short calls when the room booking fell through.'],assertiveness:[5,'Told a team member the same afternoon that the report was late and when I needed it.'],communication:[8,'Rang each employer about the date change and asked them to say it back to me.'],enthusiasm:[9,'Picked up the careers stand nobody owned and had it staffed by Friday.']};let i=2;for(const k in d){h.cur.self[k]={s:d[k][0],ex:d[k][1],d:MIND2(i++),over:false}}h.cur.selfAt=TODAY;h.cur.subT=Date.now();h.cur.step=6;save();render();scrollTo(0,0)}""".replace('MIND2(i++)', "_iso(new Date(Date.now()-(i++)*864e5))")
J_FILL = """()=>{const h=curH();const d={decisiveness:[8,'Supplier decision made and closed inside the week.'],ingenuity:[5,'The two-call induction was a neat fix, but the idea came from the team.'],assertiveness:[7,'The late report was raised the same day. Clear and direct.'],communication:[7,'Employers knew the new date before I did.'],enthusiasm:[8,'Careers stand picked up without being asked.']};let i=2;for(const k in d){h.cur.james[k]={s:d[k][0],ex:d[k][1],d:_iso(new Date(Date.now()-(i++)*864e5)),over:false}}save();render()}"""

async def main():
    global n
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox', '--lang=en-GB'], env={**os.environ, 'LANG': 'en_GB.UTF-8', 'LANGUAGE': 'en_GB'})
        ctx = await b.new_context(viewport={'width': 1280, 'height': 720}, device_scale_factor=1.5, locale='en-GB')
        async def handle(route):
            u = route.request.url
            if u.startswith(SITE + '/trial'): await route.fulfill(status=200, content_type='text/html; charset=utf-8', body=TRIAL_HTML)
            elif u.startswith(SITE + '/stage'): await route.fulfill(status=200, content_type='text/html; charset=utf-8', body=STAGE)
            else: await route.abort()
        await ctx.route('**/*', handle)
        J = await ctx.new_page(); G = await ctx.new_page(); errs = []
        J.on('pageerror', lambda e: errs.append('J ' + str(e))); G.on('pageerror', lambda e: errs.append('G ' + str(e)))
        await J.goto(SITE + '/trial'); await J.wait_for_timeout(700); await J.evaluate(OVERLAY); await J.evaluate(EXTRA)
        await G.goto(SITE + '/stage'); await G.wait_for_timeout(900)
        fr = [f for f in G.frames if 'who=head' in f.url][0]
        await fr.evaluate(OVERLAY)
        await fr.evaluate("document.getElementById('cur').style.display='none'")
        cur_pg = [J]
        async def snap(d):
            global n; n += 1; path = f'{OUT}/f{n:05d}.jpg'
            await cur_pg[0].screenshot(path=path, type='jpeg', quality=92); frames.append([path, d])
        still = snap
        async def live(sec):
            t0 = time.time(); last = t0; i0 = len(frames)
            while True:
                await snap(0); now = time.time()
                if len(frames) - i0 > 1: frames[-2][1] = now - last
                last = now
                if now - t0 >= sec: frames[-1][1] = 0.07; break
        def say(k): marks[k] = total()
        async def end(k, gap=0.3):
            el = total() - marks[k]; need = D[k] + 0.12 + gap
            if el < need: await still(need - el)
            else: over.append((k, round(el - need, 2)))
        async def move(x, y, steps=12):
            x0, y0 = mouse
            for i in range(1, steps + 1):
                q = i / steps; q = q * q * (3 - 2 * q); await cur_pg[0].mouse.move(x0 + (x - x0) * q, y0 + (y - y0) * q); await snap(F)
            mouse[0] = x; mouse[1] = y
        async def scroll_to(y, steps=14, ctxf=None):
            t = ctxf or J; y0 = await t.evaluate('scrollY')
            if abs(y - y0) < 2: return
            for i in range(1, steps + 1):
                q = i / steps; q = q * q * (3 - 2 * q); await t.evaluate(f'scrollTo(0,{y0 + (y - y0) * q})'); await snap(F)
        async def bring(sel, top=300):
            bx = await J.locator(sel).first.bounding_box()
            if bx['y'] < 80 or bx['y'] + bx['height'] > 640:
                y = await J.evaluate('scrollY'); await scroll_to(max(0, y + bx['y'] - top))
        async def ring(sel, tag='', spot=False, rad=0, t=None):
            t = t or J
            if sel is None: await t.evaluate('ringEl(null)')
            else: await t.locator(sel).first.evaluate('(el,a)=>ringEl(el,a[0],a[1],a[2])', [tag, spot, rad])
        async def cam(sel, z=1.25):
            if sel is None: await J.evaluate('camEl(null)')
            else: await J.locator(sel).first.evaluate('(el,z)=>camEl(el,z)', z)
            await live(0.55)
        async def click(sel, tag='', after=0.35, rad=0, t=None):
            t = t or J
            if t is J: await bring(sel)
            else:
                await t.locator(sel).first.evaluate("el=>el.scrollIntoView({block:'center'})"); await live(0.25)
            await ring(sel, tag, False, rad, t)
            bx = await t.locator(sel).first.bounding_box(); x = bx['x'] + bx['width'] / 2; y = bx['y'] + bx['height'] / 2
            await move(x, y); await still(0.2); await cur_pg[0].mouse.down(); await snap(0.1); await cur_pg[0].mouse.up(); await ring(None, t=t); await live(after)
        async def typ(sel, text, t=None, chunk=5):
            t = t or J
            bx = await t.locator(sel).first.bounding_box(); x = bx['x'] + bx['width'] / 2; y = bx['y'] + bx['height'] / 2
            await move(x, y, 8); await cur_pg[0].mouse.click(x, y)
            for i in range(0, len(text), chunk):
                await cur_pg[0].keyboard.type(text[i:i + chunk]); await snap(F * 2)
        async def slide(sel, v, t=None):
            t = t or J
            tr = await t.locator(sel).first.locator('.sl-track').bounding_box(); X = lambda q: tr['x'] + tr['width'] * (q - 1) / 9; Y = tr['y'] + tr['height'] / 2
            await move(X(5.5), Y, 9); await cur_pg[0].mouse.down(); await snap(0.08); await move(X(v), Y, 10); await live(0.25); await cur_pg[0].mouse.up(); await snap(0.06)
        def scene(): scenes.append(len(frames))
        async def card(html): await J.evaluate('h=>cardSet(h)', html)
        jcur = lambda v: J.evaluate(f"document.getElementById('cur').style.display='{v}'")
        async def to(pg):
            cur_pg[0] = pg; await pg.bring_to_front(); mouse[0] = 640; mouse[1] = 360; await pg.mouse.move(640, 360)
        part = lambda small, h: f'<div><small>{small}</small><h1>{h}</h1><em></em></div>'

        # 1-3 title, three parts, part one
        await jcur('none'); await card('<div><small>SCCU GROUP · TRIAL VERSION</small><h1>Your first real session</h1><em></em><p>How to run it, start to finish.</p></div>')
        say('1'); await still(0.5); await end('1', 0.25)
        scene(); await card('<div><small>THREE PARTS</small><ol><li><b>1</b>Before</li><li><b>2</b>During</li><li><b>3</b>After</li></ol></div>')
        say('2'); await still(0.4); await end('2', 0.25)
        scene(); await card(part('PART ONE', 'Before the session')); say('3'); await still(0.4); await end('3', 0.25)
        # 4 set up
        scene(); await card(''); await jcur('block'); await J.mouse.move(640, 360); await J.evaluate("stepSet(1,'Before the session')")
        say('4'); await typ('#nh-n', 'Jordan Lee', chunk=2); await typ('#nh-d', 'Futures', chunk=2); await click('[data-a=add-head]', 'Add', 0.4); await end('4')
        # 5 copy the link
        say('5'); await cam('#inv', 1.25); await click('[data-a=copy][data-id=inv]', 'Copy the link', 0.5); await end('5'); await cam(None)
        # 6 their phone
        scene(); await fr.fill('#hn', 'Jordan'); await G.evaluate("setCap('On their phone','They score themselves.','Six pillars. One real example for each.')"); await to(G)
        say('6'); await live(0.9); await click('[data-a=ss-go][data-id="0"]', '', 0.4, t=fr); await slide('.sl', 7, t=fr)
        await fr.evaluate("document.querySelector('textarea[data-k=ex]').scrollIntoView({block:'center'})"); await live(0.2)
        await typ('textarea[data-k=ex]', 'Kept the open day running when two staff were off sick.', t=fr, chunk=6)
        await fr.evaluate("(()=>{const e=S.heads.me.cur.self.resilience;e.d=_iso(new Date(Date.now()-864e5));save()})()"); await end('6')
        # 7 send to James
        scene(); await fr.evaluate(HEAD_FILL); await G.evaluate("setCap('On their phone','They press Send to James.','That sends a link back to you.')")
        say('7'); await live(0.7); await click('[data-a=share]', 'Send to James', 0.6, t=fr); await end('7')
        link = await fr.input_value('#sendlink'); print('link ok', link.startswith(SITE + '/trial#code=LP1.'), len(link))
        # 8 James scores
        scene(); await to(J); await J.evaluate('scrollTo(0,0)')
        y = await J.evaluate("document.querySelector('.jrow').getBoundingClientRect().top+scrollY-150"); await J.evaluate(f'scrollTo(0,{y})')
        say('8'); await live(0.3); await slide('.jrow .sl', 7); await typ('#jex-resilience', 'Stayed level in the Monday meeting the morning the absences landed.', chunk=7)
        await J.evaluate("(()=>{const e=curH().cur.james.resilience;e.d=_iso(new Date(Date.now()-864e5));save();render()})()"); await J.evaluate(J_FILL)
        await scroll_to(await J.evaluate('document.body.scrollHeight-720'), 22); await click('[data-a=j-lock]', 'Lock my scores', 0.3); await J.evaluate('scrollTo(0,0)'); await end('8', 0.2)
        # 9 the link arrives
        say('9'); await live(1.2); await J.goto(link); await J.wait_for_timeout(250); await J.evaluate('scrollTo(0,0)'); await live(0.8); await end('9', 0.2)
        # 10 loaded but hidden
        say('10'); await ring('main>.hidden-note', 'Loaded, and hidden', True, 16); await live(2.6); await ring('.rv-cta', 'Nothing shows until you reveal', True, 18); await end('10')
        await ring(None)
        # 11 they can change an answer
        scene(); await G.evaluate("setCap('On their phone','They can change an answer.','They just send you a new link.')"); await to(G)
        await fr.evaluate("document.querySelector('[data-a=unlock]').scrollIntoView({block:'center'})")
        say('11'); await live(0.6); await ring('[data-a=unlock]', '', False, 8, t=fr); await end('11'); await ring(None, t=fr)
        # 12 part two
        scene(); await to(J); await jcur('none'); await J.evaluate('stepSet(0)'); await card(part('PART TWO', 'In the room')); say('12'); await still(0.4); await end('12', 0.25)
        # 13 reveal
        scene(); await card(''); await jcur('block'); await J.evaluate("stepSet(2,'In the room')")
        say('13'); await click('[data-a=reveal]', 'Reveal both sets', 0.1); await live(1.5); await ring('.rv-row', 'Biggest gap first', False, 14); await end('13', 0.1); await ring(None)
        # 14 open it
        say('14'); await click('.xc-h', 'Open it', 0.3, 16); y = await J.evaluate("document.querySelector('.xc').getBoundingClientRect().top+scrollY-100"); await scroll_to(y, 12); await ring('.xc .two', 'Their example and yours', True, 16); await end('14', 0.15)
        await ring(None)
        # 15 agree
        say('15'); await bring('.xc .agree', 330); await click('.xc [data-a=agree][data-id="6"]', 'Agree a score', 0.4, 12); await end('15', 0.2)
        await J.evaluate("(()=>{const c=curH().cur;P.forEach(p=>{if(!c.agreed[p.id])c.agreed[p.id]=7});c.stage='focus';const f=suggest(curH());c.focus=f;ui.open=null;save();render();scrollTo(0,0)})()")
        # 16 focus, assignment, date
        scene(); say('16'); await live(0.5); await click('[data-a=asg][data-id="0"]', 'One assignment', 0.3, 14)
        await J.evaluate("(()=>{const c=curH().cur;c.due=_iso(new Date(Date.now()+28*864e5));save();render()})()"); await bring('#due', 420); await ring('#due', 'And a date', False, 14); await end('16', 0.3); await ring(None)
        await J.evaluate("(()=>{const c=curH().cur;c.done=true;c.sessionDate=TODAY;c.endedAt=Date.now();save();location.hash='summary';scrollTo(0,0)})()")
        # 17 part three
        scene(); await jcur('none'); await J.evaluate('stepSet(0)'); await card(part('PART THREE', 'After')); say('17'); await still(0.4); await end('17', 0.25)
        # 18 save the summary, 19 backup
        scene(); await card(''); await jcur('block'); await J.evaluate("stepSet(3,'After')"); await J.evaluate('scrollTo(0,0)')
        say('18'); await live(0.3); await cam('.sum-act', 1.2); await ring('[data-a=print]', 'Save as PDF', False, 0); await end('18', 0.25)
        say('19'); await ring('[data-a=backup]', 'Download a backup', False, 0); await live(2.2); await ring(None); await cam(None); await scroll_to(330, 30); await end('19', 0.3)
        # 20 three things, 21 close
        scene(); await jcur('none'); await J.evaluate('stepSet(0)')
        await card("<div><small>THREE THINGS TO REMEMBER</small><ol><li><b>1</b>Same laptop</li><li><b>2</b>Same browser</li><li><b>3</b>Don't clear your browsing history</li></ol></div>")
        say('20'); await still(0.4); await end('20', 0.3)
        scene(); await card('<div><small>SCCU GROUP · LEADERSHIP PILLARS</small><h1>Run your first one.</h1><em></em><p>sccu-leadership-pillars.vercel.app/trial</p></div>')
        say('21'); await still(0.4); await end('21', 1.0)
        print('page errors', errs); await b.close()
    scenes.append(len(frames)); files = []
    for i in range(len(scenes) - 1):
        fr_ = frames[scenes[i]:scenes[i + 1]]
        if not fr_: continue
        with open(f't{i}.txt', 'w') as f:
            for path, d in fr_: f.write(f"file '{os.path.abspath(path)}'\nduration {max(d, 0.02):.4f}\n")
            f.write(f"file '{os.path.abspath(fr_[-1][0])}'\n")
        r = subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f't{i}.txt', '-vf', 'fps=30,scale=1920:1080,format=yuv420p', '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', f't{i}.tmp.mp4']); assert r.returncode == 0
        os.rename(f't{i}.tmp.mp4', f't{i}.mp4'); files.append(os.path.abspath(f't{i}.mp4'))
    open('allt.txt', 'w').write(''.join(f"file '{x}'\n" for x in files))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', 'allt.txt', '-c', 'copy', 'joinedt.mp4'], check=True)
    T = total(); n_ = int((T + 0.5) * SR); rt, _ = sf.read('/home/claude/vo4/roomtone.wav', dtype='float32'); xf = int(0.05 * SR); body = rt.copy(); body[:xf] *= np.linspace(0, 1, xf); body[-xf:] *= np.linspace(1, 0, xf)
    track = np.zeros(n_ + len(body), dtype=np.float32); p_ = 0
    while p_ < n_: track[p_:p_ + len(body)] += body; p_ += len(body) - xf
    track = track[:n_]
    for k, s_ in A.items():
        o = int((marks[k] + 0.12) * SR); track[o:o + len(s_)] += s_[:len(track) - o]
    sf.write('voicet.wav', track, SR)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', 'joinedt.mp4', '-i', 'voicet.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-af', 'highpass=f=70,loudnorm=I=-16:TP=-1.5:LRA=11', '-shortest', '-movflags', '+faststart', 'outt.tmp.mp4'], check=True)
    os.rename('outt.tmp.mp4', 'SCCU-Leadership-Pillars-Trial-How-To.mp4'); json.dump({'marks': marks, 'dur': D}, open('markst.json', 'w'))
    print('total', round(T, 1), 'overruns', over)
asyncio.run(main())
