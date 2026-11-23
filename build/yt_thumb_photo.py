"""Photo-based YouTube thumbnail (1280x720): a real-looking photo (AI-generated scene, no people/logos) with bold Malayalam/English type.
Use a different accent colour per video so thumbnails don't all look the same.
Usage: python3 yt_thumb_photo.py bg.jpg out.jpg --l1 "ഹോം ലോൺ EMI" --l2 "വീണ്ടും കൂടുമോ?" --big "+₹1,382" --unit "/ മാസം"
       --sub "₹30 ലക്ഷം ലോൺ · റിപ്പോ 6% ആയാൽ" --tag "RBI · DEC 4" --acc "#FFD23F" --tagbg "#18B39A" [--focus 0.62]
"""
import argparse, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
ML = os.path.join(HERE, "fonts/Manjari-Bold.ttf"); INTER = "/usr/share/fonts/opentype/inter/"
def isml(s): return any("ഀ" <= c <= "ൿ" for c in s)
def F(s, text="", w="k"):
    if isml(text): return ImageFont.truetype(ML, int(s * 1.08), layout_engine=ImageFont.Layout.RAQM)
    return ImageFont.truetype(INTER + {"k": "Inter-Black", "b": "Inter-Bold", "s": "Inter-SemiBold"}[w] + ".otf", int(s))
def hexc(h): h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

ap = argparse.ArgumentParser(); ap.add_argument("bg"); ap.add_argument("out")
for k, v in [("l1", ""), ("l2", ""), ("big", ""), ("unit", ""), ("sub", ""), ("tag", ""), ("acc", "#FFD23F"), ("tagbg", "#18B39A"), ("focus", "0.6"), ("shift", "0"), ("numcol", "acc")]:
    ap.add_argument("--" + k, default=v)
a = ap.parse_args(); ACC = hexc(a.acc); TAGBG = hexc(a.tagbg)
W, H = 2560, 1440  # draw at 2x, downscale at the end

# photo: cover-fit, gentle contrast/colour lift and sharpening
ph = Image.open(a.bg).convert("RGB"); sc = max(W / ph.width, H / ph.height)
ph = ph.resize((int(ph.width * sc), int(ph.height * sc)), Image.LANCZOS)
x0 = int((ph.width - W) * float(a.focus)); ph = ph.crop((x0, (ph.height - H) // 2, x0 + W, (ph.height - H) // 2 + H))
sh_ = int(W * float(a.shift))
if sh_ > 0:  # slide the photo right; fill the left with a soft, blurred stretch of its own edge
    base = ph.crop((0, 0, 40, H)).resize((sh_ + 40, H)).filter(ImageFilter.GaussianBlur(30))
    canvas = Image.new("RGB", (W, H)); canvas.paste(base, (0, 0)); canvas.paste(ph.crop((0, 0, W - sh_, H)), (sh_, 0))
    edge = Image.linear_gradient("L").rotate(90).resize((160, H)); canvas.paste(base.crop((0, 0, 160, H)), (sh_, 0), edge)
    ph = canvas
ph = ImageEnhance.Contrast(ph).enhance(1.08); ph = ImageEnhance.Color(ph).enhance(1.12)
ph = ph.filter(ImageFilter.UnsharpMask(radius=3, percent=90, threshold=2))
img = ph.convert("RGBA")

# left-side deep navy gradient for legibility, plus a soft bottom vignette
grad = Image.new("RGBA", (W, H), (0, 0, 0, 0)); g = ImageDraw.Draw(grad)
for x in range(W):
    f = max(0.0, 1 - x / (W * 0.66)); g.line([(x, 0), (x, H)], fill=(8, 16, 34, int(240 * f ** 1.1)))
img.alpha_composite(grad)
vig = Image.new("RGBA", (W, H), (0, 0, 0, 0)); v = ImageDraw.Draw(vig)
for y in range(H):
    f = max(0.0, (y - H * 0.7) / (H * 0.3)); v.line([(0, y), (W, y)], fill=(5, 10, 22, int(150 * f)))
img.alpha_composite(vig); d = ImageDraw.Draw(img)

def shadow_text(xy, text, font, fill, sw=8, glow=None, anchor="ls"):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    ld.text((xy[0] + 6, xy[1] + 10), text, font=font, fill=(0, 0, 0, 170), anchor=anchor)
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(10)))
    if glow:
        gl = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(gl).text(xy, text, font=font, fill=glow + (150,), anchor=anchor)
        img.alpha_composite(gl.filter(ImageFilter.GaussianBlur(34)))
    ImageDraw.Draw(img).text(xy, text, font=font, fill=fill, anchor=anchor, stroke_width=sw, stroke_fill=(6, 12, 26))

L = 110; MAXW = 1450
y = 120
if a.tag:  # small pill top-left
    f = F(54, a.tag); tw = d.textlength(a.tag, font=f)
    d.rounded_rectangle([L, y, L + tw + 76, y + 96], 48, fill=TAGBG); d.text((L + 38, y + 50), a.tag, font=f, fill=(255, 255, 255), anchor="lm"); y += 96 + 40
def fit(text, size, maxw):
    while ImageDraw.Draw(img).textlength(text, font=F(size, text)) > maxw and size > 60: size -= 4
    return F(size, text)
if a.l1:
    f = fit(a.l1, 150, MAXW); y += 150; shadow_text((L, y), a.l1, f, (255, 255, 255)); y += 30
if a.l2:
    f = fit(a.l2, 170, MAXW); y += 175; shadow_text((L, y), a.l2, f, (255, 255, 255) if a.numcol == "acc" else ACC); y += 40
if a.big:
    f = fit(a.big, 300, 1150); y += 300
    shadow_text((L - 6, y), a.big, f, ACC if a.numcol == "acc" else (255, 255, 255), sw=14, glow=ACC)
    if a.unit:
        bw = ImageDraw.Draw(img).textlength(a.big, font=f); shadow_text((L + bw + 30, y - 10), a.unit, F(96, a.unit), (255, 255, 255), sw=6)
    y += 40
if a.sub:
    f = fit(a.sub, 78, 1500); tw = ImageDraw.Draw(img).textlength(a.sub, font=f)
    y += 40; box = [L, y, L + tw + 80, y + 128]
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([box[0] + 6, box[1] + 12, box[2] + 6, box[3] + 12], 30, fill=(0, 0, 0, 140))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12))); d = ImageDraw.Draw(img)
    d.rounded_rectangle(box, 30, fill=(255, 255, 255)); d.rounded_rectangle([box[0], box[1], box[0] + 18, box[3]], 9, fill=ACC)
    d.text((L + 48, y + 72 + (6 if isml(a.sub) else 0)), a.sub, font=f, fill=(10, 18, 36), anchor="lm")
d = ImageDraw.Draw(img); d.text((W - 60, H - 48), "calcsouq.com", font=F(46, "", "b"), fill=(235, 238, 245), anchor="rs", stroke_width=3, stroke_fill=(0, 0, 0))
img.convert("RGB").resize((1280, 720), Image.LANCZOS).save(a.out, quality=93); print(a.out)
