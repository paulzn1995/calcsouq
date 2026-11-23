"""CalcSouq Malayalam long video: will your home loan EMI rise again? RBI 4 Dec decision (16:9, 1920x1080).
Copied from the gold/Hormuz Malayalam videos (helpers in yt_long_gold_ml) with this video's script, timings and scenes.
Local 3D-style upgrades: shaded extruded bars, a perspective house, stacked 3D coins, parallax dust and slow push-ins on key numbers.
Usage: python3 yt_long_emi_ml.py S1 S2 ... | --frame S3 10 out.png | --srt-en out.srt | --srt-ml out.srt | --timeline
B-roll clips are placed by the ElevenLabs composition after the scenes in BROLL; subtitles are shifted to match.
"""
import sys, os, math, json, random, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import yt_long_gold_ml as G
from yt_long_rates import fx, F, INK, WHITE, RED, GREEN, seg, ease, back, lerp, mix, clamp, count, T, wrap, shadow, bank, arrow
from PIL import Image, ImageDraw, ImageFilter
W, H, FPS = 1920, 1080, 30
HERE = os.path.dirname(os.path.abspath(__file__))
FOLDER = os.path.join(HERE, "youtube/long/2026-11-23-emi-rbi-malayalam")
SC = json.load(open(os.path.join(FOLDER, "scenes.json")))
ORDER = list(SC.keys())
AUDIO = json.load(open(os.path.join(FOLDER, "audio.json"))) if os.path.exists(os.path.join(FOLDER, "audio.json")) else {k: 30.0 for k in ORDER}
PAD = 0.45
BROLL = {"S1": 6.12}  # house at dusk (photoreal B-roll) right after the hook
G.SC, G.AUDIO, G.ORDER, G.PAD, G.END_EXTRA = SC, AUDIO, ORDER, PAD, 0.0
def L(s): return AUDIO[s] + PAD
ts, head, panel, tag, big_num, MF, vis2, subtitle, inr = G.ts, G.head, G.panel, G.tag, G.big_num, G.MF, G.vis2, G.subtitle, G.inr
GOLDC, GOLD2 = G.GOLDC, G.GOLD2
REDC = (225, 70, 62); GRN = (60, 170, 110); BLU = (80, 130, 230); GREY = (170, 175, 195); NAVY = (30, 34, 50)

def base(s, t, seed, tint=(245, 190, 60)):
    img = G.bg(t, seed, tint); G.brand(img); return img

def zoom(img, z, cx=W / 2, cy=H / 2):
    if z <= 1.001: return img
    w, h = W / z, H / z; cx = clamp(cx, w / 2, W - w / 2); cy = clamp(cy, h / 2, H - h / 2)
    box = (int(cx - w / 2), int(cy - h / 2), int(cx - w / 2) + int(w), int(cy - h / 2) + int(h))
    return img.crop(box).resize((W, H), Image.BICUBIC)

def push(t, t0, dur=6.0, amt=0.05): return 1 + amt * ease(seg(t, t0, t0 + dur))

# ---------------- local 3D-style props ----------------
def bar3d(img, x, ybase, w, h, col, depth=26):
    """extruded bar: front face with vertical gradient, lit top and darker side, soft floor shadow and reflection"""
    if h <= 1: return
    d = ImageDraw.Draw(img)
    sh = Image.new("L", (int(w + depth + 80), 60), 0); ImageDraw.Draw(sh).ellipse([10, 10, w + depth + 70, 50], fill=110)
    img.paste((0, 0, 0), (int(x - 30), int(ybase - 20)), sh.filter(ImageFilter.GaussianBlur(12))); d = ImageDraw.Draw(img)
    top, side = mix(col, WHITE, .35), mix(col, (0, 0, 0), .35)
    d.polygon([(x + w, ybase), (x + w + depth, ybase - depth * .6), (x + w + depth, ybase - h - depth * .6), (x + w, ybase - h)], fill=side)
    d.polygon([(x, ybase - h), (x + depth, ybase - h - depth * .6), (x + w + depth, ybase - h - depth * .6), (x + w, ybase - h)], fill=top)
    for k in range(int(h)):
        f = k / max(1, h); d.line([(x, ybase - k), (x + w, ybase - k)], fill=mix(mix(col, (0, 0, 0), .18), mix(col, WHITE, .12), f))
    d.line([(x + 6, ybase - h + 4), (x + 6, ybase - 4)], fill=mix(col, WHITE, .5), width=3)
    rh = int(min(h, 90))  # faint floor reflection
    if rh > 4:
        ref = img.crop((int(x), int(ybase - rh), int(x + w), int(ybase))).transpose(Image.FLIP_TOP_BOTTOM)
        m = Image.linear_gradient("L").resize((ref.size[0], rh)).point(lambda v: int(v * .0) + int((255 - v) * .22))
        img.paste(ref, (int(x), int(ybase + 2)), m)

