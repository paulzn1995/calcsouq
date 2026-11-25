"""CalcSouq daily reels for 2026-11-25 (reading pace, SLOW = 1.75, 23.1 s each; big counting number on frame 1).
Every figure comes from the site's own formulas (checked in Python on 25 Nov). Usage:
  python3 build/reels_2026_11_25.py <reel> [t1,t2,...]   -> stills at real-time seconds (reel = uae55|cents|raise|bmi|winrate)
  python3 build/reels_2026_11_25.py <reel>               -> /tmp/<reel>_v.mp4 (silent)
  python3 build/reels_2026_11_25.py cues <reel>          -> audio cue string in real-time seconds
1 uae55  : age/date calculator. Thu 2 Dec 1971 -> Wed 2 Dec 2026 = 20,089 days (55 x 365 = 20,075 + 14 leap days 1972..2024)
           = 1,735,689,600 s (about 1.74 billion). Ras Al Khaimah joined on 10 Feb 1972 (caption only).
2 cents  : kerala-land-converter (tools_india UNITS): 1 cent = 435.6 sq ft = 40.47 m2. 5 cents = 2,178 sq ft = 202.3 m2;
           square side sqrt(2178) = 46.7 ft. 100 cents = 1 acre (43,560 sq ft).
3 raise  : percentage maths. Real raise = 1.08 / 1.06 - 1 = 1.89%. ₹50,000 -> ₹54,000; in today's prices 54,000 / 1.06 = ₹50,943.
           5% raise: 1.05 / 1.06 - 1 = -0.94% (₹52,500 / 1.06 = ₹49,528). Rates illustrative.
4 bmi    : bmi-calculator: kg = BMI x m^2. 24.9 x 1.60^2 = 63.7 kg; 24.9 x 1.85^2 = 85.2 kg; gap 21.5 kg. WHO adult normal 18.5-24.9.
5 winrate: risk-reward / expectancy. 70% x $50 - 30% x $150 = -$10 a trade; 100 trades: +3,500 - 4,500 = -$1,000.
           Break-even win rate = 150 / (50 + 150) = 75%. Before costs.
"""
import sys, os, subprocess, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_fx import *
from reels_2026_11_21 import options, row, small, end
from reels_2026_11_24 import reveal_num, bignum

SLOW = 1.75
BASE = 13.2
MINT = (140, 255, 200)
PALE = (220, 225, 255)
A_END = 10.8

# ---------------- 1. The UAE turns 55: how many days old? ----------------
def uae55(t):
    if t < 3.2:
        im = scene_bg(t, "night", 121); d = ImageDraw.Draw(im)
        kinetic(im, "On 2 Dec the UAE turns", 340, t, -1.2, 70, WHITE)
        bignum(im, t, -0.8, 1.0, 1, 55, 500, "{:.0f}", 220, GOLD)
        kinetic(im, "How many days old?", 680, t, -1.0, 84, WHITE)
        options(im, t, 0.8, ["A  12,045 days", "B  20,089 days", "C  55,000 days"], 810, win=1, t_win=2.6)
        calendar(d, 250, 1330, 0.85, "2")
        souq(im, 720, 1340, 0.6, t, "thinking"); speech(im, 760, 1210, "Guess first!", 1.4, t, 44)
        return punch(im, t, 0.0)
    if t < 6.6:
        im = scene_bg(t, "sky", 123); rays(im, W / 2, 640, t, WHITE, 24); d = ImageDraw.Draw(im)
        kinetic(im, "2 Dec 1971 → 2 Dec 2026", 470, t, 3.2, 72, WHITE)
        bignum(im, t, 3.3, 4.1, 0, 20089, 640, "{:,.0f} days", 140, GOLD)
        sparkles(im, W / 2, 640, t, 4.1, 4, 16, 380, WHITE)
        pill(im, W / 2, 820, "Answer B · 55 years old", t, 4.3, WHITE, INK, 50)
        trophy(d, 800, 1300, 0.7)
        souq(im, 330, 1320, 0.6, t, "shocked" if t < 4.6 else "wink"); speech(im, 450, 1120, "Happy 55th!", 4.6, t, 44)
        return shake(im, t, 4.1, 14)
    if t < A_END:
        im = scene_bg(t, "mint", 125); d = ImageDraw.Draw(im)
        kinetic(im, "Where 20,089 comes from", 360, t, 6.6, 72, WHITE)
        row(im, 520, "55 years × 365", "20,075", t, 6.9, vcol=WHITE, box=(20, 50, 44))
        row(im, 670, "Leap days 1972–2024", "+14", t, 7.7, vcol=MINT, box=(20, 50, 44))
        row(im, 820, "In seconds", "≈ 1.74 billion", t, 8.5, vcol=GOLD, box=(20, 50, 44))
        small(im, "How many days old are you?", 960, WHITE, 48)
        calendar(d, 250, 1300, 0.8, "55")
        souq(im, 720, 1310, 0.55, t, "happy"); speech(im, 740, 1160, "Check yours!", 9.2, t, 44)
        return punch(im, t, 6.9, 0.05)
    return end(t, A_END, "Free age|calculator", "berry", 127)

