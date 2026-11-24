"""YouTube Shorts, 24 Nov 2026: top world money news (Malayalam + English, text + music, no narration).
1080x1920, 25.5 s, reading pace (every line ≥3 s, at most 2 new items at once, end card 4 s).
Render:  python3 build/yt_shorts_2026_11_24.py <n> out_silent.mp4      (n = 1, 2, 3)
Frame:   python3 build/yt_shorts_2026_11_24.py <n> --frame <t> out.png
Helpers (ml, en, big, card, panel, chart, gold_bar3d, coin3d, end_card) come from build/yt_shorts_2026_11_23.py.
Facts (checked 24 Nov 2026, two sources each) are in build/youtube/2026-11-24-pack.md.
"""
import sys, os, subprocess, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_fx import *
from yt_shorts_2026_11_23 import ml, en, big, card, panel, chart, gold_bar3d, coin3d, end_card, GREY
from reel_hormuz_ml_teaser import barrel

DUR = 25.5
END = 21.5
LGREEN = (90, 220, 130)

def inr(v):
    """Indian digit grouping: 100886 -> 1,00,886."""
    s = f"{int(round(v))}"
    if len(s) <= 3: return s
    head, tail = s[:-3], s[-3:]
    parts = []
    while len(head) > 2: parts.insert(0, head[-2:]); head = head[:-2]
    if head: parts.insert(0, head)
    return ",".join(parts + [tail])

def src(img, txt, t):
    if t >= END: return
    d = ImageDraw.Draw(img); size = 34; f = F("s", size)
    while d.textlength(txt, font=f) > W - 80: size -= 1; f = F("s", size)
    d.text((W / 2, 1600), txt, font=f, fill=(170, 172, 185), anchor="mm")

def money_panel(img, t, label, v0, v1, reveal, rcol, fmt=lambda v: "₹" + inr(v)):
    """Beat 3: white panel with a count-up and a reveal line (reveal at 14.0, holds 3 s)."""
    if panel(img, (140, 580, 940, 1040), t, 12.6):
        d = ImageDraw.Draw(img)
        v = count(v0, v1, t, 12.8, 14.0)
        d.text((540, 680), label, font=F("b", 48), fill=(90, 95, 105), anchor="mm")
        d.text((540, 820), fmt(v), font=F("k", 140), fill=INK, anchor="mm")
        if t > 14.0: d.text((540, 960), reveal, font=F("k", 58), fill=rcol, anchor="mm")

# ---------------- Short 1: Nvidia +31.5% in one day ----------------
S1_CUES = "0:boom,0.2:tick*10,2.4:success,6.0:whoosh,6.6:pop,8.2:pop,12.0:swoosh,12.8:tick*8,14.0:cash,17.0:whoosh,17.4:pop,17.8:pop,21.5:success"
def short1(t):
    img = scene_bg(t, "berry", 81)
    if t < 6.0:
        ml(img, "ഒറ്റ ദിവസം കൊണ്ട്", 250, t, -1, 100, WHITE)
        ml(img, "ഇത്ര കയറുമോ?", 380, t, -1, 116, GOLD)
        v = count(0, 31.5, t, 0.0, 2.2)
        big(img, f"+{v:.1f}%", 600, t, -1, 240, LGREEN)
        en(img, "Nvidia shares in one day · Mon 23 Nov", 760, t, -1, 52, WHITE)
        chart(img, 120, 960, 840, 520, ease(seg(t, -0.3, 2.6)), [.1, .14, .1, .16, .12, .18, .15, .3, .55, .75, .92], LGREEN)
        if t > 2.4: img = punch(img, t, 2.4, .06)
    elif t < 12.0:
        ml(img, "എന്ത് സംഭവിച്ചു?", 330, t, 6.0, 100, WHITE)
        en(img, "What happened", 450, t, 6.2, 54, GOLD)
        card(img, 680, "Board brought its CEO back", 1, t, 6.6, GOLD)
        card(img, 880, "Nasdaq, same day", 2, t, 8.2, GREEN, "+6.51%", GREEN)
        en(img, "He had quit less than 2 weeks earlier", 1060, t, 8.2, 46, GREY, "s")
        chart(img, 140, 1180, 800, 320, ease(seg(t, 6.6, 9.6)), [.3, .25, .2, .12, .08, .4, .7, .9], LGREEN)
    elif t < 17.0:
        ml(img, "നിങ്ങളുടെ ₹1 ലക്ഷം?", 330, t, 12.0, 100, WHITE)
        en(img, "₹1 lakh in a Nasdaq-tracking fund", 450, t, 12.2, 54, GOLD)
        money_panel(img, t, "Fri ₹94,720 → Monday", 94720, 100886, "Back above ₹1 lakh", GREEN)
        for k in range(3): coin3d(img, 300 + k * 240, 1250 + 30 * math.sin(t * 2 + k), 70)
        if t > 14.0: img = punch(img, t, 14.0, .05)
    elif t < END:
        ml(img, "പാഠം എന്ത്?", 330, t, 17.0, 110, WHITE)
        en(img, "The lesson", 460, t, 17.1, 56, GOLD)
        card(img, 680, "Friday −5.28%, Monday +6.51%", 1, t, 17.4, GOLD)
        card(img, 880, "Big swings go both ways", 2, t, 17.8, GOLD)
        en(img, "Education only · not investment advice", 1080, t, 18.2, 46, GREY, "s")
        chart(img, 200, 1200, 680, 280, ease(seg(t, 17.2, 18.6)), [.6, .7, .2, .1, .75, .65, .8], GOLD, False)
    else:
        img = end_card(img, t, END)
    src(img, "Sources: Saxo, 10 Things, IC Markets, Tickmill market reports · 23–24 Nov 2026", t)
    return img

