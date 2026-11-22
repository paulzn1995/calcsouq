"""Two Instagram Stories for 2026-11-22 (1080x1920 JPEG). Figures: see build/reels_2026_11_22.py."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_fx import *
from reels_2026_11_21 import options, small
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static/media/ig/")
T = 5.0

im = scene_bg(1.0, "sunset", 61); d = ImageDraw.Draw(im)
pill(im, W / 2, 330, "QUIZ", T, 0, INK, GOLD, 50)
kinetic(im, "How many WORKING", 500, T, 0, 92, WHITE, hl=["WORKING"])
kinetic(im, "days are left in 2026?", 610, T, 0, 80, WHITE)
small(im, "Monday to Friday, from 23 Nov to 31 Dec", 690, WHITE, 36)
options(im, T, 0, ["A  52 days", "B  39 days", "C  29 days"], 820, 125)
calendar(d, 240, 1390, 0.85, "31")
souq(im, 690, 1390, 0.6, 2.0, "thinking"); speech(im, 720, 1245, "Answer in today's reel", 0, T, 38)
pill(im, W / 2, 1640, "calcsouq.com", T, 0, INK, GOLD, 60, 60)
im.convert("RGB").save(OUT + "2026-11-22-story-days-quiz.jpg", quality=92)

im = scene_bg(1.0, "mint", 63); rays(im, W / 2, 760, 1.0, GOLD, 24); d = ImageDraw.Draw(im)
kinetic(im, "₹1 lakh at 8% a year", 440, T, 0, 84, WHITE)
kinetic(im, "becomes", 550, T, 0, 80, WHITE)
d.text((W / 2, 700), "₹7.99 lakh", font=F("k", 150), fill=GOLD, anchor="mm")
pill(im, W / 2, 860, "in 27 years: it doubles 3 times", T, 0, WHITE, INK, 46)
small(im, "Rule of 72: 72 ÷ 8 = 9 years to double · assumed rate, before tax", 950, (180, 255, 220), 30)
rocket(im, 820, 1360, 0.6, 1.0)
souq(im, 380, 1390, 0.6, 1.0, "shocked"); speech(im, 440, 1245, "Only ₹1 lakh put in?!", 0, T, 38)
pill(im, W / 2, 1640, "calcsouq.com", T, 0, GOLD, INK, 60, 60)
im.convert("RGB").save(OUT + "2026-11-22-story-rule-of-72.jpg", quality=92)