# ---------------- 2. 5-cent plot = how many sq ft? ----------------
def plot(im, x, y, s, t, label="?"):
    d = ImageDraw.Draw(im); w = 300 * s
    shadow(im, (x - w, y - w * .6, x + w, y + w * .6), 30, 20, 80); d = ImageDraw.Draw(im)
    d.polygon([(x - w, y), (x, y - w * .55), (x + w, y), (x, y + w * .55)], fill=(90, 170, 80), outline=(40, 90, 40))
    for i in range(9):  # fence posts
        for (ax, ay), (bx, by) in (((x - w, y), (x, y - w * .55)), ((x, y - w * .55), (x + w, y)), ((x + w, y), (x, y + w * .55)), ((x, y + w * .55), (x - w, y))):
            px, py = lerp(ax, bx, i / 8), lerp(ay, by, i / 8)
            d.rectangle([px - 4 * s, py - 30 * s, px + 4 * s, py], fill=(140, 90, 40))
    d.text((x, y), label, font=F("k", 60 * s), fill=WHITE, anchor="mm")

def conv_screen(d, sb, t):
    x0, y0, x1, y1 = sb; cx = (x0 + x1) / 2
    d.rounded_rectangle([x0 + 14, y0 + 50, x1 - 14, y0 + 100], 14, fill=GOLD)
    d.text((cx, y0 + 75), "Converter", font=F("b", 24), fill=INK, anchor="mm")
    d.rounded_rectangle([x0 + 14, y0 + 125, x1 - 14, y0 + 195], 14, fill=WHITE, outline=(200, 200, 205), width=3)
    d.text((cx, y0 + 160), "5 cent", font=F("k", 34), fill=INK, anchor="mm")
    d.text((cx, y0 + 230), "=", font=F("k", 36), fill=INK, anchor="mm")
    d.rounded_rectangle([x0 + 14, y0 + 265, x1 - 14, y0 + 385], 14, fill=(225, 245, 232), outline=GREEN, width=3)
    d.text((cx, y0 + 305), "2,178", font=F("k", 40), fill=(20, 110, 60), anchor="mm")
    d.text((cx, y0 + 352), "sq ft", font=F("b", 28), fill=(20, 110, 60), anchor="mm")

