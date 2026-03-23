import json, pathlib, shlex, subprocess, sys, platform

# meta가 있으면 우선 사용. 없으면 자동탐색(stem 매칭)
META_PATH = pathlib.Path("meta/dataset.jsonl")

AUDIO_DIR = pathlib.Path("assets/audio")
LYRIC_DIR = pathlib.Path("assets/lyrics")
VIDEO_DIR = pathlib.Path("assets/video_raw")
OUT_DIR   = pathlib.Path("assets/shorts")

def run(cmd: str):
    print(">>", cmd)
    subprocess.run(cmd, shell=True, check=True)

def load_meta_items():
    items = []
    for line in META_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            items.append(json.loads(line))
        except Exception:
            pass
    return items

def auto_discover_items():
    """
    meta가 없을 때 자동 매칭:
    - stem 기준으로 audio(.mp3/.wav), lyrics(.srt), dance mp4를 찾음
    - dance 파일은 <stem>_dance.mp4 > <stem>.mp4 우선
    - srt가 없으면 스킵(먼저 srt_from_lyrics.py 실행)
    """
    items = []
    audio_map = {}
    for a in list(AUDIO_DIR.glob("*.mp3")) + list(AUDIO_DIR.glob("*.wav")):
        audio_map[a.stem] = a

    srt_map = {p.stem: p for p in LYRIC_DIR.glob("*.srt")}

    for stem, audio in audio_map.items():
        # SRT
        srt = srt_map.get(stem)
        if not srt:
            # _dance 접미어 보정
            alt = stem.replace("_dance", "")
            srt = srt_map.get(alt)
        if not srt:
            continue

        # Dance video
        dance = VIDEO_DIR / f"{stem}_dance.mp4"
        if not dance.exists():
            alt = VIDEO_DIR / f"{stem}.mp4"
            if alt.exists():
                dance = alt
        if not dance.exists():
            continue

        items.append({
            "id": stem,
            "files": {
                "audio": str(audio).replace("\\","/"),
                "lyrics_srt": str(srt).replace("\\","/"),
                "dance_video": str(dance).replace("\\","/"),
                "short_out": f"assets/shorts/{stem}_short.mp4"
            },
            "timing": {"start_sec": 0.0, "dur_sec": 10.0}
        })
    return items

def iter_targets():
    if META_PATH.exists():
        for it in load_meta_items():
            f = it.get("files", {})
            if f.get("audio") and f.get("lyrics_srt") and f.get("dance_video") and f.get("short_out"):
                yield it
    else:
        for it in auto_discover_items():
            yield it

def build_short(item):
    audio = pathlib.Path(item["files"]["audio"])
    srt   = pathlib.Path(item["files"]["lyrics_srt"])
    dance = pathlib.Path(item["files"]["dance_video"])
    out   = pathlib.Path(item["files"]["short_out"])
    out.parent.mkdir(parents=True, exist_ok=True)

    start = float(item.get("timing",{}).get("start_sec", 0.0))
    dur   = float(item.get("timing",{}).get("dur_sec", 10.0))

    if not (audio.exists() and dance.exists() and srt.exists()):
        print("skip (missing file):", item.get("id"))
        return

    # OS별 기본 한글 폰트 "패밀리명" (파일 경로 X)
    sysname = platform.system().lower()
    if "windows" in sysname:
        font_family = "Malgun Gothic"
    elif "darwin" in sysname:  # macOS
        font_family = "AppleSDGothicNeo"
    else:  # Linux
        font_family = "Noto Sans CJK KR"

    # force_style 안의 쉼표는 \, 로 이스케이프
    style = f"FontName={font_family}\\,Fontsize=48\\,Outline=2\\,Shadow=1\\,PrimaryColour=&H00FFFFFF&"

    srt_ = str(srt).replace("\\", "/")
    vf = f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,subtitles='{srt_}':force_style='{style}'"

    cmd = (
        f'ffmpeg -y -ss {start} -t {dur} -i "{dance}" '
        f'-ss {start} -t {dur} -i "{audio}" '
        f'-vf "{vf}" -map 0:v -map 1:a -c:v libx264 -pix_fmt yuv420p '
        f'-c:a aac -b:a 192k -shortest "{out}"'
    )
    run(cmd)

def main():
    any_job = False
    for it in iter_targets():
        print(f"[build] {it.get('id')}")
        build_short(it)
        any_job = True
    if not any_job:
        print("No matched items. Ensure files exist like:\n"
              "- assets/audio/<stem>.mp3/.wav\n"
              "- assets/lyrics/<stem>.srt (먼저 srt_from_lyrics.py 실행)\n"
              "- assets/video_raw/<stem>_dance.mp4 (또는 <stem>.mp4)")

if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print("ffmpeg error:", e)
        sys.exit(1)
