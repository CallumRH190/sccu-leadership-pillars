"""Adds the trial build to src.html. The demo build is unchanged when TRIAL is false."""
import re
s = open('src.html').read()

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (a[:70], c)
    s = s.replace(a, b)

def resub(pat, b, n=1):
    global s
    s, c = re.subn(pat, lambda m: b(m) if callable(b) else b, s, flags=re.S)
    assert c == n, (pat[:70], c)

# --- flags, page shell
rep('"use strict";', '"use strict";\n/*FLAGS*/\nconst HEADMODE=TRIAL&&/[?&]who=head\\b/.test(location.search);')
rep('<div id="app"></div>', '<div id="app"></div>\n<input type="file" id="rf" accept=".json,application/json" hidden>')

# --- dates
i = s.index("const NOW='2026-11',TODAY="); j = s.index("STD=7;", i) + len("STD=7;")
old = s[i:j]
demo_today = old[len("const NOW='2026-11',TODAY="):old.rindex(",STD=7;")]
s = s[:i] + ("const _iso=d=>d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');\n"
             "const NOW=TRIAL?_iso(new Date()).slice(0,7):'2026-11',TODAY=TRIAL?_iso(new Date()):" + demo_today + ",STD=7;\n"
             "const YEAR=NOW.slice(0,4),MIND=TRIAL?_iso(new Date(Date.now()-45*864e5)):'2026-10-12',QL={Q1:'Mar to May',Q2:'Jun to Aug',Q3:'Sep to Nov',Q4:'Dec to Feb'};") + s[j:]
rep('min="2026-10-12"', 'min="${MIND}"', 2)
rep('${mName(NOW)} 2026 · ${quarter(NOW)} (Sep to Nov)', '${mName(NOW)} ${YEAR} · ${quarter(NOW)} (${QL[quarter(NOW)]})')
n_now = s.count('${mName(NOW)} 2026')
s = s.replace('${mName(NOW)} 2026', '${mName(NOW)} ${YEAR}')
rep('${mName(l.m)} 2026', '${mName(l.m)} ${l.m.slice(0,4)}')
print('year labels replaced', n_now)

# --- head factory and seed
i = s.index(' const H=(id,name,dept,hist,cur)=>'); j = s.index('\n', i)
s = s[:i] + ' const H=mkHead;' + s[j:]
rep("function seed(){",
    "function mkHead(id,name,dept,hist,cur){return {id,name,dept,ini:name.split(' ').map(w=>w[0]||'').join('').slice(0,2).toUpperCase(),hist:hist||[],cur:Object.assign({self:{},selfAt:null,james:{},jamesAt:null,revealed:false,agreed:{},focus:null,asg:null,asgOwn:'',due:'',review:null,done:false,sessionDate:null,startedAt:null,endedAt:null,step:-1},cur||{})}}\nfunction seed(){")
rep(" const map=o=>Object.fromEntries(P.map((p,i)=>[p.id,o[i]]));",
    " const map=o=>Object.fromEntries(P.map((p,i)=>[p.id,o[i]]));\n if(TRIAL)return HEADMODE?{v:1,role:'me',headId:'me',jx:{},seenHow:{},heads:{me:mkHead('me','','',[],{})}}:{v:1,role:'james',headId:null,jx:{},seenHow:{},pending:null,heads:{}};")
rep("const KEY='sccu-pillars-demo-v3';", "const KEY=TRIAL?(HEADMODE?'sccu-pillars-trial-head-v1':'sccu-pillars-trial-v1'):'sccu-pillars-demo-v3';")
rep("if(r&&r.v===3)return r", "if(r&&r.v===(TRIAL?1:3)&&(!TRIAL||HEADMODE===!!(r.heads&&r.heads.me)))return r")