def cents(t):
    if t < 3.2:
        im = scene_bg(t, "mint", 221); d = ImageDraw.Draw(im)
        kinetic(im, "A plot of", 340, t, -1.2, 84, WHITE)
        bignum(im, t, -0.8, 0.8, 1, 5, 490, "{:.0f} cents", 190, GOLD)
        kinetic(im, "= how many sq ft?", 660, t, -1.0, 84, WHITE)
        options(im, t, 0.8, ["A  500 sq ft", "B  2,178 sq ft", "C  5,000 sq ft"], 800, win=1, t_win=2.6)
        plot(im, 280, 1330, 0.7, t)
        souq(im, 760, 1340, 0.6, t, "thinking"); speech(im, 790, 1210, "Guess first!", 1.4, t, 44)
        return punch(im, t, 0.0)
    if t < 6.6:
        im = scene_bg(t, "sunset", 223); rays(im, W / 2, 640, t, WHITE, 24); d = ImageDraw.Draw(im)
        kinetic(im, "5 cents =", 470, t, 3.2, 84, WHITE)
        reveal_num(im, "2,178 sq ft", 640, t, 3.4, 150, GOLD)
        sparkles(im, W / 2, 640, t, 3.5, 5, 16, 360, WHITE)
        pill(im, W / 2, 820, "Answer B · 1 cent = 435.6 sq ft", t, 4.2, WHITE, INK, 48)
        plot(im, 760, 1300, 0.6, t, "2,178")
        souq(im, 300, 1320, 0.6, t, "shocked" if t < 4.6 else "wink"); speech(im, 420, 1120, "Bigger than you thought?", 4.6, t, 42)
        return shake(im, t, 3.4, 16)
    if t < A_END:
        im = scene_bg(t, "night", 225); d = ImageDraw.Draw(im)
        kinetic(im, "Kerala land in numbers", 360, t, 6.6, 76, WHITE)
        row(im, 520, "1 cent", "435.6 sq ft", t, 6.9, vcol=GOLD)
        row(im, 670, "5 cents", "≈ 202 m²", t, 7.7, vcol=MINT)
        row(im, 820, "100 cents", "1 acre", t, 8.5, vcol=(255, 200, 230))
        small(im, "Square 5-cent plot ≈ 46.7 ft a side", 960, WHITE, 46)
        phone(im, 250, 1272, 0.6, conv_screen, t)
        souq(im, 740, 1330, 0.55, t, "cool" if t > 8.5 else "happy")
        return punch(im, t, 8.5, 0.05)
    return end(t, A_END, "Free land|converter", "sky", 227)

# ---------------- 3. 8% raise, 6% inflation: real raise? ----------------
def raise_(t):
    if t < 3.2:
        im = scene_bg(t, "berry", 321); d = ImageDraw.Draw(im)
        kinetic(im, "Your salary went up", 340, t, -1.2, 80, WHITE)
        bignum(im, t, -0.8, 0.8, 0, 8, 500, "+{:.0f}%", 220, MINT)
        kinetic(im, "Prices rose 6%. Real raise?", 680, t, -1.0, 68, WHITE, hl=["6%."], hl_col=(255, 170, 170))
        options(im, t, 0.8, ["A  2%", "B  1.9%", "C  14%"], 810, win=1, t_win=2.6)
        note(im, 250, 1300, 300, -12); coins_stack(d, 250, 1470, 3, 48)
        souq(im, 740, 1340, 0.6, t, "thinking"); speech(im, 770, 1210, "Guess first!", 1.4, t, 44)
        return punch(im, t, 0.0)
    if t < 6.6:
        im = scene_bg(t, "night", 323); rays(im, W / 2, 640, t, GOLD, 24); d = ImageDraw.Draw(im)
        kinetic(im, "Your real raise is", 470, t, 3.2, 84, WHITE)
        reveal_num(im, "1.9%", 640, t, 3.4, 200, GOLD)
        sparkles(im, W / 2, 640, t, 3.5, 6, 16, 330, GOLD)
        pill(im, W / 2, 830, "Answer B · 1.08 ÷ 1.06 − 1", t, 4.2, WHITE, INK, 50)
        piggy(im, 780, 1320, 0.7, t)
        souq(im, 300, 1320, 0.6, t, "shocked" if t < 4.6 else "cool"); speech(im, 420, 1120, "Not quite 2%", 4.6, t, 44)
        return shake(im, t, 3.4, 14)
    if t < A_END:
        im = scene_bg(t, "sky", 325); d = ImageDraw.Draw(im)
        kinetic(im, "On a ₹50,000 salary", 360, t, 6.6, 76, WHITE)
        row(im, 520, "New pay (+8%)", "₹54,000", t, 6.9, vcol=MINT)
        row(im, 670, "In today's prices", "₹50,943", t, 7.7, vcol=GOLD)
        row(im, 820, "Only a 5% raise?", "−0.9%", t, 8.5, vcol=(255, 170, 170))
        pill(im, W / 2, 980, "Below inflation = a pay cut", t, 9.1, RED, WHITE, 48)
        souq(im, 540, 1340, 0.55, t, "sad" if t > 8.5 else "thinking")
        return shake(im, t, 8.5, 12)
    return end(t, A_END, "Free percentage|calculator", "mint", 327)

