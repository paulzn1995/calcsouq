"""YouTube Shorts, 22 Nov 2026 (Malayalam, text + music, reading pace). 1080x1920.
  python3 build/yt_shorts_2026_11_22.py loan  out.mp4   # teaser for long video 'gold fall / gold loan trap'
  python3 build/yt_shorts_2026_11_22.py pavan out.mp4   # one number: 10 pavan cheaper by Rs 92,000 in a week
  python3 build/yt_shorts_2026_11_22.py --frame loan 5.0 f.png
Facts: build/youtube/long/2026-11-22-gold-fall-malayalam/sources.md (loan) and keralagold.com daily board,
goodreturns/flickonclick 22 Nov 2026 (pavan: 15 Nov Rs 1,00,920; 21-22 Nov Rs 91,720, 22K, 8 g).
"""
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_fx import *
from reel_gold_ml_teaser import ml, bar, card

# ---- numbers, computed (not typed) ----
PAV_NOW, PAV_15 = 91720, 100920      # 22K pavan on 21/22 Nov and on 15 Nov
LOAN, PV = 450000, 5
V_JAN, V_NOW = PV * 130000, PV * PAV_NOW   # long video example uses Rs 1,30,000 a pavan for January
LTV0, LTV1 = 100 * LOAN / V_JAN, 100 * LOAN / V_NOW
REPAY = LOAN - 0.80 * V_NOW
ADD_PAV = (LOAN / 0.80 - V_NOW) / PAV_NOW
N10 = 10
DROP10 = N10 * (PAV_15 - PAV_NOW)
DROP1 = PAV_15 - PAV_NOW
DROP_PCT = 100 * DROP1 / PAV_15
def inr(v):  # Indian grouping
    s = f"{int(round(v))}"; head, tail = s[:-3], s[-3:]
    while len(head) > 2: tail = head[-2:] + "," + tail; head = head[:-2]
    return "₹" + (head + "," + tail if head else tail)

GREY = (200, 200, 210)
def txt(img, s, y, size=52, col=WHITE, f="b"):
    d = ImageDraw.Draw(img); d.text((W / 2, y), s, font=F(f, size), fill=col, anchor="mm")

def endc(img, t, t0, sub):
    ml(img, "മുഴുവൻ വീഡിയോ", 360, t, t0, 104, WHITE)
    ml(img, "ചാനലിൽ", 490, t, t0 + .3, 112, GOLD)
    if t > t0 + .6: txt(img, "Full video on our channel", 610, 54)
    if t > t0 + .6: txt(img, sub, 685, 42, GREY)
    bar(img, W / 2, 900, 1.2 * back(seg(t, t0 + .2, t0 + .8)))
    pill(img, W / 2, 1120, "Subscribe · @calcsouq", t, t0 + 1.0, (230, 33, 23), WHITE, 56, 50)
    if t > t0 + 1.2: txt(img, "calcsouq.com · free calculators", 1250, 42)

# ---------------- Short 1: gold loan teaser ----------------
LOAN_DUR = 24.8
LOAN_CUES = "0:boom,1.6:whoosh,4.6:swoosh,5.2:pop,7.2:pop,10.6:riser,11.4:tick*10,13.4:fail,16.6:whoosh,17.2:coin*4,20.8:success"
def loan(t):
    img = scene_bg(t, "night", 41)
    if t < 4.6:
        ml(img, "സ്വർണ്ണം പണയം", 330, t, 0.1, 104, WHITE)
        ml(img, "വെച്ചവർ കുടുങ്ങിയോ?", 470, t, 0.5, 96, GOLD)
        if t > 1.6: txt(img, "Gold loan: are you stuck?", 600, 56)
        for k in range(3): bar(img, W / 2 + (k - 1) * 330, 1050 + (k % 2) * 90, 0.95 * back(seg(t, .4 + k * .2, 1.0 + k * .2)))
    elif t < 10.6:
        ml(img, "5 പവൻ, ₹4.5 ലക്ഷം ലോൺ", 330, t, 4.6, 70, WHITE)
        if t > 4.9: txt(img, "5 pavan pledged · ₹4.5 lakh loan", 440, 50, GOLD)
        card(img, 680, f"January value: {inr(V_JAN)}", 1, t, 5.2)
        card(img, 880, f"Today: {inr(V_NOW)}", 2, t, 7.2)
        if t > 7.6: txt(img, f"22K pavan {inr(PAV_NOW)} · 21 Nov 2026", 1040, 40, GREY)
    elif t < 16.6:
        ml(img, "ലോൺ അതേ, സ്വർണ്ണം കുറഞ്ഞു", 330, t, 10.6, 64, GOLD)
        if t > 10.9: txt(img, "Same loan, cheaper gold", 440, 54)
        p = back(seg(t, 11.0, 11.5))
        if p > 0:
            box = (140, 560, 940, 960); shadow(img, box, 40, 18, 90, (0, 10)); d = ImageDraw.Draw(img); d.rounded_rectangle(box, 40, fill=WHITE)
            d.text((540, 640), "Loan-to-value (LTV)", font=F("b", 44), fill=(100, 105, 115), anchor="mm")
            v = count(LTV0, LTV1, t, 11.4, 13.4); col = GREEN if v <= 80 else RED
            d.text((540, 790), f"{v:.0f}%", font=F("k", 170), fill=col, anchor="mm")
            d.text((540, 910), "loan ÷ gold value", font=F("b", 40), fill=(100, 105, 115), anchor="mm")
        if t > 13.4: shake(img, t, 13.4, 12, 0.4)
        if t > 13.4: pill(img, W / 2, 1100, "RBI cap for this loan size: 80%", t, 13.4, RED, WHITE, 48, 44)
    elif t < 20.8:
        ml(img, "ബാങ്ക് മാർജിൻ ചോദിക്കാം", 330, t, 16.6, 72, WHITE)
        if t > 16.9: txt(img, "The bank may ask for margin", 440, 52, GOLD)
        card(img, 660, f"Repay {inr(REPAY)}", 1, t, 17.2)
        card(img, 860, f"or add ~{ADD_PAV:.2f} pavan", 2, t, 17.2)
        if t > 17.6: txt(img, "to get back to 80% · example only", 1010, 40, GREY)
    else:
        endc(img, t, 20.8, "Gold loan trap explained · Malayalam")
    return img

