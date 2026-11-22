"""CalcSouq Malayalam long video: the Strait of Hormuz and your money (16:9, 1920x1080).
Reuses the gold-video helpers (yt_long_gold_ml) with this video's script, timings and scenes.
Usage: python3 yt_long_hormuz_ml.py S1 S2 ... | --frame S3 10 out.png | --srt-en out.srt | --srt-ml out.srt
B-roll clips (4 s each) are placed by the composition after the scenes listed in BROLL_AFTER; subtitles are shifted to match.
"""
import sys, os, math, json, random, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import yt_long_gold_ml as G
from yt_long_rates import fx, F, INK, WHITE, RED, GREEN, seg, ease, back, lerp, mix, clamp, count, T, wrap, shadow
from PIL import Image, ImageDraw, ImageFilter
W, H, FPS = 1920, 1080, 30
HERE = os.path.dirname(os.path.abspath(__file__))
FOLDER = os.path.join(HERE, "youtube/long/2026-11-23-hormuz-malayalam")
SC = json.load(open(os.path.join(FOLDER, "scenes.json")))
ORDER = list(SC.keys())
AUDIO = json.load(open("/tmp/yth/audio.json")) if os.path.exists("/tmp/yth/audio.json") else {k: 30.0 for k in ORDER}
PAD = 0.45
BROLL = 4.0
BROLL_AFTER = ["S1", "S4", "S6", "S7"]  # tanker, refinery, fuel nozzle, kitchen flame
G.SC, G.AUDIO, G.ORDER, G.PAD, G.END_EXTRA = SC, AUDIO, ORDER, PAD, 0.0
def L(s): return AUDIO[s] + PAD
ts, head, panel, tag, big_num, MF, vis2, subtitle, inr = G.ts, G.head, G.panel, G.tag, G.big_num, G.MF, G.vis2, G.subtitle, G.inr
GOLDC, GOLD2 = G.GOLDC, G.GOLD2
SEA = (14, 38, 66); SEA2 = (22, 60, 98); LAND = (58, 52, 44); LAND2 = (84, 74, 58); FIRE = (255, 120, 40)

def base(s, t, seed, tint=(245, 190, 60)):
    img = G.bg(t, seed, tint); G.brand(img); return img

# ---------------- map of the Gulf (stylised) ----------------
IRAN = [(0, 230), (0, 300), (200, 330), (500, 385), (800, 470), (1050, 560), (1180, 600), (1262, 588), (1400, 640), (1720, 700), (1920, 730), (1920, 230)]
ARAB = [(0, 1080), (0, 500), (200, 520), (420, 600), (560, 700), (700, 760), (715, 700), (760, 690), (775, 770), (880, 800), (1000, 790), (1120, 760), (1190, 700), (1232, 642), (1268, 700), (1330, 760), (1420, 850), (1500, 950), (1560, 1080)]
LANE = [(700, 640), (950, 640), (1150, 640), (1247, 616), (1330, 650), (1480, 720), (1700, 790), (1950, 850)]
_MAP = {}
def map_layer(dark=0.0):
    if dark not in _MAP:
        im = Image.new("RGB", (W, H), SEA); d = ImageDraw.Draw(im)
        for y in range(230, H, 6): d.line([(0, y), (W, y)], fill=mix(SEA, SEA2, 0.5 + 0.5 * math.sin(y / 40)), width=6)
        sh = Image.new("L", (W, H), 0); sd = ImageDraw.Draw(sh); sd.polygon(IRAN, fill=255); sd.polygon(ARAB, fill=255)
        im.paste((5, 12, 24), (8, 14), sh.filter(ImageFilter.GaussianBlur(10)))
        d = ImageDraw.Draw(im)
        for poly in (IRAN, ARAB):
            d.polygon(poly, fill=LAND); d.line(poly + [poly[0]], fill=LAND2, width=4)
        tex = Image.new("RGBA", (W, H), (0, 0, 0, 0)); td = ImageDraw.Draw(tex); rnd = random.Random(4)
        for _ in range(900):
            x, y = rnd.random() * W, rnd.random() * H; td.point((x, y), fill=(120, 105, 80, 60))
        im.paste(tex, (0, 0), tex)
        top = Image.new("RGB", (W, 230), (10, 12, 22)); im.paste(top, (0, 0))
        if dark: im = Image.blend(im, Image.new("RGB", (W, H), (8, 10, 18)), dark)
        _MAP[dark] = im
    return _MAP[dark].copy()

def lane_pt(p):
    seglen = [math.dist(LANE[i], LANE[i + 1]) for i in range(len(LANE) - 1)]; tot = sum(seglen); dd = p * tot
    for i, sl in enumerate(seglen):
        if dd <= sl: a = dd / sl; return (lerp(LANE[i][0], LANE[i + 1][0], a), lerp(LANE[i][1], LANE[i + 1][1], a)), math.atan2(LANE[i + 1][1] - LANE[i][1], LANE[i + 1][0] - LANE[i][0])
        dd -= sl
    return LANE[-1], 0

