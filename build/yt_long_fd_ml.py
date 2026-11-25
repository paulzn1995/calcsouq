"""CalcSouq Malayalam long video: FD rates are up - lock now or wait for 4 December? (16:9, 1920x1080).
Copied from the gold Malayalam standard (yt_long_gold_ml helpers: Manjari headings, English heading underneath,
burnt-in English subtitles) and the EMI video's local 3D props (extruded bars, 3D coins, calendar, push-ins).
New props here: a perspective vault door, an FD certificate with a lock, a 3D ladder, an hourglass and a shield.
Usage: python3 yt_long_fd_ml.py S1 S2 ... | --frame S3 10 out.png | --srt-en out.srt | --srt-ml out.srt | --timeline
B-roll clips sit between scenes (after the scenes in BROLL); narration and subtitles are shifted by them.
"""
import sys, os, math, json, random, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import yt_long_gold_ml as G
import yt_long_emi_ml as E
from yt_long_rates import fx, F, INK, WHITE, RED, GREEN, seg, ease, back, lerp, mix, clamp, count, T, wrap, shadow, bank, arrow
from PIL import Image, ImageDraw, ImageFilter
W, H, FPS = 1920, 1080, 30
HERE = os.path.dirname(os.path.abspath(__file__))
FOLDER = os.path.join(HERE, "youtube/long/2026-11-25-fd-rates-malayalam")
SC = json.load(open(os.path.join(FOLDER, "scenes.json")))
ORDER = list(SC.keys())
AUDIO = json.load(open(os.path.join(FOLDER, "audio.json")))
PAD = 0.45
BROLL = {"S1": 4.0, "S3": 4.0, "S6": 4.0, "S10": 4.0}  # vault, rising bars, hourglass, safe boxes
G.SC, G.AUDIO, G.ORDER, G.PAD, G.END_EXTRA = SC, AUDIO, ORDER, PAD, 0.0
def L(s): return AUDIO[s] + PAD
ts, head, panel, tag, big_num, MF, vis2, subtitle, inr = G.ts, G.head, G.panel, G.tag, G.big_num, G.MF, G.vis2, G.subtitle, G.inr
bar3d, coin_stack, zoom, push, pill, cal = E.bar3d, E.coin_stack, E.zoom, E.push, E.pill, E.cal
GOLDC, GOLD2 = G.GOLDC, G.GOLD2
REDC = (225, 70, 62); GRN = (60, 175, 115); BLU = (80, 130, 230); GREY = (170, 175, 195); NAVY = (30, 34, 50); TEAL = (40, 180, 170)
SKY = (90, 170, 255)

def base(s, t, seed, tint=(60, 160, 200)):
    img = G.bg(t, seed, tint); G.brand(img); return img

def P(t, a, d=.45): return back(seg(t, a, a + d))

# ---------------- local 3D-style props ----------------
def vault(img, cx, cy, r, p=1.0, rot=0.0, open_=0.0):
    """round vault door in perspective: outer ring, bolts, spoked wheel; open_ squashes it sideways like a hinge"""
    if p <= 0.01: return
    r *= back(p) if p < 1 else 1; sx = 1 - .55 * open_
    shadow(img, (cx - r * sx, cy - r, cx + r * sx, cy + r), int(r), 30, 130, (16, 24)); d = ImageDraw.Draw(img)
    if open_ > 0:  # warm light behind the door
        gl = Image.new("RGBA", img.size, (0, 0, 0, 0)); ImageDraw.Draw(gl).ellipse([cx - r * 1.1, cy - r * 1.1, cx + r * 1.1, cy + r * 1.1], fill=(255, 200, 100, int(150 * open_)))
        img.paste(gl, (0, 0), gl.filter(ImageFilter.GaussianBlur(40))); d = ImageDraw.Draw(img)
    ox = cx + r * .5 * open_
    d.ellipse([ox - r * sx - 14, cy - r - 4, ox + r * sx + 14, cy + r + 18], fill=(70, 76, 92))
    for k in range(18):
        f = k / 17; rr = r * (1 - .1 * f)
        d.ellipse([ox - rr * sx, cy - rr, ox + rr * sx, cy + rr], fill=mix((120, 128, 146), (205, 212, 225), f))
    d.ellipse([ox - r * .78 * sx, cy - r * .78, ox + r * .78 * sx, cy + r * .78], fill=(150, 158, 176), outline=(95, 100, 118), width=6)
    for k in range(12):
        a = k / 12 * math.tau; bx, by = ox + math.cos(a) * r * .9 * sx, cy + math.sin(a) * r * .9
        d.ellipse([bx - 9, by - 9, bx + 9, by + 9], fill=(230, 232, 240), outline=(90, 96, 110), width=2)
    for k in range(3):
        a = rot + k / 3 * math.pi
        d.line([(ox - math.cos(a) * r * .5 * sx, cy - math.sin(a) * r * .5), (ox + math.cos(a) * r * .5 * sx, cy + math.sin(a) * r * .5)], fill=(60, 64, 78), width=16)
    d.ellipse([ox - r * .14 * sx, cy - r * .14, ox + r * .14 * sx, cy + r * .14], fill=GOLDC, outline=(120, 90, 20), width=4)
    d.arc([ox - r * .7 * sx, cy - r * .7, ox + r * .7 * sx, cy + r * .7], 200, 260, fill=(240, 244, 250), width=5)

