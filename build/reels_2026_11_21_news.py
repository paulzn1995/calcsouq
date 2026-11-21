"""CalcSouq news reels for 2026-11-21 (rupee at 93, RBI repo hike -> EMI vs tenure).
Sources (checked 21 Nov 2026):
  rupee: touched 92.995/USD on 20 Nov 2026, first time past 93 since April (5paisa / Reuters via The United Indian);
         2026 record low 96.96 in late May (LKP Securities via 5paisa). AED peg 3.6725 per USD.
  repo:  RBI MPC 7 Oct 2026 raised repo 5.25% -> 5.50% (SCC Online 9 Oct, CAclubindia 10 Oct).
Usage:
  python3 build/reels_2026_11_21_news.py <rupee|emi> [t1,t2,...]   -> stills
  python3 build/reels_2026_11_21_news.py <rupee|emi>               -> <name>_v.mp4 (silent)
"""
import sys, os, math, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reels_2026_11_21 import *  # reel_fx + INR, small, options, row, end

PEG = 3.6725
LOW, NOW, SEND = 96.96, 93.00, 5000
R_LOW = SEND * LOW / PEG      # 1,32,008
R_NOW = SEND * NOW / PEG      # 1,26,617
GAP = R_LOW - R_NOW           # 5,391 per transfer
YEAR = GAP * 12               # 64,697 a year

def emi(P, a, n): r = a / 1200; return P * r * (1 + r) ** n / ((1 + r) ** n - 1)
P, N = 5_000_000, 240
E1, E2 = emi(P, 8.0, N), emi(P, 8.25, N)                       # 41,822 -> 42,603
UP = E2 - E1                                                    # +781 a month
EXTRA_EMI = UP * N                                              # ~1.88 lakh
n2 = -math.log(1 - (8.25 / 1200) * P / E1) / math.log(1 + 8.25 / 1200)   # 251.9 months
EXTRA_TEN = E1 * (n2 - N)                                       # ~4.96 lakh
MONTHS = math.ceil(n2 - N)                                      # 12
def lakh(x): return f"₹{x / 1e5:.2f} lakh"

# ---------------- 1. Rupee crosses 93: your transfer just shrank ----------------
def rupee(t):
    if t < 3.4:
        im = scene_bg(t, "night", 61); rays(im, W / 2, 560, t, GOLD, 26); d = ImageDraw.Draw(im)
        kinetic(im, "Rupee just hit", 380, t, -0.4, 96, WHITE)
        d.text((W / 2, 560), "₹93 / $", font=F("k", 190), fill=GOLD, anchor="mm")
        pill(im, W / 2, 740, "Strongest since April", t, 0.6, GREEN, WHITE, 50)
        kinetic(im, "Good news for NRIs?", 900, t, 1.2, 76, (255, 170, 170))
        souq(im, W / 2, 1360, 0.62, t, "thinking"); speech(im, W / 2 + 200, 1190, "Not if you send money home", 1.9, t, 38)
        return punch(im, t, 0.0)
    if t < 8.0:
        im = scene_bg(t, "berry", 63); d = ImageDraw.Draw(im)
        kinetic(im, "Same AED 5,000 sent home", 380, t, 3.4, 66, WHITE)
        small(im, "AED is pegged: $1 = AED 3.6725", 450, (255, 200, 230), 36)
        row(im, 600, "Late May (₹96.96)", INR(count(0, R_LOW, t, 3.7, 4.5)), t, 3.6)
        row(im, 750, "Now (₹93.00)", INR(R_NOW), t, 4.7)
        row(im, 900, "You get less", "−" + INR(GAP), t, 5.6, vcol=RED)
        coins_stack(d, 200, 1420, int(8 - 4 * seg(t, 5.6, 6.6)), 46); coins_stack(d, 880, 1420, int(8 - 4 * seg(t, 5.6, 6.6)), 46)
        souq(im, W / 2, 1270, 0.6, t, "shocked" if t > 5.9 else "thinking")
        speech(im, W / 2 + 180, 1100, "Every single transfer", 6.2, t, 38)
        return shake(im, t, 5.9, 18)
    if t < 11.0:
        im = scene_bg(t, "night", 65); rays(im, W / 2, 640, t, RED, 26); d = ImageDraw.Draw(im)
        kinetic(im, "Monthly sender? That's", 470, t, 8.0, 70, WHITE)
        d.text((W / 2, 640), INR(count(GAP, YEAR, t, 8.2, 9.2)), font=F("k", 150), fill=GOLD, anchor="mm")
        pill(im, W / 2, 820, "less a year vs the May low", t, 9.3, RED, WHITE, 48)
        small(im, "…before your exchange house's margin", 910, WHITE, 36)
        souq(im, W / 2 - 230, 1320, 0.62, t, "wink" if t > 9.8 else "shocked")
        speech(im, W / 2 + 140, 1110, "Compare rates before you send", 9.9, t, 36)
        return shake(im, t, 9.25, 14)
    return end(t, 11.0, "Compare|remittance rates", "mint", 67)

