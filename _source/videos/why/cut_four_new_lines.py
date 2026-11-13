import json, numpy as np, soundfile as sf
W=json.load(open('asr.json'))['words']
a,sr=sf.read('rec48.wav',dtype='float32')
from numpy.fft import rfft, irfft, rfftfreq
A=rfft(a); f=rfftfreq(len(a),1/sr); A[f<70]=0; a=irfft(A,len(a)).astype(np.float32)
hop=int(0.01*sr); env=np.array([np.sqrt(np.mean(a[i:i+hop*2]**2)+1e-12) for i in range(0,len(a)-hop*2,hop)])
noise=np.percentile(env,8); thr=max(noise*3.2,0.004)
T=lambda i: W[i][1]
def end_after(j):
    lo=int((T(j)+0.10)/0.01); hi=int((T(j+1)+0.02)/0.01) if j+1<len(W) else len(env)-1
    hi=max(hi,lo+2); seg=env[lo:hi]; k=lo+int(np.argmin(seg)); e=k
    while e>lo and env[e]<thr: e-=1
    return min((e+1)*0.01+0.09,(k*0.01)+0.12, T(j+1)-0.02 if j+1<len(W) else len(a)/sr)
def start_before(i):
    if i==0: return max(0,T(0)-0.15)
    lo=int((T(i-1)+0.10)/0.01); hi=int((T(i)+0.04)/0.01); hi=max(hi,lo+2); k=lo+int(np.argmin(env[lo:hi])); s=k
    while s<hi+6 and env[s]<thr: s+=1
    return max(s*0.01-0.07,k*0.01-0.05)
def clip(i,j):
    s,e=start_before(i),end_after(j); x=a[int(s*sr):int(e*sr)].copy(); n=int(0.008*sr)
    x[:n]*=np.linspace(0,1,n); x[-n:]*=np.linspace(1,0,n); return x,s,e
def srms(x):
    h=int(0.02*sr); e=np.array([np.sqrt(np.mean(x[i:i+h]**2)) for i in range(0,len(x)-h,h)]); return float(np.sqrt(np.mean(e[e>0.01]**2))) if (e>0.01).any() else 0
old=list(np.load('/home/claude/vo/clips.npy',allow_pickle=True)); V=json.load(open('/home/claude/vo/lines.json'))
ref=float(np.median([srms(np.asarray(c,dtype=np.float32)) for c in old])); print('old speech rms',round(ref,4))
NEW={16:(0,17),21:(18,35),27:(36,47),28:(48,63)}; cues={}
for idx,(i,j) in NEW.items():
    x,s,e=clip(i,j); g=ref/srms(x); x=(x*g).astype(np.float32)
    print(V['lines'][idx],f'{s:.2f}-{e:.2f} new dur {len(x)/sr:.2f} (was {V["dur"][idx]:.2f}) gain {g:.2f} peak {abs(x).max():.2f}')
    old[idx]=x; V['dur'][idx]=len(x)/sr
    if idx==16: cues['e2']=round(T(14)-s,2)
    if idx==28: cues['z1']=[round(T(56)-s,2),round(T(61)-s,2)]
V['cues'].update(cues); print('cues',cues)
np.save('clips.npy',np.array(old,dtype=object),allow_pickle=True); json.dump(V,open('lines.json','w')); print('total',round(sum(V['dur']),1))
