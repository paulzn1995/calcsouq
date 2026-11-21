"""CalcSouq international news reels for 2026-11-21 (bitcoin half off its high, gold 37% off its record).
Sources (checked 21 Nov 2026):
  bitcoin: $61,321.59 at 7:15 a.m. ET 20 Nov 2026; all-time high $126,198.07 on 6 Oct 2025; $86,569.90 a year ago (Fortune, 20 Nov 2026).
  gold:    record about $5,590/oz on 28 Jan 2026; $3,533/oz on 21 Nov 2026 (MetalCharts). AED peg 3.6725, 31.1035 g per troy oz.
Usage:
  python3 build/reels_2026_11_21_world.py <btc|gold> [t1,t2,...]   -> stills
  python3 build/reels_2026_11_21_world.py <btc|gold>               -> <name>_v.mp4 (silent)
"""
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reels_2026_11_21 import *  # reel_fx + INR, AED, small, options, row, end

BTC_ATH, BTC_NOW = 126198.07, 61321.59
BTC_DROP = 1 - BTC_NOW / BTC_ATH           # 51.4%
BTC_NEED = BTC_ATH / BTC_NOW - 1           # +105.8%
BTC_10K = 10000 * BTC_NOW / BTC_ATH        # $4,859

PEG, OZ = 3.6725, 31.1035
G_ATH, G_NOW = 5590, 3533
G_DROP = 1 - G_NOW / G_ATH                 # 36.8%
G_NEED = G_ATH / G_NOW - 1                 # +58.2%
G100_ATH = 100 / OZ * G_ATH * PEG          # AED 66,003
G100_NOW = 100 / OZ * G_NOW * PEG          # AED 41,715
def USD(x): return f"${x:,.0f}"
def pc(x): return f"{x * 100:.0f}%"

# ---------------- 1. Bitcoin: down 51%, needs +106% ----------------
def btc(t):
    if t < 3.4:
        im = scene_bg(t, "night", 81); rays(im, W / 2, 560, t, RED, 26); d = ImageDraw.Draw(im)
        kinetic(im, "Bitcoin is down", 380, t, -0.4, 100, WHITE)
        d.text((W / 2, 570), "−" + pc(BTC_DROP), font=F("k", 210), fill=RED, anchor="mm")
        pill(im, W / 2, 760, "from its $126,198 peak", t, 0.6, WHITE, INK, 48)
        kinetic(im, "How much to get back?", 920, t, 1.2, 76, GOLD)
        souq(im, W / 2, 1370, 0.62, t, "thinking"); speech(im, W / 2 + 200, 1200, "+51%? Guess again", 1.9, t, 40)
        return punch(im, t, 0.0)
    if t < 8.0:
        im = scene_bg(t, "berry", 83); d = ImageDraw.Draw(im)
        kinetic(im, "$10,000 bought at the top", 380, t, 3.4, 64, WHITE)
        small(im, "Peak 6 Oct 2025 → 20 Nov 2026", 450, (255, 200, 230), 36)
        row(im, 600, "At the peak", USD(10000), t, 3.6)
        row(im, 750, "Today", USD(count(10000, BTC_10K, t, 4.8, 5.6)), t, 4.7, vcol=RED)
        row(im, 900, "To break even", "+" + pc(BTC_NEED), t, 5.9, vcol=(140, 255, 200))
        chart_up(d, 140, 1460, 260, 220, 1 - seg(t, 4.8, 5.8), RED)
        souq(im, 700, 1300, 0.58, t, "shocked" if t > 6.0 else "thinking")
        speech(im, 760, 1130, "It has to DOUBLE", 6.2, t, 42)
        return shake(im, t, 5.9, 18)
    if t < 11.0:
        im = scene_bg(t, "night", 85); rays(im, W / 2, 640, t, GOLD, 26); d = ImageDraw.Draw(im)
        kinetic(im, "The loss math rule", 460, t, 8.0, 76, WHITE)
        d.text((W / 2, 610), "−50% needs +100%", font=F("k", 92), fill=GOLD, anchor="mm")
        pill(im, W / 2, 760, "−20% needs +25% · −33% needs +50%", t, 8.8, WHITE, INK, 42)
        small(im, "Losses hurt more than gains help", 860, WHITE, 38)
        souq(im, W / 2 - 230, 1320, 0.62, t, "wink" if t > 9.6 else "shocked")
        speech(im, W / 2 + 140, 1110, "Size your risk first", 9.7, t, 40)
        return punch(im, t, 8.1, 0.06)
    return end(t, 11.0, "Free percentage|change calculator", "mint", 87)

