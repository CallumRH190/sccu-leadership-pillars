import base64, sys, asyncio
from playwright.async_api import async_playwright
SITE=sys.argv[1] if len(sys.argv)>1 else 'https://sccu-leadership-pillars.vercel.app'
OUT=sys.argv[2] if len(sys.argv)>2 else 'draft2.pdf'
SHORT=SITE.replace('https://','')
B='/home/claude/build/node_modules/@fontsource'
fonts=[('Comfortaa','comfortaa',w) for w in (400,700)]+[('Nunito Sans','nunito-sans',w) for w in (400,600,700,800)]
css=''.join(f"@font-face{{font-family:'{f}';font-weight:{w};src:url(data:font/woff2;base64,{base64.b64encode(open(f'{B}/{s}/files/{s}-latin-{w}-normal.woff2','rb').read()).decode()}) format('woff2')}}" for f,s,w in fonts)
img=lambda p:'data:image/jpeg;base64,'+base64.b64encode(open(p,'rb').read()).decode()
P=[('Reactivity','Resilience'),('Inaction','Decisiveness'),('Rigidity','Ingenuity'),('Avoidance','Assertiveness'),('Assumption','Communication'),('Indifference','Enthusiasm')]
def card(n,url,pic,play,title,dur,text,btn,ghost):
    return f'''<a class="card" href="{url}"><div class="th" style="background-image:url({img(pic)})"><span class="n">{n}</span>{'<span class="play"></span>' if play else ''}</div>
<div class="cb"><span class="dur">{dur}</span><h2>{title}</h2><p>{text}</p><span class="btn {'ghost' if ghost else ''}">{btn}</span></div></a>'''
html=f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Leadership Pillars: try it before Tuesday</title><style>{css}
@page{{size:A4;margin:0}}*{{box-sizing:border-box;margin:0;padding:0}}
html{{width:210mm}}
body{{width:210mm;color:#fff;font-family:'Nunito Sans',sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact;background:#182833}}
.pg{{position:relative;width:210mm;height:297mm;overflow:hidden;background:#182833;page-break-after:always}}
.pg::before{{content:"";position:absolute;left:0;right:0;top:0;height:9px;background:linear-gradient(90deg,#6c3481,#c32e81);z-index:2}}
.pg::after{{content:"";position:absolute;left:0;right:0;top:0;height:330px;background:radial-gradient(ellipse at 50% 0%,rgba(195,46,129,.26),transparent 68%);z-index:0}}
.w{{position:relative;z-index:1;height:100%;padding:36px 46px 24px;display:flex;flex-direction:column;gap:13px}}
.eb{{font-size:10.5px;font-weight:800;letter-spacing:.2em;text-transform:uppercase;color:rgba(255,255,255,.55)}}
.top{{display:flex;justify-content:space-between;align-items:center}}
.for{{font-size:11px;font-weight:800;padding:6px 14px;border-radius:999px;border:1px solid rgba(255,255,255,.25);color:rgba(255,255,255,.85)}}
h1{{font-family:'Comfortaa';font-weight:700;font-size:35px;line-height:1.12;letter-spacing:-.01em;max-width:620px}}
.lead{{font-size:15px;line-height:1.5;color:rgba(255,255,255,.78);max-width:610px;margin-top:-6px}}
.one{{display:flex;gap:14px;align-items:center;padding:13px 18px;border-radius:14px;background:rgba(83,186,171,.1);border:1px solid rgba(83,186,171,.55);font-size:13.5px;line-height:1.45}}
.one b{{color:#53baab}}
.one a{{margin-left:auto;white-space:nowrap;padding:9px 18px;border-radius:999px;background:linear-gradient(90deg,#6c3481,#c32e81);color:#fff;font-weight:800;font-size:13px;text-decoration:none}}
.cards{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}}
.card{{display:flex;flex-direction:column;border-radius:16px;background:#1f3340;border:1px solid rgba(255,255,255,.13);overflow:hidden;text-decoration:none;color:#fff}}
.th{{position:relative;aspect-ratio:16/9;background-size:cover;background-position:top center;border-bottom:1px solid rgba(255,255,255,.1)}}
.th .n{{position:absolute;left:10px;top:10px;width:30px;height:30px;border-radius:50%;display:grid;place-items:center;background:linear-gradient(90deg,#6c3481,#c32e81);font-family:'Comfortaa';font-weight:700;font-size:14px;box-shadow:0 6px 18px rgba(0,0,0,.45)}}
.play{{position:absolute;left:50%;top:50%;width:46px;height:46px;margin:-23px 0 0 -23px;border-radius:50%;background:rgba(255,255,255,.95);box-shadow:0 10px 30px rgba(0,0,0,.5)}}
.play::after{{content:"";position:absolute;left:19px;top:14px;border-left:14px solid #182833;border-top:9px solid transparent;border-bottom:9px solid transparent}}
.cb{{padding:13px 15px 15px;display:flex;flex-direction:column;gap:4px;flex:1}}
.dur{{font-size:9.5px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:#53baab}}
.cb h2{{font-family:'Comfortaa';font-weight:700;font-size:15.5px;line-height:1.2}}
.cb p{{font-size:11.5px;line-height:1.45;color:rgba(255,255,255,.72);flex:1}}
.btn{{align-self:flex-start;margin-top:8px;padding:7px 15px;border-radius:999px;background:linear-gradient(90deg,#6c3481,#c32e81);font-weight:800;font-size:11.5px}}
.btn.ghost{{background:none;border:1px solid rgba(255,255,255,.45)}}
.try{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}}
.try div{{padding:2px 0 2px 14px;border-left:2px solid rgba(255,255,255,.25)}}
.try div.m{{border-left-color:#c32e81}}
.try small{{display:block;font-size:9.5px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:rgba(255,255,255,.55);margin-bottom:3px}}
.try div.m small{{color:#e56cae}}
.try b{{display:block;font-family:'Comfortaa';font-size:14px;margin-bottom:4px}}
.try span{{font-size:11.5px;line-height:1.45;color:rgba(255,255,255,.75)}}
.pil{{display:grid;grid-template-columns:repeat(6,1fr);gap:8px}}
.pil div{{padding:9px 6px 10px;border-radius:12px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);text-align:center}}
.pil small{{display:block;font-size:8px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:rgba(255,255,255,.5)}}
.pil i{{display:block;width:22px;height:2px;border-radius:2px;margin:5px auto;background:linear-gradient(90deg,#6c3481,#c32e81)}}
.pil b{{font-family:'Comfortaa';font-size:11.5px}}
.know{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;padding:14px 18px;border-radius:16px;border:1px dashed rgba(255,255,255,.25)}}
.know b{{display:block;font-size:12.5px;font-weight:800;margin-bottom:3px}}
.know span{{font-size:11.3px;line-height:1.45;color:rgba(255,255,255,.72)}}
.ask{{font-size:12.3px;line-height:1.5;color:rgba(255,255,255,.85)}}.ask b{{color:#53baab}}
.foot{{margin-top:auto;display:flex;justify-content:space-between;font-size:10px;color:rgba(255,255,255,.5);padding-top:11px;border-top:1px solid rgba(255,255,255,.12)}}
/* page 2 */
.p2 .w{{gap:20px;padding-top:44px}}
.p2 h1{{font-size:33px}}
h3{{font-family:'Comfortaa';font-weight:700;font-size:15px;margin-bottom:5px}}
.steps{{display:grid;gap:10px}}
.step{{display:grid;grid-template-columns:34px 92px 1fr;gap:14px;align-items:start;padding:14px 18px;border-radius:14px;background:#1f3340;border:1px solid rgba(255,255,255,.13)}}
.step i{{width:34px;height:34px;border-radius:50%;display:grid;place-items:center;background:linear-gradient(90deg,#6c3481,#c32e81);font-family:'Comfortaa';font-weight:700;font-style:normal;font-size:15px}}
.step .dur{{padding-top:9px}}
.step p{{font-size:12.3px;line-height:1.5;color:rgba(255,255,255,.76)}}
.step p b{{color:#fff}}
.dec{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}}
.dec div{{padding:15px 16px;border-radius:14px;border:1px solid rgba(195,46,129,.6);background:rgba(195,46,129,.07)}}
.dec small{{display:block;font-size:9.5px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:#e56cae;margin-bottom:6px}}
.dec p{{font-size:12px;line-height:1.5;color:rgba(255,255,255,.78)}}
.cols{{display:grid;grid-template-columns:1fr 1fr;gap:26px}}
.cols ul{{list-style:none;display:grid;gap:7px}}
.cols li{{font-size:12.2px;line-height:1.45;color:rgba(255,255,255,.78);padding-left:16px;position:relative}}
.cols li::before{{content:"";position:absolute;left:0;top:7px;width:6px;height:6px;border-radius:50%;background:#53baab}}
.cols .nx li::before{{background:none;border:1.5px solid rgba(255,255,255,.55)}}
.time{{display:flex;gap:26px;align-items:center;padding:16px 20px;border-radius:14px;border:1px dashed rgba(255,255,255,.25)}}
.time b.big{{font-family:'Comfortaa';font-size:27px;white-space:nowrap}}
.time p{{font-size:12.3px;line-height:1.5;color:rgba(255,255,255,.76)}}
</style></head><body>
<div class="pg"><div class="w">
<div class="top"><span class="eb">SCCU Group · Leadership Pillars</span><span class="for">For James Pease · before Tuesday 17 November</span></div>
<h1>Your Leadership Pillars tool is ready to try.</h1>
<p class="lead">Six pillars. One honest conversation a month with each head. Two short videos, then the tool itself. Everything inside is sample data, so you can't break anything.</p>
<div class="one"><span><b>One thing before Tuesday:</b> run Tom Ashby's practice session from start to finish. About 20 minutes. The rest is optional.</span><a href="{SITE}/start">Start here</a></div>
<div class="cards">
{card(1,SITE+'/start#why','why.jpg',True,'Why it works','2½ minutes',"What it gives you, why the head scores first, and why these six pillars.",'Play',False)}
{card(2,SITE+'/start#how','video.jpg',True,'How to run a session','90 seconds','One full session, from the self-score to the one-page summary. Every click.','Play',True)}
{card(3,SITE+'/','tool.jpg',False,'Open the tool','About 20 minutes','It opens in your browser. Nothing to install and no login.','Open',True)}
</div>
<div><p class="eb" style="margin-bottom:11px">Three ways to try it &nbsp;·&nbsp; {SHORT}/start</p><div class="try">
<div><small>2 minutes</small><b>See a reveal</b><span>Open Session and pick Dev Okafor. Both sets of scores are already in. Press Reveal both sets.</span></div>
<div class="m"><small>20 minutes · the one to do</small><b>Run Tom Ashby's session</b><span>Open Session and pick Tom. Press "Fill sample scores", then Lock my scores. Reveal, agree a score on each pillar, pick one focus and set the assignment.</span></div>
<div><small>10 minutes · optional</small><b>Be a head</b><span>Click your name, top right, and choose Elena Marsh. Score yourself on all six pillars the way a head will.</span></div>
</div></div>
<div><p class="eb" style="margin-bottom:9px">The six pillars, each from its opposite</p><div class="pil">{''.join(f'<div><small>{o}</small><i></i><b>{p}</b></div>' for o,p in P)}</div></div>
<div class="know">
<div><b>It's all sample data</b><span>The five heads are made up and it saves in your browser only. Please don't enter real heads yet. Reset the demo from your name menu. Your own examples stay.</span></div>
<div><b>Who sees the scores</b><span>A head sees only their own. You and Scott see every head's. In this demo you can switch between people from your name menu.</span></div>
<div><b>The time it takes</b><span>About 20 minutes together with each head, once a month. Scoring beforehand takes each of you about ten minutes.</span></div>
</div>
<p class="ask"><b>Two asks.</b> Tell Callum anything that feels clunky or doesn't sound like you. And send him one example of your own for each pillar. A line each is enough.</p>
<div class="foot"><span>Prepared for SCCU Group by Callum Hardingham · Leadership Infrastructure Systems</span><span>Page 1 of 2 · November 2026</span></div>
</div></div>

<div class="pg p2"><div class="w">
<div class="top"><span class="eb">SCCU Group · Leadership Pillars</span><span class="for">Tuesday 17 November · with Scott</span></div>
<h1>Tuesday: three minutes to show it, three decisions to make.</h1>
<div><p class="eb" style="margin-bottom:11px">The three-minute demo</p><div class="steps">
<div class="step"><i>1</i><span class="dur">30 seconds</span><p><b>The team picture.</b> Click your name, choose Reset the demo, then click it again and choose Scott Riddell. One screen shows each head's latest agreed scores against the standard, and the team's weakest pillar.</p></div>
<div class="step"><i>2</i><span class="dur">90 seconds</span><p><b>The reveal.</b> Switch back to yourself. Open Session, pick Dev Okafor and press Reveal both sets. Scroll down and open the first pillar, the biggest gap. His example and yours sit side by side, with the questions to ask underneath.</p></div>
<div class="step"><i>3</i><span class="dur">60 seconds</span><p><b>What the head takes away.</b> On Team, press Summary next to Priya Nair. One page: scores, evidence, one focus, one assignment. Then open Profiles and pick Priya to show six months of movement.</p></div>
</div></div>
<div><p class="eb" style="margin-bottom:11px">Three decisions for Scott</p><div class="dec">
<div><small>Decision 1</small><h3>Who starts, and when</h3><p>Every head from the first month, or two heads first. Real sessions begin once the version with logins is ready.</p></div>
<div><small>Decision 2</small><h3>Who sees the scores</h3><p>Confirm that a head sees only their own, and that you and Scott see every head's. Decide whether anyone else should.</p></div>
<div><small>Decision 3</small><h3>Who scores you both</h3><p>You and Scott are scored on the same six pillars, kept apart from the heads. Self-score only, each other, or Callum.</p></div>
</div></div>
<div class="time"><b class="big">20 + 10</b><p><b style="color:#fff">Minutes it costs, per head, per month.</b> About 20 minutes together, plus about ten minutes for you to score beforehand. The head spends the same. With five heads that is about two and a half hours of your month.</p></div>
<div class="cols">
<div><h3>Built and working today</h3><ul>
<li>The full session: self-score, blind score, reveal, agree, focus, assignment.</li>
<li>All the content: six pillars, 18 traits, the written 3, 5, 7 and 9 for each.</li>
<li>The team view, each head's profile and the one-page summary.</li></ul></div>
<div class="nx"><h3>Next build, after Tuesday</h3><ul>
<li>A login for each head. Today anyone can switch person from the name menu, so hidden scores are hidden by role only.</li>
<li>Saved history from month to month, and your real heads of department.</li>
<li>The integrity gate. The demo always shows a pass.</li></ul></div>
</div>
<div class="foot"><span>Prepared for SCCU Group by Callum Hardingham · Leadership Infrastructure Systems</span><span>Page 2 of 2 · November 2026</span></div>
</div></div>
</body></html>'''
open('page2.html','w').write(html)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox']); pg=await b.new_page(viewport={'width':794,'height':1123})
        await pg.goto('file:///home/claude/onepager/page2.html'); await pg.wait_for_timeout(700)
        for i in (0,1):
            print('page',i+1,'content',await pg.evaluate(f"(()=>{{const w=document.querySelectorAll('.w')[{i}];const f=w.querySelector('.foot');return [w.scrollHeight,w.clientHeight,Math.round(f.getBoundingClientRect().top-f.previousElementSibling.getBoundingClientRect().bottom)]}})()"))
        await pg.screenshot(path='preview2.png',full_page=True)
        await pg.pdf(path=OUT,format='A4',print_background=True,margin={'top':'0','right':'0','bottom':'0','left':'0'}); await b.close()
asyncio.run(main())
