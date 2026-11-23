"""CalcSouq Malayalam short explainer: onion +116% and your kitchen bill (16:9, 1920x1080, ~100 s).
Reuses the gold-video helpers. Usage: python3 yt_long_onion_ml.py S1 S2 ... | --frame S2 10 out.png | --srt-en out.srt | --srt-ml out.srt | --timeline
"""
import sys, os, math, json, random, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import yt_long_gold_ml as G
from yt_long_rates import F, INK, WHITE, RED, GREEN, seg, ease, back, lerp, mix, clamp, count, T, wrap, shadow
from PIL import Image, ImageDraw, ImageFilter
W, H, FPS = 1920, 1080, 30
HERE = os.path.dirname(os.path.abspath(__file__))
FOLDER = os.path.join(HERE, "youtube/long/2026-11-23-onion-inflation-malayalam")
SC = json.load(open(os.path.join(FOLDER, "scenes.json")))
ORDER = list(SC.keys())
AUDIO = json.load(open("/tmp/yto/audio.json")) if os.path.exists("/tmp/yto/audio.json") else {k: 16.0 for k in ORDER}
PAD = 0.45
G.SC, G.AUDIO, G.ORDER, G.PAD, G.END_EXTRA = SC, AUDIO, ORDER, PAD, 0.0
def L(s): return AUDIO[s] + PAD
ts, head, panel, tag, big_num, MF, vis2, subtitle = G.ts, G.head, G.panel, G.tag, G.big_num, G.MF, G.vis2, G.subtitle
GOLDC, GOLD2 = G.GOLDC, G.GOLD2
ONI = (176, 62, 104); ONI2 = (214, 112, 150); POT = (190, 150, 92); BAD = (230, 70, 70); OK = (60, 180, 110)

def base(t, seed, tint=(200, 80, 130)):
    img = G.bg(t, seed, tint); G.brand(img); return img

def onion(img, cx, cy, s=1.0, rot=0.0):
    """shaded red onion with layer lines, a shoot and roots"""
    sz = int(240 * s); lay = Image.new("RGBA", (sz, sz), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); c = sz / 2
    for k in range(10):  # body shading, dark to light
        f = k / 9; r = 92 * s * (1 - 0.35 * f); ox = -18 * s * f; oy = -16 * s * f
        d.ellipse([c - r + ox, c - r * 0.95 + oy + 20 * s, c + r + ox, c + r * 0.95 + oy + 20 * s], fill=mix((110, 30, 62), ONI2, f))
    for k in (-1, 0, 1):  # layer lines
        d.arc([c - 70 * s + k * 26 * s, c - 60 * s, c + 70 * s + k * 26 * s, c + 110 * s], 200, 340, fill=(120, 36, 70), width=max(1, int(3 * s)))
    d.polygon([(c - 10 * s, c - 64 * s), (c + 10 * s, c - 64 * s), (c + 4 * s, c - 108 * s), (c - 4 * s, c - 108 * s)], fill=(170, 120, 70))
    for k in range(5): d.line([(c, c + 108 * s), (c - 20 * s + k * 10 * s, c + 122 * s)], fill=(200, 180, 140), width=max(1, int(2 * s)))
    d.ellipse([c - 50 * s, c - 30 * s, c - 22 * s, c + 10 * s], fill=(236, 150, 186))
    if rot: lay = lay.rotate(rot, resample=Image.BICUBIC)
    shadow(img, (cx - 80 * s, cy + 60 * s, cx + 80 * s, cy + 100 * s), int(20 * s), 18, 90, (0, 0))
    img.paste(lay, (int(cx - c), int(cy - c)), lay)

def potato(img, cx, cy, s=1.0):
    sz = int(240 * s); lay = Image.new("RGBA", (sz, sz), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); c = sz / 2
    for k in range(8):
        f = k / 7; ox = -14 * s * f
        d.ellipse([c - 104 * s * (1 - .3 * f) + ox, c - 70 * s * (1 - .3 * f), c + 104 * s * (1 - .3 * f) + ox, c + 70 * s * (1 - .3 * f)], fill=mix((120, 88, 48), (214, 178, 118), f))
    rnd = random.Random(7)
    for _ in range(7):
        x, y = c + (rnd.random() - .5) * 150 * s, c + (rnd.random() - .5) * 80 * s; d.ellipse([x - 4 * s, y - 3 * s, x + 4 * s, y + 3 * s], fill=(110, 80, 44))
    shadow(img, (cx - 90 * s, cy + 40 * s, cx + 90 * s, cy + 80 * s), int(20 * s), 18, 90, (0, 0))
    img.paste(lay, (int(cx - c), int(cy - c)), lay)