def coin3d(img, cx, cy, r, col=(205, 210, 220), edge=(120, 125, 140)):
    d = ImageDraw.Draw(img); ry = r * .32
    d.rectangle([cx - r, cy - 14, cx + r, cy], fill=edge); d.ellipse([cx - r, cy - ry, cx + r, cy + ry], fill=edge)
    d.ellipse([cx - r, cy - 14 - ry, cx + r, cy - 14 + ry], fill=col)
    d.ellipse([cx - r * .7, cy - 14 - ry * .7, cx + r * .7, cy - 14 + ry * .7], outline=mix(col, WHITE, .5), width=3)

def coin_stack(img, cx, ybase, n, r=70, col=(240, 200, 90), edge=(160, 120, 30)):
    shadow(img, (cx - r, ybase - 20, cx + r, ybase + 10), int(r), 16, 90, (0, 10))
    for i in range(int(n)): coin3d(img, cx, ybase - i * 16, r, col, edge)

def house3d(img, cx, cy, s=1.0, p=1.0, glow=0.0):
    """perspective house: front and side walls, sloped roof, lit windows"""
    if p <= 0.01: return
    s *= back(p) if p < 1 else 1; d = ImageDraw.Draw(img)
    fw, fh, sw, rise = 230 * s, 170 * s, 120 * s, 60 * s
    x0, y0 = cx - fw / 2 - sw / 2, cy - fh / 2 + 40 * s
    shadow(img, (x0 - 20 * s, y0 + fh - 20 * s, x0 + fw + sw + 40 * s, y0 + fh + 30 * s), int(40 * s), 22, 120, (0, 6)); d = ImageDraw.Draw(img)
    front, side = (236, 226, 208), (186, 174, 156)
    d.polygon([(x0, y0), (x0 + fw, y0), (x0 + fw, y0 + fh), (x0, y0 + fh)], fill=front)
    d.polygon([(x0 + fw, y0), (x0 + fw + sw, y0 - sw * .35), (x0 + fw + sw, y0 + fh - sw * .35), (x0 + fw, y0 + fh)], fill=side)
    rc, rs = (176, 70, 48), (128, 48, 34)
    d.polygon([(x0 - 24 * s, y0 + 6 * s), (x0 + fw / 2, y0 - rise - 40 * s), (x0 + fw + 24 * s, y0 + 6 * s)], fill=rc)
    d.polygon([(x0 + fw / 2, y0 - rise - 40 * s), (x0 + fw / 2 + sw, y0 - rise - 40 * s - sw * .35), (x0 + fw + sw + 18 * s, y0 - sw * .35 + 4 * s), (x0 + fw + 24 * s, y0 + 6 * s)], fill=rs)
    wl = mix((60, 70, 90), (255, 210, 120), .35 + .65 * glow)
    for wx in (x0 + 30 * s, x0 + fw - 80 * s):
        d.rectangle([wx, y0 + 40 * s, wx + 50 * s, y0 + 90 * s], fill=wl, outline=(90, 80, 70), width=max(2, int(4 * s)))
    d.rectangle([x0 + fw / 2 - 26 * s, y0 + fh - 80 * s, x0 + fw / 2 + 26 * s, y0 + fh], fill=(96, 64, 44))
    if glow > 0:
        gl = Image.new("RGBA", img.size, (0, 0, 0, 0)); g = ImageDraw.Draw(gl)
        for wx in (x0 + 30 * s, x0 + fw - 80 * s): g.ellipse([wx - 30 * s, y0 + 20 * s, wx + 80 * s, y0 + 110 * s], fill=(255, 200, 110, int(60 * glow)))
        img.paste(gl, (0, 0), gl.filter(ImageFilter.GaussianBlur(18)))

def pill(img, cx, cy, ml, en, p, w=360, col=GOLDC):
    if p <= 0: return
    dd = panel(img, (cx - w / 2, cy - 62, cx + w / 2, cy + 62), p, (34, 38, 56), col)
    if dd: dd.text((cx, cy - 16), ml, font=MF(36), fill=WHITE, anchor="mm"); T(dd, cx, cy + 32, en, 24, GOLD2, "s")

def cal(img, cx, cy, p, t):
    """3D calendar block for 2-4 Dec"""
    if p <= 0: return
    s = back(p) if p < 1 else 1; w, h = 360 * s, 320 * s; d = ImageDraw.Draw(img)
    shadow(img, (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), 24, 24, 120, (14, 20)); d = ImageDraw.Draw(img)
    d.polygon([(cx + w / 2, cy - h / 2 + 20), (cx + w / 2 + 24 * s, cy - h / 2 + 6), (cx + w / 2 + 24 * s, cy + h / 2 - 14), (cx + w / 2, cy + h / 2)], fill=(150, 155, 170))
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], int(22 * s), fill=(240, 240, 245))
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy - h / 2 + 80 * s], int(22 * s), fill=REDC); d.rectangle([cx - w / 2, cy - h / 2 + 50 * s, cx + w / 2, cy - h / 2 + 80 * s], fill=REDC)
    if p > .8:
        T(d, cx, cy - h / 2 + 42 * s, "DECEMBER 2026", 30, WHITE, "k")
        for i, dd_ in enumerate(["2", "3", "4"]):
            x = cx - 110 + i * 110; col = REDC if dd_ == "4" else INK
            if dd_ == "4": d.ellipse([x - 44, cy + 6, x + 44, cy + 94], outline=REDC, width=6)
            T(d, x, cy + 50, dd_, 64, col, "k")
        T(d, cx, cy - 40, "RBI MPC", 30, (90, 96, 120), "b")

