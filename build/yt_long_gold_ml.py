"""CalcSouq Malayalam long video: why gold is falling, gold loans, what next (16:9, 1920x1080).
Malayalam narration (ElevenLabs), Malayalam headings, burned-in English subtitles (sentence pairs in scenes.json).
Usage: python3 yt_long_gold_ml.py S1 S2 ... | --frame S3 10 out.png | --srt-en out.srt | --srt-ml out.srt
"""
import sys, os, math, json, random, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import yt_long_rates as R
from yt_long_rates import fx, F, INK, GOLD, WHITE, OFF, RED, GREEN, BLUE, ORANGE, seg, ease, back, lerp, mix, clamp, count
from yt_long_rates import card, T, wrap, arrow, up_arrow, bank, house, loan_doc, shadow
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W, H, FPS = 1920, 1080, 30
HERE = os.path.dirname(os.path.abspath(__file__))
SC = json.load(open(os.path.join(HERE, "youtube/long/2026-11-22-gold-fall-malayalam/scenes.json")))
ORDER = list(SC.keys())
AUDIO = {k: 30.0 for k in ORDER}
AUDIO.update({"S1": 27.2, "S2": 38.24, "S3": 22.8, "S4": 25.92, "S5": 26.96, "S6": 20.4, "SH": 25.52, "SW": 26.16, "S7": 34.48, "S8": 36.88, "S9": 28.08, "S10": 26.88, "S11": 34.64, "S12": 25.44})
if os.path.exists("/tmp/ytg/audio.json"): AUDIO.update(json.load(open("/tmp/ytg/audio.json")))
PAD = 0.45
END_EXTRA = 0.067  # extra hold on the last scene so the video matches the music length
def L(s): return AUDIO[s] + PAD + (END_EXTRA if s == ORDER[-1] else 0)

_MLF = {}
def MF(size):
    if size not in _MLF: _MLF[size] = ImageFont.truetype(os.path.join(HERE, "fonts/Manjari-Bold.ttf"), int(size), layout_engine=ImageFont.Layout.RAQM)
    return _MLF[size]
GOLDC = (240, 190, 60); GOLD2 = (255, 214, 102); DGOLD = (170, 120, 20)

def ts(s, k):
    """start time of sentence k in scene s (by Malayalam character share)"""
    lens = [len(m) + 1 for m, _ in SC[s]]; tot = sum(lens)
    return AUDIO[s] * sum(lens[:k]) / tot

# ---------- premium background ----------
_BG = {}
def bg(t, seed=1, tint=(245, 190, 60)):
    key = (seed, tint)
    if key not in _BG:
        im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im)
        for y in range(H):
            p = y / H; d.line([(0, y), (W, y)], fill=(int(10 + 8 * p), int(12 + 8 * p), int(22 + 16 * p)))
        gl = Image.new("L", (W, H), 0); ImageDraw.Draw(gl).ellipse([W * .45, -H * .4, W * 1.3, H * .9], fill=70)
        im.paste(tint, (0, 0), gl.filter(ImageFilter.GaussianBlur(220)))
        gr = Image.new("RGBA", (W, H), (0, 0, 0, 0)); g = ImageDraw.Draw(gr)
        for x in range(0, W, 96): g.line([(x, 0), (x, H)], fill=(160, 170, 200, 14))
        for y in range(0, H, 96): g.line([(0, y), (W, y)], fill=(160, 170, 200, 14))
        im.paste(gr, (0, 0), gr); _BG[key] = im
    img = _BG[key].copy()
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov); rnd = random.Random(seed)
    for k in range(26):  # drifting gold dust
        x = (rnd.random() * W + t * (8 + 14 * rnd.random())) % W; y = (rnd.random() * H - t * (10 + 18 * rnd.random())) % H
        r = 1.5 + rnd.random() * 3.5; a = int(40 + 60 * (0.5 + 0.5 * math.sin(t * 1.3 + k)))
        od.ellipse([x - r, y - r, x + r, y + r], fill=(255, 210, 110, a))
    img.paste(ov, (0, 0), ov)
    return img

def head(img, ml, en, t, t0=0.1):
    p = ease(seg(t, t0, t0 + .6)); d = ImageDraw.Draw(img)
    if p <= 0: return
    y = 112 + 20 * (1 - p); col = mix((10, 12, 22), WHITE, p)
    d.text((W / 2, y), ml, font=MF(66), fill=col, anchor="mm")
    d.text((W / 2, y + 62), en.upper(), font=F("b", 28), fill=mix((10, 12, 22), GOLDC, p), anchor="mm")
    d.rounded_rectangle([W / 2 - 50, y + 88, W / 2 + 50, y + 93], 3, fill=mix((10, 12, 22), GOLDC, p))

def brand(img):
    d = ImageDraw.Draw(img); d.rounded_rectangle([40, 32, 236, 82], 25, fill=GOLDC); T(d, 138, 57, "CalcSouq", 28, INK, "k")