def certificate(img, cx, cy, p, rate="6.60%", locked=1.0, tilt=0.0):
    """FD certificate card with a padlock; tilt gives a slight perspective lean"""
    if p <= 0.01: return
    s = back(p) if p < 1 else 1; w, h = 520 * s, 330 * s
    lay = Image.new("RGBA", (int(w + 60), int(h + 60)), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle([30, 30, 30 + w, 30 + h], int(22 * s), fill=(250, 244, 226), outline=(200, 170, 90), width=5)
    d.rounded_rectangle([46, 46, 14 + w, 14 + h], int(16 * s), outline=(220, 196, 130), width=2)
    if s > .8:
        d.text((30 + w / 2, 30 + 52), "FIXED DEPOSIT", font=F("k", 34), fill=(110, 84, 30), anchor="mm")
        d.text((30 + w / 2, 30 + 150), rate, font=F("k", 92), fill=INK, anchor="mm")
        d.text((30 + w / 2, 30 + 230), "rate fixed until maturity", font=F("s", 28), fill=(110, 100, 80), anchor="mm")
    if tilt:
        lay = lay.transform(lay.size, Image.PERSPECTIVE, (1, tilt, -tilt * 100, 0, 1, 0, tilt * .0006, 0), Image.BICUBIC)
    x0, y0 = int(cx - lay.size[0] / 2), int(cy - lay.size[1] / 2)
    shadow(img, (x0 + 30, y0 + 30, x0 + 30 + w, y0 + 30 + h), 22, 26, 130, (14, 22)); img.paste(lay, (x0, y0), lay)
    if locked > 0 and s > .8:  # padlock at the corner
        d = ImageDraw.Draw(img); lx, ly = x0 + 30 + w - 10, y0 + 40; q = back(locked)
        d.arc([lx - 34 * q, ly - 70 * q, lx + 34 * q, ly + 2], 180, 360, fill=(150, 156, 170), width=int(12 * q) or 1)
        d.rounded_rectangle([lx - 52 * q, ly - 18 * q, lx + 52 * q, ly + 62 * q], int(12 * q), fill=GOLDC, outline=(130, 96, 20), width=4)
        d.ellipse([lx - 9, ly + 12, lx + 9, ly + 30], fill=(90, 66, 10))

def ladder(img, x0, ybase, steps, p_list, labels, sub):
    """3D staircase: each step is an extruded block that rises in"""
    for i, p in enumerate(p_list):
        if p <= 0: continue
        h = (120 + i * 120) * ease(p); x = x0 + i * 300
        bar3d(img, x, ybase, 250, h, [GOLDC, (230, 170, 60), (215, 145, 50)][i], 34)
        if p > .7:
            d = ImageDraw.Draw(img); T(d, x + 125, ybase - h - 60, labels[i], 44, WHITE, "k"); T(d, x + 125, ybase + 50, sub[i], 28, GREY, "s")

def hourglass(img, cx, cy, s, t, p=1.0):
    if p <= 0.01: return
    s *= back(p) if p < 1 else 1; d = ImageDraw.Draw(img); w, h = 150 * s, 240 * s
    shadow(img, (cx - w, cy + h / 2 - 10, cx + w, cy + h / 2 + 20), 30, 18, 110, (0, 6)); d = ImageDraw.Draw(img)
    d.rounded_rectangle([cx - w * .75, cy - h / 2 - 22 * s, cx + w * .75, cy - h / 2], 8, fill=(120, 80, 40))
    d.rounded_rectangle([cx - w * .75, cy + h / 2, cx + w * .75, cy + h / 2 + 22 * s], 8, fill=(120, 80, 40))
    glass = Image.new("RGBA", img.size, (0, 0, 0, 0)); g = ImageDraw.Draw(glass)
    g.polygon([(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + 8 * s, cy), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2), (cx - 8 * s, cy)], fill=(200, 225, 255, 60), outline=(220, 235, 255, 180))
    img.paste(glass, (0, 0), glass); d = ImageDraw.Draw(img)
    f = (t * .05) % 1  # sand level
    top = h / 2 * (1 - f) * .8; d.polygon([(cx - w / 2 * (1 - f) * .8, cy - top), (cx + w / 2 * (1 - f) * .8, cy - top), (cx, cy - 4 * s)], fill=GOLD2)
    bh = h / 2 * f * .7; d.polygon([(cx - w * .42, cy + h / 2), (cx + w * .42, cy + h / 2), (cx, cy + h / 2 - bh)], fill=GOLDC)
    d.line([(cx, cy - 2), (cx, cy + h / 2 - bh)], fill=GOLD2, width=max(2, int(3 * s)))