# ---------------- scenes ----------------
def S1(t):
    s = "S1"; img = base(s, t, 1, (255, 150, 80)); d = ImageDraw.Draw(img)
    house3d(img, 470, 520, 1.5, ease(seg(t, .1, .7)), glow=.5 + .5 * math.sin(t * 1.4) ** 2)
    dd = panel(img, (900, 250, 1760, 640), vis2(t, .3))
    if dd:
        T(dd, 1330, 300, "₹30 LAKH HOME LOAN · 20 YEARS", 28, GREY, "b")
        v = count(0, 1382, t, .4, 2.2); big_num(dd, 1330, 420, f"+{inr(v)}", 140, (255, 130, 115))
        T(dd, 1330, 520, "more EMI every month", 36, WHITE, "s")
        T(dd, 1330, 585, "if all hikes reach your loan (repo to 6%)", 26, GREY, "s")
    if t > ts(s, 1): tag(img, 1330, 720, "RBI: hike on 7 Oct · next decision 4 Dec", t, ts(s, 1), NAVY, WHITE, 34)
    if t > ts(s, 2):
        p = ease(seg(t, ts(s, 2), ts(s, 2) + .6)); d = ImageDraw.Draw(img)
        d.text((W / 2, 128 - 20 * (1 - p)), "ഇ എം ഐ വീണ്ടും കൂടുമോ?", font=MF(72), fill=mix((10, 12, 22), WHITE, p), anchor="mm")
        T(d, W / 2, 196, "WILL YOUR EMI GO UP AGAIN?", 30, mix((10, 12, 22), GOLDC, p), "b")
    if t > ts(s, 3):
        items = [("റിപ്പോ നിരക്ക്", "Repo rate"), ("ലോണിൽ എങ്ങനെ", "How it reaches you"), ("നിശബ്ദ കെണി", "The tenure trap"), ("ഇപ്പോൾ ചെയ്യേണ്ടത്", "What to do now")]
        for i, (ml, en) in enumerate(items):
            pill(img, 300 + i * 440, 860, ml, en, back(seg(t, ts(s, 3) + i * .9, ts(s, 3) + i * .9 + .4)), 400)
    subtitle(img, s, t); return img

def S2(t):
    s = "S2"; img = base(s, t, 2, (120, 150, 255)); head(img, "റിപ്പോ നിരക്ക് എന്താണ്?", "What is the repo rate?", t)
    d = ImageDraw.Draw(img)
    bank(img, 330, 480, 1.15, back(seg(t, ts(s, 1), ts(s, 1) + .5)), "RBI", (230, 232, 240))
    bank(img, 960, 480, 0.95, back(seg(t, ts(s, 1) + 1.0, ts(s, 1) + 1.5)), "YOUR BANK", (200, 210, 235))
    house3d(img, 1580, 480, 1.0, ease(seg(t, ts(s, 2), ts(s, 2) + .6)), glow=.6)
    d = ImageDraw.Draw(img)
    if t > ts(s, 1) + 1.5:
        p = ease(seg(t, ts(s, 1) + 1.5, ts(s, 1) + 2.3)); arrow(d, 520, 400, 760, 400, p, GOLDC, 10, 28)
        if p > .9: T(d, 640, 350, "lends at REPO", 28, GOLD2, "b")
    if t > ts(s, 2) + .8:
        p = ease(seg(t, ts(s, 2) + .8, ts(s, 2) + 1.6)); arrow(d, 1140, 400, 1390, 400, p, REDC, 10, 28)
        if p > .9: T(d, 1265, 350, "cost passed on", 28, (255, 150, 140), "b")
    if t > ts(s, 1) + .5: tag(img, 330, 700, "Repo rate today: 5.50%", t, ts(s, 1) + .5, GOLDC, INK, 34)
    if t > ts(s, 3):
        dd = panel(img, (520, 770, 1400, 890), vis2(t, ts(s, 3)), (24, 28, 42), GOLDC)
        if dd: T(dd, 960, 810, "Since Oct 2019: new floating loans → outside benchmark", 28, WHITE, "b"); T(dd, 960, 855, "Most banks chose the repo rate", 26, GOLD2, "s")
    if t > ts(s, 4): tag(img, 1580, 700, "EBLR / RLLR = repo + spread", t, ts(s, 4), NAVY, WHITE, 30)
    subtitle(img, s, t); return img

