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
S={'t':(5,18),'1a':(19,29),'1b':(30,36),'2a':(37,39),'2b':(40,55),'2c':(56,68),'2d':(69,88),'3a':(89,93),'3b':(94,107),'3c':(108,123),'3d':(124,132),
'4a':(133,139),'4b':(140,156),'5a':(157,167),'5b':(168,173),'5c':(174,188),'5d':(189,196),'6a':(197,204),'6b':(205,216),'6c':(217,225),'7':(226,237),'8':(238,256)}
clips={}; 
for k,(i,j) in S.items():
    x,s,e=clip(i,j); clips[k]=x
    print(k,f'{s:.2f}-{e:.2f} dur {len(x)/sr:.2f} lead {T(i)-s:.2f} tail {e-T(j):.2f}',W[i][0],'..',W[j][0])
np.save('clips_how.npy',clips,allow_pickle=True)
# room tone: quietest 1s stretch
win=100; rm=[env[i:i+win].mean() for i in range(0,len(env)-win,10)]; k=int(np.argmin(rm))*10
rt=a[int(k*0.01*sr):int((k+win)*0.01*sr)].copy(); sf.write('roomtone.wav',rt,sr); print('roomtone at',k*0.01,'rms',float(np.sqrt(np.mean(rt**2))),'thr',thr)
print('total speech',round(sum(len(c) for c in clips.values())/sr,1))
chk=np.concatenate(sum(([c,np.zeros(int(0.35*sr),dtype=np.float32)] for c in clips.values()),[])); sf.write('check.wav',chk,sr)