def shield(img, cx, cy, s, p, col=GRN, txt="₹5 L"):
    if p <= 0.01: return
    s *= back(p) if p < 1 else 1; w, h = 170 * s, 200 * s
    pts = [(cx - w, cy - h * .7), (cx, cy - h), (cx + w, cy - h * .7), (cx + w * .85, cy + h * .15), (cx, cy + h), (cx - w * .85, cy + h * .15)]
    shadow(img, (cx - w, cy - h, cx + w, cy + h), int(w), 26, 120, (12, 20)); d = ImageDraw.Draw(img)
    d.polygon([(x + 10, y + 10) for x, y in pts], fill=mix(col, (0, 0, 0), .45)); d.polygon(pts, fill=col)
    inner = [(cx + (x - cx) * .82, cy + (y - cy) * .82) for x, y in pts]; d.polygon(inner, fill=mix(col, WHITE, .18))
    d.polygon([pts[0], pts[1], (cx, cy), inner[0]], fill=mix(col, WHITE, .3))
    if s > .7: T(d, cx, cy - 10 * s, txt, int(64 * s), WHITE, "k")

def rate_row(img, y, name, sub, val, vmax, col, p, note=None):
    """bank row: name on the left, extruded horizontal bar, rate at the end"""
    if p <= 0: return
    d = panel(img, (150, y - 62, 1770, y + 62), p, (26, 30, 46), (60, 66, 90), 24)
    if not d: return
    T(d, 190, y - 14, name, 40, WHITE, "b", "lm"); T(d, 190, y + 30, sub, 25, GREY, "s", "lm")
    q = ease(seg(p, .8, 1)); bw = 820 * (val / vmax) * q; x = 700
    d.rounded_rectangle([x, y - 26, x + 820, y + 26], 14, fill=(40, 44, 62))
    if bw > 10:
        d.rounded_rectangle([x, y - 26, x + bw, y + 26], 14, fill=col); d.rounded_rectangle([x + 6, y - 22, x + bw - 6, y - 10], 6, fill=mix(col, WHITE, .35))
    T(d, 1690, y, f"{val:.2f}%", 46, mix(col, WHITE, .3), "k")
    if note: T(d, 1690, y + 44, note, 22, GREY, "s")

def ticker_line(img, y, items, t):
    """timeline axis with dated markers"""
    d = ImageDraw.Draw(img); d.line([(200, y), (1720, y)], fill=(90, 96, 120), width=6)
    for (x, date, ml, en, col, t0) in items:
        p = P(t, t0)
        if p <= 0: continue
        d = ImageDraw.Draw(img); r = 22 * p; d.ellipse([x - r, y - r, x + r, y + r], fill=col, outline=WHITE, width=4)
        if p > .8:
            T(d, x, y - 60, date, 36, WHITE, "k")
            dd = panel(img, (x - 210, y + 50, x + 210, y + 190), p, (34, 38, 56), col)
            if dd: dd.text((x, y + 98), ml, font=MF(36), fill=WHITE, anchor="mm"); T(dd, x, y + 150, en, 26, mix(col, WHITE, .4), "s")

def check_item(img, y, ml, en, p, col=GRN, n=None):
    if p <= 0: return
    d = panel(img, (230, y - 58, 1690, y + 58), p, (28, 32, 48), col, 24)
    if not d: return
    d.ellipse([262, y - 34, 330, y + 34], fill=col); T(d, 296, y, str(n) if n else "✓", 38, WHITE, "k")
    d.text((370, y - 16), ml, font=MF(40), fill=WHITE, anchor="lm"); T(d, 370, y + 30, en, 26, GOLD2, "s", "lm")

def money(v): return inr(v)

# =========================== scenes ===========================
def S1(t):
    s = "S1"; img = base(s, t, 1, (245, 190, 60))
    # parallax depth: far coin stacks drift slower than near ones
    for i, (x, n, sp) in enumerate([(220, 5, 6), (1700, 7, 10), (380, 9, 14)]):
        coin_stack(img, x + math.sin(t * .3 + i) * sp, 900 - i * 10, n * ease(seg(t, .2 + i * .2, 1.2 + i * .2)), 60 + i * 8)
    dd = panel(img, (540, 120, 1380, 500), vis2(t, .2))
    if dd:
        T(dd, 960, 175, "SENIOR CITIZEN FD · BIG BANKS · NOV 2026", 28, GREY, "b")
        v = count(6.0, 7.20, t, .3, 2.0); big_num(dd, 960, 305, f"{v:.2f}%", 170, GOLD2)
        T(dd, 960, 435, "HDFC Bank, 3 to 5 years (from 4 Nov)", 32, WHITE, "s")
    img = zoom(img, push(t, .3, 8, .05), 960, 330)
    if ts(s, 1) < t < ts(s, 4): tag(img, 700, 570, "November: banks raise FD rates", t, ts(s, 1), GRN, WHITE, 34)
    if ts(s, 2) < t < ts(s, 4): tag(img, 1260, 570, "RBI decision: 4 Dec", t, ts(s, 2), NAVY, WHITE, 34)
    if ts(s, 3) < t < ts(s, 4):
        p = ease(seg(t, ts(s, 3), ts(s, 3) + .6)); d = ImageDraw.Draw(img)
        d.rounded_rectangle([0, 640, W, 770], 0, fill=mix((12, 14, 24), (16, 18, 30), p))
        d.text((W / 2, 680), "എഫ് ഡി ഇപ്പോൾ ഇടണോ, കാത്തിരിക്കണോ?", font=MF(62), fill=mix((10, 12, 22), WHITE, p), anchor="mm")
        T(d, W / 2, 742, "OPEN AN FD NOW, OR WAIT?", 30, mix((10, 12, 22), GOLDC, p), "b")
    if t > ts(s, 4):
        items = [("ആര് എത്ര തരുന്നു", "Who pays what"), ("₹5 ലക്ഷത്തിന് എത്ര", "₹5 lakh, in rupees"), ("കാത്തിരിക്കണോ", "Wait or not"), ("എത്ര സുരക്ഷിതം", "How safe")]
        for i, (ml, en) in enumerate(items):
            pill(img, 300 + i * 440, 700, ml, en, back(seg(t, ts(s, 4) + i * 1.2, ts(s, 4) + i * 1.2 + .4)), 400)
    subtitle(img, s, t); return img