# ---------------- 2. Gold: 37% off January's record ----------------
def gold_w(t):
    if t < 3.4:
        im = scene_bg(t, "gold", 91); d = ImageDraw.Draw(im)
        kinetic(im, "Gold hit $5,590", 400, t, -0.4, 104, INK)
        kinetic(im, "in January.", 520, t, -0.2, 90, INK)
        kinetic(im, "Now?", 680, t, 0.9, 130, (150, 40, 40))
        gold_bar(d, 250, 880, 1.0); gold_bar(d, 830, 880, 1.0)
        souq(im, W / 2 + 120, 1420, 0.6, t, "thinking"); speech(im, W / 2 + 290, 1290, "Guess first!", 1.6, t, 42)
        return punch(im, t, 0.0)
    if t < 8.0:
        im = scene_bg(t, "night", 93); d = ImageDraw.Draw(im)
        kinetic(im, "100 g of gold (spot value)", 380, t, 3.4, 64, WHITE)
        small(im, "Record 28 Jan 2026 vs 21 Nov 2026", 450, GOLD, 36)
        row(im, 600, "January peak", AED(G100_ATH), t, 3.6)
        row(im, 750, "Today ($3,533/oz)", AED(count(G100_ATH, G100_NOW, t, 4.8, 5.6)), t, 4.7, vcol=RED)
        row(im, 900, "Down", "−" + pc(G_DROP), t, 5.9, vcol=RED)
        coins_stack(d, 200, 1430, int(8 - 4 * seg(t, 4.8, 5.8)), 46); coins_stack(d, 880, 1430, int(8 - 4 * seg(t, 4.8, 5.8)), 46)
        souq(im, W / 2, 1280, 0.6, t, "shocked" if t > 6.0 else "thinking")
        speech(im, W / 2 + 180, 1110, "That's AED 24,000 gone", 6.2, t, 38)
        return shake(im, t, 5.9, 18)
    if t < 11.0:
        im = scene_bg(t, "berry", 95); rays(im, W / 2, 640, t, GOLD, 26); d = ImageDraw.Draw(im)
        kinetic(im, "To get back to the record", 460, t, 8.0, 66, WHITE)
        d.text((W / 2, 630), "+" + pc(G_NEED), font=F("k", 170), fill=GOLD, anchor="mm")
        pill(im, W / 2, 800, "Jewellery? Making charges don't come back", t, 9.0, WHITE, INK, 36)
        small(im, "Coins and bars resell closest to spot", 890, WHITE, 36)
        souq(im, W / 2 - 230, 1320, 0.62, t, "wink" if t > 9.6 else "shocked")
        speech(im, W / 2 + 140, 1110, "Check the real price", 9.7, t, 40)
        return punch(im, t, 8.1, 0.06)
    return end(t, 11.0, "Free gold|price calculator", "mint", 97)

REELS = dict(btc=(btc, 13.5), gold=(gold_w, 13.5))

if __name__ == "__main__":
    print(f"btc: -{BTC_DROP:.1%}, need +{BTC_NEED:.1%}, $10k -> {BTC_10K:,.0f}")
    print(f"gold: -{G_DROP:.1%}, need +{G_NEED:.1%}, 100 g AED {G100_ATH:,.0f} -> {G100_NOW:,.0f}")
    name = sys.argv[1]; fn, dur = REELS[name]
    if len(sys.argv) > 2:
        for s in map(float, sys.argv[2].split(",")): fn(s).save(f"{name}-{s}.png")
    else:
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                              "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", f"{name}.tmp.mp4"], stdin=subprocess.PIPE)
        for i in range(int(dur * FPS)): p.stdin.write(fn(i / FPS).tobytes())
        p.stdin.close(); assert p.wait() == 0; os.replace(f"{name}.tmp.mp4", f"{name}_v.mp4")
