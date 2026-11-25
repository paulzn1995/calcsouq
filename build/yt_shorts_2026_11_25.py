"""YouTube Shorts, 25 Nov 2026: top world money news (Malayalam + English, text + music, no narration).
1080x1920, 25 s, reading pace (every line ≥3 s, at most 2 new items at once, end card 4 s).
All text kept between y 250 and 1540 (Instagram/YouTube overlays).
Render:  python3 build/yt_shorts_2026_11_25.py <n> out_silent.mp4      (n = 1, 2, 3; 4 = Instagram copy of 1)
Frame:   python3 build/yt_shorts_2026_11_25.py <n> --frame <t> out.png
Helpers come from build/yt_shorts_2026_11_23.py / _24.py.
Facts (checked 25 Nov 2026, two sources each) are in build/youtube/2026-11-25-pack.md.
"""
import sys, os, subprocess, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_fx import *
from yt_shorts_2026_11_23 import ml, en, big, card, panel, chart, gold_bar3d, coin3d, end_card, GREY
from yt_shorts_2026_11_24 import inr

DUR = 25.0
END = 21.0
LGREEN = (90, 220, 130)

def src(img, txt, t):
    if t >= END: return
    d = ImageDraw.Draw(img); size = 36; f = F("s", size)
    while d.textlength(txt, font=f) > W - 80: size -= 1; f = F("s", size)
    d.text((W / 2, 1505), txt, font=f, fill=(170, 172, 185), anchor="mm")

def money_panel(img, t, label, v0, v1, reveal, rcol, fmt=lambda v: "₹" + inr(v)):
    """Beat 3: white panel with a count-up (12.8–14.0) and a reveal line (14.0 → 17.0)."""
    if panel(img, (140, 580, 940, 1040), t, 12.6):
        d = ImageDraw.Draw(img)
        v = count(v0, v1, t, 12.8, 14.0)
        lf = F("b", 48)
        while d.textlength(label, font=lf) > 740: lf = F("b", lf.size - 2)
        d.text((540, 680), label, font=lf, fill=(90, 95, 105), anchor="mm")
        d.text((540, 820), fmt(v), font=F("k", 140), fill=INK, anchor="mm")
        if t > 14.0: d.text((540, 960), reveal, font=F("k", 58), fill=rcol, anchor="mm")

def btc_coin(img, cx, cy, r):
    if r < 4: return
    d = ImageDraw.Draw(img)
    d.ellipse([cx - r, cy - r + 12, cx + r, cy + r + 12], fill=(170, 95, 10))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(247, 147, 26), outline=(200, 110, 10), width=5)
    d.ellipse([cx - r * .78, cy - r * .78, cx + r * .78, cy + r * .78], outline=(255, 200, 120), width=4)
    d.text((cx, cy), "₿", font=F("k", r * 1.1), fill=WHITE, anchor="mm")

# ---------------- Short 1: Kerala gold −₹2,360 in one go ----------------
S1_CUES = "0:boom,0.2:coin*8,2.4:hit,6.0:whoosh,6.6:pop,8.2:fail,12.0:swoosh,12.8:tick*8,14.0:fail,17.0:whoosh,17.4:pop,17.8:pop,21.0:success"
def short1(t):
    img = scene_bg(t, "night", 111)
    if t < 6.0:
        ml(img, "ഒറ്റയടിക്ക് പവന്", 320, t, -1, 100, WHITE)
        ml(img, "എത്ര കുറഞ്ഞു?", 440, t, -1, 116, GOLD)
        v = count(0, 2360, t, 0.0, 2.2)
        big(img, "−₹" + inr(v), 650, t, -1, 220, RED)
        en(img, "1 pavan of Kerala gold, today · 25 Nov", 810, t, -1, 52, WHITE)
        if t > 3.0: pill(img, W / 2, 930, "Now ₹91,360 · lowest this month", t, 3.0, GOLD, INK, 50, 44)
        for k in range(3): gold_bar3d(img, W / 2 + (k - 1) * 320, 1260 + (k % 2) * 100, 0.95 * back(seg(t, -.2 + k * .25, .4 + k * .25)))
        if t > 2.4: img = shake(img, t, 2.4, 12, .4)
    elif t < 12.0:
        ml(img, "ഇന്നത്തെ വില", 330, t, 6.0, 104, WHITE)
        en(img, "Today's price", 450, t, 6.2, 54, GOLD)
        card(img, 680, "22K gold, 1 gram", 1, t, 6.6, GOLD, "₹11,420", INK)
        card(img, 880, "1 pavan, fell today", 2, t, 8.2, RED, "−₹2,360", RED)
        en(img, "Yesterday ₹93,720 → today ₹91,360", 1060, t, 8.2, 46, GREY, "s")
        chart(img, 140, 1150, 800, 300, ease(seg(t, 6.6, 10.0)), [.5, .4, .3, .45, .62, .8, .2], GOLD)
    elif t < 17.0:
        ml(img, "10 പവൻ ഉള്ളവർക്ക്?", 330, t, 12.0, 100, WHITE)
        en(img, "If you hold 10 pavan (80 g)", 450, t, 12.2, 54, GOLD)
        money_panel(img, t, "Gold value, yesterday → today", 937200, 913600, "−₹23,600 in one day", RED)
        for k in range(3): gold_bar3d(img, 300 + k * 240, 1250 + 20 * math.sin(t * 2 + k), .75)
        if t > 14.0: img = shake(img, t, 14.0, 10, .35)
    elif t < END:
        ml(img, "എന്തുകൊണ്ട്?", 330, t, 17.0, 110, WHITE)
        en(img, "Why it fell", 460, t, 17.1, 56, GOLD)
        card(img, 680, "A stronger US dollar", 1, t, 17.4, GOLD)
        card(img, 880, "Bets on another US rate hike", 2, t, 17.8, GOLD)
        en(img, "Buying? Making charge + 3% GST come on top", 1080, t, 18.2, 46, GREY, "s")
        for k in range(3): gold_bar3d(img, W / 2 + (k - 1) * 300, 1300 + (k % 2) * 60, .8 * back(seg(t, 17.2 + .2 * k, 17.8 + .2 * k)))
    else:
        img = end_card(img, t, END)
    src(img, "Sources: Siraj Live, Oneindia Malayalam (Kerala 22K rate) · 24–25 Nov 2026", t)
    return img