def S2(t):
    s = "S2"; img = base(s, t, 2, (80, 130, 230)); head(img, "പലിശ കൂടുന്നത് എന്തുകൊണ്ട്?", "Why rates are rising", t)
    if t > ts(s, 1):
        for i, (v, lab, col) in enumerate([(5.25, "Before 7 Oct", (120, 126, 150)), (5.50, "From 7 Oct 2026", GOLDC)]):
            p = ease(seg(t, ts(s, 1) + i * 1.0, ts(s, 1) + i * 1.0 + 1.0))
            if p > 0:
                x = 330 + i * 290; h = (v - 4.0) * 230 * p; bar3d(img, x, 820, 200, h, col, 30); d = ImageDraw.Draw(img)
                T(d, x + 100, 820 - h - 56, f"{v:.2f}%", 50, WHITE, "k"); T(d, x + 100, 862, lab, 28, GREY, "s")
        T(ImageDraw.Draw(img), 520, 300, "RBI REPO RATE", 34, GOLD2, "k")
    if t > ts(s, 2):
        dd = panel(img, (1010, 290, 1780, 520), vis2(t, ts(s, 2), ts(s, 3)))
        if dd:
            bank(img, 1120, 405, .55, 1)
            d = ImageDraw.Draw(img); d.text((1440, 370), "റിപ്പോ = ബാങ്കുകൾ RBI-ക്ക്", font=MF(36), fill=WHITE, anchor="mm")
            d.text((1440, 420), "കൊടുക്കുന്ന പലിശ", font=MF(36), fill=WHITE, anchor="mm")
            T(d, 1440, 475, "Rate banks pay to borrow from RBI", 26, GOLD2, "s")
    if t > ts(s, 3):
        dd = panel(img, (1010, 290, 1780, 640), vis2(t, ts(s, 3)))
        if dd:
            T(dd, 1395, 340, "OCTOBER 2026 RETAIL INFLATION", 28, GREY, "b")
            v = count(5.54, 6.09, t, ts(s, 3) + .3, ts(s, 3) + 2); big_num(dd, 1395, 450, f"{v:.2f}%", 130, (255, 130, 115))
            T(dd, 1395, 560, "RBI upper limit: 6%", 32, WHITE, "s")
    if t > ts(s, 4): tag(img, 1395, 720, "Food inflation: 8.94%", t, ts(s, 4), REDC, WHITE, 38)
    subtitle(img, s, t); return img

def S3(t):
    s = "S3"; img = base(s, t, 3, (225, 90, 70)); head(img, "ലോൺ വേഗം, എഫ് ഡി പതുക്കെ", "Loans fast, deposits slow", t)
    items = [(250, "7 Oct", "റിപ്പോ കൂടി", "Repo hike", GOLDC, .6),
             (700, "8 Oct", "ലോൺ പലിശ കൂടി", "Loan rates up", REDC, ts(s, 1)),
             (1560, "4 Nov", "എഫ് ഡി പലിശ കൂടി", "HDFC FD rates up", GRN, ts(s, 2))]
    ticker_line(img, 420, items, t)
    if t > ts(s, 2) + 1.2:
        p = ease(seg(t, ts(s, 2) + 1.2, ts(s, 2) + 2)); d = ImageDraw.Draw(img); x1 = lerp(700, 1560, p)
        d.line([(700, 330), (x1, 330)], fill=GOLD2, width=5)
        if p > .9: d.line([(1560, 315), (1560, 345)], fill=GOLD2, width=5); T(d, 1130, 296, "≈ 4 weeks later", 36, GOLD2, "k")
    if t > ts(s, 3): check_item(img, 690, "ഓരോ ബാങ്കും സ്വയം തീരുമാനിക്കുന്നു", "Each bank decides when to raise FD rates", P(t, ts(s, 3)), BLU, 1)
    if t > ts(s, 4): check_item(img, 820, "ലോൺ കൂടുന്നു, ബാങ്കിന് നിക്ഷേപം വേണം", "Loans growing fast → banks want deposits", P(t, ts(s, 4)), GOLDC, 2)
    subtitle(img, s, t); return img

