"""Instagram teaser reel for YouTube long video #5 (Malayalam: will your home loan EMI rise again? RBI 4 Dec). 1080x1920, reading pace, 25 s.
Render: python3 reel_emi_ml_teaser.py out_silent.mp4 ; then reel_audio.py with CUES below.
"""
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_fx import *
from PIL import ImageFont
DUR = 25.0
CUES = "0:boom,1.2:tick*8,3.4:hit,6.0:whoosh,6.8:pop,8.2:pop,9.6:pop,13.4:whoosh,14.6:tick*6,16.2:fail,19.6:swoosh,20.8:success"
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
    x = 110 + (1 - p) * 80; r = x + 860; d = ImageDraw.Draw(img)  # whole card slides, so text never overruns the right edge
    shadow(img, (x, y - 70, r, y + 70), 36, 16, 80, (0, 8)); d = ImageDraw.Draw(img)
    d.rounded_rectangle([x, y - 70, r, y + 70], 36, fill=WHITE)
    d.ellipse([x + 26, y - 40, x + 106, y + 40], fill=GOLD); d.text((x + 66, y), str(i), font=F("k", 48), fill=INK, anchor="mm")
    d.text((x + 134, y), txt, font=F("b", 46), fill=INK, anchor="lm")

def house(img, cx, cy, s):
    if s < 0.05: return
    d = ImageDraw.Draw(img); fw, fh, sw = 300 * s, 210 * s, 150 * s; x0, y0 = cx - fw / 2 - sw / 2, cy - fh / 2 + 40 * s
    shadow(img, (x0, y0 + fh - 20 * s, x0 + fw + sw, y0 + fh + 30 * s), int(40 * s), 20, 110, (0, 6)); d = ImageDraw.Draw(img)
    d.polygon([(x0, y0), (x0 + fw, y0), (x0 + fw, y0 + fh), (x0, y0 + fh)], fill=(236, 226, 208))
    d.polygon([(x0 + fw, y0), (x0 + fw + sw, y0 - sw * .35), (x0 + fw + sw, y0 + fh - sw * .35), (x0 + fw, y0 + fh)], fill=(176, 164, 146))
    d.polygon([(x0 - 28 * s, y0 + 8 * s), (x0 + fw / 2, y0 - 130 * s), (x0 + fw + 28 * s, y0 + 8 * s)], fill=(176, 70, 48))
    d.polygon([(x0 + fw / 2, y0 - 130 * s), (x0 + fw / 2 + sw, y0 - 130 * s - sw * .35), (x0 + fw + sw + 20 * s, y0 - sw * .35 + 6 * s), (x0 + fw + 28 * s, y0 + 8 * s)], fill=(124, 46, 34))
    for wx in (x0 + 40 * s, x0 + fw - 100 * s): d.rectangle([wx, y0 + 50 * s, wx + 60 * s, y0 + 110 * s], fill=(255, 205, 110), outline=(90, 80, 70), width=max(2, int(4 * s)))
    d.rectangle([x0 + fw / 2 - 32 * s, y0 + fh - 100 * s, x0 + fw / 2 + 32 * s, y0 + fh], fill=(96, 64, 44))

