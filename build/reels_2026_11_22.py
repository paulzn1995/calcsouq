"""CalcSouq daily reels for 2026-11-22 (reading pace, SLOW = 1.75).
Every figure comes from the site's own formulas (see comments). Usage:
  python3 build/reels_2026_11_22.py <reel> [t1,t2,...]   -> stills at real-time seconds (reel = days|fdsip|grat|double|lots)
  python3 build/reels_2026_11_22.py <reel>               -> <reel>_v.mp4 (silent)
1 days   : date-calculator logic, 23 Nov–31 Dec 2026 inclusive = 39 days, 29 Mon–Fri, 10 weekend days; 2026 has 261 Mon–Fri.
2 fdsip  : ₹10,000/month, 15 years. SIP calc (12%, monthly, start of month) = ₹50,45,760; compound-interest calc
           (7%, quarterly, monthly additions at month end) = ₹31,58,504; invested ₹18,00,000.
3 grat   : uae-gratuity-calculator: basic/30 per day, 21 days × first 5 yrs, 30 days × later yrs, cap 24 × basic.
           AED 10,000 basic: 5 yrs 35,000; 10 yrs 85,000; cap 240,000 reached at 25.5 yrs.
4 double : compound-interest calc, yearly: ₹1 lakh at 8% → 9 yrs ₹1,99,900; 27 yrs ₹7,98,806. ln2/ln1.08 = 9.006.
5 lots   : position-size-calculator: $10,000, 1% = $100, 25-pip stop, $10/pip/lot → 0.40 lots; 1 lot loses $250.
           10 losses in a row risking % of balance: 1% → $9,044; 5% → $5,987.
"""
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_fx import *
from reels_2026_11_21 import options, row, small, end

SLOW = 1.75
BASE = 13.4
MINT = (140, 255, 200)

# ---------------- 1. Working days left in 2026 ----------------
def days(t):
    if t < 3.4:
        im = scene_bg(t, "sunset", 11); d = ImageDraw.Draw(im)
        kinetic(im, "How many WORKING", 420, t, -1.2, 92, WHITE, hl=["WORKING"])
        kinetic(im, "days are left in 2026?", 530, t, -1.0, 80, WHITE)
        options(im, t, 1.0, ["A  52 days", "B  39 days", "C  29 days"], 700)
        calendar(d, 250, 1290, 0.85, "31")
        souq(im, 720, 1300, 0.6, t, "thinking"); speech(im, 760, 1170, "Guess first!", 1.8, t, 42)
        return punch(im, t, 0.0)
    if t < 8.4:
        im = scene_bg(t, "sky", 13); d = ImageDraw.Draw(im)
        kinetic(im, "From tomorrow to 31 Dec", 380, t, 3.4, 70, WHITE)
        row(im, 560, "Days left", f"{count(0, 39, t, 3.7, 4.6):.0f}", t, 3.6)
        row(im, 710, "Weekend days", f"{count(0, 10, t, 4.9, 5.6):.0f}", t, 4.8, vcol=(255, 200, 200))
        row(im, 860, "Working days", f"{count(0, 29, t, 6.1, 6.9):.0f}", t, 6.0, vcol=MINT)
        calendar(d, 250, 1290, 0.8, str(int(count(39, 29, t, 6.0, 7.0))))
        souq(im, 720, 1300, 0.55, t, "shocked" if t > 6.9 else "thinking")
        im = shake(im, t, 6.9, 14)
        return im
    if t < 11.0:
        im = scene_bg(t, "night", 15); rays(im, W / 2, 640, t, GOLD, 26); d = ImageDraw.Draw(im)
        kinetic(im, "Only", 470, t, 8.4, 84, WHITE)
        d.text((W / 2, 640), "29 working days", font=F("k", 118), fill=GOLD, anchor="mm")
        sparkles(im, W / 2, 640, t, 8.6, 4, 16, 330, GOLD)
        pill(im, W / 2, 810, "= 232 hours at 8 a day", t, 9.0, WHITE, INK, 50)
        small(im, "Mon–Fri, before public holidays · 89% of 2026 is done", 900, (220, 225, 255), 34)
        souq(im, 330, 1320, 0.6, t, "wink"); speech(im, 470, 1120, "Pick ONE goal. Go!", 9.4, t, 40)
        calendar(d, 800, 1300, 0.7, "29")
        return punch(im, t, 8.5, 0.06)
    return end(t, 11.0, "Free days between|dates calculator", "mint", 17)