def gold_bar(img, cx, cy, s=1.0, p=1.0, dim=0.0):
    if p <= 0.01: return
    s *= back(p) if p < 1 else 1; d = ImageDraw.Draw(img)
    w, h, top = 230 * s, 90 * s, 160 * s
    shadow(img, (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), 10, 18, 90, (0, 14)); d = ImageDraw.Draw(img)
    base = mix(GOLDC, (90, 70, 40), dim); hi = mix(GOLD2, (120, 100, 60), dim); lo = mix(DGOLD, (60, 50, 30), dim)
    d.polygon([(cx - w / 2, cy + h / 2), (cx + w / 2, cy + h / 2), (cx + top / 2, cy - h / 2), (cx - top / 2, cy - h / 2)], fill=base)
    d.polygon([(cx - top / 2, cy - h / 2), (cx + top / 2, cy - h / 2), (cx + top / 2 - 14 * s, cy - h / 2 + 18 * s), (cx - top / 2 + 14 * s, cy - h / 2 + 18 * s)], fill=hi)
    d.polygon([(cx + top / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx + w / 2 - 22 * s, cy + h / 2), (cx + top / 2 - 14 * s, cy - h / 2 + 18 * s)], fill=lo)
    if s > .5: d.text((cx, cy + 12 * s), "999.9", font=F("k", 26 * s), fill=mix(DGOLD, (50, 40, 20), dim), anchor="mm")

def gold_stack(img, cx, cy, n, s=0.7, dim=0.0):
    pos = [(0, 0), (-1, 0), (1, 0), (-.5, -1), (.5, -1), (0, -2)]
    for i in range(int(n)):
        dx, dy = pos[i]; gold_bar(img, cx + dx * 220 * s, cy + dy * 92 * s, s, 1, dim)

def panel(img, box, p, fill=(24, 28, 42), outline=(70, 76, 100), r=28):
    if p <= 0.01: return None
    cx, cy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2; w, h = (box[2] - box[0]) * p, (box[3] - box[1]) * p
    b = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2); shadow(img, b, r, 26, 120, (0, 16)); d = ImageDraw.Draw(img)
    d.rounded_rectangle(b, int(r * p), fill=fill, outline=outline, width=2)
    return d if p > 0.8 else None

def tag(img, cx, cy, text, t, t0, bg=GOLDC, fg=INK, size=40, ml=False):
    p = back(seg(t, t0, t0 + .4))
    if p <= 0: return
    d = ImageDraw.Draw(img); f = MF(size) if ml else F("b", size); tw = d.textlength(text, font=f); w = (tw + 64) * p; h = (size + 38) * p
    box = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2); shadow(img, box, int(h / 2), 14, 90, (0, 8)); d = ImageDraw.Draw(img)
    d.rounded_rectangle(box, int(h / 2), fill=bg)
    if p > .8: d.text((cx, cy + (4 if ml else 0)), text, font=f, fill=fg, anchor="mm")

def big_num(d, x, y, text, size, col, anchor="mm"):
    d.text((x, y), text, font=F("k", size), fill=col, anchor=anchor)

def inr(v): # Indian grouping
    s = f"{int(round(v))}";
    if len(s) <= 3: return "₹" + s
    head_, tail = s[:-3], s[-3:]; parts = []
    while len(head_) > 2: parts.insert(0, head_[-2:]); head_ = head_[:-2]
    if head_: parts.insert(0, head_)
    return "₹" + ",".join(parts) + "," + tail

def subtitle(img, s, t):
    for k, (m, e) in enumerate(SC[s]):
        t0 = ts(s, k) - 0.05; t1 = ts(s, k + 1) - 0.05 if k + 1 < len(SC[s]) else AUDIO[s] + 0.4
        if t0 <= t < t1:
            d = ImageDraw.Draw(img); f = F("s", 40); lines = wrap(d, e, f, 1500)
            hh = 54 * len(lines) + 26; tw = max(d.textlength(l, font=f) for l in lines)
            box = (int(W / 2 - tw / 2 - 34), int(1050 - hh), int(W / 2 + tw / 2 + 34), 1050)
            reg = img.crop(box); m_ = Image.new("L", reg.size, 0); ImageDraw.Draw(m_).rounded_rectangle([0, 0, reg.size[0] - 1, reg.size[1] - 1], 18, fill=255)
            img.paste(Image.blend(reg, Image.new("RGB", reg.size, (0, 0, 0)), 0.68), box[:2], m_); d = ImageDraw.Draw(img)
            for j, l in enumerate(lines): d.text((W / 2, box[1] + 13 + 27 + j * 54), l, font=f, fill=WHITE, anchor="mm")
            return

def frame_base(s, t, seed, tint=(245, 190, 60)):
    img = bg(t, seed, tint); brand(img); return img

