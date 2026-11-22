"""CalcSouq reel graphics kit: original mascot, illustrated props, effects and backgrounds (PIL only).

Everything here is drawn from code (original artwork), safe to publish.
Import:  from reel_fx import *
Main pieces:
  scene_bg(t, theme)                       animated gradient + floating shapes, themes: night, gold, mint, sky, berry, sunset
  souq(img, x, y, s, t, mood, wave=False)  "Souq", the CalcSouq mascot (a friendly calculator character).
                                            mood: happy, shocked, thinking, wink, cool, sad. Blinks and bobs with t.
  speech(img, x, y, text, t0, t)           pop-in speech bubble anchored at (x, y)
  coin(d, x, y, r), coins_stack(d, x, y, n, r), note(d, x, y, w, rot), piggy(img, x, y, s, t), gold_bar(d, x, y, s),
  phone(img, x, y, s, screen_fn), calendar(d, x, y, s, label), doc(d, x, y, s, label, colour), trophy(d, x, y, s),
  rocket(img, x, y, s, t), chart_up(d, x, y, w, h, p, colour)
  confetti(img, t, t0, seed), sparkles(img, cx, cy, t, t0, seed), rays(img, cx, cy, t, colour)
  punch(img, t, t0)  quick zoom punch;  shake(img, t, t0)  camera shake
  kinetic(img, text, y, t, t0, size, colour)  word-by-word pop-in headline
  count(v0, v1, t, t0, t1)  eased count-up value
"""
import math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

W, H, FPS = 1080, 1920, 30
_I = "/usr/share/fonts/opentype/inter/"
def F(w, s): return ImageFont.truetype(_I + {"k": "Inter-Black", "b": "Inter-Bold", "s": "Inter-SemiBold", "r": "Inter-Regular"}[w] + ".otf", int(s))
INK = (21, 23, 26); GOLD = (245, 195, 0); OFF = (246, 246, 244); WHITE = (255, 255, 255)
RED = (235, 87, 87); GREEN = (46, 184, 114); BLUE = (82, 140, 255); PINK = (255, 105, 160); PURPLE = (150, 100, 240); ORANGE = (255, 150, 60)

def clamp(v, a=0, b=1): return max(a, min(b, v))
def seg(t, a, b): return clamp((t - a) / (b - a))
def ease(t): t = clamp(t); return 1 - (1 - t) ** 3
def eio(t): t = clamp(t); return 4 * t ** 3 if t < .5 else 1 - (-2 * t + 2) ** 3 / 2
def back(t):
    # exact 0 at the start: the formula gives ~1e-16 there, which made `if p > 0` items flash in early, offset
    t = clamp(t)
    if t <= 0: return 0.0
    if t >= 1: return 1.0
    c = 1.70158; return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2
def elastic(t):
    t = clamp(t)
    if t in (0, 1): return t
    return 2 ** (-10 * t) * math.sin((t * 10 - .75) * (2 * math.pi / 3)) + 1
def lerp(a, b, p): return a + (b - a) * p
def mix(c1, c2, p): return tuple(int(lerp(a, b, p)) for a, b in zip(c1, c2))
def count(v0, v1, t, t0, t1): return lerp(v0, v1, ease(seg(t, t0, t1)))

THEMES = {
    "night": ((14, 16, 22), (40, 34, 70), GOLD), "gold": ((255, 214, 64), (245, 160, 0), INK),
    "mint": ((14, 60, 52), (20, 120, 100), (180, 255, 220)), "sky": ((30, 70, 160), (90, 150, 255), WHITE),
    "berry": ((60, 16, 60), (170, 40, 110), (255, 200, 230)), "sunset": ((255, 120, 80), (140, 50, 140), WHITE),
}