def frame(t):
    img = scene_bg(t, "night", 53); d = ImageDraw.Draw(img)
    if t < 6.0:
        ml(img, "ഹോം ലോൺ EMI", 290, t, 0.1, 100, WHITE)
        ml(img, "വീണ്ടും കൂടുമോ?", 420, t, 0.5, 112, GOLD)
        v = count(0, 1382, t, 1.2, 3.0); d = ImageDraw.Draw(img)
        if t > 1.2: d.text((W / 2, 630), "+₹{:,}".format(int(v)), font=F("k", 170), fill=RED, anchor="mm"); d.text((W / 2, 750), "more EMI a month", font=F("b", 52), fill=WHITE, anchor="mm")
        if t > 3.0: pill(img, W / 2, 880, "₹30 lakh loan · if repo reaches 6%", t, 3.0, WHITE, INK, 46, 40)
        house(img, W / 2, 1330, 1.4 * back(seg(t, .4, 1.0)))
        if t > 3.4: shake(img, t, 3.4, 10, 0.4)
    elif t < 13.4:
        ml(img, "എന്തുകൊണ്ട്?", 380, t, 6.0, 110, WHITE)
        d = ImageDraw.Draw(img); d.text((W / 2, 490), "Why rates are rising", font=F("b", 56), fill=GOLD, anchor="mm")
        for i, (txt, t0) in enumerate([("Inflation 6.09% in October", 6.8), ("RBI repo 5.25% → 5.50%", 8.2), ("Next RBI decision: 4 Dec", 9.6)]):
            card(img, 680 + i * 190, txt, i + 1, t, t0)
    elif t < 19.6:
        ml(img, "നിശബ്ദ കെണി", 380, t, 13.4, 104, GOLD)
        d = ImageDraw.Draw(img); d.text((W / 2, 490), "Same EMI, longer loan", font=F("b", 56), fill=WHITE, anchor="mm")
        p = back(seg(t, 13.9, 14.4))
        if p > 0:
            box = (140, 600, 940, 1010); shadow(img, box, 40, 18, 90, (0, 10)); d = ImageDraw.Draw(img); d.rounded_rectangle(box, 40, fill=WHITE)
            d.text((540, 680), "₹30 lakh · 20 years · 8%", font=F("b", 46), fill=(100, 105, 115), anchor="mm")
            v = count(0, 39, t, 14.6, 16.2); d.text((540, 820), f"+{v:.0f} months", font=F("k", 120), fill=RED, anchor="mm")
            d.text((540, 950), "≈ ₹9.3 lakh more paid", font=F("b", 48), fill=(100, 105, 115), anchor="mm")
        if t > 16.4: pill(img, W / 2, 1140, "Raise the EMI: ≈ ₹3.3 lakh", t, 16.4, (40, 160, 90), WHITE, 52, 46)
    else:
        ml(img, "ഇപ്പോൾ എന്ത് ചെയ്യാം?", 330, t, 19.6, 92, WHITE)
        ml(img, "മുഴുവൻ വീഡിയോ കാണുക", 460, t, 19.9, 72, GOLD)
        d = ImageDraw.Draw(img)
        if t > 20.2: d.text((W / 2, 580), "4 steps + prepayment maths", font=F("b", 52), fill=WHITE, anchor="mm")
        if t > 20.2: d.text((W / 2, 650), "Malayalam · English subtitles", font=F("b", 44), fill=(200, 200, 210), anchor="mm")
        house(img, W / 2, 905, 0.8 * back(seg(t, 19.8, 20.4)))
        pill(img, W / 2, 1110, "Watch on YouTube", t, 20.8, (230, 33, 23), WHITE, 58, 52)
        if t > 21.2: d = ImageDraw.Draw(img); d.text((W / 2, 1240), "youtube.com/@calcsouq · link in bio", font=F("b", 44), fill=WHITE, anchor="mm")
    return img

def barrel(img, cx, cy, s):
    if s < 0.05: return
    d = ImageDraw.Draw(img); w, h = 170 * s, 240 * s
    for i in range(int(w)):
        f = i / w; light = 0.35 + 0.9 * max(0, 1 - abs(f - 0.32) / 0.5) ** 1.6
        d.line([(cx - w / 2 + i, cy - h / 2 + 10 * s), (cx - w / 2 + i, cy + h / 2 - 10 * s)], fill=tuple(min(255, int(c * light)) for c in (160, 30, 30)))
    d.ellipse([cx - w / 2, cy - h / 2, cx + w / 2, cy - h / 2 + 26 * s], fill=(110, 20, 20), outline=(210, 210, 215), width=3)
    for fr in (.33, .66): d.line([(cx - w / 2, cy - h / 2 + h * fr), (cx + w / 2, cy - h / 2 + h * fr)], fill=(20, 10, 10), width=max(3, int(8 * s)))

if __name__ == "__main__":
    if sys.argv[1] == "--frame":
        frame(float(sys.argv[2])).convert("RGB").save(sys.argv[3]); sys.exit()
    out = sys.argv[1]; tmp = out + ".tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)): p.stdin.write(frame(i / FPS).convert("RGB").tobytes())
    p.stdin.close(); assert p.wait() == 0; os.replace(tmp, out); print(out)