# ---------------- 2. RBI hiked: higher EMI or longer loan? ----------------
def emi_reel(t):
    if t < 3.4:
        im = scene_bg(t, "sky", 71); d = ImageDraw.Draw(im)
        kinetic(im, "RBI raised rates.", 400, t, -0.4, 100, WHITE)
        kinetic(im, "Your EMI didn't change?", 530, t, -0.2, 76, GOLD)
        pill(im, W / 2, 680, "Repo 5.25% → 5.50% · 7 Oct", t, 0.7, WHITE, INK, 46)
        kinetic(im, "Check your tenure.", 860, t, 1.3, 84, (255, 190, 190))
        calendar(d, 260, 1330, 0.8, "+?")
        souq(im, 740, 1340, 0.6, t, "thinking"); speech(im, 760, 1200, "Guess the cost!", 1.8, t, 42)
        return punch(im, t, 0.0)
    if t < 8.4:
        im = scene_bg(t, "berry", 73); d = ImageDraw.Draw(im)
        kinetic(im, "₹50 lakh · 20 years", 360, t, 3.4, 74, WHITE)
        small(im, "Loan rate 8.00% → 8.25%", 430, (255, 200, 230), 38)
        row(im, 570, "A: EMI goes up", f"+₹{UP:,.0f}/mo", t, 3.7, vcol=ORANGE)
        row(im, 700, "   total extra", lakh(EXTRA_EMI), t, 4.3)
        row(im, 860, f"B: +{MONTHS} months", "same EMI", t, 5.3, vcol=ORANGE)
        row(im, 990, "   total extra", lakh(EXTRA_TEN), t, 5.9, vcol=RED)
        souq(im, W / 2, 1340, 0.58, t, "shocked" if t > 6.3 else "thinking")
        speech(im, W / 2 + 170, 1180, "B costs way more!", 6.4, t, 40)
        return shake(im, t, 6.2, 16)
    if t < 11.2:
        im = scene_bg(t, "night", 75); rays(im, W / 2, 640, t, GOLD, 28); d = ImageDraw.Draw(im)
        kinetic(im, "Longer tenure costs", 470, t, 8.4, 78, WHITE)
        d.text((W / 2, 640), f"{EXTRA_TEN / EXTRA_EMI:.1f}× more", font=F("k", 150), fill=GOLD, anchor="mm")
        sparkles(im, W / 2, 640, t, 8.7, 4, 16, 320, GOLD)
        pill(im, W / 2, 820, "You can ask your bank to choose", t, 9.2, GREEN, WHITE, 46)
        small(im, "Higher EMI, longer tenure, or both", 910, WHITE, 36)
        souq(im, W / 2 - 230, 1320, 0.62, t, "wink")
        speech(im, W / 2 + 140, 1110, "Pick A if you can", 9.7, t, 40)
        return punch(im, t, 8.5, 0.06)
    return end(t, 11.2, "Free loan|EMI calculator", "mint", 77)

REELS = dict(rupee=(rupee, 13.5), emi=(emi_reel, 13.5))

if __name__ == "__main__":
    print(f"rupee: {R_LOW:,.0f} -> {R_NOW:,.0f}, gap {GAP:,.0f}, year {YEAR:,.0f}")
    print(f"emi: {E1:,.0f} -> {E2:,.0f} (+{UP:,.0f}); extra {EXTRA_EMI:,.0f} vs tenure +{n2 - N:.1f} mo, extra {EXTRA_TEN:,.0f}")
    name = sys.argv[1]; fn, dur = REELS[name]
    if len(sys.argv) > 2:
        for s in map(float, sys.argv[2].split(",")): fn(s).save(f"{name}-{s}.png")
    else:
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                              "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", f"{name}.tmp.mp4"], stdin=subprocess.PIPE)
        for i in range(int(dur * FPS)): p.stdin.write(fn(i / FPS).tobytes())
        p.stdin.close(); assert p.wait() == 0; os.replace(f"{name}.tmp.mp4", f"{name}_v.mp4")
