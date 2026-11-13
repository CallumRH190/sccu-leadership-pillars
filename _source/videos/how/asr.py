import sherpa_onnx, soundfile as sf, numpy as np, json
d='sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8'
rec=sherpa_onnx.OfflineRecognizer.from_transducer(encoder=f'{d}/encoder.int8.onnx',decoder=f'{d}/decoder.int8.onnx',joiner=f'{d}/joiner.int8.onnx',tokens=f'{d}/tokens.txt',model_type='nemo_transducer',num_threads=4)
a,sr=sf.read('rec16.wav',dtype='float32')
cfg=sherpa_onnx.VadModelConfig(); cfg.silero_vad.model='silero_vad.onnx'; cfg.silero_vad.min_silence_duration=0.35; cfg.silero_vad.min_speech_duration=0.2; cfg.silero_vad.max_speech_duration=25; cfg.sample_rate=sr
vad=sherpa_onnx.VoiceActivityDetector(cfg,buffer_size_in_seconds=200)
W=cfg.silero_vad.window_size; segs=[]
i=0
while i+W<=len(a):
    vad.accept_waveform(a[i:i+W]); i+=W
    while not vad.empty():
        s=vad.front; segs.append((s.start/sr,np.array(s.samples))); vad.pop()
vad.flush()
while not vad.empty():
    s=vad.front; segs.append((s.start/sr,np.array(s.samples))); vad.pop()
words=[]; out=[]
for st,smp in segs:
    stt=rec.create_stream(); stt.accept_waveform(sr,smp); rec.decode_stream(stt); r=stt.result
    toks=r.tokens; ts=r.timestamps
    cur=None
    for t,tm in zip(toks,ts):
        if t.startswith(' ') or cur is None:
            if cur: words.append(cur)
            cur=[t.strip(),st+tm,st+tm]
        else: cur[0]+=t
        cur[2]=st+tm
    if cur: words.append(cur)
    out.append((round(st,2),round(st+len(smp)/sr,2),r.text.strip()))
json.dump({'segs':out,'words':words},open('asr.json','w'))
for o in out: print(o)
print(len(words),'words')