def scene_bg(t, theme="night", seed=1):
    c1, c2, acc = THEMES.get(theme, THEMES["night"])
    im = Image.new("RGB", (W, H), c1); d = ImageDraw.Draw(im)
    for y in range(0, H, 8):
        p = y / H + 0.08 * math.sin(t * 0.8 + y / 300)
        d.rectangle([0, y, W, y + 8], fill=mix(c1, c2, clamp(p)))
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov); rnd = random.Random(seed)
    for k in range(14):  # floating shapes
        x = (rnd.random() * W + t * (20 + 30 * rnd.random()) * (1 if k % 2 else -1)) % (W + 200) - 100
        y = (rnd.random() * H - t * (40 + 40 * rnd.random())) % (H + 200) - 100
        r = 20 + rnd.random() * 70; a = 25 + int(rnd.random() * 30); kind = k % 3
        col = (*acc, a)
        if kind == 0: od.ellipse([x - r, y - r, x + r, y + r], outline=col, width=6)
        elif kind == 1: od.rounded_rectangle([x - r, y - r, x + r, y + r], int(r / 3), fill=col)
        else:
            pts = [(x + r * math.cos(t + i * 2.094), y + r * math.sin(t + i * 2.094)) for i in range(3)]; od.polygon(pts, fill=col)
    im.paste(ov, (0, 0), ov.filter(ImageFilter.GaussianBlur(2)))
    return im

def shadow(img, box, radius=40, blur=30, alpha=110, off=(0, 18)):
    sh = Image.new("L", (W, H), 0); ImageDraw.Draw(sh).rounded_rectangle([box[0] + off[0], box[1] + off[1], box[2] + off[0], box[3] + off[1]], radius, fill=alpha)
    sh = sh.filter(ImageFilter.GaussianBlur(blur)); img.paste((0, 0, 0), (0, 0), sh)

# ---------- Mascot: "Souq" the calculator ----------
def souq(img, x, y, s=1.0, t=0.0, mood="happy", wave=False, body=GOLD):
    bob = math.sin(t * 4) * 10 * s; y = y + bob
    w, h = 300 * s, 380 * s
    shadow(img, (x - w / 2, y - h / 2, x + w / 2, y + h / 2), int(70 * s), 25, 90)
    d = ImageDraw.Draw(img)
    limb = mix(body, INK, .45)
    # legs
    for dx in (-60, 60):
        d.rounded_rectangle([x + dx * s - 18 * s, y + h / 2 - 10 * s, x + dx * s + 18 * s, y + h / 2 + 60 * s], int(16 * s), fill=limb, outline=WHITE, width=max(2, int(3 * s)))
        d.ellipse([x + dx * s - 40 * s, y + h / 2 + 45 * s, x + dx * s + 30 * s, y + h / 2 + 80 * s], fill=limb, outline=WHITE, width=max(2, int(3 * s)))
    # arms
    lw = int(22 * s)
    d.line([(x - w / 2, y + 20 * s), (x - w / 2 - 70 * s, y + 90 * s)], fill=WHITE, width=lw + max(4, int(6 * s)))
    d.line([(x - w / 2, y + 20 * s), (x - w / 2 - 70 * s, y + 90 * s)], fill=limb, width=lw)
    ang = math.sin(t * 9) * 0.6 if wave else 0.2
    ex, ey = x + w / 2 + 80 * s * math.cos(-1.0 + ang), y - 10 * s + 80 * s * math.sin(-1.0 + ang) if wave else y + 90 * s
    if not wave: ex = x + w / 2 + 70 * s
    d.line([(x + w / 2, y + 20 * s), (ex, ey)], fill=WHITE, width=lw + max(4, int(6 * s)))
    d.line([(x + w / 2, y + 20 * s), (ex, ey)], fill=limb, width=lw)
    for hx, hy in ((x - w / 2 - 70 * s, y + 90 * s), (ex, ey)): d.ellipse([hx - 26 * s, hy - 26 * s, hx + 26 * s, hy + 26 * s], fill=WHITE, outline=INK, width=int(6 * s))
    # body
    d.rounded_rectangle([x - w / 2, y - h / 2, x + w / 2, y + h / 2], int(70 * s), fill=body, outline=INK, width=int(8 * s))
    # screen (face)
    sx0, sy0, sx1, sy1 = x - w / 2 + 35 * s, y - h / 2 + 35 * s, x + w / 2 - 35 * s, y - h / 2 + 185 * s
    d.rounded_rectangle([sx0, sy0, sx1, sy1], int(30 * s), fill=(28, 40, 36), outline=INK, width=int(6 * s))
    blink = (t % 3.2) > 3.05
    ex1, ex2, ey_ = x - 55 * s, x + 55 * s, sy0 + 60 * s
    eye = (140, 255, 200)
    def eyeo(cx, open_=True, big=False):
        r = (30 if big else 20) * s
        if not open_ or blink: d.line([(cx - r, ey_), (cx + r, ey_)], fill=eye, width=int(8 * s))
        else:
            d.ellipse([cx - r, ey_ - r, cx + r, ey_ + r], fill=eye); d.ellipse([cx - r / 3, ey_ - r / 2, cx + r / 6, ey_], fill=WHITE)
    my = sy0 + 115 * s
    if mood == "happy":
        eyeo(ex1); eyeo(ex2); d.arc([x - 45 * s, my - 35 * s, x + 45 * s, my + 25 * s], 15, 165, fill=eye, width=int(8 * s))
    elif mood == "shocked":
        eyeo(ex1, big=True); eyeo(ex2, big=True); d.ellipse([x - 18 * s, my - 18 * s, x + 18 * s, my + 22 * s], outline=eye, width=int(8 * s))
    elif mood == "thinking":
        eyeo(ex1); d.line([(ex2 - 20 * s, ey_), (ex2 + 20 * s, ey_ - 10 * s)], fill=eye, width=int(8 * s)); d.line([(x - 30 * s, my), (x + 30 * s, my - 8 * s)], fill=eye, width=int(8 * s))
    elif mood == "wink":
        eyeo(ex1); eyeo(ex2, open_=False); d.arc([x - 45 * s, my - 35 * s, x + 45 * s, my + 25 * s], 15, 165, fill=eye, width=int(8 * s))
    elif mood == "cool":
        d.rounded_rectangle([ex1 - 45 * s, ey_ - 22 * s, ex2 + 45 * s, ey_ + 22 * s], int(12 * s), fill=INK); d.line([(x - 35 * s, my), (x + 35 * s, my)], fill=eye, width=int(8 * s))
    elif mood == "sad":
        eyeo(ex1); eyeo(ex2); d.arc([x - 40 * s, my, x + 40 * s, my + 50 * s], 200, 340, fill=eye, width=int(8 * s))
    # keypad
    for r in range(3):
        for c in range(3):
            kx = x - w / 2 + 50 * s + c * 75 * s; ky = y - h / 2 + 215 * s + r * 50 * s
            col = (ORANGE if (r, c) == (2, 2) else WHITE)
            d.rounded_rectangle([kx, ky, kx + 52 * s, ky + 36 * s], int(10 * s), fill=col, outline=INK, width=int(4 * s))