# =========================== scenes ===========================
def S1(t):
    s = "S1"; img = frame_base(s, t, 1); head(img, "സ്വർണ്ണവില കുത്തനെ താഴേക്ക്", "Gold price crash explained", t)
    d = panel(img, (180, 260, 940, 640), vis2(t, .4))
    if d:
        T(d, 560, 315, "1 PAVAN (8 g) · 22K · KERALA", 28, (170, 175, 195), "b")
        v = count(131000, 91720, t, ts(s, 1), ts(s, 1) + 2.2) if t > ts(s, 1) else 131000
        big_num(d, 560, 430, inr(v), 120, GOLD2 if t < ts(s, 1) else mix(GOLD2, (255, 120, 110), ease(seg(t, ts(s, 1), ts(s, 1) + 2.2))))
        T(d, 560, 525, "Jan record: over ₹1,31,000" if t < ts(s, 1) + .3 else "21 Nov: ₹91,720", 34, (200, 205, 220), "s")
    if t > ts(s, 2): tag(img, 560, 690, "−₹39,480 per pavan (−30%)", t, ts(s, 2), (220, 60, 60), WHITE, 40)
    shrink = 6 - 3 * ease(seg(t, ts(s, 1), ts(s, 1) + 2.2)); gold_stack(img, 1420, 560, round(shrink), 0.8, 0.0)
    t3 = ts(s, 3)
    if t > t3:
        for i, (ml, en) in enumerate([("വീട്ടിലെ സ്വർണ്ണം", "Gold at home"), ("കല്യാണ സ്വർണ്ണം", "Wedding buyers"), ("ഗോൾഡ് ലോൺ", "Gold loans")]):
            p = back(seg(t, t3 + i * .5, t3 + i * .5 + .4))
            if p > 0:
                x = 400 + i * 560; dd = panel(img, (x - 230, 770, x + 230, 890), p, (34, 38, 56), GOLDC)
                if dd: dd.text((x, 812), ml, font=MF(40), fill=WHITE, anchor="mm"); dd.text((x, 862), en, font=F("s", 26), fill=GOLD2, anchor="mm")
    subtitle(img, s, t); return img

def vis2(t, a, b=1e9): return min(ease(seg(t, a, a + .5)), 1 - ease(seg(t, b, b + .35)))

def S2(t):
    s = "S2"; img = frame_base(s, t, 2); head(img, "കണക്കുകൾ നോക്കാം", "The numbers", t)
    d = ImageDraw.Draw(img); x0, x1, y0, y1 = 200, 1150, 290, 760
    pts = [(0, 4300), (.04, 5589), (.12, 4780), (.3, 4700), (.5, 4500), (.7, 4100), (.82, 3990), (.9, 3868), (1, 3520)]
    def Y(v): return lerp(y1, y0, (v - 3000) / (6000 - 3000))
    for v in (3500, 4500, 5500):
        d.line([(x0, Y(v)), (x1, Y(v))], fill=(70, 76, 100), width=1); T(d, x0 - 16, Y(v), f"${v:,}", 26, (160, 165, 185), "s", "rm")
    p = ease(seg(t, ts(s, 1), ts(s, 2) + 2.5)); n = p * (len(pts) - 1); k = int(n)
    path = [(lerp(x0, x1, a), Y(v)) for a, v in pts[:k + 1]]
    if k < len(pts) - 1:
        a0, v0 = pts[k]; a1, v1 = pts[k + 1]; path.append((lerp(x0, x1, lerp(a0, a1, n - k)), Y(lerp(v0, v1, n - k))))
    if len(path) > 1: d.line(path, fill=GOLDC if n < 1.5 else (240, 110, 90), width=9, joint="curve")
    T(d, x0, y1 + 34, "Jan 2026", 26, (160, 165, 185), "s", "lm"); T(d, x1, y1 + 34, "20 Nov", 26, (160, 165, 185), "s", "rm")
    T(d, x1, y0 - 24, "Spot gold $/oz (path approximate)", 22, (150, 155, 175), "s", "rm")
    if t > ts(s, 1): tag(img, 380, 270, "Record $5,589 · 28 Jan", t, ts(s, 1), GOLDC, INK, 30)
    if t > ts(s, 2): tag(img, 1020, 800, "≈ $3,520 · 20 Nov", t, ts(s, 2), (220, 60, 60), WHITE, 30)
    if t > ts(s, 3): tag(img, 700, 560, "−36%", t, ts(s, 3), (220, 60, 60), WHITE, 60)
    if t > ts(s, 4): tag(img, 700, 660, "Last week −9.5% · worst in 8 months", t, ts(s, 4), (40, 44, 60), WHITE, 28)
    dd = panel(img, (1260, 300, 1760, 760), vis2(t, ts(s, 5) - .3))
    if dd:
        dd.text((1510, 350), "കേരളം · 1 പവൻ", font=MF(40), fill=WHITE, anchor="mm")
        T(dd, 1510, 430, "1 Nov", 30, (170, 175, 195), "s"); big_num(dd, 1510, 485, "₹1,01,840", 64, GOLD2)
        if t > ts(s, 6): T(dd, 1510, 570, "21 Nov", 30, (170, 175, 195), "s"); big_num(dd, 1510, 625, "₹91,720", 64, (255, 130, 115))
        if t > ts(s, 7): T(dd, 1510, 710, "−₹10,120 in one month", 32, (255, 150, 140), "b")
    subtitle(img, s, t); return img

