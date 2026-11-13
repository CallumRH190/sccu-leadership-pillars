import sherpa_onnx, soundfile as sf, numpy as np, sys, subprocess
src=sys.argv[1]; subprocess.run(['ffmpeg','-y','-loglevel','error','-i',src,'-ac','1','-ar','16000','/tmp/chk16.wav'],check=True)
d='sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8'
rec=sherpa_onnx.OfflineRecognizer.from_transducer(encoder=f'{d}/encoder.int8.onnx',decoder=f'{d}/decoder.int8.onnx',joiner=f'{d}/joiner.int8.onnx',tokens=f'{d}/tokens.txt',model_type='nemo_transducer',num_threads=2)
a,sr=sf.read('/tmp/chk16.wav',dtype='float32'); out=[]
step=20*sr
# find silent split points near every 20s
i=0
while i<len(a):
    j=min(len(a),i+step)
    if j<len(a):
        w=a[j-3*sr:j+3*sr]; h=sr//50; e=[np.abs(w[k:k+h]).mean() for k in range(0,len(w)-h,h)]; j=j-3*sr+int(np.argmin(e))*h
    st=rec.create_stream(); st.accept_waveform(sr,a[i:j]); rec.decode_stream(st); out.append(st.result.text.strip()); i=j
print(' '.join(out))
# silence report
h=sr//100; e=np.array([np.sqrt(np.mean(a[k:k+h]**2)) for k in range(0,len(a)-h,h)]); q=e<0.006; runs=[];s=None
for k,v in enumerate(q):
    if v and s is None: s=k
    if not v and s is not None:
        if k-s>130: runs.append((round(s/100,1),round((k-s)/100,1)))
        s=None
print('duration',round(len(a)/sr,1),'silences over 1.3s',runs,'silent share',round(q.mean(),2))
