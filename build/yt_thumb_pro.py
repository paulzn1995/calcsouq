"""Premium, realistic-style YouTube thumbnail (1280x720): dark trading-screen look, candlestick chart, glow, bold type.
No mascot, no logos, no photos of people.
Usage: python3 yt_thumb_pro.py out.jpg --big "−47%" --top "NVIDIA" --sub "IS THE AI BUBBLE BURSTING?" --trend down --start 239 --end 125 --tag "STOCK CRASH EXPLAINED"
"""
import argparse, math, random
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

I = "/usr/share/fonts/opentype/inter/"
import os
_ML = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts/Manjari-Bold.ttf")
def F(w, s, text=""):
    if any("\u0d00" <= ch <= "\u0d7f" for ch in text): return ImageFont.truetype(_ML, int(s * 1.05), layout_engine=ImageFont.Layout.RAQM)
    return ImageFont.truetype(I + {"k": "Inter-Black", "b": "Inter-Bold", "s": "Inter-SemiBold", "r": "Inter-Regular"}[w] + ".otf", int(s))
W, H = 2560, 1440  # draw at 2x, downscale

ap = argparse.ArgumentParser(); ap.add_argument("out"); ap.add_argument("--big", default="−47%"); ap.add_argument("--top", default="NVIDIA")
ap.add_argument("--sub", default="IS THE AI BUBBLE BURSTING?"); ap.add_argument("--trend", default="down"); ap.add_argument("--start", type=float, default=239)
ap.add_argument("--end", type=float, default=125); ap.add_argument("--tag", default=""); ap.add_argument("--chip", default="AI"); ap.add_argument("--seed", type=int, default=7); ap.add_argument("--prop", default="chip")
a = ap.parse_args()
down = a.trend == "down"; ACC = (235, 60, 60) if down else (40, 200, 120)

# background: deep navy with vignette and screen glow
img = Image.new("RGB", (W, H), (6, 8, 14)); d = ImageDraw.Draw(img)
for y in range(H):
    p = y / H; d.line([(0, y), (W, y)], fill=(int(8 + 10 * p), int(10 + 8 * p), int(18 + 14 * p)))
glow = Image.new("L", (W, H), 0); ImageDraw.Draw(glow).ellipse([W * .38, -H * .2, W * 1.25, H * 1.0], fill=120)
img.paste(tuple(int(c * .55) for c in ACC), (0, 0), glow.filter(ImageFilter.GaussianBlur(260)))

# grid like a trading terminal
grid = Image.new("RGBA", (W, H), (0, 0, 0, 0)); g = ImageDraw.Draw(grid)
for x in range(0, W, 120): g.line([(x, 0), (x, H)], fill=(120, 140, 170, 22), width=2)
for y in range(0, H, 120): g.line([(0, y), (W, y)], fill=(120, 140, 170, 22), width=2)
img.paste(grid, (0, 0), grid)

# realistic candlestick chart on the right
rnd = random.Random(a.seed); n = 32; x0, x1, ytop, ybot = 1000, 2480, 230, 1180
lo_v, hi_v = min(a.start, a.end) * 0.9, max(a.start, a.end) * 1.06
def Y(v): return ybot - (v - lo_v) / (hi_v - lo_v) * (ybot - ytop)
price = a.start; closes = []
for i in range(n):
    target = a.start + (a.end - a.start) * (i / (n - 1)) ** 1.35
    o = price; c = target + rnd.gauss(0, (hi_v - lo_v) * 0.018)
    if i == n - 1: c = a.end
    hi = max(o, c) + abs(rnd.gauss(0, (hi_v - lo_v) * 0.012)); lo = min(o, c) - abs(rnd.gauss(0, (hi_v - lo_v) * 0.012))
    closes.append((o, hi, lo, c)); price = c
ch = Image.new("RGBA", (W, H), (0, 0, 0, 0)); cd = ImageDraw.Draw(ch); bw = (x1 - x0) / n
for i, (o, hi, lo, c) in enumerate(closes):
    x = x0 + bw * (i + .5); up = c >= o; col = (40, 200, 120, 255) if up else (235, 60, 60, 255)
    cd.line([(x, Y(hi)), (x, Y(lo))], fill=col, width=4)
    cd.rectangle([x - bw * .32, Y(max(o, c)), x + bw * .32, Y(min(o, c)) + 3], fill=col)
# moving-average line
ma = [];
for i in range(n): w = closes[max(0, i - 6):i + 1]; ma.append(sum(c for *_, c in w) / len(w))
cd.line([(x0 + bw * (i + .5), Y(v)) for i, v in enumerate(ma)], fill=(255, 200, 60, 230), width=7, joint="curve")
gl = ch.filter(ImageFilter.GaussianBlur(14)); img.paste(gl, (0, 0), gl); img.paste(ch, (0, 0), ch)
# fade chart into the left text area
fade = Image.new("L", (W, H), 0); fd = ImageDraw.Draw(fade)
for x in range(W): fd.line([(x, 0), (x, H)], fill=int(255 * max(0, min(1, (x - 900) / 500)) * 0 + 255 * max(0, min(1, (1500 - x) / 600))))
shade = Image.new("RGB", (W, H), (6, 8, 14)); img = Image.composite(shade, img, fade.point(lambda v: int(v * .78))); d = ImageDraw.Draw(img)