def S3(t):
    s = "S3"; img = frame_base(s, t, 3, (120, 150, 255)); head(img, "കാരണം 1: അമേരിക്കൻ ഫെഡ്", "Reason 1: the US Federal Reserve", t)
    bank(img, 520, 560, 1.25, vis2(t, .3), "Federal Reserve")
    d = ImageDraw.Draw(img)
    if t > ts(s, 1):
        tag(img, 1300, 330, "US inflation still high", t, ts(s, 1), (220, 60, 60), WHITE, 34)
        R.thermo(img, 1680, 520, 0.8, 0.85, vis2(t, ts(s, 1)), (230, 70, 60))
    if t > ts(s, 2): tag(img, 1300, 450, "Fix: raise interest rates", t, ts(s, 2), GOLDC, INK, 34)
    if t > ts(s, 3):
        dd = panel(img, (980, 520, 1560, 760), vis2(t, ts(s, 3)), (240, 240, 235), None, 18)
        if dd:
            dd.text((1270, 570), "FED MINUTES · 18 NOV", font=F("k", 30), fill=INK, anchor="mm")
            f = F("s", 30)
            for j, l in enumerate(wrap(dd, "“Almost all participants” saw further rate increases as likely appropriate", f, 520)): dd.text((1270, 625 + j * 40), l, font=f, fill=(60, 64, 74), anchor="mm")
    if t > ts(s, 4): tag(img, 1270, 830, "December hike: almost certain", t, ts(s, 4), (220, 60, 60), WHITE, 38)
    subtitle(img, s, t); return img

def S4(t):
    s = "S4"; img = frame_base(s, t, 4); head(img, "പലിശ കൂടിയാൽ സ്വർണ്ണം എന്തിന് കുറയണം?", "Why higher rates hurt gold", t)
    t2 = ts(s, 2)
    dl = panel(img, (200, 270, 900, 760), vis2(t, t2 - .2))
    if dl:
        dl.text((550, 320), "ബാങ്ക് നിക്ഷേപം", font=MF(46), fill=WHITE, anchor="mm"); T(dl, 550, 368, "BANK DEPOSIT", 26, GOLD2, "b")
        big_num(dl, 550, 450, "₹1,00,000", 76, WHITE)
        if t > ts(s, 3):
            n = int(clamp((t - ts(s, 3)) * 2.5, 0, 6)); dd = ImageDraw.Draw(img)
            for k in range(n): fx.coin(dd, 400 + k * 60, 580, 26, GOLDC, "%")
            T(dd, 550, 680, "+ interest every year", 34, (140, 230, 160), "b")
    dr = panel(img, (1020, 270, 1720, 760), vis2(t, ts(s, 4) - .2))
    if dr:
        dr.text((1370, 320), "ലോക്കറിലെ സ്വർണ്ണം", font=MF(46), fill=WHITE, anchor="mm"); T(dr, 1370, 368, "GOLD IN A LOCKER", 26, GOLD2, "b")
        gold_bar(img, 1370, 500, 0.9, 1); dd = ImageDraw.Draw(img); T(dd, 1370, 680, "0 interest", 40, (255, 130, 115), "k")
    if t > ts(s, 6): tag(img, 960, 830, "US 10-year bond ≈ 5%", t, ts(s, 6), GOLDC, INK, 38)
    if t > ts(s, 7):
        dd = ImageDraw.Draw(img); arrow(dd, 1240, 600, 860, 600, ease(seg(t, ts(s, 7), ts(s, 7) + .8)), (255, 210, 110), 10)
        T(dd, 1050, 560, "money moves to bonds", 28, WHITE, "b")
    subtitle(img, s, t); return img

def S5(t):
    s = "S5"; img = frame_base(s, t, 5, (90, 200, 140)); head(img, "കാരണം 2, 3: ഡോളർ, ഓഹരി തകർച്ച", "Reasons 2 and 3: strong dollar, stock crash", t)
    t4 = ts(s, 4)
    if t < t4 + .3:
        p = vis2(t, .3, t4); d = ImageDraw.Draw(img)
        if p > .05:
            r = 170 * p; d.ellipse([520 - r, 560 - r, 520 + r, 560 + r], fill=(40, 120, 80), outline=(140, 230, 160), width=6)
            if p > .6: d.text((520, 560), "$", font=F("k", int(220 * p)), fill=WHITE, anchor="mm")
            if t > ts(s, 3): up_arrow(d, 760, 470, 1.3 * p, (140, 230, 160))
        if t > ts(s, 1): tag(img, 1290, 380, "Gold is priced in dollars", t, ts(s, 1), (40, 44, 60), WHITE, 36)
        if t > ts(s, 2): tag(img, 1290, 500, "Strong $ → gold dearer abroad", t, ts(s, 2), (40, 44, 60), WHITE, 36)
        if t > ts(s, 3): tag(img, 1290, 640, "Dollar ≈ 19-month high", t, ts(s, 3), GOLDC, INK, 44)
    else:
        p = vis2(t, t4); R_chip(img, 520, 560, 1.4 * p + 1e-3, ease(seg(t, t4 + .5, t4 + 1.5)))
        d = ImageDraw.Draw(img)
        if p > .5:
            pts = [(700, 380), (780, 420), (850, 520), (920, 600), (1000, 760)]; q = ease(seg(t, t4 + .4, t4 + 2)); n = q * 4; k = int(n); path = pts[:k + 1]
            if k < 4: path.append((lerp(pts[k][0], pts[k + 1][0], n - k), lerp(pts[k][1], pts[k + 1][1], n - k)))
            if len(path) > 1: d.line(path, fill=(240, 80, 70), width=12)
        if t > ts(s, 5):
            tag(img, 1420, 430, "AI stocks crash (Nvidia −47%)", t, ts(s, 5), (220, 60, 60), WHITE, 34)
            gold_bar(img, 1420, 620, 0.8, vis2(t, ts(s, 5) + .8)); dd = ImageDraw.Draw(img)
            if t > ts(s, 5) + 1.4: T(dd, 1420, 740, "investors sell gold to cover losses", 32, WHITE, "b")
    subtitle(img, s, t); return img