def S3(t):
    s = "S3"; img = base(s, t, 3, (90, 200, 140)); head(img, "2025-ൽ കുറഞ്ഞു, 2026-ൽ കൂടി", "Repo rate: down in 2025, up in 2026", t)
    yb = 760; vals = [("Feb 2025", 6.50, GREY, 1), ("Dec 2025", 5.25, GRN, 1), ("7 Oct 2026", 5.50, REDC, 3), ("4 Dec ?", 5.75, (120, 60, 60), 99)]
    def Hh(v): return (v - 4.0) * 170
    for i, (lab, v, col, k) in enumerate(vals):
        tk = ts(s, k) + (i % 2) * 1.2 if k < 99 else 1e9
        p = ease(seg(t, tk, tk + 1.2))
        if p > 0:
            x = 260 + i * 340; bar3d(img, x, yb, 200, Hh(v) * p, col); d = ImageDraw.Draw(img)
            big_num(d, x + 100, yb - Hh(v) * p - 60, f"{v:.2f}%", 50, WHITE); T(d, x + 100, yb + 50, lab, 30, (200, 205, 220), "s")
    if t > ts(s, 3) + 4:  # dashed "?" bar for December
        d = ImageDraw.Draw(img); x = 260 + 3 * 340; h = Hh(5.75)
        for yy in range(int(yb - h), yb, 22): d.line([(x, yy), (x, yy + 10)], fill=(255, 150, 140), width=4); d.line([(x + 200, yy), (x + 200, yy + 10)], fill=(255, 150, 140), width=4)
        d.line([(x, yb - h), (x + 200, yb - h)], fill=(255, 150, 140), width=4); big_num(d, x + 100, yb - h - 60, "5.75%?", 50, (255, 150, 140)); T(d, x + 100, yb + 50, "4 Dec ?", 30, (255, 150, 140), "s")
    if t > ts(s, 1) + 2: tag(img, 700, 250, "−1.25% in 2025 · EMIs fell", t, ts(s, 1) + 2, GRN, WHITE, 32)
    if t > ts(s, 4): tag(img, 1250, 250, "First hike since Feb 2023", t, ts(s, 4), REDC, WHITE, 32)
    if t > ts(s, 5): tag(img, W / 2, 880, "RBI Governor: rate cuts are off the table for now", t, ts(s, 5), NAVY, WHITE, 30)
    subtitle(img, s, t); return img

def S4(t):
    s = "S4"; img = base(s, t, 4, (255, 120, 90)); head(img, "കാരണം: വിലക്കയറ്റം", "The reason: inflation", t)
    d = ImageDraw.Draw(img)
    if t > ts(s, 1):
        z = push(t, ts(s, 1), 8, .04); dd = panel(img, (160, 260, 900, 600), vis2(t, ts(s, 1)))
        if dd:
            T(dd, 530, 305, "RETAIL INFLATION · OCTOBER 2026", 26, GREY, "b")
            v = count(5.54, 6.09, t, ts(s, 1) + .3, ts(s, 1) + 2); big_num(dd, 530, 410, f"{v:.2f}%", int(130 * z), (255, 130, 115))
            T(dd, 530, 500, "24-month high · Sept: 5.54%", 30, WHITE, "s")
    if t > ts(s, 2):  # tolerance band strip
        p = ease(seg(t, ts(s, 2), ts(s, 2) + 1.2)); d = ImageDraw.Draw(img); x0, x1, y = 200, 860, 700
        def X(v): return lerp(x0, x1, v / 8)
        d.rounded_rectangle([x0, y - 16, x0 + (x1 - x0) * p, y + 16], 16, fill=(50, 56, 76))
        if p > .9:
            d.rounded_rectangle([X(2), y - 16, X(6), y + 16], 16, fill=GRN); d.line([(X(4), y - 34), (X(4), y + 34)], fill=WHITE, width=5)
            for v in (0, 2, 4, 6, 8): T(d, X(v), y + 52, f"{v}%", 24, GREY, "s")
            T(d, X(4), y - 56, "target 4%", 26, WHITE, "b"); mk = X(6.09); d.polygon([(mk, y - 26), (mk - 16, y - 54), (mk + 16, y - 54)], fill=REDC)
            T(d, (X(2) + X(6)) / 2, y + 92, "tolerance band 2–6%", 26, (140, 230, 160), "s")
    if t > ts(s, 3):
        dd = panel(img, (1020, 260, 1760, 470), vis2(t, ts(s, 3)), (40, 22, 24), REDC)
        if dd: T(dd, 1390, 300, "FOOD INFLATION", 26, GREY, "b"); big_num(dd, 1390, 385, "8.94%", 96, WHITE)
    items = [("ഉള്ളി", "Onion", "+116%", 3, 1.5), ("വെളുത്തുള്ളി", "Garlic", "+61%", 4, 0), ("ഇഞ്ചി", "Ginger", "+48%", 4, 1.2)]
    for i, (ml, en, v, k, dt) in enumerate(items):
        p = back(seg(t, ts(s, k) + dt, ts(s, k) + dt + .4))
        if p > 0:
            x = 1140 + i * 250; dd = panel(img, (x - 110, 520, x + 110, 720), p, (34, 38, 56), GOLDC)
            if dd: dd.text((x, 560), ml, font=MF(32), fill=WHITE, anchor="mm"); T(dd, x, 600, en, 22, GOLD2, "s"); big_num(dd, x, 660, v, 46, (255, 130, 115))
    if t > ts(s, 5):
        for i, (ml, en) in enumerate([("മോശം മൺസൂൺ", "Weak monsoon"), ("എൽ നിനോ", "El Niño"), ("ഇന്ധനവില", "Energy prices")]):
            pill(img, 1140 + i * 250, 850, ml, en, back(seg(t, ts(s, 5) + i * .8, ts(s, 5) + i * .8 + .4)), 236)
    subtitle(img, s, t); return img

