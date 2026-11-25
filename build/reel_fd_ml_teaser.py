"""Instagram teaser reel for the Malayalam long video "FD rates up: open now or wait for 4 Dec?" 1080x1920, reading pace, 24.5 s.
Render: python3 reel_fd_ml_teaser.py out_silent.mp4 ; then reel_audio.py with CUES below.
"""
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_fx import *
from PIL import ImageFont
DUR = 24.5
CUES = "0:boom,1.2:tick*10,3.6:hit,6.0:whoosh,6.6:coin*4,8.4:pop,10.0:ding,13.0:whoosh,13.6:pop,15.2:pop,16.6:fail,19.0:swoosh,20.4:success"
_MLF = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts", "Manjari-Bold.ttf")
def MF(s): return ImageFont.truetype(_MLF, int(s), layout_engine=ImageFont.Layout.RAQM)

def ml(img, txt, y, t, t0, size, col):
    p = ease(seg(t, t0, t0 + .5))
    if p <= 0: return
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    while size > 40 and d.textlength(txt, font=MF(size)) > 940: size -= 4  # keep inside the frame with side margins
    d.text((W / 2, y + (1 - p) * 40), txt, font=MF(size), fill=col + (int(255 * p),), anchor="mm", stroke_width=2, stroke_fill=col + (int(255 * p),))
    img.alpha_composite(layer) if img.mode == "RGBA" else img.paste(layer, (0, 0), layer)

def bar(img, cx, cy, s):
    if s < 0.05: return
    d = ImageDraw.Draw(img)
    top = [(cx - 120 * s, cy - 50 * s), (cx + 120 * s, cy - 50 * s), (cx + 170 * s, cy + 60 * s), (cx - 170 * s, cy + 60 * s)]
    d.polygon(top, fill=(236, 190, 70), outline=(150, 105, 20))
    d.polygon([(cx - 120 * s, cy - 50 * s), (cx + 120 * s, cy - 50 * s), (cx + 95 * s, cy - 20 * s), (cx - 95 * s, cy - 20 * s)], fill=(255, 222, 120))
    if s > 0.3: d.text((cx, cy + 22 * s), "999.9", font=F("b", 34 * s), fill=(150, 105, 20), anchor="mm")

def card(img, y, txt, i, t, t0):
    p = back(seg(t, t0, t0 + .6))
    if p <= 0: return
    x = 110 + (1 - p) * 80; d = ImageDraw.Draw(img)
    shadow(img, (x, y - 70, 970, y + 70), 36, 16, 80, (0, 8)); d = ImageDraw.Draw(img)
    d.rounded_rectangle([x, y - 70, 970, y + 70], 36, fill=WHITE)
    d.ellipse([x + 26, y - 40, x + 106, y + 40], fill=GOLD); d.text((x + 66, y), str(i), font=F("k", 48), fill=INK, anchor="mm")
    d.text((x + 134, y), txt, font=F("b", 46), fill=INK, anchor="lm")

def coin(img, cx, cy, r):
    d = ImageDraw.Draw(img); ry = r * .32
    d.rectangle([cx - r, cy - 16, cx + r, cy], fill=(160, 120, 30)); d.ellipse([cx - r, cy - ry, cx + r, cy + ry], fill=(160, 120, 30))
    d.ellipse([cx - r, cy - 16 - ry, cx + r, cy - 16 + ry], fill=(240, 200, 90)); d.ellipse([cx - r * .7, cy - 16 - ry * .7, cx + r * .7, cy - 16 + ry * .7], outline=(255, 230, 150), width=4)

def stack(img, cx, ybase, n, r=90):
    for i in range(int(n)): coin(img, cx, ybase - i * 18, r)

def box2(img, y, top, val, sub, col, t, t0):
    p = back(seg(t, t0, t0 + .6))
    if p <= 0: return
    x0 = 120 + (1 - p) * 80; box = (x0, y - 120, 960, y + 120); shadow(img, box, 40, 18, 90, (0, 10)); d = ImageDraw.Draw(img)
    d.rounded_rectangle(box, 40, fill=WHITE)
    d.text((540, y - 70), top, font=F("b", 38), fill=(100, 105, 115), anchor="mm")
    d.text((540, y + 10), val, font=F("k", 96), fill=col, anchor="mm")
    d.text((540, y + 85), sub, font=F("b", 34), fill=(100, 105, 115), anchor="mm")