# metallic chip with glow (bottom-right), or gold bars
cx, cy, s = 2160, 1030, 1.6
if a.prop == "gold":
    gb = Image.new("RGBA", (W, H), (0, 0, 0, 0)); g2 = ImageDraw.Draw(gb)
    for (dx, dy) in [(-260, 80), (0, 80), (260, 80), (-130, -60), (130, -60)]:
        x, y = cx + dx - 60, cy + dy - 40; w, h, tp = 250, 110, 170
        g2.polygon([(x - w/2, y + h/2), (x + w/2, y + h/2), (x + tp/2, y - h/2), (x - tp/2, y - h/2)], fill=(232, 182, 52, 255))
        g2.polygon([(x - tp/2, y - h/2), (x + tp/2, y - h/2), (x + tp/2 - 16, y - h/2 + 22), (x - tp/2 + 16, y - h/2 + 22)], fill=(255, 222, 120, 255))
        g2.polygon([(x + tp/2, y - h/2), (x + w/2, y + h/2), (x + w/2 - 26, y + h/2), (x + tp/2 - 16, y - h/2 + 22)], fill=(170, 120, 20, 255))
    gg = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(gg).ellipse([cx - 520, cy - 300, cx + 400, cy + 260], fill=(255, 190, 60, 120))
    gg = gg.filter(ImageFilter.GaussianBlur(90)); img.paste(gg, (0, 0), gg); img.paste(gb, (0, 0), gb); d = ImageDraw.Draw(img)
chip = Image.new("RGBA", (W, H), (0, 0, 0, 0)); c2 = ImageDraw.Draw(chip)
if a.prop == "gold": cx = -9999
chip = Image.new("RGBA", (W, H), (0, 0, 0, 0)); c2 = ImageDraw.Draw(chip)
for k in range(7):
    o = -150 + k * 50
    for (xa, ya, xb, yb) in [(cx + o, cy - 210, cx + o, cy - 160), (cx + o, cy + 160, cx + o, cy + 210), (cx - 210, cy + o, cx - 160, cy + o), (cx + 160, cy + o, cx + 210, cy + o)]:
        c2.line([(xa, ya), (xb, yb)], fill=(200, 170, 90, 255), width=14)
c2.rounded_rectangle([cx - 165, cy - 165, cx + 165, cy + 165], 26, fill=(28, 30, 36, 255), outline=(120, 125, 135, 255), width=6)
for r in range(110, 0, -4):  # brushed metal die
    t = r / 110; c2.rounded_rectangle([cx - r, cy - r, cx + r, cy + r], 14, fill=(int(150 + 80 * (1 - t)), int(150 + 75 * (1 - t)), int(160 + 70 * (1 - t)), 255))
c2.text((cx, cy), a.chip, font=F("k", 110), fill=(20, 22, 28, 255), anchor="mm")
cg = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(cg).rounded_rectangle([cx - 230, cy - 230, cx + 230, cy + 230], 60, fill=ACC + (150,))
cg = cg.filter(ImageFilter.GaussianBlur(70)); img.paste(cg, (0, 0), cg); img.paste(chip, (0, 0), chip); d = ImageDraw.Draw(img)

# typography
def stroked(xy, text, font, fill, sw=10, anchor="ls"):
    d.text(xy, text, font=font, fill=fill, anchor=anchor, stroke_width=sw, stroke_fill=(0, 0, 0))
if a.tag:
    f = F("k", 58, a.tag); tw = d.textlength(a.tag, font=f); d.rounded_rectangle([110, 120, 110 + tw + 70, 210], 14, fill=ACC); d.text((145, 166), a.tag, font=f, fill=(255, 255, 255), anchor="lm")
ML_TOP = any("\u0d00" <= ch <= "\u0d7f" for ch in a.top); OFF_Y = 80 if ML_TOP else 0
tsz = 230
while d.textlength(a.top, font=F("k", tsz, a.top)) > 2380 and tsz > 120: tsz -= 6
stroked((100, 430), a.top, F("k", tsz, a.top), (255, 255, 255))
size = 470
while d.textlength(a.big, font=F("k", size)) > 1250: size -= 10
# big number with glow
gtxt = Image.new("L", (W, H), 0); ImageDraw.Draw(gtxt).text((90, 430 + OFF_Y + size * 0.92), a.big, font=F("k", size), fill=255, anchor="ls")
img.paste(ACC, (0, 0), gtxt.filter(ImageFilter.GaussianBlur(40)).point(lambda v: int(v * .8))); d = ImageDraw.Draw(img)
stroked((90, 430 + OFF_Y + size * 0.92), a.big, F("k", size), ACC, 12)
sub = a.sub; fs = 96
while d.textlength(sub, font=F("k", fs, sub)) > 1500 and fs > 50: fs -= 4
yb = 430 + OFF_Y + size * 0.92 + 150
tw = d.textlength(sub, font=F("k", fs, sub)); d.rounded_rectangle([90, yb - fs - 26, 90 + tw + 60, yb + 34], 18, fill=(255, 205, 40))
d.text((120, yb + (8 if sub != sub.encode("ascii","ignore").decode() else 0)), sub, font=F("k", fs, sub), fill=(12, 12, 16), anchor="ls", stroke_width=2, stroke_fill=(12, 12, 16))
d.text((W - 70, H - 50), "calcsouq.com", font=F("b", 44), fill=(200, 205, 215), anchor="rs")
img.resize((1280, 720), Image.LANCZOS).convert("RGB").save(a.out, quality=92); print(a.out)
