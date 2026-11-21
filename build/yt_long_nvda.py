"""CalcSouq YouTube long video #2: Why Nvidia & AI stocks are crashing (16:9). Reuses helpers from yt_long_rates.
Usage: python3 yt_long_nvda.py S1 S2 ... | --frame S3 10 out.png | --srt out.srt
"""
import sys, os, math, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import yt_long_rates as R
from yt_long_rates import fx, F, INK, GOLD, WHITE, OFF, RED, GREEN, BLUE, PINK, PURPLE, ORANGE, seg, ease, back, lerp, mix, clamp, count
from yt_long_rates import vis, card, T, wrap, arrow, up_arrow, bank, house, loan_doc, heading, brand, shadow
from PIL import ImageDraw
W, H = 1920, 1080
HERE = os.path.dirname(os.path.abspath(__file__))
R.TEXT = json.load(open(os.path.join(HERE, "youtube/long/2026-11-22-nvidia-ai-crash/scenes.json")))
R.AUDIO = {"S1": 25.6, "S2": 23.28, "S3": 24.72, "S4": 28.64, "S5": 17.28, "S6": 20.72, "S7": 26.16, "S8": 25.6}
R.REPL += [(tuple(a.split()), b) for a, b in [
    ("fourteen percent", "14%"), ("march twenty twenty", "March 2020"), ("s and p five hundred", "S&P 500"),
    ("two hundred and thirty-nine dollars", "$239"), ("six trillion dollars", "$6 trillion"),
    ("one hundred and twenty-five dollars", "$125"), ("forty-seven percent", "47%"), ("twenty-three percent", "23%"),
    ("october two thousand and eight", "October 2008"), ("november third", "3 November"), ("november twelfth", "12 November"),
    ("thirty-three years", "33 years"), ("one thousand dollars", "$1,000"), ("five hundred and twenty-five dollars", "$525"),
    ("one thousand", "1,000"), ("ninety-one percent", "91%"), ("fifty percent", "50%"), ("one hundred percent", "100%"),
    ("two thousand", "2000"), ("eighty percent", "80%"), ("twenty twenty-two", "2022")]]
at = R.at

def chip(img, cx, cy, s, p, label="AI", col=(40, 44, 56)):
    if p <= 0.01: return
    s *= p; shadow(img, (cx - 120 * s, cy - 120 * s, cx + 120 * s, cy + 120 * s), 20, 22, 90, (0, 12)); d = ImageDraw.Draw(img); lw = max(2, int(5 * s))
    for k in range(5):
        o = -80 + k * 40
        for (x1, y1, x2, y2) in [(cx + o * s, cy - 150 * s, cx + o * s, cy - 110 * s), (cx + o * s, cy + 110 * s, cx + o * s, cy + 150 * s),
                                 (cx - 150 * s, cy + o * s, cx - 110 * s, cy + o * s), (cx + 110 * s, cy + o * s, cx + 150 * s, cy + o * s)]:
            d.line([(x1, y1), (x2, y2)], fill=(200, 205, 215), width=max(2, int(10 * s)))
    d.rounded_rectangle([cx - 120 * s, cy - 120 * s, cx + 120 * s, cy + 120 * s], int(22 * s), fill=col, outline=INK, width=lw)
    d.rounded_rectangle([cx - 75 * s, cy - 75 * s, cx + 75 * s, cy + 75 * s], int(14 * s), fill=GOLD, outline=INK, width=lw)
    if p > 0.7: T(d, cx, cy, label, int(64 * s), INK, "k")

def server(img, cx, cy, s, p, t=0):
    if p <= 0.01: return
    s *= p; shadow(img, (cx - 90 * s, cy - 150 * s, cx + 90 * s, cy + 150 * s), 14, 20, 80, (0, 10)); d = ImageDraw.Draw(img); lw = max(2, int(5 * s))
    d.rounded_rectangle([cx - 90 * s, cy - 150 * s, cx + 90 * s, cy + 150 * s], int(14 * s), fill=(55, 60, 75), outline=INK, width=lw)
    for i in range(5):
        y = cy - 125 * s + i * 55 * s; d.rounded_rectangle([cx - 70 * s, y, cx + 70 * s, y + 40 * s], int(6 * s), fill=(30, 34, 44))
        on = (int(t * 4) + i) % 3 != 0; d.ellipse([cx + 40 * s, y + 13 * s, cx + 54 * s, y + 27 * s], fill=GREEN if on else (40, 90, 60))
        d.rectangle([cx - 55 * s, y + 16 * s, cx + 10 * s, y + 24 * s], fill=(90, 96, 110))

