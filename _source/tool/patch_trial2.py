"""Fixes from the independent tester's report on the trial version, 13 November 2026."""
s = open('src.html').read()

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (a[:80], c)
    s = s.replace(a, b)

# 1. two open tabs: the stale tab picks up what the other tab saved
rep("function save(){try{localStorage.setItem(KEY,JSON.stringify(S))}catch(e){}}",
    "function save(){try{localStorage.setItem(KEY,JSON.stringify(S))}catch(e){}}\n"
    "function resync(){try{const r=localStorage.getItem(KEY);if(r&&r!==JSON.stringify(S)){const o=JSON.parse(r);if(o&&o.v===S.v){S=o;render()}}}catch(e){}}\n"
    "window.addEventListener('storage',e=>{if(e.key===KEY)resync()});window.addEventListener('focus',resync);document.addEventListener('visibilitychange',()=>{if(!document.hidden)resync()});")

# 2 + 4 + 5. the head's scores stay sealed until the reveal; unmatched names ask; older links are refused
i = s.index("function applyCode(o){"); j = s.index("function setupHTML(){")
s = s[:i] + r'''function applyCode(o,toId){
 const hs=Object.values(S.heads);if(!hs.length){S.pending=o;ui.codeErr=false;return 'Add the head first. Their scores load as soon as you do.'}
 const nm=(o.n||'').toLowerCase().split(' ')[0];
 const h=toId?S.heads[toId]:(hs.length===1?hs[0]:hs.find(x=>nm&&first(x).toLowerCase()===nm));
 if(!h){S.pending=o;ui.codeErr=false;return ''}
 const c=h.cur;S.pending=null;
 if(c.revealed){ui.codeErr=true;return `${first(h)}'s session has already been revealed, so new scores can't be loaded.`}
 if(c.sealedT&&o.t&&o.t<c.sealedT){ui.codeErr=true;return `That is an older set of scores from ${o.n||first(h)}. The newer set is already loaded.`}
 c.sealed='LP1.'+b64e(JSON.stringify(o));c.sealedT=o.t||0;c.self={};c.selfAt=o.at||TODAY;S.headId=h.id;ui.codeErr=false;
 return `${o.n?o.n+"'s":'The'} scores are loaded into ${h.name}'s session. They stay hidden until you reveal both sets.`}
function unseal(c){if(!c.sealed)return;const o=readCode(c.sealed);if(o)P.forEach((p,i)=>c.self[p.id]={s:+o.s[i][0],ex:o.s[i][1],d:o.s[i][2],over:false});c.sealed=null}
function pendingHTML(){if(!S.pending||!Object.keys(S.heads).length)return '';
 return `<div class="card prn-hide" style="margin:0 0 22px;border-color:var(--sea)"><p class="eyebrow">Scores have arrived from ${esc(S.pending.n||'a head')}</p><p style="margin:8px 0 12px;color:var(--ink-2)">Whose session are they for?</p><div style="display:flex;gap:10px;flex-wrap:wrap;align-items:center">${Object.values(S.heads).filter(h=>!h.cur.revealed).map(h=>`<button class="btn ghost sm" data-a="assign" data-id="${h.id}">${esc(h.name)}</button>`).join('')}<button class="link" data-a="drop-pending">Ignore them</button></div></div>`}
function noteHTML(){if(!TRIAL||HEADMODE)return '';
 return pendingHTML()+(ui.codeMsg?`<div class="hidden-note prn-hide" style="margin-bottom:22px${ui.codeErr?';border-color:var(--warn)':''}"><span class="lockic">${ui.codeErr?'!':'🔒'}</span><span>${esc(ui.codeMsg)}</span><button class="link" data-a="dismiss" style="margin-left:auto;white-space:nowrap">Dismiss</button></div>`:'')}
''' + s[j:]
rep("function makeCode(h){return 'LP1.'+b64e(JSON.stringify({v:1,n:h.name.trim(),m:NOW,at:h.cur.selfAt,s:",
    "function makeCode(h){return 'LP1.'+b64e(JSON.stringify({v:1,n:h.name.trim(),m:NOW,at:h.cur.selfAt,t:h.cur.subT||0,s:")
rep("'ss-submit'(){const h=me();if(allFull(h.cur.self)){h.cur.selfAt=TODAY;", "'ss-submit'(){const h=me();if(allFull(h.cur.self)){h.cur.selfAt=TODAY;h.cur.subT=Date.now();")
rep("reveal(){const h=S.heads[S.headId],c=h.cur;c.revealed=true;", "reveal(){const h=S.heads[S.headId],c=h.cur;unseal(c);c.revealed=true;")

# 9. messages are visible on every screen, including errors
rep("<main>${views[r]()}</main>", "<main>${noteHTML()}${views[r]()}</main>")
rep("${head}${TRIAL&&ui.codeMsg&&!ui.codeErr?`<div class=\"hidden-note\" style=\"margin-bottom:22px\"><span class=\"lockic\">🔒</span><span>${esc(ui.codeMsg)}</span></div>`:''}${body}", "${head}${body}")
rep("<span class=\"hint ${ui.codeErr?'bad':''}\">${ui.codeErr?esc(ui.codeMsg||''):''}</span></div></div>`}", "</div></div>`}")
rep("window.addEventListener('hashchange',()=>{ui.menu=false;takeIncoming();render()});",
    "window.addEventListener('hashchange',()=>{ui.menu=false;if(!takeIncoming()){if(ui.noteKeep)ui.noteKeep=0;else{ui.codeMsg='';ui.codeErr=false}}render()});")