def S5(t):
    s = "S5"; img = base(s, t, 5, (200, 170, 255)); head(img, "ഡിസംബർ 4: എന്ത് പ്രതീക്ഷിക്കാം?", "4 December: what forecasters expect", t)
    cal(img, 330, 540, ease(seg(t, .4, 1.0)), t)
    rows = [("ICRA", "Dec +0.25% “almost certain”", "5.75%", REDC, 1), ("Barclays · Emkay · IDFC First", "Dec + Feb, 0.25% each", "6.00%", REDC, 2), ("SBI Research", "50% chance it stops at", "5.75%", GOLDC, 3)]
    for i, (who, what, v, col, k) in enumerate(rows):
        p = back(seg(t, ts(s, k), ts(s, k) + .5))
        if p > 0:
            y = 310 + i * 150; dd = panel(img, (640, y - 66, 1760, y + 66), p, (24, 28, 42), col)
            if dd: T(dd, 690, y - 22, who, 32, WHITE, "b", "lm"); T(dd, 690, y + 26, what, 28, GREY, "s", "lm"); big_num(dd, 1690, y, v, 64, GOLD2 if col == GOLDC else (255, 140, 125), "rm")
    if t > ts(s, 4): tag(img, 1200, 760, "Brent: over $117 → below $95 · rupee steadier", t, ts(s, 4), NAVY, WHITE, 30)
    if t > ts(s, 5): tag(img, 1200, 845, "Expectations, not certainties", t, ts(s, 5), GOLDC, INK, 32)
    subtitle(img, s, t); return img

def S6(t):
    s = "S6"; img = base(s, t, 6, (120, 150, 255)); head(img, "നിങ്ങളുടെ ലോണിൽ എങ്ങനെ എത്തും?", "How a repo rise reaches your loan", t)
    rows = [("8 OCT", "PNB repo-linked rate", "8.10% → 8.35%", 1, 0), ("8 OCT", "Bank of Baroda BRLLR", "→ 8.15%", 1, 1.6), ("15 OCT", "SBI EBLR +0.25%", "home loans 7.50–8.80%", 2, 0)]
    for i, (dt, who, v, k, dd_) in enumerate(rows):
        p = back(seg(t, ts(s, k) + dd_, ts(s, k) + dd_ + .5))
        if p > 0:
            y = 300 + i * 130; dd = panel(img, (160, y - 55, 1060, y + 55), p, (24, 28, 42), (70, 76, 100))
            if dd:
                dd.rounded_rectangle([180, y - 30, 320, y + 30], 14, fill=REDC); T(dd, 250, y, dt, 28, WHITE, "k")
                T(dd, 350, y, who, 30, WHITE, "b", "lm"); big_num(dd, 1030, y, v, 34, GOLD2, "rm")
    cards = [("റിപ്പോ ലിങ്ക്ഡ്", "Reset: at least every 3 months", GOLDC, 3), ("എം സി എൽ ആർ", "Often reset once a year", BLU, 4), ("ഫിക്സഡ്", "No change in fixed period", GRN, 5)]
    for i, (ml, en, col, k) in enumerate(cards):
        p = back(seg(t, ts(s, k), ts(s, k) + .5))
        if p > 0:
            x = 360 + i * 600; dd = panel(img, (x - 270, 720, x + 270, 880), p, (34, 38, 56), col)
            if dd: dd.text((x, 768), ml, font=MF(40), fill=WHITE, anchor="mm"); T(dd, x, 830, en, 28, GOLD2, "s")
    if t > ts(s, 3) + .8: house3d(img, 1480, 460, 1.0, ease(seg(t, ts(s, 3) + .8, ts(s, 3) + 1.4)), glow=.5)
    subtitle(img, s, t); return img