# ---------------- 2. FD vs SIP, same ₹10,000 a month ----------------
def fdsip(t):
    if t < 3.4:
        im = scene_bg(t, "gold", 21); d = ImageDraw.Draw(im)
        kinetic(im, "₹10,000 a month.", 420, t, -1.2, 104, INK)
        kinetic(im, "FD vs SIP: the gap?", 540, t, -1.0, 84, (150, 40, 40))
        small(im, "15 years · FD 7% vs SIP 12% (assumed)", 615, INK, 38)
        options(im, t, 1.0, ["A  ₹5 lakh", "B  ₹10 lakh", "C  ₹19 lakh"], 760)
        coins_stack(d, 200, 1420, 7, 52)
        souq(im, 700, 1300, 0.6, t, "thinking"); speech(im, 740, 1170, "Guess first!", 1.8, t, 42)
        return punch(im, t, 0.0)
    if t < 8.4:
        im = scene_bg(t, "berry", 23); d = ImageDraw.Draw(im)
        kinetic(im, "Same ₹18 lakh paid in", 380, t, 3.4, 72, WHITE)
        row(im, 560, "You put in", "₹18.0 lakh", t, 3.6, vcol=WHITE)
        row(im, 710, "FD/RD at 7%", f"₹{count(18, 31.6, t, 4.9, 5.8):.1f} lakh", t, 4.8, vcol=(255, 200, 230))
        row(im, 860, "SIP at 12%", f"₹{count(18, 50.5, t, 6.1, 7.2):.1f} lakh", t, 6.0, vcol=MINT)
        p = seg(t, 6.0, 7.4)
        note(im, 220, 1250, 240, -10); note(im, 260, 1320, 240, 8)
        piggy(im, 260, 1330, 0.55, t) if p == 0 else coins_stack(d, 250, 1430, int(3 + 6 * p), 48)
        souq(im, 720, 1300, 0.55, t, "shocked" if t > 7.2 else "thinking")
        return shake(im, t, 7.2, 14)
    if t < 11.0:
        im = scene_bg(t, "night", 25); rays(im, W / 2, 640, t, GOLD, 26); d = ImageDraw.Draw(im)
        kinetic(im, "The gap:", 470, t, 8.4, 84, WHITE)
        d.text((W / 2, 640), f"₹{count(0, 18.9, t, 8.5, 9.4):.1f} lakh", font=F("k", 150), fill=GOLD, anchor="mm")
        if t > 9.4: sparkles(im, W / 2, 640, t, 9.4, 5, 16, 330, GOLD)
        pill(im, W / 2, 820, "FD = fixed rate · SIP = market risk", t, 9.5, WHITE, INK, 44)
        small(im, "12% is an assumption, not a promise · before tax", 910, (220, 225, 255), 34)
        rocket(im, 820, 1290, 0.55, t)
        souq(im, 360, 1330, 0.6, t, "cool"); speech(im, 440, 1130, "Know the trade-off", 9.8, t, 40)
        return punch(im, t, 9.4, 0.06)
    return end(t, 11.0, "Free SIP &|FD calculators", "sky", 27)