def frame(t):
    img = scene_bg(t, "night", 41); d = ImageDraw.Draw(img)
    if t < 6.0:
        ml(img, "FD ഇപ്പോൾ ഇടണോ?", 300, t, 0.1, 104, WHITE)
        ml(img, "കാത്തിരിക്കണോ?", 430, t, 0.5, 110, GOLD)
        v = count(6.0, 7.20, t, 1.2, 3.4); d = ImageDraw.Draw(img)
        if t > 1.2: d.text((W / 2, 650), f"{v:.2f}%", font=F("k", 200), fill=GREEN, anchor="mm")
        if t > 2.6: pill(img, W / 2, 830, "senior FD · big bank · Nov 2026", t, 2.6, WHITE, INK, 50, 42)
        for k in range(3): stack(img, W / 2 + (k - 1) * 300, 1250 - (k % 2) * 60, 7 * ease(seg(t, .4 + k * .25, 1.6 + k * .25)))
    elif t < 13.0:
        ml(img, "₹5 ലക്ഷം, ഒരു വർഷം", 330, t, 6.0, 92, WHITE)
        d = ImageDraw.Draw(img); d.text((W / 2, 440), "₹5 lakh FD for 1 year (6.25%)", font=F("b", 50), fill=GOLD, anchor="mm")
        box2(img, 680, "Interest", "+₹31,990", "quarterly compounding", GREEN, t, 6.6)
        box2(img, 960, "Prices up 6.09%", "₹30,450", "what inflation takes", RED, t, 8.4)
        if t > 10.0: pill(img, W / 2, 1200, "Real gain ≈ ₹1,540", t, 10.0, GOLD, INK, 64, 56)
    elif t < 19.0:
        ml(img, "ഡിസംബർ 4 വരെ", 250, t, 13.0, 92, WHITE)
        ml(img, "കാത്തിരുന്നാൽ?", 365, t, 13.2, 96, GOLD)
        d = ImageDraw.Draw(img); d.text((W / 2, 465), "Wait for the RBI on 4 Dec?", font=F("b", 50), fill=WHITE, anchor="mm")
        box2(img, 680, "One month of interest lost", "₹2,604", "₹5 lakh at 6.25%, money idle", RED, t, 13.6)
        box2(img, 960, "If rates rise 0.25%", "+₹1,311", "extra in a whole year", GREEN, t, 15.2)
        if t > 16.6: pill(img, W / 2, 1200, "Idle waiting often loses", t, 16.6, RED, WHITE, 58, 50)
    else:
        ml(img, "ലാഡർ, സുരക്ഷ, ടി ഡി എസ്", 330, t, 19.0, 84, WHITE)
        ml(img, "മുഴുവൻ വീഡിയോ YouTube-ൽ", 460, t, 19.3, 80, GOLD)
        d = ImageDraw.Draw(img)
        if t > 19.6: d.text((W / 2, 580), "Malayalam · English subtitles", font=F("b", 46), fill=(200, 200, 210), anchor="mm")
        stack(img, W / 2, 940, 8 * ease(seg(t, 19.2, 20.2)), 110)
        pill(img, W / 2, 1110, "Watch on YouTube", t, 20.4, (230, 33, 23), WHITE, 58, 52)
        if t > 21.0: d = ImageDraw.Draw(img); d.text((W / 2, 1240), "youtube.com/@calcsouq · link in bio", font=F("b", 44), fill=WHITE, anchor="mm")
    return img

if __name__ == "__main__":
    if sys.argv[1] == "--frame":
        frame(float(sys.argv[2])).convert("RGB").save(sys.argv[3]); sys.exit()
    out = sys.argv[1]; tmp = out + ".tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)): p.stdin.write(frame(i / FPS).convert("RGB").tobytes())
    p.stdin.close(); assert p.wait() == 0; os.replace(tmp, out); print(out)
