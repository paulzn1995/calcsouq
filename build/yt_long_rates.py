"""CalcSouq YouTube long video #1: Why interest rates are rising again (16:9, 1920x1080, 30 fps).
Silent animation, scene by scene, timed to the ElevenLabs narration durations in AUDIO.
Visual events are synced to the narration with at(scene, phrase) (position of the phrase in the script).
Usage: python3 yt_long_rates.py S1 [S2 ...] [--frame S5 12.0 out.png]
Output: /tmp/ytl/<scene>.mp4 ; then concat with ffmpeg.
"""
import sys, os, math, json, subprocess, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFilter
import reel_fx as fx
fx.W, fx.H = 1920, 1080
from reel_fx import F, INK, GOLD, WHITE, OFF, RED, GREEN, BLUE, PINK, PURPLE, ORANGE, seg, ease, back, eio, lerp, mix, clamp, count
W, H, FPS = 1920, 1080, 30
HERE = os.path.dirname(os.path.abspath(__file__))
TEXT = json.load(open(os.path.join(HERE, "youtube/long/2026-11-22-rates-rising/scenes.json")))
AUDIO = {"S1": 22.48, "S2": 24.0, "S3": 28.4, "S4": 23.36, "S5": 26.64, "S6": 36.0, "S7": 15.84, "S8": 19.76}
if os.path.exists("/tmp/ytl/audio.json"): AUDIO.update(json.load(open("/tmp/ytl/audio.json")))
PAD = 0.7
def L(s): return AUDIO[s] + PAD

def at(s, phrase):
    i = TEXT[s].find(phrase); assert i >= 0, (s, phrase)
    return AUDIO[s] * i / len(TEXT[s])

# ---- cheaper shadow (cropped blur) used by reel_fx too ----
def shadow(img, box, radius=40, blur=30, alpha=110, off=(0, 18)):
    x0, y0, x1, y1 = [int(v) for v in box]; m = blur * 2 + 10
    bx0, by0 = max(0, x0 + off[0] - m), max(0, y0 + off[1] - m); bx1, by1 = min(W, x1 + off[0] + m), min(H, y1 + off[1] + m)
    if bx1 <= bx0 or by1 <= by0: return
    sh = Image.new("L", (bx1 - bx0, by1 - by0), 0)
    ImageDraw.Draw(sh).rounded_rectangle([x0 + off[0] - bx0, y0 + off[1] - by0, x1 + off[0] - bx0, y1 + off[1] - by0], max(0, int(radius)), fill=alpha)
    sh = sh.filter(ImageFilter.GaussianBlur(blur / 2)); img.paste((0, 0, 0), (bx0, by0), sh)
fx.shadow = shadow

def vis(t, a, b=1e9, d=0.4):
    """scale factor: pops in at a, shrinks out at b"""
    return min(back(seg(t, a, a + d)), 1 - ease(seg(t, b, b + 0.35)))

def card(img, box, p, fill=WHITE, outline=None, r=36):
    if p <= 0.01: return None
    cx, cy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2; w, h = (box[2] - box[0]) * p, (box[3] - box[1]) * p
    b = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2); shadow(img, b, r, 24, 90, (0, 14)); d = ImageDraw.Draw(img)
    d.rounded_rectangle(b, int(r * p), fill=fill, outline=outline, width=8 if outline else 0)
    return d if p > 0.75 else None

def T(d, x, y, s, size, fill=INK, font="b", anchor="mm"): d.text((x, y), s, font=F(font, size), fill=fill, anchor=anchor)

def wrap(d, s, f, maxw):
    out, cur = [], ""
    for w in s.split():
        if d.textlength((cur + " " + w).strip(), font=f) > maxw and cur: out.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    return out + [cur]

def arrow(d, x1, y1, x2, y2, p, col=WHITE, w=10, head=26):
    if p <= 0: return
    x, y = lerp(x1, x2, p), lerp(y1, y2, p); d.line([(x1, y1), (x, y)], fill=col, width=w)
    a = math.atan2(y2 - y1, x2 - x1)
    d.polygon([(x + head * math.cos(a), y + head * math.sin(a)), (x + head * math.cos(a + 2.4), y + head * math.sin(a + 2.4)),
               (x + head * math.cos(a - 2.4), y + head * math.sin(a - 2.4))], fill=col)

def up_arrow(d, cx, cy, s, col=RED):
    d.polygon([(cx, cy - 60 * s), (cx + 50 * s, cy - 5 * s), (cx + 20 * s, cy - 5 * s), (cx + 20 * s, cy + 55 * s),
               (cx - 20 * s, cy + 55 * s), (cx - 20 * s, cy - 5 * s), (cx - 50 * s, cy - 5 * s)], fill=col, outline=INK, width=max(2, int(4 * s)))

