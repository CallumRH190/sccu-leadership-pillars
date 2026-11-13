import asyncio, time, os, subprocess, json, numpy as np, soundfile as sf
from playwright.async_api import async_playwright
OUT='frames_w'; os.makedirs(OUT,exist_ok=True)
V=json.load(open('/home/claude/vo3/lines.json')); L=[(x[0],x[1],'') for x in V['lines']]; D=V['dur']; SR=V['sr']
A=list(np.load('/home/claude/vo3/clips.npy',allow_pickle=True))
frames=[]; marks=[]; cuts=[0]; n=0
total=lambda: sum(d for _,d in frames)
async def main():
    global n
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        ctx=await b.new_context(viewport={'width':1280,'height':720},device_scale_factor=1.5); pg=await ctx.new_page()
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file:///home/claude/why/why_voice.html'); await pg.wait_for_timeout(700)
        async def snap(d):
            global n; n+=1; path=f'{OUT}/f{n:05d}.jpg'; await pg.screenshot(path=path,type='jpeg',quality=92); frames.append([path,d])
        async def live(sec):
            t0=time.time(); last=t0; i0=len(frames)
            while True:
                await snap(0); now=time.time()
                if len(frames)-i0>1: frames[-2][1]=now-last
                last=now
                if now-t0>=sec: frames[-1][1]=0.07; break
        prev=None
        for i,(sc,st,t) in enumerate(L):
            if sc!=prev: cuts.append(len(frames)); prev=sc
            marks.append(total()); await pg.evaluate('([a,b])=>go(a,b)',[sc,st])
            await live(min(D[i]+0.2, 9.5 if (sc,st) in (('a',1),('c',1),('c',2),('d',3),('e',2),('f',2),('g',1)) else 3.0))
            need=D[i]+0.12+(1.2 if i==len(L)-1 else 0.22); el=total()-marks[i]
            if el<need: await snap(need-el)
        print('errors',errs); await b.close()
    cuts.append(len(frames)); files=[]
    for i in range(1,len(cuts)-1):
        fr=frames[cuts[i]:cuts[i+1]]
        if not fr: continue
        with open(f'w{i}.txt','w') as f:
            for path,d in fr: f.write(f"file '{os.path.abspath(path)}'\nduration {max(d,0.02):.4f}\n")
            f.write(f"file '{os.path.abspath(fr[-1][0])}'\n")
        r=subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',f'w{i}.txt','-vf','fps=30,scale=1920:1080,format=yuv420p','-c:v','libx264','-crf','18','-preset','veryfast','-pix_fmt','yuv420p',f'w{i}.tmp.mp4']); assert r.returncode==0
        os.rename(f'w{i}.tmp.mp4',f'w{i}.mp4'); files.append(os.path.abspath(f'w{i}.mp4'))
    open('allw.txt','w').write(''.join(f"file '{x}'\n" for x in files))
    subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i','allw.txt','-c','copy','joinedw.mp4'],check=True)
    T=total(); rt,_=sf.read('/home/claude/vo/roomtone.wav',dtype='float32'); n=int((T+0.5)*SR)
    xf=int(0.05*SR); body=rt.copy(); body[:xf]*=np.linspace(0,1,xf); body[-xf:]*=np.linspace(1,0,xf)
    track=np.zeros(n+len(body),dtype=np.float32); p=0
    while p<n: track[p:p+len(body)]+=body; p+=len(body)-xf
    track=track[:n]
    for m,s_ in zip(marks,A):
        o=int((m+0.12)*SR); s_=np.asarray(s_,dtype=np.float32); track[o:o+len(s_)]+=s_[:len(track)-o]
    sf.write('voice_w.wav',track,SR)
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i','joinedw.mp4','-i','voice_w.wav','-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','160k','-af','highpass=f=70,loudnorm=I=-16:TP=-1.5:LRA=11','-shortest','-movflags','+faststart','outw.tmp.mp4'],check=True)
    os.rename('outw.tmp.mp4','SCCU-Leadership-Pillars-Why-It-Works-Callum-v3.mp4'); json.dump(marks,open('marks_w.json','w')); print('total',round(T,1))
asyncio.run(main())