def S4(t):
    s = "S4"; img = base(s, t, 4, (60, 175, 115)); head(img, "ആര് എത്ര തരുന്നു?", "Who pays what · Nov 2026", t)
    rows = [(310, "HDFC Bank", "Senior · 3 to 5 years (regular: 6.60%)", 7.20, GOLDC, 1, None),
            (450, "Federal Bank", "Senior · 18 months, 2 to <3 years", 7.40, SKY, 2, None),
            (590, "Bank of Baroda", "Senior · 555-day special FD", 7.35, TEAL, 3, None),
            (730, "Small finance banks", "Senior · select tenures", 8.60, (255, 150, 60), 4, "up to · see safety")]
    for y, name, sub, v, col, k, note in rows:
        if t > ts(s, k): rate_row(img, y, name, sub, v, 9.0, col, ease(seg(t, ts(s, k), ts(s, k) + 1.0)), note)
    if t > ts(s, 4) + 2.5: tag(img, 960, 860, "Higher rate ≠ same safety (more later)", t, ts(s, 4) + 2.5, REDC, WHITE, 32)
    subtitle(img, s, t); return img

def SO(t):
    s = "SO"; img = base(s, t, 5, (245, 190, 60)); head(img, "പഴയ എഫ് ഡിക്ക് പുതിയ പലിശ?", "Does my old FD get the new rate?", t)
    certificate(img, 560, 520, ease(seg(t, .4, 1.1)), "6.25%", P(t, ts(s, 1) + .5), tilt=0.0)
    if t > ts(s, 1): tag(img, 560, 760, "ഇല്ല · NO", t, ts(s, 1), REDC, WHITE, 52, ml=True)
    if t > ts(s, 2):
        for i, (ml, en) in enumerate([("പുതിയ എഫ് ഡി", "New FD"), ("പുതുക്കുമ്പോൾ", "On renewal")]):
            pill(img, 1180 + i * 430, 380, ml, en, P(t, ts(s, 2) + i * .8), 380, GRN)
        T(ImageDraw.Draw(img), 1395, 290, "New rate applies only to", 30, GREY, "s")
    if t > ts(s, 3):
        dd = panel(img, (1000, 500, 1790, 650), P(t, ts(s, 3)), (28, 32, 48), GOLDC)
        if dd: dd.text((1395, 552), "പലിശ കുറഞ്ഞാലും നിരക്ക് മാറില്ല", font=MF(38), fill=WHITE, anchor="mm"); T(dd, 1395, 606, "If rates fall later, your locked rate stays", 26, GOLD2, "s")
    if t > ts(s, 4): tag(img, 1395, 760, "Maturing soon? Choose the tenure, don't just auto-renew", t, ts(s, 4), NAVY, WHITE, 28)
    subtitle(img, s, t); return img

def S5(t):
    s = "S5"; img = base(s, t, 6, (245, 190, 60)); head(img, "₹5 ലക്ഷം: രൂപയിൽ", "₹5 lakh, in rupees", t)
    if t > ts(s, 1):
        dd = panel(img, (150, 270, 900, 460), P(t, ts(s, 1)))
        if dd: big_num(dd, 525, 335, "₹5,00,000", 76, WHITE); T(dd, 525, 412, "1-year FD · HDFC 6.25% · interest added quarterly", 24, GREY, "s")
    if t > ts(s, 2):
        dd = panel(img, (150, 500, 900, 700), P(t, ts(s, 2)), (26, 40, 34), GRN)
        if dd:
            v = count(0, 31990, t, ts(s, 2) + .3, ts(s, 2) + 2.2); big_num(dd, 525, 575, "+" + money(v), 86, (140, 230, 170)); T(dd, 525, 655, "interest in one year (regular)", 26, WHITE, "s")
        coin_stack(img, 1060, 690, 6 * ease(seg(t, ts(s, 2), ts(s, 2) + 2)), 70)
    if t > ts(s, 3):
        dd = panel(img, (1180, 500, 1790, 700), P(t, ts(s, 3)), (26, 40, 34), GOLDC)
        if dd:
            v = count(0, 34614, t, ts(s, 3) + .3, ts(s, 3) + 2.2); big_num(dd, 1485, 575, "+" + money(v), 80, GOLD2); T(dd, 1485, 655, "senior citizen · 6.75%", 26, WHITE, "s")
    if t > ts(s, 4):
        dd = panel(img, (1020, 260, 1790, 480), P(t, ts(s, 4)), (40, 34, 20), GOLDC)
        if dd:
            T(dd, 1405, 302, "5 YEARS · 7.20% · SENIOR", 26, GREY, "b")
            big_num(dd, 1405, 375, money(count(500000, 714374, t, ts(s, 4) + .3, ts(s, 4) + 2.5)), 80, GOLD2)
            T(dd, 1405, 448, "from ₹5,00,000", 24, WHITE, "s")
    subtitle(img, s, t); return img