def chair(img, cx, cy, s, p):
    if p <= 0.01: return
    s *= p; d = ImageDraw.Draw(img); lw = max(2, int(6 * s))
    d.rounded_rectangle([cx - 70 * s, cy - 150 * s, cx + 70 * s, cy - 10 * s], int(24 * s), fill=(120, 80, 60), outline=INK, width=lw)
    d.rounded_rectangle([cx - 85 * s, cy - 20 * s, cx + 85 * s, cy + 20 * s], int(14 * s), fill=(140, 95, 70), outline=INK, width=lw)
    d.rectangle([cx - 8 * s, cy + 20 * s, cx + 8 * s, cy + 90 * s], fill=INK)
    for dx in (-60, 0, 60): d.line([(cx, cy + 90 * s), (cx + dx * s, cy + 120 * s)], fill=INK, width=lw)
    if p > 0.8: T(d, cx, cy - 80 * s, "?", int(80 * s), GOLD, "k")

def capitol(img, cx, cy, s, p):
    if p <= 0.01: return
    s *= p; d = ImageDraw.Draw(img); lw = max(2, int(5 * s)); col = OFF
    d.pieslice([cx - 80 * s, cy - 200 * s, cx + 80 * s, cy - 40 * s], 180, 360, fill=col, outline=INK, width=lw)
    d.rectangle([cx - 6 * s, cy - 235 * s, cx + 6 * s, cy - 195 * s], fill=INK)
    bank(img, cx, cy + 40 * s, s, 1)

def price_chart(img, box, p, t, pts, col=RED, labels=None):
    x0, y0, x1, y1 = box; d = ImageDraw.Draw(img); vmin, vmax = 100, 260
    d.line([(x0, y1), (x1, y1)], fill=(120, 125, 140), width=3)
    for v in (125, 175, 225):
        y = lerp(y1, y0, (v - vmin) / (vmax - vmin)); d.line([(x0, y), (x1, y)], fill=(70, 74, 90), width=1)
        T(d, x0 - 20, y, f"${v}", 26, (170, 172, 185), "s", "rm")
    n = len(pts) - 1; xy = [(lerp(x0, x1, i / n), lerp(y1, y0, (v - vmin) / (vmax - vmin))) for i, v in enumerate(pts)]
    m = p * n; k = int(m); path = xy[:k + 1]
    if k < n: path.append((lerp(xy[k][0], xy[k + 1][0], m - k), lerp(xy[k][1], xy[k + 1][1], m - k)))
    if len(path) > 1: d.line(path, fill=col, width=10, joint="curve")
    ex, ey = path[-1]; d.ellipse([ex - 14, ey - 14, ex + 14, ey + 14], fill=col, outline=WHITE, width=4)
    if labels:
        for txt, xi in labels: T(d, lerp(x0, x1, xi), y1 + 34, txt, 28, (190, 192, 205), "s")
    return ex, ey

# =========================== scenes ===========================
def S1(t):
    s = "S1"; img = fx.scene_bg(t, "night", 101); brand(img)
    heading(img, "Nvidia lost almost half its value", t, 0.15, {"half"})
    tc = at(s, "On Friday"); pc = vis(t, 0.5)
    chip(img, 560, 520, 1.25 * (1 - 0.15 * ease(seg(t, tc, tc + 1))), pc, "AI", mix((40, 44, 56), (120, 30, 40), ease(seg(t, tc, tc + 1))))
    d = ImageDraw.Draw(img)
    if t > 1.2:  # falling line
        pts = [(770, 330), (830, 380), (880, 480), (930, 560), (990, 760)]
        q = ease(seg(t, 1.2, 3.5)); n = q * 4; k = int(n); path = pts[:k + 1]
        if k < 4: path.append((lerp(pts[k][0], pts[k + 1][0], n - k), lerp(pts[k][1], pts[k + 1][1], n - k)))
        if len(path) > 1: d.line(path, fill=RED, width=12)
    fx.pill(img, 1350, 300, "−14% on Friday", t, tc, RED, WHITE, 48, 40)
    tn = at(s, "The Nasdaq"); fx.pill(img, 1350, 410, "Nasdaq: worst week since 2020", t, tn, WHITE, INK, 40, 34)
    tsp = at(s, "the S and P"); fx.pill(img, 1350, 520, "S&P 500 & Dow: correction", t, tsp, WHITE, INK, 40, 34)
    tq = at(s, "So what happened")
    if t > tq:
        fx.souq(img, 1350, 810, 0.5 * back(seg(t, tq, tq + .5)) + 1e-3, t, "shocked")
        fx.speech(img, 1580, 710, "Bubble bursting?", at(s, "Is the AI bubble"), t, 34)
    R.subtitle(img, s, t); return img

