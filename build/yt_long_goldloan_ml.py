"""CalcSouq Malayalam long video: "Gold loan danger line" (1920x1080, ~15+ min).
New look: hyper-real stills with a teal/gold grade, chapter header, DANGER METER gauge (LTV), lower-third data cards,
stress-test table, formula card, recap list, burnt-in English subtitles on a dark band.
Usage: python3 yt_long_goldloan_ml.py S01 S02 ... | --frame S06 8 out.png | --srt-en out.srt | --srt-ml out.srt | --timeline
"""
import sys, os, json, subprocess, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_fx import F, seg, ease, back, lerp
from yt_long_rates import wrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W, H, FPS = 1920, 1080, 30
HERE = os.path.dirname(os.path.abspath(__file__))
FOLDER = os.path.join(HERE, "youtube/long/2026-11-25-gold-loan-danger-line-malayalam")
IMG = os.path.join(HERE, "reel_assets/2026-11-25-goldloan")
SC = json.load(open(os.path.join(FOLDER, "scenes.json")))
ORDER = list(SC.keys())
AUDIO = json.load(open(os.path.join(FOLDER, "audio.json")))
PAD = 0.7
GOLD = (245, 195, 60); WHITE = (255, 255, 255); RED = (232, 64, 64); AMBER = (245, 160, 40); GREEN = (60, 200, 130)
TEAL = (20, 120, 130); INKD = (8, 14, 20)
_MF = {}
def MF(s):
    if s not in _MF: _MF[s] = ImageFont.truetype(os.path.join(HERE, "fonts/Manjari-Bold.ttf"), int(s), layout_engine=ImageFont.Layout.RAQM)
    return _MF[s]
def L(s): return AUDIO[s] + PAD
def ts(s, k):
    lens = [len(m) + 1 for m, *_ in SC[s]["s"]]; return AUDIO[s] * sum(lens[:k]) / sum(lens)
def t_end(s, k): return ts(s, k + 1) if k + 1 < len(SC[s]["s"]) else L(s)

_IM = {}
def img(k):
    if k not in _IM:
        p = os.path.join(IMG, k + ".png")
        if not os.path.exists(p): p = os.path.join(IMG, k[:-1] + "A.png")
        im = Image.open(p).convert("RGB"); tw, th = int(W * 1.22), int(H * 1.22)
        sc = max(tw / im.width, th / im.height); im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
        l, t = (im.width - tw) // 2, (im.height - th) // 2
        _IM[k] = im.crop((l, t, l + tw, t + th))
    return _IM[k]

MOVES = [(1.0, 1.10, .5, .5, .52, .46), (1.10, 1.0, .46, .52, .54, .5), (1.03, 1.12, .42, .55, .58, .47), (1.08, 1.01, .58, .46, .44, .54)]
def cam(k, p, mv):
    z0, z1, x0, y0, x1, y1 = mv; q = ease(p) * .5 + p * .5
    im = img(k); z = lerp(z0, z1, q)
    vw = im.width * 0.82 / z; vh = vw * H / W
    cx = lerp(x0, x1, q) * im.width; cy = lerp(y0, y1, q) * im.height
    cx = min(max(cx, vw / 2), im.width - vw / 2); cy = min(max(cy, vh / 2), im.height - vh / 2)
    return im.crop((int(cx - vw / 2), int(cy - vh / 2), int(cx + vw / 2), int(cy + vh / 2))).resize((W, H), Image.BILINEAR)