def bank(img, cx, cy, s, p, label=None, col=OFF, lab_col=WHITE):
    if p <= 0.01: return
    s = s * p; d = ImageDraw.Draw(img); lw = max(2, int(5 * s)); w = 260 * s
    shadow(img, (cx - w / 2 - 20 * s, cy - 170 * s, cx + w / 2 + 20 * s, cy + 85 * s), 20, 20, 70, (0, 12)); d = ImageDraw.Draw(img)
    d.polygon([(cx - w / 2 - 25 * s, cy - 88 * s), (cx, cy - 170 * s), (cx + w / 2 + 25 * s, cy - 88 * s)], fill=col, outline=INK, width=lw)
    d.ellipse([cx - 24 * s, cy - 145 * s, cx + 24 * s, cy - 97 * s], fill=GOLD, outline=INK, width=lw)
    if s > 0.4: T(d, cx, cy - 121 * s, "%", int(30 * s), INK, "k")
    d.rectangle([cx - w / 2 - 10 * s, cy - 88 * s, cx + w / 2 + 10 * s, cy - 66 * s], fill=col, outline=INK, width=lw)
    for i in range(4):
        x = cx - w / 2 + 30 * s + i * (w - 60 * s) / 3
        d.rectangle([x - 15 * s, cy - 66 * s, x + 15 * s, cy + 58 * s], fill=col, outline=INK, width=lw)
    d.rectangle([cx - w / 2 - 25 * s, cy + 58 * s, cx + w / 2 + 25 * s, cy + 85 * s], fill=col, outline=INK, width=lw)
    if label and p > 0.8: T(d, cx, cy + 125 * s / p * p + 10, label, int(max(30, 44 * s)), lab_col, "b")

def house(img, cx, cy, s, p, col=(255, 170, 120)):
    if p <= 0.01: return
    s *= p; d = ImageDraw.Draw(img); lw = max(2, int(5 * s))
    shadow(img, (cx - 110 * s, cy - 120 * s, cx + 110 * s, cy + 100 * s), 20, 20, 70, (0, 12)); d = ImageDraw.Draw(img)
    d.rectangle([cx - 95 * s, cy - 20 * s, cx + 95 * s, cy + 100 * s], fill=col, outline=INK, width=lw)
    d.polygon([(cx - 125 * s, cy - 15 * s), (cx, cy - 125 * s), (cx + 125 * s, cy - 15 * s)], fill=RED, outline=INK, width=lw)
    d.rectangle([cx - 25 * s, cy + 30 * s, cx + 25 * s, cy + 100 * s], fill=INK)
    d.rectangle([cx + 45 * s, cy + 5 * s, cx + 80 * s, cy + 40 * s], fill=(190, 230, 255), outline=INK, width=lw)
    d.rectangle([cx - 80 * s, cy + 5 * s, cx - 45 * s, cy + 40 * s], fill=(190, 230, 255), outline=INK, width=lw)

def loan_doc(img, cx, cy, s, p, label="LOAN", col=BLUE):
    if p <= 0.01: return
    s *= p; shadow(img, (cx - 85 * s, cy - 110 * s, cx + 85 * s, cy + 110 * s), 16, 18, 70, (0, 10)); d = ImageDraw.Draw(img)
    d.rounded_rectangle([cx - 85 * s, cy - 110 * s, cx + 85 * s, cy + 110 * s], int(16 * s), fill=WHITE, outline=INK, width=max(2, int(5 * s)))
    d.rectangle([cx - 85 * s, cy - 110 * s, cx + 85 * s, cy - 55 * s], fill=col, outline=INK, width=max(2, int(5 * s)))
    if p > 0.7: T(d, cx, cy - 82 * s, label, int(34 * s), WHITE, "k")
    for i in range(4): d.rounded_rectangle([cx - 60 * s, cy - 30 * s + i * 32 * s, cx + (60 - 30 * (i == 3)) * s, cy - 18 * s + i * 32 * s], 4, fill=(200, 205, 215))