def R_chip(img, cx, cy, s, red=0.0):
    d = ImageDraw.Draw(img); body = mix((40, 44, 56), (130, 30, 40), red)
    for k in range(5):
        o = -80 + k * 40
        for (x1, y1, x2, y2) in [(cx + o * s, cy - 150 * s, cx + o * s, cy - 110 * s), (cx + o * s, cy + 110 * s, cx + o * s, cy + 150 * s),
                                 (cx - 150 * s, cy + o * s, cx - 110 * s, cy + o * s), (cx + 110 * s, cy + o * s, cx + 150 * s, cy + o * s)]:
            d.line([(x1, y1), (x2, y2)], fill=(210, 180, 100), width=max(2, int(10 * s)))
    d.rounded_rectangle([cx - 120 * s, cy - 120 * s, cx + 120 * s, cy + 120 * s], int(22 * s), fill=body, outline=(110, 115, 130), width=5)
    d.rounded_rectangle([cx - 75 * s, cy - 75 * s, cx + 75 * s, cy + 75 * s], int(14 * s), fill=(200, 202, 210))
    if s > .3: d.text((cx, cy), "AI", font=F("k", 64 * s), fill=INK, anchor="mm")

def S6(t):
    s = "S6"; img = frame_base(s, t, 6); head(img, "കേരളത്തിലെ സ്വർണ്ണവില", "How Kerala's price is set", t)
    t2 = ts(s, 2)
    if t > t2:
        items = [("World price ($ / oz)", t2), ("×", t2 + .6), ("₹ per $", t2 + 1.0), ("=", ts(s, 3)), ("Kerala price", ts(s, 3) + .4)]
        x = 330
        for txt, t0 in items:
            w = 360 if len(txt) > 2 else 80; p = back(seg(t, t0, t0 + .4))
            if p > 0:
                if len(txt) > 2:
                    dd = panel(img, (x, 400, x + w, 540), p, (34, 38, 56), GOLDC)
                    if dd: T(dd, x + w / 2, 470, txt, 36, WHITE, "b")
                else: T(ImageDraw.Draw(img), x + w / 2, 470, txt, 80, GOLD2, "k")
            x += w + 20
    if t > ts(s, 4): tag(img, 960, 640, "Stronger rupee → lower price here", t, ts(s, 4), (40, 44, 60), WHITE, 36)
    if t > ts(s, 5): tag(img, 960, 780, "Kerala pavan: about −30% from January record", t, ts(s, 5), (220, 60, 60), WHITE, 40)
    subtitle(img, s, t); return img

def SH(t):
    s = "SH"; img = frame_base(s, t, 7); head(img, "ഇതാദ്യമല്ല", "Gold has crashed before", t)
    d = ImageDraw.Draw(img); x0, x1, y0, y1 = 220, 1700, 300, 760
    yrs = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, "Jan 26", "Nov 26"]
    vals = [1421, 1531, 1675, 1202, 1184, 1061, 1146, 1303, 1282, 1517, 1898, 1829, 1824, 2063, 2624, 4300, 5589, 3520]
    def X(i): return lerp(x0, x1, i / (len(yrs) - 1))
    def Y(v): return lerp(y1, y0, math.log(v / 900) / math.log(6200 / 900))
    for i, y in enumerate(yrs):
        if i % 2 == 0 or i == len(yrs) - 1: T(d, X(i), y1 + 30, str(y), 24, (160, 165, 185), "s")
    p = ease(seg(t, 0.6, ts(s, 3) + 2)); n = p * (len(yrs) - 1); k = int(n)
    path = [(X(i), Y(v)) for i, v in enumerate(vals[:k + 1])]
    if k < len(yrs) - 1: path.append((lerp(X(k), X(k + 1), n - k), lerp(Y(vals[k]), Y(vals[k + 1]), n - k)))
    if len(path) > 1: d.line(path, fill=GOLDC, width=8, joint="curve")
    if t > ts(s, 1) and n > 3: tag(img, X(3) + 60, Y(1900) - 40, "2013: −28% in a year", t, ts(s, 1), (220, 60, 60), WHITE, 30)
    if t > ts(s, 2) and n > 10: tag(img, X(10) - 40, Y(2060) - 90, "2020: 2011 record finally beaten", t, ts(s, 2), GOLDC, INK, 28)
    if t > ts(s, 4): tag(img, 960, 860, "Long-term holders: patience · Short-term loans: no such time", t, ts(s, 4), (40, 44, 60), WHITE, 30)
    T(d, x1, y0 - 20, "Gold $/oz, year-end prices, approx. (log scale)", 22, (150, 155, 175), "s", "rm")
    subtitle(img, s, t); return img

