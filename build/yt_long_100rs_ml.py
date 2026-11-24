"""CalcSouq Malayalam long video: "₹100 a day in Kochi" animated experiment (1920x1080).
Two AI 3D stills per scene (build/reel_assets/2026-11-25-100rs/, ElevenLabs flow xIQdFvxv4IA1bxpleMvH) with slow
Ken Burns moves and a crossfade, a Malayalam chapter chip, Appu's wallet counter, fact tags and burnt-in English subtitles.
Usage: python3 yt_long_100rs_ml.py S01 S02 ... | --frame S06 8 out.png | --srt-en out.srt | --srt-ml out.srt | --timeline
"""
import sys, os, json, subprocess, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from yt_long_rates import F, seg, ease, back, lerp, mix, T, wrap, shadow
from PIL import Image, ImageDraw, ImageFilter, ImageFont
W, H, FPS = 1920, 1080, 30
HERE = os.path.dirname(os.path.abspath(__file__))
FOLDER = os.path.join(HERE, "youtube/long/2026-11-25-100-rupees-a-day-malayalam")
IMG = os.path.join(HERE, "reel_assets/2026-11-25-100rs")
SC = json.load(open(os.path.join(FOLDER, "scenes.json")))
ORDER = list(SC.keys())
AUDIO = json.load(open(os.path.join(FOLDER, "audio.json")))
PAD = 0.6
GOLD = (255, 205, 60); WHITE = (255, 255, 255); RED = (235, 70, 70); GREEN = (70, 200, 120)
_MF = {}
def MF(s):
    if s not in _MF: _MF[s] = ImageFont.truetype(os.path.join(HERE, "fonts/Manjari-Bold.ttf"), int(s), layout_engine=ImageFont.Layout.RAQM)
    return _MF[s]
def L(s): return AUDIO[s] + PAD
def ts(s, k):
    lens = [len(m) + 1 for m, *_ in SC[s]["s"]]; return AUDIO[s] * sum(lens[:k]) / sum(lens)

_IM = {}
def img(k):
    if k not in _IM:
        k = {"S01A": "S01B", "S16B": "S16A"}.get(k, k)
        p = os.path.join(IMG, k + ".png")
        if not os.path.exists(p): p = os.path.join(IMG, k[:-1] + "A.png")
        im = Image.open(p).convert("RGB")
        _IM[k] = im.resize((int(W * 1.25), int(H * 1.25)), Image.LANCZOS)
    return _IM[k]

MOVES = [(1.0, 1.12, .5, .5, .5, .45), (1.12, 1.0, .45, .5, .55, .5), (1.04, 1.14, .4, .55, .6, .48), (1.1, 1.02, .6, .45, .45, .55)]
def cam(k, p, mv):
    z0, z1, x0, y0, x1, y1 = mv; q = ease(p) * .6 + p * .4
    im = img(k); z = lerp(z0, z1, q)
    vw = im.width * 0.8 / z; vh = vw * H / W
    cx = lerp(x0, x1, q) * im.width; cy = lerp(y0, y1, q) * im.height
    cx = min(max(cx, vw / 2), im.width - vw / 2); cy = min(max(cy, vh / 2), im.height - vh / 2)
    return im.crop((int(cx - vw / 2), int(cy - vh / 2), int(cx + vw / 2), int(cy + vh / 2))).resize((W, H), Image.BILINEAR)

_VG = None
def vignette(im):
    global _VG
    if _VG is None:
        m = Image.new("L", (W, H), 0); d = ImageDraw.Draw(m)
        for y in range(H):
            a = 0
            if y > H - 330: a = 200 * ((y - (H - 330)) / 330) ** 1.4
            if y < 200: a = max(a, 150 * (1 - y / 200) ** 1.6)
            d.line([(0, y), (W, y)], fill=int(a))
        _VG = m
    im.paste((0, 0, 0), (0, 0), _VG); return im

def chip(im, s, t):
    ml, en = SC[s]["head"]; p = min(ease(seg(t, .2, .9)), 1 - ease(seg(t, 6.0, 6.6)))
    if p <= 0.02: return
    d = ImageDraw.Draw(im); f1 = MF(52); f2 = F("b", 24)
    w = max(d.textlength(ml, font=f1), d.textlength(en.upper(), font=f2)) + 70
    x = 60 - (1 - p) * 60; box = (x, 60, x + w, 190)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    ld.rounded_rectangle(box, 26, fill=(12, 14, 24, int(200 * p))); ld.rounded_rectangle((x, 60, x + 10, 190), 5, fill=GOLD + (int(255 * p),))
    ld.text((x + 34, 108), ml, font=f1, fill=WHITE + (int(255 * p),), anchor="lm")
    ld.text((x + 34, 162), en.upper(), font=f2, fill=GOLD + (int(255 * p),), anchor="lm")
    im.paste(lay, (0, 0), lay)

# wallet state through the story (S01..S12)
WALLET_SCENES = ["S01", "S02", "S03", "S04", "S04B", "S05", "S06", "S07", "S08", "S09", "S10", "S11", "S12"]
def wallet_at(s, t):
    if s not in WALLET_SCENES: return None
    val = None
    for sc in WALLET_SCENES[:WALLET_SCENES.index(s) + 1]:
        for k, (m, e, wv, tg) in enumerate(SC[sc]["s"]):
            if wv is None: continue
            if sc == s and ts(s, k) > t: return val if val is not None else wv, (val, wv, ts(s, k))
            val = wv
    return val, None

