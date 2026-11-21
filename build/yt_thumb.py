"""YouTube thumbnail (1280x720) for CalcSouq long videos: big 2-line headline, one highlight word, mascot + a prop.
Usage: python3 yt_thumb.py out.png "LINE ONE" "LINE TWO" --hl WORD --tag "small top tag" --theme night --mood shocked --prop up|bank|oil|house|coins|chart|none
Rules: max ~4 words per line, readable on a phone, no clickbait claims the video does not back up.
"""
import sys, os, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reel_fx as fx
fx.W, fx.H = 1920, 1080
import yt_long_rates as Y
from PIL import ImageDraw
from reel_fx import F, GOLD, WHITE, INK, RED, GREEN

ap = argparse.ArgumentParser(); ap.add_argument("out"); ap.add_argument("l1"); ap.add_argument("l2")
ap.add_argument("--hl", default=""); ap.add_argument("--tag", default=""); ap.add_argument("--theme", default="night")
ap.add_argument("--mood", default="shocked"); ap.add_argument("--prop", default="up"); ap.add_argument("--stat", default="")
a = ap.parse_args()
img = fx.scene_bg(1.3, a.theme, 7); d = ImageDraw.Draw(img)
y = 300
for line in (a.l1, a.l2):
    size = 190
    while d.textlength(line, font=F("k", size)) > 1150: size -= 6
    x = 90
    for w in line.split(" "):
        col = GOLD if a.hl and w.strip(",.?!").upper() == a.hl.upper() else WHITE
        for dx, dy in ((8, 8), (6, 6)): d.text((x + dx, y + dy), w, font=F("k", size), fill=INK, anchor="ls")
        d.text((x, y), w, font=F("k", size), fill=col, anchor="ls"); x += d.textlength(w + " ", font=F("k", size))
    y += size + 40
if a.tag:
    f = F("k", 54); tw = d.textlength(a.tag, font=f); d.rounded_rectangle([90, 70, 90 + tw + 60, 150], 40, fill=RED); d.text((120, 110), a.tag, font=f, fill=WHITE, anchor="lm")
if a.stat:
    f = F("k", 80); tw = d.textlength(a.stat, font=f); d.rounded_rectangle([90, y - 40, 90 + tw + 80, y + 90], 30, fill=WHITE, outline=INK, width=8); d.text((130, y + 25), a.stat, font=f, fill=RED, anchor="lm")
fx.souq(img, 1560, 640, 1.25, 0.2, a.mood)
d = ImageDraw.Draw(img)
if a.prop == "up": Y.up_arrow(d, 1800, 300, 2.0, RED)
elif a.prop == "bank": Y.bank(img, 1760, 330, 0.8, 1)
elif a.prop == "oil": Y.barrel(img, 1790, 330, 1.0, 1)
elif a.prop == "house": Y.house(img, 1790, 330, 1.0, 1)
elif a.prop == "coins": fx.coins_stack(d, 1800, 420, 6, 70, "$")
elif a.prop == "chart": fx.chart_up(d, 1640, 150, 260, 260, 1, GREEN)
d = ImageDraw.Draw(img); d.rounded_rectangle([90, 930, 470, 1010], 40, fill=GOLD); d.text((280, 970), "calcsouq.com", font=F("k", 46), fill=INK, anchor="mm")
img.convert("RGB").resize((1280, 720)).save(a.out, quality=92); print(a.out)