# ---------------- Short 2: Sensex +1,502 ----------------
S2_CUES = "0:boom,0.2:tick*10,2.4:success,6.0:whoosh,6.6:fail,8.2:pop,12.0:swoosh,12.8:tick*8,14.0:cash,17.0:whoosh,17.4:pop,17.8:pop,21.0:success"
def short2(t):
    img = scene_bg(t, "berry", 122)
    if t < 6.0:
        ml(img, "ഷെയർ വിപണി", 320, t, -1, 104, WHITE)
        ml(img, "ഇന്ന് എത്ര കയറി?", 440, t, -1, 112, GOLD)
        v = count(0, 1502, t, 0.0, 2.2)
        big(img, f"+{v:,.0f}", 650, t, -1, 240, LGREEN)
        en(img, "Sensex points today · 25 Nov · +1.82%", 810, t, -1, 52, WHITE)
        if t > 3.0: pill(img, W / 2, 930, "Closed at 83,938", t, 3.0, GREEN, WHITE, 52, 44)
        chart(img, 120, 1080, 840, 370, ease(seg(t, -0.3, 2.6)), [.3, .22, .1, .05, .2, .45, .7, .95], LGREEN)
        if t > 2.4: img = punch(img, t, 2.4, .06)
    elif t < 12.0:
        ml(img, "രണ്ട് ദിവസം, രണ്ട് കഥ", 330, t, 6.0, 96, WHITE)
        en(img, "Two trading days, two stories", 450, t, 6.2, 54, GOLD)
        card(img, 680, "Monday, 23 Nov", 1, t, 6.6, RED, "−1,484", RED)
        card(img, 880, "Wednesday, 25 Nov", 2, t, 8.2, GREEN, "+1,502", GREEN)
        en(img, "Markets were shut on Tuesday", 1060, t, 8.2, 46, GREY, "s")
        chart(img, 140, 1150, 800, 300, ease(seg(t, 6.6, 10.0)), [.6, .5, .25, .1, .15, .45, .75, .9], LGREEN)
    elif t < 17.0:
        ml(img, "നിങ്ങളുടെ ₹1 ലക്ഷം?", 330, t, 12.0, 100, WHITE)
        en(img, "₹1 lakh in a Sensex index fund", 450, t, 12.2, 54, GOLD)
        money_panel(img, t, "Value before → after today", 100000, 101820, "+₹1,820 in one day", GREEN)
        for k in range(3): coin3d(img, 300 + k * 240, 1250 + 30 * math.sin(t * 2 + k), 70)
        if t > 14.0: img = punch(img, t, 14.0, .05)
    elif t < END:
        ml(img, "എന്തുകൊണ്ട്?", 330, t, 17.0, 110, WHITE)
        en(img, "Why it jumped", 460, t, 17.1, 56, GOLD)
        card(img, 680, "Foreign funds buying again", 1, t, 17.4, GOLD)
        card(img, 880, "Stronger rupee, about ₹92.2 per $", 2, t, 17.8, GOLD)
        en(img, "Education only · not investment advice", 1080, t, 18.2, 46, GREY, "s")
        chart(img, 200, 1180, 680, 270, ease(seg(t, 17.2, 18.6)), [.5, .6, .2, .1, .55, .7, .9], GOLD, False)
    else:
        img = end_card(img, t, END)
    src(img, "Sources: Reuters via Business Recorder, 5paisa, Udaipur Kiran, Univest · 23–25 Nov 2026", t)
    return img