def S2(t):
    s = "S2"; img = fx.scene_bg(t, "night", 102); brand(img)
    heading(img, "From record to −47%", t, 0.15, {"−47%"})
    pts = [215, 230, 239, 228, 214, 200, 182, 163, 156, 146, 125.53]
    tr = at(s, "In early October"); tf = at(s, "By Friday")
    p = 0.18 * ease(seg(t, tr, tr + 1.5)) + 0.82 * ease(seg(t, tf - 0.5, tf + 3))
    ex, ey = price_chart(img, (300, 260, 1250, 820), p, t, pts, RED, [("Sep", 0), ("6 Oct", 0.2), ("Nov", 0.6), ("20 Nov", 1)])
    d = ImageDraw.Draw(img)
    if t > tr + 0.5: fx.pill(img, 500, 230, "Record ≈ $239", t, tr + .5, GOLD, INK, 38, 30)
    if t > tf:
        v = count(239, 125.53, t, tf, tf + 3); T(d, 1560, 380, f"${v:,.2f}", 110, WHITE, "k")
        T(d, 1560, 470, "Nvidia close, Fri 20 Nov", 32, (180, 182, 195), "s")
    tp = at(s, "That's a fall")
    if t > tp: fx.pill(img, 1560, 580, "−47% from record", t, tp, RED, WHITE, 46, 40)
    tw = at(s, "Last week")
    if t > tw: fx.pill(img, 1600, 680, "Week: −23% · worst since 2008", t, tw, WHITE, INK, 34, 30)
    R.subtitle(img, s, t); return img

def S3(t):
    s = "S3"; img = fx.scene_bg(t, "berry", 103); brand(img)
    heading(img, "Reason 1: spending vs profit", t, 0.15, {"1:"})
    ts = at(s, "Big tech"); d = ImageDraw.Draw(img)
    for i, x in enumerate((360, 560, 760)): server(img, x, 540, 1.0, vis(t, ts + i * .2), t)
    if t > ts + .5:
        for k in range(6):
            u = ((t - ts) * 0.6 + k / 6) % 1.0; fx.coin(ImageDraw.Draw(img), lerp(1000, 820, u), lerp(260, 420, u) + 40 * math.sin(u * 3), 26, GOLD, "$")
        fx.pill(img, 1100, 240, "Hundreds of billions", t, ts + .5, GOLD, INK, 36, 30)
    tq = at(s, "how fast"); d = ImageDraw.Draw(img)
    if t > tq:
        arrow(d, 900, 560, 1180, 560, ease(seg(t, tq, tq + .6)), WHITE, 10)
        c = card(img, (1210, 430, 1610, 690), vis(t, tq + .4))
        if c: T(c, 1410, 520, "Profit?", 70, INK, "k"); T(c, 1410, 610, "how fast?", 40, (110, 115, 125), "b")
    tb = at(s, "latest results beat")
    if t > tb: fx.pill(img, 1410, 770, "Results beat expectations ✓", t, tb, GREEN, WHITE, 34, 30)
    td = at(s, "priced for perfection")
    if t > td: fx.pill(img, 960, 880, "Priced for perfection → doubt hurts", t, td, WHITE, INK, 38, 34)
    R.subtitle(img, s, t); return img

