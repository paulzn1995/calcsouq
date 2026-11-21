"""Funny milestone reel: '@calcsouq went from 0 followers to 1 follower. Yipeeee'.
Format idea from Paulson (21 Nov 2026): the 'I went from this -> Yipeeee' profile-header meme.
Uses only crops of our own @calcsouq profile screenshots (build/ig_src/). Output: build/static/media/ig/2026-11-21-first-follower.mp4
"""
import math, os, random, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "ig_src")
OUT = os.path.join(HERE, "static/media/ig/2026-11-21-first-follower.mp4")
W, H, FPS, DUR = 1080, 1920, 30, 10.0
GOLD, YEL, RED = (240, 226, 160), (247, 230, 140), (255, 70, 70)
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerifCondensed-Bold.ttf"
MONT = "/usr/share/fonts/truetype/google-fonts/ofl/montserrat/Montserrat[wght].ttf"


def mont(size, weight=b"ExtraBold"):
    f = ImageFont.truetype(MONT, size)
    try: f.set_variation_by_name(weight)
    except Exception: pass
    return f


def ease(x): x = max(0, min(1, x)); return 1 - (1 - x) ** 3


def strip(name, box, hl):
    """Crop our profile header; hl = (x0,y0,x1,y1) of the follower count inside the crop."""
    im = Image.open(os.path.join(SRC, name)).convert("RGB").crop(box)
    s = W / im.width; im = im.resize((W, int(im.height * s)), Image.LANCZOS)
    return im, tuple(int(v * s) for v in hl)


A, A_HL = strip("profile-0-followers.jpg", (20, 40, 1178, 400), (560, 185, 775, 295))
B, B_HL = strip("profile-1-follower.png", (20, 490, 1179, 830), (565, 175, 760, 285))

rng = random.Random(20261121)
CONF = [(rng.uniform(0, W), rng.uniform(-900, -20), rng.uniform(260, 520), rng.uniform(0, 6.28), rng.choice([YEL, RED, (90, 200, 255), (120, 230, 140), (255, 255, 255)]), rng.randint(10, 20)) for _ in range(140)]


def text_c(d, y, s, font, fill, alpha=1.0):
    w = d.textlength(s, font=font); col = tuple(int(c * alpha) for c in fill)
    d.text(((W - w) / 2, y), s, font=font, fill=col)


def circle(d, box, prog, y_off):
    if prog <= 0: return
    x0, y0, x1, y1 = box; pad = 14
    d.arc((x0 - pad, y0 - pad + y_off, x1 + pad, y1 + pad + y_off), -100, -100 + 360 * ease(prog), fill=RED, width=9)


def frame(t):
    img = Image.new("RGB", (W, H), (0, 0, 0)); d = ImageDraw.Draw(img)
    if t < 3.2:  # part 1: I went from this
        a = ease(t / 0.35)
        text_c(d, 560 - 40 * (1 - a), "I went from this", ImageFont.truetype(SERIF, 100), GOLD, a)
        if t > 0.5:
            k = ease((t - 0.5) / 0.3); y = 790
            sw = int(W * (0.9 + 0.1 * k)); sh = int(A.height * sw / W)
            im = A.resize((sw, sh)); img.paste(im, ((W - sw) // 2, y + (A.height - sh) // 2))
            d.rectangle((0, y - 2, W, y + A.height + 2), outline=(70, 70, 70), width=2)
            circle(d, A_HL, (t - 1.2) / 0.5, y)
            if t > 1.9:
                text_c(d, y + A.height + 70, "(not even my mum followed)", mont(58, b"SemiBold"), (200, 200, 200), ease((t - 1.9) / 0.3))
    elif t < 7.0:  # part 2: Yipeeee
        tt = t - 3.2
        if tt < 0.15:  # flash
            v = int(255 * (1 - tt / 0.15)); img.paste((v, v, v), (0, 0, W, H)); return img
        es = min(10, 1 + int(tt / 0.12))
        sz = 128 if es < 8 else 128 - (es - 7) * 6
        text_c(d, 600, "Yip" + "e" * es, mont(sz), YEL)
        y = 800; img.paste(B, (0, y)); d = ImageDraw.Draw(img)
        circle(d, B_HL, (tt - 0.6) / 0.5, y)
        if tt > 1.3:
            text_c(d, y + B.height + 70, "+1 follower. We're basically famous.", mont(50, b"SemiBold"), (230, 230, 230), ease((tt - 1.3) / 0.3))
        for x, y0, sp, ph, col, s in CONF:  # confetti
            yy = y0 + sp * tt
            if 0 < yy < H:
                xx = x + 30 * math.sin(ph + tt * 3); r = s * (0.6 + 0.4 * abs(math.sin(ph + tt * 5)))
                d.rectangle((xx, yy, xx + s, yy + r), fill=col)
    else:  # part 3: end card
        tt = t - 7.0; a = ease(tt / 0.4)
        text_c(d, 640, "Dear 1 follower,", mont(84), (255, 255, 255), a)
        text_c(d, 750, "you ARE the fan club.", mont(84), YEL, a)
        if tt > 0.9:
            b = ease((tt - 0.9) / 0.35)
            text_c(d, 960, "Be follower #2", mont(96), (255, 255, 255), b)
            text_c(d, 1090, "@calcsouq  ·  free calculators", mont(48, b"SemiBold"), (190, 190, 190), b)
    return img


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True); tmp = OUT + ".silent.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "medium", tmp], stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)): p.stdin.write(np.asarray(frame(i / FPS)).tobytes())
    p.stdin.close(); p.wait()
    sys.path.insert(0, HERE); import reel_audio
    print(reel_audio.mux(tmp, OUT, cues="0:hit,0.5:pop,1.2:swoosh,1.9:fail,2.3:riser,3.2:boom,3.3:sparkle,3.9:pop,4.5:success,7:whoosh,7.9:ding", style="funk", seed=20261124))
    os.remove(tmp)


if __name__ == "__main__":
    main()