# ---------------- Short 2: Brent $109.55 → $89.37 ----------------
S2_CUES = "0:boom,0.2:tick*10,2.4:hit,6.0:whoosh,6.6:pop,8.2:fail,12.0:swoosh,12.8:tick*8,14.0:ding,17.0:whoosh,17.4:pop,17.8:pop,21.5:success"
def short2(t):
    img = scene_bg(t, "night", 92)
    if t < 6.0:
        ml(img, "എണ്ണ വില", 250, t, -1, 110, WHITE)
        ml(img, "ഇടിയുന്നോ?", 380, t, -1, 124, GOLD)
        v = count(109.55, 89.37, t, 0.0, 2.2)
        big(img, f"${v:.2f}", 600, t, -1, 220, ORANGE)
        en(img, "Brent crude, 1 barrel · 23 Nov close", 760, t, -1, 52, WHITE)
        if t > 3.0: pill(img, W / 2, 880, "Lowest close since August", t, 3.0, RED, WHITE, 50, 44)
        for k in range(3): barrel(img, W / 2 + (k - 1) * 260, 1290 + (k % 2) * 60, 1.05 * back(seg(t, -.2 + k * .25, .4 + k * .25)))
        if t > 2.4: img = shake(img, t, 2.4, 12, .4)
    elif t < 12.0:
        ml(img, "ഒരു മാസത്തിൽ", 330, t, 6.0, 100, WHITE)
        en(img, "In one month", 450, t, 6.2, 54, GOLD)
        card(img, 680, "Brent, 20 Oct close", 1, t, 6.6, GOLD, "$109.55", INK)
        card(img, 880, "Brent, 23 Nov close", 2, t, 8.2, RED, "$89.37", RED)
        chart(img, 140, 1120, 800, 380, ease(seg(t, 6.6, 10.0)), [.92, .95, .85, .8, .7, .66, .5, .38, .3, .2], ORANGE)
    elif t < 17.0:
        ml(img, "ഒരു ലിറ്റർ ക്രൂഡിന്?", 330, t, 12.0, 96, WHITE)
        en(img, "Crude in 1 litre (1 barrel = 159 L)", 450, t, 12.2, 54, GOLD)
        money_panel(img, t, "At $89.37 and ₹92.9 per $", 0, 52.2, "−$20 a barrel in a month", GREEN,
                    fmt=lambda v: f"₹{v:.0f}")
        for k in range(2): barrel(img, 380 + k * 320, 1300 + 16 * math.sin(t * 2 + k), .9)
        if t > 14.0: img = punch(img, t, 14.0, .05)
    elif t < END:
        ml(img, "എന്തുകൊണ്ട്?", 330, t, 17.0, 110, WHITE)
        en(img, "Why it fell", 460, t, 17.1, 56, GOLD)
        card(img, 680, "Libya's Sharara pipeline reopened", 1, t, 17.4, GOLD)
        card(img, 880, "More Middle East oil flowing again", 2, t, 17.8, GOLD)
        en(img, "Fuel bills may ease later · not certain", 1080, t, 18.2, 46, GREY, "s")
        for k in range(3): barrel(img, W / 2 + (k - 1) * 260, 1330 + (k % 2) * 50, .85 * back(seg(t, 17.2 + .2 * k, 17.8 + .2 * k)))
    else:
        img = end_card(img, t, END)
    src(img, "Sources: Brent settlements via Nation Thailand, Saxo, IC Markets, ScanX · 20 Oct–23 Nov 2026", t)
    return img