def SW(t):
    s = "SW"; img = frame_base(s, t, 8, (255, 150, 170)); head(img, "കല്യാണത്തിന് സ്വർണ്ണം വാങ്ങുന്നവർക്ക്", "For wedding gold buyers", t)
    dd = panel(img, (200, 280, 900, 700), vis2(t, ts(s, 1) - .3))
    if dd:
        dd.text((550, 330), "10 പവൻ", font=MF(54), fill=WHITE, anchor="mm")
        T(dd, 550, 420, "January", 30, (170, 175, 195), "s"); big_num(dd, 550, 475, "₹13.1 lakh+", 66, GOLD2)
        if t > ts(s, 2):
            T(dd, 550, 570, "Today (21 Nov)", 30, (170, 175, 195), "s"); v = count(1310000, 917200, t, ts(s, 2), ts(s, 2) + 1.8)
            big_num(dd, 550, 625, inr(v), 66, (140, 230, 160))
    if t > ts(s, 4):
        d = ImageDraw.Draw(img)
        for k in range(4):
            p = back(seg(t, ts(s, 4) + k * .35, ts(s, 4) + k * .35 + .4))
            if p > 0.05: fx.calendar(d, 1100 + k * 170, 470, 0.55 * p, ["M1", "M2", "M3", "M4"][k])
        T(d, 1355, 620, "buy in stages", 38, WHITE, "k")
    if t > ts(s, 3): tag(img, 1355, 330, "Nobody knows the lowest day", t, ts(s, 3), (40, 44, 60), WHITE, 32)
    if t > ts(s, 5): tag(img, 960, 800, "Add making charges + 3% GST", t, ts(s, 5), GOLDC, INK, 40)
    subtitle(img, s, t); return img

def S7(t):
    s = "S7"; img = frame_base(s, t, 9); head(img, "ഗോൾഡ് ലോൺ: ശ്രദ്ധിക്കുക", "Gold loans: what to know", t)
    loan_doc(img, 420, 470, 1.5, vis2(t, .3), "LOAN", (200, 150, 40)); gold_bar(img, 420, 690, 0.7, vis2(t, .6))
    if t > ts(s, 2): tag(img, 420, 820, "Bank gold loans +125% in a year (to Nov 2025)", t, ts(s, 2), (40, 44, 60), WHITE, 28)
    if t > ts(s, 3): tag(img, 1270, 300, "LTV = loan ÷ gold value", t, ts(s, 3), GOLDC, INK, 40)
    rows = [("Loan up to ₹2.5 lakh", 85, ts(s, 4)), ("₹2.5 – 5 lakh", 80, ts(s, 5)), ("Above ₹5 lakh", 75, ts(s, 5) + 1.2)]
    for i, (lab, v, t0) in enumerate(rows):
        if t > t0:
            d = ImageDraw.Draw(img); y = 420 + i * 130; p = ease(seg(t, t0, t0 + 1))
            T(d, 900, y - 30, lab, 32, WHITE, "b", "lm"); d.rounded_rectangle([900, y, 1660, y + 50], 25, fill=(40, 44, 60))
            d.rounded_rectangle([900, y, 900 + 760 * v / 100 * p, y + 50], 25, fill=GOLDC)
            if p > .9: T(d, 900 + 760 * v / 100 - 20, y + 25, f"max {v}%", 30, INK, "k", "rm")
    if t > ts(s, 4): T(ImageDraw.Draw(img), 1280, 800, "RBI rules from 1 April 2026", 28, (170, 175, 195), "s")
    subtitle(img, s, t); return img