def S6(t):
    s = "S6"; img = base(s, t, 7, (225, 90, 70)); head(img, "വിലക്കയറ്റം തിന്നുന്നത്", "What inflation eats", t)
    if t > ts(s, 1):
        vals = [("FD interest (6.25%)", 31990, GRN, ts(s, 1) + .3), ("Prices up (6.09%)", 30450, REDC, ts(s, 1) + 1.5)]
        for i, (lab, v, col, t0) in enumerate(vals):
            p = ease(seg(t, t0, t0 + 1.2))
            if p > 0:
                x = 260 + i * 330; h = v / 34000 * 400 * p; bar3d(img, x, 790, 220, h, col, 30); d = ImageDraw.Draw(img)
                T(d, x + 110, 790 - h - 52, money(v * p), 46, WHITE, "k"); T(d, x + 110, 832, lab, 28, GREY, "s")
    if t > ts(s, 2):
        dd = panel(img, (1020, 300, 1780, 520), P(t, ts(s, 2)), (26, 40, 34), GRN)
        if dd: T(dd, 1400, 350, "REAL GAIN, BEFORE TAX", 28, GREY, "b"); big_num(dd, 1400, 440, "≈ " + money(1540), 96, (140, 230, 170))
    if t > ts(s, 3):
        dd = panel(img, (1020, 550, 1780, 790), P(t, ts(s, 3)), (46, 26, 30), REDC)
        if dd:
            T(dd, 1400, 595, "AFTER 10% TAX: KEEP " + money(28791), 28, GREY, "b")
            big_num(dd, 1400, 675, "−" + money(1659), 96, (255, 130, 115)); T(dd, 1400, 755, "behind prices", 26, WHITE, "s")
    if t > ts(s, 4): tag(img, 1400, 860, "FD = safety, not fast growth", t, ts(s, 4), NAVY, WHITE, 36)
    subtitle(img, s, t); return img

def S7(t):
    s = "S7"; img = base(s, t, 8, (80, 130, 230)); head(img, "ഡിസംബർ 4 വരെ കാത്തിരിക്കണോ?", "Wait until 4 December?", t)
    cal(img, 480, 520, ease(seg(t, ts(s, 1) - .2, ts(s, 1) + .5)), t)
    if t > ts(s, 1) + 1.5: tag(img, 480, 760, "Many economists expect +0.25%", t, ts(s, 1) + 1.5, GOLDC, INK, 32)
    if t > ts(s, 2): tag(img, 480, 860, "Not certain: RBI may hold", t, ts(s, 2), REDC, WHITE, 32)
    if t > ts(s, 3):
        dd = panel(img, (1000, 330, 1790, 600), P(t, ts(s, 3)), (28, 32, 48), BLU)
        if dd:
            dd.text((1395, 385), "എഫ് ഡി പലിശ ഉടനെ കൂടണമെന്നില്ല", font=MF(36), fill=WHITE, anchor="mm"); T(dd, 1395, 437, "FD rates can lag by weeks", 28, GOLD2, "s")
            T(dd, 1395, 520, "Oct: repo 7 Oct → HDFC FD 4 Nov", 30, WHITE, "b")
    if t > ts(s, 4): tag(img, 1395, 720, "So what does waiting cost?", t, ts(s, 4), NAVY, WHITE, 36)
    subtitle(img, s, t); return img

def S8(t):
    s = "S8"; img = base(s, t, 9, (245, 190, 60)); head(img, "കാത്തിരിപ്പിന്റെ കണക്ക്", "The cost of waiting · ₹5 lakh", t)
    dd = panel(img, (150, 280, 900, 500), vis2(t, .4))
    if dd: T(dd, 525, 330, "ONE MONTH OF INTEREST AT 6.25%", 28, GREY, "b"); big_num(dd, 525, 425, money(count(0, 2604, t, .6, 2.2)), 100, GOLD2)
    if t > ts(s, 1):
        dd = panel(img, (1020, 280, 1770, 500), P(t, ts(s, 1)), (26, 40, 34), GRN)
        if dd: T(dd, 1395, 330, "IF RATES RISE 0.25%: EXTRA IN A YEAR", 26, GREY, "b"); big_num(dd, 1395, 425, "+" + money(count(0, 1311, t, ts(s, 1) + .3, ts(s, 1) + 2)), 100, (140, 230, 170))
    if t > ts(s, 2):
        hourglass(img, 960, 700, 1.0, t, ease(seg(t, ts(s, 2), ts(s, 2) + .6)))
        tag(img, 960, 900, "≈ 2 weeks of interest", t, ts(s, 2) + .4, GOLDC, INK, 38)
    if t > ts(s, 3): tag(img, 420, 680, "Idle money + uncertain rise", t, ts(s, 3), REDC, WHITE, 30)
    if t > ts(s, 4): tag(img, 1500, 680, "A better way →", t, ts(s, 4), GRN, WHITE, 34)
    subtitle(img, s, t); return img

def S9(t):
    s = "S9"; img = base(s, t, 10, (60, 175, 115)); head(img, "എഫ് ഡി ലാഡർ", "The FD ladder", t)
    if t < ts(s, 1) + 2.5:
        p = ease(seg(t, ts(s, 1) - .3, ts(s, 1) + .3)); q = ease(seg(t, ts(s, 1) + 1.2, ts(s, 1) + 2.4))
        if p > 0:
            dd = panel(img, (660 - 300 * q, 330, 1260 + 300 * q, 520), p * (1 - q * .999))
            if dd: big_num(dd, 960, 400, "₹6,00,000", 90, WHITE); T(dd, 960, 475, "one big FD?", 30, GREY, "s")
    if t > ts(s, 1) + 2:
        pl = [ease(seg(t, ts(s, 2) + i * 1.2, ts(s, 2) + i * 1.2 + 1)) if t > ts(s, 2) else (ease(seg(t, ts(s, 1) + 2, ts(s, 1) + 3)) * .25) for i in range(3)]
        ladder(img, 510, 770, 3, pl, ["1 yr", "2 yr", "3 yr"], ["₹2,00,000", "₹2,00,000", "₹2,00,000"])
    if t > ts(s, 3): tag(img, 1560, 280, "Each year one matures → reinvest", t, ts(s, 3), GRN, WHITE, 30)
    if t > ts(s, 4):
        tag(img, 380, 290, "Rates fall? The rest stays locked", t, ts(s, 4), NAVY, WHITE, 30)
        if t > ts(s, 4) + 3: tag(img, 380, 390, "Emergency? Break just one", t, ts(s, 4) + 3, BLU, WHITE, 30)
    subtitle(img, s, t); return img

