"""Reel: F&O margin calculator. Render: python3 reel_margin.py  (or with "1.5,7,..." to save key frames)."""
import os, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_fx import *

DUR = 33
DARK = (24, 27, 36); CARD = (34, 38, 52); MUTE = (170, 176, 190)

def card(img, box, fill=CARD, r=34, outline=None):
    shadow(img, box, r, 24, 120, (0, 16)); d = ImageDraw.Draw(img)
    d.rounded_rectangle(box, r, fill=fill, outline=outline, width=4 if outline else 0)

def slide_x(t, t0, frm, to, dur=0.5): return lerp(frm, to, back(seg(t, t0, t0 + dur)))

def note_small(img, t, t0, text="Example figures · margins change daily"):
    if t < t0: return
    d = ImageDraw.Draw(img); a = ease(seg(t, t0, t0 + .4))
    d.text((W / 2, 1860), text, font=F("s", 30), fill=mix(DARK, MUTE, a), anchor="mm")

def scene_hook(t):
    im = scene_bg(t, "night", 11); d = ImageDraw.Draw(im)
    kinetic(im, "Same Nifty idea.", 330, t, 0.05, 92, WHITE)
    kinetic(im, "Two very different margins.", 430, t, 0.45, 64, GOLD)
    # left card: short strangle
    x1 = slide_x(t, 0.9, -520, 70); card(im, (x1, 540, x1 + 450, 1000), CARD, outline=RED)
    d = ImageDraw.Draw(im)
    d.text((x1 + 225, 610), "Short strangle", font=F("b", 46), fill=WHITE, anchor="mm")
    d.text((x1 + 225, 670), "sell call + sell put", font=F("s", 32), fill=MUTE, anchor="mm")
    if t > 1.3: d.text((x1 + 225, 800), "≈ ₹2 lakh", font=F("k", 84), fill=RED, anchor="mm")
    d.text((x1 + 225, 920), "risk: unlimited", font=F("b", 36), fill=RED, anchor="mm")
    # right card: iron condor
    x2 = slide_x(t, 1.6, W + 40, W - 520); card(im, (x2, 540, x2 + 450, 1000), CARD, outline=GREEN)
    d = ImageDraw.Draw(im)
    d.text((x2 + 225, 610), "Iron condor", font=F("b", 46), fill=WHITE, anchor="mm")
    d.text((x2 + 225, 670), "same + 2 cheap wings", font=F("s", 32), fill=MUTE, anchor="mm")
    if t > 2.0:
        v = count(0, 7150, t, 2.0, 2.9); d.text((x2 + 225, 800), f"₹{v:,.0f}", font=F("k", 84), fill=GREEN, anchor="mm")
    d.text((x2 + 225, 920), "risk: capped", font=F("b", 36), fill=GREEN, anchor="mm")
    souq(im, W / 2, 1420, 0.85, t, "shocked" if t > 2.6 else "thinking")
    speech(im, W / 2 + 200, 1170, "28× less?!", 2.9, t, 50)
    im = shake(im, t, 2.9, 16)
    return punch(im, t, 0.05)

def scene_futures(t):
    u = t - 4.5; im = scene_bg(t, "sky", 13); d = ImageDraw.Draw(im)
    pill(im, W / 2, 230, "1 · FUTURES MARGIN", t, 4.55, WHITE, INK, 40)
    kinetic(im, "1 lot Nifty future", 380, t, 4.7, 78, WHITE)
    # equation
    f = F("k", 72); parts = [("65", GOLD), ("×", WHITE), ("26,000", GOLD), ("=", WHITE)]
    xs = [170, 330, 560, 790]
    for i, (s, c) in enumerate(parts):
        p = back(seg(t, 5.1 + i * .18, 5.4 + i * .18))
        if p > 0: d.text((xs[i], 530 + (1 - p) * 40), s, font=f, fill=c, anchor="mm")
    d.text((170, 600), "units", font=F("s", 30), fill=WHITE, anchor="mm"); d.text((560, 600), "price", font=F("s", 30), fill=WHITE, anchor="mm")
    if u > 1.0:
        v = count(0, 16.9, t, 5.5, 6.3); d.text((930, 530), f"₹{v:.1f}L", font=F("k", 66), fill=WHITE, anchor="mm")
        d.text((930, 600), "contract value", font=F("s", 30), fill=WHITE, anchor="mm")
    # bar: contract value with margin slice
    p = ease(seg(u, 1.0, 2.0)); bx0, bx1, by = 90, 990, 760
    d.rounded_rectangle((bx0, by, bx0 + (bx1 - bx0) * p, by + 120), 28, fill=(255, 255, 255))
    q = ease(seg(u, 2.2, 2.9))
    if q > 0:
        d.rounded_rectangle((bx0, by, bx0 + (bx1 - bx0) * 0.12 * q + 2, by + 120), 28, fill=GOLD)
        d.line((bx0 + (bx1 - bx0) * 0.12, by + 130, bx0 + (bx1 - bx0) * 0.12, by + 190), fill=GOLD, width=6)
        d.text((bx0 + 140, by + 240), "Margin ≈ 12%", font=F("k", 64), fill=GOLD, anchor="lm")
        d.text((bx0 + 140, by + 320), f"= ₹{count(0, 2.03, t, 6.8, 7.6):.2f} lakh", font=F("k", 64), fill=WHITE, anchor="lm")
    pill(im, W / 2, 1220, "Leverage 8.3×", t, 7.9, GOLD, INK, 56)
    pill(im, W / 2, 1360, "1% move = ₹16,900 profit or loss", t, 8.5, RED, WHITE, 44)
    souq(im, 900, 1640, 0.55, t, "thinking" if u < 4 else "wink")
    note_small(im, t, 5.0)
    return im