def S8(t):
    s = "S8"; img = frame_base(s, t, 10); head(img, "ഒരു ഉദാഹരണം", "A worked example", t)
    dl = panel(img, (160, 260, 880, 640), vis2(t, ts(s, 1) - .3))
    if dl:
        dl.text((520, 305), "ജനുവരി", font=MF(46), fill=WHITE, anchor="mm")
        T(dl, 520, 375, "5 pavan × ₹1,30,000", 36, (200, 205, 220), "s")
        if t > ts(s, 2): big_num(dl, 520, 450, "Gold ₹6,50,000", 54, GOLD2)
        if t > ts(s, 3): big_num(dl, 520, 540, "Loan ₹4,50,000", 54, WHITE); T(dl, 520, 600, "LTV 69%", 34, (140, 230, 160), "b")
    dr = panel(img, (1040, 260, 1760, 640), vis2(t, ts(s, 4) - .3))
    if dr:
        dr.text((1400, 305), "ഇന്ന്", font=MF(46), fill=WHITE, anchor="mm")
        T(dr, 1400, 375, "5 pavan × ₹91,720", 36, (200, 205, 220), "s")
        big_num(dr, 1400, 450, "Gold ₹4,58,600", 54, (255, 130, 115)); big_num(dr, 1400, 540, "Loan ₹4,50,000", 54, WHITE)
        if t > ts(s, 5): T(dr, 1400, 600, "LTV ≈ 98%", 34, (255, 130, 115), "k")
    if t > ts(s, 5) - .5:  # gauge
        d = ImageDraw.Draw(img); x0, x1, y = 300, 1620, 720; p = ease(seg(t, ts(s, 5) - .5, ts(s, 5) + 1.5)); v = lerp(69, 98, p)
        d.rounded_rectangle([x0, y, x1, y + 46], 23, fill=(40, 44, 60)); d.rounded_rectangle([x0, y, x0 + (x1 - x0) * v / 100, y + 46], 23, fill=(220, 60, 60) if v > 80 else GOLDC)
        xl = x0 + (x1 - x0) * .8; d.line([(xl, y - 16), (xl, y + 62)], fill=WHITE, width=5); T(d, xl, y - 34, "80% limit", 26, WHITE, "b")
        T(d, x0 + (x1 - x0) * v / 100, y + 23, f"{v:.0f}%", 28, WHITE, "k", "rm")
    if t > ts(s, 6):
        tag(img, 640, 850, "Repay ≈ ₹83,000", t, ts(s, 6), GOLDC, INK, 38)
        tag(img, 1280, 850, "or pledge 1+ more pavan", t, ts(s, 6) + 1.5, GOLDC, INK, 38)
    subtitle(img, s, t); return img

def S9(t):
    s = "S9"; img = frame_base(s, t, 11, (255, 120, 100)); head(img, "മാർജിൻ കോൾ, ലേലം", "Margin call and auction", t)
    dd = panel(img, (200, 280, 820, 700), vis2(t, .3), (240, 240, 235), None, 18)
    if dd:
        dd.rectangle([200, 280, 820, 350], fill=(220, 60, 60)); T(dd, 510, 315, "NOTICE · MARGIN CALL", 34, WHITE, "k")
        f = F("s", 32)
        for j, l in enumerate(["Your LTV is above the limit.", "Please do one of these:", "• Pay part of the loan", "• Pledge more gold"]):
            if t > ts(s, 1) or j < 2: dd.text((250, 400 + j * 60), l, font=f, fill=(40, 44, 54))
    if t > ts(s, 2):
        d = ImageDraw.Draw(img); p = back(seg(t, ts(s, 2), ts(s, 2) + .5)); cx, cy = 1050, 480; ang = math.sin((t - ts(s, 2)) * 4) * .3
        hx, hy = cx + math.cos(-0.8 + ang) * 120 * p, cy + math.sin(-0.8 + ang) * 120 * p
        d.line([(cx, cy), (hx, hy)], fill=(150, 100, 60), width=int(18 * p) + 1)
        d.rounded_rectangle([hx - 60 * p, hy - 30 * p, hx + 60 * p, hy + 30 * p], 10, fill=(120, 80, 50))
        d.rounded_rectangle([cx - 90 * p, cy + 120 * p, cx + 90 * p, cy + 150 * p], 8, fill=(120, 80, 50))
        T(d, cx, cy + 210, "Auction (after notice)", 32, WHITE, "b")
    if t > ts(s, 3): tag(img, 1500, 420, "Reserve price ≥ 90% of value", t, ts(s, 3), GOLDC, INK, 34)
    if t > ts(s, 4): tag(img, 1500, 560, "Surplus back in 7 working days", t, ts(s, 4), (40, 44, 60), WHITE, 34)
    subtitle(img, s, t); return img

def S10(t):
    s = "S10"; img = frame_base(s, t, 12, (140, 230, 160)); head(img, "ഇപ്പോൾ ചെയ്യേണ്ടത്", "What to do now", t)
    items = [("ലോൺ + പലിശ vs ഇന്നത്തെ വില", "Compare loan + interest with today's gold value"), ("നോട്ടീസിന് മുമ്പ് ബാങ്കുമായി സംസാരിക്കുക", "Talk to your lender before a notice"),
             ("ഒരു നോട്ടീസും അവഗണിക്കരുത്", "Never ignore a notice"), ("RBI നിയന്ത്രിത സ്ഥാപനങ്ങൾ മാത്രം", "Only RBI-regulated lenders")]
    for i, (ml, en) in enumerate(items):
        t0 = ts(s, i + 1); p = ease(seg(t, t0 - .2, t0 + .4))
        if p > 0:
            y = 300 + i * 140; x = 260 - 60 * (1 - p); d = ImageDraw.Draw(img)
            d.ellipse([x, y - 40, x + 80, y + 40], fill=GOLDC); T(d, x + 40, y, str(i + 1), 44, INK, "k")
            d.text((x + 120, y - 16), ml, font=MF(46), fill=WHITE, anchor="lm"); T(d, x + 120, y + 34, en, 28, GOLD2, "s", "lm")
    if t > ts(s, 5): tag(img, 960, 880, "General information, not financial advice", t, ts(s, 5), (40, 44, 60), WHITE, 30)
    subtitle(img, s, t); return img

