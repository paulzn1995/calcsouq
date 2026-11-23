"""CalcSouq daily reels for 2026-11-23 (reading pace, SLOW = 1.75; answer revealed by ~6 s real time).
Every figure comes from the site's own formulas. Usage:
  python3 build/reels_2026_11_23.py <reel> [t1,t2,...]   -> stills at real-time seconds (reel = days10k|flat|half|hundred|winrate)
  python3 build/reels_2026_11_23.py <reel>               -> /tmp/<reel>_v.mp4 (silent)
  python3 build/reels_2026_11_23.py cues <reel>          -> audio cue string in real-time seconds
1 days10k : age-calculator (total days = round((to - from) / 1 day)). Born 15 Jul 1999 -> 30 Nov 2026 (Mon) = 10,000 days,
            age 27 y 4 m 15 d. 10,000 / 365.2425 = 27.38 y; 20,000 days = 54.76 y; 30,000 days = 82.14 y.
2 flat    : loan-emi-calculator (reducing balance). ₹1 lakh, 3 years. Flat 10%: interest 1,00,000 x 10% x 3 = ₹30,000,
            EMI 1,30,000 / 36 = ₹3,611. Reducing 10%: EMI ₹3,227, interest ₹16,162. Same EMI ₹3,611 on reducing
            balance = 17.9% a year (bisection on the EMI formula).
3 half    : percentage-calculator. ₹1,000 -50% = ₹500, +50% = ₹750 (-25%). +50% first: 1,500 then -50% = 750.
            After -50% you need +100% to get back.
4 hundred : compound-interest-calculator, ₹0 start, add ₹3,000 at the end of each month (₹100 a day x 30), 30 years,
            monthly compounding: 0% ₹10,80,000; 7% ₹36,59,913; 12% ₹1,04,84,892.
5 winrate : risk-reward-calculator: breakeven win rate = 1 / (1 + R). 1:1 50%, 1:2 33.3%, 1:3 25%.
            10 trades at 1:3 risking 1R, 3 wins: 3 x 3R - 7 x 1R = +2R (before costs).
"""
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_fx import *
from reels_2026_11_21 import options, row, small, end

SLOW = 1.75
BASE = 13.2
MINT = (140, 255, 200)
PALE = (220, 225, 255)
A_END = 10.8  # end-card start (base time)

def reveal_num(im, text, y, t, t0, size=150, col=GOLD):
    p = back(seg(t, t0, t0 + 0.35))
    if p <= 0: return
    d = ImageDraw.Draw(im); f = F("k", size * (0.6 + 0.4 * p))
    d.text((W / 2, y), text, font=f, fill=col, anchor="mm")

# ---------------- 1. When are you 10,000 days old? ----------------
def days10k(t):
    if t < 3.2:
        im = scene_bg(t, "sunset", 101); d = ImageDraw.Draw(im)
        kinetic(im, "You turn 10,000", 420, t, -1.2, 104, WHITE, hl=["10,000"])
        kinetic(im, "days old at…?", 535, t, -1.0, 104, WHITE)
        options(im, t, 0.8, ["A  25 years", "B  27 years 4 months", "C  30 years"], 700, win=1, t_win=2.6)
        calendar(d, 250, 1290, 0.85, "?")
        souq(im, 720, 1300, 0.6, t, "thinking"); speech(im, 760, 1170, "Guess first!", 1.4, t, 44)
        return punch(im, t, 0.0)
    if t < 6.6:
        im = scene_bg(t, "night", 103); rays(im, W / 2, 640, t, GOLD, 26); d = ImageDraw.Draw(im)
        kinetic(im, "10,000 days =", 470, t, 3.2, 84, WHITE)
        reveal_num(im, "27.4 years", 640, t, 3.4, 150)
        sparkles(im, W / 2, 640, t, 3.5, 4, 16, 330, GOLD)
        pill(im, W / 2, 820, "Answer B · 27 y 4 m (and a bit)", t, 4.2, WHITE, INK, 48)
        trophy(d, 800, 1300, 0.7)
        souq(im, 330, 1320, 0.6, t, "shocked" if t < 4.6 else "wink"); speech(im, 450, 1120, "Did you notice?", 4.6, t, 44)
        return shake(im, t, 3.4, 14)
    if t < A_END:
        im = scene_bg(t, "sky", 105); d = ImageDraw.Draw(im)
        kinetic(im, "Born 15 July 1999?", 360, t, 6.6, 80, WHITE)
        row(im, 520, "10,000 days old on", "Mon 30 Nov", t, 6.9, vcol=GOLD)
        row(im, 670, "20,000 days", "≈ 54.8 yrs", t, 7.9, vcol=MINT)
        row(im, 820, "30,000 days", "≈ 82.1 yrs", t, 8.7, vcol=(255, 200, 230))
        calendar(d, 250, 1290, 0.8, "30")
        souq(im, 720, 1300, 0.55, t, "happy"); speech(im, 740, 1150, "Plan a party!", 8.0, t, 44)
        return punch(im, t, 6.9, 0.05)
    return end(t, A_END, "Free age|calculator", "mint", 107)

