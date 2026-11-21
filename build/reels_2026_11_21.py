"""CalcSouq reels for 2026-11-21 (gold, SIP 25 vs 30, life in numbers, Dubai property, return-home planner).
Every figure comes from the site's own formulas (see comments). Usage:
  python3 build/reels_2026_11_21.py <reel> [t1,t2,...]   -> stills  (reel = gold|sip|life|dubai|home)
  python3 build/reels_2026_11_21.py <reel>               -> <reel>_v.mp4 (silent)
"""
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_fx import *

def INR(x):
    s = str(int(round(x)))
    if len(s) <= 3: return "₹" + s
    head, tail = s[:-3], s[-3:]; parts = []
    while len(head) > 2: parts.insert(0, head[-2:]); head = head[:-2]
    if head: parts.insert(0, head)
    return "₹" + ",".join(parts) + "," + tail
def AED(x): return f"AED {int(round(x)):,}"
def small(img, text, y, col=WHITE, size=36):
    ImageDraw.Draw(img).text((W / 2, y), text, font=F("s", size), fill=col, anchor="mm")

def options(img, t, t0, opts, y0=1000, gap=118, win=None, t_win=99):
    for i, o in enumerate(opts):
        bg, fg = WHITE, INK
        if win is not None and t >= t_win: bg, fg = (GREEN, WHITE) if i == win else ((210, 210, 214), (120, 120, 126))
        pill(img, W / 2, y0 + i * gap, o, t, t0 + i * 0.15, bg, fg, 50, 50)

def row(img, y, label, value, t, t0, col=WHITE, vcol=GOLD, box=(30, 30, 40)):
    p = back(seg(t, t0, t0 + 0.35))
    if p <= 0: return
    x0 = 90 + (1 - p) * -300; d = ImageDraw.Draw(img)
    shadow(img, (x0, y - 62, x0 + 900, y + 62), 34, 14, 60, (0, 8)); d = ImageDraw.Draw(img)
    d.rounded_rectangle([x0, y - 62, x0 + 900, y + 62], 34, fill=box)
    d.text((x0 + 44, y), label, font=F("b", 44), fill=col, anchor="lm")
    d.text((x0 + 860, y), value, font=F("k", 52), fill=vcol, anchor="rm")

def end(t, t0, title, theme, seed):
    im = scene_bg(t, theme, seed); d = ImageDraw.Draw(im); u = t - t0
    l1, l2 = title.split("|")
    kinetic(im, l1, 640, t, t0, 84, WHITE); kinetic(im, l2, 750, t, t0 + 0.15, 84, GOLD)
    p = ease(seg(u, .3, .7)); d.text((W / 2, 850 + 20 * (1 - p)), "Free · no sign-up · private", font=F("s", 44), fill=WHITE, anchor="mm")
    pill(im, W / 2, 1000, "calcsouq.com", t, t0 + .45, GOLD, INK, 64, 70)
    if u > 0.9: d.text((W / 2, 1130), "Link in bio ↗", font=F("b", 46), fill=WHITE, anchor="mm")
    souq(im, W / 2, 1420, 0.6, t, "happy", wave=True)
    confetti(im, t, t0 + 0.05, seed, 70); return im

# ---------------- 1. Gold: the hidden cost (India, tools_uae.py gold formula) ----------------
# gold 100000, making 12% = 12000, GST 3% on (gold + making) = 3360, total 115360; at 20% making: 123600
def gold(t):
    if t < 3.4:
        im = scene_bg(t, "gold", 3); d = ImageDraw.Draw(im)
        kinetic(im, "₹1 lakh of gold.", 420, t, -0.4, 116, INK)
        kinetic(im, "What's the bill?", 545, t, -0.3, 92, (150, 40, 40))
        gold_bar(d, 250, 760, 1.0); gold_bar(d, 830, 760, 1.0)
        options(im, t, 1.1, ["A  ₹1,03,000", "B  ₹1,08,000", "C  ₹1,15,360"], 900)
        souq(im, W / 2 + 120, 1430, 0.6, t, "thinking"); speech(im, W / 2 + 290, 1300, "Guess first!", 1.8, t, 42)
        return punch(im, t, 0.0)
    if t < 8.0:
        im = scene_bg(t, "berry", 5); d = ImageDraw.Draw(im)
        kinetic(im, "Where the money goes", 380, t, 3.4, 72, WHITE)
        small(im, "22K jewellery · making 12% · GST 3% (India)", 450, (255, 200, 230), 36)
        row(im, 600, "Gold value", INR(count(0, 100000, t, 3.7, 4.6)), t, 3.6)
        row(im, 750, "+ Making 12%", INR(12000), t, 4.9, vcol=ORANGE)
        row(im, 900, "+ GST 3% on both", INR(3360), t, 5.7, vcol=ORANGE)
        coins_stack(d, 200, 1420, int(1 + 7 * seg(t, 3.7, 6.5)), 46); coins_stack(d, 880, 1420, int(1 + 7 * seg(t, 3.7, 6.5)), 46)
        souq(im, W / 2, 1270, 0.6, t, "shocked" if t > 6.4 else "thinking")
        speech(im, W / 2 + 180, 1100, "Wait, GST on making too?", 6.4, t, 38)
        return shake(im, t, 6.4, 20)
    if t < 11.0:
        im = scene_bg(t, "night", 7); rays(im, W / 2, 640, t, GOLD, 30); d = ImageDraw.Draw(im)
        kinetic(im, "The bill", 470, t, 8.0, 84, WHITE)
        d.text((W / 2, 640), INR(count(100000, 115360, t, 8.2, 9.2)), font=F("k", 150), fill=GOLD, anchor="mm")
        sparkles(im, W / 2, 640, t, 9.2, 4, 16, 320, GOLD)
        pill(im, W / 2, 820, "₹15,360 of it is not gold", t, 9.3, RED, WHITE, 50)
        souq(im, W / 2 - 230, 1320, 0.62, t, "wink" if t > 9.8 else "shocked")
        speech(im, W / 2 + 140, 1110, "At 20% making: ₹1,23,600", 9.9, t, 36)
        return shake(im, t, 9.25, 16)
    return end(t, 11.0, "Free gold|price calculator", "mint", 9)