def S11(t):
    s = "S11"; img = frame_base(s, t, 13, (120, 150, 255)); head(img, "അടുത്ത മാസങ്ങളിൽ?", "What could happen next", t)
    if t < ts(s, 4):
        if t > ts(s, 2): tag(img, 960, 380, "Goldman Sachs: Fed hikes in Dec and March", t, ts(s, 2), (40, 44, 60), WHITE, 38)
        if t > ts(s, 3): tag(img, 960, 520, "While rates rise → pressure on gold may continue", t, ts(s, 3), (220, 60, 60), WHITE, 36)
        if t > ts(s, 1) - .5: tag(img, 960, 260 + 380, "Nobody knows for sure", t, ts(s, 1), GOLDC, INK, 40)
    else:
        bars = [("Now (20 Nov)", 3520, (220, 60, 60), ts(s, 4)), ("Goldman · end-2026", 4150, GOLDC, ts(s, 4) + .8), ("Reuters poll median · 2027", 4650, GOLDC, ts(s, 5))]
        d = ImageDraw.Draw(img); base, top = 760, 300
        for i, (lab, v, col, t0) in enumerate(bars):
            if t > t0:
                p = ease(seg(t, t0, t0 + 1)); x = 420 + i * 420; h = (v / 5600) * (base - top) * p
                d.rounded_rectangle([x - 90, base - h, x + 90, base], 14, fill=col)
                T(d, x, base - h - 34, f"${v:,}", 40, WHITE, "k"); T(d, x, base + 36, lab, 26, (190, 195, 210), "s")
        if t > ts(s, 6): tag(img, 1640, 330, "Central banks still buying", t, ts(s, 6), (40, 44, 60), WHITE, 30)
        if t > ts(s, 7): tag(img, 1640, 450, "Forecasts change often", t, ts(s, 7), (220, 60, 60), WHITE, 30)
    subtitle(img, s, t); return img

def S12(t):
    s = "S12"; img = frame_base(s, t, 14); head(img, "ചുരുക്കത്തിൽ", "In short", t)
    for i, (ml, en) in enumerate([("ഫെഡ് പലിശ", "Fed rate hikes"), ("ശക്തമായ ഡോളർ", "Strong dollar"), ("ഓഹരി തകർച്ച", "Stock crash")]):
        p = back(seg(t, .5 + i * .6, .9 + i * .6))
        if p > 0:
            x = 420 + i * 540; dd = panel(img, (x - 220, 280, x + 220, 420), p, (34, 38, 56), GOLDC)
            if dd: dd.text((x, 330), ml, font=MF(46), fill=WHITE, anchor="mm"); T(dd, x, 385, en, 28, GOLD2, "s")
    if t > ts(s, 2):
        tag(img, 960, 540, "calcsouq.com/gold-price-calculator", t, ts(s, 2), GOLDC, INK, 50)
        if t > ts(s, 2) + .6: T(ImageDraw.Draw(img), 960, 620, "Free gold value calculator · pavan & gram", 32, WHITE, "s")
    if t > ts(s, 3): tag(img, 700, 760, "Share with family", t, ts(s, 3), (40, 44, 60), WHITE, 38)
    if t > ts(s, 4):
        p = back(seg(t, ts(s, 4), ts(s, 4) + .4)); bw, bh = 400 * p, 100 * p; cx, cy = 1250, 760; d = ImageDraw.Draw(img)
        d.rounded_rectangle([cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2], int(28 * p), fill=(230, 33, 23))
        if p > .8: T(d, cx + 26, cy, "SUBSCRIBE", 46, WHITE, "k"); R.bell(d, cx - 140, cy - 6, 0.75)
    subtitle(img, s, t); return img

SCENES = {k: globals()[k] for k in ORDER}

def render(s, out_dir="/tmp/ytg"):
    os.makedirs(out_dir, exist_ok=True); out = f"{out_dir}/{s}.mp4"; tmp = f"{out_dir}/{s}.tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-r", str(FPS), tmp], stdin=subprocess.PIPE)
    n = round(L(s) * FPS)
    for i in range(n): p.stdin.write(SCENES[s](i / FPS).convert("RGB").tobytes())
    p.stdin.close(); assert p.wait() == 0; os.replace(tmp, out); print(out, n / FPS, flush=True)

def write_srt(path, lang):
    def stamp(x): h, r = divmod(x, 3600); m, sec = divmod(r, 60); return f"{int(h):02}:{int(m):02}:{int(sec):02},{int(round((sec % 1) * 1000)) % 1000:03}"
    off, n, out = 0.0, 1, []
    for s in ORDER:
        for k, (m, e) in enumerate(SC[s]):
            t0 = ts(s, k); t1 = ts(s, k + 1) if k + 1 < len(SC[s]) else AUDIO[s] + 0.3
            out.append(f"{n}\n{stamp(off + t0)} --> {stamp(off + t1)}\n{e if lang == 'en' else m}\n"); n += 1
        off += round(L(s) * FPS) / FPS
    open(path, "w").write("\n".join(out)); print(path, n - 1)

if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "--frame": SCENES[a[1]](float(a[2])).convert("RGB").save(a[3])
    elif a and a[0] in ("--srt-en", "--srt-ml"): write_srt(a[1], a[0][-2:])
    else:
        for s in a: render(s)