def ST(t):
    s = "ST"; img = base(s, t, 11, (80, 130, 230)); head(img, "പ്രത്യേക കാലാവധി", "Special tenures", t)
    if t > ts(s, 1): tag(img, 960, 290, "Longer FD ≠ always a higher rate", t, ts(s, 1), REDC, WHITE, 36)
    if t > ts(s, 2):
        for i, txt in enumerate(["444 days", "555 days"]): tag(img, 760 + i * 400, 400, txt, t, ts(s, 2) + i * .8, GOLDC, INK, 40)
    if t > ts(s, 3):
        rows = [("IOB · 444 days", 6.75, SKY, ts(s, 3)), ("Bank of Baroda · 555 days", 6.85, TEAL, ts(s, 3) + 3.5), ("HDFC · 5 years", 6.60, (140, 146, 170), ts(s, 4))]
        for i, (lab, v, col, t0) in enumerate(rows):
            if t > t0:
                p = ease(seg(t, t0, t0 + 1.2)); x = 420 + i * 430; h = (v - 5.8) * 230 * p
                bar3d(img, x, 800, 230, h, col, 30); d = ImageDraw.Draw(img)
                T(d, x + 115, 800 - h - 50, f"{v:.2f}%", 50, WHITE, "k"); T(d, x + 115, 844, lab, 26, GREY, "s")
        T(ImageDraw.Draw(img), 1660, 470, "Regular depositors, Nov 2026", 24, GREY, "s")
    if t > ts(s, 4) + 3.5: tag(img, 330, 470, "Ask for the full table", t, ts(s, 4) + 3.5, GRN, WHITE, 32)
    subtitle(img, s, t); return img

def S10(t):
    s = "S10"; img = base(s, t, 12, (245, 190, 60)); head(img, "മുതിർന്ന പൗരന്മാർക്ക്", "For senior citizens", t)
    if t > ts(s, 1):
        pill(img, 560, 330, "+0.50% അധികം", "Most banks: extra for seniors", P(t, ts(s, 1)), 560, GOLDC)
        if t > ts(s, 1) + 3: pill(img, 1360, 330, "ഫെഡറൽ: +0.60%", "Federal Bank, select tenures", P(t, ts(s, 1) + 3), 560, SKY)
    if t > ts(s, 2):
        for i, (lab, v, col) in enumerate([("Senior citizens", "₹1,00,000", GOLDC), ("Others", "₹50,000", (140, 146, 170))]):
            dd = panel(img, (180 + i * 420, 470, 560 + i * 420, 660), P(t, ts(s, 2) + i * 1.5), (28, 32, 48), col)
            if dd: T(dd, 370 + i * 420, 515, "TDS ONLY ABOVE", 24, GREY, "b"); big_num(dd, 370 + i * 420, 575, v, 58, WHITE); T(dd, 370 + i * 420, 628, lab + " · per bank / year", 22, GREY, "s")
    if t > ts(s, 3):
        dd = panel(img, (1060, 470, 1780, 760), P(t, ts(s, 3)), (26, 40, 34), GRN)
        if dd:
            T(dd, 1420, 515, "₹10 LAKH · ONE BANK · 7.20%", 26, GREY, "b")
            v = count(0, 73967, t, ts(s, 3) + .3, ts(s, 3) + 2); big_num(dd, 1420, 590, money(v) + " / yr", 64, (140, 230, 170))
            d = ImageDraw.Draw(img); x0, x1 = 1120, 1720; d.rounded_rectangle([x0, 660, x1, 690], 15, fill=(40, 44, 62))
            d.rounded_rectangle([x0, 660, x0 + (x1 - x0) * v / 100000, 690], 15, fill=GRN); d.line([(x1, 645), (x1, 705)], fill=REDC, width=5)
            T(d, x1 - 10, 728, "₹1 lakh limit", 22, GREY, "s", "rm")
    if t > ts(s, 4): tag(img, 960, 850, "TDS = tax collected in advance · declaration if income is below the taxable limit", t, ts(s, 4), NAVY, WHITE, 28)
    subtitle(img, s, t); return img