_VG = None
def grade(im):
    global _VG
    if _VG is None:
        m = Image.new("L", (W // 4, H // 4), 0); d = ImageDraw.Draw(m)
        for y in range(H // 4):
            for x in range(0, W // 4, 2):
                dx = (x - W / 8) / (W / 8); dy = (y - H / 8) / (H / 8); r = (dx * dx * .55 + dy * dy * .8)
                a = int(min(200, max(0, (r - .35) * 190)))
                if y > H // 4 - 70: a = max(a, int(215 * ((y - (H // 4 - 70)) / 70) ** 1.3))
                if y < 45: a = max(a, int(160 * (1 - y / 45) ** 1.5))
                d.line([(x, y), (x + 1, y)], fill=a)
        _VG = m.resize((W, H), Image.BILINEAR)
    im = Image.blend(im, Image.new("RGB", (W, H), (10, 40, 48)), .10)
    im.paste((0, 0, 0), (0, 0), _VG); return im

def layer(): return Image.new("RGBA", (W, H), (0, 0, 0, 0))

def chapter(im, s, t):
    i = ORDER.index(s) + 1; ml, en = SC[s]["head"]
    p = min(ease(seg(t, .15, .9)), 1 - ease(seg(t, 7.0, 7.7)))
    if p <= .02: return
    lay = layer(); d = ImageDraw.Draw(lay); a = int(255 * p); x = 70 - 40 * (1 - p)
    d.text((x, 70), f"CHAPTER {i:02d}", font=F("b", 24), fill=GOLD + (a,), anchor="lm")
    d.text((x, 122), ml, font=MF(58), fill=WHITE + (a,), anchor="lm", stroke_width=2, stroke_fill=(0, 0, 0, int(a * .6)))
    d.text((x, 176), en.upper(), font=F("s", 22), fill=(205, 215, 220, a), anchor="lm")
    ln = max(d.textlength(ml, font=MF(58)), 260) * ease(seg(t, .4, 1.4))
    d.rectangle((x, 200, x + ln, 204), fill=GOLD + (a,))
    im.paste(lay, (0, 0), lay)

# ---- danger meter --------------------------------------------------------------------------
def meter_value(s, t):
    who = SC[s].get("who")
    if not who: return None
    owner = who[0]; val = None
    for sc in ORDER[:ORDER.index(s) + 1]:
        w2 = SC[sc].get("who")
        if not w2 or w2[0] != owner: continue
        for k, (m, e, mv, tg) in enumerate(SC[sc]["s"]):
            if mv is None: continue
            if sc == s and ts(s, k) + .3 > t: break
            prev = val; val = mv
            if sc == s and prev is not None and t < ts(s, k) + 1.6: val = lerp(prev, mv, ease(seg(t, ts(s, k) + .3, ts(s, k) + 1.5)))
            elif sc == s and prev is None and t < ts(s, k) + 1.6: val = lerp(0, mv, ease(seg(t, ts(s, k) + .3, ts(s, k) + 1.5)))
    return val

def meter(im, s, t):
    who = SC[s].get("who")
    if not who: return
    owner, limit = who; v = meter_value(s, t)
    p = ease(seg(t, .5, 1.2)) * (1 - ease(seg(t, L(s) - .5, L(s))))
    if p <= .02: return
    lay = layer(); d = ImageDraw.Draw(lay); a = int(255 * p)
    x1, y0 = W - 60, 70; x0 = x1 - 400; box = (x0, y0, x1, y0 + 340)
    d.rounded_rectangle(box, 28, fill=(6, 12, 18, int(215 * p)), outline=GOLD + (int(120 * p),), width=2)
    d.text(((x0 + x1) / 2, y0 + 32), f"{owner} · LTV", font=F("b", 22), fill=(205, 215, 220, a), anchor="mm")
    cx, cy, R = (x0 + x1) / 2, y0 + 215, 125; MAXV = 120
    def ang(val): return 180 + 180 * min(max(val, 0), MAXV) / MAXV
    for lo, hi, col in ((0, limit, GREEN), (limit, min(limit + 10, MAXV), AMBER), (min(limit + 10, MAXV), MAXV, RED)):
        d.arc((cx - R, cy - R, cx + R, cy + R), ang(lo), ang(hi), fill=col + (a,), width=20)
    la = math.radians(ang(limit)); d.line((cx + (R - 26) * math.cos(la), cy + (R - 26) * math.sin(la), cx + (R + 10) * math.cos(la), cy + (R + 10) * math.sin(la)), fill=WHITE + (a,), width=4)
    d.text((cx + R + 10, cy + 22), f"limit {limit}%", font=F("b", 18), fill=(220, 225, 230, a), anchor="rm")
    if v is not None:
        na = math.radians(ang(v)); d.line((cx, cy, cx + (R - 30) * math.cos(na), cy + (R - 30) * math.sin(na)), fill=WHITE + (a,), width=6)
        d.ellipse((cx - 11, cy - 11, cx + 11, cy + 11), fill=WHITE + (a,))
        col = GREEN if v <= limit + .05 else (AMBER if v <= limit + 10 else RED)
        d.text((cx, cy + 62), f"{v:.0f}%" if abs(v - round(v)) < .05 or v > 100 else f"{v:.1f}%", font=F("k", 56), fill=col + (a,), anchor="mm")
        if v > limit + .05 and int(t * 2) % 2 == 0: d.text((cx, y0 + 62), "ABOVE LIMIT", font=F("k", 20), fill=RED + (a,), anchor="mm")
    im.paste(lay, (0, 0), lay)

# ---- price ticker (S01, S02) ------------------------------------------------------------
def ticker(im, s, t):
    if SC[s].get("fx") != "ticker": return
    p = ease(seg(t, .6, 1.3)) * (1 - ease(seg(t, L(s) - .5, L(s))))
    if p <= .02: return
    lay = layer(); d = ImageDraw.Draw(lay); a = int(255 * p)
    x1, y0 = W - 60, 70; x0 = x1 - 500
    d.rounded_rectangle((x0, y0, x1, y0 + 210), 28, fill=(6, 12, 18, int(215 * p)), outline=GOLD + (int(120 * p),), width=2)
    if s == "S01":
        d.text((x0 + 30, y0 + 38), "KERALA · 1 PAVAN · 22K", font=F("b", 21), fill=(205, 215, 220, a), anchor="lm")
        q = ease(seg(t, ts(s, 1) + .2, ts(s, 1) + 2.2)); v = round(lerp(107080, 91360, q))
        d.text((x0 + 30, y0 + 105), f"₹{v:,}".replace(",", "_").replace("_", ","), font=F("k", 64), fill=(WHITE if q < .05 else RED) + (a,), anchor="lm")
        d.text((x0 + 30, y0 + 170), "▼ −14.7% since 5 Nov" if q > .5 else "5 Nov 2026", font=F("b", 26), fill=(RED if q > .5 else GOLD) + (a,), anchor="lm")
    else:
        d.text((x0 + 30, y0 + 38), "SPOT GOLD · US$ / OZ", font=F("b", 21), fill=(205, 215, 220, a), anchor="lm")
        q = ease(seg(t, ts(s, 0) + .5, ts(s, 2) + 1.5)); v = round(lerp(5595, 3720, q))
        d.text((x0 + 30, y0 + 105), f"${v:,}", font=F("k", 64), fill=(WHITE if q < .05 else RED) + (a,), anchor="lm")
        d.text((x0 + 30, y0 + 170), "▼ ≈ −32% from Jan record" if q > .5 else "Jan record", font=F("b", 26), fill=(RED if q > .5 else GOLD) + (a,), anchor="lm")
    # sparkline
    pts = []
    for j in range(40):
        u = j / 39; yy = .15 + .7 * u + .06 * math.sin(j * 1.7) * (1 - u * .5)
        pts.append((x1 - 140 + 110 * u, y0 + 55 + 60 * yy))
    n = max(2, int(40 * ease(seg(t, 1.0, 3.0))))
    d.line(pts[:n], fill=RED + (a,), width=4)
    im.paste(lay, (0, 0), lay)

# ---- lower-third data card ---------------------------------------------------------------
def card(im, s, t):
    fxs = SC[s].get("fx")
    if fxs in ("recap",): return
    for k, (m, e, mv, tg) in enumerate(SC[s]["s"]):
        if not tg: continue
        t0 = ts(s, k) + .25; t1 = t_end(s, k) + .3
        p = min(back(seg(t, t0, t0 + .5)), 1 - ease(seg(t, t1, t1 + .35)))
        if p <= .02: continue
        lay = layer(); d = ImageDraw.Draw(lay); a = int(255 * min(p, 1))
        f = F("k", 52); tw = d.textlength(tg, font=f)
        bad = any(x in tg for x in ("−", "ABOVE", "88%", "99%", "Only", "Danger", "0", "Worst", "low")) and not any(x in tg for x in ("Bank value", "Fictional"))
        acc = RED if ("−" in tg or "Danger" in tg or "Only" in tg or "99%" in tg or "88%" in tg or "cushion 0" in tg or "low" in tg or "Worst" in tg) else GOLD
        x0 = 70 - 120 * (1 - min(p, 1)); y0 = 760
        d.rounded_rectangle((x0, y0, x0 + tw + 80, y0 + 104), 22, fill=(6, 12, 18, int(225 * min(p, 1))))
        d.rounded_rectangle((x0, y0, x0 + 12, y0 + 104), 6, fill=acc + (a,))
        d.text((x0 + 44, y0 + 52), tg, font=f, fill=WHITE + (a,), anchor="lm")
        im.paste(lay, (0, 0), lay)

# ---- special panels ----------------------------------------------------------------------
def panel(d, box, p):
    d.rounded_rectangle(box, 30, fill=(6, 12, 18, int(222 * p)), outline=GOLD + (int(110 * p),), width=2)

def stress(im, s, t):
    if SC[s].get("fx") != "stress": return
    rows = [("Today", "₹91,360", 87.9), ("−5%", "₹86,792", 92.5), ("−10%", "₹82,224", 97.7), ("−20%", "₹73,088", 109.9)]
    p = ease(seg(t, .6, 1.3)) * (1 - ease(seg(t, L(s) - .5, L(s))))
    if p <= .02: return
    lay = layer(); d = ImageDraw.Draw(lay); a = int(255 * p)
    x0, y0 = 70, 250; panel(d, (x0, y0, x0 + 900, y0 + 470), p)
    d.text((x0 + 40, y0 + 50), "STRESS TEST · SREEJA'S LOAN", font=F("b", 26), fill=GOLD + (a,), anchor="lm")
    for j, (h, c) in enumerate((("Price move", 40), ("Pavan", 330), ("LTV", 640))):
        d.text((x0 + c, y0 + 105), h.upper(), font=F("b", 20), fill=(170, 185, 195, a), anchor="lm")
    for j, (lab, pv, ltv) in enumerate(rows):
        tj = .9 if j == 0 else ts(s, j) + .3
        q = ease(seg(t, tj, tj + .5))
        if q <= .02: continue
        y = y0 + 170 + j * 82; aa = int(a * q)
        col = AMBER if ltv < 90 else RED
        d.text((x0 + 40, y), lab, font=F("k", 44), fill=WHITE + (aa,), anchor="lm")
        d.text((x0 + 330, y), pv, font=F("k", 44), fill=WHITE + (aa,), anchor="lm")
        d.text((x0 + 640, y), f"{ltv:.1f}%", font=F("k", 44), fill=col + (aa,), anchor="lm")
        if ltv > 100: d.text((x0 + 830, y), "!", font=F("k", 44), fill=RED + (aa,), anchor="mm")
    im.paste(lay, (0, 0), lay)

def formula(im, s, t):
    if SC[s].get("fx") != "formula": return
    steps = [(1, "Payable at maturity", "₹8,03,000"), (2, "÷ net grams (no stones)", "80 g"), (3, "= danger line / gram", "₹10,037"),
             (3, "× 8 = danger line / pavan", "₹80,300"), (4, "÷ 0.75 = margin-call line / g", "₹13,383"), (5, "Today's 22K price / g", "₹11,420")]
    p = ease(seg(t, .6, 1.3)) * (1 - ease(seg(t, L(s) - .5, L(s))))
    if p <= .02: return
    lay = layer(); d = ImageDraw.Draw(lay); a = int(255 * p)
    x0, y0 = 300, 230; panel(d, (x0, y0, x0 + 1320, y0 + 540), p)
    d.text((x0 + 50, y0 + 52), "YOUR DANGER LINE · EXAMPLE: SREEJA", font=F("b", 26), fill=GOLD + (a,), anchor="lm")
    for j, (k, lab, val) in enumerate(steps):
        tj = ts(s, k) + .3 + (.9 if j == 3 else 0)
        q = ease(seg(t, tj, tj + .5))
        if q <= .02: continue
        y = y0 + 125 + j * 70; aa = int(a * q)
        col = RED if j in (2, 3) else (AMBER if j == 4 else WHITE)
        d.text((x0 + 60, y), lab, font=F("s", 38), fill=(220, 228, 232, aa), anchor="lm")
        d.text((x0 + 1260, y), val, font=F("k", 44), fill=col + (aa,), anchor="rm")
    if t > ts(s, 5) + 1.2:
        q = ease(seg(t, ts(s, 5) + 1.2, ts(s, 5) + 1.8)); aa = int(a * q)
        d.text((x0 + 660, y0 + 510), "Below the margin line · 12% above the danger line", font=F("b", 30), fill=RED + (aa,), anchor="mm")
    im.paste(lay, (0, 0), lay)

def recap(im, s, t):
    if SC[s].get("fx") != "recap": return
    p = ease(seg(t, .4, 1.0)) * (1 - ease(seg(t, L(s) - .5, L(s))))
    if p <= .02: return
    lay = layer(); d = ImageDraw.Draw(lay); a = int(255 * p)
    x0, y0 = 70, 250; panel(d, (x0, y0, x0 + 980, y0 + 500), p)
    for k, (m, e, mv, tg) in enumerate(SC[s]["s"]):
        q = ease(seg(t, ts(s, k) + .2, ts(s, k) + .7))
        if q <= .02: continue
        y = y0 + 70 + k * 88; aa = int(a * q)
        d.ellipse((x0 + 40, y - 30, x0 + 100, y + 30), fill=GOLD + (aa,))
        d.text((x0 + 70, y), str(k + 1), font=F("k", 34), fill=INKD + (aa,), anchor="mm")
        d.text((x0 + 130, y), tg, font=F("k", 44), fill=WHITE + (aa,), anchor="lm")
    im.paste(lay, (0, 0), lay)

def endcard(im, s, t):
    if SC[s].get("fx") != "end" or t < ts(s, 4): return
    p = back(seg(t, ts(s, 4), ts(s, 4) + .5)); d = ImageDraw.Draw(im)
    bw, bh = 480 * p, 112 * p; cx, cy = W / 2, 430
    if p > 0: d.rounded_rectangle([cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2], int(30 * p), fill=(230, 33, 23))
    if p > .8:
        d.text((cx, cy), "SUBSCRIBE", font=F("k", 56), fill=WHITE, anchor="mm")
        d.text((cx, cy + 110), "calcsouq.com", font=F("b", 36), fill=GOLD, anchor="mm")

def subtitle(im, s, t):
    for k, (m, e, mv, tg) in enumerate(SC[s]["s"]):
        t0 = ts(s, k) - .05; t1 = ts(s, k + 1) - .05 if k + 1 < len(SC[s]["s"]) else AUDIO[s] + .5
        if t0 <= t < t1:
            d = ImageDraw.Draw(im); f = F("s", 40); lines = wrap(d, e, f, 1600)
            y0 = 1045 - 56 * len(lines)
            lay = layer(); ld = ImageDraw.Draw(lay)
            w = max(d.textlength(l, font=f) for l in lines) + 60
            ld.rounded_rectangle((W / 2 - w / 2, y0 - 34, W / 2 + w / 2, 1045 - 34 + 30), 16, fill=(0, 0, 0, 150))
            im.paste(lay, (0, 0), lay); d = ImageDraw.Draw(im)
            for j, l in enumerate(lines): d.text((W / 2, y0 + j * 56), l, font=f, fill=WHITE, anchor="mm")
            return

def frame(s, t):
    i = ORDER.index(s); dur = L(s); hasB = os.path.exists(os.path.join(IMG, s + "B.png")) and "B" in SC[s]
    mvA, mvB = MOVES[i % 4], MOVES[(i + 2) % 4]
    if hasB:
        mid = dur * .5; A = cam(s + "A", seg(t, 0, mid + .9), mvA)
        p = seg(t, mid - .7, mid + .7)
        if p > 0:
            B = cam(s + "B", seg(t, mid - .7, dur), mvB); A = Image.blend(A, B, ease(p)) if p < 1 else B
    else:
        A = cam(s + "A", seg(t, 0, dur), mvA)
    if i == 0 and t < .8: A = Image.blend(Image.new("RGB", (W, H)), A, ease(t / .8))
    if t > dur - .35 and i < len(ORDER) - 1: A = Image.blend(A, Image.new("RGB", (W, H)), ease(seg(t, dur - .35, dur)) * .7)
    if i > 0 and t < .35: A = Image.blend(Image.new("RGB", (W, H)), A, .3 + .7 * ease(t / .35))
    im = grade(A)
    chapter(im, s, t); ticker(im, s, t); meter(im, s, t); stress(im, s, t); formula(im, s, t); recap(im, s, t); card(im, s, t); endcard(im, s, t); subtitle(im, s, t)
    d = ImageDraw.Draw(im); d.text((W - 60, 1062), "CalcSouq", font=F("b", 22), fill=(220, 220, 225), anchor="rm")
    return im

def render(s, out_dir="/tmp/ytgl"):
    os.makedirs(out_dir, exist_ok=True); out = f"{out_dir}/{s}.mp4"; tmp = f"{out_dir}/{s}.tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p", "-r", str(FPS), tmp], stdin=subprocess.PIPE)
    n = round(L(s) * FPS)
    for i in range(n): p.stdin.write(frame(s, i / FPS).tobytes())
    p.stdin.close(); assert p.wait() == 0; os.replace(tmp, out); print(out, n / FPS, flush=True)

def timeline():
    off, out = 0.0, {}
    for s in ORDER: out[s] = round(off, 3); off += round(L(s) * FPS) / FPS
    return out, off

def write_srt(path, lang):
    def stamp(x): h, r = divmod(x, 3600); m, sec = divmod(r, 60); return f"{int(h):02}:{int(m):02}:{int(sec):02},{int(round((sec % 1) * 1000)) % 1000:03}"
    st, _ = timeline(); n, out = 1, []
    for s in ORDER:
        rows = SC[s]["s"]
        for k, (m, e, mv, tg) in enumerate(rows):
            t0 = ts(s, k); t1 = ts(s, k + 1) if k + 1 < len(rows) else AUDIO[s] + .3
            out.append(f"{n}\n{stamp(st[s] + t0)} --> {stamp(st[s] + t1)}\n{e if lang == 'en' else m}\n"); n += 1
    open(path, "w").write("\n".join(out)); print(path, n - 1)

if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "--frame": frame(a[1], float(a[2])).save(a[3])
    elif a and a[0] in ("--srt-en", "--srt-ml"): write_srt(a[1], a[0][-2:])
    elif a and a[0] == "--timeline": print(json.dumps(timeline(), indent=1))
    else:
        for s in a: render(s)