# ---------------- 2. SIP: start at 25 or 30? (sip-calculator formula, start-of-month, monthly compounding) ----------------
# 5000/month to age 60 at 12%: from 25 -> 3,24,76,345 (inv 21L); from 30 -> 1,76,49,569 (inv 18L); from 35 -> 94,88,175 (inv 15L)
V25, V30, V35 = 32476345, 17649569, 9488175
def cr(x): return f"₹{x / 1e7:.2f} cr" if x >= 1e7 else f"₹{x / 1e5:.0f} lakh"
def sip(t):
    if t < 3.4:
        im = scene_bg(t, "sunset", 11); d = ImageDraw.Draw(im)
        kinetic(im, "Start at 25", 430, t, -0.4, 124, WHITE)
        kinetic(im, "or at 30?", 560, t, -0.2, 124, GOLD)
        kinetic(im, "₹5,000 a month till 60", 680, t, 0.5, 60, WHITE)
        calendar(d, 260, 930, 1.0, "25"); calendar(d, 820, 930, 1.0, "30")
        d.text((W / 2, 950), "vs", font=F("k", 80), fill=WHITE, anchor="mm")
        souq(im, W / 2, 1360, 0.6, t, "thinking"); speech(im, W / 2 + 190, 1200, "Just 5 years apart...", 1.4, t, 40)
        return punch(im, t, 0.0)
    if t < 8.2:
        im = scene_bg(t, "mint", 13); d = ImageDraw.Draw(im)
        kinetic(im, "Value at 60", 360, t, 3.4, 80, WHITE)
        pill(im, W / 2, 460, "Assumes 12% a year", t, 3.6, (180, 255, 220), INK, 40)
        base, top = 1250, 620; sc = top / V25
        for i, (lab, v, t0) in enumerate((("Start 35", V35, 3.8), ("Start 30", V30, 4.8), ("Start 25", V25, 5.8))):
            p = ease(seg(t, t0, t0 + 1.0)); x = 150 + i * 290; h = v * sc * p
            col = [WHITE, (180, 255, 220), GOLD][i]
            if p > 0:
                d.rounded_rectangle([x, base - h, x + 200, base], 26, fill=col)
                d.text((x + 100, base - h - 50), cr(count(0, v, t, t0, t0 + 1.0)), font=F("k", 50), fill=WHITE, anchor="mm")
            d.text((x + 100, base + 50), lab, font=F("b", 42), fill=WHITE, anchor="mm")
        souq(im, 900, 1450, 0.42, t, "shocked" if t > 6.8 else "thinking")
        return shake(im, t, 6.8, 18)
    if t < 11.2:
        im = scene_bg(t, "night", 15); rays(im, W / 2, 640, t, GOLD, 30); d = ImageDraw.Draw(im)
        kinetic(im, "Waiting 5 years costs", 480, t, 8.2, 76, WHITE)
        d.text((W / 2, 640), cr(count(0, V25 - V30, t, 8.4, 9.4)), font=F("k", 150), fill=GOLD, anchor="mm")
        sparkles(im, W / 2, 640, t, 9.4, 6, 16, 320, GOLD)
        pill(im, W / 2, 820, "for only ₹3 lakh less invested", t, 9.5, GREEN, WHITE, 46)
        rocket(im, 830, 1260, 0.7, t)
        souq(im, 330, 1330, 0.6, t, "cool" if t > 9.9 else "shocked")
        speech(im, 400, 1110, "Start small, start early", 9.9, t, 38)
        return im
    return end(t, 11.2, "Free step-up|SIP calculator", "sunset", 17)

