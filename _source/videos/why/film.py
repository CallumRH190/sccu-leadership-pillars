import asyncio, time, os, subprocess, json, numpy as np, soundfile as sf
from playwright.async_api import async_playwright
from kokoro_onnx import Kokoro
OUT='frames'; os.makedirs(OUT,exist_ok=True)
L=[
('t',1,"Before you learn how to use it, here's why it's built the way it is."),
('a',1,"James, this is built to give you three things. Fewer fires landing on your desk."),
('a',2,"Heads who deal with problems at their own level."),
('a',3,"And one fair standard you can hold every head to."),
('b',1,"You already have scorecards. They tell you what happened."),
('b',2,"They don't tell you why. A head can hit the numbers, and still leave problems for you to clean up."),
('b',3,"The pillars cover the part the scorecard can't see. How your heads behave."),
('c',1,"There are six. Resilience. Decisiveness. Ingenuity. Assertiveness. Communication. Enthusiasm."),
('c',2,"They came from your own words, and Callum's. They were checked against the leadership research, and tested on five real situations here at S C C U."),
('c',3,"Each one runs from its opposite. So a head isn't good or bad at communication. They're somewhere between assumption and communication, this month."),
('c',4,"And each has a counterfeit. Something that looks like the pillar, but isn't. Cheerleading without delivery looks like enthusiasm."),
('d',1,"Now the order. The head scores themselves first."),
('d',2,"Why? Because the moment they see your number, they stop thinking, and start agreeing. Scoring first makes them look honestly at their own month."),
('d',3,"Then you score them, without seeing theirs. For the same reason. If you saw their number first, it would pull yours towards it."),
('d',4,"Two independent views are worth far more than one view and an echo."),
('e',1,"Then you reveal both together. Where you agree, move on. Where there's a gap, that's your conversation."),
('e',2,"If they've scored higher than you, they have a blind spot. If you've scored higher than them, they're underrating themselves, and you get to tell them."),
('e',3,"You never average the two. You agree the score in the room."),
('f',1,"Every score needs one dated example. That turns opinion into evidence."),
('f',2,"And the score is this month. Not a label on the person. A hard month drops it. A good month brings it back."),
('g',1,"Seven is the standard for a head here. But give people a pass mark, and they score themselves just above it."),
('g',2,"So nothing marks seven while they're scoring. They read the behaviour, and pick what's true."),
('g',3,"The line only appears once both scores are in."),
('h',1,"Two more rules. One case counts on one pillar. So a single bad day can't sink three scores, and the heads keep trusting the numbers."),
('h',2,"And every session ends with one focus, and one real assignment, done in the job. Behaviour changes by doing."),
('i',1,"And it grows. Later, the same six pillars become the questions you ask when you hire."),
('i',2,"Heads can run it with their own teams."),
('i',3,"And Scott sees the whole leadership picture on one screen."),
('z',1,"Twenty minutes a month, per head. That's the why."),
('z',2,"Next, how to use it."),
]
k=Kokoro('/home/claude/tts/kokoro-v1.0.onnx','/home/claude/tts/voices-v1.0.bin'); A=[]; SR=24000
for sc,st,t in L:
    s,SR=k.create(t,voice='bm_george',speed=1.0,lang='en-gb'); A.append(s)
D=[len(s)/SR for s in A]; print('voice',round(sum(D),1),'words',sum(len(t.split()) for _,_,t in L))
json.dump({'lines':[[a,b,c] for a,b,c in L],'dur':D},open('lines.json','w'))
frames=[]; marks=[]; cuts=[0]; n=0
total=lambda: sum(d for _,d in frames)
async def main():
    global n
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        ctx=await b.new_context(viewport={'width':1280,'height':720},device_scale_factor=1.5); pg=await ctx.new_page()
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file:///home/claude/why/why.html'); await pg.wait_for_timeout(700)
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
            await live(min(D[i]+0.2, 5.4 if (sc,st) in (('c',1),('c',2),('e',2)) else 3.0))
            need=D[i]+0.12+(0.9 if i==len(L)-1 else 0.32); el=total()-marks[i]
            if el<need: await snap(need-el)
        print('errors',errs); await b.close()
    cuts.append(len(frames)); files=[]
    for i in range(1,len(cuts)-1):
        fr=frames[cuts[i]:cuts[i+1]]
        if not fr: continue
        with open(f's{i}.txt','w') as f:
            for path,d in fr: f.write(f"file '{os.path.abspath(path)}'\nduration {max(d,0.02):.4f}\n")
            f.write(f"file '{os.path.abspath(fr[-1][0])}'\n")
        r=subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',f's{i}.txt','-vf','fps=30,scale=1920:1080,format=yuv420p','-c:v','libx264','-crf','18','-preset','veryfast','-pix_fmt','yuv420p',f's{i}.tmp.mp4']); assert r.returncode==0
        os.rename(f's{i}.tmp.mp4',f's{i}.mp4'); files.append(os.path.abspath(f's{i}.mp4'))
    open('all.txt','w').write(''.join(f"file '{x}'\n" for x in files))
    subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i','all.txt','-c','copy','joined.mp4'],check=True)
    T=total(); track=np.zeros(int((T+0.5)*SR),dtype=np.float32)
    for m,s in zip(marks,A):
        o=int((m+0.12)*SR); track[o:o+len(s)]+=s[:len(track)-o]
    sf.write('voice.wav',track,SR)
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i','joined.mp4','-i','voice.wav','-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','160k','-af','loudnorm=I=-16:TP=-1.5','-shortest','-movflags','+faststart','out.tmp.mp4'],check=True)
    os.rename('out.tmp.mp4','SCCU-Leadership-Pillars-Why-It-Works.mp4'); json.dump(marks,open('marks.json','w')); print('total',round(T,1))
asyncio.run(main())