def wallet(im, s, t):
    r = wallet_at(s, t)
    if not r or r[0] is None: return
    v, nxt = r
    # animate the count in the 1.2 s after a change
    for k, (m, e, wv, tg) in enumerate(SC[s]["s"]):
        t0 = ts(s, k)
        if wv is not None and t0 <= t < t0 + 1.2:
            prev = wallet_prev(s, k)
            if prev is not None: v = round(lerp(prev, wv, ease(seg(t, t0, t0 + 1.0))))
    d = ImageDraw.Draw(im); x1 = W - 60; box = (x1 - 330, 60, x1, 190)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    ld.rounded_rectangle(box, 26, fill=(12, 14, 24, 205))
    col = GREEN if v >= 50 else (GOLD if v >= 20 else RED)
    ld.text((x1 - 165, 96), "APPU'S WALLET", font=F("b", 22), fill=(200, 205, 220, 255), anchor="mm")
    ld.text((x1 - 165, 148), f"₹{v}", font=F("k", 64), fill=col + (255,), anchor="mm")
    im.paste(lay, (0, 0), lay)

def wallet_prev(s, k):
    prev = None
    for sc in WALLET_SCENES[:WALLET_SCENES.index(s) + 1]:
        for j, (m, e, wv, tg) in enumerate(SC[sc]["s"]):
            if sc == s and j >= k: return prev
            if wv is not None: prev = wv
    return prev

def tags(im, s, t):
    for k, (m, e, wv, tg) in enumerate(SC[s]["s"]):
        if not tg: continue
        t0 = ts(s, k) + .3; t1 = (ts(s, k + 1) if k + 1 < len(SC[s]["s"]) else L(s)) + .2
        p = min(back(seg(t, t0, t0 + .45)), 1 - ease(seg(t, t1, t1 + .3)))
        if p <= 0.02: continue
        d = ImageDraw.Draw(im); f = F("k", 58); tw = d.textlength(tg, font=f)
        bad = any(x in tg for x in ("FAILED", "NO", "Short", "−", "Needs"))
        bg = (210, 50, 50) if bad else (245, 195, 0); fg = WHITE if bad else (18, 16, 10)
        cx, cy = W / 2, 560; w, h = (tw + 90) * p, 112 * p
        box = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2); shadow(im, box, int(h / 2), 22, 120, (0, 10))
        d = ImageDraw.Draw(im); d.rounded_rectangle(box, int(h / 2), fill=bg)
        if p > .85: d.text((cx, cy), tg, font=f, fill=fg, anchor="mm")

def subtitle(im, s, t):
    for k, (m, e, wv, tg) in enumerate(SC[s]["s"]):
        t0 = ts(s, k) - .05; t1 = ts(s, k + 1) - .05 if k + 1 < len(SC[s]["s"]) else AUDIO[s] + .5
        if t0 <= t < t1:
            d = ImageDraw.Draw(im); f = F("s", 42); lines = wrap(d, e, f, 1560)
            y0 = 1040 - 58 * len(lines)
            for j, l in enumerate(lines):
                yy = y0 + j * 58
                d.text((W / 2 + 3, yy + 3), l, font=f, fill=(0, 0, 0), anchor="mm")
                d.text((W / 2, yy), l, font=f, fill=WHITE, anchor="mm", stroke_width=2, stroke_fill=(0, 0, 0))
            return

def endcard(im, s, t):
    if s != ORDER[-1] or t < ts(s, 4): return
    p = back(seg(t, ts(s, 4), ts(s, 4) + .5)); d = ImageDraw.Draw(im)
    bw, bh = 460 * p, 110 * p; cx, cy = W / 2, 400
    if p > 0: d.rounded_rectangle([cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2], int(30 * p), fill=(230, 33, 23))
    if p > .8: d.text((cx, cy), "SUBSCRIBE", font=F("k", 56), fill=WHITE, anchor="mm")

def frame(s, t):
    i = ORDER.index(s); dur = L(s); mid = dur * .5
    mvA, mvB = MOVES[i % 4], MOVES[(i + 2) % 4]
    A = cam(s + "A", seg(t, 0, mid + 1.2), mvA)
    p = seg(t, mid - .6, mid + .6)
    if p > 0:
        B = cam(s + "B", seg(t, mid - .6, dur), mvB)
        A = Image.blend(A, B, ease(p)) if p < 1 else B
    if s == ORDER[0] and t < .8: A = Image.blend(Image.new("RGB", (W, H)), A, ease(t / .8))
    im = vignette(A)
    chip(im, s, t); wallet(im, s, t); tags(im, s, t); endcard(im, s, t); subtitle(im, s, t)
    d = ImageDraw.Draw(im); d.text((W - 60, 1062), "CalcSouq", font=F("b", 22), fill=(220, 220, 225), anchor="rm")
    return im

def render(s, out_dir="/tmp/yt100"):
    os.makedirs(out_dir, exist_ok=True); out = f"{out_dir}/{s}.mp4"; tmp = f"{out_dir}/{s}.tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-r", str(FPS), tmp], stdin=subprocess.PIPE)
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
        for k, (m, e, wv, tg) in enumerate(rows):
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