def scene_spread(t):
    u = t - 10.5; im = scene_bg(t, "mint", 17); d = ImageDraw.Draw(im)
    pill(im, W / 2, 230, "2 · CALENDAR SPREAD", t, 10.55, WHITE, INK, 40)
    kinetic(im, "Buy one month, sell the next", 380, t, 10.7, 60, WHITE)
    # two legs moving together
    for i, (lbl, col, x) in enumerate([("BUY Jan", GREEN, 300), ("SELL Feb", RED, 780)]):
        p = back(seg(t, 11.0 + i * .25, 11.4 + i * .25))
        if p <= 0: continue
        bob = 40 * math.sin((t - 11) * 2.4)
        box = (x - 150, 560 + bob, x + 150, 760 + bob); card(im, box, CARD, 30, col); d = ImageDraw.Draw(im)
        d.text((x, 630 + bob), lbl, font=F("k", 50), fill=col, anchor="mm")
        d.text((x, 700 + bob), "moves together ↕", font=F("s", 30), fill=WHITE, anchor="mm")
    p = ease(seg(u, 1.6, 2.2))
    if p > 0:
        d.text((W / 2, 900), "Two outright legs", font=F("b", 48), fill=WHITE, anchor="mm")
        d.text((W / 2, 990), "₹4.06 lakh", font=F("k", 96), fill=(255, 190, 190), anchor="mm")
        s = ease(seg(u, 2.4, 2.8))
        if s > 0: d.line((W / 2 - 250, 990, W / 2 - 250 + 500 * s, 990), fill=RED, width=12)
    if u > 2.9:
        d.text((W / 2, 1130), "Spread margin", font=F("b", 48), fill=WHITE, anchor="mm")
        d.text((W / 2, 1230), f"≈ ₹{count(4.06, 1.01, t, 13.4, 14.2):.2f} lakh", font=F("k", 104), fill=GOLD, anchor="mm")
        sparkles(im, W / 2, 1230, t, 14.2, 7, 14, 300, GOLD)
    pill(im, W / 2, 1420, "75% spread benefit (example)", t, 14.3, WHITE, INK, 40)
    souq(im, 170, 1640, 0.5, t, "cool")
    note_small(im, t, 11.0)
    return im

def scene_condor(t):
    u = t - 15.5; im = scene_bg(t, "night", 19); d = ImageDraw.Draw(im)
    pill(im, W / 2, 200, "3 · OPTION STRATEGIES", t, 15.55, GOLD, INK, 40)
    kinetic(im, "Why wings cut margin", 330, t, 15.7, 70, WHITE)
    # chart frame
    X0, X1, Y0, Y1 = 110, 990, 470, 1130; zero = 830
    card(im, (X0 - 30, Y0 - 30, X1 + 30, Y1 + 30), CARD, 30); d = ImageDraw.Draw(im)
    d.line((X0, zero, X1, zero), fill=(90, 96, 115), width=3)
    lo, hi = 25300, 26700
    px = lambda s: X0 + (s - lo) / (hi - lo) * (X1 - X0)
    sc = 1.5  # pixels per rupee-point for payoff (points)
    py = lambda v: zero - v * sc
    def ic(s):  # payoff per unit at expiry, points
        return 90 - max(25800 - s, 0) + max(25600 - s, 0) - max(s - 26200, 0) + max(s - 26400, 0)
    def strangle(s): return 175 - max(25800 - s, 0) - max(s - 26200, 0)
    # strike ticks
    for k, lbl, col, tt in [(25600, "Buy 25,600 P", GREEN, 16.2), (25800, "Sell 25,800 P", RED, 16.4), (26200, "Sell 26,200 C", RED, 16.6), (26400, "Buy 26,400 C", GREEN, 16.8)]:
        a = ease(seg(t, tt, tt + .3))
        if a > 0:
            x = px(k); d.line((x, Y1 - 10, x, Y1 + 10), fill=col, width=5)
            d.text((x, Y1 + 50 + (40 if k in (25800, 26400) else 0)), lbl, font=F("b", 26), fill=mix(DARK, col, a), anchor="mm")
    # strangle dashed (unlimited)
    ps = ease(seg(u, 1.5, 3.0))
    if ps > 0:
        pts = [(px(s), max(Y0 + 5, min(Y1 - 5, py(strangle(s))))) for s in range(lo, int(lo + (hi - lo) * ps), 10)]
        for i in range(0, len(pts) - 1, 2): d.line((pts[i], pts[i + 1]), fill=RED, width=5)
    if u > 3.0:
        a = ease(seg(u, 3.0, 3.4)); d.text((X0 + 10, Y1 - 40), "↓ unlimited", font=F("b", 28), fill=mix(CARD, RED, a), anchor="lm")
        d.text((X1 - 10, Y1 - 40), "unlimited ↓", font=F("b", 28), fill=mix(CARD, RED, a), anchor="rm")
    # condor solid
    pc = ease(seg(u, 3.2, 5.0))
    if pc > 0:
        pts = [(px(s), py(ic(s))) for s in range(lo, int(lo + (hi - lo) * pc), 5)]
        if len(pts) > 1: d.line(pts, fill=GOLD, width=10, joint="curve")
    if u > 5.0:
        a = ease(seg(u, 5.0, 5.5))
        # max profit band and max loss band
        d.text((px(26000), py(90) - 50), "Max profit ₹5,850", font=F("k", 40), fill=mix(DARK, GREEN, a), anchor="mm")
        d.text((px(25450), py(-110) - 40), "Max loss", font=F("k", 36), fill=mix(DARK, GOLD, a), anchor="mm")
        d.text((px(26560), py(-110) - 40), "capped", font=F("k", 36), fill=mix(DARK, GOLD, a), anchor="mm")
    pill(im, W / 2, 1330, "Margin ≈ max loss = ₹7,150", t, 21.2, GOLD, INK, 50)
    pill(im, W / 2, 1460, "Naked strangle ≈ ₹2 lakh (unlimited risk)", t, 22.0, RED, WHITE, 38)
    souq(im, W / 2, 1700, 0.5, t, "happy" if u > 6 else "thinking")
    note_small(im, t, 16.0)
    return im

