"""Two Instagram Stories for 2026-11-25 (1080x1920 JPEG). Figures: see build/reels_2026_11_25.py."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_fx import *
from reels_2026_11_21 import options, small
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static/media/ig/")
T = 5.0

im = scene_bg(1.0, "night", 181); d = ImageDraw.Draw(im)
pill(im, W / 2, 330, "QUIZ", T, 0, GOLD, INK, 50)
kinetic(im, "On 2 Dec the UAE turns", 470, T, 0, 72, WHITE)
d.text((W / 2, 610), "55", font=F("k", 200), fill=GOLD, anchor="mm")
kinetic(im, "How many days old?", 770, T, 0, 84, WHITE)
options(im, T, 0, ["A  12,045 days", "B  20,089 days", "C  55,000 days"], 890, 115)
calendar(d, 240, 1420, 0.85, "2")
souq(im, 690, 1420, 0.6, 2.0, "thinking"); speech(im, 720, 1290, "Answer in today's reel", 0, T, 40)
pill(im, W / 2, 1660, "calcsouq.com", T, 0, GOLD, INK, 60, 60)
im.convert("RGB").save(OUT + "2026-11-25-story-uae-55-quiz.jpg", quality=92)

im = scene_bg(1.0, "berry", 183); rays(im, W / 2, 700, 1.0, WHITE, 20); d = ImageDraw.Draw(im)
pill(im, W / 2, 330, "QUIZ", T, 0, GOLD, INK, 50)
kinetic(im, "5% raise, 6% inflation:", 470, T, 0, 76, WHITE)
d.text((W / 2, 620), "Raise or pay cut?", font=F("k", 100), fill=GOLD, anchor="mm")
options(im, T, 0, ["A  Small raise", "B  No change", "C  Pay cut"], 800, 115)
small(im, "Answer: today's reel", 1170, WHITE, 46)
piggy(im, 280, 1420, 0.6, 1.0)
souq(im, 740, 1420, 0.6, 2.0, "shocked"); speech(im, 760, 1290, "Check your raise!", 0, T, 40)
pill(im, W / 2, 1660, "calcsouq.com", T, 0, GOLD, INK, 60, 60)
im.convert("RGB").save(OUT + "2026-11-25-story-raise-vs-inflation.jpg", quality=92)