# ---------------- 2. Flat 10% is not 10% ----------------
def flat_screen(d, sb, t):
    x0, y0, x1, y1 = sb; cx = (x0 + x1) / 2; s = (x1 - x0) / 376
    d.text((cx, y0 + 90 * s), "Loan EMI", font=F("k", 36 * s), fill=INK, anchor="mm")
    for i, (a, b) in enumerate([("Loan", "₹1,00,000"), ("Tenure", "3 years"), ("EMI", "₹3,611")]):
        y = y0 + 180 * s + i * 92 * s
        d.rounded_rectangle([x0 + 24 * s, y - 36 * s, x1 - 24 * s, y + 36 * s], int(16 * s), fill=WHITE, outline=(215, 218, 222), width=2)
        d.text((x0 + 44 * s, y), a, font=F("s", 26 * s), fill=(90, 95, 105), anchor="lm"); d.text((x1 - 44 * s, y), b, font=F("b", 28 * s), fill=INK, anchor="rm")
    y = y0 + 520 * s
    d.rounded_rectangle([x0 + 24 * s, y - 64 * s, x1 - 24 * s, y + 64 * s], int(20 * s), fill=INK)
    d.text((cx, y), f"{count(10, 17.9, t, 7.2, 8.2):.1f}% real", font=F("k", 46 * s), fill=GOLD, anchor="mm")

def flat(t):
    if t < 3.2:
        im = scene_bg(t, "night", 201); d = ImageDraw.Draw(im)
        kinetic(im, "Loan at \"10% flat\".", 420, t, -1.2, 86, WHITE)
        kinetic(im, "The REAL rate?", 535, t, -1.0, 104, GOLD, hl=["REAL"], hl_col=RED)
        small(im, "₹1 lakh · 3 years · monthly EMI", 615, PALE, 44)
        options(im, t, 0.8, ["A  10%", "B  14%", "C  about 18%"], 760, win=2, t_win=2.6)
        doc(d, 230, 1300, 0.75, "LOAN", RED)
        souq(im, 700, 1300, 0.6, t, "thinking"); speech(im, 740, 1170, "Guess first!", 1.4, t, 44)
        return punch(im, t, 0.0)
    if t < 6.6:
        im = scene_bg(t, "berry", 203); rays(im, W / 2, 640, t, WHITE, 24); d = ImageDraw.Draw(im)
        kinetic(im, "Flat 10% really costs", 470, t, 3.2, 80, WHITE)
        reveal_num(im, "17.9% a year", 640, t, 3.4, 140, GOLD)
        sparkles(im, W / 2, 640, t, 3.5, 5, 16, 330, GOLD)
        pill(im, W / 2, 820, "Answer C · on the reducing balance", t, 4.2, WHITE, INK, 46)
        coins_stack(d, 820, 1430, 7, 50)
        souq(im, 330, 1320, 0.6, t, "shocked"); speech(im, 440, 1120, "Wait, WHAT?", 4.6, t, 44)
        return shake(im, t, 3.4, 20)
    if t < A_END:
        im = scene_bg(t, "sunset", 205); d = ImageDraw.Draw(im)
        kinetic(im, "Interest on the full loan", 340, t, 6.6, 64, WHITE)
        kinetic(im, "for all 3 years", 420, t, 6.75, 64, WHITE)
        phone(im, 300, 1000, 0.9, lambda dd, sb, tt: flat_screen(dd, sb, t), t)
        pill(im, 790, 760, "Flat: ₹30,000", t, 7.0, RED, WHITE, 50, 34)
        pill(im, 790, 900, "Reducing: ₹16,162", t, 7.9, GREEN, WHITE, 48, 30)
        pill(im, 790, 1040, "17.9% real", t, 8.6, GOLD, INK, 50, 34)
        souq(im, 800, 1300, 0.5, t, "cool" if t > 8.6 else "thinking")
        return im
    return end(t, A_END, "Free loan EMI|calculator", "sky", 207)