def arrow(d, x, y, up=True, s=1.0, col=BAD):
    k = -1 if up else 1
    d.polygon([(x, y + k * 40 * s), (x - 30 * s, y), (x - 12 * s, y), (x - 12 * s, y - k * 40 * s), (x + 12 * s, y - k * 40 * s), (x + 12 * s, y), (x + 30 * s, y)], fill=col)

# ---------------- scenes ----------------
def S1(t):
    s = "S1"; img = base(t, 1)
    p = back(seg(t, .1, .8))
    if p > 0: onion(img, 960, 470, 1.6 * p, 6 * math.sin(t * 1.4))
    d = ImageDraw.Draw(img)
    pp = ease(seg(t, .2, .9))
    if pp > 0: d.text((W / 2, 112 - 20 * (1 - pp)), "ഉള്ളിക്ക് എന്ത് പറ്റി?", font=MF(72), fill=mix((10, 12, 22), WHITE, pp), anchor="mm"); T(d, W / 2, 182, "WHAT HAPPENED TO ONIONS?", 30, mix((10, 12, 22), GOLDC, pp), "b")
    if t > ts(s, 1):
        v = count(0, 116, t, ts(s, 1), ts(s, 1) + 1.6); d = ImageDraw.Draw(img)
        dd = panel(img, (1260, 330, 1780, 640), vis2(t, ts(s, 1)), (40, 14, 26), BAD)
        if dd: big_num(dd, 1520, 450, f"+{v:.0f}%", 120, (255, 120, 120)); T(dd, 1520, 560, "Onion · Oct 2026 vs Oct 2025", 26, WHITE, "s")
    if t > ts(s, 2):
        pq = back(seg(t, ts(s, 2), ts(s, 2) + .5))
        if pq > 0:
            potato(img, 420, 500, 1.1 * pq); d = ImageDraw.Draw(img)
            if pq > .8: tag(img, 420, 680, "Potato  −14%", t, ts(s, 2) + .3, OK, WHITE, 40); arrow(d, 600, 470, False, 1.0, OK)
        if t > ts(s, 2) + 1.5: tag(img, W / 2, 800, "എന്തുകൊണ്ട്?  WHY?", t, ts(s, 2) + 1.5, GOLDC, INK, 54, ml=True)
    subtitle(img, s, t); return img

def gauge(img, cx, cy, r, val, p, lim=6.0, mx=10.0):
    d = ImageDraw.Draw(img); box = [cx - r, cy - r, cx + r, cy + r]
    d.arc(box, 180, 360, fill=(50, 56, 76), width=34)
    a_lim = 180 + 180 * lim / mx; d.arc(box, 180, a_lim, fill=(60, 150, 100), width=34); d.arc(box, a_lim, 360, fill=(150, 50, 50), width=34)
    a = math.radians(180 + 180 * min(val * p, mx) / mx); d.line([(cx, cy), (cx + (r - 40) * math.cos(a), cy + (r - 40) * math.sin(a))], fill=WHITE, width=10)
    d.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], fill=WHITE)
    al = math.radians(a_lim); T(d, cx + (r + 46) * math.cos(al), cy + (r + 46) * math.sin(al), "RBI limit 6%", 26, GOLD2, "b")

def S2(t):
    s = "S2"; img = base(t, 2, (255, 120, 90)); head(img, "വിലക്കയറ്റം പരിധി കടന്നു", "Inflation crossed the RBI limit", t)
    p = ease(seg(t, .4, 2.0)); gauge(img, 520, 620, 250, 6.09, p); d = ImageDraw.Draw(img)
    big_num(d, 520, 710, f"{6.09 * p:.2f}%", 84, WHITE); T(d, 520, 775, "CPI inflation · October", 28, (200, 205, 220), "s")
    if t > ts(s, 1): tag(img, 520, 870, "Food inflation 8.94%", t, ts(s, 1), BAD, WHITE, 40)
    if t > ts(s, 2):
        dd = panel(img, (1000, 300, 1820, 860), vis2(t, ts(s, 2)))
        if dd:
            T(dd, 1410, 340, "YEAR-ON-YEAR PRICE RISE · OCT", 24, (170, 175, 195), "b")
            for i, (ml, en, v) in enumerate([("ഉള്ളി", "Onion", 116), ("വെളുത്തുള്ളി", "Garlic", 61), ("ഇഞ്ചി", "Ginger", 48), ("ചെറുനാരങ്ങ", "Lemon", 47)]):
                q = ease(seg(t, ts(s, 2) + .3 + i * .45, ts(s, 2) + 1.3 + i * .45)); y = 430 + i * 110; d = ImageDraw.Draw(img)
                d.text((1050, y), ml, font=MF(36), fill=WHITE, anchor="lm"); T(d, 1050, y + 36, en, 22, GOLD2, "s", "lm")
                d.rounded_rectangle([1300, y - 22, 1300 + 330 * v / 116 * q, y + 22], 12, fill=ONI2 if i == 0 else (220, 120, 90))
                if q > .1: T(d, 1300 + 330 * v / 116 * q + 16, y, f"+{v * q:.0f}%", 34, WHITE, "k", "lm")
    subtitle(img, s, t); return img

