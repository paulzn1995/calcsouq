"""CalcSouq nostalgic Indian 3D story reels (25 Nov 2026). AI 3D stills: ElevenLabs flow IrYfOAQOPzHCumV3oI7z
(gemini-3.1-flash-lite-image, original characters), kept in build/reel_assets/2026-11-25/.

1. calls  - "Why did families wait till late night to call?"  Fact: India's DoT charged long-distance (STD) calls at a
           quarter of the normal rate late at night (Lok Sabha papers 24 Feb 1988: late-night STD reduced to 25% of the
           normal tariff; quarter-rate tariff 10 p.m.-6 a.m. described in "STD PCO and Indian Telecom"). Hours changed
           over the years, so the caption says so.
2. gold   - 1990 24K average ₹3,200 per 10 g (Aditya Birla Capital, Upstox, BankBazaar tables); mid-Nov 2026 24K
           about ₹1.38-1.44 lakh per 10 g (Goodreturns 15 Nov, HDFC Sky 11 Nov, IBTimes 7 Nov). 80 g (10 pavan):
           8 x 3,200 = ₹25,600; 8 x 1,40,000 = ₹11.2 lakh; 1,40,000 / 3,200 = 43.75 (about 44 times).
           Jewellery is usually 22K plus making charges, so a real bill differs; the caption says so.
3. tin    - emotional story, no numbers.
Usage: python3 build/reels_2026_11_25_nostalgia.py <calls|gold|tin> [t,...]
"""
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reels_2026_11_24_emotion as E
from reels_2026_11_24_emotion import cam, grade, line, mark, W, H, FPS, seg, eio
from PIL import Image
E.SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reel_assets/2026-11-25")
GOLD = (255, 214, 102)

def seq(t, shots, fade=1.1):
    """shots: list of (key, t0, t1, z0, z1, cx0, cy0, cx1, cy1); crossfade into each next shot at its t0"""
    def shot(i):
        k, a, b, z0, z1, x0, y0, x1, y1 = shots[i]
        return cam(k, seg(t, a, b), z0, z1, x0, y0, x1, y1)
    cur = 0
    for i, s in enumerate(shots):
        if t >= s[1]: cur = i
    im = shot(cur)
    if cur + 1 < len(shots):
        pass
    if cur > 0:
        p = seg(t, shots[cur][1], shots[cur][1] + fade)
        if p < 1: im = Image.blend(shot(cur - 1), im, eio(p))
    return im

def calls(t):
    im = grade(seq(t, [("P1", 0, 6.5, 1.0, 1.2, .5, .62, .45, .6), ("P2", 5.8, 12.5, 1.25, 1.0, .62, .45, .55, .5),
                        ("P3", 11.8, 18, 1.0, 1.22, .5, .45, .48, .4), ("P4", 17.3, 25, 1.18, 1.0, .5, .55, .5, .5)]))
    line(im, "Why did our families wait", 310, t, 0.3, 68, t1=5.6)
    line(im, "till late night to call?", 405, t, 0.9, 68, GOLD, t1=5.6)
    line(im, "Late at night, STD calls", 310, t, 6.4, 66, t1=11.6)
    line(im, "cost just one quarter.", 405, t, 7.4, 74, GOLD, t1=11.6)
    line(im, "So every call was short.", 310, t, 12.4, 66, t1=17.1)
    line(im, "And every word mattered.", 405, t, 13.6, 66, GOLD, t1=17.1)
    line(im, "Today calls are free. Call them anyway.", 320, t, 18.0, 60)
    line(im, "Tag someone who remembers night calls.", 1430, t, 20.0, 46, font="b")
    mark(im); return im

def gold(t):
    im = grade(seq(t, [("G1", 0, 7, 1.0, 1.2, .5, .55, .45, .45), ("G2", 6.3, 13.5, 1.3, 1.05, .35, .58, .4, .55),
                        ("G3", 12.8, 22, 1.15, 1.0, .5, .45, .5, .5)]), .6, .6)
    line(im, "1990. Amma's wedding.", 310, t, 0.3, 70, t1=6.1)
    line(im, "10 pavan of gold (80 g)", 405, t, 1.4, 62, GOLD, t1=6.1)
    line(im, "It cost about ₹25,600.", 310, t, 6.9, 72, t1=12.6)
    line(im, "Same gold today: about ₹11 lakh", 1400, t, 8.8, 58, GOLD, t1=12.6)
    line(im, "The gold never changed.", 310, t, 13.4, 70)
    line(im, "Its price grew about 44 times.", 405, t, 14.6, 62, GOLD)
    line(im, "Ask your amma what her wedding gold cost.", 1430, t, 16.6, 46, font="b")
    line(im, "24K average price, 1990 vs Nov 2026", 1500, t, 16.6, 30, (215, 215, 220), font="b")
    mark(im); return im

def tin(t):
    im = grade(seq(t, [("R1", 0, 6.5, 1.0, 1.2, .5, .5, .55, .48), ("R2", 5.8, 12, 1.25, 1.0, .5, .6, .5, .55),
                        ("R3", 11.3, 18, 1.0, 1.18, .5, .6, .4, .55), ("R4", 17.3, 25, 1.2, 1.0, .5, .55, .5, .5)]))
    line(im, "Every month, Amma hid", 310, t, 0.3, 70, t1=5.6)
    line(im, "a few coins in the rice tin.", 405, t, 1.3, 66, GOLD, t1=5.6)
    line(im, "Nobody knew how much was there.", 310, t, 6.4, 62, t1=11.1)
    line(im, "Then one day, there was a new bicycle.", 310, t, 11.9, 62, t1=17.1)
    line(im, "You grew up.", 310, t, 18.0, 76)
    line(im, "She is still saving for you.", 405, t, 19.2, 64, GOLD)
    line(im, "Tag the person who saved for you without telling anyone.", 1410, t, 21.0, 46, font="b")
    mark(im); return im

DUR = {"calls": 25.0, "gold": 22.0, "tin": 25.0}
FN = {"calls": calls, "gold": gold, "tin": tin}

if __name__ == "__main__":
    n = sys.argv[1]; fn = FN[n]
    if len(sys.argv) > 2:
        for x in sys.argv[2].split(","): fn(float(x)).save(f"/tmp/vir/{n}_{x}.png")
        sys.exit()
    out = f"/tmp/vir/{n}_v.mp4"; tmp = out + ".tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for i in range(int(DUR[n] * FPS)): p.stdin.write(fn(i / FPS).convert("RGB").tobytes())
    p.stdin.close(); assert p.wait() == 0; os.replace(tmp, out); print(out)
