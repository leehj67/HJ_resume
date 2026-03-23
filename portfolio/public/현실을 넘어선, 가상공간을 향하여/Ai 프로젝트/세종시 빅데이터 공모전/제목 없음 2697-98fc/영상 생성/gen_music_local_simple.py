import argparse, math, wave, struct, os
import numpy as np

SR = 44100

def env_exp(len_s, attack=0.005, release=0.3):
    n = int(len_s*SR)
    a = int(SR*attack)
    r = int(SR*release)
    sustain = max(0, n - a - r)
    e = np.zeros(n, dtype=np.float32)
    if a>0: e[:a] = np.linspace(0, 1, a, endpoint=False)
    if sustain>0: e[a:a+sustain] = 1.0
    if r>0: e[a+sustain:] = np.linspace(1, 0.0001, r)
    return e

def sine(f, dur, amp=0.5):
    t = np.arange(int(SR*dur))/SR
    return amp*np.sin(2*np.pi*f*t)

def bell_tone(f, dur, amp=0.6):
    """ 유아풍 벨: 기본파 + 살짝 FM + 빠른 감쇠 """
    t = np.arange(int(SR*dur))/SR
    mod = 2*np.pi*(f*2)*t
    y = np.sin(2*np.pi*f*t + 0.2*np.sin(mod))
    e = env_exp(dur, attack=0.002, release=min(0.25, dur*0.8))
    return (y*e*amp).astype(np.float32)

def noise(dur, amp=0.3):
    n = int(SR*dur)
    y = np.random.randn(n).astype(np.float32)
    # 가벼운 하이패스 느낌(노이즈를 조금 얇게)
    y = y - np.convolve(y, np.ones(64)/64, mode="same")
    return (y*amp).astype(np.float32)

def kick(dur=0.12, f0=80, f1=45, amp=0.9):
    n = int(SR*dur)
    t = np.arange(n)/SR
    # 피치가 아래로 떨어지는 킥
    f = np.linspace(f0, f1, n)
    phase = 2*np.pi*np.cumsum(f)/SR
    y = np.sin(phase)
    e = env_exp(dur, attack=0.001, release=dur*0.85)
    return (y*e*amp).astype(np.float32)

def snare(dur=0.10, amp=0.5):
    y = noise(dur, amp=amp)
    tone = sine(180, dur, amp=0.2)
    return (y*0.8 + tone*0.2).astype(np.float32)

def clap(dur=0.10, amp=0.6):
    # 짧은 여러 번의 노이즈 펄스(손뼉) + 감쇠
    base = noise(dur, amp=amp)
    # 3타 느낌
    delays = [0, int(0.01*SR), int(0.018*SR)]
    out = np.zeros_like(base)
    for d in delays:
        end = min(len(base), len(base)-d)
        out[d:d+end] += base[:end]* (0.8 if d==0 else (0.5 if d>0 else 1.0))
    e = env_exp(dur, attack=0.001, release=0.08)
    return (out*e).astype(np.float32)

def hihat(dur=0.06, amp=0.25):
    y = noise(dur, amp=amp)
    e = env_exp(dur, attack=0.001, release=0.04)
    return (y*e).astype(np.float32)

def mix_at(buf, y, start_s):
    i = int(start_s*SR)
    end = i + len(y)
    if end > len(buf):
        pad = end - len(buf)
        buf = np.pad(buf, (0,pad))
    buf[i:end] += y
    return buf

def save_wav(path, y):
    y = np.clip(y, -1.0, 1.0)
    # 16-bit PCM
    with wave.open(path, 'w') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        # 스테레오: 간단히 좌/우 동일 신호
        pcm = (y*32767).astype(np.int16)
        interleaved = np.column_stack((pcm, pcm)).ravel().tolist()
        w.writeframes(struct.pack('<'+'h'*len(interleaved), *interleaved))

def make_jingle(duration=12.0, bpm=110):
    beat = 60.0/bpm
    bar  = beat*4
    total = np.zeros(int(SR*duration), dtype=np.float32)

    # 코드 진행: C(60-64-67) - G(55-59-62) - Am(57-60-64) - F(53-57-60)
    chords = [(60,64,67), (55,59,62), (57,60,64), (53,57,60)]
    # 멜로디 노트(도~라) 범위
    def midi_to_freq(m): return 440.0*(2**((m-69)/12))

    t = 0.0
    while t < duration:
        for tri in chords:
            # 1마디(4/4) 동안 8분음표 × 4박 × 2 = 8개
            for i in range(8):
                note_dur = beat/2 * 0.95
                if t + i*(beat/2) >= duration: break
                pitch = np.random.choice(tri)  # 코드톤 기반
                tone = bell_tone(midi_to_freq(pitch), note_dur, amp=0.55)
                total = mix_at(total, tone, t + i*(beat/2))
            # 드럼: 킥(1,3), 스네어+클랩(2,4), 하이햇 8분
            for k in range(4):
                st = t + k*beat
                if st >= duration: break
                # 하이햇 8분
                for j in range(2):
                    hh = hihat(dur=0.05, amp=0.22)
                    total = mix_at(total, hh, st + j*(beat/2))
                # 킥
                if k in (0,2):
                    total = mix_at(total, kick(), st)
                # 스네어+클랩
                if k in (1,3):
                    total = mix_at(total, snare(), st)
                    total = mix_at(total, clap(),  st)
            t += bar
            if t >= duration: break

    # 살짝 마스터링: 부드러운 리미트
    peak = np.max(np.abs(total)) + 1e-6
    if peak > 0.9:
        total *= (0.9/peak)
    return total

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="assets/audio/seri_intro.wav")
    ap.add_argument("--duration", type=float, default=12.0)
    ap.add_argument("--bpm", type=int, default=110)
    args = ap.parse_args()

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    y = make_jingle(duration=args.duration, bpm=args.bpm)
    save_wav(args.out, y)
    print("Saved:", args.out)

if __name__ == "__main__":
    main()