# ---------------- 4. Same BMI, 160 cm vs 185 cm ----------------
def bmi(t):
    if t < 3.2:
        im = scene_bg(t, "sky", 421); d = ImageDraw.Draw(im)
        kinetic(im, "Same BMI:", 340, t, -1.2, 84, WHITE)
        bignum(im, t, -0.8, 0.8, 15, 24.9, 490, "{:.1f}", 220, GOLD)
        kinetic(im, "160 cm vs 185 cm. Weight gap?", 670, t, -1.0, 62, WHITE)
        options(im, t, 0.8, ["A  About 5 kg", "B  About 12 kg", "C  About 21 kg"], 800, win=2, t_win=2.6)
        souq(im, 340, 1370, 0.48, t, "thinking"); souq(im, 720, 1330, 0.62, t + 0.7, "thinking", body=(120, 200, 255))
        speech(im, 760, 1170, "Guess first!", 1.4, t, 44)
        return punch(im, t, 0.0)
    if t < 6.6:
        im = scene_bg(t, "mint", 423); rays(im, W / 2, 640, t, WHITE, 22); d = ImageDraw.Draw(im)
        kinetic(im, "Same BMI, but", 470, t, 3.2, 84, WHITE)
        reveal_num(im, "21.5 kg apart", 640, t, 3.4, 140, GOLD)
        sparkles(im, W / 2, 640, t, 3.5, 7, 16, 360, WHITE)
        pill(im, W / 2, 820, "Answer C · 63.7 kg vs 85.2 kg", t, 4.2, WHITE, INK, 48)
        souq(im, 330, 1370, 0.48, t, "shocked" if t < 4.6 else "happy"); souq(im, 720, 1330, 0.62, t + 0.7, "shocked" if t < 4.6 else "wink", body=(120, 200, 255))
        speech(im, 720, 1170, "Both 24.9!", 4.6, t, 44)
        return shake(im, t, 3.4, 14)
    if t < A_END:
        im = scene_bg(t, "sunset", 425); d = ImageDraw.Draw(im)
        kinetic(im, "BMI = kg ÷ (height in m)²", 360, t, 6.6, 66, WHITE)
        row(im, 520, "160 cm at 24.9", "63.7 kg", t, 6.9, vcol=GOLD)
        row(im, 670, "185 cm at 24.9", "85.2 kg", t, 7.7, vcol=GOLD)
        row(im, 820, "WHO adult 'normal'", "18.5–24.9", t, 8.5, vcol=MINT)
        small(im, "A screening number, not a diagnosis", 960, WHITE, 46)
        souq(im, 540, 1340, 0.55, t, "cool" if t > 8.5 else "happy")
        return punch(im, t, 8.5, 0.05)
    return end(t, A_END, "Free BMI|calculator", "berry", 427)