# --- trial helpers, placed before the shell
TRIAL_JS = r'''
/* ---------- trial: one real session, no logins ---------- */
const curH=()=>S.heads[S.headId]||Object.values(S.heads)[0]||null;
const pageBase=()=>location.href.split(/[?#]/)[0];
const b64e=s=>btoa(unescape(encodeURIComponent(s))).replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'');
const b64d=s=>{s=s.replace(/-/g,'+').replace(/_/g,'/');while(s.length%4)s+='=';return decodeURIComponent(escape(atob(s)))};
function copyText(v){try{if(navigator.clipboard&&window.isSecureContext){navigator.clipboard.writeText(v).catch(()=>{});return}}catch(e){}const t=document.createElement('textarea');t.value=v;t.style.position='fixed';t.style.opacity='0';document.body.appendChild(t);t.select();try{document.execCommand('copy')}catch(e){}t.remove()}
function makeCode(h){return 'LP1.'+b64e(JSON.stringify({v:1,n:h.name.trim(),m:NOW,at:h.cur.selfAt,s:P.map(p=>{const e=h.cur.self[p.id];return [e.s,e.ex,e.d]})}))}
function readCode(raw){try{let t=String(raw||'').trim();const i=t.indexOf('LP1.');if(i<0)return null;t=t.slice(i+4).replace(/\s+/g,'');const o=JSON.parse(b64d(t));
 if(o.v!==1||!Array.isArray(o.s)||o.s.length!==6)return null;
 for(const r of o.s){if(!(r[0]>=1&&r[0]<=10)||typeof r[1]!=='string'||!/^\d{4}-\d\d-\d\d$/.test(r[2]))return null}
 return o}catch(e){return null}}
function applyCode(o){
 const hs=Object.values(S.heads);if(!hs.length){S.pending=o;return 'Add the head first. Their scores load as soon as you do.'}
 const nm=(o.n||'').toLowerCase().split(' ')[0];const h=hs.find(x=>nm&&first(x).toLowerCase()===nm)||curH();
 if(h.cur.revealed){ui.codeErr=true;return `${first(h)}'s session has already been revealed, so new scores can't be loaded.`}
 P.forEach((p,i)=>h.cur.self[p.id]={s:+o.s[i][0],ex:o.s[i][1],d:o.s[i][2],over:false});h.cur.selfAt=o.at||TODAY;h.cur.step=6;S.headId=h.id;S.pending=null;ui.codeErr=false;
 return `${o.n?o.n+"'s":'The'} scores are loaded into ${h.name}'s session. They stay hidden until you reveal both sets.`}
function setupHTML(){const any=Object.keys(S.heads).length>0;ui.nh=ui.nh||{n:'',d:''};
 return `<div class="intro"><p class="eyebrow">Trial version${any?' · add a head':''}</p><h1>${any?'Who is the next session with?':'Who is this session with?'}</h1>
 <p class="muted" style="font-size:18px">${any?'':'This is the trial version. It runs real sessions without logins, and everything you enter stays in this browser on this device. '}Their name is never sent anywhere.</p>
 <div class="evi" style="margin-top:26px"><div><label class="fl" for="nh-n">Their name</label><input type="text" id="nh-n" data-nh="n" value="${esc(ui.nh.n)}" placeholder="First and last name" autocomplete="off"></div><div><label class="fl" for="nh-d">Department</label><input type="text" id="nh-d" data-nh="d" value="${esc(ui.nh.d)}" placeholder="For example, Futures" autocomplete="off"></div></div>
 <div class="snav" style="justify-content:flex-start"><button class="btn" data-a="add-head" data-gate="newhead">Add and open the session</button>${any?'<button class="btn ghost" data-a="cancel-add">Cancel</button>':''}<span class="hint" data-hint="newhead"></span></div>
 ${S.pending?`<div class="hidden-note" style="margin-top:22px"><span class="lockic">🔒</span><span>Scores from ${esc(S.pending.n||'a head')} have arrived. They load as soon as you add them here.</span></div>`:''}</div>`}
function inviteHTML(h){const c=h.cur,link=pageBase()+'?who=head',f=first(h);
 return `<div class="card" style="margin:0 0 22px"><p class="eyebrow">${c.selfAt?`${f}'s scores are loaded`:`First, ${f}'s self-score`}</p>
 ${c.selfAt?`<p style="margin:8px 0 0;color:var(--ink-2)">Loaded and hidden. If ${f} sends a newer link, open it on this device or paste the code below.</p>`
 :`<p style="margin:8px 0 14px;color:var(--ink-2)">Send ${f} this private link. They score on their own phone or laptop, then send a link back to you. Open that link on this device and their scores load here, hidden until the reveal.</p>
 <div style="display:flex;gap:10px;flex-wrap:wrap;align-items:center"><input type="text" readonly id="inv" value="${esc(link)}" aria-label="Private scoring link" style="flex:1;min-width:240px"><button class="btn sm" data-a="copy" data-id="inv">${ui.copied==='inv'?'Copied':'Copy the link'}</button></div>`}
 <label class="fl" for="code" style="margin-top:16px;display:block">${c.selfAt?'Paste a newer code':`Or paste the code ${f} sent you`}</label>
 <textarea id="code" data-code placeholder="Starts with LP1." style="min-height:56px">${esc(ui.code||'')}</textarea>
 <div class="snav" style="justify-content:flex-start;margin-top:10px"><button class="btn ghost sm" data-a="load-code">Load the scores</button><span class="hint ${ui.codeErr?'bad':''}">${ui.codeErr?esc(ui.codeMsg||''):''}</span></div></div>`}
function sendHTML(h){const code=makeCode(h),link=pageBase()+'#code='+code;
 return `<div class="card" style="margin:22px 0"><p class="eyebrow">Last step · send it to James</p><p style="margin:8px 0 14px;color:var(--ink-2)">Send James the link below. Your numbers stay hidden on his screen until he has locked his own and you reveal both sets together.</p>
 <div class="snav" style="justify-content:flex-start;margin-top:0"><button class="btn" data-a="share">${ui.copied==='share'?'Copied. Now paste it to James':'Send to James'}</button><button class="btn ghost" data-a="copy" data-id="sendcode">${ui.copied==='sendcode'?'Copied':'Copy the code only'}</button></div>
 <textarea id="sendlink" readonly style="min-height:70px;margin-top:14px;font-size:12px;word-break:break-all" aria-label="Your link for James">${esc(link)}</textarea><textarea id="sendcode" readonly hidden>${esc(code)}</textarea>
 <p class="hint" style="margin-top:8px">Nothing has left this device yet. James only gets your scores when you send him this.</p>
 <button class="link" data-a="unlock" style="margin-top:12px">I need to change something first</button></div>`}
function headIntro(h){return `<div class="intro"><p class="eyebrow">${mName(NOW)} ${YEAR} · Self-score</p><h1>Welcome. This is your first one.</h1>
 <p class="muted" style="font-size:18px">Once a month you score yourself on six pillars, James scores you, and the two of you compare. It takes about ten minutes.</p>
 <ul><li><b>Your score is this month.</b>A hard month can drop a number and a good month brings it back. Nobody is a 5.</li><li><b>One example for every score.</b>One real thing that happened, with a date. No example, no score.</li><li><b>James can't see yours until you sit down together.</b>When you finish, you send him a link. Your numbers stay hidden on his screen until his own are locked.</li><li><b>Nothing leaves this device until you send it.</b>Your answers save in this browser as you go, so you can stop and come back.</li></ul>
 <div style="max-width:340px;margin-bottom:26px"><label class="fl" for="hn">Your first name</label><input type="text" id="hn" data-hn value="${esc(h.name)}" autocomplete="given-name"></div>
 <div class="snav" style="justify-content:flex-start;margin-top:0"><button class="btn" data-a="ss-go" data-id="0" data-gate="hname">Start scoring</button><button class="btn ghost" data-a="modal" data-id="how">How it works</button><span class="hint" data-hint="hname"></span></div></div>`}

'''
rep("/* ---------- shell ---------- */", TRIAL_JS + "/* ---------- shell ---------- */")