rep("if(S.pending)ui.codeMsg=applyCode(S.pending);location.hash='session'},", "if(S.pending){ui.codeMsg=applyCode(S.pending);ui.noteKeep=1}location.hash='session'},")
rep("'new-head'(){ui.adding=true;ui.menu=false;location.hash='team'}, 'cancel-add'(){ui.adding=false},",
    "'new-head'(){ui.adding=true;ui.menu=false;location.hash='team'}, 'cancel-add'(){ui.adding=false},\n"
    " assign(d){ui.codeMsg=applyCode(S.pending,d.id)}, 'drop-pending'(){S.pending=null;ui.codeMsg='';ui.codeErr=false}, dismiss(){ui.codeMsg='';ui.codeErr=false},\n"
    " 'j-unlock'(){const c=S.heads[S.headId].cur;if(!c.revealed){c.jamesAt=null;window.scrollTo(0,0)}},")
rep("r.onload=()=>{try{const o=JSON.parse(r.result);if(o&&o.v===1&&o.heads&&!o.heads.me){S=o;S.role='james';save();ui.menu=false;ui.codeMsg='';location.hash='team';render()}}catch(_){}e.target.value=''};",
    "r.onload=()=>{let ok=false;try{const o=JSON.parse(r.result);if(o&&o.v===1&&o.heads&&!o.heads.me){S=o;S.role='james';save();ok=true}}catch(_){}\n"
    "  ui.menu=false;ui.codeErr=!ok;ui.codeMsg=ok?'Backup restored.':\"That file isn't a Leadership Pillars backup. Nothing was changed.\";if(location.hash!=='#team'){ui.noteKeep=1;location.hash='team'}render();e.target.value=''};")

# 6. James can change his scores before the reveal
rep("Nothing is visible to either of you until then.`}</p>${TRIAL?'':", "Nothing is visible to either of you until then.`}</p><button class=\"link\" data-a=\"j-unlock\">I need to change my scores</button>${TRIAL?'':")
rep("Turn the screen so you can both see it.</p><button class=\"btn\" data-a=\"reveal\">Reveal both sets</button></div>",
    "Turn the screen so you can both see it.</p><button class=\"btn\" data-a=\"reveal\">Reveal both sets</button><p style=\"margin-top:14px\"><button class=\"link\" data-a=\"j-unlock\">I need to change my scores first</button></p></div>")

# 7 + 13. the head's send card says the right thing after a change
rep("unlock(){const h=me();h.cur.selfAt=null;h.cur.step=6;", "unlock(){const h=me();h.cur.selfAt=null;h.cur.changed=true;h.cur.step=6;")
rep("<p class=\"hint\" style=\"margin-top:8px\">Nothing has left this device yet. James only gets your scores when you send him this.</p>",
    "<p class=\"hint\" style=\"margin-top:8px\">${h.cur.changed?'You changed your answers, so send James this new link. It replaces the one you sent before.':'Nothing has left this device yet. James only gets your scores when you send him this.'} The link is long. That is normal.</p>")

# 10. say why an example is refused
rep("`${n} of 6 complete. Each needs a score, an example and a date.`", "`${n} of 6 complete. Each needs a score, a date and an example of a few words.`")

# 12. no claim about James's and Scott's own scores in the trial
rep("Heads never see this page. James's and Scott's own scores are kept separately and are not shown here.</p>",
    "Heads never see this page.${TRIAL?'':\" James's and Scott's own scores are kept separately and are not shown here.\"}</p>")

# 8. long strings wrap
rep(".rrow p{color:var(--ink-2);font-size:15px;margin-top:10px}",
    ".rrow p{color:var(--ink-2);font-size:15px;margin-top:10px}\n.rrow>div,.ev,.sh-ev div,.two>div,.evi>div{min-width:0}.rrow p,.ev p,.sh-ev div,.xc-b p,.open-line,textarea{overflow-wrap:anywhere}")

# 3. the summary prints on one page, without the head picker or notices
rep("  .top,.sum-act{display:none!important} body,main{background:var(--navy);padding:0;margin:0;max-width:none}\n  .sheet{border:0;box-shadow:none;margin:0}",
    "  @page{size:A4;margin:0}\n  .top,.sum-act,.hpick,.prn-hide{display:none!important} body,main{background:var(--navy);padding:0;margin:0;max-width:none}\n  .sheetwrap{overflow:visible}.sheet{border:0;box-shadow:none;margin:0 auto;min-height:0;zoom:var(--pz,1)}")
rep(" print(){try{window.print()}catch(e){}}", " print(){fitPrint();try{window.print()}catch(e){}}")
rep("function takeIncoming(){", "function fitPrint(){const sh=document.querySelector('.sheet');if(sh)document.documentElement.style.setProperty('--pz',String(Math.min(1,1118/sh.offsetHeight)))}\nwindow.addEventListener('beforeprint',fitPrint);\nfunction takeIncoming(){")
open('src.html', 'w').write(s)
print('patched')
