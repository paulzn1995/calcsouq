"""YouTube Shorts, 23 Nov 2026: top world money news (Malayalam + English, text + music, no narration).
1080x1920, 25 s, reading pace (every line ≥3 s, at most 2 new items at once).
Render:  python3 build/yt_shorts_2026_11_23.py <n> out_silent.mp4      (n = 1, 2, 3)
Frame:   python3 build/yt_shorts_2026_11_23.py <n> --frame <t> out.png
Facts (checked 23 Nov 2026, two sources each) are in build/youtube/2026-11-23-pack.md.
"""
import sys, os, subprocess, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_fx import *
from PIL import ImageFont

DUR = 25.0
_MLF = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts", "Manjari-Bold.ttf")
def MF(s): return ImageFont.truetype(_MLF, int(s), layout_engine=ImageFont.Layout.RAQM)
GREY = (200, 202, 212)

# ---------------- helpers ----------------
def ml(img, txt, y, t, t0, size, col):
    p = ease(seg(t, t0, t0 + .6))
    if p <= 0: return
    f = MF(size); d0 = ImageDraw.Draw(img)
    while d0.textlength(txt, font=f) > W - 120 and size > 50: size -= 4; f = MF(size)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    d.text((W / 2, y + (1 - p) * 40), txt, font=f, fill=col + (int(255 * p),), anchor="mm", stroke_width=2, stroke_fill=col + (int(255 * p),))
    img.paste(layer, (0, 0), layer)

def en(img, txt, y, t, t0, size=52, col=WHITE, font="b"):
    p = ease(seg(t, t0, t0 + .6))
    if p <= 0: return
    f = F(font, size); d0 = ImageDraw.Draw(img)
    while d0.textlength(txt, font=f) > W - 120 and size > 44: size -= 2; f = F(font, size)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    d.text((W / 2, y + (1 - p) * 30), txt, font=f, fill=col + (int(255 * p),), anchor="mm")
    img.paste(layer, (0, 0), layer)

def big(img, txt, y, t, t0, size=200, col=RED):
    if t < t0: return
    f = F("k", size); d = ImageDraw.Draw(img)
    while d.textlength(txt, font=f) > W - 100: size -= 6; f = F("k", size)
    s = 1 + 0.25 * (1 - back(seg(t, t0, t0 + .4)))
    # soft glow
    glow = Image.new("L", (W, H), 0); ImageDraw.Draw(glow).text((W / 2, y), txt, font=F("k", size * s), anchor="mm", fill=150)
    img.paste(col, (0, 0), glow.filter(ImageFilter.GaussianBlur(28)))
    d.text((W / 2, y), txt, font=F("k", size * s), fill=col, anchor="mm", stroke_width=4, stroke_fill=(20, 20, 26))

def card(img, y, txt, i, t, t0, accent=GOLD, val=None, vcol=RED):
    p = back(seg(t, t0, t0 + .6))
    if p <= 0: return
    x = 90 + (1 - p) * 80; r = x + 900
    shadow(img, (x, y - 75, r, y + 75), 36, 16, 90, (0, 10)); d = ImageDraw.Draw(img)
    d.rounded_rectangle([x, y - 75, r, y + 75], 36, fill=WHITE)
    d.rounded_rectangle([x, y - 75, x + 14, y + 75], 7, fill=accent)
    d.ellipse([x + 34, y - 38, x + 110, y + 38], fill=accent); d.text((x + 72, y), str(i), font=F("k", 46), fill=INK, anchor="mm")
    size = 46; f = F("b", size); room = (r - x - 160) - (d.textlength(val, font=F("k", 54)) + 30 if val else 0)
    while d.textlength(txt, font=f) > room and size > 44: size -= 1; f = F("b", size)
    d.text((x + 136, y), txt, font=f, fill=INK, anchor="lm")
    if val: d.text((r - 34, y), val, font=F("k", 54), fill=vcol, anchor="rm")

def panel(img, box, t, t0):
    p = back(seg(t, t0, t0 + .5))
    if p <= 0: return False
    cx, cy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2; w, h = (box[2] - box[0]) * p / 2, (box[3] - box[1]) * p / 2
    b = (cx - w, cy - h, cx + w, cy + h); shadow(img, b, 44, 20, 110, (0, 12)); d = ImageDraw.Draw(img)
    d.rounded_rectangle(b, 44, fill=WHITE); return p > 0.9

