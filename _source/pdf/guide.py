import base64, sys, asyncio
from playwright.async_api import async_playwright
SITE=sys.argv[1] if len(sys.argv)>1 else 'https://sccu-leadership-pillars.vercel.app'
OUT=sys.argv[2] if len(sys.argv)>2 else 'Leadership-Pillars-First-Real-Session-Guide.pdf'
SHORT=SITE.replace('https://','')
B='/home/claude/build/node_modules/@fontsource'
fonts=[('Comfortaa','comfortaa',w) for w in (400,700)]+[('Nunito Sans','nunito-sans',w) for w in (400,600,700,800)]
css=''.join(f"@font-face{{font-family:'{f}';font-weight:{w};src:url(data:font/woff2;base64,{base64.b64encode(open(f'{B}/{s}/files/{s}-latin-{w}-normal.woff2','rb').read()).decode()}) format('woff2')}}" for f,s,w in fonts)
html=f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Leadership Pillars: your first real session</title><style>{css}
@page{{size:A4;margin:0}}*{{box-sizing:border-box;margin:0;padding:0}}
html{{width:210mm}}body{{width:210mm;color:#fff;font-family:'Nunito Sans',sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact;background:#182833}}
.pg{{position:relative;width:210mm;height:297mm;overflow:hidden;background:#182833}}
.pg::before{{content:"";position:absolute;left:0;right:0;top:0;height:9px;background:linear-gradient(90deg,#6c3481,#c32e81);z-index:2}}
.pg::after{{content:"";position:absolute;left:0;right:0;top:0;height:300px;background:radial-gradient(ellipse at 50% 0%,rgba(195,46,129,.24),transparent 68%);z-index:0}}
.w{{position:relative;z-index:1;height:100%;padding:34px 44px 22px;display:flex;flex-direction:column;gap:13px}}
.eb{{font-size:10px;font-weight:800;letter-spacing:.2em;text-transform:uppercase;color:rgba(255,255,255,.55)}}
.top{{display:flex;justify-content:space-between;align-items:center}}
.for{{font-size:10.5px;font-weight:800;padding:5px 13px;border-radius:999px;border:1px solid rgba(255,255,255,.25);color:rgba(255,255,255,.85)}}
h1{{font-family:'Comfortaa';font-weight:700;font-size:31px;line-height:1.12;letter-spacing:-.01em}}
.lead{{font-size:13.5px;line-height:1.5;color:rgba(255,255,255,.78);max-width:640px;margin-top:-5px}}
.lead a{{color:#53baab;font-weight:800;text-decoration:none;white-space:nowrap}}
h3{{font-family:'Comfortaa';font-weight:700;font-size:14px;margin-bottom:8px}}
.cols{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}
.card{{padding:15px 17px;border-radius:14px;background:#1f3340;border:1px solid rgba(255,255,255,.13)}}
ol{{list-style:none;display:grid;gap:8px;counter-reset:n}}
ol li{{counter-increment:n;position:relative;padding-left:27px;font-size:11.6px;line-height:1.45;color:rgba(255,255,255,.8)}}
ol li::before{{content:counter(n);position:absolute;left:0;top:0;width:19px;height:19px;border-radius:50%;display:grid;place-items:center;background:linear-gradient(90deg,#6c3481,#c32e81);font-family:'Comfortaa';font-weight:700;font-size:10px;color:#fff}}
ol li b,ul li b{{color:#fff}}
ul{{list-style:none;display:grid;gap:7px}}
ul li{{position:relative;padding-left:15px;font-size:11.6px;line-height:1.45;color:rgba(255,255,255,.8)}}
ul li::before{{content:"";position:absolute;left:0;top:7px;width:6px;height:6px;border-radius:50%;background:#53baab}}
.msg{{padding:14px 17px;border-radius:14px;border:1px solid rgba(83,186,171,.55);background:rgba(83,186,171,.09)}}
.msg p{{font-size:12px;line-height:1.5;color:rgba(255,255,255,.9);font-style:italic}}
.hard{{padding:15px 17px;border-radius:14px;border:1px solid rgba(195,46,129,.6);background:rgba(195,46,129,.07)}}
.three{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}}
.three div{{padding-left:13px;border-left:2px solid rgba(255,255,255,.25)}}
.three b{{display:block;font-size:12px;font-weight:800;margin-bottom:3px}}
.three span{{font-size:11.2px;line-height:1.45;color:rgba(255,255,255,.75)}}
.foot{{margin-top:auto;display:flex;justify-content:space-between;font-size:9.5px;color:rgba(255,255,255,.5);padding-top:10px;border-top:1px solid rgba(255,255,255,.12)}}
</style></head><body><div class="pg"><div class="w">
<div class="top"><span class="eb">SCCU Group · Leadership Pillars</span><span class="for">For James Pease · trial version</span></div>
<h1>Your first real session.</h1>
<p class="lead">The trial version runs a real session with a real head, without logins. Everything you enter stays on your laptop, and everything they enter stays on their device until they send it to you. Open it at <a href="{SITE}/trial">{SHORT}/trial</a></p>
<div class="cols">
<div class="card"><h3>Before the session</h3><ol>
<li><b>Set it up.</b> Open the trial on the laptop you will run the session on. Type the head's name. It stays in your browser.</li>
<li><b>Send their link.</b> Press Copy the link and send it to them with the message below. Give them a day or two.</li>
<li><b>Score them yourself.</b> Six pillars, one dated example each. About ten minutes. Then press Lock my scores.</li>
<li><b>Open the link they send back.</b> Same laptop, same browser. The link is long, which is normal. Their scores load and stay hidden until the reveal.</li>
</ol></div>
<div class="card"><h3>In the room, about 20 to 30 minutes</h3><ol>
<li><b>Say what it is.</b> "This is where you were this month. It isn't who you are."</li>
<li><b>Reveal both sets.</b> Turn the screen so you can both see it.</li>
<li><b>Take the biggest gap first.</b> They talk first. Use the opening line on screen. Then give your example.</li>
<li><b>Agree a score for each pillar.</b> Never the average.</li>
<li><b>One focus, one assignment, one date.</b></li>
<li><b>Save the summary</b> as a PDF and send them a copy. Then press Download a backup.</li>
</ol></div>
</div>
<div class="msg"><p class="eb" style="font-style:normal;margin-bottom:7px;color:#53baab">A message you can send with the link</p>
<p>"I'd like to try something new in our next 1-1. Before we meet, score yourself on six leadership pillars using this link. It takes about ten minutes, and each score needs one real example from this month. I'm scoring you too, and neither of us sees the other's numbers until we sit down together. It's there to start a good conversation. When you finish, it gives you a link to send back to me."</p></div>
<div class="hard"><h3>If they disagree, or go quiet</h3><ul>
<li><b>Go back to the two examples.</b> "Tell me more about that day." The examples settle it, not the numbers.</li>
<li><b>They may be right.</b> If their example changes your mind, say so and agree the higher number. That builds more trust than holding your line.</li>
<li><b>If you still see it differently, say so out loud.</b> Agree a number for this month only, and make that pillar the first thing you look at next time.</li>
<li><b>Keep it to one month.</b> A hard month drops a score and a good month brings it back. A one-point difference is not worth a long debate.</li>
</ul></div>
<div><p class="eb" style="margin-bottom:10px">Good to know</p><div class="three">
<div><b>It lives on one laptop</b><span>Use the same laptop and the same browser throughout. Don't clear your browsing data. Download a backup when you finish.</span></div>
<div><b>Hidden by design, not locked</b><span>Their scores stay off your screen until the reveal. The trial relies on both of you playing it straight. Logins come with the full version.</span></div>
<div><b>They can change their mind</b><span>If they want to fix something after sending, they can. They send a new link and you open it before the reveal.</span></div>
</div></div>
<div class="card" style="padding:13px 17px"><h3 style="margin-bottom:5px">Afterwards, tell Callum three things</h3><ul style="grid-template-columns:repeat(3,1fr);gap:14px">
<li>Did the reveal start a real conversation?</li><li>Where did you get stuck, or have to guess?</li><li>What did they say about it afterwards?</li></ul></div>
<div class="foot"><span>Prepared for SCCU Group by Callum Hardingham · Leadership Infrastructure Systems</span><span>November 2026</span></div>
</div></div></body></html>'''
open('guide.html','w').write(html)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox']); pg=await b.new_page(viewport={'width':794,'height':1123})
        await pg.goto('file:///home/claude/onepager/guide.html'); await pg.wait_for_timeout(700)
        print('content',await pg.evaluate("(()=>{const w=document.querySelector('.w');const f=w.querySelector('.foot');return [w.scrollHeight,w.clientHeight,Math.round(f.getBoundingClientRect().top-f.previousElementSibling.getBoundingClientRect().bottom)]})()"))
        await pg.screenshot(path='guide.png'); await pg.pdf(path=OUT,format='A4',print_background=True,margin={'top':'0','right':'0','bottom':'0','left':'0'}); await b.close()
asyncio.run(main())