def tanker(img, x, y, s=1.0, ang=0.0, burn=0.0, t=0.0):
    lay = Image.new("RGBA", (int(260 * s), int(120 * s)), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); w, h = lay.size
    d.polygon([(10 * s, 40 * s), (220 * s, 40 * s), (250 * s, 60 * s), (220 * s, 80 * s), (10 * s, 80 * s)], fill=(150, 40, 40))
    d.rectangle([10 * s, 40 * s, 220 * s, 52 * s], fill=(200, 205, 215))
    d.rectangle([20 * s, 30 * s, 52 * s, 50 * s], fill=(235, 235, 240))
    for k in range(5): d.ellipse([70 * s + k * 28 * s, 50 * s, 86 * s + k * 28 * s, 66 * s], fill=(90, 30, 30))
    lay = lay.rotate(-math.degrees(ang), expand=True, resample=Image.BICUBIC)
    img.paste(lay, (int(x - lay.size[0] / 2), int(y - lay.size[1] / 2)), lay)
    if burn > 0:
        gl = Image.new("RGBA", img.size, (0, 0, 0, 0)); g = ImageDraw.Draw(gl); r = 30 + 12 * math.sin(t * 9)
        for k in range(3):
            rr = r * (1.6 - k * .4) * burn; g.ellipse([x - rr, y - 30 - rr, x + rr, y - 30 + rr], fill=FIRE + (int(90 + k * 50),))
        for k in range(6):  # smoke
            yy = y - 60 - k * 28 - (t * 30) % 28; xx = x + math.sin(t + k) * 14 + k * 8; rr = (18 + k * 6) * burn
            g.ellipse([xx - rr, yy - rr, xx + rr, yy + rr], fill=(60, 60, 66, max(0, 120 - k * 18)))
        img.paste(gl, (0, 0), gl.filter(ImageFilter.GaussianBlur(3)))

def zoom(img, z, cx=W / 2, cy=H / 2):
    if z <= 1.001: return img
    w, h = W / z, H / z; cx = clamp(cx, w / 2, W - w / 2); cy = clamp(cy, h / 2, H - h / 2)
    box = (int(cx - w / 2), int(cy - h / 2), int(cx - w / 2) + int(w), int(cy - h / 2) + int(h))
    return img.crop(box).resize((W, H), Image.BICUBIC)

def label(d, x, y, text, size=30, col=(225, 215, 190)): T(d, x, y, text, size, col, "b")

def barrel(img, cx, cy, s=1.0, col=(40, 44, 56), band=GOLDC):
    d = ImageDraw.Draw(img); w, h = 70 * s, 96 * s
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], int(14 * s), fill=col, outline=band, width=max(2, int(4 * s)))
    for f in (.3, .7): d.line([(cx - w / 2, cy - h / 2 + h * f), (cx + w / 2, cy - h / 2 + h * f)], fill=band, width=max(2, int(4 * s)))

def cylinder(img, cx, cy, s=1.0, col=(200, 40, 40)):
    d = ImageDraw.Draw(img); w, h = 150 * s, 230 * s
    shadow(img, (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), int(40 * s), 20, 100, (0, 12)); d = ImageDraw.Draw(img)
    d.rounded_rectangle([cx - w / 2, cy - h / 2 + 30 * s, cx + w / 2, cy + h / 2], int(50 * s), fill=col)
    d.rounded_rectangle([cx - w / 2 + 16 * s, cy - h / 2 + 50 * s, cx - w / 2 + 36 * s, cy + h / 2 - 30 * s], int(10 * s), fill=mix(col, WHITE, .35))
    d.rectangle([cx - 30 * s, cy - h / 2, cx + 30 * s, cy - h / 2 + 34 * s], fill=(160, 165, 175))
    d.rounded_rectangle([cx - 50 * s, cy - h / 2 - 16 * s, cx + 50 * s, cy - h / 2 + 4 * s], int(8 * s), fill=(120, 125, 135))
    if s > 0.2: T(d, cx, cy + 30 * s, "14.2 kg", int(34 * s), WHITE, "k")

def pump(img, cx, cy, s=1.0):
    d = ImageDraw.Draw(img); w, h = 260 * s, 420 * s
    shadow(img, (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), 24, 24, 110, (0, 14)); d = ImageDraw.Draw(img)
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], int(24 * s), fill=(230, 232, 236))
    d.rounded_rectangle([cx - w / 2 + 24 * s, cy - h / 2 + 30 * s, cx + w / 2 - 24 * s, cy - h / 2 + 170 * s], int(14 * s), fill=(18, 22, 30))
    d.rounded_rectangle([cx + w / 2, cy - 40 * s, cx + w / 2 + 40 * s, cy + 120 * s], int(16 * s), outline=(60, 64, 74), width=int(10 * s))
    return (cx, cy - h / 2 + 100 * s)