def barrel(img, cx, cy, s, p):
    if p <= 0.01: return
    s *= p; shadow(img, (cx - 90 * s, cy - 120 * s, cx + 90 * s, cy + 120 * s), 30, 20, 80, (0, 12)); d = ImageDraw.Draw(img); lw = max(2, int(5 * s))
    d.rounded_rectangle([cx - 90 * s, cy - 120 * s, cx + 90 * s, cy + 120 * s], int(30 * s), fill=(40, 44, 52), outline=INK, width=lw)
    for k in (-70, 0, 70): d.rectangle([cx - 90 * s, cy + (k - 8) * s, cx + 90 * s, cy + (k + 8) * s], fill=(90, 96, 110))
    d.ellipse([cx - 55 * s, cy - 45 * s, cx + 55 * s, cy + 45 * s], fill=GOLD, outline=INK, width=lw)
    if p > 0.7: T(d, cx, cy, "OIL", int(36 * s), INK, "k")

def factory(img, cx, cy, s, p):
    if p <= 0.01: return
    s *= p; d = ImageDraw.Draw(img); lw = max(2, int(5 * s))
    d.rectangle([cx + 40 * s, cy - 130 * s, cx + 80 * s, cy - 20 * s], fill=(150, 150, 165), outline=INK, width=lw)
    d.polygon([(cx - 110 * s, cy + 80 * s), (cx - 110 * s, cy - 20 * s), (cx - 50 * s, cy - 60 * s), (cx - 50 * s, cy - 20 * s), (cx + 10 * s, cy - 60 * s),
               (cx + 10 * s, cy - 20 * s), (cx + 110 * s, cy - 20 * s), (cx + 110 * s, cy + 80 * s)], fill=(120, 170, 255), outline=INK, width=lw)
    for i in range(3): d.rectangle([cx - 85 * s + i * 65 * s, cy + 10 * s, cx - 50 * s + i * 65 * s, cy + 45 * s], fill=GOLD, outline=INK, width=lw)

def truck(img, cx, cy, s, p, t=0):
    if p <= 0.01: return
    s *= p; d = ImageDraw.Draw(img); lw = max(2, int(5 * s)); bob = math.sin(t * 12) * 2 * s; cy += bob
    d.rounded_rectangle([cx - 120 * s, cy - 70 * s, cx + 30 * s, cy + 40 * s], int(10 * s), fill=(255, 150, 60), outline=INK, width=lw)
    d.rounded_rectangle([cx + 30 * s, cy - 35 * s, cx + 110 * s, cy + 40 * s], int(14 * s), fill=OFF, outline=INK, width=lw)
    d.rectangle([cx + 50 * s, cy - 22 * s, cx + 95 * s, cy + 5 * s], fill=(190, 230, 255), outline=INK, width=lw)
    for x in (-80, 70): d.ellipse([cx + (x - 25) * s, cy + 20 * s - bob, cx + (x + 25) * s, cy + 70 * s - bob], fill=INK)

def thermo(img, cx, cy, s, level, p, col=RED):
    if p <= 0.01: return
    s *= p; d = ImageDraw.Draw(img); lw = max(2, int(5 * s)); top, bot = cy - 200 * s, cy + 120 * s
    d.rounded_rectangle([cx - 30 * s, top, cx + 30 * s, bot], int(30 * s), fill=WHITE, outline=INK, width=lw)
    d.ellipse([cx - 60 * s, bot - 40 * s, cx + 60 * s, bot + 80 * s], fill=col, outline=INK, width=lw)
    ly = lerp(bot - 10 * s, top + 25 * s, clamp(level)); d.rounded_rectangle([cx - 16 * s, ly, cx + 16 * s, bot + 10 * s], int(14 * s), fill=col)
    for k in range(5): d.line([(cx + 30 * s, top + 40 * s + k * 55 * s), (cx + 50 * s, top + 40 * s + k * 55 * s)], fill=WHITE, width=lw)

def bell(d, cx, cy, s, col=WHITE):
    d.pieslice([cx - 30 * s, cy - 34 * s, cx + 30 * s, cy + 26 * s], 180, 360, fill=col)
    d.rectangle([cx - 30 * s, cy - 4 * s, cx + 30 * s, cy + 18 * s], fill=col)
    d.polygon([(cx - 40 * s, cy + 18 * s), (cx + 40 * s, cy + 18 * s), (cx + 30 * s, cy + 6 * s), (cx - 30 * s, cy + 6 * s)], fill=col)
    d.ellipse([cx - 9 * s, cy + 18 * s, cx + 9 * s, cy + 34 * s], fill=col)

def heading(img, text, t, t0=0.15, hl=None, y=128, size=76, col=WHITE):
    fx.kinetic(img, text, y, t, t0, size, col, 0.07, "k", hl)

def brand(img):
    d = ImageDraw.Draw(img); d.rounded_rectangle([40, 32, 236, 82], 25, fill=GOLD); T(d, 138, 57, "CalcSouq", 28, INK, "k")