EMIS = [(7.25, 23711, 0), (7.50, 24168, 457), (7.75, 24628, 917), (8.00, 25093, 1382)]
def S7(t):
    s = "S7"; img = base(s, t, 7, (255, 190, 60)); head(img, "കണക്ക്: ₹30 ലക്ഷം, 20 വർഷം", "Worked example: ₹30 lakh, 20 years left", t)
    yb = 800; labels = ["Before Oct", "After Oct", "If Dec", "If Feb (repo 6%)"]; keys = [1, 2, 3, 4]
    for i, (r, e, dlt) in enumerate(EMIS):
        p = ease(seg(t, ts(s, keys[i]), ts(s, keys[i]) + 1.2))
        if p > 0:
            x = 200 + i * 300; hgt = (e - 20000) * .07 * p + 40; col = mix(GOLDC, REDC, i / 3)
            bar3d(img, x, yb, 190, hgt, col); d = ImageDraw.Draw(img)
            big_num(d, x + 95, yb - hgt - 110, inr(e), 44, WHITE); T(d, x + 95, yb - hgt - 62, f"{r:.2f}%", 30, GOLD2, "b")
            T(d, x + 95, yb + 46, labels[i], 26, (200, 205, 220), "s")
            if dlt and p > .9: tag(img, x + 95, yb - hgt / 2, f"+{inr(dlt)}", t, ts(s, keys[i]) + 1.2, REDC, WHITE, 30)
    if t > ts(s, 5):
        z = push(t, ts(s, 5), 7, .06); dd = panel(img, (1400, 300, 1820, 700), vis2(t, ts(s, 5)), (40, 22, 24), REDC)
        if dd:
            T(dd, 1610, 345, "VS BEFORE OCTOBER", 24, GREY, "b"); big_num(dd, 1610, 440, "+₹1,382", int(80 * z), WHITE); T(dd, 1610, 505, "per month", 30, (255, 200, 190), "s")
            big_num(dd, 1610, 590, "+₹16,584", int(54 * z), GOLD2); T(dd, 1610, 645, "per year", 28, (255, 200, 190), "s")
    if t > ts(s, 6): tag(img, 1610, 790, "Assumes full pass-through", t, ts(s, 6), NAVY, WHITE, 28)
    subtitle(img, s, t); return img

def S8(t):
    s = "S8"; img = base(s, t, 8, (90, 200, 140)); head(img, "വലിയ ലോൺ, വലിയ വർധന", "Bigger loan, bigger rise (7.25% → 8%, 20 years)", t)
    rows = [("₹20 ലക്ഷം", "₹20 lakh", 15808, 16729, 921, 1, 3), ("₹50 ലക്ഷം", "₹50 lakh", 39519, 41822, 2303, 2, 6), ("₹75 ലക്ഷം", "₹75 lakh", 59278, 62733, 3455, 3, 9)]
    for i, (ml, en, a, b, dlt, k, n) in enumerate(rows):
        p = back(seg(t, ts(s, k), ts(s, k) + .5))
        if p > 0:
            x = 380 + i * 580; dd = panel(img, (x - 260, 270, x + 260, 800), p, (24, 28, 42), GOLDC)
            if dd:
                dd.text((x, 320), ml, font=MF(48), fill=WHITE, anchor="mm"); T(dd, x, 370, en, 26, GOLD2, "s")
                coin_stack(img, x, 560, min(n, int(1 + 9 * ease(seg(t, ts(s, k) + .3, ts(s, k) + 1.6)))), 80); dd = ImageDraw.Draw(img)
                T(dd, x, 640, f"{inr(a)} → {inr(b)}", 30, (200, 205, 220), "s"); big_num(dd, x, 720, f"+{inr(dlt)}/mo", 56, (255, 130, 115))
    if t > ts(s, 4): tag(img, W / 2, 880, "Rule of thumb: each 0.25% ≈ +₹15 a month per ₹1 lakh", t, ts(s, 4), GOLDC, INK, 34)
    subtitle(img, s, t); return img

def S9(t):
    s = "S9"; img = base(s, t, 9, (255, 110, 90)); head(img, "നിശബ്ദ കെണി: കാലാവധി നീളുന്നു", "The silent trap: a longer loan", t)
    d = ImageDraw.Draw(img); x0, y = 200, 380; per = 52  # px per year
    if t > ts(s, 0) + 1:
        p = ease(seg(t, ts(s, 0) + 1, ts(s, 0) + 2)); d.rounded_rectangle([x0, y - 34, x0 + 20 * per * p, y + 34], 20, fill=GOLDC)
        if p > .9: T(d, x0 + 10 * per, y, "20 years · EMI ₹23,711", 30, INK, "k")
    if t > ts(s, 3):
        p = ease(seg(t, ts(s, 3), ts(s, 3) + 1.6)); d = ImageDraw.Draw(img)
        d.rounded_rectangle([x0 + 20 * per - 20, y - 34, x0 + 20 * per + 3.26 * per * p, y + 34], 20, fill=REDC)
        if p > .9: tag(img, x0 + 21.6 * per, y - 90, "+39 months", t, ts(s, 3) + 1.6, REDC, WHITE, 36); T(d, x0 + 23.3 * per + 30, y, "≈ 23.3 yrs", 30, (255, 150, 140), "b", "lm")
    if t > ts(s, 2): tag(img, 520, 470, "Same EMI · rate 8%", t, ts(s, 2), NAVY, WHITE, 30)
    for i, (ml, en, v, col, k) in enumerate([("കാലാവധി നീട്ടിയാൽ", "Stretch the term", "+₹9.27 lakh", REDC, 4), ("ഇ എം ഐ കൂട്ടിയാൽ", "Raise the EMI", "+₹3.32 lakh", GRN, 5)]):
        p = back(seg(t, ts(s, k), ts(s, k) + .5))
        if p > 0:
            x = 560 + i * 800; dd = panel(img, (x - 340, 520, x + 340, 740), p, (24, 28, 42), col)
            if dd:
                dd.text((x, 566), ml, font=MF(44), fill=WHITE, anchor="mm"); T(dd, x, 614, en + " · extra paid", 28, GOLD2, "s")
                z = push(t, ts(s, k) + .5, 5, .05); big_num(dd, x, 688, v, int(70 * z), (255, 130, 115) if i == 0 else (140, 230, 160))
    if t > ts(s, 6): tag(img, W / 2, 800, "≈ ₹6 lakh difference", t, ts(s, 6), GOLDC, INK, 40)
    if t > ts(s, 7): tag(img, W / 2, 878, "RBI rule: at reset you can choose EMI up · longer term · fixed rate", t, ts(s, 7), NAVY, WHITE, 28)
    subtitle(img, s, t); return img