# ---------------- 3. Your life in numbers (age & date calculators) ----------------
# born 21 Nov 1996, today 21 Nov 2026: 10,957 days, 262,968 hours, 1,565 weekends; Mon-Fri to 21 Nov 2056: 7,826
def life(t):
    if t < 3.2:
        im = scene_bg(t, "sky", 21); d = ImageDraw.Draw(im)
        kinetic(im, "You're 30?", 440, t, -0.4, 140, WHITE)
        kinetic(im, "You've lived", 570, t, -0.6, 72, WHITE)
        d.text((W / 2, 710), "10,957 days", font=F("k", 128), fill=GOLD, anchor="mm")
        calendar(d, 250, 1000, 0.9, "30")
        souq(im, 720, 1260, 0.6, t, "happy" if t < 1.5 else "shocked"); speech(im, 760, 1030, "That many?!", 1.5, t, 42)
        return punch(im, t, 0.0)
    if t < 6.6:
        im = scene_bg(t, "berry", 23)
        kinetic(im, "Your life in numbers", 380, t, 3.2, 78, WHITE)
        row(im, 560, "Hours lived", f"{int(count(0, 262968, t, 3.5, 4.4)):,}", t, 3.4)
        row(im, 710, "Weekends", f"{int(count(0, 1565, t, 4.1, 4.9)):,}", t, 4.0, vcol=PINK)
        row(im, 860, "Weekdays", f"{int(count(0, 7827, t, 4.7, 5.5)):,}", t, 4.6, vcol=(140, 255, 200))
        souq(im, W / 2, 1260, 0.6, t, "cool")
        return im
    if t < 11.0:
        im = scene_bg(t, "night", 25); d = ImageDraw.Draw(im)
        if t > 9.0: rays(im, W / 2, 1050, t, GOLD, 26)
        kinetic(im, "Weekdays left", 400, t, 6.6, 92, WHITE); kinetic(im, "until 60?", 525, t, 6.8, 92, GOLD)
        options(im, t, 7.0, ["A  5,200", "B  7,826", "C  11,000"], 680, 120, win=1, t_win=9.0)
        pill(im, W / 2, 1060, "Mon to Fri, before holidays and leave", t, 9.2, GOLD, INK, 38)
        sparkles(im, W / 2, 800, t, 9.0, 8, 16, 300, GOLD)
        souq(im, W / 2, 1360, 0.55, t, "thinking" if t < 9.0 else "wink")
        speech(im, W / 2 + 200, 1190, "Make them count", 9.6, t, 40)
        return punch(im, t, 9.0, 0.05)
    return end(t, 11.0, "Free|age calculator", "sky", 27)

# ---------------- 4. Dubai property: cash on top (property-buying-cost-calculator, AE preset) ----------------
# price 1,500,000: DLD 4% 60,000; agent 2.1% (2% + 5% VAT) 31,500; trustee 4,000 + VAT 4,200; admin & title deed 580 -> 96,280 (6.4%)
def dubai(t):
    if t < 3.4:
        im = scene_bg(t, "night", 31); d = ImageDraw.Draw(im)
        kinetic(im, "AED 1.5M flat.", 420, t, -0.4, 118, WHITE)
        kinetic(im, "How much cash ON TOP?", 535, t, -0.3, 70, GOLD, hl=["ON", "TOP?"], hl_col=RED)
        options(im, t, 1.0, ["A  AED 15,000", "B  AED 45,000", "C  AED 96,280"], 700)
        doc(d, 230, 1330, 0.75, "DEED", BLUE)
        souq(im, 720, 1340, 0.6, t, "thinking"); speech(im, 700, 1215, "Price is the price?", 1.7, t, 40)
        return punch(im, t, 0.0)
    if t < 8.0:
        im = scene_bg(t, "sky", 33); d = ImageDraw.Draw(im)
        kinetic(im, "The costs nobody lists", 360, t, 3.4, 70, WHITE)
        row(im, 520, "DLD transfer 4%", AED(count(0, 60000, t, 3.7, 4.4)), t, 3.6)
        row(im, 670, "Agent 2% + VAT", AED(31500), t, 4.5, vcol=ORANGE)
        row(im, 820, "Trustee fee + VAT", AED(4200), t, 5.2, vcol=ORANGE)
        row(im, 970, "Admin & title deed", AED(580), t, 5.8, vcol=ORANGE)
        coins_stack(d, 180, 1460, int(1 + 7 * seg(t, 3.7, 6.5)), 44)
        souq(im, W / 2 + 80, 1330, 0.55, t, "shocked" if t > 6.4 else "thinking")
        return shake(im, t, 6.4, 20)
    if t < 11.0:
        im = scene_bg(t, "sunset", 35); rays(im, W / 2, 640, t, WHITE, 30); d = ImageDraw.Draw(im)
        kinetic(im, "Cash on top", 470, t, 8.0, 84, WHITE)
        d.text((W / 2, 640), AED(count(0, 96280, t, 8.2, 9.2)), font=F("k", 124), fill=WHITE, anchor="mm")
        sparkles(im, W / 2, 640, t, 9.2, 4, 16, 320, GOLD)
        pill(im, W / 2, 810, "6.4% more than the price", t, 9.3, INK, GOLD, 50)
        small(im, "Cash buyer · before mortgage fees", 900, WHITE, 36)
        souq(im, W / 2 - 220, 1330, 0.6, t, "cool" if t > 9.8 else "shocked")
        speech(im, W / 2 + 160, 1110, "Budget it before you sign", 9.9, t, 38)
        return shake(im, t, 9.25, 14)
    return end(t, 11.0, "Free property|cost calculator", "night", 37)