def S3(t):  # SX: kitchen bill
    s = "SX"; img = base(t, 3, (240, 170, 70)); head(img, "നിങ്ങളുടെ അടുക്കളയിൽ", "What it means in your kitchen", t)
    if t > ts(s, 1):
        pp = vis2(t, ts(s, 1))
        for i, (lab, v, col) in enumerate([("Last year", 30, (120, 130, 160)), ("Now (+116%)", 65, BAD)]):
            x = 380 + i * 520; dd = panel(img, (x - 220, 300, x + 220, 640), pp, (24, 28, 42), col)
            if dd:
                onion(img, x, 410, 0.6); dd = ImageDraw.Draw(img); vv = count(30, v, t, ts(s, 1) + .4 + i * .8, ts(s, 1) + 1.6 + i * .8) if i else 30
                big_num(dd, x, 540, f"₹{vv:.0f}/kg", 64, WHITE); T(dd, x, 605, lab, 26, GOLD2, "s")
        if pp > .8: d = ImageDraw.Draw(img); d.polygon([(625, 450), (675, 470), (625, 490)], fill=GOLDC)
    if t > ts(s, 2):
        dd = panel(img, (1180, 300, 1800, 760), vis2(t, ts(s, 2)), (24, 28, 42), GOLDC)
        if dd:
            T(dd, 1490, 345, "4 KG A MONTH", 26, (170, 175, 195), "b")
            T(dd, 1490, 430, "₹120  →  ₹260", 58, WHITE, "k")
            v = count(0, 140, t, ts(s, 2) + 1.5, ts(s, 2) + 3); big_num(dd, 1490, 560, f"+₹{v:.0f}", 110, (255, 120, 120))
            dd.text((1490, 660), "മാസം ഉള്ളിക്ക് മാത്രം", font=MF(38), fill=WHITE, anchor="mm"); T(dd, 1490, 710, "every month, onions alone", 24, GOLD2, "s")
    if t > ts(s, 1) + 1: T(ImageDraw.Draw(img), 600, 700, "Example · your local price may differ", 24, (170, 175, 195), "s")
    subtitle(img, s, t); return img

# South India map points (stylised) for S3
STATES = [("Kerala", 780, 760), ("Tamil Nadu", 900, 720), ("Karnataka", 800, 560), ("Andhra", 950, 520), ("Telangana", 910, 420)]
def S3b(t):
    s = "S3"; img = base(t, 4, (90, 170, 255)); head(img, "ദക്ഷിണേന്ത്യയിൽ കൂടുതൽ", "South India hit hardest", t)
    d = ImageDraw.Draw(img)
    pen = [(700, 330), (1060, 330), (1080, 470), (990, 620), (930, 760), (860, 880), (800, 860), (740, 700), (720, 520)]
    d.polygon(pen, fill=(40, 46, 66), outline=(90, 96, 120))
    for i, (n, x, y) in enumerate(STATES):
        p = back(seg(t, .6 + i * .35, 1.0 + i * .35))
        if p > 0:
            r = 22 * p; col = BAD if n != "Kerala" else GOLDC; d = ImageDraw.Draw(img)
            d.ellipse([x - r, y - r, x + r, y + r], fill=col); T(d, x + 40, y, n, 28, WHITE, "b", "lm")
    tag(img, 880, 960 - 40, "Top 5 food-inflation states: all South", t, ts(s, 0) + 1.8, (30, 34, 50), WHITE, 30)
    if t > ts(s, 1):
        dd = panel(img, (1220, 290, 1800, 520), vis2(t, ts(s, 1)), (40, 14, 26), BAD)
        if dd: T(dd, 1510, 330, "KERALA · SEPTEMBER", 24, (200, 170, 180), "b"); big_num(dd, 1510, 420, "₹58 – ₹80/kg", 66, (255, 140, 140)); T(dd, 1510, 485, "onion retail price", 26, WHITE, "s")
    if t > ts(s, 2):
        dd = panel(img, (1220, 570, 1800, 820), vis2(t, ts(s, 2)), (16, 40, 30), OK)
        if dd: T(dd, 1510, 610, "STATE SALE", 24, (170, 220, 190), "b"); big_num(dd, 1510, 700, "₹35/kg", 80, (140, 235, 170)); T(dd, 1510, 775, "Horticorp · Supplyco", 28, WHITE, "s")
    subtitle(img, s, t); return img