def speech(img, x, y, text, t0, t, size=46, fill=WHITE, ink=INK):
    p = back(seg(t, t0, t0 + 0.35))
    if p <= 0: return
    f = F("b", size); d = ImageDraw.Draw(img)
    tw = d.textlength(text, font=f); w, h = (tw + 70) * p, (size + 50) * p
    box = (x - w / 2, y - h, x + w / 2, y)
    shadow(img, box, 40, 18, 80, (0, 10)); d = ImageDraw.Draw(img)
    d.rounded_rectangle(box, int(40 * p), fill=fill, outline=ink, width=5)
    d.polygon([(x - 20 * p, y - 2), (x + 10 * p, y - 2), (x - 30 * p, y + 34 * p)], fill=fill)
    if p > 0.8: d.text((x, y - h / 2), text, font=f, fill=ink, anchor="mm")

# ---------- Props ----------
def coin(d, x, y, r=50, face=GOLD, sym="₹"):
    d.ellipse([x - r, y - r * 0.92 + r * 0.14, x + r, y + r * 0.92 + r * 0.14], fill=(190, 140, 0))
    d.ellipse([x - r, y - r * 0.92, x + r, y + r * 0.92], fill=face, outline=(200, 150, 0), width=max(2, int(r / 10)))
    d.ellipse([x - r * .68, y - r * .62, x + r * .68, y + r * .62], outline=(255, 235, 150), width=max(2, int(r / 14)))
    d.text((x, y), sym, font=F("k", r * 0.9), fill=(170, 115, 0), anchor="mm")

def coins_stack(d, x, y, n, r=50, sym="₹"):
    for i in range(int(n)): coin(d, x, y - i * r * 0.32, r, sym=sym)