# ---------------- Short 2: one number ----------------
PAV_DUR = 25.0
PAV_CUES = "0:hit,1.2:whoosh,4.4:riser,5.2:tick*12,7.0:cash,10.0:swoosh,10.5:pop,12.0:pop,13.5:ding,16.5:whoosh,21.0:sparkle"
def pavan(t):
    img = scene_bg(t, "night", 52)
    if t < 4.5:
        ml(img, "10 പവൻ സ്വർണ്ണം", 330, t, 0.1, 104, WHITE)
        ml(img, "ഇപ്പോൾ എത്ര കുറവ്?", 470, t, 0.5, 100, GOLD)
        if t > 1.2: txt(img, "Buying 10 pavan? How much cheaper now?", 600, 46)
        for k in range(5): bar(img, W / 2 + (k - 2) * 200, 1000 + (k % 2) * 80, 0.6 * back(seg(t, .3 + k * .15, .9 + k * .15)))
    elif t < 10.0:
        ml(img, "ഒരാഴ്ച കൊണ്ട്", 360, t, 4.5, 100, WHITE)
        if t > 4.8: txt(img, "In one week (15 → 22 Nov)", 470, 52, GOLD)
        v = count(0, DROP10, t, 5.2, 7.0)
        if t > 5.2: txt(img, f"−{inr(v)}", 700, 170, GREEN, "k")
        if t > 7.0: punch(img, t, 7.0)
        if t > 7.0: pill(img, W / 2, 900, "10 pavan · 22K · gold value only", t, 7.0, WHITE, INK, 46, 40)
    elif t < 16.5:
        ml(img, "ഒരു പവന്", 330, t, 10.0, 104, GOLD)
        if t > 10.2: txt(img, "Per pavan (8 g, 22K), Kerala", 440, 50)
        card(img, 640, f"15 Nov: {inr(PAV_15)}", 1, t, 10.5)
        card(img, 840, f"22 Nov: {inr(PAV_NOW)}", 2, t, 12.0)
        if t > 13.5: pill(img, W / 2, 1040, f"−{inr(DROP1)} a pavan (−{DROP_PCT:.1f}%)", t, 13.5, GREEN, WHITE, 52, 46)
    elif t < 21.0:
        ml(img, "നാളത്തെ വില?", 340, t, 16.5, 110, WHITE)
        if t > 16.8: txt(img, "Tomorrow's price? No one knows.", 460, 52, GOLD)
        pill(img, W / 2, 640, "GST + making charges are extra", t, 17.2, WHITE, INK, 46, 40)
        pill(img, W / 2, 780, "Check the day's rate before you pay", t, 17.2, GOLD, INK, 46, 40)
        if t > 17.8: txt(img, "Gold price calculator: calcsouq.com", 920, 44, GREY)
    else:
        endc(img, t, 21.0, "Why gold is falling · Malayalam")
    return img

SH = {"loan": (loan, LOAN_DUR, LOAN_CUES), "pavan": (pavan, PAV_DUR, PAV_CUES)}
if __name__ == "__main__":
    if sys.argv[1] == "--frame":
        SH[sys.argv[2]][0](float(sys.argv[3])).convert("RGB").save(sys.argv[4]); sys.exit()
    if sys.argv[1] == "--facts":
        print(dict(V_JAN=V_JAN, V_NOW=V_NOW, LTV0=LTV0, LTV1=LTV1, REPAY=REPAY, ADD_PAV=ADD_PAV, DROP10=DROP10, DROP1=DROP1, DROP_PCT=DROP_PCT)); sys.exit()
    fn, dur, _ = SH[sys.argv[1]]; out = sys.argv[2]; tmp = out + ".tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for i in range(int(dur * FPS)): p.stdin.write(fn(i / FPS).convert("RGB").tobytes())
    p.stdin.close(); assert p.wait() == 0; os.replace(tmp, out); print(out)
