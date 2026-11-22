"""High-contrast thumbnail for the Malayalam Hormuz video: burning tanker at night + huge text.
Usage: python3 yt_thumb_hormuz.py out.jpg
"""
import sys, os, math, random
from PIL import Image, ImageDraw, ImageFilter, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from reel_fx import F
W, H = 2560, 1440
def MF(s): return ImageFont.truetype(os.path.join(HERE, "fonts/Manjari-Bold.ttf"), int(s), layout_engine=ImageFont.Layout.RAQM)
rnd = random.Random(11)

img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
for y in range(H):  # night sky to dark sea
    p = y / H
    col = (int(8 + 20 * p), int(10 + 14 * p), int(26 + 30 * p)) if y < 820 else (int(6 + 8 * p), int(14 + 18 * p), int(30 + 36 * p))
    d.line([(0, y), (W, y)], fill=col)
# fire glow on the horizon (right)
glow = Image.new("L", (W, H), 0); ImageDraw.Draw(glow).ellipse([1300, 200, 2900, 1300], fill=255)
img.paste((255, 90, 20), (0, 0), glow.filter(ImageFilter.GaussianBlur(260)).point(lambda v: int(v * .75)))
glow2 = Image.new("L", (W, H), 0); ImageDraw.Draw(glow2).ellipse([1600, 380, 2500, 1000], fill=255)
img.paste((255, 170, 40), (0, 0), glow2.filter(ImageFilter.GaussianBlur(160)).point(lambda v: int(v * .55)))
# sea shimmer
sea = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sea)
for k in range(260):
    y = 860 + rnd.random() * 580; x = 1100 + rnd.random() * 1460; w = 30 + rnd.random() * 140
    a = int(40 + 120 * max(0, 1 - abs(x - 2000) / 900))
    sd.line([(x, y), (x + w, y)], fill=(255, 150, 60, a), width=3)
img.paste(sea, (0, 0), sea)

# smoke plume
sm = Image.new("RGBA", (W, H), (0, 0, 0, 0)); g = ImageDraw.Draw(sm)
for k in range(40):
    t = k / 40; x = 2100 - 520 * t + rnd.gauss(0, 30); y = 640 - 620 * t; r = 90 + 260 * t
    g.ellipse([x - r, y - r, x + r, y + r], fill=(22, 20, 24, int(230 - 120 * t)))
img.paste(sm.filter(ImageFilter.GaussianBlur(40)), (0, 0), sm.filter(ImageFilter.GaussianBlur(40)))

# tanker (large, slightly angled perspective)
tk = Image.new("RGBA", (W, H), (0, 0, 0, 0)); t2 = ImageDraw.Draw(tk)
hull = [(1300, 820), (2480, 760), (2560, 800), (2460, 930), (1380, 960)]
t2.polygon(hull, fill=(22, 24, 30, 255))
t2.polygon([(1380, 960), (2460, 930), (2440, 960), (1400, 990)], fill=(120, 20, 20, 255))
t2.line([(1300, 820), (2480, 760)], fill=(90, 95, 110, 255), width=6)
t2.polygon([(1380, 700), (1560, 690), (1560, 818), (1380, 826)], fill=(40, 44, 54, 255))  # bridge
for i in range(4): t2.rectangle([1400 + i * 40, 715, 1424 + i * 40, 735], fill=(255, 200, 120, 255))
for i in range(6): t2.rectangle([1640 + i * 130, 790 - i * 6, 1700 + i * 130, 808 - i * 6], fill=(50, 54, 64, 255))
img.paste(tk, (0, 0), tk)
# reflection
rf = tk.transpose(Image.FLIP_TOP_BOTTOM).crop((0, H - 1000, W, H - 1000 + 440))
rfl = Image.new("RGBA", (W, H), (0, 0, 0, 0)); rfl.paste(rf, (0, 960)); a = rfl.split()[3].point(lambda v: int(v * .25))
img.paste(rfl.convert("RGB").filter(ImageFilter.GaussianBlur(6)), (0, 0), a.filter(ImageFilter.GaussianBlur(6)))