def note(img, x, y, w=260, rot=0, col=(110, 200, 140)):
    h = w * 0.48; n = Image.new("RGBA", (int(w), int(h)), (0, 0, 0, 0)); nd = ImageDraw.Draw(n)
    nd.rounded_rectangle([0, 0, w - 1, h - 1], 14, fill=col + (255,), outline=(40, 110, 70, 255), width=5)
    nd.ellipse([w / 2 - h * .3, h * .2, w / 2 + h * .3, h * .8], outline=(40, 110, 70, 255), width=5)
    nd.text((w / 2, h / 2), "₹", font=F("k", h * .4), fill=(40, 110, 70, 255), anchor="mm")
    n = n.rotate(rot, expand=True, resample=Image.BICUBIC); img.paste(n, (int(x - n.width / 2), int(y - n.height / 2)), n)

def gold_bar(d, x, y, s=1.0):
    pts = [(x - 110 * s, y + 40 * s), (x + 110 * s, y + 40 * s), (x + 80 * s, y - 40 * s), (x - 80 * s, y - 40 * s)]
    d.polygon(pts, fill=GOLD, outline=(190, 140, 0)); d.polygon([(x - 80 * s, y - 40 * s), (x + 80 * s, y - 40 * s), (x + 65 * s, y - 55 * s), (x - 65 * s, y - 55 * s)], fill=(255, 225, 120))
    d.text((x, y), "999.9", font=F("k", 30 * s), fill=(170, 115, 0), anchor="mm")

def piggy(img, x, y, s=1.0, t=0.0, col=PINK):
    d = ImageDraw.Draw(img); y += math.sin(t * 5) * 6 * s
    shadow(img, (x - 170 * s, y - 120 * s, x + 170 * s, y + 130 * s), int(120 * s), 25, 80)
    d = ImageDraw.Draw(img)
    for dx in (-100, 70): d.rounded_rectangle([x + dx * s, y + 70 * s, x + (dx + 40) * s, y + 150 * s], int(14 * s), fill=mix(col, INK, .25))
    d.ellipse([x - 170 * s, y - 120 * s, x + 170 * s, y + 130 * s], fill=col, outline=mix(col, INK, .4), width=int(6 * s))
    d.polygon([(x - 90 * s, y - 95 * s), (x - 50 * s, y - 165 * s), (x - 20 * s, y - 105 * s)], fill=mix(col, INK, .15))
    d.ellipse([x + 120 * s, y - 20 * s, x + 200 * s, y + 50 * s], fill=mix(col, WHITE, .3), outline=mix(col, INK, .4), width=int(5 * s))
    for dx in (145, 172): d.ellipse([x + dx * s - 7 * s, y + 8 * s, x + dx * s + 7 * s, y + 22 * s], fill=mix(col, INK, .5))
    d.ellipse([x + 50 * s, y - 50 * s, x + 74 * s, y - 26 * s], fill=INK)
    d.rounded_rectangle([x - 50 * s, y - 118 * s, x + 30 * s, y - 104 * s], int(6 * s), fill=mix(col, INK, .6))

def phone(img, x, y, s=1.0, screen_fn=None, t=0.0):
    w, h = 420 * s, 840 * s; box = (x - w / 2, y - h / 2, x + w / 2, y + h / 2)
    shadow(img, box, int(70 * s), 35, 120); d = ImageDraw.Draw(img)
    d.rounded_rectangle(box, int(70 * s), fill=(28, 30, 36), outline=(90, 95, 105), width=int(6 * s))
    sb = (box[0] + 22 * s, box[1] + 22 * s, box[2] - 22 * s, box[3] - 22 * s)
    d.rounded_rectangle(sb, int(52 * s), fill=OFF)
    d.rounded_rectangle([x - 60 * s, box[1] + 36 * s, x + 60 * s, box[1] + 62 * s], int(13 * s), fill=(28, 30, 36))
    if screen_fn: screen_fn(d, sb, t)

def calendar(d, x, y, s=1.0, label="15"):
    d.rounded_rectangle([x - 110 * s, y - 100 * s, x + 110 * s, y + 120 * s], int(26 * s), fill=WHITE, outline=INK, width=int(6 * s))
    d.rounded_rectangle([x - 110 * s, y - 100 * s, x + 110 * s, y - 40 * s], int(26 * s), fill=RED, outline=INK, width=int(6 * s))
    for dx in (-60, 60): d.rounded_rectangle([x + dx * s - 10 * s, y - 125 * s, x + dx * s + 10 * s, y - 80 * s], int(8 * s), fill=INK)
    d.text((x, y + 42 * s), label, font=F("k", 90 * s), fill=INK, anchor="mm")