# ---------------- 3. Down 50%, up 50% ----------------
def mini_chart(im, x0, y0, w, h, p, pts, col):
    d = ImageDraw.Draw(im); n = len(pts) - 1
    d.line([(x0, y0 + h), (x0 + w, y0 + h)], fill=(255, 255, 255), width=4)
    k = p * n
    for i in range(n):
        q = clamp(k - i)
        if q <= 0: break
        xa, ya = x0 + w * i / n, y0 + h * (1 - pts[i]); xb, yb = x0 + w * (i + 1) / n, y0 + h * (1 - pts[i + 1])
        d.line([(xa, ya), (lerp(xa, xb, q), lerp(ya, yb, q))], fill=col, width=14)
        d.ellipse([xa - 14, ya - 14, xa + 14, ya + 14], fill=WHITE)
    if p >= 1:
        xa, ya = x0 + w, y0 + h * (1 - pts[-1]); d.ellipse([xa - 14, ya - 14, xa + 14, ya + 14], fill=WHITE)

def half(t):
    if t < 3.2:
        im = scene_bg(t, "berry", 301); d = ImageDraw.Draw(im)
        kinetic(im, "Down 50%. Then up 50%.", 420, t, -1.2, 72, WHITE)
        kinetic(im, "Back to even?", 535, t, -1.0, 110, GOLD)
        options(im, t, 0.8, ["A  Yes, ₹1,000", "B  No, ₹750", "C  More, ₹1,250"], 700, win=1, t_win=2.6)
        mini_chart(im, 120, 1130, 420, 300, 1.0, [0.9, 0.2, 0.6], (255, 200, 230))
        souq(im, 760, 1300, 0.6, t, "thinking"); speech(im, 800, 1170, "Guess first!", 1.4, t, 44)
        return punch(im, t, 0.0)
    if t < 6.6:
        im = scene_bg(t, "night", 303); rays(im, W / 2, 640, t, RED, 22); d = ImageDraw.Draw(im)
        kinetic(im, "₹1,000 ends up at", 470, t, 3.2, 84, WHITE)
        reveal_num(im, "₹750", 650, t, 3.4, 190, GOLD)
        sparkles(im, W / 2, 650, t, 3.5, 6, 16, 330, GOLD)
        pill(im, W / 2, 830, "Answer B · still 25% down", t, 4.2, RED, WHITE, 50)
        mini_chart(im, 560, 1130, 400, 300, seg(t, 3.3, 4.6), [0.9, 0.2, 0.6], RED)
        souq(im, 290, 1320, 0.6, t, "shocked"); speech(im, 400, 1120, "Where did ₹250 go?", 4.6, t, 42)
        return shake(im, t, 3.4, 18)
    if t < A_END:
        im = scene_bg(t, "mint", 305); d = ImageDraw.Draw(im)
        kinetic(im, "The % is on a new base", 360, t, 6.6, 72, WHITE)
        row(im, 520, "−50% of ₹1,000", "₹500", t, 6.9, vcol=(255, 170, 170), box=(20, 50, 44))
        row(im, 670, "+50% of ₹500", "₹750", t, 7.7, vcol=GOLD, box=(20, 50, 44))
        pill(im, W / 2, 830, "To get back after −50%: +100%", t, 8.5, GOLD, INK, 50)
        coins_stack(d, 230, 1440, int(count(8, 4, t, 6.9, 7.6)) if t < 7.7 else int(count(4, 6, t, 7.7, 8.3)), 50)
        souq(im, 720, 1300, 0.55, t, "wink" if t > 8.5 else "thinking"); speech(im, 740, 1150, "Order doesn't matter", 9.0, t, 42)
        return punch(im, t, 8.5, 0.05)
    return end(t, A_END, "Free percentage|calculator", "sky", 307)