# fire on deck (organic, layered blurred blobs)
for layer, (blur, cols, n, spread, hmax) in enumerate([(28, [(255, 80, 10)], 70, 170, 420), (14, [(255, 140, 30), (255, 110, 20)], 90, 130, 330), (6, [(255, 210, 90), (255, 240, 170)], 70, 90, 220)]):
    fire = Image.new("RGBA", (W, H), (0, 0, 0, 0)); f2 = ImageDraw.Draw(fire)
    for k in range(n):
        x = 2080 + rnd.gauss(0, spread); hh = abs(rnd.gauss(0, hmax)); y = 790 - hh * rnd.random(); r = 26 + (1 - hh / (hmax * 2.5)) * 60 * rnd.random() + 10
        f2.ellipse([x - r * .7, y - r, x + r * .7, y + r], fill=rnd.choice(cols) + (170,))
    fb_ = fire.filter(ImageFilter.GaussianBlur(blur)); img.paste(fb_, (0, 0), fb_)
fg = fire.filter(ImageFilter.GaussianBlur(90)); img.paste(fg, (0, 0), fg)
core = Image.new("RGBA", (W, H), (0, 0, 0, 0)); cd_ = ImageDraw.Draw(core)
cd_.ellipse([1900, 600, 2260, 820], fill=(255, 230, 120, 230)); cd_.ellipse([1980, 660, 2180, 800], fill=(255, 250, 220, 255))
for k in range(14):  # flame tongues
    x = 1920 + k * 26 + rnd.gauss(0, 10); hh = 160 + rnd.random() * 260
    cd_.polygon([(x - 30, 790), (x + 30, 790), (x + rnd.gauss(0, 25), 790 - hh)], fill=(255, 170, 40, 200))
cc = core.filter(ImageFilter.GaussianBlur(22)); img.paste(cc, (0, 0), cc)
for k in range(90):  # sparks
    x = 2080 + rnd.gauss(0, 260); y = 760 - abs(rnd.gauss(0, 260)); r = 2 + rnd.random() * 4
    ImageDraw.Draw(img).ellipse([x - r, y - r, x + r, y + r], fill=(255, 210, 120))

# left dark gradient for text
sh = Image.new("L", (W, H), 0); s2 = ImageDraw.Draw(sh)
for x in range(W): s2.line([(x, 0), (x, H)], fill=int(235 * max(0, min(1, (1350 - x) / 800))))
img = Image.composite(Image.new("RGB", (W, H), (4, 6, 12)), img, sh); d = ImageDraw.Draw(img)

def stroked(xy, text, font, fill, sw=14, anchor="ls", sc=(0, 0, 0)):
    d.text(xy, text, font=font, fill=fill, anchor=anchor, stroke_width=sw, stroke_fill=sc)

# tag
f = F("k", 64); tw = d.textlength("HORMUZ · OIL WAR", font=f)
d.rounded_rectangle([110, 110, 110 + tw + 80, 214], 18, fill=(230, 30, 30)); d.text((150, 163), "HORMUZ · OIL WAR", font=f, fill=(255, 255, 255), anchor="lm")
# line 1 Malayalam
stroked((100, 470), "ഈ കടൽ അടഞ്ഞാൽ?", MF(200), (255, 255, 255), 14)
# huge number with glow
big = "39 KM"; fb = F("k", 460)
gl = Image.new("L", (W, H), 0); ImageDraw.Draw(gl).text((90, 960), big, font=fb, fill=255, anchor="ls")
img.paste((255, 200, 0), (0, 0), gl.filter(ImageFilter.GaussianBlur(40)).point(lambda v: int(v * .55))); d = ImageDraw.Draw(img)
stroked((90, 960), big, fb, (255, 214, 0), 18)
# bottom strip
fs = MF(92); txt = "പെട്രോൾ · ഗ്യാസ് · EMI കൂടുമോ?"; tw = d.textlength(txt, font=fs)
d.rounded_rectangle([100, 1050, 100 + tw + 90, 1210], 26, fill=(230, 30, 30))
d.text((145, 1145), txt, font=fs, fill=(255, 255, 255), anchor="lm")
d.text((W - 60, H - 50), "calcsouq.com", font=F("b", 44), fill=(235, 235, 240), anchor="rs")

out = img.resize((1280, 720), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.2, 60, 2))
out.save(sys.argv[1] if len(sys.argv) > 1 else "/tmp/thumb.jpg", quality=94); print("ok")