# --- shell
rep("function routes(){return S.role==='james'", "function routes(){if(HEADMODE)return [['self-score','My scores'],['model','The Model']];return S.role==='james'")
i = s.index('function whoHTML(){'); j = s.index('function render(){')
old_who = s[i:j]
k = old_who.index('${ui.menu?`<div class="menu">'); demo_menu = old_who[k + len('${ui.menu?`'):old_who.rindex("`:''}`;")]
new_who = r'''function whoHTML(){
 const r=S.role, n=r==='james'?'James Pease':r==='scott'?'Scott Riddell':(me().name.trim()||'Your scoring page'), t=r==='james'?'COO':r==='scott'?'CEO':'Head of '+me().dept, a=r==='james'?'j':r==='scott'?'s':'h';
 const ini=HEADMODE?((me().name.trim()[0]||'·').toUpperCase()):n.split(' ').map(w=>w[0]).join('');
 const item=(id,name,sub,cls)=>`<button data-a="role" data-id="${id}" class="${S.role===id?'on':''}"><i class="av ${cls}" style="font-style:normal">${name.split(' ').map(w=>w[0]).join('')}</i><span>${name}<small>${sub}</small></span></button>`;
 const clr=ui.confirm==='clear';
 const menu=!ui.menu?'':HEADMODE?`<div class="menu"><button data-a="clear"><span>${clr?'Click again to clear everything':'Start again'}<small>Clears your answers on this device</small></span></button></div>`
  :TRIAL?`<div class="menu"><p class="eyebrow">View the tool as</p>${item('james','James Pease','COO. Runs the sessions','j')}${item('scott','Scott Riddell','CEO. Sees the team picture','s')}<hr><button data-a="new-head"><span>Add a head<small>Set up another session</small></span></button><button data-a="backup"><span>Download a backup file<small>Saves everything on this device to a file</small></span></button><button data-a="restore"><span>Restore from a backup<small>Loads a backup file you saved earlier</small></span></button><hr><button data-a="clear"><span>${clr?'Click again to clear everything':'Clear the trial'}<small>Removes every head and score from this device</small></span></button></div>`
  :`DEMO_MENU`;
 return `<button class="who" data-a="menu" aria-expanded="${ui.menu}"><i class="av ${a}" style="font-style:normal">${ini}</i><span>${esc(n)}<small>${HEADMODE?'Private to you':'Viewing as '+t}</small></span></button>${menu}`;
}
'''.replace('DEMO_MENU', demo_menu)
s = s[:i] + new_who + s[j:]
rep('<span class="pill">Sample data</span>', "<span class=\"pill\">${TRIAL?'Trial':'Sample data'}</span>")

