"""Thumbnail for the onion-inflation Malayalam video (2560x1440 -> saved 1280x720 JPEG).
Usage: python3 yt_thumb_onion.py out.jpg"""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import yt_long_onion_ml as O
HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 2560, 1440
def MF(s): return ImageFont.truetype(os.path.join(HERE, "fonts/Manjari-Bold.ttf"), s, layout_engine=ImageFont.Layout.RAQM)
def IF(s): return O.F("k", s)

import numpy as np
def onion3d(img, cx, cy, r, rot=0, dim=0.0):
    """smooth radial-shaded red onion: skin veins, papery neck, soft highlight"""
    S = int(r * 2.8); yy, xx = np.mgrid[0:S, 0:S].astype(float); c = S / 2
    nx = (xx - c) / r; ny = (yy - c - r * 0.12) / (r * 0.92)
    nx = nx / (1 - 0.42 * np.clip(-ny, 0, 1) ** 1.6); rr = np.sqrt(nx ** 2 + ny ** 2); inside = rr <= 1
    nz = np.sqrt(np.clip(1 - rr ** 2, 0, 1)); lx, ly, lz = -0.45, -0.55, 0.7
    diff = np.clip(nx * lx + ny * ly + nz * lz, 0, 1)
    base = np.array([170, 34, 84.]); light = np.array([236, 128, 172.]); deep = np.array([60, 8, 30.])
    col = deep[None, None] * (1 - diff[..., None]) + base[None, None] * diff[..., None]
    col = col + (light - base)[None, None] * (diff ** 6)[..., None]
    veins = 0.5 + 0.5 * np.cos(np.arctan2(nx, np.maximum(nz, 1e-3)) * 14)
    col = col * (0.84 + 0.16 * veins[..., None])
    a = (np.clip((1 - rr) * r * 0.6, 0, 1) * 255) * inside
    lay = Image.fromarray(np.dstack([np.clip(col * (1 - dim), 0, 255), a]).astype("uint8"), "RGBA")
    d2 = ImageDraw.Draw(lay)
    d2.polygon([(c - r * .09, c - r * .66), (c + r * .09, c - r * .66), (c + r * .03, c - r * 1.15), (c - r * .05, c - r * 1.12)], fill=(176, 130, 80, 255))
    for k in range(7): d2.line([(c, c + r * 1.0), (c - r * .18 + k * r * .06, c + r * 1.14)], fill=(214, 196, 160, 255), width=max(2, int(r * .015)))
    hl = Image.new("L", lay.size, 0); ImageDraw.Draw(hl).ellipse([c - r * .62, c - r * .55, c - r * .22, c - r * .05], fill=110)
    lay.paste((255, 225, 240), (0, 0), Image.composite(hl.filter(ImageFilter.GaussianBlur(r * .08)), Image.new("L", lay.size, 0), lay.split()[3]))
    if rot: lay = lay.rotate(rot, resample=Image.BICUBIC)
    sh = Image.new("L", img.size, 0); ImageDraw.Draw(sh).ellipse([cx - r * .9, cy + r * .82, cx + r * .9, cy + r * 1.12], fill=170)
    img.paste((0, 0, 0), (0, 0), sh.filter(ImageFilter.GaussianBlur(r * .12)))
    img.paste(lay, (int(cx - c), int(cy - c)), lay)

img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
for y in range(H): p = y / H; d.line([(0, y), (W, y)], fill=(int(28 - 16 * p), int(8 + 4 * p), int(20 + 6 * p)))
glow = Image.new("L", (W, H), 0); ImageDraw.Draw(glow).ellipse([1300, 100, 2700, 1500], fill=150)
img.paste((200, 40, 90), (0, 0), glow.filter(ImageFilter.GaussianBlur(260)))
# pile of onions on the right
onion3d(img, 1640, 1080, 260, 12, 0.25); onion3d(img, 2400, 1060, 280, -10, 0.25)
onion3d(img, 1990, 760, 470, -6)
d = ImageDraw.Draw(img)
# price tag on hero
tg = [(2140, 200), (2480, 200), (2480, 430), (2140, 430), (2080, 315)]
d.polygon(tg, fill=(230, 40, 40)); d.ellipse([2110, 302, 2136, 328], fill=(28, 8, 20))
d.text((2310, 280), "+116%", font=IF(110), fill=(255, 255, 255), anchor="mm"); d.text((2310, 375), "1 YEAR", font=IF(46), fill=(255, 220, 220), anchor="mm")
# left text panel
dark = Image.new("L", (W, H), 0); ImageDraw.Draw(dark).rectangle([0, 0, 1500, H], fill=170)
img.paste((6, 4, 10), (0, 0), dark.filter(ImageFilter.GaussianBlur(160))); d = ImageDraw.Draw(img)
def fit(text, font_fn, maxw, start):
    s = start
    while d.textlength(text, font=font_fn(s)) > maxw and s > 40: s -= 6
    return font_fn(s)
l1 = "ഉള്ളി വില"; l2 = "ഇരട്ടിയായി!"
for dx, dy in ((8, 8),): d.text((110 + dx, 330 + dy), l1, font=fit(l1, MF, 1350, 230), fill=(0, 0, 0))
d.text((110, 330), l1, font=fit(l1, MF, 1350, 230), fill=(255, 255, 255))
d.text((118, 618), l2, font=fit(l2, MF, 1400, 250), fill=(0, 0, 0)); d.text((110, 610), l2, font=fit(l2, MF, 1400, 250), fill=(255, 205, 60))
st = "അടുക്കള ബിൽ മാസം +₹140?"
f = fit(st, MF, 1250, 96); tw = d.textlength(st, font=f)
d.rounded_rectangle([100, 1000, 100 + tw + 90, 1180], 40, fill=(230, 40, 40)); d.text((145, 1095), st, font=f, fill=(255, 255, 255), anchor="lm")
d.rounded_rectangle([100, 1230, 700, 1320], 30, fill=(245, 195, 0)); d.text((400, 1275), "ONION PRICE SHOCK", font=IF(48), fill=(20, 16, 10), anchor="mm")
img.resize((1280, 720), Image.LANCZOS).save(sys.argv[1] if len(sys.argv) > 1 else "thumb.jpg", quality=92)