def chart(img, x, y, w, h, p, pts, col=RED, grid=True):
    """Shaded line chart; pts are 0..1 heights; p reveals left to right."""
    if p <= 0: return
    d = ImageDraw.Draw(img)
    if grid:
        for k in range(5): d.line([(x, y + h * k / 4), (x + w, y + h * k / 4)], fill=(255, 255, 255, 40) if img.mode == "RGBA" else (60, 62, 80), width=2)
    n = len(pts) - 1; m = p * n; xy = []
    for i in range(int(m) + 1): xy.append((x + w * i / n, y + h * (1 - pts[i])))
    if int(m) < n:
        f = m - int(m); a, b = pts[int(m)], pts[int(m) + 1]; xy.append((x + w * m / n, y + h * (1 - (a + (b - a) * f))))
    if len(xy) < 2: return
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    for k in range(12):  # vertical gradient fill
        a = int(90 * (1 - k / 12))
        poly = xy + [(xy[-1][0], y + h), (xy[0][0], y + h)]
        mask = Image.new("L", (W, H), 0); ImageDraw.Draw(mask).polygon(poly, fill=255)
        band = Image.new("L", (W, H), 0); ImageDraw.Draw(band).rectangle([0, y + h * k / 12 - 40, W, y + h * (k + 1) / 12], fill=a)
        ov.paste(col + (255,), (0, 0), ImageChops.multiply(mask, band))
    img.paste(ov, (0, 0), ov); d = ImageDraw.Draw(img)
    d.line(xy, fill=col, width=12, joint="curve")
    ex, ey = xy[-1]; d.ellipse([ex - 18, ey - 18, ex + 18, ey + 18], fill=WHITE, outline=col, width=8)

def gold_bar3d(img, cx, cy, s):
    if s < 0.05: return
    d = ImageDraw.Draw(img)
    top = [(cx - 120 * s, cy - 50 * s), (cx + 120 * s, cy - 50 * s), (cx + 95 * s, cy - 20 * s), (cx - 95 * s, cy - 20 * s)]
    front = [(cx - 95 * s, cy - 20 * s), (cx + 95 * s, cy - 20 * s), (cx + 170 * s, cy + 60 * s), (cx - 170 * s, cy + 60 * s)]
    shadow(img, (cx - 170 * s, cy + 40 * s, cx + 170 * s, cy + 80 * s), 20, 18, 120, (0, 10)); d = ImageDraw.Draw(img)
    d.polygon([(cx - 120 * s, cy - 50 * s), (cx + 120 * s, cy - 50 * s), (cx + 170 * s, cy + 60 * s), (cx - 170 * s, cy + 60 * s)], fill=(196, 146, 36))
    d.polygon(front, fill=(236, 190, 70), outline=(150, 105, 20))
    d.polygon(top, fill=(255, 226, 130))
    d.line([(cx - 80 * s, cy - 42 * s), (cx + 20 * s, cy - 42 * s)], fill=(255, 245, 200), width=max(2, int(5 * s)))
    if s > 0.3: d.text((cx, cy + 22 * s), "916", font=F("b", 38 * s), fill=(140, 95, 15), anchor="mm")

def coin3d(img, cx, cy, r, sym="₹"):
    d = ImageDraw.Draw(img)
    d.ellipse([cx - r, cy - r + 10, cx + r, cy + r + 10], fill=(170, 120, 20))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(245, 195, 40), outline=(190, 140, 20), width=4)
    d.ellipse([cx - r * .78, cy - r * .78, cx + r * .78, cy + r * .78], outline=(255, 230, 140), width=3)
    d.text((cx, cy), sym, font=F("k", r), fill=(150, 100, 10), anchor="mm")

def falling_coins(img, t, t0, n=7, seed=3):
    if t < t0: return
    rnd = random.Random(seed)
    for k in range(n):
        x = 120 + rnd.random() * 840; sp = 500 + rnd.random() * 400; st = t0 + rnd.random() * 1.0
        if t < st: continue
        y = -80 + (t - st) * sp
        if y < H + 80: coin3d(img, x, y, 40 + rnd.random() * 18)

