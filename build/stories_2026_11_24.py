"""Two Instagram Stories for 2026-11-24 (1080x1920 JPEG). Figures: see build/reels_2026_11_24.py."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_fx import *
from reels_2026_11_21 import options, small
from reels_2026_11_24 import strip
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static/media/ig/")
T = 5.0

im = scene_bg(1.0, "night", 171); d = ImageDraw.Draw(im)
pill(im, W / 2, 330, "QUIZ", T, 0, GOLD, INK, 50)
kinetic(im, "You turn", 470, T, 0, 96, WHITE)
d.text((W / 2, 590), "1,000,000,000", font=F("k", 112), fill=GOLD, anchor="mm")
kinetic(im, "seconds old at…?", 740, T, 0, 92, WHITE)
options(im, T, 0, ["A  21 years", "B  31 years 8 months", "C  41 years"], 860, 115)
calendar(d, 240, 1420, 0.85, "?")
souq(im, 690, 1420, 0.6, 2.0, "thinking"); speech(im, 720, 1290, "Answer in today's reel", 0, T, 40)
pill(im, W / 2, 1660, "calcsouq.com", T, 0, GOLD, INK, 60, 60)
im.convert("RGB").save(OUT + "2026-11-24-story-billion-seconds.jpg", quality=92)

im = scene_bg(1.0, "sunset", 173); rays(im, W / 2, 760, 1.0, WHITE, 22); d = ImageDraw.Draw(im)
kinetic(im, "UAE National Day:", 400, T, 0, 84, WHITE)
kinetic(im, "1 day of leave =", 510, T, 0, 92, WHITE)
d.text((W / 2, 660), "5 days off", font=F("k", 150), fill=GOLD, anchor="mm")
strip(im, T, 0, 900)
pill(im, W / 2, 1110, "Take Fri 4 Dec · off Wed 2 → Sun 6", T, 0, WHITE, INK, 44)
souq(im, 540, 1380, 0.55, 1.0, "cool"); speech(im, 600, 1250, "Book it early!", 0, T, 40)
pill(im, W / 2, 1660, "calcsouq.com", T, 0, GOLD, INK, 60, 60)
im.convert("RGB").save(OUT + "2026-11-24-story-national-day.jpg", quality=92)