def doc(d, x, y, s=1.0, label="PDF", col=RED):
    d.rounded_rectangle([x - 120 * s, y - 160 * s, x + 120 * s, y + 160 * s], int(20 * s), fill=WHITE, outline=INK, width=int(6 * s))
    for i in range(5): d.rounded_rectangle([x - 80 * s, y - 100 * s + i * 40 * s, x + (80 - 40 * (i % 2)) * s, y - 86 * s + i * 40 * s], int(6 * s), fill=(215, 218, 222))
    d.rounded_rectangle([x - 90 * s, y + 90 * s, x + 30 * s, y + 140 * s], int(10 * s), fill=col); d.text((x - 30 * s, y + 115 * s), label, font=F("k", 34 * s), fill=WHITE, anchor="mm")

def trophy(d, x, y, s=1.0):
    d.pieslice([x - 110 * s, y - 160 * s, x + 110 * s, y + 60 * s], 0, 180, fill=GOLD, outline=(190, 140, 0), width=int(6 * s))
    d.rectangle([x - 110 * s, y - 160 * s, x + 110 * s, y - 50 * s], fill=GOLD)
    for sgn in (-1, 1): d.arc([x + sgn * 110 * s - 50 * s, y - 140 * s, x + sgn * 110 * s + 50 * s, y - 40 * s], 90 if sgn > 0 else 270, 270 if sgn > 0 else 90, fill=GOLD, width=int(16 * s))
    d.rectangle([x - 22 * s, y + 50 * s, x + 22 * s, y + 110 * s], fill=(200, 150, 0)); d.rounded_rectangle([x - 90 * s, y + 105 * s, x + 90 * s, y + 150 * s], int(10 * s), fill=INK)
    d.text((x, y - 80 * s), "1", font=F("k", 90 * s), fill=(170, 115, 0), anchor="mm")

def rocket(img, x, y, s=1.0, t=0.0):
    d = ImageDraw.Draw(img)
    for i in range(6):  # flame
        r = (40 - i * 5) * s * (0.8 + 0.3 * math.sin(t * 30 + i))
        d.ellipse([x - r, y + 150 * s + i * 22 * s - r, x + r, y + 150 * s + i * 22 * s + r], fill=mix(ORANGE, GOLD, i / 6))
    d.polygon([(x - 70 * s, y + 60 * s), (x - 130 * s, y + 160 * s), (x - 60 * s, y + 140 * s)], fill=RED)
    d.polygon([(x + 70 * s, y + 60 * s), (x + 130 * s, y + 160 * s), (x + 60 * s, y + 140 * s)], fill=RED)
    d.rounded_rectangle([x - 70 * s, y - 120 * s, x + 70 * s, y + 150 * s], int(60 * s), fill=WHITE, outline=INK, width=int(6 * s))
    d.pieslice([x - 70 * s, y - 220 * s, x + 70 * s, y - 20 * s], 180, 360, fill=RED, outline=INK, width=int(6 * s))
    d.ellipse([x - 38 * s, y - 70 * s, x + 38 * s, y + 6 * s], fill=BLUE, outline=INK, width=int(6 * s))

def chart_up(d, x, y, w, h, p, col=GREEN, n=7):
    vals = [0.15, 0.25, 0.22, 0.42, 0.5, 0.72, 0.95][:n]
    bw = w / n * 0.62
    for i, v in enumerate(vals):
        q = ease(seg(p, i / n * 0.7, i / n * 0.7 + 0.4)); bh = h * v * q
        bx = x + i * w / n
        d.rounded_rectangle([bx, y - bh, bx + bw, y], int(bw / 4), fill=mix(col, WHITE, 0.15 * (i % 2)))

# ---------- Effects ----------
def confetti(img, t, t0, seed=1, n=90):
    if t < t0: return
    u = t - t0; d = ImageDraw.Draw(img); rnd = random.Random(seed)
    cols = [GOLD, PINK, BLUE, GREEN, ORANGE, PURPLE, WHITE]
    for i in range(n):
        ang = rnd.uniform(-math.pi * .9, -math.pi * .1); sp = rnd.uniform(700, 1500)
        x = W / 2 + math.cos(ang) * sp * u + rnd.uniform(-60, 60); y = H * .55 + math.sin(ang) * sp * u + 900 * u * u
        if y > H + 50: continue
        sz = rnd.uniform(10, 22); rot = u * rnd.uniform(4, 12); c = rnd.choice(cols)
        pts = [(x + sz * math.cos(rot + k * math.pi / 2) * (1 if k % 2 else .45), y + sz * math.sin(rot + k * math.pi / 2) * (1 if k % 2 else .45)) for k in range(4)]
        d.polygon(pts, fill=c)

