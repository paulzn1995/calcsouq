"""Instagram teaser reel for the Malayalam onion-inflation video. 1080x1920, reading pace, ~22 s.
Render: python3 reel_onion_ml_teaser.py out_silent.mp4 ; then reel_audio.py with CUES below.
"""
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_fx import *
from reel_hormuz_ml_teaser import ml, card, MF
import reel_fx as _RF
_SZ = (_RF.W, _RF.H)
import yt_long_onion_ml as O
_RF.W, _RF.H = _SZ  # the 16:9 helpers resize reel_fx on import; restore 1080x1920
for _m in [m for m in list(sys.modules.values()) if m and getattr(m, '__name__', '').startswith('reel_')]:
    if hasattr(_m, 'W') and _m.__name__ != 'reel_audio': _m.W, _m.H = _SZ
W, H = _SZ
HOLD = 1.6  # EOD QA 23 Nov: keep "+₹140" on screen 3.2 s (was 1.6 s) before the end card
DUR = 22.0 + HOLD
CUES = "0:boom,1.0:tick*10,2.8:hit,6.0:whoosh,6.8:pop,8.2:pop,9.6:pop,13.0:whoosh,14.0:coin*4,18.8:swoosh,19.8:success"

def frame(t):
    img = scene_bg(t, "night", 43)
    if t >= 17.2 + HOLD: t -= HOLD
    elif t >= 17.2: t = 17.19
    if t < 6.0:
        ml(img, "ഉള്ളി വില", 300, t, 0.1, 110, WHITE)
        ml(img, "ഇരട്ടിയായി!", 440, t, 0.5, 120, GOLD)
        v = count(0, 116, t, 1.0, 2.8); d = ImageDraw.Draw(img)
        if t > 1.0: d.text((W / 2, 650), f"+{v:.0f}%", font=F("k", 200), fill=RED, anchor="mm")
        if t > 2.8: pill(img, W / 2, 830, "Onion · Oct, year on year", t, 2.8, WHITE, INK, 46, 40)
        O.onion(img, W / 2, 1300, 2.2 * back(seg(t, .3, 1.0)))
        if t > 2.8: shake(img, t, 2.8, 12, 0.4)
    elif t < 13.0:
        ml(img, "അടുക്കളയിൽ", 380, t, 6.0, 110, WHITE)
        d = ImageDraw.Draw(img); d.text((W / 2, 480), "Not just onions", font=F("b", 56), fill=GOLD, anchor="mm")
        for i, (txt, t0) in enumerate([("Garlic +61% · Ginger +48%", 6.8), ("Food inflation 8.94%", 8.2), ("CPI 6.09% · above RBI's 6%", 9.6)]):
            card(img, 680 + i * 190, txt, i + 1, t, t0)
    elif t < 17.2:
        ml(img, "ഒരു വീടിന് മാസം", 380, t, 13.0, 90, GOLD)
        d = ImageDraw.Draw(img); d.text((W / 2, 480), "4 kg a month · example", font=F("b", 46), fill=WHITE, anchor="mm")
        p = back(seg(t, 13.4, 13.9))
        if p > 0:
            box = (140, 600, 940, 1000); shadow(img, box, 40, 18, 90, (0, 10)); d = ImageDraw.Draw(img); d.rounded_rectangle(box, 40, fill=WHITE)
            d.text((540, 680), "₹120  →  ₹260", font=F("b", 60), fill=(100, 105, 115), anchor="mm")
            v = count(0, 140, t, 14.0, 15.6); d.text((540, 840), f"+₹{v:.0f}", font=F("k", 160), fill=RED, anchor="mm")
            d.text((540, 950), "more, just for onions", font=F("b", 40), fill=(100, 105, 115), anchor="mm")
    else:
        ml(img, "എന്തുകൊണ്ട്?", 330, t, 17.2, 110, WHITE)
        ml(img, "മുഴുവൻ വീഡിയോ കാണുക", 470, t, 17.5, 72, GOLD)
        d = ImageDraw.Draw(img)
        if t > 17.8: d.text((W / 2, 590), "Why potatoes got cheaper", font=F("b", 52), fill=WHITE, anchor="mm")
        if t > 17.8: d.text((W / 2, 660), "Malayalam · English subtitles", font=F("b", 42), fill=(200, 200, 210), anchor="mm")
        O.onion(img, W / 2, 870, 1.4 * back(seg(t, 17.4, 18.0)))
        pill(img, W / 2, 1110, "Watch on YouTube", t, 18.2, (230, 33, 23), WHITE, 58, 52)
        if t > 18.6: d = ImageDraw.Draw(img); d.text((W / 2, 1240), "youtube.com/@calcsouq · link in bio", font=F("b", 44), fill=WHITE, anchor="mm")
    return img

if __name__ == "__main__":
    if sys.argv[1] == "--frame":
        frame(float(sys.argv[2])).convert("RGB").save(sys.argv[3]); sys.exit()
    out = sys.argv[1]; tmp = out + ".tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)): p.stdin.write(frame(i / FPS).convert("RGB").tobytes())
    p.stdin.close(); assert p.wait() == 0; os.replace(tmp, out); print(out)