# --- the model: James's own example
rep("Saves as you type, and stays when you reset the demo. Heads see this on the pillar page.",
    "${TRIAL?'Saves as you type on this device. In the full version, heads see it on this page.':'Saves as you type, and stays when you reset the demo. Heads see this on the pillar page.'}")

# --- self-score (head)
rep("function vSelf(){\n const h=me(),c=h.cur,last=h.hist[h.hist.length-1];",
    "function vSelf(){\n const h=me(),c=h.cur,last=h.hist[h.hist.length-1];\n if(HEADMODE&&c.step<0&&!c.selfAt)return headIntro(h);")
a = '''<div class="hidden-note" style="margin:22px 0"><span class="lockic">🔒</span><span>${c.jamesAt?"James's scores are in too. You'll both see them together in the session.":"James hasn't scored yet. His scores stay hidden from you, and yours from him, until you sit down together."}</span></div>'''
rep(a, '${HEADMODE?sendHTML(h):`' + a + '`}')

# --- session (James)
a = "const h=S.heads[S.headId]||S.heads.tom,c=h.cur,st=stageOf(h);"
rep(a, "if(TRIAL&&!curH())return setupHTML();\n const h=curH(),c=h.cur,st=stageOf(h);")
rep('body=`<div class="hidden-note"><span class="lockic">🔒</span><span>${c.selfAt?`${first(h)} submitted on',
    'body=`${TRIAL?inviteHTML(h):\'\'}<div class="hidden-note"><span class="lockic">🔒</span><span>${c.selfAt?`${first(h)} submitted on')
a = '''body=`<div class="blank"><h2>Your scores are locked.</h2><p>${first(h)} hasn't self-scored yet. The reveal opens as soon as ${first(h)} submits. Nothing is visible to either of you until then.</p><p class="hint">For the demo: switch to ${h.name} from the menu top right, complete the self-score, then come back.</p></div>`;'''
b = '''body=`${TRIAL?inviteHTML(h):''}<div class="blank"><h2>Your scores are locked.</h2><p>${TRIAL?`${first(h)}'s scores haven't arrived yet. The reveal opens as soon as they load. Nothing is visible to either of you until then.`:`${first(h)} hasn't self-scored yet. The reveal opens as soon as ${first(h)} submits. Nothing is visible to either of you until then.`}</p>${TRIAL?'':`<p class="hint">For the demo: switch to ${h.name} from the menu top right, complete the self-score, then come back.</p>`}</div>`;'''
rep(a, b)
rep("return pick+`<div class=\"sess\">${rail(h,st)}<div>${head}${body}</div></div>`;",
    "return pick+`<div class=\"sess\">${rail(h,st)}<div>${head}${TRIAL&&ui.codeMsg&&!ui.codeErr?`<div class=\"hidden-note\" style=\"margin-bottom:22px\"><span class=\"lockic\">🔒</span><span>${esc(ui.codeMsg)}</span></div>`:''}${body}</div></div>`;")

