
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
 s.innerHTML='<span style="padding-left:12px">'+t+'</span><i>'+[1,2,3,4,5,6].map(i=>'<u class="'+(i<=n?'on':'')+'"></u>').join('')+'</i>'};
window.cardSet=(html)=>{const c=document.getElementById('card');c.style.display=html?'grid':'none';c.innerHTML=html||''};
})()