def end_card(img, t, t0):
    if t < t0: return img
    ml(img, "കൂടുതൽ അറിയാൻ", 520, t, t0, 92, WHITE)
    ml(img, "ചാനൽ സബ്സ്ക്രൈബ് ചെയ്യൂ", 650, t, t0 + .2, 86, GOLD)
    en(img, "Subscribe for daily world money news", 790, t, t0 + .6, 50, WHITE)
    pill(img, W / 2, 960, "SUBSCRIBE", t, t0 + .9, (230, 33, 23), WHITE, 62, 60)
    if t > t0 + 1.2:
        d = ImageDraw.Draw(img); d.text((W / 2, 1100), "calcsouq.com", font=F("k", 64), fill=GOLD, anchor="mm")
        d.text((W / 2, 1180), "Free money calculators", font=F("s", 46), fill=GREY, anchor="mm")
    for k in range(3):
        if t > t0 + .3 + .2 * k: coin3d(img, 360 + k * 180, 1380 + 18 * math.sin(t * 2.5 + k), 64)
    return img

def src(img, txt, t=0):
    if t >= 21.0: return
    d = ImageDraw.Draw(img); size = 34; f = F("s", size)
    while d.textlength(txt, font=f) > W - 80: size -= 1; f = F("s", size)
    d.text((W / 2, 1580), txt, font=f, fill=(170, 172, 185), anchor="mm")

# ---------------- Short 1: Sensex crash ----------------
S1_CUES = "0:boom,0.2:tick*10,2.6:hit,6.0:whoosh,6.6:pop,8.2:pop,12.4:swoosh,13.2:tick*8,15.0:fail,17.4:whoosh,17.8:pop,18.2:pop,21.0:success"
def short1(t):
    img = scene_bg(t, "night", 51)
    if t < 6.0:
        ml(img, "ഷെയറിൽ ഇട്ടവർക്ക്", 250, t, -1, 96, WHITE)
        ml(img, "ഇന്ന് എത്ര പോയി?", 380, t, -1, 112, GOLD)
        v = count(900, 1484, t, 0.0, 2.2)
        big(img, f"−{v:,.0f}", 600, t, -1, 230, RED)
        en(img, "Sensex points lost today · 23 Nov", 760, t, -1, 52, WHITE)
        chart(img, 120, 960, 840, 520, ease(seg(t, -0.3, 2.6)), [.9, .86, .92, .88, .95, .9, .82, .6, .45, .3, .2, .12], RED)
        if t > 3.2: img = shake(img, t, 3.2, 14, .4)
    elif t < 12.4:
        ml(img, "ഇന്ന് എന്ത് സംഭവിച്ചു?", 330, t, 6.0, 92, WHITE)
        en(img, "What happened today", 450, t, 6.2, 54, GOLD)
        card(img, 680, "Sensex closed 82,436", 1, t, 6.6, RED, "−1.77%")
        card(img, 880, "Nifty 50 closed 25,350", 2, t, 8.2, RED, "−1.75%")
        chart(img, 140, 1120, 800, 380, ease(seg(t, 6.6, 9.0)), [.85, .8, .9, .86, .7, .55, .4, .3], RED)
    elif t < 17.4:
        ml(img, "നിങ്ങളുടെ ₹1 ലക്ഷം?", 330, t, 12.4, 100, WHITE)
        en(img, "₹1 lakh in a Nifty index fund", 450, t, 12.6, 54, GOLD)
        if panel(img, (140, 580, 940, 1040), t, 13.0):
            d = ImageDraw.Draw(img)
            v = count(100000, 98250, t, 13.2, 15.0)
            d.text((540, 680), "Value tonight, about", font=F("b", 48), fill=(90, 95, 105), anchor="mm")
            d.text((540, 820), f"₹{v:,.0f}", font=F("k", 140), fill=INK, anchor="mm")
            if t > 15.0: d.text((540, 960), "−₹1,750 in one day", font=F("k", 60), fill=RED, anchor="mm")
        for k in range(3): coin3d(img, 300 + k * 240, 1250 + 30 * math.sin(t * 2 + k), 70)
        if t > 15.0: img = punch(img, t, 15.0, .05)
    elif t < 21.0:
        ml(img, "എന്തുകൊണ്ട്?", 330, t, 17.4, 110, WHITE)
        en(img, "Why it fell", 460, t, 17.5, 56, GOLD)
        card(img, 680, "US AI-stock sell-off spread to Asia", 1, t, 17.8, GOLD)
        card(img, 880, "Markets shut 24 Nov · reopen Wed", 2, t, 18.2, GOLD)
        en(img, "A paper loss until you sell · education only", 1080, t, 18.2, 46, GREY, "s")
        chart(img, 200, 1200, 680, 280, ease(seg(t, 17.6, 19.0)), [.8, .75, .82, .6, .4, .3, .38], RED, False)
    else:
        img = end_card(img, t, 21.0)
    src(img, "Sources: BSE/NSE close via Business Standard, NationPath, InCred · 23 Nov 2026", t)
    return img