# ---------------- Short 3: Bitcoin under $60,000 ----------------
S3_CUES = "0:boom,0.2:tick*10,2.4:fail,6.0:whoosh,6.6:pop,8.2:hit,12.0:swoosh,12.8:tick*8,14.0:fail,17.0:whoosh,17.4:pop,17.8:pop,21.0:success"
def short3(t):
    img = scene_bg(t, "night", 133)
    if t < 6.0:
        ml(img, "ബിറ്റ്കോയിൻ", 320, t, -1, 108, WHITE)
        ml(img, "പകുതിയിലും താഴെ?", 440, t, -1, 108, GOLD)
        v = count(126000, 58600, t, 0.0, 2.2)
        big(img, f"${v:,.0f}", 650, t, -1, 210, ORANGE)
        en(img, "1 Bitcoin, 25 Nov · peak was ~$126,000", 810, t, -1, 52, WHITE)
        if t > 3.0: pill(img, W / 2, 930, "About −53% from its peak", t, 3.0, RED, WHITE, 52, 44)
        for k in range(3): btc_coin(img, W / 2 + (k - 1) * 280, 1260 + (k % 2) * 80, 100 * back(seg(t, -.2 + k * .25, .4 + k * .25)) + 0.01)
        if t > 2.4: img = shake(img, t, 2.4, 12, .4)
    elif t < 12.0:
        ml(img, "എന്ത് സംഭവിച്ചു?", 330, t, 6.0, 100, WHITE)
        en(img, "What happened", 450, t, 6.2, 54, GOLD)
        card(img, 680, "Bitcoin today", 1, t, 6.6, ORANGE, "< $60,000", RED)
        card(img, 880, "ETF outflow, Nov", 2, t, 8.2, RED, "$4.7 bn+", RED)
        en(img, "Biggest monthly ETF outflow on record", 1060, t, 8.2, 46, GREY, "s")
        chart(img, 140, 1150, 800, 300, ease(seg(t, 6.6, 10.0)), [.95, .8, .7, .55, .6, .4, .3, .15], ORANGE)
    elif t < 17.0:
        ml(img, "ഉയരത്തിൽ ₹1 ലക്ഷം ഇട്ടെങ്കിൽ?", 330, t, 12.0, 96, WHITE)
        en(img, "₹1 lakh put in at the peak ($ terms)", 450, t, 12.2, 54, GOLD)
        money_panel(img, t, "Value then → now", 100000, 46500, "−₹53,500", RED)
        for k in range(3): btc_coin(img, 300 + k * 240, 1250 + 25 * math.sin(t * 2 + k), 62)
        if t > 14.0: img = shake(img, t, 14.0, 10, .35)
    elif t < END:
        ml(img, "എന്തുകൊണ്ട്?", 330, t, 17.0, 110, WHITE)
        en(img, "Why it fell", 460, t, 17.1, 56, GOLD)
        card(img, 680, "Fear of higher US rates", 1, t, 17.4, GOLD)
        card(img, 880, "Tech sell-off and tariff worries", 2, t, 17.8, GOLD)
        en(img, "Education only · not investment advice", 1080, t, 18.2, 46, GREY, "s")
        for k in range(3): btc_coin(img, W / 2 + (k - 1) * 280, 1300 + (k % 2) * 50, 70 * back(seg(t, 17.2 + .2 * k, 17.8 + .2 * k)) + 0.01)
    else:
        img = end_card(img, t, END)
    src(img, "Sources: Business Today (Bloomberg data), CoinDesk · 25 Nov 2026", t)
    return img

def ig_end(img, t, t0):
    """Instagram copy: end on a share/comment prompt instead of the YouTube subscribe card."""
    ml(img, "സ്വർണ്ണം വാങ്ങാൻ", 520, t, t0, 92, WHITE)
    ml(img, "ഇരിക്കുന്നവർക്ക് അയക്കൂ", 650, t, t0 + .2, 86, GOLD)
    en(img, "Send this to someone buying gold", 790, t, t0 + .6, 50, WHITE)
    pill(img, W / 2, 960, "Buy now or wait? Comment 👇".replace(" 👇", ""), t, t0 + .9, GOLD, INK, 56, 56)
    if t > t0 + 1.2:
        d = ImageDraw.Draw(img); d.text((W / 2, 1100), "calcsouq.com", font=F("k", 64), fill=GOLD, anchor="mm")
        d.text((W / 2, 1180), "Gold price calculator", font=F("s", 46), fill=GREY, anchor="mm")
    for k in range(3):
        if t > t0 + .3 + .2 * k: gold_bar3d(img, W / 2 + (k - 1) * 300, 1340 + (k % 2) * 50, .7)
    return img

def short1_ig(t):
    if t < END: return short1(t)
    return ig_end(scene_bg(t, "night", 111), t, END)

SHORTS = {1: (short1, S1_CUES), 2: (short2, S2_CUES), 3: (short3, S3_CUES), 4: (short1_ig, S1_CUES)}

if __name__ == "__main__":
    fn, _ = SHORTS[int(sys.argv[1])]
    if sys.argv[2] == "--frame":
        fn(float(sys.argv[3])).convert("RGB").save(sys.argv[4]); sys.exit()
    out = sys.argv[2]; tmp = out + ".tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)): p.stdin.write(fn(i / FPS).convert("RGB").tobytes())
    p.stdin.close(); assert p.wait() == 0; os.replace(tmp, out); print(out)