# ---- subtitles (spoken words → display tokens with digits) ----
REPL = [("three point seven five and four percent", "3.75% and 4%"), ("five point five percent", "5.5%"), ("one hundred dollars", "$100"),
        ("four hundred thousand dollar", "$400,000"), ("thirty years", "30 years"), ("six point two five percent", "6.25%"),
        ("two thousand four hundred and sixty-three dollars", "$2,463"), ("six point five percent", "6.5%"),
        ("two thousand five hundred and twenty-eight", "$2,528"), ("sixty-five dollars", "$65"),
        ("twenty-three thousand five hundred dollars", "$23,500"), ("fifty lakh rupee", "₹50 lakh"), ("twenty years", "20 years"),
        ("seven hundred and eighty rupees", "₹780"), ("one point nine lakh", "₹1.9 lakh"), ("five lakh", "₹5 lakh"),
        ("e m i", "EMI"), ("calc souq dot com", "calcsouq.com"), ("four minutes", "4 minutes")]
REPL = [(tuple(a.split()), b) for a, b in REPL]

def captions(s):
    text = TEXT[s]; words, pos, i = [], [], 0
    for m in re.finditer(r"\S+", text): words.append(m.group()); pos.append(m.start())
    toks = []; k = 0
    norm = lambda w: re.sub(r"[^\w\-']", "", w.lower())
    while k < len(words):
        for a, b in REPL:
            if tuple(norm(w) for w in words[k:k + len(a)]) == a:
                tail = re.sub(r"^.*?([,.?!]*)$", r"\1", words[k + len(a) - 1]); toks.append((b + tail, pos[k])); k += len(a); break
        else: toks.append((words[k], pos[k])); k += 1
    chunks, cur = [], []
    for w, p in toks:
        cur.append((w, p))
        line = " ".join(x for x, _ in cur)
        if len(line) > 48 or w[-1] in ".?!": chunks.append(cur); cur = []
    if cur: chunks.append(cur)
    out = []
    for j, c in enumerate(chunks):
        t0 = AUDIO[s] * c[0][1] / len(text) - 0.1
        t1 = AUDIO[s] * chunks[j + 1][0][1] / len(text) - 0.1 if j + 1 < len(chunks) else AUDIO[s] + 0.3
        out.append((max(0, t0), t1, " ".join(x for x, _ in c)))
    return out

_CAP = {}
def subtitle(img, s, t):
    if s not in _CAP: _CAP[s] = captions(s)
    for t0, t1, line in _CAP[s]:
        if t0 <= t < t1:
            d = ImageDraw.Draw(img); f = F("s", 44); tw = d.textlength(line, font=f)
            box = (int(W / 2 - tw / 2 - 34), 958, int(W / 2 + tw / 2 + 34), 1036)
            reg = img.crop(box); m = Image.new("L", reg.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, reg.size[0] - 1, reg.size[1] - 1], 22, fill=255)
            img.paste(Image.blend(reg, Image.new("RGB", reg.size, (0, 0, 0)), 0.62), box[:2], m)
            ImageDraw.Draw(img).text((W / 2, 997), line, font=f, fill=WHITE, anchor="mm"); return