# ---------------- Short 3: Kerala gold ₹93,720 ----------------
S3_CUES = "0:boom,0.2:coin*8,2.4:ding,6.0:whoosh,6.6:pop,8.2:cash,12.0:swoosh,12.8:coin*6,14.0:cash,17.0:whoosh,17.4:pop,17.8:pop,21.5:success"
def short3(t):
    img = scene_bg(t, "night", 103)
    if t < 6.0:
        ml(img, "2 ദിവസം കൊണ്ട്", 250, t, -1, 100, WHITE)
        ml(img, "സ്വർണ്ണം എത്ര കൂടി?", 380, t, -1, 108, GOLD)
        v = count(91720, 93720, t, 0.0, 2.2)
        big(img, "₹" + inr(v), 600, t, -1, 200, GOLD)
        en(img, "1 pavan, Kerala 22K gold · 24 Nov", 760, t, -1, 52, WHITE)
        if t > 3.0: pill(img, W / 2, 880, "+₹2,000 in 2 days", t, 3.0, GREEN, WHITE, 56, 46)
        rays(img, W / 2, 1300, t, GOLD, 28)
        for k in range(3): gold_bar3d(img, W / 2 + (k - 1) * 320, 1280 + (k % 2) * 110, 0.95 * back(seg(t, -.2 + k * .25, .4 + k * .25)))
    elif t < 12.0:
        ml(img, "ഇന്ന് മാത്രം", 330, t, 6.0, 104, WHITE)
        en(img, "Today alone", 450, t, 6.2, 54, GOLD)
        card(img, 680, "22K gold, 1 gram", 1, t, 6.6, GOLD, "₹11,715", INK)
        card(img, 880, "1 pavan, up today", 2, t, 8.2, GREEN, "+₹920", GREEN)
        chart(img, 140, 1120, 800, 380, ease(seg(t, 6.6, 10.0)), [.5, .35, .2, .1, .15, .3, .55, .75], GOLD)
    elif t < 17.0:
        ml(img, "10 പവൻ ഉള്ളവർക്ക്?", 330, t, 12.0, 100, WHITE)
        en(img, "If you hold 10 pavan (80 g)", 450, t, 12.2, 54, GOLD)
        money_panel(img, t, "Gold value, Sat → today", 917200, 937200, "+₹20,000 in 2 days", GREEN)
        for k in range(3): gold_bar3d(img, 300 + k * 240, 1250 + 20 * math.sin(t * 2 + k), .75)
        if t > 14.0: img = punch(img, t, 14.0, .05)
    elif t < END:
        ml(img, "എന്തുകൊണ്ട്?", 330, t, 17.0, 110, WHITE)
        en(img, "Why it rose", 460, t, 17.1, 56, GOLD)
        card(img, 680, "World gold back near $3,635/oz", 1, t, 17.4, GOLD)
        card(img, 880, "Weak rupee, about ₹92.9 per $", 2, t, 17.8, GOLD)
        en(img, "Nobody knows tomorrow's price", 1080, t, 18.2, 46, GREY, "s")
        for k in range(3): gold_bar3d(img, W / 2 + (k - 1) * 300, 1320 + (k % 2) * 60, .8 * back(seg(t, 17.2 + .2 * k, 17.8 + .2 * k)))
    else:
        img = end_card(img, t, END)
    src(img, "Sources: Kerala 22K via Times Kerala, Oneindia Malayalam · spot: Saxo, IC Markets · 24 Nov 2026", t)
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