def S11(t):
    s = "S11"; img = base(s, t, 13, (60, 175, 115)); head(img, "എത്ര സുരക്ഷിതം?", "How safe is your FD?", t)
    if t > ts(s, 1):
        shield(img, 400, 520, 1.0, ease(seg(t, ts(s, 1), ts(s, 1) + .6)))
        d = ImageDraw.Draw(img); T(d, 400, 770, "DICGC insurance", 34, WHITE, "b"); T(d, 400, 815, "per depositor, per bank", 26, GREY, "s"); T(d, 400, 852, "principal + interest", 26, GREY, "s")
    if t > ts(s, 2):
        p = ease(seg(t, ts(s, 2), ts(s, 2) + 1.5)); d = ImageDraw.Draw(img)
        T(d, 1250, 300, "₹10 LAKH IN ONE BANK", 32, WHITE, "k")
        x0, w = 820, 860; d.rounded_rectangle([x0, 340, x0 + w, 440], 20, fill=(40, 44, 62))
        d.rounded_rectangle([x0, 340, x0 + w / 2 * p, 440], 20, fill=GRN)
        if p > .5: d.rounded_rectangle([x0 + w / 2, 340, x0 + w / 2 + w / 2 * (p - .5) * 2, 440], 20, fill=REDC)
        if p > .9: T(d, x0 + w / 4, 390, "₹5 L insured", 34, WHITE, "k"); T(d, x0 + 3 * w / 4, 390, "₹5 L not insured", 34, WHITE, "k")
    if t > ts(s, 3):
        dd = panel(img, (820, 500, 1680, 690), P(t, ts(s, 3)), (28, 32, 48), (255, 150, 60))
        if dd:
            dd.text((1250, 550), "സ്മോൾ ഫിനാൻസ് ബാങ്ക്: ഇൻഷുറൻസ് ഉണ്ട്", font=MF(34), fill=WHITE, anchor="mm")
            T(dd, 1250, 600, "Higher rate usually means a little more risk", 26, GOLD2, "s"); T(dd, 1250, 645, "Many keep under ₹5 lakh there", 26, WHITE, "s")
    if t > ts(s, 4): tag(img, 1250, 790, "Company / NBFC FDs: no DICGC cover", t, ts(s, 4), REDC, WHITE, 34)
    subtitle(img, s, t); return img

def S12(t):
    s = "S12"; img = base(s, t, 14, (60, 175, 115)); head(img, "ഇപ്പോൾ എന്ത് ചെയ്യാം?", "What you can do now", t)
    items = [("വെറുതെ കിടക്കുന്ന പണം: ഒരു ഭാഗം ഇപ്പോൾ", "Idle savings: put part in now, don't wait long"),
             ("ഒന്ന്, രണ്ട്, മൂന്ന് വർഷത്തെ ലാഡർ", "Build a 1, 2 and 3 year ladder"),
             ("ഒരു ബാങ്കിൽ ₹5 ലക്ഷത്തിൽ കൂടുതലോ? വിഭജിക്കുക", "Over ₹5 lakh in one bank? Consider two banks"),
             ("പൊട്ടിക്കും മുമ്പ് പിഴ ചോദിക്കുക", "Before breaking an old FD, ask about the penalty")]
    for i, (ml, en) in enumerate(items):
        if t > ts(s, i + 1): check_item(img, 320 + i * 150, ml, en, P(t, ts(s, i + 1)), [GRN, GOLDC, SKY, (255, 150, 60)][i], i + 1)
    subtitle(img, s, t); return img

def S13(t):
    s = "S13"; img = base(s, t, 15, (245, 190, 60)); head(img, "ചുരുക്കത്തിൽ", "In short", t)
    for i, (ml, en) in enumerate([("പലിശ കൂടി", "Seniors ≈ 7.2–7.4% at big banks"), ("ഡിസംബർ 4: ഉറപ്പില്ല", "4 Dec: a rise is not certain"), ("ലാഡർ", "A ladder works either way")]):
        p = back(seg(t, .5 + i * (ts(s, 1) - .5) / 2 if i else .5, (.9 + i * (ts(s, 1) - .5) / 2) if i else .9))
        if i == 0: p = back(seg(t, .5, .9))
        elif i == 1: p = back(seg(t, ts(s, 1), ts(s, 1) + .4))
        else: p = back(seg(t, ts(s, 1) + 3.5, ts(s, 1) + 3.9))
        if p > 0:
            x = 420 + i * 540; dd = panel(img, (x - 240, 280, x + 240, 420), p, (34, 38, 56), GOLDC)
            if dd: dd.text((x, 330), ml, font=MF(44), fill=WHITE, anchor="mm"); T(dd, x, 385, en, 24, GOLD2, "s")
    if t > ts(s, 2):
        tag(img, 960, 540, "calcsouq.com/compound-interest-calculator", t, ts(s, 2), GOLDC, INK, 46)
        if t > ts(s, 2) + .6: T(ImageDraw.Draw(img), 960, 620, "Free · see what your own FD grows to", 32, WHITE, "s")
    if t > ts(s, 3):
        tag(img, 640, 760, "Now or wait? Tell us in the comments", t, ts(s, 3), (40, 44, 60), WHITE, 34)
        if t > ts(s, 3) + 2:
            p = back(seg(t, ts(s, 3) + 2, ts(s, 3) + 2.4)); bw, bh = 400 * p, 100 * p; cx, cy = 1380, 760; d = ImageDraw.Draw(img)
            d.rounded_rectangle([cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2], int(28 * p), fill=(230, 33, 23))
            if p > .8: T(d, cx + 26, cy, "SUBSCRIBE", 46, WHITE, "k"); G.R.bell(d, cx - 140, cy - 6, 0.75)
    subtitle(img, s, t); return img

SCENES = {k: globals()[k] for k in ORDER}

def render(s, out_dir="/tmp/ytf"):
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