# =========================== scenes ===========================
def S1(t):
    s = "S1"; img = fx.scene_bg(t, "night", 11); brand(img)
    heading(img, "Interest rates are rising again", t, 0.15, {"rising", "again"})
    out = at(s, "So what does"); ta, tb = at(s, "India's central"), at(s, "in America")
    p = vis(t, ta, out); d = card(img, (230, 250, 900, 560), p)
    if d:
        T(d, 565, 310, "INDIA · RBI", 34, (110, 115, 125)); T(d, 565, 395, "Rate hike in October", 52, INK, "k")
        T(d, 565, 470, "First hike in 3+ years", 38, RED, "b"); up_arrow(d, 300, 300, 0.45, RED)
    p = vis(t, tb, out); d = card(img, (1020, 250, 1690, 560), p)
    if d:
        T(d, 1355, 310, "UNITED STATES · FED", 34, (110, 115, 125)); T(d, 1355, 395, "Hike expected in December", 48, INK, "k")
        T(d, 1355, 470, "Markets now price it in", 38, ORANGE, "b")
    # rate line: years of cuts, then up again
    tc = at(s, "After years"); p = min(ease(seg(t, tc, tc + 2.2)), 1 - ease(seg(t, out, out + .35)))
    if p > 0:
        d = ImageDraw.Draw(img); pts = [(300, 640), (520, 690), (760, 760), (1000, 820), (1200, 850), (1380, 830), (1550, 760), (1660, 690)]
        n = p * (len(pts) - 1); k = int(n); seg_pts = pts[:k + 1]
        if k < len(pts) - 1: seg_pts.append((lerp(pts[k][0], pts[k + 1][0], n - k), lerp(pts[k][1], pts[k + 1][1], n - k)))
        if len(seg_pts) > 1: d.line(seg_pts, fill=GOLD, width=12, joint="curve")
        ex, ey = seg_pts[-1]; d.ellipse([ex - 16, ey - 16, ex + 16, ey + 16], fill=RED if n > 5 else GOLD, outline=WHITE, width=4)
        T(d, 640, 880, "Years of cuts", 36, WHITE, "b")
        if n > 5.2: T(d, 1520, 880, "Going up again", 36, RED, "k")
    # phase 2: what it means for you
    for i, (ph, fn) in enumerate([("your loan", "loan"), ("your rent", "rent"), ("your savings", "save")]):
        tt = at(s, ph); x = 470 + i * 430; p = vis(t, tt)
        if fn == "loan": loan_doc(img, x, 520, 1.3, p)
        elif fn == "rent": house(img, x, 540, 1.25, p)
        else: fx.piggy(img, x, 530, 1.0 * p, t) if p > 0.05 else None
        if p > 0.8: T(ImageDraw.Draw(img), x, 740, ["Your loan", "Your rent", "Your savings"][i], 46, GOLD, "k")
    tw = at(s, "Let's walk")
    if t > out:
        fx.souq(img, 1700, 560, 0.62 * back(seg(t, out + 0.2, out + 0.6)), t, "thinking" if t < tw else "happy", wave=t > tw)
        fx.speech(img, 1700, 380, "Let's see!", tw, t, 40)
    subtitle(img, s, t); return img

def S2(t):
    s = "S2"; img = fx.scene_bg(t, "sky", 22); brand(img)
    heading(img, "The bank for banks", t, 0.15, {"banks"})
    bank(img, 960, 470, 1.05, vis(t, 0.4), "Central bank")
    tb = at(s, "When your bank"); tr = at(s, "When that rate"); hot = ease(seg(t, tr, tr + 0.8))
    xs = [560, 960, 1360]
    for i, x in enumerate(xs):
        bank(img, x, 790, 0.5, vis(t, tb + i * 0.25), "Your bank" if i == 1 else "Bank", (225, 235, 255))
        p = ease(seg(t, tb + 0.6 + i * .2, tb + 1.4 + i * .2)); d = ImageDraw.Draw(img)
        col = mix(GOLD, RED, hot); arrow(d, 960 + (x - 960) * 0.12, 650, x, 700, p, col, 9, 24)
        if p >= 1:  # coins flowing down the arrow
            for k in range(2):
                u = ((t * 0.7 + k * 0.5 + i * 0.17) % 1.0); cxp, cyp = lerp(960 + (x - 960) * .12, x, u), lerp(650, 700, u)
                fx.coin(d, cxp, cyp, 18, GOLD if hot < .5 else (255, 140, 120), "%")
        if hot > 0.5 and t > tr + 0.3 + i * 0.15: fx.pill(img, x + 120, 700, "costlier", t, tr + 0.3 + i * .15, RED, WHITE, 28, 22)
    fx.pill(img, 330, 470, "India · repo 5.50%", t, at(s, "In India"), WHITE, INK, 40, 34)
    fx.pill(img, 1600, 470, "US · 3.75–4.00%", t, at(s, "In the United"), WHITE, INK, 40, 34)
    if t > at(s, "In the United") + 0.5: T(ImageDraw.Draw(img), 1600, 540, "Fed funds target", 30, WHITE, "s")
    if t > at(s, "In India") + 0.5: T(ImageDraw.Draw(img), 330, 540, "RBI policy rate", 30, WHITE, "s")
    subtitle(img, s, t); return img

