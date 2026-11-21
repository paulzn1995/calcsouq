"""Two Instagram Stories for 2026-11-21 (1080x1920 JPEG)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_fx import *
from reels_2026_11_21 import options, small
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static/media/ig/")
T = 5.0  # all animations finished

im = scene_bg(1.0, "gold", 51); d = ImageDraw.Draw(im)
pill(im, W / 2, 330, "QUIZ", T, 0, INK, GOLD, 50)
kinetic(im, "₹1 lakh of gold.", 500, T, 0, 110, INK)
kinetic(im, "What's the bill?", 620, T, 0, 88, (150, 40, 40))
small(im, "22K jewellery · making 12% · GST 3% (India)", 690, INK, 36)
options(im, T, 0, ["A  ₹1,03,000", "B  ₹1,08,000", "C  ₹1,15,360"], 820, 125)
gold_bar(d, 220, 1400, 0.9)
souq(im, 640, 1390, 0.6, 2.0, "thinking"); speech(im, 700, 1245, "Answer in today's reel", 0, T, 38)
pill(im, W / 2, 1640, "calcsouq.com", T, 0, INK, GOLD, 60, 60)
im.save(OUT + "2026-11-21-story-gold-quiz.jpg", quality=92)

im = scene_bg(1.0, "berry", 53); rays(im, W / 2, 760, 1.0, GOLD, 26); d = ImageDraw.Draw(im)
kinetic(im, "Start a SIP at 25,", 440, T, 0, 92, WHITE)
kinetic(im, "not 30, and you end", 550, T, 0, 80, WHITE)
kinetic(im, "with an extra", 650, T, 0, 80, WHITE)
d.text((W / 2, 800), "₹1.48 crore", font=F("k", 150), fill=GOLD, anchor="mm")
pill(im, W / 2, 960, "for only ₹3 lakh more invested", T, 0, GREEN, WHITE, 44)
small(im, "₹5,000 a month till 60 · assumes 12% a year · not advice", 1050, (255, 200, 230), 32)
rocket(im, 820, 1360, 0.6, 1.0)
souq(im, 380, 1390, 0.6, 1.0, "shocked"); speech(im, 440, 1245, "5 years = ₹1.48 crore?!", 0, T, 38)
pill(im, W / 2, 1640, "calcsouq.com", T, 0, GOLD, INK, 60, 60)
im.save(OUT + "2026-11-21-story-sip-gap.jpg", quality=92)
