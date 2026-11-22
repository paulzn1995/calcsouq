"""Instagram teaser reel for YouTube long video #3 (Malayalam: why gold is falling + gold loan). 1080x1920, reading pace, ~24.5 s.
Render: python3 reel_gold_ml_teaser.py out_silent.mp4 ; then reel_audio.py with CUES below.
"""
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_fx import *
from PIL import ImageFont
DUR = 24.5
CUES = "0:boom,1.2:tick*10,3.8:hit,6.0:whoosh,6.6:pop,8.2:pop,9.8:pop,13.0:whoosh,14.4:coin*4,16.0:fail,19.0:swoosh,20.4:success"
_MLF = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts", "Manjari-Bold.ttf")
def MF(s): return ImageFont.truetype(_MLF, int(s), layout_engine=ImageFont.Layout.RAQM)

def ml(img, txt, y, t, t0, size, col):
    p = ease(seg(t, t0, t0 + .5))
    if p <= 0: return
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
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

def frame(t):
    img = scene_bg(t, "night", 33); d = ImageDraw.Draw(img)
    if t < 6.0:
        ml(img, "പണയം വെച്ചവർ", 300, t, 0.1, 110, WHITE)
        ml(img, "കുടുങ്ങിയോ?", 430, t, 0.5, 120, GOLD)
        v = count(0, 39480, t, 1.2, 3.6); d = ImageDraw.Draw(img)
        if t > 1.2: d.text((W / 2, 640), f"−₹{v:,.0f}", font=F("k", 170), fill=RED, anchor="mm")
        if t > 3.0: pill(img, W / 2, 810, "gold, per pavan · January → today", t, 3.0, WHITE, INK, 50, 42)
        for k in range(3): bar(img, W / 2 + (k - 1) * 330, 1150 + (k % 2) * 90, 0.95 * back(seg(t, .4 + k * .2, 1.0 + k * .2)))
        if t > 3.8: shake(img, t, 3.8, 12, 0.4)
    elif t < 13.0:
        ml(img, "എന്തുകൊണ്ട്?", 380, t, 6.0, 120, WHITE)
        d = ImageDraw.Draw(img); d.text((W / 2, 480), "Why is gold falling?", font=F("b", 56), fill=GOLD, anchor="mm")
        for i, (txt, t0) in enumerate([("US Fed: more rate hikes", 6.6), ("Dollar near 19-month high", 8.2), ("Stock crash: gold sold for cash", 9.8)]):
            card(img, 680 + i * 190, txt, i + 1, t, t0)
    elif t < 19.0:
        ml(img, "ഗോൾഡ് ലോൺ ഉണ്ടോ?", 380, t, 13.0, 86, GOLD)
        d = ImageDraw.Draw(img); d.text((W / 2, 480), "Have a gold loan?", font=F("b", 56), fill=WHITE, anchor="mm")
        p = back(seg(t, 13.6, 14.1))
        if p > 0:
            box = (140, 600, 940, 1000); shadow(img, box, 40, 18, 90, (0, 10)); d = ImageDraw.Draw(img); d.rounded_rectangle(box, 40, fill=WHITE)
            d.text((540, 680), "Same loan, cheaper gold", font=F("b", 44), fill=(100, 105, 115), anchor="mm")
            v = count(69, 98, t, 14.4, 16.0); col = GREEN if v < 80 else RED
            d.text((540, 830), f"LTV {v:.0f}%", font=F("k", 150), fill=col, anchor="mm")
            d.text((540, 950), "loan ÷ gold value", font=F("b", 40), fill=(100, 105, 115), anchor="mm")
        if t > 16.2: pill(img, W / 2, 1140, "Bank may ask for margin", t, 16.2, RED, WHITE, 56, 48)
    else:
        ml(img, "ബാങ്ക് വിളിക്കും മുൻപ്", 330, t, 19.0, 92, WHITE)
        ml(img, "ഈ വീഡിയോ കാണുക", 460, t, 19.3, 86, GOLD)
        d = ImageDraw.Draw(img)
        if t > 19.6: d.text((W / 2, 580), "Watch before the bank calls", font=F("b", 52), fill=WHITE, anchor="mm")
        if t > 19.6: d.text((W / 2, 650), "Malayalam · English subtitles", font=F("b", 42), fill=(200, 200, 210), anchor="mm")
        bar(img, W / 2, 880, 1.2 * back(seg(t, 19.2, 19.8)))
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
