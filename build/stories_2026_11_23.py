"""Two Instagram Stories for 2026-11-23 (1080x1920 JPEG). Figures: see build/reels_2026_11_23.py."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_fx import *
from reels_2026_11_21 import options, small
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static/media/ig/")
T = 5.0

im = scene_bg(1.0, "berry", 161); d = ImageDraw.Draw(im)
pill(im, W / 2, 330, "QUIZ", T, 0, GOLD, INK, 50)
kinetic(im, "You turn 10,000", 500, T, 0, 100, WHITE, hl=["10,000"])
kinetic(im, "days old at…?", 615, T, 0, 100, WHITE)
options(im, T, 0, ["A  25 years", "B  27 years 4 months", "C  30 years"], 800, 125)
calendar(d, 240, 1370, 0.85, "?")
souq(im, 690, 1370, 0.6, 2.0, "thinking"); speech(im, 720, 1225, "Answer in today's reel", 0, T, 40)
pill(im, W / 2, 1660, "calcsouq.com", T, 0, GOLD, INK, 60, 60)
im.convert("RGB").save(OUT + "2026-11-23-story-10000-days.jpg", quality=92)

im = scene_bg(1.0, "night", 163); rays(im, W / 2, 700, 1.0, GOLD, 24); d = ImageDraw.Draw(im)
kinetic(im, "A loan at \"10% flat\"", 440, T, 0, 84, WHITE)
kinetic(im, "really costs about", 550, T, 0, 80, WHITE)
d.text((W / 2, 700), "17.9% a year", font=F("k", 140), fill=GOLD, anchor="mm")
pill(im, W / 2, 860, "Flat interest is on the full loan", T, 0, WHITE, INK, 46)
small(im, "₹1 lakh · 3 years · on the reducing balance", 950, (220, 225, 255), 44)
doc(d, 250, 1340, 0.75, "LOAN", RED)
souq(im, 700, 1370, 0.6, 1.0, "shocked"); speech(im, 730, 1225, "Check the real rate!", 0, T, 40)
pill(im, W / 2, 1660, "calcsouq.com", T, 0, GOLD, INK, 60, 60)
im.convert("RGB").save(OUT + "2026-11-23-story-flat-rate.jpg", quality=92)