# --- team
rep("function vTeam(){\n", "function vTeam(){\n if(TRIAL&&(ui.adding||!Object.keys(S.heads).length))return setupHTML();\n")
rep("const avg=P.map((_,i)=>withData.reduce((s,r)=>s+r.l.ag[i],0)/withData.length);",
    "const has=withData.length>0,avg=P.map((_,i)=>has?withData.reduce((s,r)=>s+r.l.ag[i],0)/withData.length:0);")
rep("const wi=avg.indexOf(Math.min(...avg)),", "const wi=has?avg.indexOf(Math.min(...avg)):-1,")
rep("const lowOn=withData.filter(r=>r.l.ag[wi]<STD).length;", "const lowOn=has?withData.filter(r=>r.l.ag[wi]<STD).length:0;")
rep("<h1>The team this month</h1><p class=\"lead\">Agreed scores only. Each head's latest session, against the standard of 7 on every pillar.</p></div></div>",
    "<h1>The team this month</h1><p class=\"lead\">Agreed scores only. Each head's latest session, against the standard of 7 on every pillar.</p></div>${TRIAL&&S.role==='james'?'<button class=\"btn ghost\" data-a=\"new-head\">Add a head</button>':''}</div>")
rep("<small class=\"eyebrow\">Team's weakest pillar</small><b>${P[wi].name}</b><p>Team average ${avg[wi].toFixed(1)}. ${lowOn} of ${withData.length} heads are below standard on it.</p>",
    "<small class=\"eyebrow\">Team's weakest pillar</small>${has?`<b>${P[wi].name}</b><p>Team average ${avg[wi].toFixed(1)}. ${lowOn} of ${withData.length} heads are below standard on it.</p>`:'<b>No scores yet</b><p>The picture builds after the first session.</p>'}")
i = s.index("<tfoot><tr><td>Team average</td>"); j = s.index("</tfoot>", i) + len("</tfoot>")
s = s[:i] + "${has?`" + s[i:j] + "`:''}" + s[j:]

# --- profile
a = "const own=isHead(),h=own?me():(S.heads[S.headId]||S.heads.tom),"
rep(a, "if(TRIAL&&!isHead()&&!curH())return setupHTML();\n const own=isHead(),h=own?me():curH(),")
rep('<span class="chip ok">Integrity: pass</span>', "${TRIAL?'':'<span class=\"chip ok\">Integrity: pass</span>'}")
i = s.index('<div class="card" style="grid-column:span 2"><p class="eyebrow">Results · from the scorecard</p>')
j = s.index("never blended into them.</p></div>", i) + len("never blended into them.</p></div>")
kpi = s[i:j]
s = s[:i] + "${TRIAL?`<div class=\"card\" style=\"grid-column:span 2\"><p class=\"eyebrow\">Results · from the scorecard</p><p class=\"empty\" style=\"margin-top:10px\">In the full version, ${first(h)}'s scorecard results sit here. Results sit beside the pillars and are never blended into them.</p></div>`:`" + kpi + "`}" + s[j:]

# --- summary
a = "const own=isHead(),h=own?me():(S.heads[S.headId]||S.heads.priya),c=h.cur;"
rep(a, "if(TRIAL&&!isHead()&&!curH())return setupHTML();\n const own=isHead(),h=own?me():curH(),c=h.cur;")
rep('<span class="chip ok" style="margin-top:8px">Integrity: pass</span>', "${TRIAL?'':'<span class=\"chip ok\" style=\"margin-top:8px\">Integrity: pass</span>'}")
rep("One page. ${canPrint?'Save it as a PDF from the print dialog.':'PDF export is switched on in the live tool.'}</span>${canPrint?'<button class=\"btn sm\" data-a=\"print\">Save as PDF</button>':''}",
    "One page. ${canPrint?'Save it as a PDF from the print dialog'+(TRIAL?', then send '+first(h)+' a copy.':'.'):'PDF export is switched on in the live tool.'}</span><span style=\"display:flex;gap:10px\">${TRIAL?'<button class=\"btn ghost sm\" data-a=\"backup\">Download a backup</button>':''}${canPrint?'<button class=\"btn sm\" data-a=\"print\">Save as PDF</button>':''}</span>")

