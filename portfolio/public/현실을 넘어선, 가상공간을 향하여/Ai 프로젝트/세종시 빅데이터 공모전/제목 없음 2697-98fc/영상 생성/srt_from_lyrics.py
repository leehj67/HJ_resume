import pathlib
from typing import List

LYRIC_DIR = pathlib.Path("assets/lyrics")

def _fmt_ms(ms: int) -> str:
    h = ms // 3600000
    m = (ms % 3600000) // 60000
    s = (ms % 60000) // 1000
    ms = ms % 1000
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def make_srt_lines(lines: List[str], start_ms=500, per_line_ms=1600, gap_ms=200, cap_ms=10000) -> str:
    """간단한 10초 숏츠용 타이밍: 시작 0.5s, 줄당 1.6s, 줄사이 0.2s, 10초 이내로 컷"""
    t = start_ms
    blocks = []
    idx = 1
    for txt in lines:
        if not txt.strip():
            continue
        s = t
        e = min(t + per_line_ms, cap_ms - 1)
        if s >= cap_ms:
            break
        blocks.append(f"{idx}\n{_fmt_ms(s)} --> {_fmt_ms(e)}\n{txt.strip()}\n")
        t = e + gap_ms
        idx += 1
        if t >= cap_ms:
            break
    return "\n".join(blocks)

def process_txt(txt_path: pathlib.Path, **kw):
    lines = [l.rstrip("\n") for l in txt_path.read_text(encoding="utf-8").splitlines()]
    srt_txt = make_srt_lines(lines, **kw)
    out = txt_path.with_suffix(".srt")
    out.write_text(srt_txt, encoding="utf-8")
    print("Wrote:", out)

def main():
    LYRIC_DIR.mkdir(parents=True, exist_ok=True)
    cnt = 0
    for txt in sorted(LYRIC_DIR.glob("*.txt")):
        process_txt(txt)  # 기본 파라미터(10초)로 생성
        cnt += 1
    if cnt == 0:
        print("No .txt found in assets/lyrics")

if __name__ == "__main__":
    main()