# ---------------- scenes ----------------
def S1(t):
    s = "S1"; z = 1 + 0.06 * ease(seg(t, 0, L(s)))
    img = map_layer(); d = ImageDraw.Draw(img)
    label(d, 880, 360, "IRAN"); label(d, 420, 820, "SAUDI ARABIA"); label(d, 1040, 860, "UAE", 26); label(d, 1400, 900, "OMAN", 26)
    n = 6
    for k in range(n):
        p = ((t * 0.035 + k / n) % 1.0); (x, y), a = lane_pt(p); tanker(img, x, y, 0.42, a, burn=1.0 if (k == 2 and t > ts(s, 4)) else 0, t=t)
    img = zoom(img, z, 1240, 620); G.brand(img); d = ImageDraw.Draw(img)
    p0 = ease(seg(t, .2, .9))
    if p0 > 0:
        d.text((W / 2, 112 - 20 * (1 - p0)), "ലോകത്തിന്റെ എണ്ണയുടെ 1/5", font=MF(64), fill=mix((10, 12, 22), WHITE, p0), anchor="mm")
        T(d, W / 2, 176, "ONE FIFTH OF THE WORLD'S OIL & GAS (PRE-WAR)", 28, mix((10, 12, 22), GOLDC, p0), "b")
    if t > ts(s, 1):
        p = ease(seg(t, ts(s, 1), ts(s, 1) + .8)); d = ImageDraw.Draw(img); cx = 1250
        d.line([(cx - 40, 560), (cx - 40, 560 + 130 * p)], fill=GOLDC, width=5)
        tag(img, 1560, 420, "≈ 39 km", t, ts(s, 1), GOLDC, INK, 64)
        if t > ts(s, 1) + .6: T(ImageDraw.Draw(img), 1560, 500, "narrowest point", 30, WHITE, "s")
    if t > ts(s, 2): tag(img, 1560, 580, "Each shipping lane < 4 km", t, ts(s, 2), (30, 34, 50), WHITE, 34)
    if t > ts(s, 3): tag(img, 560, 330, "STRAIT OF HORMUZ", t, ts(s, 3), (220, 60, 60), WHITE, 52)
    if t > ts(s, 4):
        for i, (ml, en) in enumerate([("പെട്രോൾ പമ്പ്", "Petrol pump"), ("അടുക്കള", "Your kitchen")]):
            p = back(seg(t, ts(s, 4) + .6 + i * .5, ts(s, 4) + 1.0 + i * .5))
            if p > 0:
                x = 420 + i * 440; dd = panel(img, (x - 190, 420, x + 190, 540), p, (24, 28, 42), GOLDC)
                if dd: dd.text((x, 462), ml, font=MF(40), fill=WHITE, anchor="mm"); T(dd, x, 510, en, 26, GOLD2, "s")
    subtitle(img, s, t); return img