# ---------------- Short 2: gold rebound ----------------
S2_CUES = "0:boom,0.2:coin*8,2.6:ding,6.0:whoosh,6.6:fail,8.2:pop,12.4:swoosh,13.2:coin*6,15.0:cash,17.4:whoosh,17.8:pop,18.2:pop,21.0:success"
def short2(t):
    img = scene_bg(t, "night", 62)
    if t < 6.0:
        ml(img, "സ്വർണ്ണം വീണ്ടും", 250, t, -1, 100, WHITE)
        ml(img, "കയറുന്നോ?", 380, t, -1, 120, GOLD)
        v = count(91720, 92800, t, 0.0, 2.2)
        big(img, f"₹{v:,.0f}", 600, t, -1, 200, GOLD)
        en(img, "1 pavan, Kerala 22K gold · 23 Nov", 760, t, -1, 52, WHITE)
        if t > 3.2: pill(img, W / 2, 880, "+₹1,080 today", t, 3.2, GREEN, WHITE, 56, 46)
        rays(img, W / 2, 1300, t, GOLD, 28)
        for k in range(3): gold_bar3d(img, W / 2 + (k - 1) * 320, 1280 + (k % 2) * 110, 0.95 * back(seg(t, -.2 + k * .25, .4 + k * .25)))
    elif t < 12.4:
        ml(img, "കഴിഞ്ഞ ആഴ്ച വൻ ഇടിവ്", 330, t, 6.0, 92, WHITE)
        en(img, "Last week: a big fall", 450, t, 6.2, 54, GOLD)
        card(img, 680, "World gold, last week", 1, t, 6.6, RED, "−8.9%")
        card(img, 880, "Worst week in about 8 months", 2, t, 8.2, GOLD)
        chart(img, 140, 1120, 800, 380, ease(seg(t, 6.6, 10.0)), [.95, .9, .85, .7, .5, .3, .2, .32], GOLD)
    elif t < 17.4:
        ml(img, "10 പവൻ ഉള്ളവർക്ക്?", 330, t, 12.4, 100, WHITE)
        en(img, "If you hold 10 pavan (80 g)", 450, t, 12.6, 54, GOLD)
        if panel(img, (140, 580, 940, 1040), t, 13.0):
            d = ImageDraw.Draw(img)
            v = count(917200, 928000, t, 13.2, 15.0)
            d.text((540, 680), "Gold value today", font=F("b", 48), fill=(90, 95, 105), anchor="mm")
            d.text((540, 820), f"₹{v:,.0f}", font=F("k", 140), fill=INK, anchor="mm")
            if t > 15.0: d.text((540, 960), "+₹10,800 since Saturday", font=F("k", 56), fill=GREEN, anchor="mm")
        for k in range(3): gold_bar3d(img, 300 + k * 240, 1250 + 20 * math.sin(t * 2 + k), .75)
        if t > 15.0: img = punch(img, t, 15.0, .05)
    elif t < 21.0:
        ml(img, "എന്തുകൊണ്ട് കയറി?", 330, t, 17.4, 100, WHITE)
        en(img, "Why it bounced", 460, t, 17.5, 56, GOLD)
        card(img, 680, "Stock sell-off: money ran to gold", 1, t, 17.8, GOLD)
        card(img, 880, "Spot gold back near $3,570/oz", 2, t, 18.2, GOLD)
        en(img, "Nobody knows tomorrow's price · education only", 1080, t, 18.2, 46, GREY, "s")
        for k in range(3): gold_bar3d(img, W / 2 + (k - 1) * 300, 1320 + (k % 2) * 60, .8 * back(seg(t, 17.6 + .2 * k, 18.2 + .2 * k)))
    else:
        img = end_card(img, t, 21.0)
    src(img, "Sources: Kerala 22K rate via Kerala9, IIFL/Goodreturns · spot: Amillex · 23 Nov 2026", t)
    return img

