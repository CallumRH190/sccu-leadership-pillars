import re
s=open('src.html').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:60],s.count(a))
    s=s.replace(a,b)
# 1 live date, held inside November so the sample history still makes sense
rep("const NOW='2026-11',TODAY='2026-11-11',STD=7;",
"const NOW='2026-11',TODAY=(()=>{const d=new Date(),s=d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');return s<'2026-11-11'?'2026-11-11':s>'2026-11-30'?'2026-11-30':s})(),STD=7;")
# 2 reset keeps James's own examples
rep("reset(){S=seed();","reset(){const jx=S.jx||{};S=seed();S.jx=jx;")
rep("Saves as you type. Heads see this on the pillar page.","Saves as you type, and stays when you reset the demo. Heads see this on the pillar page.")
# 3 what the scores are for
rep("<li><b>James can't see yours until his are in.</b>And you can't see his until you've submitted.</li></ul>",
"<li><b>James can't see yours until his are in.</b>And you can't see his until you've submitted.</li><li><b>This is for your development.</b>Scores are not linked to pay or commission. You see your own. James and Scott see every head's.</li></ul>")
rep(" <h3>One focus, one assignment</h3>",
" <h3>What the scores are for</h3><p>Development. They are not linked to pay or commission. You see your own scores. James and Scott see every head's.</p>\n <h3>One focus, one assignment</h3>")
rep("Agreed scores only. Each head's latest session, against the standard of 7 on every pillar.</p>",
"Agreed scores only. Each head's latest session, against the standard of 7 on every pillar. Scores are for development and are not linked to pay or commission.</p>")
# 4 summary uses names, never "You"
rep("<th>Pillar</th><th>You</th><th>James</th>","<th>Pillar</th><th>${first(h)}</th><th>James</th>")
rep('<i class="h">You, ${fDate(c.self[p.id].d)}.</i>','<i class="h">${first(h)}, ${fDate(c.self[p.id].d)}.</i>')
# 5 equal scores sit side by side
rep("${marks.map(k=>`<b class=\"mk ${k.c}\" style=\"left:${pct(k.v)}%\">${k.l}</b>`).join('')}</div>`}",
"${marks.map(k=>{const tw=k.c!=='a'&&marks.some(o=>o!==k&&o.c!=='a'&&o.v===k.v);return `<b class=\"mk ${k.c}\" style=\"left:${pct(k.v)}%${tw?';transform:translateX('+(k.c==='h'?-10:10)+'px)':''}\">${k.l}</b>`}).join('')}</div>`}")
rep(".xc-h{display:grid;grid-template-columns:170px 1fr auto;",".xc-h{display:grid;grid-template-columns:170px 1fr 236px;")
rep("<span style=\"display:flex;gap:8px;align-items:center\">${j.over?","<span style=\"display:flex;gap:8px;align-items:center;justify-content:flex-end;flex-wrap:wrap\">${j.over?")
# 6 summary radar: side labels anchored outwards so nothing clips
rep("const[x,y]=pt(i,o.tight?(side?15.2:12):12.4);const an=o.tight||Math.abs(x-c)<8?'middle':x>c?'start':'end';",
"const[x,y]=pt(i,o.tight?(side?11.6:12):12.4);const an=Math.abs(x-c)<8?'middle':x>c?'start':'end';")
rep("viewBox=\"${o.tight?-S_*0.1:-S_*0.14} ${o.tight?S_*0.06:0} ${o.tight?S_*1.2:S_*1.28} ${o.tight?S_*0.88:S_}\"",
"viewBox=\"${o.tight?-S_*0.26:-S_*0.14} ${o.tight?S_*0.04:0} ${o.tight?S_*1.52:S_*1.28} ${o.tight?S_*0.92:S_}\"")
open('src.html','w').write(s); print('ok')