def S2(t):
    s = "S2"; img = map_layer(); d = ImageDraw.Draw(img)
    label(d, 880, 360, "IRAN"); label(d, 300, 440, "IRAQ · KUWAIT", 26); label(d, 420, 820, "SAUDI ARABIA"); label(d, 760, 735, "QATAR", 22); label(d, 1040, 860, "UAE", 26); label(d, 1400, 900, "OMAN", 26)
    if t > ts(s, 1):  # flows converge to the strait
        for k, src in enumerate([(300, 520), (520, 650), (760, 720), (1060, 740), (650, 470)]):
            p = ease(seg(t, ts(s, 1) + k * .25, ts(s, 1) + k * .25 + 1.2))
            if p > 0:
                ex, ey = 1247, 616; pts = [(lerp(src[0], ex, a * p), lerp(src[1], ey, a * p) - 40 * math.sin(math.pi * a * p)) for a in [i / 20 for i in range(21)]]
                d.line(pts, fill=GOLDC, width=5, joint="curve")
    for k in range(5):
        p = ((t * 0.04 + k / 5) % 1.0); (x, y), a = lane_pt(p); tanker(img, x, y, 0.38, a)
    head(img, "എണ്ണയുടെ പ്രധാന വാതിൽ", "The Gulf's main door to the sea", t)
    if t > ts(s, 2):
        dd = panel(img, (1340, 250, 1840, 470), vis2(t, ts(s, 2)))
        if dd:
            T(dd, 1590, 290, "CRUDE THROUGH HORMUZ · 2025", 24, (170, 175, 195), "b")
            v = count(0, 15, t, ts(s, 2) + .2, ts(s, 2) + 1.6); big_num(dd, 1590, 370, f"{v:.0f} million", 64, GOLD2); T(dd, 1590, 430, "barrels every day", 28, WHITE, "s")
    if t > ts(s, 3):
        for i, c in enumerate(["CHINA", "INDIA", "JAPAN", "KOREA"]):
            tag(img, 1440 + (i % 2) * 230, 560 + (i // 2) * 90, "→ " + c, t, ts(s, 3) + i * .3, (30, 34, 50), WHITE, 30)
    subtitle(img, s, t); return img

def S3(t):
    s = "S3"; img = base(s, t, 3, (255, 110, 90)); head(img, "2026-ൽ എന്ത് സംഭവിച്ചു?", "What happened in 2026", t)
    d = ImageDraw.Draw(img); y = 470; x0, x1 = 220, 1700
    p = ease(seg(t, .5, ts(s, 3) + 1)); d.line([(x0, y), (lerp(x0, x1, p), y)], fill=(90, 96, 120), width=6)
    ev = [(0.0, "28 FEB", "US & Israel strike Iran", 0), (0.12, "MARCH", "Iran restricts Hormuz", 1), (0.55, "APR – OCT", "Talks and strikes take turns", 2), (1.0, "THIS WEEK", "Tankers on fire · Iran says sea mines", 3)]
    for a, dt, tx, k in ev:
        tk = ts(s, k) if k < len(SC[s]) else 0
        pp = back(seg(t, tk, tk + .5))
        if pp > 0:
            x = lerp(x0, x1, a); d = ImageDraw.Draw(img); r = 16 * pp
            d.ellipse([x - r, y - r, x + r, y + r], fill=(220, 60, 60) if k in (0, 3) else GOLDC)
            up = k % 2 == 0; bx = clamp(x, 360, 1560)
            dd = panel(img, (bx - 200, (y - 230) if up else (y + 50), bx + 200, (y - 50) if up else (y + 230)), pp)
            if dd: T(dd, bx, (y - 190) if up else (y + 90), dt, 30, GOLD2, "k"); [T(dd, bx, ((y - 140) if up else (y + 140)) + j * 36, l, 28, WHITE, "s") for j, l in enumerate(wrap(dd, tx, F("s", 28), 360))]
    if t > ts(s, 3):
        (x, yy), a = (1650, 790), 0; tanker(img, x, yy, 0.8, 0, burn=ease(seg(t, ts(s, 3), ts(s, 3) + 1)), t=t)
        T(ImageDraw.Draw(img), 1650, 870, "Illustration · Iran's claim, not independently verified", 22, (170, 175, 195), "s")
    if t > ts(s, 4): tag(img, 560, 860, "UN: at least 25 seafarers killed since Feb", t, ts(s, 4), (220, 60, 60), WHITE, 34)
    subtitle(img, s, t); return img

def S4(t):
    s = "S4"; img = base(s, t, 4, (255, 140, 70)); head(img, "ചരിത്രത്തിലെ ഏറ്റവും വലുത്", "The biggest oil & gas disruption in history", t)
    if t > ts(s, 0) + .8: tag(img, W / 2, 270, "IEA · World Energy Outlook · 19 Nov 2026", t, ts(s, 0) + .8, (30, 34, 50), WHITE, 30)
    d = ImageDraw.Draw(img); yb = 820
    for i, (lab, v, col, tk) in enumerate([("1979 Iranian revolution", 1.0, (120, 130, 160), 3), ("2026 Iran war", 2.8, (220, 60, 60), 2)]):
        p = ease(seg(t, ts(s, tk), ts(s, tk) + 1.6))
        if p > 0:
            x = 620 + i * 640; hgt = 160 * v * p; d = ImageDraw.Draw(img)
            shadow(img, (x - 130, yb - hgt, x + 130, yb), 14, 20, 100, (0, 10)); d = ImageDraw.Draw(img)
            d.rounded_rectangle([x - 130, yb - hgt, x + 130, yb], 14, fill=col)
            for k in range(int(v * p * 3)): barrel(img, x - 80 + (k % 3) * 80, yb - 60 - (k // 3) * 110, 0.8, (30, 34, 48))
            d = ImageDraw.Draw(img); big_num(d, x, yb - hgt - 50, f"{v * p:.1f} billion", 48, WHITE); T(d, x, yb + 40, lab, 30, (200, 205, 220), "s")
    if t > ts(s, 3) + 2: tag(img, 960, 400, "≈ 3×", t, ts(s, 3) + 2, GOLDC, INK, 80)
    if t > ts(s, 4): tag(img, 400, 420, "Hormuz crude flow now ≈ ½ pre-war", t, ts(s, 4), (30, 34, 50), WHITE, 30)
    subtitle(img, s, t); return img

def SW(t):
    s = "SW"; img = base(s, t, 5, (120, 150, 255)); head(img, "ലോകം വിറച്ചപ്പോൾ", "How the world reacted", t)
    items = [("400 million", "barrels released from emergency stocks (Mar)", 1), ("~6 weeks", "of jet fuel left in Europe, IEA warned", 2), ("Fertiliser · helium", "petrochemical trade disrupted too", 3)]
    for i, (big, small, k) in enumerate(items):
        p = back(seg(t, ts(s, k), ts(s, k) + .5))
        if p > 0:
            x = 380 + i * 580; dd = panel(img, (x - 260, 330, x + 260, 720), p)
            if dd:
                if i == 0:
                    for j in range(6): barrel(img, x - 150 + j * 60, 430, 0.6)
                elif i == 1:
                    dd2 = ImageDraw.Draw(img); dd2.polygon([(x - 120, 440), (x + 120, 420), (x + 40, 445), (x + 120, 470)], fill=(200, 205, 215)); dd2.polygon([(x - 20, 440), (x + 30, 380), (x + 50, 380), (x + 20, 440)], fill=(170, 175, 185))
                else:
                    fx.coin(ImageDraw.Draw(img), x - 60, 430, 40, GOLDC, "N"); fx.coin(ImageDraw.Draw(img), x + 60, 430, 40, (140, 200, 230), "He")
                dd = ImageDraw.Draw(img); big_num(dd, x, 550, big, 52 if i < 2 else 40, GOLD2)
                for j, l in enumerate(wrap(dd, small, F("s", 28), 440)): T(dd, x, 620 + j * 36, l, 28, WHITE, "s")
    if t > ts(s, 4): tag(img, W / 2, 820, "ഒരു കടൽ വഴി · ലോകം മുഴുവൻ", t, ts(s, 4), (220, 60, 60), WHITE, 44, ml=True)
    subtitle(img, s, t); return img

def S5(t):
    s = "S5"; img = base(s, t, 6, (255, 150, 60)); head(img, "എണ്ണവിലയുടെ റോളർകോസ്റ്റർ", "Brent crude, $ per barrel", t)
    d = ImageDraw.Draw(img); x0, x1, y0, y1 = 220, 1300, 290, 800
    pts = [(0, 70.7), (.09, 73), (.18, 104), (.27, 112.6), (.36, 104), (.45, 96), (.55, 101), (.64, 98), (.75, 108), (.84, 117.3), (.92, 95.8), (1, 92.6)]
    def Y(v): return lerp(y1, y0, (v - 60) / (125 - 60))
    for v in (70, 90, 110): d.line([(x0, Y(v)), (x1, Y(v))], fill=(70, 76, 100), width=1); T(d, x0 - 16, Y(v), f"${v}", 26, (160, 165, 185), "s", "rm")
    p = ease(seg(t, ts(s, 1), ts(s, 3) + 1.5)); n = p * (len(pts) - 1); k = int(n)
    path = [(lerp(x0, x1, a), Y(v)) for a, v in pts[:k + 1]]
    if k < len(pts) - 1: a0, v0 = pts[k]; a1, v1 = pts[k + 1]; path.append((lerp(x0, x1, lerp(a0, a1, n - k)), Y(lerp(v0, v1, n - k))))
    if len(path) > 1: d.line(path, fill=GOLDC, width=9, joint="curve")
    T(d, x0, y1 + 34, "End Jan", 26, (160, 165, 185), "s", "lm"); T(d, x1, y1 + 34, "20 Nov", 26, (160, 165, 185), "s", "rm")
    T(d, x1, y0 - 26, "Path between marked points approximate", 22, (150, 155, 175), "s", "rm")
    if t > ts(s, 1): tag(img, 330, Y(70.7) - 60, "$71", t, ts(s, 1), GOLDC, INK, 34)
    if t > ts(s, 2): tag(img, lerp(x0, x1, .84), Y(117.3) - 50, "Oct high $117", t, ts(s, 2), (220, 60, 60), WHITE, 32)
    if t > ts(s, 3): tag(img, x1, Y(92.6) + 60, "$92.6 · −21%", t, ts(s, 3), (60, 160, 100), WHITE, 32)
    if t > ts(s, 4):
        dd = panel(img, (1400, 330, 1820, 760), vis2(t, ts(s, 4)))
        if dd:
            dd.text((1610, 380), "എന്തുകൊണ്ട്?", font=MF(48), fill=WHITE, anchor="mm")
            if t > ts(s, 5):
                for j, l in enumerate(["Gulf oil flowing again", "by other routes", "", "IEA: world surplus", "this quarter"]): T(dd, 1610, 470 + j * 50, l, 32, GOLD2 if j < 2 else (140, 230, 160), "s")
    subtitle(img, s, t); return img

def donut(img, cx, cy, r, frac, col, p, label_big, label_small):
    d = ImageDraw.Draw(img); w = int(r * .32)
    d.arc([cx - r, cy - r, cx + r, cy + r], 0, 360, fill=(50, 56, 76), width=w)
    if p > 0: d.arc([cx - r, cy - r, cx + r, cy + r], -90, -90 + 360 * frac * p, fill=col, width=w)
    big_num(d, cx, cy - 6, label_big, int(r * .42), WHITE); T(d, cx, cy + r + 46, label_small, 28, (200, 205, 220), "s")

def S6(t):
    s = "S6"; img = base(s, t, 7, (90, 200, 140)); head(img, "ഇന്ത്യ എത്രത്തോളം ആശ്രയിക്കുന്നു?", "How exposed is India?", t)
    if t > ts(s, 0): donut(img, 330, 520, 150, .88, GOLDC, ease(seg(t, ts(s, 0), ts(s, 0) + 1.2)), "88%", "crude imported")
    if t > ts(s, 1): donut(img, 760, 520, 150, .5, (220, 60, 60), ease(seg(t, ts(s, 1), ts(s, 1) + 1.2)), "≈50%", "via Hormuz (pre-war)")
    if t > ts(s, 2):
        p = ease(seg(t, ts(s, 2), ts(s, 2) + 1.2)); donut(img, 1190, 520, 150, .7, (60, 170, 110), p, "≈70%", "now avoids Hormuz")
        tag(img, 1190, 300, "40+ supplier countries", t, ts(s, 2) + .5, (30, 34, 50), WHITE, 28)
    if t > ts(s, 3):
        dd = panel(img, (1420, 300, 1860, 820), vis2(t, ts(s, 3)), (40, 20, 24), (220, 60, 60))
        if dd:
            dd.text((1640, 350), "പാചകവാതകം", font=MF(46), fill=WHITE, anchor="mm"); T(dd, 1640, 400, "LPG", 30, GOLD2, "k")
            cylinder(img, 1560, 560, 0.7); dd = ImageDraw.Draw(img)
            if t > ts(s, 4): big_num(dd, 1730, 510, "60%", 54, WHITE); T(dd, 1730, 555, "imported", 24, (220, 220, 230), "s"); big_num(dd, 1730, 625, "90%", 54, (255, 130, 115)); T(dd, 1730, 670, "of that via Hormuz", 22, (220, 220, 230), "s")
            if t > ts(s, 5): T(dd, 1640, 760, "No strategic LPG reserve", 28, (255, 150, 140), "b")
    subtitle(img, s, t); return img

def S7(t):
    s = "S7"; img = base(s, t, 8, (255, 190, 60)); head(img, "നിങ്ങളുടെ പോക്കറ്റ്: പെട്രോൾ", "Your pocket: petrol in Kochi", t)
    sx, sy = pump(img, 420, 560, 1.15); d = ImageDraw.Draw(img)
    v = 105.55 if t < ts(s, 2) else count(105.55, 113.53, t, ts(s, 2), ts(s, 2) + 1.6)
    if t > ts(s, 1): T(d, sx, sy - 30, "PETROL · ₹/L", 24, (150, 155, 175), "b"); big_num(d, sx, sy + 30, f"₹{v:.2f}", 64, GOLD2 if t < ts(s, 2) else (255, 140, 120))
    if t > ts(s, 1): tag(img, 420, 840, "A year ago ≈ ₹106 → now ≈ ₹114", t, ts(s, 1), (30, 34, 50), WHITE, 30)
    if t > ts(s, 2): tag(img, 1000, 330, "+ ≈ ₹8 per litre", t, ts(s, 2) + .8, (220, 60, 60), WHITE, 42)
    if t > ts(s, 3):
        dd = panel(img, (820, 420, 1500, 760), vis2(t, ts(s, 3)))
        if dd:
            T(dd, 1160, 470, "40 litres a month × ₹8", 34, (200, 205, 220), "s")
            m = count(0, 319, t, ts(s, 3) + .3, ts(s, 3) + 1.8); big_num(dd, 1160, 560, f"+₹{m:.0f} / month", 70, WHITE)
            if t > ts(s, 4): y_ = count(0, 3830, t, ts(s, 4), ts(s, 4) + 1.5); big_num(dd, 1160, 670, f"≈ +{inr(y_)} / year", 56, (255, 140, 120))
    if t > ts(s, 5):
        for i, (ml, en) in enumerate([("ഡീസൽ", "Diesel"), ("ലോറി ചാർജ്", "Freight"), ("പച്ചക്കറി · അരി", "Food prices")]):
            p = back(seg(t, ts(s, 5) + i * .6, ts(s, 5) + i * .6 + .4))
            if p > 0:
                x = 1650; y = 380 + i * 170; dd = panel(img, (x - 190, y - 60, x + 190, y + 60), p, (34, 38, 56), GOLDC)
                if dd: dd.text((x, y - 14), ml, font=MF(38), fill=WHITE, anchor="mm"); T(dd, x, y + 32, en, 24, GOLD2, "s")
                if i < 2 and p > .9: ImageDraw.Draw(img).line([(x, y + 64), (x, y + 106)], fill=GOLDC, width=5)
    subtitle(img, s, t); return img

def S8(t):
    s = "S8"; img = base(s, t, 9, (255, 110, 90)); head(img, "അടുക്കളയിലെ ഗ്യാസ്", "Your kitchen: LPG cylinder", t)
    cylinder(img, 380, 580, 1.4 * back(seg(t, .2, .8)) + 1e-3)
    d = ImageDraw.Draw(img)
    if t > ts(s, 1):
        for i, (lab, v, tk) in enumerate([("March", "+₹60", 0), ("June", "+₹29", .8)]):
            tag(img, 820, 380 + i * 110, f"{lab} {v}", t, ts(s, 1) + tk, (220, 60, 60), WHITE, 40)
        tag(img, 820, 600, "= +₹89", t, ts(s, 1) + 2.2, GOLDC, INK, 50)
    if t > ts(s, 2):
        dd = panel(img, (1100, 300, 1820, 560), vis2(t, ts(s, 2)))
        if dd:
            T(dd, 1460, 345, "DOMESTIC 14.2 kg · DELHI", 26, (170, 175, 195), "b")
            v = count(853, 942, t, ts(s, 2) + .4, ts(s, 2) + 2); big_num(dd, 1460, 440, f"₹853 → {inr(v)}", 72, WHITE)
            T(dd, 1460, 520, "Kerala prices are similar", 24, (160, 165, 185), "s")
    if t > ts(s, 3): tag(img, 1460, 640, "19 kg commercial: up 3 months in a row", t, ts(s, 3), (30, 34, 50), WHITE, 30)
    if t > ts(s, 4): tag(img, 1460, 760, "June: oil firms losing ≈ ₹700 per cylinder", t, ts(s, 4), (220, 60, 60), WHITE, 32)
    if t > ts(s, 5): tag(img, 1460, 870, "Pressure for more hikes remains", t, ts(s, 5), GOLDC, INK, 34)
    subtitle(img, s, t); return img

def S9(t):
    s = "S9"; img = base(s, t, 10, (120, 150, 255)); head(img, "എണ്ണ, ഡോളർ, രൂപ, EMI", "Oil → dollar → rupee → your EMI", t)
    chain = [("എണ്ണവില", "Oil price up", 0), ("ഡോളർ വേണം", "More dollars", 1), ("രൂപ ദുർബലം", "Rupee weaker", 1), ("വിലക്കയറ്റം", "Inflation", 4), ("റിപ്പോ 5.5%", "RBI repo", 4)]
    for i, (ml, en, k) in enumerate(chain):
        p = back(seg(t, ts(s, k) + (i % 2) * .7, ts(s, k) + (i % 2) * .7 + .4))
        if p > 0:
            x = 240 + i * 360; dd = panel(img, (x - 150, 270, x + 150, 390), p, (34, 38, 56), GOLDC)
            if dd: dd.text((x, 312), ml, font=MF(36), fill=WHITE, anchor="mm"); T(dd, x, 360, en, 24, GOLD2, "s")
            if i < 4 and p > .9: T(ImageDraw.Draw(img), x + 180, 330, "→", 44, GOLDC, "k")
    if t > ts(s, 2):
        dd = panel(img, (220, 470, 1100, 860), vis2(t, ts(s, 2)))
        if dd:
            T(dd, 660, 515, "RUPEE PER US DOLLAR", 28, (170, 175, 195), "b")
            for j, (lab, v, col, tk) in enumerate([("Record low · May 2026", "≈ 97.0", (255, 130, 115), 2), ("19 Nov close", "93.32", (140, 230, 160), 3)]):
                if t > ts(s, tk): T(dd, 660, 600 + j * 130, lab, 30, (200, 205, 220), "s"); big_num(dd, 660, 655 + j * 130, "₹" + v, 64, col)
    if t > ts(s, 4):
        dd = panel(img, (1220, 470, 1820, 860), vis2(t, ts(s, 4)))
        if dd:
            T(dd, 1520, 515, "RBI REPO RATE", 28, (170, 175, 195), "b"); big_num(dd, 1520, 600, "5.25% → 5.50%", 58, WHITE); T(dd, 1520, 670, "7 Oct 2026", 28, GOLD2, "s")
            T(dd, 1520, 740, "Next meeting: 2–4 Dec", 30, WHITE, "b")
            if t > ts(s, 5): T(dd, 1520, 805, "Floating-rate EMIs can change", 28, (255, 150, 140), "s")
    subtitle(img, s, t); return img

def S10(t):
    s = "S10"; img = map_layer(0.15); d = ImageDraw.Draw(img)
    label(d, 880, 360, "IRAN"); label(d, 420, 820, "SAUDI ARABIA"); label(d, 760, 735, "QATAR", 22); label(d, 1040, 860, "UAE", 26)
    head(img, "വഴി മാറ്റാൻ പറ്റുമോ?", "Can oil avoid Hormuz?", t)
    if t > ts(s, 1):
        p = ease(seg(t, ts(s, 1), ts(s, 1) + 2)); d = ImageDraw.Draw(img)
        a = [(560, 690), (300, 820), (0, 960)]; b = [(1080, 790), (1250, 830), (1420, 880)]
        for path, lab, lx, ly in [(a, "Saudi pipeline → Red Sea", 330, 870), (b, "UAE pipeline → Gulf of Oman", 1560, 870)]:
            n = int(p * 20); pts = []
            for i in range(n + 1):
                q = i / 20 * (len(path) - 1); k = min(int(q), len(path) - 2); f = q - k; pts.append((lerp(path[k][0], path[k + 1][0], f), lerp(path[k][1], path[k + 1][1], f)))
            if len(pts) > 1: d.line(pts, fill=(60, 200, 120), width=10)
            if p > .9: tag(img, lx, ly, lab, t, ts(s, 1) + 2, (30, 34, 50), WHITE, 26)
    if t > ts(s, 2):
        dd = panel(img, (1380, 270, 1840, 560), vis2(t, ts(s, 2)))
        if dd:
            T(dd, 1610, 310, "MIDDLE EAST OIL EXPORTS · NOV", 22, (170, 175, 195), "b"); v = count(100, 64, t, ts(s, 2) + .3, ts(s, 2) + 1.8)
            big_num(dd, 1610, 410, f"{v:.0f}%", 96, (255, 130, 115)); T(dd, 1610, 500, "of pre-war, incl. pipelines (Kpler)", 24, WHITE, "s")
    if t > ts(s, 3): tag(img, 760, 640, "Qatar LNG: no other way out", t, ts(s, 3), (220, 60, 60), WHITE, 30)
    if t > ts(s, 4): tag(img, 1247, 520, "39 km", t, ts(s, 4), GOLDC, INK, 56)
    subtitle(img, s, t); return img

def S11(t):
    s = "S11"; img = base(s, t, 11, (200, 170, 255)); head(img, "അടുത്ത മാസങ്ങളിൽ?", "Three possible paths (not a forecast)", t)
    sc = [("ചർച്ച വിജയിച്ചാൽ", "Deal · route reopens", "Oil could fall further", "40+ damaged sites need time", (60, 170, 110), 1),
          ("ഇടയ്ക്കിടെ ആക്രമണം", "On-off attacks", "Prices keep swinging", "Like the last few weeks", GOLDC, 2),
          ("യുദ്ധം കനത്താൽ", "Escalation", "Spike above $110 possible", "As in October", (220, 60, 60), 3)]
    for i, (ml, en, l1, l2, col, k) in enumerate(sc):
        p = back(seg(t, ts(s, k), ts(s, k) + .5))
        if p > 0:
            x = 380 + i * 580; dd = panel(img, (x - 260, 290, x + 260, 760), p, (24, 28, 42), col)
            if dd:
                dd.rounded_rectangle([x - 260, 290, x + 260, 340], 20, fill=col); T(dd, x, 315, ["1", "2", "3"][i], 30, INK if i == 1 else WHITE, "k")
                dd.text((x, 400), ml, font=MF(42), fill=WHITE, anchor="mm"); T(dd, x, 455, en, 28, GOLD2, "s")
                arr = ["↓", "↕", "↑"][i]; big_num(dd, x, 560, arr, 110, col)
                T(dd, x, 660, l1, 28, WHITE, "b"); T(dd, x, 705, l2, 24, (180, 185, 200), "s")
    if t > ts(s, 4): tag(img, W / 2, 830, "UN Security Council: new Hormuz resolution being negotiated", t, ts(s, 4), (30, 34, 50), WHITE, 28)
    if t > ts(s, 5): tag(img, W / 2, 920, "IEA chief: “The energy world will never be the same again”", t, ts(s, 5), GOLDC, INK, 30)
    subtitle(img, s, t); return img

def S12(t):
    s = "S12"; img = base(s, t, 12, (140, 230, 160)); head(img, "പരിഭ്രാന്തി വേണ്ട, പ്ലാൻ മതി", "No panic. Just a plan.", t)
    items = [("ഇന്ധനച്ചെലവ് എഴുതുക", "Track fuel costs for a month", 1), ("EMI മുൻകൂട്ടി കണക്കാക്കുക", "Check your EMI if rates rise", 2), ("3–6 മാസത്തെ എമർജൻസി ഫണ്ട്", "Emergency fund: 3–6 months", 3), ("വാട്സാപ്പ് കിംവദന്തി വേണ്ട", "Ignore panic-buying rumours", 4)]
    for i, (ml, en, k) in enumerate(items):
        p = back(seg(t, ts(s, k), ts(s, k) + .5))
        if p > 0:
            y = 290 + i * 135; x = 960; dd = panel(img, (x - 640, y - 60, x + 640, y + 60), p, (24, 28, 42), (60, 170, 110))
            if dd:
                dd.ellipse([x - 610, y - 34, x - 542, y + 34], fill=(60, 170, 110)); T(dd, x - 576, y, "✓", 40, WHITE, "k")
                dd.text((x - 500, y - 14), ml, font=MF(40), fill=WHITE, anchor="lm"); T(dd, x - 500, y + 32, en, 26, GOLD2, "s", "lm")
    if t > ts(s, 5): tag(img, W / 2, 840, "ദൂരെയുള്ള കടൽ · നമ്മുടെ വീട്ടുചെലവ്", t, ts(s, 5), GOLDC, INK, 40, ml=True)
    subtitle(img, s, t); return img

def S13(t):
    s = "S13"; img = base(s, t, 13); head(img, "സൗജന്യ കാൽക്കുലേറ്റർ", "Free EMI calculator", t)
    tag(img, 960, 330, "calcsouq.com/loan-emi-calculator", t, .4, GOLDC, INK, 50)
    if t > ts(s, 1):
        dd = panel(img, (460, 420, 1460, 600), vis2(t, ts(s, 1)))
        if dd: dd.text((960, 480), "നിങ്ങളുടെ നാട്ടിൽ പെട്രോൾ വില?", font=MF(46), fill=WHITE, anchor="mm"); T(dd, 960, 550, "Tell us in the comments 👇".replace("👇", ""), 32, GOLD2, "s")
    if t > ts(s, 2):
        p = back(seg(t, ts(s, 2), ts(s, 2) + .4)); bw, bh = 420 * p, 104 * p; cx, cy = 960, 760; d = ImageDraw.Draw(img)
        d.rounded_rectangle([cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2], int(28 * p), fill=(230, 33, 23))
        if p > .8: T(d, cx + 26, cy, "SUBSCRIBE", 48, WHITE, "k"); G.R.bell(d, cx - 150, cy - 6, 0.75)
        if t > ts(s, 2) + 1: tag(img, 960, 880, "Share with family", t, ts(s, 2) + 1, (30, 34, 50), WHITE, 34)
    subtitle(img, s, t); return img

SCENES = {k: globals()[k] for k in ORDER}

def render(s, out_dir="/tmp/yth"):
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
        if s in BROLL_AFTER: off += BROLL
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