# ---------------- 4. ₹100 a day for 30 years ----------------
def hundred(t):
    if t < 3.2:
        im = scene_bg(t, "gold", 401); d = ImageDraw.Draw(im)
        kinetic(im, "₹100 a day.", 420, t, -1.2, 120, INK)
        kinetic(im, "30 years. Becomes…?", 540, t, -1.0, 84, (150, 40, 40))
        small(im, "Invested at an assumed 12% a year", 615, INK, 44)
        options(im, t, 0.8, ["A  ₹11 lakh", "B  ₹40 lakh", "C  over ₹1 crore"], 760, win=2, t_win=2.6)
        piggy(im, 250, 1320, 0.6, t)
        souq(im, 740, 1300, 0.6, t, "thinking"); speech(im, 770, 1170, "Guess first!", 1.4, t, 44)
        return punch(im, t, 0.0)
    if t < 6.6:
        im = scene_bg(t, "night", 403); rays(im, W / 2, 640, t, GOLD, 26); d = ImageDraw.Draw(im)
        kinetic(im, "After 30 years:", 470, t, 3.2, 84, WHITE)
        reveal_num(im, f"₹{count(10.8, 99, t, 3.4, 4.3):.1f} lakh" if t < 4.4 else "₹1.05 crore", 640, t, 3.4, 140, GOLD)
        sparkles(im, W / 2, 640, t, 4.4, 7, 16, 330, GOLD)
        pill(im, W / 2, 820, "Answer C · ₹1.05 crore", t, 4.4, WHITE, INK, 50)
        rocket(im, 820, 1290, 0.55, t)
        souq(im, 330, 1320, 0.6, t, "shocked" if t < 5.0 else "cool"); speech(im, 440, 1120, "From ₹100 a day?!", 4.8, t, 44)
        return punch(im, t, 4.4, 0.06)
    if t < A_END:
        im = scene_bg(t, "mint", 405); d = ImageDraw.Draw(im)
        kinetic(im, "₹3,000 a month · 30 years", 360, t, 6.6, 66, WHITE)
        row(im, 520, "Put in (0%)", "₹10.8 lakh", t, 6.9, vcol=WHITE, box=(20, 50, 44))
        row(im, 670, "At 7%", "₹36.6 lakh", t, 7.7, vcol=MINT, box=(20, 50, 44))
        row(im, 820, "At 12% (assumed)", "₹1.05 crore", t, 8.5, vcol=GOLD, box=(20, 50, 44))
        small(im, "Not guaranteed · before tax · not advice", 940, WHITE, 44)
        coins_stack(d, 230, 1440, int(count(2, 9, t, 6.9, 9.0)), 50)
        souq(im, 720, 1300, 0.55, t, "happy")
        return im
    return end(t, A_END, "Free compound|interest calculator", "berry", 407)

# ---------------- 5. Break-even win rate at 1:3 ----------------
def winrate(t):
    if t < 3.2:
        im = scene_bg(t, "sky", 501); d = ImageDraw.Draw(im)
        kinetic(im, "Risk 1 to make 3.", 420, t, -1.2, 100, WHITE)
        kinetic(im, "What win rate breaks even?", 530, t, -1.0, 68, GOLD)
        options(im, t, 0.8, ["A  75%", "B  50%", "C  25%"], 700, win=2, t_win=2.6)
        chart_up(d, 130, 1450, 420, 300, 1.0, WHITE)
        souq(im, 760, 1300, 0.6, t, "thinking"); speech(im, 800, 1170, "Guess first!", 1.4, t, 44)
        return punch(im, t, 0.0)
    if t < 6.6:
        im = scene_bg(t, "mint", 503); rays(im, W / 2, 640, t, MINT, 26); d = ImageDraw.Draw(im)
        kinetic(im, "At 1:3 you break even at", 470, t, 3.2, 70, WHITE)
        reveal_num(im, f"{count(75, 25, t, 3.4, 4.3):.0f}%", 650, t, 3.4, 190, GOLD)
        sparkles(im, W / 2, 650, t, 4.3, 8, 16, 330, GOLD)
        pill(im, W / 2, 840, "Answer C · 1 win in 4", t, 4.4, WHITE, INK, 50)
        trophy(d, 820, 1330, 0.7)
        souq(im, 330, 1320, 0.6, t, "shocked" if t < 5.0 else "cool"); speech(im, 440, 1120, "Only 1 in 4?", 4.8, t, 44)
        return punch(im, t, 4.3, 0.06)
    if t < A_END:
        im = scene_bg(t, "night", 505); d = ImageDraw.Draw(im)
        kinetic(im, "Breakeven = 1 ÷ (1 + R)", 360, t, 6.6, 72, WHITE)
        row(im, 520, "Risk 1 : reward 1", "50%", t, 6.9, vcol=(255, 170, 170))
        row(im, 670, "Risk 1 : reward 2", "33%", t, 7.6, vcol=GOLD)
        row(im, 820, "Risk 1 : reward 3", "25%", t, 8.3, vcol=MINT)
        pill(im, W / 2, 980, "3 wins in 10 at 1:3 = +2R", t, 9.0, GOLD, INK, 50)
        small(im, "Before costs · education only", 1090, PALE, 44)
        souq(im, 540, 1330, 0.55, t, "wink" if t > 9.0 else "thinking")
        return im
    return end(t, A_END, "Free risk–reward|calculator", "sunset", 507)

