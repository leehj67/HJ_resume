import argparse, os, re, pathlib, sys, subprocess
import win32com.client

TIME_RE = re.compile(r"(\d{2}):(\d{2}):(\d{2}),(\d{3})")

def parse_srt(srt_path):
    text = pathlib.Path(srt_path).read_text(encoding="utf-8", errors="ignore")
    blocks = re.split(r"\r?\n\r?\n", text.strip())
    items = []
    for b in blocks:
        lines = [l for l in b.splitlines() if l.strip()]
        if len(lines) < 2:
            continue
        if "-->" in lines[0]:
            time_line = lines[0]; content = lines[1:]
        else:
            if len(lines) < 2: continue
            time_line = lines[1]; content = lines[2:]
        if "-->" not in time_line:
            continue
        a, b = [t.strip() for t in time_line.split("-->")]
        def to_ms(t):
            m = TIME_RE.match(t)
            if not m: return 0
            hh, mm, ss, ms = map(int, m.groups())
            return ((hh*3600+mm*60+ss)*1000+ms)
        start_ms = to_ms(a); end_ms = to_ms(b)
        txt = " ".join(content).strip()
        if txt:
            items.append({"start_ms":start_ms, "end_ms":end_ms, "text":txt})
    return items

def sapi_tts_to_wav(text, out_wav, rate=0, volume=100, voice_idx=None):
    spk = win32com.client.Dispatch("SAPI.SpVoice")
    if voice_idx is not None:
        try:
            spk.Voice = spk.GetVoices().Item(int(voice_idx))
        except Exception:
            pass
    spk.Rate = int(rate); spk.Volume = int(volume)
    stream = win32com.client.Dispatch("SAPI.SpFileStream")
    SSFMCreateForWrite = 3
    stream.Open(out_wav, SSFMCreateForWrite)
    spk.AudioOutputStream = stream
    spk.Speak(text)
    stream.Close()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--srt", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--rate", type=int, default=0)
    ap.add_argument("--voice_index", type=int, default=None)
    args = ap.parse_args()

    items = parse_srt(args.srt)
    if not items:
        print("No subtitles found"); sys.exit(1)

    tmpdir = "assets/tmp_tts"
    os.makedirs(tmpdir, exist_ok=True)

    inputs = []
    chains = []
    labels = []
    for i, it in enumerate(items, start=1):
        seg = os.path.join(tmpdir, f"seg_{i:03d}.wav")
        sapi_tts_to_wav(it["text"], seg, rate=args.rate, voice_idx=args.voice_index)
        inputs += ["-i", seg]
        lbl = f"v{i}"
        # 44.1kHz mono 정규화 + 시작시간 지연
        chains.append(f"[{i-1}:a]aformat=sample_fmts=s16:sample_rates=44100:channel_layouts=mono,adelay={it['start_ms']}[{lbl}]")
        labels.append(f"[{lbl}]")

    n = len(labels)
    if n == 1:
        chains.append(f"{labels[0]}anull,volume=+12dB[outa]")
    else:
        chains.append("".join(labels)+f"amix=inputs={n}:normalize=1,volume=+12dB[outa]")

    filter_complex = "; ".join(chains)

    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    cmd = ["ffmpeg", "-y"] + inputs + [
        "-filter_complex", filter_complex,
        "-map", "[outa]",
        "-c:a", "pcm_s16le",
        str(out)
    ]
    print(">>", " ".join(cmd))
    # 핵심: shell=False 로 안전 전달
    subprocess.run(cmd, shell=False, check=True)
    print("Saved:", out)

if __name__=="__main__":
    main()