def sparkles(img, cx, cy, t, t0, seed=2, n=14, radius=260, col=WHITE):
    if t < t0: return
    u = t - t0; d = ImageDraw.Draw(img); rnd = random.Random(seed)
    for i in range(n):
        a = rnd.uniform(0, 2 * math.pi); r = radius * (0.4 + 0.6 * rnd.random()) * ease(u * 2)
        x, y = cx + math.cos(a) * r, cy + math.sin(a) * r; s = 22 * max(0, 1 - u / 1.2) * (0.6 + rnd.random())
        if s <= 1: continue
        d.polygon([(x, y - s), (x + s * .25, y - s * .25), (x + s, y), (x + s * .25, y + s * .25), (x, y + s), (x - s * .25, y + s * .25), (x - s, y), (x - s * .25, y - s * .25)], fill=col)

def rays(img, cx, cy, t, col=GOLD, alpha=50, n=16):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    for i in range(n):
        a = t * 0.6 + i * 2 * math.pi / n
        od.polygon([(cx, cy), (cx + 1600 * math.cos(a - .08), cy + 1600 * math.sin(a - .08)), (cx + 1600 * math.cos(a + .08), cy + 1600 * math.sin(a + .08))], fill=(*col, alpha))
    img.paste(ov, (0, 0), ov)

def punch(img, t, t0, amt=0.08, dur=0.35):
    p = seg(t, t0, t0 + dur)
    if p <= 0 or p >= 1: return img
    z = 1 + amt * math.sin(p * math.pi); w, h = int(W * z), int(H * z)
    big = img.resize((w, h), Image.BILINEAR); return big.crop(((w - W) // 2, (h - H) // 2, (w - W) // 2 + W, (h - H) // 2 + H))

def shake(img, t, t0, amt=18, dur=0.4):
    p = seg(t, t0, t0 + dur)
    if p <= 0 or p >= 1: return img
    dx = int(amt * (1 - p) * math.sin(t * 90)); dy = int(amt * (1 - p) * math.cos(t * 70))
    return ImageChops.offset(img, dx, dy)

def kinetic(img, text, y, t, t0, size=110, col=WHITE, gap=0.09, font="k", hl=None, hl_col=GOLD):
    d = ImageDraw.Draw(img); f = F(font, size); words = text.split(" ")
    widths = [d.textlength(w + " ", font=f) for w in words]; x = (W - sum(widths)) / 2
    for i, w in enumerate(words):
        p = back(seg(t, t0 + i * gap, t0 + i * gap + 0.3))
        if p > 0:
            c = hl_col if hl and w.strip(",.?!") in hl else col
            yy = y + (1 - p) * 60
            d.text((x, yy), w, font=f, fill=c, anchor="ls")
        x += widths[i]

def pill(img, cx, cy, text, t, t0, bg=GOLD, fg=INK, size=48, pad=40):
    p = back(seg(t, t0, t0 + 0.35))
    if p <= 0: return
    d = ImageDraw.Draw(img); f = F("b", size); tw = d.textlength(text, font=f); w = (tw + pad * 2) * p; h = (size + 44) * p
    box = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2); shadow(img, box, int(h / 2), 14, 70, (0, 8)); d = ImageDraw.Draw(img)
    d.rounded_rectangle(box, int(h / 2), fill=bg)
    if p > 0.8: d.text((cx, cy), text, font=f, fill=fg, anchor="mm")

def endcard(img, t, t0, title, tool_line="Free · no sign-up · private", theme_col=GOLD):
    if t < t0: return
    u = t - t0; d = ImageDraw.Draw(img)
    kinetic(img, title, 760, t, t0, 92, theme_col)
    p = ease(seg(u, .3, .7)); d.text((W / 2, 850 + 20 * (1 - p)), tool_line, font=F("s", 44), fill=WHITE, anchor="mm")
    pill(img, W / 2, 1010, "calcsouq.com", t, t0 + .45, GOLD, INK, 64, 70)
    if u > 0.9: d.text((W / 2, 1140), "Link in bio ↗", font=F("b", 46), fill=WHITE, anchor="mm")