# ---------------- 3. UAE gratuity: 21 vs 30 days ----------------
def grat(t):
    if t < 3.4:
        im = scene_bg(t, "night", 31); d = ImageDraw.Draw(im)
        kinetic(im, "10 years in the UAE.", 420, t, -1.2, 92, WHITE)
        kinetic(im, "Your gratuity?", 535, t, -1.0, 100, GOLD)
        small(im, "Basic salary AED 10,000 a month", 615, (220, 225, 255), 40)
        options(im, t, 1.0, ["A  AED 70,000", "B  AED 85,000", "C  AED 100,000"], 760)
        doc(d, 230, 1300, 0.75, "EOSB", GREEN)
        souq(im, 700, 1300, 0.6, t, "thinking"); speech(im, 740, 1170, "Guess first!", 1.8, t, 42)
        return punch(im, t, 0.0)
    if t < 8.4:
        im = scene_bg(t, "mint", 33); d = ImageDraw.Draw(im)
        kinetic(im, "The rule changes at year 5", 380, t, 3.4, 66, WHITE)
        row(im, 560, "Years 1–5: 21 days", "AED 7,000/yr", t, 3.6, box=(20, 50, 44))
        row(im, 710, "Year 6 on: 30 days", "AED 10,000/yr", t, 4.9, vcol=MINT, box=(20, 50, 44))
        pill(im, W / 2, 880, "Each year after 5 pays 43% more", t, 6.2, GOLD, INK, 48)
        calendar(d, 250, 1300, 0.8, str(int(count(1, 10, t, 3.8, 7.0))))
        souq(im, 720, 1300, 0.55, t, "shocked" if t > 6.2 else "thinking")
        return shake(im, t, 6.2, 14)
    if t < 11.0:
        im = scene_bg(t, "sunset", 35); rays(im, W / 2, 640, t, WHITE, 26); d = ImageDraw.Draw(im)
        kinetic(im, "After 10 years:", 470, t, 8.4, 84, WHITE)
        d.text((W / 2, 640), f"AED {count(0, 85000, t, 8.5, 9.4):,.0f}", font=F("k", 136), fill=WHITE, anchor="mm")
        if t > 9.4: sparkles(im, W / 2, 640, t, 9.4, 6, 16, 330, GOLD)
        pill(im, W / 2, 810, "35,000 + 50,000 · answer B", t, 9.5, INK, GOLD, 46)
        small(im, "Capped at 2 years' basic (AED 240,000)", 900, WHITE, 36)
        coins_stack(d, 820, 1430, 8, 50, "Dh")
        souq(im, 360, 1330, 0.6, t, "wink"); speech(im, 440, 1130, "Basic pay only!", 9.8, t, 40)
        return punch(im, t, 9.4, 0.06)
    return end(t, 11.0, "Free UAE gratuity|calculator", "berry", 37)

# ---------------- 4. How long to double your money ----------------
def double(t):
    if t < 3.4:
        im = scene_bg(t, "mint", 41); d = ImageDraw.Draw(im)
        kinetic(im, "₹1 lakh at 8%.", 420, t, -1.2, 110, WHITE)
        kinetic(im, "When does it double?", 540, t, -1.0, 80, MINT)
        options(im, t, 1.0, ["A  6 years", "B  9 years", "C  12.5 years"], 720)
        coins_stack(d, 230, 1420, 5, 52)
        souq(im, 700, 1300, 0.6, t, "thinking"); speech(im, 740, 1170, "Guess first!", 1.8, t, 42)
        return punch(im, t, 0.0)
    if t < 8.4:
        im = scene_bg(t, "gold", 43); d = ImageDraw.Draw(im)
        kinetic(im, "The Rule of 72", 380, t, 3.4, 92, INK)
        small(im, "72 ÷ interest rate = years to double", 460, INK, 40)
        row(im, 620, "At 6%", "about 12 yrs", t, 3.8, vcol=(255, 200, 200))
        row(im, 770, "At 8%", "about 9 yrs", t, 5.0)
        row(im, 920, "At 12%", "about 6 yrs", t, 6.2, vcol=MINT)
        chart_up(d, 130, 1450, 420, 300, seg(t, 3.6, 7.6), (40, 140, 90))
        souq(im, 760, 1300, 0.55, t, "happy" if t > 6.4 else "thinking")
        return im
    if t < 11.0:
        im = scene_bg(t, "berry", 45); rays(im, W / 2, 640, t, GOLD, 26); d = ImageDraw.Draw(im)
        kinetic(im, "Wait 27 years and it", 460, t, 8.4, 70, WHITE)
        kinetic(im, "doubles 3 times:", 550, t, 8.55, 70, WHITE)
        d.text((W / 2, 700), f"₹{count(1, 7.99, t, 8.7, 9.6):.2f} lakh", font=F("k", 140), fill=GOLD, anchor="mm")
        if t > 9.6: sparkles(im, W / 2, 700, t, 9.6, 7, 16, 330, GOLD)
        pill(im, W / 2, 870, "1 → 2 → 4 → 8", t, 9.7, WHITE, INK, 56)
        small(im, "8% a year, compounded yearly · before tax", 960, (255, 200, 230), 34)
        rocket(im, 820, 1290, 0.55, t)
        souq(im, 360, 1330, 0.6, t, "cool"); speech(im, 440, 1130, "Time does the work", 9.9, t, 40)
        return punch(im, t, 9.6, 0.06)
    return end(t, 11.0, "Free compound|interest calculator", "night", 47)

