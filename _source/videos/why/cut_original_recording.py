import json, numpy as np, soundfile as sf
W=json.load(open('asr.json'))['words']
a,sr=sf.read('rec48.wav',dtype='float32')
# gentle high-pass to remove rumble
from numpy.fft import rfft, irfft, rfftfreq
A=rfft(a); f=rfftfreq(len(a),1/sr); A[f<70]=0; a=irfft(A,len(a)).astype(np.float32)
hop=int(0.01*sr); env=np.array([np.sqrt(np.mean(a[i:i+hop*2]**2)+1e-12) for i in range(0,len(a)-hop*2,hop)])
noise=np.percentile(env,8); thr=max(noise*3.2,0.004)
T=lambda i: W[i][1]
def end_after(j):   # cut point after word j
    lo=int((T(j)+0.10)/0.01); hi=int((T(j+1)+0.02)/0.01) if j+1<len(W) else len(env)-1
    hi=max(hi,lo+2); seg=env[lo:hi]; k=lo+int(np.argmin(seg))
    e=k
    while e>lo and env[e]<thr: e-=1
    return min((e+1)*0.01+0.09,(k*0.01)+0.12, T(j+1)-0.02 if j+1<len(W) else len(a)/sr)
def start_before(i):
    if i==0: return max(0,T(0)-0.15)
    lo=int((T(i-1)+0.10)/0.01); hi=int((T(i)+0.04)/0.01); hi=max(hi,lo+2); k=lo+int(np.argmin(env[lo:hi]))
    s=k
    while s<hi+6 and env[s]<thr: s+=1
    return max(s*0.01-0.07,k*0.01-0.05)
def clip(i,j,s0=None):
    s,e=(s0 if s0 is not None else start_before(i)),end_after(j); x=a[int(s*sr):int(e*sr)].copy(); n=int(0.008*sr)
    x[:n]*=np.linspace(0,1,n); x[-n:]*=np.linspace(1,0,n); return x
def join(parts):  # parts: arrays and float gaps
    out=[]
    for p in parts: out.append(np.zeros(int(p*sr),dtype=np.float32) if isinstance(p,float) else p)
    return np.concatenate(out)
S=[ # (scene, step, spec) spec = list of (i,j) spans or float gaps
('t',1,[(0,15)]),('a',1,[(16,30)]),('a',2,[(31,39)]),('a',3,[(40,49)]),
('b',1,[(50,59)]),('b',2,[(60,78)]),('b',3,[(79,90)]),
('c',1,[(91,101)]),('c',2,[(102,128)]),('c',3,[(129,153)]),('c',4,[(154,172)]),
('d',1,[(173,182)]),('d',2,[(183,206)]),('d',3,[(207,228)]),('d',4,[(234,246,76.72)]),
('e',1,[(247,266)]),('e',2,[(267,291)]),('e',3,[(292,293),0.10,(294,303)]),
('f',1,[(304,314)]),('f',2,[(315,338)]),
('g',1,[(358,365),0.30,(366,369),0.04,(372,378)]),
('g',2,[(379,382),0.03,(385,387),0.38,(388,395)]),
('g',3,[(396,404)]),
('h',1,[(405,429)]),('h',2,[(430,447)]),
('i',1,[(448,464)]),('i',2,[(465,472)]),('i',3,[(473,482)]),
('z',1,[(483,490)]),('z',2,[(491,495)])]
clips=[]
for sc,st,spec in S:
    x=join([p if isinstance(p,float) else clip(*p) for p in spec]); clips.append(x)
# room tone from the quiet stretch between takes
rt=a[int(115.6*sr):int(116.7*sr)].copy(); print('room tone rms',float(np.sqrt(np.mean(rt**2))),'speech thr',thr)
np.save('clips.npy',np.array(clips,dtype=object),allow_pickle=True); sf.write('roomtone.wav',rt,sr)
json.dump({'lines':[[s[0],s[1]] for s in S],'dur':[len(c)/sr for c in clips],'sr':sr},open('lines.json','w'))
print('total speech',round(sum(len(c) for c in clips)/sr,1))
# quick check file: all clips with 0.35s gaps
chk=join(sum(([c,0.35] for c in clips),[])); sf.write('check.wav',chk,sr)
cue=lambda li,wi: round(T(wi)-(S[li][2][0][2] if len(S[li][2][0])>2 else start_before(S[li][2][0][0])),2)
cues={'a1':cue(1,25),'c1':[cue(7,k) for k in (95,96,97,98,99,101)],'c2':[cue(8,105),cue(8,116),cue(8,124)],'d3':cue(13,218),'e2':cue(16,277)}
d=json.load(open('lines.json')); d['cues']=cues; json.dump(d,open('lines.json','w')); print('cues',cues)
import sys; sys.exit()
print('--- lead/tail check')
for sc,st,spec in S:
    for p in spec:
        if isinstance(p,float): continue
        i,j=p[0],p[1]; s=start_before(i); e=end_after(j); nxt=T(j+1) if j+1<len(W) else len(a)/sr
        flag='  <-- long lead' if T(i)-s>0.30 else ''
        print(sc,st,W[i][0],f'lead {T(i)-s:.2f}',W[j][0],f'tail {e-T(j):.2f} gap-to-next {nxt-T(j):.2f}',flag)
