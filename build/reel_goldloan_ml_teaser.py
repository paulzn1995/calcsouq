"""Instagram teaser for the Malayalam gold-loan danger-line video (1080x1920, 23 s), built from the video's stills."""
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reels_2026_11_24_emotion as E
from reels_2026_11_24_emotion import cam, grade, line, mark, W, H, FPS, seg, eio
from PIL import Image
E.SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reel_assets/2026-11-25-goldloan")
GOLD = (255, 214, 102); RED = (255, 110, 110)
SH = [("S01A", 0, 6), ("S07B", 5.4, 11.5), ("S11A", 10.9, 16.5), ("S18A", 15.9, 23.5)]
def frame(t):
    cur = max(i for i, s in enumerate(SH) if t >= s[1])
    def shot(i):
        k, a, b = SH[i]; return cam(k, seg(t, a, b), 1.0, 1.18, .55, .5, .5, .45)
    im = shot(cur)
    if cur > 0:
        p = seg(t, SH[cur][1], SH[cur][1] + 1.0)
        if p < 1: im = Image.blend(shot(cur - 1), im, eio(p))
    im = grade(im, .78, .7)  # stronger top scrim: white/red lines sat on the bright verandah (EOD QA 25 Nov)
    line(im, "Gold: −₹15,720 a pavan", 320, t, -0.7, 74, t1=5.2)  # fully visible on frame 1 (EOD QA 25 Nov)
    line(im, "in just 20 days", 430, t, 1.3, 64, RED, t1=5.2)
    line(im, "Gold loan? This message", 320, t, 5.9, 66, t1=10.7)
    line(im, "may be on its way", 430, t, 6.9, 66, GOLD, t1=10.7)
    line(im, "Small loans: gold ≈ debt", 320, t, 11.4, 66, t1=15.7)
    line(im, "LTV can hit 99% today", 430, t, 12.4, 66, RED, t1=15.7)
    line(im, "Know your danger line.", 320, t, 16.4, 70)
    line(im, "Full video on YouTube · Malayalam", 1410, t, 17.4, 50, font="b")
    line(im, "youtube.com/@calcsouq · link in bio", 1490, t, 18.0, 44, (220, 220, 230), font="b")
    mark(im); return im
if __name__ == "__main__":
    if sys.argv[1] == "--frame": frame(float(sys.argv[2])).save(sys.argv[3]); sys.exit()
    out = sys.argv[1]; tmp = out + ".tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for i in range(int(23 * FPS)): p.stdin.write(frame(i / FPS).convert("RGB").tobytes())
    p.stdin.close(); assert p.wait() == 0; os.replace(tmp, out); print(out)
