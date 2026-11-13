import base64
B='/home/claude/build/node_modules/@fontsource'
fonts=[('Comfortaa','comfortaa',w) for w in (400,700)]+[('Nunito Sans','nunito-sans',w) for w in (400,600,700,800)]
css=''.join(f"@font-face{{font-family:'{f}';font-weight:{w};src:url(data:font/woff2;base64,{base64.b64encode(open(f'{B}/{s}/files/{s}-latin-{w}-normal.woff2','rb').read()).decode()}) format('woff2')}}" for f,s,w in fonts)
P=[('Reactivity','Resilience'),('Inaction','Decisiveness'),('Rigidity','Ingenuity'),('Avoidance','Assertiveness'),('Assumption','Communication'),('Indifference','Enthusiasm')]
rows=''.join(f'<div class="prow r{i}" data-s="1" style="transition-delay:{0.75+i*0.72:.2f}s"><span class="o">{o}</span><i></i><b>{p}</b></div>' for i,(o,p) in enumerate(P))
ticks=''.join(f'<u style="left:{i/9*100:.2f}%">{i+1}</u>' for i in range(10))
dots=''.join(f'<em style="left:{71.6+ (k%3)*3.2:.1f}%;bottom:{18+(k//3)*20}px"></em>' for k in range(9))
html=f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Why it works</title><style>{css}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1280px;height:720px;overflow:hidden;background:#182833;color:#fff;font-family:'Nunito Sans',sans-serif}}
body::before{{content:"";position:absolute;inset:0;background:radial-gradient(ellipse at 50% -10%,rgba(195,46,129,.26),transparent 60%)}}
body::after{{content:"";position:absolute;left:0;right:0;top:0;height:5px;background:linear-gradient(90deg,#6c3481,#c32e81)}}
.brand{{position:absolute;left:48px;top:30px;font-size:12px;font-weight:800;letter-spacing:.24em;color:rgba(255,255,255,.5);z-index:3}}
.prog{{position:absolute;left:48px;right:48px;bottom:28px;height:3px;background:rgba(255,255,255,.12);border-radius:3px;z-index:3}}
.prog i{{display:block;height:100%;width:0;background:#53baab;border-radius:3px;transition:width .6s}}
.sc{{position:absolute;inset:0;padding:86px 72px 70px;display:none;flex-direction:column;justify-content:center;z-index:2}}
.sc.on{{display:flex}}
[data-s]{{opacity:0;transform:translateY(16px);transition:opacity .6s ease,transform .6s ease}}
[data-s].v{{opacity:1;transform:none}}
[data-h].gone{{opacity:0!important}}
.eb{{font-size:14px;font-weight:800;letter-spacing:.2em;text-transform:uppercase;color:#53baab;margin-bottom:14px}}
h1{{font-family:'Comfortaa';font-weight:700;font-size:64px;line-height:1.1}}
h2{{font-family:'Comfortaa';font-weight:700;font-size:44px;line-height:1.15;max-width:900px}}
.sub{{font-size:24px;color:rgba(255,255,255,.75);margin-top:16px;max-width:760px}}
.rule{{width:120px;height:4px;border-radius:4px;background:linear-gradient(90deg,#6c3481,#c32e81);margin:24px 0}}
.center{{align-items:center;text-align:center}}
.list{{display:grid;gap:18px;margin-top:34px}}
.li{{display:flex;align-items:center;gap:22px;font-family:'Comfortaa';font-weight:700;font-size:34px}}
.li b{{flex:none;width:54px;height:54px;border-radius:50%;display:grid;place-items:center;background:linear-gradient(90deg,#6c3481,#c32e81);font-size:22px}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:28px;margin-top:34px}}
.card{{background:#1f3340;border:1px solid rgba(255,255,255,.13);border-radius:22px;padding:30px 32px}}
.card small{{display:block;font-size:13px;font-weight:800;letter-spacing:.18em;text-transform:uppercase;color:rgba(255,255,255,.55);margin-bottom:10px}}
.card h3{{font-family:'Comfortaa';font-weight:700;font-size:34px;line-height:1.15}}
.card p{{font-size:20px;color:rgba(255,255,255,.78);margin-top:10px;line-height:1.4}}
.card.hot{{border-color:#c32e81;box-shadow:0 0 0 3px rgba(195,46,129,.35)}}
.note{{margin-top:22px;font-size:22px;color:#f2b866;font-weight:700}}
.prows{{display:grid;gap:9px;margin-top:22px}}
.prow{{display:grid;grid-template-columns:230px 1fr 300px;align-items:center;gap:22px}}
.prow .o{{font-family:'Comfortaa';font-size:22px;color:rgba(255,255,255,.5);text-align:right}}
.prow i{{height:4px;border-radius:4px;background:linear-gradient(90deg,rgba(255,255,255,.14),#6c3481 45%,#c32e81)}}
.prow b{{font-family:'Comfortaa';font-weight:700;font-size:30px}}
.chips{{display:flex;gap:12px;margin-top:22px}}
.chip{{font-size:18px;font-weight:800;padding:10px 20px;border-radius:999px;border:1.5px solid #53baab;color:#53baab}}
.prow.r4.hi b{{color:#53baab}}.prow.r4.hi .o{{color:#fff}}
.fake{{position:absolute;right:72px;top:92px;width:400px;border:1.5px dashed rgba(255,255,255,.4);border-radius:18px;padding:18px 22px;background:#182833}}
.fake small{{font-size:12px;font-weight:800;letter-spacing:.16em;text-transform:uppercase;color:#f2b866}}
.fake p{{font-family:'Comfortaa';font-size:22px;margin-top:6px}}
.lane{{display:grid;grid-template-columns:150px 1fr;gap:26px;align-items:center}}
.lane .who{{font-family:'Comfortaa';font-weight:700;font-size:26px}}
.words{{display:flex;justify-content:space-between;font-family:'Comfortaa';font-size:18px;color:rgba(255,255,255,.55);margin-bottom:22px}}
.trk{{position:relative;height:6px;border-radius:6px;background:rgba(255,255,255,.16)}}
.mk{{position:absolute;top:50%;left:0;width:50px;height:50px;margin:-25px 0 0 -25px;border-radius:50%;display:grid;place-items:center;font-family:'Comfortaa';font-weight:700;font-size:21px;opacity:0;transition:left 1.1s cubic-bezier(.2,.8,.2,1),opacity .4s;transform:none!important;box-shadow:0 8px 22px rgba(0,0,0,.4)}}
.mk.v{{opacity:1;left:var(--x)}}
.mk.h{{background:#53baab;color:#0e2a26}}.mk.j{{background:#c32e81;left:100%}}.mk.j.v{{left:var(--x)}}.mk.a{{background:linear-gradient(90deg,#6c3481,#c32e81);width:58px;height:58px;margin:-29px 0 0 -29px}}
.why{{font-size:21px;color:rgba(255,255,255,.8);margin:20px 0 0 176px}}
.why b{{color:#fff}}
.wall{{display:flex;align-items:center;gap:16px;margin:26px 0 26px 176px;font-size:14px;font-weight:800;letter-spacing:.18em;text-transform:uppercase;color:rgba(255,255,255,.5)}}
.wall::before,.wall::after{{content:"";flex:1;border-top:2px dashed rgba(255,255,255,.25)}}
.banner{{margin-top:30px;align-self:center;font-family:'Comfortaa';font-weight:700;font-size:26px;padding:14px 30px;border-radius:999px;background:linear-gradient(90deg,#6c3481,#c32e81)}}
.gap{{position:absolute;top:50%;height:6px;margin-top:-3px;background:#fff;border-radius:6px;left:var(--l);width:var(--w);transform:scaleX(0)!important;transform-origin:left;transition:transform .8s ease-out .9s,opacity .3s}}
.gap.v{{transform:scaleX(1)!important}}
.gaplab{{position:absolute;left:var(--l);width:var(--w);top:-58px;text-align:center;font-family:'Comfortaa';font-weight:700;font-size:20px;transition-delay:1.5s}}
.std{{position:absolute;left:66.67%;top:-30px;bottom:-30px;width:3px;margin-left:-1.5px;background:rgba(255,255,255,.75);transform:none!important}}
.std b{{position:absolute;top:-30px;left:50%;transform:translateX(-50%);font-size:13px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;white-space:nowrap}}
.ticks u{{position:absolute;top:26px;transform:translateX(-50%);text-decoration:none;font-size:15px;font-weight:700;color:rgba(255,255,255,.5)}}
.dots em{{position:absolute;width:16px;height:16px;border-radius:50%;background:#53baab;margin-left:-8px;opacity:.9}}
.quote{{font-family:'Comfortaa';font-size:28px;line-height:1.4}}
.date{{display:inline-block;font-size:14px;font-weight:800;letter-spacing:.14em;padding:6px 14px;border-radius:999px;background:#53baab;color:#0e2a26;margin-bottom:16px}}
.big{{font-family:'Comfortaa';font-weight:700;font-size:92px;line-height:1;background:linear-gradient(90deg,#b56cd0,#f07ab8);-webkit-background-clip:text;color:transparent}}
.pc{{display:flex;gap:10px;margin-top:20px;flex-wrap:wrap}}
.pc span{{font-size:18px;font-weight:800;padding:10px 18px;border-radius:999px;border:1.5px solid rgba(255,255,255,.25);color:rgba(255,255,255,.4);text-decoration:line-through}}
.pc span.y{{border-color:#53baab;color:#0e2a26;background:#53baab;text-decoration:none}}
.three{{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;margin-top:34px}}
.next{{margin-top:34px;font-family:'Comfortaa';font-weight:700;font-size:28px;padding:16px 36px;border-radius:999px;background:linear-gradient(90deg,#6c3481,#c32e81)}}
svg.sp path{{stroke-dasharray:700;stroke-dashoffset:700;transition:stroke-dashoffset 2.2s ease .3s}}
.v svg.sp path,svg.sp.v path{{stroke-dashoffset:0}}
</style></head><body>
<div class="brand">SCCU GROUP · LEADERSHIP PILLARS</div><div class="prog"><i id="pg"></i></div>

<section class="sc center" id="sc-t"><p class="eb" data-s="1">Before the how</p><h1 data-s="1">Why it works</h1><div class="rule" data-s="1"></div><p class="sub" data-s="1">The thinking behind Leadership Pillars, in three minutes.</p></section>

<section class="sc" id="sc-a"><p class="eb" data-s="1">What it gives you</p><h2 data-s="1">Three things, James.</h2><div class="list">
<div class="li" data-s="1" style="transition-delay:1.6s"><b>1</b>Fewer fires landing on your desk</div>
<div class="li" data-s="2"><b>2</b>Heads who deal with it at their own level</div>
<div class="li" data-s="3"><b>3</b>One fair standard for every head</div></div></section>

<section class="sc" id="sc-b"><p class="eb" data-s="1">The idea underneath</p><h2 data-s="1">Results tell you what. Behaviour tells you why.</h2><div class="two">
<div class="card" data-s="1" style="transition-delay:.9s"><small>Scorecards</small><h3>What happened</h3><p>Targets, numbers, deadlines.</p></div>
<div class="card" id="bcard" data-s="3"><small>Leadership Pillars</small><h3>Why it happened</h3><p>How your heads behave.</p></div></div>
<p class="note" data-s="2">A head can hit the numbers and still leave problems for you to clean up.</p></section>

<section class="sc" id="sc-c"><p class="eb" data-s="1">The six pillars</p><h2 data-s="1" style="font-size:36px">Each one runs from its opposite.</h2><div class="prows">{rows}</div>
<div class="chips"><span class="chip" data-s="2">Your words and Callum's</span><span class="chip" data-s="2" style="transition-delay:1.6s">The leadership research</span><span class="chip" data-s="2" style="transition-delay:3.6s">Five real SCCU situations</span></div>
<div class="fake" data-s="4"><small>Looks like Enthusiasm but isn't</small><p>Cheerleading without delivery</p></div></section>

<section class="sc" id="sc-d"><p class="eb" data-s="1">The order</p><h2 data-s="1" style="font-size:38px;margin-bottom:34px">The head scores first. Then you score blind.</h2>
<div class="lane" data-s="1"><span class="who" style="color:#53baab">The head</span><div><div class="words"><span>Avoidance</span><span>Assertiveness</span></div><div class="trk"><b class="mk h" data-s="1" style="--x:55.6%;transition-delay:.8s">6</b></div></div></div>
<p class="why" data-s="2"><b>Scores first,</b> so the thinking is their own. See your number and they stop thinking and start agreeing.</p>
<div class="wall" data-s="3">Neither sees the other</div>
<div class="lane" data-s="3"><span class="who" style="color:#f07ab8">You</span><div><div class="trk"><b class="mk j" data-s="3" style="--x:77.8%;transition-delay:.9s">8</b></div></div></div>
<p class="why" data-s="3" style="transition-delay:2.4s"><b>Score blind,</b> so their number can't pull yours towards it.</p>
<div class="banner" data-s="4">Two independent views beat one view and an echo</div></section>

<section class="sc" id="sc-e"><p class="eb" data-s="1">The reveal</p><h2 data-s="1" style="margin-bottom:96px">The gap is the conversation.</h2>
<div style="padding:0 40px" data-s="1"><div class="words"><span>Avoidance</span><span>Assertiveness</span></div><div class="trk"><i class="gap" data-s="1" style="--l:55.6%;--w:22.2%"></i><span class="gaplab" data-s="1" style="--l:55.6%;--w:22.2%">Gap of 2</span><b class="mk h" data-s="1" style="--x:55.6%">6</b><b class="mk j" data-s="1" style="--x:77.8%">8</b><b class="mk a" data-s="3" style="--x:66.7%;left:66.7%">7</b></div></div>
<div class="two" style="margin-top:70px"><div class="card" data-s="2" style="padding:22px 26px"><small>They scored higher than you</small><h3 style="font-size:26px">A blind spot to open up</h3></div><div class="card" data-s="2" style="padding:22px 26px;transition-delay:3.4s"><small>You scored higher than them</small><h3 style="font-size:26px">They're underrating themselves. Tell them.</h3></div></div>
<p class="note" data-s="3" style="color:#fff;text-align:center">Never the average. You agree the score in the room.</p></section>

<section class="sc" id="sc-f"><p class="eb" data-s="1">Evidence</p><h2 data-s="1">One dated example for every score.</h2><div class="two">
<div class="card" data-s="1" style="transition-delay:.8s"><span class="date">4 NOV</span><p class="quote" style="margin:0">"Told the team the deadline had moved, the same morning I found out."</p><p style="color:#53baab;font-weight:800">Evidence, not opinion</p></div>
<div class="card" data-s="2"><small>The score is this month</small><h3>Not a label on the person</h3><svg class="sp" viewBox="0 0 400 110" width="100%" style="margin-top:16px"><line x1="0" x2="400" y1="38" y2="38" stroke="rgba(255,255,255,.3)" stroke-dasharray="4 6"/><path d="M10 34 L90 30 L170 78 L250 70 L330 36 L390 26" fill="none" stroke="#c32e81" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg><p>A hard month drops it. A good month brings it back.</p></div></div></section>

<section class="sc" id="sc-g"><p class="eb" data-s="1">The standard</p><h2 data-s="1" style="margin-bottom:130px">Seven is the standard. Nothing marks it while they score.</h2>
<div style="padding:0 40px;position:relative" data-s="1"><div class="trk"><div class="ticks">{ticks}</div>
<div class="dots" data-s="1" data-h="2" style="transition-delay:1.2s">{dots}</div>
<i class="std" data-s="1" data-h="2" style="transition-delay:.6s"><b>Pass mark</b></i>
<b class="mk h" data-s="2" data-h="3" style="--x:44.4%">5</b>
<b class="mk h" data-s="3" style="--x:55.6%">6</b><b class="mk j" data-s="3" style="--x:77.8%">8</b><i class="std" data-s="3" style="transition-delay:1s"><b>The standard</b></i></div></div>
<p class="note" data-s="1" data-h="2" style="margin-top:70px;text-align:center;transition-delay:1.8s">Show a pass mark and everyone lands just above it.</p>
<p class="note" data-s="2" data-h="3" style="margin-top:-30px;text-align:center;color:#fff">They read the behaviour and pick what's true.</p>
<p class="note" data-s="3" style="margin-top:-30px;text-align:center;color:#53baab">The line appears only once both scores are in.</p></section>

<section class="sc" id="sc-h"><p class="eb" data-s="1">Two more rules</p><div class="two" style="margin-top:8px">
<div class="card" data-s="1"><small>One case, one pillar</small><h3>One bad day counts once</h3><div class="pc"><span class="y">Resilience</span><span>Communication</span><span>Enthusiasm</span></div><p>So the heads keep trusting the numbers.</p></div>
<div class="card" data-s="2"><small>Every session ends with</small><div style="display:flex;gap:34px;align-items:baseline"><span class="big">1</span><h3>focus</h3><span class="big">1</span><h3>assignment</h3></div><p>Done in the job, before next month. Behaviour changes by doing.</p></div></div></section>

<section class="sc" id="sc-i"><p class="eb" data-s="1">How it grows</p><h2 data-s="1">One standard, used three ways.</h2><div class="three">
<div class="card" data-s="1" style="transition-delay:1s"><small>Hiring</small><h3 style="font-size:28px">The same six pillars as interview questions</h3></div>
<div class="card" data-s="2"><small>Their teams</small><h3 style="font-size:28px">Heads run it with their own people</h3></div>
<div class="card" data-s="3"><small>Scott</small><h3 style="font-size:28px">The whole leadership team on one screen</h3></div></div></section>

<section class="sc center" id="sc-z"><p class="eb" data-s="1">That's the why</p><h1 data-s="1" style="font-size:58px">20 minutes a month, per head.</h1><div class="next" data-s="2">Next: how to use it</div></section>

<script>
const ORDER=['t','a','b','c','d','e','f','g','h','i','z'];
window.go=(sc,step)=>{{document.querySelectorAll('.sc').forEach(e=>e.classList.toggle('on',e.id==='sc-'+sc));
 const el=document.getElementById('sc-'+sc);void el.offsetWidth;
 requestAnimationFrame(()=>requestAnimationFrame(()=>{{el.querySelectorAll('[data-s]').forEach(n=>n.classList.toggle('v',+n.dataset.s<=step));
 el.querySelectorAll('[data-h]').forEach(n=>n.classList.toggle('gone',step>=+n.dataset.h));
 if(sc==='b')document.getElementById('bcard').classList.toggle('hot',step>=3);
 if(sc==='c')el.querySelector('.r4').classList.toggle('hi',step>=3);}}));
 document.getElementById('pg').style.width=(ORDER.indexOf(sc)+1)/ORDER.length*100+'%'}};
</script></body></html>'''
open('why.html','w').write(html); print(len(html)//1024,'KB')