def S4(t):
    s = "S4"; img = base(t, 5, (120, 200, 255)); head(img, "ഉള്ളിക്ക് മാത്രം എന്താ?", "Why onions?", t)
    d = ImageDraw.Draw(img)
    # left: cold store with potatoes
    p = vis2(t, ts(s, 1))
    if p > 0:
        dd = panel(img, (180, 260, 860, 730), p, (18, 34, 52), (120, 190, 240))
        if dd:
            for k in range(5): dd.line([(220, 330 + k * 75), (820, 330 + k * 75)], fill=(60, 90, 120), width=3)
            for k in range(9): potato(img, 290 + (k % 3) * 200, 370 + (k // 3) * 110, 0.42)
            dd = ImageDraw.Draw(img); T(dd, 520, 690, "Cold storage: months", 32, WHITE, "b")
            tag(img, 520, 785, "Potato −14%", t, ts(s, 1) + .6, OK, WHITE, 40)
    q = vis2(t, ts(s, 2))
    if q > 0:
        dd = panel(img, (1060, 260, 1740, 730), q, (40, 14, 26), BAD)
        if dd:
            for k in range(3): onion(img, 1250 + k * 150, 400, 0.5, -8 + k * 8)
            dd = ImageDraw.Draw(img); T(dd, 1400, 530, "Limited storage", 34, WHITE, "b")
            T(dd, 1400, 580, "supply drops → price jumps", 28, (255, 160, 160), "s")
            arrow(dd, 1400, 660, True, 1.2, BAD)
    if t > ts(s, 2) + 3.5: tag(img, 1400, 790, "Storage, not just rate hikes", t, ts(s, 2) + 3.5, GOLDC, INK, 44)
    subtitle(img, s, t); return img

def S5(t):
    s = "S5"; img = base(t, 6, (245, 190, 60)); head(img, "ഇനി എന്ത്?", "What next", t)
    for i, (dt, en, k) in enumerate([("4 DEC", "RBI rate decision", 0), ("14 DEC", "Next inflation data", 0)]):
        p = back(seg(t, ts(s, k) + .6 + i * .5, ts(s, k) + 1.1 + i * .5))
        if p > 0:
            x = 620 + i * 680; dd = panel(img, (x - 260, 280, x + 260, 480), p, (24, 28, 42), GOLDC)
            if dd: big_num(dd, x, 350, dt, 72, GOLD2); T(dd, x, 430, en, 30, WHITE, "s")
    if t > ts(s, 1):
        for i, (ml, en) in enumerate([("സപ്ലൈകോ / ഹോർട്ടികോർപ്പ് വില നോക്കുക", "Compare Supplyco & Horticorp prices"), ("ആവശ്യത്തിന് മാത്രം വാങ്ങുക", "Buy only what you need")]):
            p = back(seg(t, ts(s, 1) + i * .5, ts(s, 1) + .5 + i * .5))
            if p > 0:
                y = 560 + i * 120; dd = panel(img, (380, y - 50, 1540, y + 50), p, (24, 28, 42), OK)
                if dd: dd.ellipse([410, y - 30, 470, y + 30], fill=OK); T(dd, 440, y, "✓", 36, WHITE, "k"); dd.text((500, y - 12), ml, font=MF(36), fill=WHITE, anchor="lm"); T(dd, 500, y + 28, en, 22, GOLD2, "s", "lm")
    if t > ts(s, 2):
        tag(img, 700, 830, "നിങ്ങളുടെ നാട്ടിൽ ഉള്ളി വില?", t, ts(s, 2), (30, 34, 50), WHITE, 38, ml=True)
        p = back(seg(t, ts(s, 2) + .6, ts(s, 2) + 1.0)); bw, bh = 380 * p, 96 * p; cx, cy = 1360, 830; d = ImageDraw.Draw(img)
        if p > 0: d.rounded_rectangle([cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2], int(26 * p), fill=(230, 33, 23))
        if p > .8: T(d, cx, cy, "SUBSCRIBE", 44, WHITE, "k")
    subtitle(img, s, t); return img

SCENES = {"S1": S1, "S2": S2, "SX": S3, "S3": S3b, "S4": S4, "S5": S5}

def render(s, out_dir="/tmp/yto"):
    os.makedirs(out_dir, exist_ok=True); out = f"{out_dir}/{s}.mp4"; tmp = f"{out_dir}/{s}.tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-r", str(FPS), tmp], stdin=subprocess.PIPE)
    n = round(L(s) * FPS)
    for i in range(n): p.stdin.write(SCENES[s](i / FPS).convert("RGB").tobytes())
    p.stdin.close(); assert p.wait() == 0; os.replace(tmp, out); print(out, n / FPS, flush=True)

def timeline():
    off, out = 0.0, {}
    for s in ORDER: out[s] = off; off += round(L(s) * FPS) / FPS
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