# ---------------- 5. How long to ₹1 crore? (gulf-savings-return-planner formula) ----------------
# AED 3,000/month at ₹24, start from 0: plain saving 139 months (11y 7m); + 7% growth 103 months (8y 7m);
# + 3% yearly raise + gratuity on AED 8,000 basic (new job) 88 months (7y 4m)
def home(t):
    if t < 3.4:
        im = scene_bg(t, "mint", 41); d = ImageDraw.Draw(im)
        kinetic(im, "AED 3,000 a month.", 420, t, -0.4, 94, WHITE)
        kinetic(im, "How long to ₹1 crore?", 540, t, -0.3, 80, GOLD)
        options(im, t, 1.0, ["A  5 years", "B  7 years", "C  11 years"], 700)
        piggy(im, 260, 1340, 0.75, t)
        souq(im, 760, 1340, 0.58, t, "thinking"); speech(im, 760, 1215, "Guess first!", 1.7, t, 42)
        return punch(im, t, 0.0)
    if t < 8.4:
        im = scene_bg(t, "sky", 43); d = ImageDraw.Draw(im)
        kinetic(im, "Same AED 3,000 a month", 360, t, 3.4, 70, WHITE)
        small(im, "₹24 per AED · starting from zero", 430, WHITE, 36)
        row(im, 580, "Just saving", "11 yrs 7 mo", t, 3.7, vcol=(255, 170, 170))
        row(im, 730, "+ 7% growth", "8 yrs 7 mo", t, 4.8)
        row(im, 880, "+ 3% raises, gratuity", "7 yrs 4 mo", t, 5.9, vcol=(140, 255, 200))
        calendar(d, 230, 1290, 0.8, str(int(count(11, 7, t, 4.8, 6.4))))
        souq(im, 720, 1290, 0.55, t, "happy" if t > 6.4 else "thinking")
        return im
    if t < 11.2:
        im = scene_bg(t, "night", 45); rays(im, W / 2, 640, t, (140, 255, 200), 28); d = ImageDraw.Draw(im)
        kinetic(im, "₹1 crore in", 470, t, 8.4, 84, WHITE)
        d.text((W / 2, 640), "7 yrs 4 mo", font=F("k", 150), fill=(140, 255, 200), anchor="mm")
        sparkles(im, W / 2, 640, t, 8.7, 4, 16, 320, GOLD)
        pill(im, W / 2, 820, "4 years sooner than just saving", t, 9.2, GOLD, INK, 46)
        small(im, "7% return · 3% raises · AED 8,000 basic", 910, WHITE, 34)
        piggy(im, 800, 1300, 0.6, t)
        souq(im, 330, 1330, 0.6, t, "wink"); speech(im, 420, 1120, "Growth does the work", 9.6, t, 38)
        return punch(im, t, 8.5, 0.06)
    return end(t, 11.2, "Free savings|goal planner", "mint", 47)

REELS = dict(gold=(gold, 13.5), sip=(sip, 13.5), life=(life, 13.5), dubai=(dubai, 13.5), home=(home, 13.5))

if __name__ == "__main__":
    name = sys.argv[1]; fn, dur = REELS[name]
    if len(sys.argv) > 2:
        for s in map(float, sys.argv[2].split(",")): fn(s).save(f"{name}-{s}.png")
    else:
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                              "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", f"{name}.tmp.mp4"], stdin=subprocess.PIPE)
        for i in range(int(dur * FPS)): p.stdin.write(fn(i / FPS).tobytes())
        p.stdin.close(); assert p.wait() == 0; os.replace(f"{name}.tmp.mp4", f"{name}_v.mp4")