def scene_markets(t):
    u = t - 24; im = scene_bg(t, "berry", 23); d = ImageDraw.Draw(im)
    kinetic(im, "Every market.", 300, t, 24.05, 96, WHITE)
    kinetic(im, "Latest lot sizes.", 420, t, 24.35, 72, GOLD)
    tiles = [("NSE", "Nifty", "65"), ("NSE", "Bank Nifty", "30"), ("BSE", "Sensex", "20"), ("LME", "Copper", "25 t"),
             ("LME", "Nickel", "6 t"), ("CME", "E-mini S&P", "$50/pt"), ("CME", "Gold", "100 oz"), ("US", "Stock options", "100")]
    for i, (ex, nm, lot) in enumerate(tiles):
        r, c = divmod(i, 2); x = 90 + c * 470; y = 540 + r * 250
        p = back(seg(t, 24.6 + i * .17, 25.0 + i * .17))
        if p <= 0: continue
        dy = (1 - p) * 80; box = (x, y + dy, x + 430, y + 210 + dy)
        card(im, box, (255, 255, 255)); d = ImageDraw.Draw(im)
        d.rounded_rectangle((x + 24, y + 24 + dy, x + 24 + d.textlength(ex, font=F("k", 30)) + 30, y + 72 + dy), 16, fill=GOLD)
        d.text((x + 39, y + 48 + dy), ex, font=F("k", 30), fill=INK, anchor="lm")
        d.text((x + 30, y + 120 + dy), nm, font=F("b", 40), fill=INK, anchor="lm")
        d.text((x + 400, y + 170 + dy), lot, font=F("k", 52), fill=(160, 40, 110), anchor="rm")
    pill(im, W / 2, 1600, "Futures · spreads · 12 option strategies", t, 26.6, WHITE, INK, 40)
    return im

def scene_end(t):
    im = scene_bg(t, "night", 29)
    endcard(im, t, 28.55, "Margin calculator", "Free · NSE · BSE · LME · CME · US options")
    souq(im, W / 2, 1480, 0.65, t, "happy", wave=True); confetti(im, t, 28.7, 9, 70)
    d = ImageDraw.Draw(im)
    if t > 29.6: d.text((W / 2, 1260), "Not investment advice · check live margins with your broker", font=F("s", 30), fill=MUTE, anchor="mm")
    return im

def frame(i):
    t = i / FPS
    if t < 4.5: return scene_hook(t)
    if t < 10.5: return scene_futures(t)
    if t < 15.5: return scene_spread(t)
    if t < 24: return scene_condor(t)
    if t < 28.5: return scene_markets(t)
    return scene_end(t)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        for s in map(float, sys.argv[1].split(",")): frame(int(s * FPS)).convert("RGB").save(f"/tmp/mg-{s}.png")
    else:
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                              "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "/tmp/margin.tmp.mp4"], stdin=subprocess.PIPE)
        for i in range(DUR * FPS): p.stdin.write(frame(i).convert("RGB").tobytes())
        p.stdin.close(); assert p.wait() == 0; os.replace("/tmp/margin.tmp.mp4", "/tmp/margin_v.mp4")