def S10(t):
    s = "S10"; img = base(s, t, 10, (120, 150, 255)); head(img, "എഫ് ഡി ഉള്ളവർക്ക്?", "What about fixed deposits?", t)
    yb = 800
    for i, (lab, v, col, k) in enumerate([("New loans", 8.61, REDC, 3), ("New deposits", 5.67, GRN, 3)]):
        tk = ts(s, k) + i * 2.0; p = ease(seg(t, tk, tk + 1.2))
        if p > 0:
            x = 260 + i * 360; hgt = v * 48 * p; bar3d(img, x, yb, 220, hgt, col); d = ImageDraw.Draw(img)
            big_num(d, x + 110, yb - hgt - 60, f"{v * p:.2f}%", 56, WHITE); T(d, x + 110, yb + 46, lab, 30, (200, 205, 220), "s")
    if t > ts(s, 3): tag(img, 590, 250, "Average rates · August · RBI data", t, ts(s, 3), NAVY, WHITE, 28)
    if t > ts(s, 1): tag(img, 1400, 330, "Each bank sets its own FD rate", t, ts(s, 1), GOLDC, INK, 32)
    for i, (ml, en, k) in enumerate([("ഇപ്പോഴുള്ള എഫ് ഡി", "Existing FD: rate fixed till maturity", 4), ("പുതുക്കും മുമ്പ്", "Compare banks before renewing", 5)]):
        p = back(seg(t, ts(s, k), ts(s, k) + .5))
        if p > 0:
            y = 520 + i * 180; dd = panel(img, (1060, y - 70, 1780, y + 70), p, (34, 38, 56), GRN)
            if dd: dd.text((1420, y - 18), ml, font=MF(40), fill=WHITE, anchor="mm"); T(dd, 1420, y + 34, en, 28, GOLD2, "s")
    if t > ts(s, 4): coin_stack(img, 1420, 960 - 30, int(1 + 6 * ease(seg(t, ts(s, 4), ts(s, 4) + 1.5))), 54)
    subtitle(img, s, t); return img

def S11(t):
    s = "S11"; img = base(s, t, 11, (140, 230, 160)); head(img, "ഇപ്പോൾ ചെയ്യാവുന്ന 4 കാര്യങ്ങൾ", "Four things you can do now", t)
    items = [("പലിശ, ബാക്കി, റീസെറ്റ് തീയതി എഴുതുക", "Note your rate, balance, term and reset date", 1), ("കാലാവധി നീട്ടിയോ? ഇ എം ഐ കൂട്ടാം", "Term stretched? Ask to raise the EMI", 2), ("ചെറിയ മുൻകൂർ അടവ്", "Make small prepayments", 3), ("മറ്റ് ബാങ്കുകൾ താരതമ്യം ചെയ്യുക", "Compare lenders, count all fees", 4)]
    for i, (ml, en, k) in enumerate(items):
        p = back(seg(t, ts(s, k), ts(s, k) + .5))
        if p > 0:
            y = 290 + i * 135; x = 960; dd = panel(img, (x - 640, y - 60, x + 640, y + 60), p, (24, 28, 42), GRN)
            if dd:
                dd.ellipse([x - 610, y - 34, x - 542, y + 34], fill=GRN); T(dd, x - 576, y, str(i + 1), 40, WHITE, "k")
                dd.text((x - 500, y - 14), ml, font=MF(40), fill=WHITE, anchor="lm"); T(dd, x - 500, y + 32, en, 26, GOLD2, "s", "lm")
    if t > ts(s, 5): tag(img, W / 2, 860, "Education only · not financial advice", t, ts(s, 5), NAVY, WHITE, 32)
    subtitle(img, s, t); return img