def S3(t):
    s = "S3"; img = fx.scene_bg(t, "sunset", 33); brand(img)
    heading(img, "Why raise rates? Inflation", t, 0.15, {"Inflation"})
    ty = at(s, "This year"); tp = at(s, "When prices rise"); tcool = at(s, "prices cool down"); tr = at(s, "raises rates")
    if t < ty + .4:
        fx.souq(img, 1560, 560, 0.75 * min(back(seg(t, .3, .8)), 1 - ease(seg(t, ty, ty + .35))) + 1e-3, t, "thinking")
        fx.speech(img, 1560, 340, "On purpose?!", 0.6, t, 42) if t < ty else None
    level = 0.25 + 0.6 * ease(seg(t, tp, tp + 2)) - 0.35 * ease(seg(t, tcool, tcool + 2))
    pth = vis(t, tp - 0.5); thermo(img, 360, 560, 1.15, level, pth, mix(RED, BLUE, ease(seg(t, tcool, tcool + 2))))
    if pth > .8: T(ImageDraw.Draw(img), 360, 835, "Prices", 44, WHITE, "k")
    pr = vis(t, tr, ty);
    if pr > 0.05:
        bank(img, 760, 520, 0.6, pr, None)
        fx.pill(img, 760, 680, "Rates ↑", t, tr + .2, GOLD, INK, 40, 30)
        d = ImageDraw.Draw(img); arrow(d, 640, 470, 470, 470, ease(seg(t, tcool - .4, tcool + .4)), WHITE, 9)
        if t > tcool: T(d, 555, 420, "cools", 34, WHITE, "b")
    to = at(s, "oil jumped"); barrel(img, 960, 520, 1.15, vis(t, to - .3))
    if t > to + .3: fx.pill(img, 960, 735, "$100+ a barrel", t, to + .3, RED, WHITE, 40, 30)
    tm = at(s, "made or moved"); tpush = at(s, "pushed up")
    factory(img, 1480, 400, 0.95, vis(t, tpush)); truck(img, 1480, 700, 1.0, vis(t, tm - .4), t)
    d = ImageDraw.Draw(img)
    arrow(d, 1080, 470, 1350, 410, ease(seg(t, tpush, tpush + .6)), WHITE, 8); arrow(d, 1080, 580, 1350, 690, ease(seg(t, tm - .3, tm + .3)), WHITE, 8)
    if t > tpush + .4: T(d, 1720, 400, "Made", 40, WHITE, "k")
    if t > tm: T(d, 1720, 700, "Moved", 40, WHITE, "k")
    tc = at(s, "Central banks are trying")
    if t > tc: fx.pill(img, 960, 880, "Goal: stop it becoming permanent", t, tc, WHITE, INK, 40, 40)
    subtitle(img, s, t); return img

def S4(t):
    s = "S4"; img = fx.scene_bg(t, "night", 44); brand(img)
    heading(img, "How it reaches your wallet", t, 0.15, {"wallet"})
    xs = [290, 740, 1190, 1640]
    times = [at(s, "The central bank raises"), at(s, "Banks now pay"), at(s, "Floating-rate"), at(s, "And companies")]
    caps = ["Central bank raises its rate", "Banks borrow dearer, lend dearer", "Home, car and business loans reset higher", "Some costs pass on to prices and rents"]
    for i, x in enumerate(xs):
        p = vis(t, times[i] - .2)
        if i == 0: bank(img, x, 500, 0.75, p)
        elif i == 1: bank(img, x, 520, 0.55, p, None, (225, 235, 255))
        elif i == 2: loan_doc(img, x, 470, 1.0, p, "LOAN")
        else: house(img, x, 490, 1.0, p)
        d = ImageDraw.Draw(img)
        if p > .8:
            f = F("b", 34)
            for j, ln in enumerate(wrap(d, caps[i], f, 420)): d.text((x, 650 + j * 44), ln, font=f, fill=GOLD if j == 0 else WHITE, anchor="mm")
        if i < 3:
            arrow(d, x + 125, 470, xs[i + 1] - 125, 470, ease(seg(t, times[i + 1] - .5, times[i + 1])), GOLD, 10)
    tn = at(s, "It doesn't happen")
    if t > tn:
        d = ImageDraw.Draw(img); p = ease(seg(t, tn + .3, AUDIO[s] - 1.5))
        d.rounded_rectangle([290, 820, 1640, 852], 16, fill=(60, 60, 80)); d.rounded_rectangle([290, 820, 290 + 1350 * max(p, .02), 852], 16, fill=GOLD)
        T(d, 290, 892, "Today", 32, WHITE, "b", "lm"); T(d, 1640, 892, "A few months", 32, WHITE, "b", "rm")
        tm = at(s, "shows up in your")
        if t > tm: fx.pill(img, 965, 780, "Your monthly payment ↑", t, tm, RED, WHITE, 36, 30)
    subtitle(img, s, t); return img

