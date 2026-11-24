"""CalcSouq daily reels for 2026-11-24 (reading pace, SLOW = 1.75, 23.1 s each; big counting number on frame 1).
Every figure comes from the site's own formulas. Usage:
  python3 build/reels_2026_11_24.py <reel> [t1,t2,...]   -> stills at real-time seconds (reel = billion|gst|natday|ounce|traders)
  python3 build/reels_2026_11_24.py <reel>               -> /tmp/<reel>_v.mp4 (silent)
  python3 build/reels_2026_11_24.py cues <reel>          -> audio cue string in real-time seconds
1 billion : age-calculator. 1e9 s = 11,574.07 days = 31.69 y (31 y 8 m). Born 1 Jan 1996 00:00 -> Thu 9 Sep 2027 01:46.
            2e9 s = 63.4 y.
2 gst     : gst-calculator (remove GST): GST = incl x r / (100 + r). ₹118 at 18% -> ₹18, base ₹100. Trap: 118 x 18% = ₹21.24.
3 natday  : date-calculator. UAE private sector Eid Al Etihad paid holiday Wed 2 + Thu 3 Dec 2026 (MoHRE, The National /
            Gulf News 13 Nov 2026). Take Fri 4 Dec -> Wed 2 to Sun 6 Dec = 5 days off for 1 day of leave (Sat-Sun weekend).
4 ounce   : gold-tola-pavan-converter (tools_extra.GU): pavan 8 g, tola 11.6638 g, troy oz 31.1035 g.
            31.1035 / 8 = 3.89 pavan; / 11.6638 = 2.67 tola.
5 traders : trading-strategy-simulator logic (tools_unique.py), 100 runs x 100 trades, ₹/$10,000 start, risk 1% of balance,
            50% win, win 1.5R, costs 0.05R, random.Random(2026112405): 90 ended up, 10 down; best 16,347 (+63%),
            worst 9,209 (-8%), median 11,818 (+18%), longest losing streak 15. Expectancy +0.2R a trade.
            (300 repeats: 89-97 of 100 in profit, so "about 9 in 10" is stable.)
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

def bignum(im, t, t0, t1, v0, v1, y, fmt, size, col):
    d = ImageDraw.Draw(im); d.text((W / 2, y), fmt.format(count(v0, v1, t, t0, t1)), font=F("k", size), fill=col, anchor="mm")

# ---------------- 1. 1 billion seconds old ----------------
def billion(t):
    if t < 3.2:
        im = scene_bg(t, "night", 111); d = ImageDraw.Draw(im)
        kinetic(im, "You turn", 340, t, -1.2, 90, WHITE)
        bignum(im, t, -0.8, 1.2, 1e8, 1e9, 470, "{:,.0f}", 108, GOLD)
        kinetic(im, "seconds old at…?", 620, t, -1.0, 90, WHITE)
        options(im, t, 0.8, ["A  21 years", "B  31 years 8 months", "C  41 years"], 760, win=1, t_win=2.6)
        calendar(d, 250, 1320, 0.85, "?")
        souq(im, 720, 1330, 0.6, t, "thinking"); speech(im, 760, 1200, "Guess first!", 1.4, t, 44)
        return punch(im, t, 0.0)
    if t < 6.6:
        im = scene_bg(t, "sunset", 113); rays(im, W / 2, 640, t, WHITE, 24); d = ImageDraw.Draw(im)
        kinetic(im, "1 billion seconds =", 470, t, 3.2, 84, WHITE)
        reveal_num(im, "31.7 years", 640, t, 3.4, 150, GOLD)
        sparkles(im, W / 2, 640, t, 3.5, 4, 16, 330, WHITE)
        pill(im, W / 2, 820, "Answer B · 11,574 days", t, 4.2, WHITE, INK, 50)
        trophy(d, 800, 1300, 0.7)
        souq(im, 330, 1320, 0.6, t, "shocked" if t < 4.6 else "wink"); speech(im, 450, 1120, "Older than you think!", 4.6, t, 42)
        return shake(im, t, 3.4, 16)
    if t < A_END:
        im = scene_bg(t, "mint", 115); d = ImageDraw.Draw(im)
        kinetic(im, "Born 1 Jan 1996?", 360, t, 6.6, 84, WHITE)
        row(im, 520, "Your billion day", "Thu 9 Sep 2027", t, 6.9, vcol=GOLD, box=(20, 50, 44))
        row(im, 670, "Days lived by then", "11,574", t, 7.7, vcol=MINT, box=(20, 50, 44))
        row(im, 820, "2 billion seconds", "≈ 63.4 yrs", t, 8.5, vcol=(255, 200, 230), box=(20, 50, 44))
        calendar(d, 250, 1300, 0.8, "9")
        souq(im, 720, 1310, 0.55, t, "happy"); speech(im, 740, 1160, "Set a reminder!", 8.9, t, 44)
        return punch(im, t, 6.9, 0.05)
    return end(t, A_END, "Free age|calculator", "berry", 117)

# ---------------- 2. GST inside ₹118 ----------------
def gst(t):
    if t < 3.2:
        im = scene_bg(t, "gold", 211); d = ImageDraw.Draw(im)
        kinetic(im, "Bill with 18% GST:", 360, t, -1.2, 80, INK)
        bignum(im, t, -0.6, 0.8, 60, 118, 520, "₹{:,.0f}", 210, INK)
        kinetic(im, "How much is GST?", 700, t, -1.0, 84, (150, 40, 40))
        options(im, t, 0.8, ["A  ₹21.24", "B  ₹18", "C  ₹11.80"], 820, gap=112, win=1, t_win=2.6)
        doc(d, 230, 1340, 0.7, "BILL", RED)
        souq(im, 720, 1340, 0.6, t, "thinking"); speech(im, 760, 1210, "Guess first!", 1.4, t, 44)
        return punch(im, t, 0.0)
    if t < 6.6:
        im = scene_bg(t, "night", 213); rays(im, W / 2, 640, t, GOLD, 26); d = ImageDraw.Draw(im)
        kinetic(im, "GST inside ₹118 is", 470, t, 3.2, 84, WHITE)
        reveal_num(im, "₹18", 650, t, 3.4, 200, GOLD)
        sparkles(im, W / 2, 650, t, 3.5, 5, 16, 330, GOLD)
        pill(im, W / 2, 840, "Answer B · not ₹21.24", t, 4.2, WHITE, INK, 50)
        coins_stack(d, 820, 1430, 5, 50)
        souq(im, 330, 1320, 0.6, t, "shocked" if t < 4.6 else "wink"); speech(im, 450, 1120, "Divide, don't multiply", 4.6, t, 42)
        return shake(im, t, 3.4, 16)
    if t < A_END:
        im = scene_bg(t, "sky", 215); d = ImageDraw.Draw(im)
        kinetic(im, "GST = bill × 18 ÷ 118", 360, t, 6.6, 76, WHITE)
        row(im, 520, "Bill (incl. GST)", "₹118", t, 6.9, vcol=WHITE)
        row(im, 670, "Price before GST", "₹100", t, 7.7, vcol=MINT)
        row(im, 820, "GST at 18%", "₹18", t, 8.5, vcol=GOLD)
        small(im, "Any rate: bill × rate ÷ (100 + rate)", 960, WHITE, 44)
        souq(im, 540, 1330, 0.55, t, "cool" if t > 8.5 else "thinking")
        return punch(im, t, 8.5, 0.05)
    return end(t, A_END, "Free GST|calculator", "mint", 217)

# ---------------- 3. UAE National Day: 1 day of leave = 5 days off ----------------
DAYS = [("WED", "2", "Holiday", GREEN), ("THU", "3", "Holiday", GREEN), ("FRI", "4", "Leave", GOLD), ("SAT", "5", "Weekend", BLUE), ("SUN", "6", "Weekend", BLUE)]
def strip(im, t, t0, y):
    d = ImageDraw.Draw(im)
    for i, (dn, num, lab, col) in enumerate(DAYS):
        p = back(seg(t, t0 + i * 0.12, t0 + i * 0.12 + 0.35))
        if p <= 0: continue
        x = 140 + i * 200; yy = y + (1 - p) * 60
        shadow(im, (x - 85, yy - 110, x + 85, yy + 110), 26, 12, 60, (0, 8)); d = ImageDraw.Draw(im)
        d.rounded_rectangle([x - 85, yy - 110, x + 85, yy + 110], 26, fill=WHITE, outline=INK, width=5)
        d.rounded_rectangle([x - 85, yy - 110, x + 85, yy - 50], 26, fill=col, outline=INK, width=5)
        d.text((x, yy - 80), dn, font=F("k", 36), fill=INK if col == GOLD else WHITE, anchor="mm")
        d.text((x, yy + 20), num, font=F("k", 96), fill=INK, anchor="mm")
        d.text((x, yy + 84), lab, font=F("b", 28), fill=(80, 85, 95), anchor="mm")

def natday(t):
    if t < 3.2:
        im = scene_bg(t, "mint", 311); d = ImageDraw.Draw(im)
        kinetic(im, "UAE National Day:", 350, t, -1.2, 80, WHITE)
        kinetic(im, "1 day of leave =", 470, t, -1.0, 92, WHITE)
        bignum(im, t, -1.0, 0.3, 1, 5, 630, "{:.0f} days off", 150, GOLD)
        options(im, t, 0.8, ["A  Tue 1 Dec", "B  Fri 4 Dec", "C  Mon 7 Dec"], 800, win=1, t_win=2.6)
        calendar(d, 250, 1330, 0.85, "?")
        souq(im, 720, 1340, 0.6, t, "thinking"); speech(im, 760, 1210, "Which day?", 1.4, t, 44)
        return punch(im, t, 0.0)
    if t < 6.6:
        im = scene_bg(t, "sunset", 313); rays(im, W / 2, 700, t, WHITE, 24); d = ImageDraw.Draw(im)
        kinetic(im, "Take Friday 4 Dec off", 420, t, 3.2, 80, WHITE)
        strip(im, t, 3.4, 640)
        pill(im, W / 2, 860, "Answer B · Wed 2 → Sun 6 Dec", t, 4.2, WHITE, INK, 48)
        sparkles(im, 540, 640, t, 3.9, 6, 16, 420, GOLD)
        souq(im, 540, 1310, 0.6, t, "shocked" if t < 4.6 else "cool"); speech(im, 600, 1110, "5 days for 1!", 4.6, t, 44)
        return punch(im, t, 3.4, 0.06)
    if t < A_END:
        im = scene_bg(t, "night", 315); d = ImageDraw.Draw(im)
        kinetic(im, "Private sector · Mon–Fri job", 360, t, 6.6, 64, WHITE)
        row(im, 520, "Wed 2 · Thu 3 Dec", "Paid holiday", t, 6.9, vcol=MINT)
        row(im, 670, "Fri 4 Dec", "1 day leave", t, 7.7, vcol=GOLD)
        row(im, 820, "Sat 5 · Sun 6 Dec", "Weekend", t, 8.5, vcol=(170, 200, 255))
        small(im, "Check your employer's notice", 960, PALE, 44)
        calendar(d, 250, 1320, 0.8, "4")
        souq(im, 720, 1320, 0.55, t, "wink" if t > 8.5 else "happy")
        return im
    return end(t, A_END, "Free date|calculator", "sky", 317)

# ---------------- 4. 1 troy ounce = how many pavan? ----------------
def ounce(t):
    if t < 3.2:
        im = scene_bg(t, "berry", 411); d = ImageDraw.Draw(im)
        kinetic(im, "1 ounce of gold", 350, t, -1.2, 96, WHITE)
        bignum(im, t, -0.6, 1.0, 10, 31.1, 510, "{:.1f} g", 180, GOLD)
        kinetic(im, "= how many pavan?", 670, t, -1.0, 84, WHITE)
        options(im, t, 0.8, ["A  1 pavan", "B  About 2", "C  Almost 4"], 800, win=2, t_win=2.6)
        gold_bar(d, 250, 1330, 1.1); gold_bar(d, 250, 1240, 0.9)
        souq(im, 720, 1340, 0.6, t, "thinking"); speech(im, 760, 1210, "Guess first!", 1.4, t, 44)
        return punch(im, t, 0.0)
    if t < 6.6:
        im = scene_bg(t, "night", 413); rays(im, W / 2, 640, t, GOLD, 26); d = ImageDraw.Draw(im)
        kinetic(im, "1 troy ounce =", 470, t, 3.2, 84, WHITE)
        reveal_num(im, "3.9 pavan", 640, t, 3.4, 160, GOLD)
        sparkles(im, W / 2, 640, t, 3.5, 7, 16, 330, GOLD)
        pill(im, W / 2, 820, "Answer C · 31.1 g ÷ 8 g", t, 4.2, WHITE, INK, 50)
        for i in range(4): gold_bar(d, 700 + (i % 2) * 120, 1400 - (i // 2) * 90 - (i % 2) * 0, 0.8)
        souq(im, 300, 1320, 0.6, t, "shocked" if t < 4.6 else "cool"); speech(im, 420, 1120, "Almost 4!", 4.6, t, 44)
        return shake(im, t, 3.4, 14)
    if t < A_END:
        im = scene_bg(t, "sunset", 415); d = ImageDraw.Draw(im)
        kinetic(im, "Lightest to heaviest", 360, t, 6.6, 76, WHITE)
        row(im, 520, "1 pavan (sovereign)", "8 g", t, 6.9, vcol=GOLD)
        row(im, 670, "1 tola", "11.66 g", t, 7.7, vcol=GOLD)
        row(im, 820, "1 troy ounce", "31.10 g", t, 8.5, vcol=GOLD)
        pill(im, W / 2, 980, "1 ounce ≈ 2.67 tola", t, 9.1, GOLD, INK, 50)
        souq(im, 540, 1330, 0.55, t, "happy")
        return punch(im, t, 8.5, 0.05)
    return end(t, A_END, "Free tola & pavan|converter", "mint", 417)

# ---------------- 5. 100 traders, same strategy ----------------
def grid(im, t, t0, cx, cy, up=90, gap=42, r=15):
    d = ImageDraw.Draw(im); order = list(range(100)); import random as _r; _r.Random(5).shuffle(order)
    red = set(order[:100 - up])
    for i in range(100):
        p = ease(seg(t, t0 + i * 0.008, t0 + i * 0.008 + 0.2))
        if p <= 0: continue
        x = cx + (i % 10 - 4.5) * gap; y = cy + (i // 10 - 4.5) * gap; rr = r * p
        d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=RED if i in red else GREEN, outline=WHITE, width=2)

def traders(t):
    if t < 3.2:
        im = scene_bg(t, "sky", 511); d = ImageDraw.Draw(im)
        kinetic(im, "Same strategy for", 340, t, -1.2, 80, WHITE)
        bignum(im, t, -1.0, 0.4, 1, 100, 480, "{:.0f} traders", 136, GOLD)
        kinetic(im, "How many end up?", 640, t, -1.0, 84, WHITE)
        small(im, "50% wins · win 1.5R · lose 1R · 100 trades", 720, WHITE, 44)
        options(im, t, 0.8, ["A  About half", "B  About 9 in 10", "C  All 100"], 850, win=1, t_win=2.6)
        chart_up(d, 120, 1500, 380, 260, 1.0, WHITE)
        souq(im, 760, 1360, 0.6, t, "thinking"); speech(im, 800, 1230, "Guess first!", 1.4, t, 44)
        return punch(im, t, 0.0)
    if t < 6.6:
        im = scene_bg(t, "night", 513); d = ImageDraw.Draw(im)
        kinetic(im, "After 100 trades each:", 400, t, 3.2, 76, WHITE)
        reveal_num(im, "90 up · 10 down", 520, t, 3.4, 110, GOLD)
        grid(im, t, 3.5, W / 2, 830)
        pill(im, W / 2, 1100, "Answer B · same rules, 10 lost", t, 4.4, WHITE, INK, 46)
        souq(im, 540, 1390, 0.5, t, "shocked" if t < 5.0 else "thinking"); speech(im, 600, 1265, "Same rules?!", 4.8, t, 44)
        return shake(im, t, 3.4, 14)
    if t < A_END:
        im = scene_bg(t, "berry", 515); d = ImageDraw.Draw(im)
        kinetic(im, "Same edge, different luck", 360, t, 6.6, 70, WHITE)
        row(im, 520, "Best trader", "+63%", t, 6.9, vcol=MINT, box=(50, 20, 50))
        row(im, 670, "Worst trader", "−8%", t, 7.7, vcol=(255, 170, 170), box=(50, 20, 50))
        row(im, 820, "Longest losing run", "15 in a row", t, 8.5, vcol=GOLD, box=(50, 20, 50))
        small(im, "One simulator run · costs 0.05R · education only", 960, WHITE, 44)
        rocket(im, 260, 1300, 0.5, t)
        souq(im, 720, 1330, 0.55, t, "wink" if t > 8.5 else "thinking")
        return im
    return end(t, A_END, "Free trading|simulator", "sunset", 517)

REELS = dict(billion=billion, gst=gst, natday=natday, ounce=ounce, traders=traders)

# audio cues in BASE seconds (scaled by SLOW for the real video)
CUES = {
    "billion": "0:boom,0.3:tick*8,0.8:pop,0.95:pop2,1.1:pop,1.4:pop2,1.9:riser,2.6:ding,3.2:whoosh,3.4:hit,3.5:sparkle,4.2:pop,4.6:pop2,6.6:swoosh,6.9:pop,7.7:pop,8.5:pop,8.9:pop2,10.8:whoosh,10.9:success",
    "gst": "0:boom,0.1:coin*5,0.8:pop,0.95:pop2,1.1:pop,1.4:pop2,1.9:riser,2.6:ding,3.2:whoosh,3.4:cash,3.5:sparkle,4.2:pop,4.6:pop2,6.6:swoosh,6.9:pop,7.7:pop,8.5:ding,10.8:whoosh,10.9:success",
    "natday": "0:boom,0.2:tick*5,0.8:pop,0.95:pop2,1.1:pop,1.4:pop2,1.9:riser,2.6:ding,3.2:whoosh,3.4:pop,3.55:pop,3.7:pop,3.85:pop,4.0:pop2,4.2:success,4.6:pop2,6.6:swoosh,6.9:pop,7.7:pop,8.5:pop,10.8:whoosh,10.9:sparkle",
    "ounce": "0:boom,0.2:tick*6,0.8:pop,0.95:pop2,1.1:pop,1.4:pop2,1.9:riser,2.6:ding,3.2:whoosh,3.4:coin*4,3.6:sparkle,4.2:pop,4.6:pop2,6.6:swoosh,6.9:pop,7.7:pop,8.5:pop,9.1:ding,10.8:whoosh,10.9:success",
    "traders": "0:boom,0.2:tick*8,0.8:pop,0.95:pop2,1.1:pop,1.4:pop2,1.9:riser,2.6:ding,3.2:whoosh,3.4:hit,3.5:tick*10,4.4:fail,4.8:pop2,6.6:swoosh,6.9:cash,7.7:fail,8.5:pop,10.8:whoosh,10.9:success",
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