def S12(t):
    s = "S12"; img = base(s, t, 12, (255, 190, 60)); head(img, "മുൻകൂർ അടവിന്റെ ശക്തി", "The power of prepayment", t)
    if t > ts(s, 1):
        coin_stack(img, 420, 620, int(1 + 11 * ease(seg(t, ts(s, 1), ts(s, 1) + 2))), 110); d = ImageDraw.Draw(img)
        T(d, 420, 700, "Prepay ₹1 lakh now", 36, WHITE, "b"); T(d, 420, 748, "₹30 lakh · 8% · same EMI", 28, GREY, "s")
    if t > ts(s, 1) + 2: arrow(ImageDraw.Draw(img), 640, 450, 880, 450, ease(seg(t, ts(s, 1) + 2, ts(s, 1) + 2.8)), GOLDC, 12, 30)
    if t > ts(s, 2):
        dd = panel(img, (940, 240, 1780, 420), vis2(t, ts(s, 2)), (24, 28, 42), GRN)
        if dd: T(dd, 1360, 280, "LOAN ENDS SOONER BY", 26, GREY, "b"); big_num(dd, 1360, 355, "≈ 18.5 months", 76, (140, 230, 160))
    if t > ts(s, 3):
        z = push(t, ts(s, 3), 6, .06); dd = panel(img, (940, 450, 1780, 650), vis2(t, ts(s, 3)), (24, 28, 42), GOLDC)
        if dd: T(dd, 1360, 492, "INTEREST SAVED", 26, GREY, "b"); big_num(dd, 1360, 578, "≈ ₹3.65 lakh", int(84 * z), GOLD2)
    if t > ts(s, 4): tag(img, 1360, 710, "Interest is heaviest in the early years", t, ts(s, 4), NAVY, WHITE, 30)
    if t > ts(s, 5): tag(img, W / 2, 850, "RBI: no prepayment penalty on floating-rate home loans (individuals)", t, ts(s, 5), GRN, WHITE, 28)
    subtitle(img, s, t); return img

def S13(t):
    s = "S13"; img = base(s, t, 13); head(img, "ചുരുക്കത്തിൽ", "In short", t)
    for i, (ml, en, t0) in enumerate([("വിലക്കയറ്റം 6% കടന്നു", "Inflation above 6%", ts(s, 0) + .6), ("4 ഡിസംബർ: വീണ്ടും കൂടാം", "Another hike likely 4 Dec", ts(s, 0) + 2.2), ("കാലാവധി കെണി ശ്രദ്ധിക്കുക", "Watch the tenure trap", ts(s, 1))]):
        pill(img, 380 + i * 580, 300, ml, en, back(seg(t, t0, t0 + .4)), 520)
    if t > ts(s, 2): tag(img, 960, 470, "calcsouq.com/loan-emi-calculator", t, ts(s, 2), GOLDC, INK, 50)
    if t > ts(s, 3):
        dd = panel(img, (460, 560, 1460, 720), vis2(t, ts(s, 3)))
        if dd: dd.text((960, 610), "നിങ്ങളുടെ ലോൺ പലിശ എത്ര?", font=MF(46), fill=WHITE, anchor="mm"); T(dd, 960, 675, "Tell us in the comments", 32, GOLD2, "s")
    if t > ts(s, 3) + 3:
        p = back(seg(t, ts(s, 3) + 3, ts(s, 3) + 3.4)); bw, bh = 420 * p, 104 * p; cx, cy = 960, 820; d = ImageDraw.Draw(img)
        d.rounded_rectangle([cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2], int(28 * p), fill=(230, 33, 23))
        if p > .8: T(d, cx + 26, cy, "SUBSCRIBE", 48, WHITE, "k"); G.R.bell(d, cx - 150, cy - 6, 0.75)
    subtitle(img, s, t); return img

SCENES = {k: globals()[k] for k in ORDER}

def render(s, out_dir="/tmp/yte"):
    os.makedirs(out_dir, exist_ok=True); out = f"{out_dir}/{s}.mp4"; tmp = f"{out_dir}/{s}.tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-r", str(FPS), tmp], stdin=subprocess.PIPE)
    n = round(L(s) * FPS)
    for i in range(n): p.stdin.write(SCENES[s](i / FPS).convert("RGB").tobytes())
    p.stdin.close(); assert p.wait() == 0; os.replace(tmp, out); print(out, n / FPS, flush=True)

def timeline():
    """scene start times in the final video, including B-roll after the listed scenes"""
    off, out = 0.0, {}
    for s in ORDER:
        out[s] = off; off += round(L(s) * FPS) / FPS
        off += BROLL.get(s, 0.0)
    return out, off

def write_srt(path, lang):
    def stamp(x): h, r = divmod(x, 3600); m, sec = divmod(r, 60); return f"{int(h):02}:{int(m):02}:{int(sec):02},{int(round((sec % 1) * 1000)) % 1000:03}"
    st, _ = timeline(); n, out = 1, []
    for s in ORDER:
        for k, (m, e) in enumerate(SC[s]):
            t0 = ts(s, k); t1 = ts(s, k + 1) if k + 1 < len(SC[s]) else AUDIO[s] + 0.3
            out.append(f"{n}\n{stamp(st[s] + t0)} --> {stamp(st[s] + t1)}\n{e if lang == 'en' else m}\n"); n += 1
    open(path, "w").write("\n".join(out)); print(path, n - 1)

if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "--frame": SCENES[a[1]](float(a[2])).convert("RGB").save(a[3])
    elif a and a[0] in ("--srt-en", "--srt-ml"): write_srt(a[1], a[0][-2:])
    elif a and a[0] == "--timeline": print(json.dumps(timeline(), indent=1))
    else:
        for s in a: render(s)