# ---------------- 5. Position size: how many lots? ----------------
def lots_screen(d, sb, t):
    x0, y0, x1, y1 = sb; cx = (x0 + x1) / 2; s = (x1 - x0) / 376
    d.text((cx, y0 + 90 * s), "Position size", font=F("k", 34 * s), fill=INK, anchor="mm")
    for i, (a, b) in enumerate([("Balance", "$10,000"), ("Risk", "1%"), ("Stop loss", "25 pips"), ("Pair", "EUR/USD")]):
        y = y0 + 170 * s + i * 88 * s
        d.rounded_rectangle([x0 + 24 * s, y - 34 * s, x1 - 24 * s, y + 34 * s], int(16 * s), fill=WHITE, outline=(215, 218, 222), width=2)
        d.text((x0 + 44 * s, y), a, font=F("s", 24 * s), fill=(90, 95, 105), anchor="lm"); d.text((x1 - 44 * s, y), b, font=F("b", 26 * s), fill=INK, anchor="rm")
    y = y0 + 560 * s
    d.rounded_rectangle([x0 + 24 * s, y - 60 * s, x1 - 24 * s, y + 60 * s], int(20 * s), fill=INK)
    d.text((cx, y), f"{count(0, 0.40, t, 4.4, 5.4):.2f} lots", font=F("k", 46 * s), fill=GOLD, anchor="mm")

def lots(t):
    if t < 3.4:
        im = scene_bg(t, "sky", 51); d = ImageDraw.Draw(im)
        kinetic(im, "$10,000 account.", 420, t, -1.2, 100, WHITE)
        kinetic(im, "Risk 1%. How many lots?", 530, t, -1.0, 72, GOLD)
        small(im, "EUR/USD · 25-pip stop loss", 605, WHITE, 40)
        options(im, t, 1.0, ["A  0.04 lots", "B  0.40 lots", "C  4.00 lots"], 750)
        chart_up(d, 130, 1450, 420, 300, 1.0, WHITE)
        souq(im, 760, 1300, 0.6, t, "thinking"); speech(im, 800, 1170, "Guess first!", 1.8, t, 42)
        return punch(im, t, 0.0)
    if t < 8.4:
        im = scene_bg(t, "night", 53); d = ImageDraw.Draw(im)
        kinetic(im, "Risk $100 ÷ (25 pips × $10)", 340, t, 3.4, 60, WHITE)
        phone(im, 330, 950, 0.95, lambda dd, sb, tt: lots_screen(dd, sb, t), t)
        pill(im, 800, 700, "0.40 lots", t, 5.5, GOLD, INK, 56)
        pill(im, 770, 860, "1 lot? −$250 (2.5%)", t, 6.4, RED, WHITE, 40, 34)
        souq(im, 800, 1240, 0.5, t, "shocked" if t > 6.4 else "thinking")
        return shake(im, t, 6.4, 14)
    if t < 11.0:
        im = scene_bg(t, "mint", 55); rays(im, W / 2, 640, t, MINT, 26); d = ImageDraw.Draw(im)
        kinetic(im, "10 losses in a row:", 440, t, 8.4, 80, WHITE)
        row(im, 600, "Risk 1% a trade", f"${count(10000, 9044, t, 8.7, 9.4):,.0f}", t, 8.5, vcol=MINT, box=(20, 50, 44))
        row(im, 750, "Risk 5% a trade", f"${count(10000, 5987, t, 9.3, 10.0):,.0f}", t, 9.1, vcol=(255, 170, 170), box=(20, 50, 44))
        if t > 10.0: sparkles(im, 820, 1250, t, 10.0, 8, 14, 260, GOLD)
        small(im, "Each loss = that % of the current balance", 860, WHITE, 34)
        souq(im, 360, 1330, 0.6, t, "wink" if t > 10 else "shocked"); speech(im, 460, 1130, "Size first, trade later", 9.9, t, 40)
        trophy(d, 820, 1330, 0.7)
        return punch(im, t, 10.0, 0.06)
    return end(t, 11.0, "Free position|size calculator", "sky", 57)

REELS = dict(days=days, fdsip=fdsip, grat=grat, double=double, lots=lots)

if __name__ == "__main__":
    name = sys.argv[1]; fn = REELS[name]
    if len(sys.argv) > 2:
        for s in map(float, sys.argv[2].split(",")): fn(s / SLOW).convert("RGB").save(f"/tmp/{name}-{s}.png")
    else:
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                              "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", f"/tmp/{name}.tmp.mp4"], stdin=subprocess.PIPE)
        for i in range(int(BASE * SLOW * FPS)): p.stdin.write(fn(i / FPS / SLOW).convert("RGB").tobytes())
        p.stdin.close(); assert p.wait() == 0; os.replace(f"/tmp/{name}.tmp.mp4", f"/tmp/{name}_v.mp4")
