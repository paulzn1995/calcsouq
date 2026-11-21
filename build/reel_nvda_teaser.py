"""Instagram teaser reel for YouTube long video #2 (Nvidia / AI stocks crash). 1080x1920, reading pace, ~24.5 s.
Render: python3 reel_nvda_teaser.py out_silent.mp4 ; then reel_audio.py with CUES below.
"""
import sys, os, math, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_fx import *
DUR = 24.5
CUES = "0:boom,1.2:tick*10,3.6:hit,5.2:whoosh,5.6:pop,7.0:pop,8.4:pop,9.8:pop,12.4:whoosh,13:coin*5,15.2:riser,16.2:fail,19:swoosh,20.4:success"

def chip(img, cx, cy, s, red=0.0):
    d = ImageDraw.Draw(img); body = mix((40, 44, 56), (130, 30, 40), red)
    for k in range(5):
        o = -80 + k * 40
        for (x1, y1, x2, y2) in [(cx + o * s, cy - 150 * s, cx + o * s, cy - 110 * s), (cx + o * s, cy + 110 * s, cx + o * s, cy + 150 * s),
                                 (cx - 150 * s, cy + o * s, cx - 110 * s, cy + o * s), (cx + 110 * s, cy + o * s, cx + 150 * s, cy + o * s)]:
            d.line([(x1, y1), (x2, y2)], fill=(210, 180, 100), width=max(2, int(10 * s)))
    d.rounded_rectangle([cx - 120 * s, cy - 120 * s, cx + 120 * s, cy + 120 * s], int(22 * s), fill=body, outline=INK, width=6)
    d.rounded_rectangle([cx - 75 * s, cy - 75 * s, cx + 75 * s, cy + 75 * s], int(14 * s), fill=(200, 202, 210), outline=INK, width=5)
    if s > 0.2: d.text((cx, cy), "AI", font=F("k", 64 * s), fill=INK, anchor="mm")

def frame(t):
    img = scene_bg(t, "night", 21); d = ImageDraw.Draw(img)
    if t < 5.2:
        kinetic(img, "NVIDIA", 420, t, 0.1, 150, WHITE)
        v = count(0, 47, t, 1.2, 3.4); d = ImageDraw.Draw(img)
        if t > 1.2: d.text((W / 2, 640), f"−{v:.0f}%", font=F("k", 260), fill=RED, anchor="mm")
        if t > 3.0: pill(img, W / 2, 820, "in about 7 weeks", t, 3.0, WHITE, INK, 54, 44)
        chip(img, W / 2, 1180, 1.2 * back(seg(t, .3, .8)) + 1e-3, ease(seg(t, 3.4, 4.2)))
        if t > 3.6: shake(img, t, 3.6, 14, 0.4)
    elif t < 12.2:
        kinetic(img, "4 reasons it fell", 380, t, 5.2, 92, GOLD)
        items = [("AI spending vs profit", 5.6), ("Midterms: AI rule fears", 7.0), ("CEO resigned 12 Nov", 8.4), ("Rate hike expected", 9.8)]
        for i, (txt, t0) in enumerate(items):
            p = back(seg(t, t0, t0 + .6))
            if p > 0:
                y = 560 + i * 190; x = 110 + (1 - p) * 80; d = ImageDraw.Draw(img)
                shadow(img, (x, y - 70, 970, y + 70), 36, 16, 80, (0, 8)); d = ImageDraw.Draw(img)
                d.rounded_rectangle([x, y - 70, 970, y + 70], 36, fill=WHITE)
                d.ellipse([x + 26, y - 40, x + 106, y + 40], fill=GOLD); d.text((x + 66, y), str(i + 1), font=F("k", 48), fill=INK, anchor="mm")
                d.text((x + 134, y), txt, font=F("b", 50), fill=INK, anchor="lm")
    elif t < 19:
        kinetic(img, "The maths of a crash", 380, t, 12.3, 84, GOLD)
        for i, (lab, val, col, t0) in enumerate([("$1,000 at the record", 1000, GREEN, 12.6), ("Worth now", 525, RED, 13.4)]):
            p = back(seg(t, t0, t0 + .5))
            if p > 0:
                y = 640 + i * 300; d = ImageDraw.Draw(img); box = (140, y - 120, 940, y + 120)
                shadow(img, box, 40, 18, 90, (0, 10)); d = ImageDraw.Draw(img); d.rounded_rectangle(box, 40, fill=WHITE)
                d.text((540, y - 60), lab, font=F("b", 44), fill=(100, 105, 115), anchor="mm")
                v = val if i == 0 else count(1000, val, t, t0 + .3, t0 + 1.8)
                d.text((540, y + 40), f"${v:,.0f}", font=F("k", 120), fill=col, anchor="mm")
        if t > 15.6: pill(img, W / 2, 1290, "+91% just to get back", t, 15.6, GOLD, INK, 60, 50)
    else:
        kinetic(img, "Is the AI bubble", 420, t, 19.0, 100, WHITE)
        kinetic(img, "bursting?", 540, t, 19.3, 120, GOLD)
        souq(img, W / 2, 900, 0.85 * back(seg(t, 19.2, 19.7)) + 1e-3, t, "thinking", wave=t > 21.5)
        pill(img, W / 2, 1210, "Full explainer on YouTube", t, 20.4, (230, 33, 23), WHITE, 56, 50)
        if t > 21.0: d = ImageDraw.Draw(img); d.text((W / 2, 1340), "youtube.com/@calcsouq · link in bio", font=F("b", 44), fill=WHITE, anchor="mm")
    return img

REELS = {"nvda": (frame, DUR)}

if __name__ == "__main__":
    out = sys.argv[1]; tmp = out + ".tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)): p.stdin.write(frame(i / FPS).convert("RGB").tobytes())
    p.stdin.close(); assert p.wait() == 0; os.replace(tmp, out); print(out)
