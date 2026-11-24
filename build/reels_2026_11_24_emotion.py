"""CalcSouq emotional 'story' reels (24 Nov 2026), modelled on viral 3D metaphor reels: two AI-generated 3D stills
(ElevenLabs flow FWqCCNs368RY0PJb8THO, gemini-3.1-flash-lite-image, original characters, brand text removed),
slow camera moves, a crossfade reveal and few words. Goal: shares, tags and comments, not numbers.
Images: /tmp/vir/{A1,A2,B1,B2,C1,C2}.png (also kept in build/reel_assets/2026-11-24/).
Usage: python3 build/reels_2026_11_24_emotion.py <father|house|friends> [t,...]
Maths for 'friends': ₹5,000 a month for 30 years at an assumed 12% a year (1% a month, paid at start of month)
  = 5000 × ((1.01^360 − 1)/0.01) × 1.01 ≈ ₹1.76 crore. Assumption, not a promise.
"""
import sys, os, subprocess, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_fx import W, H, FPS, F, seg, ease, eio, lerp
from PIL import Image, ImageDraw, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "reel_assets/2026-11-24")
_IM = {}
def img(k):
    if k not in _IM:
        im = Image.open(os.path.join(SRC, k + ".png")).convert("RGB")
        s = max(W * 1.18 / im.width, H * 1.18 / im.height)
        im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 60, 2))
        _IM[k] = im
    return _IM[k]

def cam(k, p, z0, z1, cx0, cy0, cx1, cy1):
    """camera: zoom z (1 = fills frame) and centre (fractions of the image), eased by p"""
    im = img(k); q = eio(p); z = lerp(z0, z1, q)
    w = W / (W * 1.18 / im.width if W * 1.18 / im.width > H * 1.18 / im.height else H * 1.18 / im.height) / 1.18
    vw = im.width / 1.18 / z * 1.0; vh = vw * H / W
    vw = min(vw, im.width); vh = min(vh, im.height)
    cx = lerp(cx0, cx1, q) * im.width; cy = lerp(cy0, cy1, q) * im.height
    cx = min(max(cx, vw / 2), im.width - vw / 2); cy = min(max(cy, vh / 2), im.height - vh / 2)
    return im.crop((int(cx - vw / 2), int(cy - vh / 2), int(cx + vw / 2), int(cy + vh / 2))).resize((W, H), Image.BICUBIC)

_GR = {}
def grade(im, top=0.55, bot=0.55):
    key = (top, bot)
    if key not in _GR:
        m = Image.new("L", (W, H), 0); d = ImageDraw.Draw(m)
        for y in range(H):
            a = 0
            if y < 700: a = top * 255 * (1 - y / 700) ** 1.5
            if y > H - 760: a = max(a, bot * 255 * ((y - (H - 760)) / 760) ** 1.5)
            d.line([(0, y), (W, y)], fill=int(a))
        _GR[key] = m
    im.paste((0, 0, 0), (0, 0), _GR[key]); return im

def line(im, txt, y, t, t0, size=74, col=(255, 255, 255), t1=None, font="k"):
    p = ease(seg(t, t0, t0 + .7))
    if t1 is not None: p = min(p, 1 - ease(seg(t, t1, t1 + .5)))
    if p <= 0: return
    f = F(font, size); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    words, lines_, cur = txt.split(), [], ""
    for wd in words:
        if d.textlength((cur + " " + wd).strip(), font=f) > W - 150: lines_.append(cur); cur = wd
        else: cur = (cur + " " + wd).strip()
    lines_.append(cur)
    for i, l in enumerate(lines_):
        yy = y + i * size * 1.22 + (1 - p) * 26
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).text((W / 2, yy + 4), l, font=f, fill=(0, 0, 0, int(200 * p)), anchor="mm")
        lay.alpha_composite(sh.filter(ImageFilter.GaussianBlur(7)))
        d.text((W / 2, yy), l, font=f, fill=col + (int(255 * p),), anchor="mm")
    im.paste(lay, (0, 0), lay)

def mark(im):
    d = ImageDraw.Draw(im); d.text((W / 2, H - 70), "@calcsouq", font=F("b", 34), fill=(255, 255, 255, 150), anchor="mm")

def xfade(t, a, b, t0, d=1.2):
    p = seg(t, t0, t0 + d)
    if p <= 0: return a()
    if p >= 1: return b()
    return Image.blend(a(), b(), eio(p))

# ---------------- 1. father's shoes ----------------
def father(t):
    A = lambda: cam("A1", seg(t, 0, 7), 1.0, 1.22, .5, .62, .5, .45)
    B = lambda: cam("A2", seg(t, 5.6, 16), 1.3, 0.86, .38, .8, .45, .45)
    im = grade(xfade(t, A, B, 5.6))
    line(im, "Everyone clapped for his degree.", 230, t, 0.5, t1=5.4)
    line(im, "Nobody looked at the shoes", 170, t, 6.6, 70, t1=11.2)
    line(im, "that paid for it.", 360, t, 7.8, 80, (255, 214, 102), t1=11.2)
    line(im, "Tag someone who wore old shoes so you could wear new ones.", 1560, t, 11.0, 52, font="b")
    mark(im); return im

# ---------------- 2. the house ----------------
def house(t):
    A = lambda: cam("B1", seg(t, 0, 6.5), 1.0, 1.2, .5, .7, .5, .52)
    B = lambda: cam("B2", seg(t, 5.4, 17), 1.35, 1.0, .5, .86, .5, .45)
    im = grade(xfade(t, A, B, 5.4))
    line(im, "They clapped for the house.", 230, t, 0.5, t1=5.2)
    line(im, "They never saw the road.", 200, t, 6.4)
    line(im, "Old bike. Packed lunch. Years of small savings.", 1540, t, 8.6, 54, font="b", t1=12.4)
    line(im, "Respect the walk, not just the house.", 1540, t, 13.0, 58, col=(255, 214, 102))
    mark(im); return im

# ---------------- 3. two friends ----------------
def friends(t):
    A = lambda: cam("C1", seg(t, 0, 7), 1.05, 1.22, .5, .55, .5, .5)
    B = lambda: cam("C2", seg(t, 6.2, 18), 1.0, 1.12, .5, .5, .5, .48)
    im = grade(xfade(t, A, B, 6.2), .6, .7)
    line(im, "Age 25. Same salary.", 200, t, 0.4, t1=6.0)
    line(im, "One spent it. One planted it.", 300, t, 2.2, 66, (255, 214, 102), t1=6.0)
    line(im, "Age 55.", 210, t, 7.0, 96)
    line(im, "Which one are you becoming?", 1480, t, 9.6, 66)
    line(im, "₹5,000 a month from 25 to 55 at an assumed 12% ≈ ₹1.76 crore", 1650, t, 12.0, 38, (230, 230, 235), font="b")
    mark(im); return im

DUR = {"father": 16.0, "house": 17.0, "friends": 17.0}
FN = {"father": father, "house": house, "friends": friends}

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
