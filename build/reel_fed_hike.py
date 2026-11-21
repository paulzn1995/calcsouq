"""Reel: markets expect a Fed rate hike on 9 Dec 2026 — what +0.25% does to a $400,000 30-year mortgage.
Sources (checked 22 Nov 2026): Fed held 3.75–4.00% on 28 Oct 2026, two officials voted to hike; markets price
about a 76% chance of a 25 bp hike on 9 Dec (Norada Real Estate / CME FedWatch reporting, Nov 2026).
Numbers: standard amortisation, $400,000, 30 years, example rates 6.25% vs 6.50%.
"""
import os, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_fx import *

P, N = 400000, 360
def pay(r): i = r / 1200; return P * i / (1 - (1 + i) ** -N)
A1, A2 = pay(6.25), pay(6.50)
DM, DT = A2 - A1, (A2 - A1) * N            # ~$65/month, ~$23,545 over the loan
DUR = 14
MUTE = (170, 176, 190)

def row(im, y, label, val, t, t0, col=WHITE):
    p = back(seg(t, t0, t0 + .4))
    if p <= 0: return
    x0 = lerp(-900, 90, p); box = (x0, y - 70, x0 + 900, y + 70)
    shadow(im, box, 34, 20, 110, (0, 12)); d = ImageDraw.Draw(im)
    d.rounded_rectangle(box, 34, fill=(34, 38, 52))
    d.text((x0 + 40, y), label, font=F("b", 46), fill=WHITE, anchor="lm")
    d.text((x0 + 860, y), val, font=F("k", 60), fill=col, anchor="rm")

def frame(i):
    t = i / FPS
    if t < 3.6:
        im = scene_bg(t, "night", 61); rays(im, W / 2, 620, t, GOLD, 22); d = ImageDraw.Draw(im)
        pill(im, W / 2, 300, "BREAKING · US FED", t, 0.0, RED, WHITE, 40)
        kinetic(im, "Markets expect the Fed", 460, t, 0.15, 74, WHITE)
        kinetic(im, "to RAISE rates", 570, t, 0.5, 100, GOLD, hl=["RAISE"], hl_col=RED)
        kinetic(im, "on 9 December.", 680, t, 0.85, 74, WHITE)
        d.text((W / 2, 800), "What does +0.25% cost you?", font=F("b", 52), fill=mix((14, 16, 22), WHITE, ease(seg(t, 1.6, 2.1))), anchor="mm")
        souq(im, W / 2, 1300, 0.85, t, "shocked" if t > 1.4 else "thinking")
        speech(im, W / 2 + 200, 1060, "Guess first!", 2.0, t, 46)
        return punch(im, t, 0.05)
    if t < 8.6:
        im = scene_bg(t, "sky", 63); d = ImageDraw.Draw(im)
        kinetic(im, "$400,000 home loan · 30 years", 360, t, 3.65, 60, WHITE)
        row(im, 560, "At 6.25%", f"${count(0, A1, t, 4.0, 4.8):,.0f}/mo", t, 3.9)
        row(im, 740, "At 6.50%", f"${count(0, A2, t, 5.0, 5.8):,.0f}/mo", t, 4.9, GOLD)
        pill(im, W / 2, 920, f"+${DM:,.0f} every month", t, 6.1, RED, WHITE, 54)
        coins_stack(d, 160, 1500, int(2 + 7 * seg(t, 6.2, 7.6)), 44, "$"); coins_stack(d, 920, 1500, int(2 + 7 * seg(t, 6.2, 7.6)), 44, "$")
        souq(im, W / 2, 1380, 0.6, t, "thinking" if t < 6.2 else "shocked")
        d.text((W / 2, 1840), "Example rates · the Fed doesn't set mortgage rates directly", font=F("s", 30), fill=(225, 232, 255), anchor="mm")
        return shake(im, t, 6.1, 14)
    if t < 11.4:
        im = scene_bg(t, "berry", 65); rays(im, W / 2, 700, t, GOLD, 30); d = ImageDraw.Draw(im)
        kinetic(im, "Over the whole loan:", 480, t, 8.65, 70, WHITE)
        v = count(0, DT, t, 8.9, 9.9)
        d.text((W / 2, 680), f"+${v:,.0f}", font=F("k", 160), fill=GOLD, anchor="mm")
        if t > 9.9: sparkles(im, W / 2, 680, t, 9.9, 3, 16, 330, GOLD)
        pill(im, W / 2, 870, "Same house. A quarter of a percent.", t, 10.1, WHITE, INK, 44)
        souq(im, W / 2 - 210, 1360, 0.66, t, "wink" if t > 10.4 else "shocked")
        speech(im, W / 2 + 170, 1140, "Check yours first", 10.5, t, 42)
        return punch(im, t, 9.9, 0.06)
    im = scene_bg(t, "night", 67)
    endcard(im, t, 11.45, "Mortgage calculator", "Free · equal payments vs equal principal")
    souq(im, W / 2, 1480, 0.62, t, "happy", wave=True); confetti(im, t, 11.6, 6, 70)
    return im

if __name__ == "__main__":
    print(f"A1 {A1:,.2f}  A2 {A2:,.2f}  +{DM:,.2f}/mo  +{DT:,.0f} total")
    if len(sys.argv) > 1:
        for s in map(float, sys.argv[1].split(",")): frame(int(s * FPS)).convert("RGB").save(f"/tmp/fed-{s}.png")
    else:
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                              "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "/tmp/fed.tmp.mp4"], stdin=subprocess.PIPE)
        for i in range(DUR * FPS): p.stdin.write(frame(i).convert("RGB").tobytes())
        p.stdin.close(); assert p.wait() == 0; os.replace("/tmp/fed.tmp.mp4", "/tmp/fed_v.mp4")