# ---------------- Short 3: Nasdaq crash ----------------
S3_CUES = "0:boom,0.2:tick*10,2.6:hit,6.0:whoosh,6.6:pop,8.2:pop,12.4:swoosh,13.2:tick*8,15.0:fail,17.4:whoosh,17.8:pop,18.2:pop,21.0:success"
def short3(t):
    img = scene_bg(t, "berry", 73)
    if t < 6.0:
        ml(img, "US ഫണ്ടിൽ ₹1 ലക്ഷം", 250, t, -1, 100, WHITE)
        ml(img, "ഇട്ടിരുന്നോ?", 380, t, -1, 120, GOLD)
        v = count(3.0, 5.28, t, 0.0, 2.2)
        big(img, f"−{v:.2f}%", 600, t, -1, 220, (255, 90, 90))
        en(img, "Nasdaq in one day · Friday 20 Nov", 760, t, -1, 52, WHITE)
        chart(img, 120, 960, 840, 520, ease(seg(t, -0.3, 2.6)), [.7, .78, .85, .9, .95, .88, .7, .5, .35, .2, .1], (255, 90, 90))
        if t > 3.2: img = shake(img, t, 3.2, 14, .4)
    elif t < 12.4:
        ml(img, "ടെക് ഓഹരികൾ തകർന്നു", 330, t, 6.0, 92, WHITE)
        en(img, "AI and tech shares crashed", 450, t, 6.2, 54, GOLD)
        card(img, 680, "S&P 500 · 7th fall in a row", 1, t, 6.6, RED, "−3.7%")
        card(img, 880, "Dow Jones, same day", 2, t, 8.2, RED, "−1.93%")
        chart(img, 140, 1120, 800, 380, ease(seg(t, 6.6, 10.0)), [.9, .92, .85, .8, .6, .45, .3, .15], (255, 90, 90))
    elif t < 17.4:
        ml(img, "നിങ്ങളുടെ ₹1 ലക്ഷം", 330, t, 12.4, 100, WHITE)
        en(img, "₹1 lakh in a Nasdaq-tracking fund", 450, t, 12.6, 54, GOLD)
        if panel(img, (140, 580, 940, 1040), t, 13.0):
            d = ImageDraw.Draw(img)
            v = count(100000, 94720, t, 13.2, 15.0)
            d.text((540, 680), "After one day", font=F("b", 48), fill=(90, 95, 105), anchor="mm")
            d.text((540, 820), f"₹{v:,.0f}", font=F("k", 140), fill=INK, anchor="mm")
            if t > 15.0: d.text((540, 960), "−₹5,280 in one day", font=F("k", 60), fill=RED, anchor="mm")
        falling_coins(img, t, 13.2, 6, 9)
        if t > 15.0: img = punch(img, t, 15.0, .05)
    elif t < 21.0:
        ml(img, "ഇനി എന്ത്?", 330, t, 17.4, 110, WHITE)
        en(img, "What now", 460, t, 17.5, 56, GOLD)
        card(img, 680, "Monday: US futures bounced back", 1, t, 17.8, GREEN)
        card(img, 880, "To get back: +5.6%, not 5.28%", 2, t, 18.2, GOLD)
        en(img, "Loss maths, education only · not advice", 1080, t, 18.2, 46, GREY, "s")
        chart(img, 200, 1200, 680, 280, ease(seg(t, 17.6, 19.0)), [.6, .45, .3, .15, .3, .45, .55], GREEN, False)
    else:
        img = end_card(img, t, 21.0)
    src(img, "Sources: Nasdaq/S&P close via Business Standard, JournalArta, Amillex · 20–23 Nov 2026", t)
    return img

SHORTS = {1: (short1, S1_CUES), 2: (short2, S2_CUES), 3: (short3, S3_CUES)}

if __name__ == "__main__":
    fn, _ = SHORTS[int(sys.argv[1])]
    if sys.argv[2] == "--frame":
        fn(float(sys.argv[3])).convert("RGB").save(sys.argv[4]); sys.exit()
    out = sys.argv[2]; tmp = out + ".tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)): p.stdin.write(fn(i / FPS).convert("RGB").tobytes())
    p.stdin.close(); assert p.wait() == 0; os.replace(tmp, out); print(out)