def S5(t):
    s = "S5"; img = fx.scene_bg(t, "mint", 55); brand(img)
    heading(img, "Let's put a number on it", t, 0.15, {"number"})
    fx.pill(img, 960, 270, "$400,000 home loan · 30 years", t, at(s, "Take a four"), WHITE, INK, 44, 40)
    ta, tb = at(s, "At six point two five"), at(s, "At six point five")
    for i, (tt, rate, val, col) in enumerate([(ta, "At 6.25%", 2463, GREEN), (tb, "At 6.50%", 2528, RED)]):
        x0 = 260 if i == 0 else 1060; d = card(img, (x0, 350, x0 + 600, 700), vis(t, tt - .2))
        if d:
            T(d, x0 + 300, 420, rate, 50, (100, 105, 115), "b")
            v = count(2000 if i == 0 else 2463, val, t, tt + .2, tt + 1.6); T(d, x0 + 300, 540, f"${v:,.0f}", 110, col, "k")
            T(d, x0 + 300, 640, "per month", 38, (100, 105, 115), "s")
    if t > tb: arrow(ImageDraw.Draw(img), 875, 525, 1045, 525, ease(seg(t, tb, tb + .5)), WHITE, 10)
    tq, tt2 = at(s, "Just a quarter"), at(s, "That's about")
    if tq < t < tt2 + .1: fx.pill(img, 960, 800, "+0.25%  =  +$65 every month", t, tq, RED, WHITE, 52, 46)
    if t > tt2: fx.pill(img, 960, 800, "≈ $23,500 more over the loan", t, tt2, GOLD, INK, 52, 46); fx.confetti(img, t, tt2 + .3, 5, 40) if False else None
    if t > tt2 + .3:
        d = ImageDraw.Draw(img); n = int(clamp((t - tt2 - .3) * 6, 0, 9))
        for k in range(n): fx.coin(d, 1540 + (k % 3) * 70, 880 - (k // 3) * 30, 30, GOLD, "$")
    subtitle(img, s, t); return img

def S6(t):
    s = "S6"; img = fx.scene_bg(t, "berry", 66); brand(img)
    heading(img, "Pay more each month, or for longer?", t, 0.15, {"more", "longer?"}, size=70)
    tf = at(s, "On a fifty")
    if t < tf + .4:
        q = 1 - ease(seg(t, tf, tf + .35)); d = ImageDraw.Draw(img)
        if q > 0.02:
            tl = at(s, "quietly make"); ext = ease(seg(t, tl, tl + 1.5)); a = ease(seg(t, .4, 1.2)) * q
            T(d, 300, 330, "Your loan", 44, WHITE, "k", "lm")
            x1 = 300 + 1000 * a; d.rounded_rectangle([300, 380, max(330, x1), 470], 22, fill=GOLD)
            if ext > 0: d.rounded_rectangle([x1 - 20, 380, x1 + 320 * ext * q, 470], 22, fill=RED); T(d, x1 + 160 * ext, 330, "more months", 40, RED, "k") if ext > .5 else None
            for k in range(int(10 * a)): fx.calendar(d, 300 + k * 100, 580, 0.45 * q, "EMI")
            for k in range(int(4 * ext)): fx.calendar(d, 1300 + k * 80, 580, 0.45 * q, "+")
            te = at(s, "stays the same")
            if t > te: fx.pill(img, 960, 800, "Same EMI  →  more EMIs", t, te, WHITE, INK, 46, 40)
    if t > tf:
        fx.pill(img, 960, 250, "₹50 lakh loan · 20 years · rate +0.25%", t, tf, WHITE, INK, 42, 40)
        ta, tb, tk = at(s, "a quarter-point"), at(s, "Keep the same"), at(s, "So if your bank")
        for i, (tt, ttl, l1, l2, col, tot) in enumerate([(ta, "A · Raise the EMI", "+₹780 a month", "≈ ₹1.9 lakh extra", GREEN, 1.9),
                                                          (tb, "B · Keep EMI, extend", "≈ 1 year longer", "≈ ₹5 lakh extra", RED, 5.0)]):
            x0 = 260 if i == 0 else 1060; best = i == 0 and t > tk
            d = card(img, (x0, 330, x0 + 600, 760), vis(t, tt - .2), WHITE, GOLD if best else None)
            if d:
                T(d, x0 + 300, 395, ttl, 44, INK, "k"); T(d, x0 + 300, 480, l1, 56, col, "k"); T(d, x0 + 300, 555, l2, 44, (90, 95, 105), "b")
                bw = 480 * tot / 5.0 * ease(seg(t, tt + 1, tt + 2.2)); d.rounded_rectangle([x0 + 60, 625, x0 + 540, 675], 25, fill=(232, 232, 238))
                if bw > 30: d.rounded_rectangle([x0 + 60, 625, x0 + 60 + bw, 675], 25, fill=col)
                T(d, x0 + 300, 715, "total extra interest", 30, (120, 125, 135), "s")
            if best: fx.pill(img, x0 + 300, 805, "Costs less in total", t, tk, GOLD, INK, 34, 30)
        if t > tk: fx.souq(img, 960, 860, 0.38 * back(seg(t, tk, tk + .5)), t, "wink")
    subtitle(img, s, t); return img

def S7(t):
    s = "S7"; img = fx.scene_bg(t, "mint", 77); brand(img)
    heading(img, "Good news for savers", t, 0.15, {"savers"})
    tp = at(s, "banks usually pay"); fx.piggy(img, 560, 540, 1.3 * back(seg(t, .3, .8)) + 1e-3, t)
    d = ImageDraw.Draw(img)
    if t > tp:
        for k in range(5):
            u = ((t - tp) * 0.8 + k * 0.2) % 1.0; fx.coin(d, 560 + 30 * math.sin(k * 2), lerp(230, 430, u), 32, GOLD, "%")
        fx.pill(img, 560, 775, "Deposit rates ↑", t, tp, GOLD, INK, 44, 36)
    tc = at(s, "comparing deposit")
    if t > tc - .3:
        hs = [0.55, 0.8, 0.65]
        for i, h in enumerate(hs):
            p = ease(seg(t, tc + i * .2, tc + i * .2 + .8)); x = 1110 + i * 190; d.rounded_rectangle([x, 720 - 380 * h * p, x + 130, 720], 18, fill=GOLD if i == 1 else (200, 240, 225))
            T(d, x + 65, 760, f"Bank {'ABC'[i]}", 34, WHITE, "b")
        if t > tc + 1: fx.pill(img, 1490, 300, "Compare before you park cash", t, tc + 1, WHITE, INK, 36, 30)
    tj = at(s, "Just remember")
    if t > tj: fx.pill(img, 960, 880, "Real gain = deposit rate − inflation", t, tj, WHITE, INK, 44, 40)
    subtitle(img, s, t); return img

def S8(t):
    s = "S8"; img = fx.scene_bg(t, "night", 88); brand(img)
    heading(img, "What it means for you", t, 0.15, {"you"})
    d = ImageDraw.Draw(img)
    for i, (ph, line, col) in enumerate([("dearer loans", "Loans cost more", RED), ("relief for savers", "Savers earn a little more", GREEN), ("check your own", "Check your own numbers", GOLD)]):
        tt = at(s, ph); p = ease(seg(t, tt - .2, tt + .3))
        if p > 0:
            y = 330 + i * 120; x = 200 - 60 * (1 - p); d.ellipse([x, y - 30, x + 60, y + 30], fill=col)
            d.line([(x + 16, y), (x + 27, y + 12), (x + 46, y - 12)], fill=INK, width=8); T(d, x + 90, y, line, 50, WHITE, "k", "lm")
    tc = at(s, "calc souq dot com")
    if t > tc:
        fx.pill(img, 1400, 380, "calcsouq.com", t, tc, GOLD, INK, 72, 60)
        if t > tc + .6: T(d, 1400, 490, "Mortgage & EMI calculators · free", 36, WHITE, "s")
    tsub = at(s, "subscribe")
    if t > tsub:
        p = back(seg(t, tsub, tsub + .4)); bw, bh = 420 * p, 110 * p; cx, cy = 1400, 660
        shadow(img, (cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2), 30, 20, 90); d = ImageDraw.Draw(img)
        d.rounded_rectangle([cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2], int(30 * p), fill=(230, 33, 23))
        if p > .8:
            T(d, cx + 30, cy, "SUBSCRIBE", 50, WHITE, "k"); sw = math.sin((t - tsub) * 10) * 6 * math.exp(-(t - tsub))
            bell(d, cx - 150 + sw, cy - 6, 0.8)
    tw = at(s, "See you")
    fx.souq(img, 300, 820, 0.5 * back(seg(t, at(s, "check your own") + .5, at(s, "check your own") + 1)) + 1e-3, t, "happy", wave=t > tw)
    if t > tw: fx.speech(img, 560, 720, "See you next time!", tw, t, 38)
    subtitle(img, s, t); return img

SCENES = {k: globals()[k] for k in ("S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8")}

def render(s, out_dir="/tmp/ytl"):
    os.makedirs(out_dir, exist_ok=True); out = f"{out_dir}/{s}.mp4"; tmp = f"{out_dir}/{s}.tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-r", str(FPS), tmp], stdin=subprocess.PIPE)
    n = round(L(s) * FPS)
    for i in range(n): p.stdin.write(SCENES[s](i / FPS).convert("RGB").tobytes())
    p.stdin.close(); assert p.wait() == 0; os.replace(tmp, out); print(out, n / FPS, "s", flush=True)

if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "--frame":
        SCENES[a[1]](float(a[2])).convert("RGB").save(a[3])
    else:
        for s in a: render(s)