def S4(t):
    s = "S4"; img = fx.scene_bg(t, "sky", 104); brand(img)
    heading(img, "Reasons 2 & 3: politics, leadership", t, 0.15, {"2", "3:"}, size=70)
    tp = at(s, "After the US"); pa = vis(t, tp - .4)
    d = card(img, (180, 230, 900, 860), pa)
    if pa > 0.05:
        capitol(img, 540, 470, 0.75, pa); d = ImageDraw.Draw(img)
        if pa > .8:
            T(d, 540, 620, "US midterms · 3 Nov", 42, INK, "k")
            tw = at(s, "tighter rules")
            if t > tw: T(d, 540, 700, "Tighter AI rules?", 38, RED, "b")
            if t > at(s, "local opposition"): T(d, 540, 770, "Data-centre pushback", 38, RED, "b")
    tl = at(s, "Reason three"); pb = vis(t, tl - .3)
    d = card(img, (1020, 230, 1740, 860), pb)
    if pb > 0.05:
        chair(img, 1380, 480, 1.0, pb); d = ImageDraw.Draw(img)
        if pb > .8:
            th = at(s, "On November twelfth")
            if t > th: T(d, 1380, 680, "CEO resigned · 12 Nov", 42, INK, "k")
            if t > at(s, "Finance chief"): T(d, 1380, 760, "Interim CEO: Colette Kress", 36, (90, 95, 105), "b")
    R.subtitle(img, s, t); return img

def S5(t):
    s = "S5"; img = fx.scene_bg(t, "mint", 105); brand(img)
    heading(img, "Reason 4: interest rates", t, 0.15, {"4:"})
    tf = at(s, "Markets now expect"); d = ImageDraw.Draw(img)
    if t > tf:
        bank(img, 420, 560, 0.9, vis(t, tf - .2), "Federal Reserve")
        up_arrow(ImageDraw.Draw(img), 600, 380, 0.8 * back(seg(t, tf + .5, tf + 1)) + 1e-3, RED)
        fx.pill(img, 420, 820, "Hike expected in December", t, tf + .6, GOLD, INK, 34, 30)
    th = at(s, "Higher rates make")
    if t > th:
        shrink = 1 - 0.45 * ease(seg(t, th + 1, th + 4)); d = ImageDraw.Draw(img)
        T(d, 1300, 300, "Profit in 2035", 44, WHITE, "k")
        fx.coins_stack(d, 1180, 640, int(1 + 6 * shrink), 60, "$")
        T(d, 1500, 470, "Value today", 40, WHITE, "s")
        T(d, 1500, 550, "shrinks ↓" if shrink < 0.9 else "…", 70, RED if shrink < 0.9 else GOLD, "k")
        T(d, 1300, 360, "(illustration)", 28, (190, 220, 210), "s")
    tt = at(s, "That hits")
    if t > tt: fx.pill(img, 1340, 820, "Growth stocks hit hardest", t, tt, RED, WHITE, 40, 34)
    R.subtitle(img, s, t); return img

def S6(t):
    s = "S6"; img = fx.scene_bg(t, "berry", 106); brand(img)
    heading(img, "The maths of a crash", t, 0.15, {"crash"})
    ta, tb = at(s, "If you had put"), at(s, "To get back")
    for i, (tt, top, val, col, sub) in enumerate([(ta, "$1,000 at the record", None, INK, "6 Oct"), (ta + 3.5, "Worth now", 524.70, RED, "20 Nov")]):
        x0 = 260 if i == 0 else 1060; c = card(img, (x0, 260, x0 + 600, 560), vis(t, tt))
        if c:
            T(c, x0 + 300, 320, top, 40, (100, 105, 115), "b")
            v = 1000 if val is None else count(1000, val, t, tt + .2, tt + 2)
            T(c, x0 + 300, 430, f"${v:,.0f}", 110, col if val else GREEN, "k"); T(c, x0 + 300, 520, sub, 32, (120, 125, 135), "s")
    if t > ta + 3.5: arrow(ImageDraw.Draw(img), 875, 410, 1045, 410, ease(seg(t, ta + 3.5, ta + 4)), WHITE, 10)
    if t > tb: fx.pill(img, 960, 650, "To get back: +91% needed", t, tb, GOLD, INK, 50, 44)
    tg = at(s, "In general")
    if t > tg:
        d = ImageDraw.Draw(img); p = ease(seg(t, tg + .3, tg + 1.8))
        T(d, 330, 790, "−50%", 44, RED, "k", "rm"); d.rounded_rectangle([360, 770, 360 + 500 * p, 810], 20, fill=RED)
        T(d, 330, 860, "+100%", 44, GREEN, "k", "rm"); d.rounded_rectangle([360, 840, 360 + 1000 * p, 880], 20, fill=GREEN)
        if p > .9: T(d, 1420, 860, "to break even", 38, WHITE, "b", "lm")
    R.subtitle(img, s, t); return img