REELS = dict(days10k=days10k, flat=flat, half=half, hundred=hundred, winrate=winrate)

# audio cues in BASE seconds (scaled by SLOW for the real video)
CUES = {
    "days10k": "0:boom,0.8:pop,0.95:pop2,1.1:pop,1.4:pop2,1.9:riser,2.6:ding,3.2:whoosh,3.4:sparkle,4.2:pop,4.6:pop2,6.6:swoosh,6.9:tick*6,7.9:pop,8.7:pop,10.8:whoosh,10.9:success",
    "flat": "0:boom,0.8:pop,0.95:pop2,1.1:pop,1.4:pop2,1.9:riser,2.6:ding,3.2:whoosh,3.4:hit,3.5:fail,4.2:pop,4.6:pop2,6.6:swoosh,7.0:pop,7.2:tick*6,7.9:pop2,8.6:cash,10.8:whoosh,10.9:success",
    "half": "0:boom,0.8:pop,0.95:pop2,1.1:pop,1.4:pop2,1.9:riser,2.6:ding,3.2:whoosh,3.4:fail,4.2:pop,4.6:pop2,6.6:swoosh,6.9:coin*4,7.7:coin*3,8.5:ding,9.0:pop2,10.8:whoosh,10.9:success",
    "hundred": "0:boom,0.8:pop,0.95:pop2,1.1:pop,1.4:pop2,1.9:riser,2.6:ding,3.2:whoosh,3.4:coin*8,4.4:cash,4.5:sparkle,4.8:pop2,6.6:swoosh,6.9:pop,7.7:pop,8.5:cash,10.8:whoosh,10.9:success",
    "winrate": "0:boom,0.8:pop,0.95:pop2,1.1:pop,1.4:pop2,1.9:riser,2.6:ding,3.2:whoosh,3.4:tick*8,4.3:ding,4.4:sparkle,4.8:pop2,6.6:swoosh,6.9:pop,7.6:pop,8.3:pop,9.0:success,10.8:whoosh,10.9:sparkle",
}
def real_cues(name):
    out = []
    for c in CUES[name].split(","):
        ts, k = c.split(":"); out.append(f"{float(ts) * SLOW:.2f}:{k}")
    return ",".join(out)

if __name__ == "__main__":
    if sys.argv[1] == "cues": print(real_cues(sys.argv[2])); sys.exit()
    name = sys.argv[1]; fn = REELS[name]
    if len(sys.argv) > 2:
        for s in map(float, sys.argv[2].split(",")): fn(s / SLOW).convert("RGB").save(f"/tmp/{name}-{s}.png")
    else:
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                              "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", f"/tmp/{name}.tmp.mp4"], stdin=subprocess.PIPE)
        for i in range(int(BASE * SLOW * FPS)): p.stdin.write(fn(i / FPS / SLOW).convert("RGB").tobytes())
        p.stdin.close(); assert p.wait() == 0; os.replace(f"/tmp/{name}.tmp.mp4", f"/tmp/{name}_v.mp4")