# --- gates and inputs
rep("  if(g==='finish')m=finishMissing(S.heads[S.headId]);",
    "  if(g==='finish')m=finishMissing(S.heads[S.headId]);\n  if(g==='newhead')m=((ui.nh&&ui.nh.n)||'').trim().length<2?'Type their name.':'';\n  if(g==='hname')m=(me().name||'').trim().length<2?'Type your first name to start.':'';")
rep(" else if(t.dataset.jx){S.jx[t.dataset.jx]=t.value;save()}",
    " else if(t.dataset.nh){ui.nh=ui.nh||{n:'',d:''};ui.nh[t.dataset.nh]=t.value;gates()}\n else if(t.dataset.hn!==undefined){const h=me();h.name=t.value;h.ini=(t.value.trim()[0]||'').toUpperCase();gates();save()}\n else if(t.dataset.code!==undefined){ui.code=t.value}\n else if(t.dataset.jx){S.jx[t.dataset.jx]=t.value;save()}")

# --- actions
rep(" menu(){ui.menu=!ui.menu},", r''' menu(){ui.menu=!ui.menu;ui.confirm=null},
 copy(d){const el=document.getElementById(d.id);copyText(el?el.value:'');ui.copied=d.id},
 share(){const link=pageBase()+'#code='+makeCode(me()),text='My Leadership Pillars scores for our session. Open this on the device you will run the session on: '+link;
  if(navigator.share){navigator.share({text}).catch(()=>{})}else copyText(link);ui.copied='share'},
 unlock(){const h=me();h.cur.selfAt=null;h.cur.step=6;ui.copied=null;window.scrollTo(0,0)},
 'load-code'(){const o=readCode(ui.code);if(!o){ui.codeErr=true;ui.codeMsg="That doesn't look like a scores code. It starts with LP1.";return}ui.codeMsg=applyCode(o);if(!ui.codeErr)ui.code=''},
 'add-head'(){const n=(ui.nh.n||'').trim(),dp=(ui.nh.d||'').trim();if(n.length<2)return false;const id='h'+Date.now().toString(36);S.heads[id]=mkHead(id,n,dp||'Head of department',[],{});S.headId=id;ui.nh={n:'',d:''};ui.adding=false;ui.open=null;if(S.pending)ui.codeMsg=applyCode(S.pending);location.hash='session'},
 'new-head'(){ui.adding=true;ui.menu=false;location.hash='team'}, 'cancel-add'(){ui.adding=false},
 backup(){const b=new Blob([JSON.stringify(S,null,1)],{type:'application/json'}),a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='leadership-pillars-trial-backup-'+TODAY+'.json';document.body.appendChild(a);a.click();a.remove();ui.menu=false},
 restore(){document.getElementById('rf').click();ui.menu=false},
 clear(){if(ui.confirm!=='clear'){ui.confirm='clear';return}S=seed();ui={menu:false,modal:null,open:null,mopen:null};location.hash=routes()[0][0]},''')

# --- restore listener and arriving links, just before the first render
rep("render();\n</script>", r'''document.addEventListener('change',e=>{if(e.target.id!=='rf')return;const f=e.target.files[0];if(!f)return;const r=new FileReader();
 r.onload=()=>{try{const o=JSON.parse(r.result);if(o&&o.v===1&&o.heads&&!o.heads.me){S=o;S.role='james';save();ui.menu=false;ui.codeMsg='';location.hash='team';render()}}catch(_){}e.target.value=''};r.readAsText(f)});
if(TRIAL&&!HEADMODE&&/^#code=/.test(location.hash)){const o=readCode(location.hash.slice(6));try{history.replaceState(null,'',pageBase()+'#session')}catch(e){location.hash='session'}
 if(o){ui.codeMsg=applyCode(o);save()}else{ui.codeErr=true;ui.codeMsg="That link didn't carry a readable scores code. Ask for it again, or paste the code."}}
render();
</script>''')
open('src.html', 'w').write(s)
print('patched')
