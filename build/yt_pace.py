"""Re-render an existing reel (module with REELS = {name: (fn(t), dur)}) at reading pace for YouTube Shorts / Reels.
Usage: python3 yt_pace.py <module> <reel> <out.mp4> [--slow 1.75]
Writes a silent video; add sound with reel_audio.py (multiply the original cue times by the same SLOW factor).
"""
import importlib, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_fx import W, H, FPS

mod, name, out = sys.argv[1], sys.argv[2], sys.argv[3]
slow = float(sys.argv[sys.argv.index("--slow") + 1]) if "--slow" in sys.argv else 1.75
fn, dur = importlib.import_module(mod).REELS[name]
tmp = out + ".tmp.mp4"
p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                      "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
for i in range(int(dur * slow * FPS)):
    p.stdin.write(fn(i / FPS / slow).convert("RGB").tobytes())
p.stdin.close(); assert p.wait() == 0; os.replace(tmp, out)
print(out, round(dur * slow, 2), "s")