def S7(t):
    s = "S7"; img = fx.scene_bg(t, "night", 107); brand(img)
    heading(img, "Is the AI bubble bursting?", t, 0.15, {"bubble"})
    tn = at(s, "Nobody knows")
    if t < at(s, "After the dot-com") + .2:
        fx.souq(img, 960, 560, 0.75 * back(seg(t, .3, .8)) + 1e-3, t, "thinking"); fx.speech(img, 960, 330, "Nobody knows for sure", tn, t, 40)
    else:
        td = at(s, "After the dot-com"); tv = at(s, "Nvidia itself")
        for i, (tt, yr, l1, l2) in enumerate([(td, "2000", "Nasdaq −78%", "Then the internet kept growing"), (tv, "2022", "Nvidia ≈ −66%", "Then AI demand → new records")]):
            x0 = 230 if i == 0 else 1030; c = card(img, (x0, 260, x0 + 660, 720), vis(t, tt))
            if c:
                T(c, x0 + 330, 330, yr, 60, (110, 115, 125), "k"); T(c, x0 + 330, 450, l1, 70, RED, "k")
                f = F("b", 38)
                for j, ln in enumerate(wrap(c, l2, f, 560)): c.text((x0 + 330, 560 + j * 50), ln, font=f, fill=GREEN, anchor="mm")
        tm = at(s, "Share prices and")
        if t > tm: fx.pill(img, 960, 830, "Share prices ≠ technology", t, tm, GOLD, INK, 46, 40)
    R.subtitle(img, s, t); return img

def S8(t):
    s = "S8"; img = fx.scene_bg(t, "night", 108); brand(img)
    heading(img, "What to watch next", t, 0.15, {"next"})
    d = ImageDraw.Draw(img)
    items = [("how much big tech", "Big tech AI spending plans"), ("the Fed's decision", "Fed decision in December"), ("new rules on AI", "New AI & data-centre rules"), ("who becomes", "Nvidia's next CEO")]
    for i, (ph, line) in enumerate(items):
        tt = at(s, ph); p = ease(seg(t, tt - .2, tt + .3))
        if p > 0:
            y = 280 + i * 105; x = 190 - 60 * (1 - p); d.ellipse([x, y - 28, x + 56, y + 28], fill=GOLD)
            T(d, x + 28, y, str(i + 1), 34, INK, "k"); T(d, x + 85, y, line, 46, WHITE, "k", "lm")
    te = at(s, "This video is for education")
    if t > te: T(d, 190, 720, "Education only · not investment advice", 32, (170, 172, 185), "s", "lm")
    tc = at(s, "calc souq dot com")
    if t > tc:
        fx.pill(img, 1450, 380, "calcsouq.com", t, tc, GOLD, INK, 70, 56)
        if t > tc + .6: T(ImageDraw.Draw(img), 1450, 480, "Free percentage calculator", 36, WHITE, "s")
    tsub = at(s, "subscribe")
    if t > tsub:
        p = back(seg(t, tsub, tsub + .4)); bw, bh = 420 * p, 110 * p; cx, cy = 1450, 650
        shadow(img, (cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2), 30, 20, 90); d = ImageDraw.Draw(img)
        d.rounded_rectangle([cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2], int(30 * p), fill=(230, 33, 23))
        if p > .8: T(d, cx + 30, cy, "SUBSCRIBE", 50, WHITE, "k"); R.bell(d, cx - 150 + math.sin((t - tsub) * 10) * 6 * math.exp(-(t - tsub)), cy - 6, 0.8)
        fx.souq(img, 1700, 830, 0.42, t, "happy", wave=True)
    R.subtitle(img, s, t); return img

R.SCENES = {k: globals()[k] for k in ("S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8")}

if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "--srt": R.write_srt(a[1])
    elif a and a[0] == "--frame": R.SCENES[a[1]](float(a[2])).convert("RGB").save(a[3])
    else:
        for s in a: R.render(s, "/tmp/ytn")