# ---------------- 5. 70% win rate and still losing ----------------
def winrate(t):
    if t < 3.2:
        im = scene_bg(t, "night", 521); d = ImageDraw.Draw(im)
        kinetic(im, "You win", 340, t, -1.2, 84, WHITE)
        bignum(im, t, -0.8, 0.8, 0, 70, 490, "{:.0f}%", 220, MINT)
        kinetic(im, "of trades. Still losing?", 660, t, -1.0, 76, WHITE)
        small(im, "Average win $50 · average loss $150", 740, WHITE, 44)
        options(im, t, 0.8, ["A  Impossible", "B  Yes: −$10 a trade", "C  You break even"], 860, gap=112, win=1, t_win=2.6)
        chart_up(d, 120, 1500, 380, 220, 1.0, WHITE)
        souq(im, 760, 1360, 0.6, t, "thinking"); speech(im, 790, 1230, "Guess first!", 1.4, t, 44)
        return punch(im, t, 0.0)
    if t < 6.6:
        im = scene_bg(t, "berry", 523); d = ImageDraw.Draw(im)
        kinetic(im, "Average per trade:", 470, t, 3.2, 84, WHITE)
        reveal_num(im, "−$10", 640, t, 3.4, 220, (255, 120, 120))
        pill(im, W / 2, 830, "Answer B · 100 trades = −$1,000", t, 4.2, WHITE, INK, 48)
        coins_stack(d, 800, 1450, 2, 50, "$")
        souq(im, 330, 1330, 0.6, t, "shocked" if t < 4.6 else "sad"); speech(im, 450, 1130, "70% wins?!", 4.6, t, 44)
        return shake(im, t, 3.4, 18)
    if t < A_END:
        im = scene_bg(t, "sky", 525); rays(im, W / 2, 900, t, WHITE, 18); d = ImageDraw.Draw(im)
        kinetic(im, "100 trades at 70%", 360, t, 6.6, 80, WHITE)
        row(im, 520, "70 wins × $50", "+$3,500", t, 6.9, vcol=MINT)
        row(im, 670, "30 losses × $150", "−$4,500", t, 7.7, vcol=(255, 170, 170))
        row(im, 820, "Break-even win rate", "75%", t, 8.5, vcol=GOLD)
        small(im, "Size of wins matters as much as how often", 960, WHITE, 44)
        sparkles(im, W / 2, 820, t, 8.6, 8, 14, 420, GOLD)
        souq(im, 540, 1340, 0.55, t, "wink" if t > 8.5 else "thinking")
        return punch(im, t, 8.5, 0.05)
    return end(t, A_END, "Free risk-reward|calculator", "sunset", 527)

REELS = dict(uae55=uae55, cents=cents, raise_=raise_, bmi=bmi, winrate=winrate)
REELS["raise"] = raise_

CUES = {
    "uae55": "0:boom,0.2:tick*8,0.8:pop,0.95:pop2,1.1:pop,1.4:pop2,1.9:riser,2.6:ding,3.2:whoosh,3.3:tick*10,4.1:success,4.15:sparkle,4.3:pop,4.6:pop2,6.6:swoosh,6.9:pop,7.7:pop,8.5:pop,9.2:pop2,10.8:whoosh,10.9:sparkle",
    "cents": "0:boom,0.2:tick*5,0.8:pop,0.95:pop2,1.1:pop,1.4:pop2,1.9:riser,2.6:ding,3.2:whoosh,3.4:hit,3.5:sparkle,4.2:pop,4.6:pop2,6.6:swoosh,6.9:pop,7.7:pop,8.5:pop,10.8:whoosh,10.9:success",
    "raise": "0:boom,0.2:coin*6,0.8:pop,0.95:pop2,1.1:pop,1.4:pop2,1.9:riser,2.6:ding,3.2:whoosh,3.4:hit,3.5:sparkle,4.2:pop,4.6:pop2,6.6:swoosh,6.9:cash,7.7:pop,8.5:fail,9.1:pop2,10.8:whoosh,10.9:success",
    "bmi": "0:boom,0.2:tick*6,0.8:pop,0.95:pop2,1.1:pop,1.4:pop2,1.9:riser,2.6:ding,3.2:whoosh,3.4:ding,3.5:sparkle,4.2:pop,4.6:pop2,6.6:swoosh,6.9:pop,7.7:pop,8.5:pop,10.8:whoosh,10.9:success",
    "winrate": "0:boom,0.2:tick*8,0.8:pop,0.95:pop2,1.1:pop,1.4:pop2,1.9:riser,2.6:ding,3.2:whoosh,3.4:fail,4.2:pop,4.6:pop2,6.6:swoosh,6.9:cash,7.7:fail,8.5:ding,8.6:sparkle,10.8:whoosh,10.9:success",
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
