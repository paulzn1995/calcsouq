"""CalcSouq news reels 23 Nov 2026: Nvidia jumps ~29% premarket (Huang reinstated); AI stocks rebound premarket.
Sources (checked 23 Nov 2026, ~18:20 Dubai):
  Yahoo Finance live blog 23 Nov 9:15 a.m. ET: NVDA +27% premarket after board reinstated Jensen Huang as CEO; quote page +29.15% (+23.87% at 8:58).
  Phemex 23 Nov: NVDA +25%+ premarket after a 14% Friday plunge, close $125.53; nearly 50% below October high before the jump.
  CNBC via mlq.ai: Nasdaq 100 futures +3.17%, Arm +9.46% at 8:34–8:44 a.m. ET; GuruFocus: Nasdaq 100 futures +3.49%.
  BigGo Finance: SK Hynix >10%, Arm >8%, AMD and Applied Materials >7%, Micron +6%, TSMC ADR up to 7.62%; Nasdaq worst week since 2020 (also Phemex).
  TrendingTopics (Yahoo data): 15 hardest-hit AI stocks all up premarket, ~6% average.
Usage: python3 build/reels_2026_11_23_nvda.py <nvda|ai> [t,...] -> stills, or no times -> /tmp/<name>_v.mp4 (silent)
       python3 build/reels_2026_11_23_nvda.py story out.jpg
"""
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_fx import *

def chip(img, cx, cy, s=1.0, glow=0.0):
    if s < 0.05: return
    d = ImageDraw.Draw(img); w = 300 * s
    if glow > 0:
        g = Image.new("RGBA", img.size, (0, 0, 0, 0)); ImageDraw.Draw(g).rounded_rectangle([cx - w * .8, cy - w * .8, cx + w * .8, cy + w * .8], int(60 * s), fill=(118, 185, 0, int(120 * glow)))
        img.paste(g, (0, 0), g.filter(ImageFilter.GaussianBlur(50 * s))); d = ImageDraw.Draw(img)
    for k in range(7):
        o = -w / 2 + 30 * s + k * (w - 60 * s) / 6
        for a, b in (((cx + o, cy - w / 2 - 40 * s), (cx + o, cy - w / 2)), ((cx + o, cy + w / 2), (cx + o, cy + w / 2 + 40 * s)),
                     ((cx - w / 2 - 40 * s, cy + o), (cx - w / 2, cy + o)), ((cx + w / 2, cy + o), (cx + w / 2 + 40 * s, cy + o))):
            d.line([a, b], fill=(190, 195, 205), width=max(3, int(10 * s)))
    d.rounded_rectangle([cx - w / 2, cy - w / 2, cx + w / 2, cy + w / 2], int(30 * s), fill=(30, 34, 44), outline=(118, 185, 0), width=max(3, int(8 * s)))
    d.rounded_rectangle([cx - w / 3, cy - w / 3, cx + w / 3, cy + w / 3], int(20 * s), fill=(44, 50, 62))
    d.text((cx, cy), "AI", font=F("k", 110 * s), fill=(150, 220, 40), anchor="mm")

def small(img, txt, y, col=WHITE, size=40):
    ImageDraw.Draw(img).text((W / 2, y), txt, font=F("b", size), fill=col, anchor="mm")

def row(img, y, label, val, t, t0, vcol=GREEN):
    p = back(seg(t, t0, t0 + .5))
    if p <= 0: return
    x = 90 + (1 - p) * 80; r = x + 900; shadow(img, (x, y - 62, r, y + 62), 34, 16, 80, (0, 8)); d = ImageDraw.Draw(img)
    d.rounded_rectangle([x, y - 62, r, y + 62], 34, fill=(24, 28, 40))
    d.text((x + 40, y), label, font=F("b", 46), fill=WHITE, anchor="lm"); d.text((r - 40, y), val, font=F("k", 58), fill=vcol, anchor="rm")

def tail(t, t0):
    im = scene_bg(t, "night", 77); d = ImageDraw.Draw(im)
    kinetic(im, "Premarket moves fast", 520, t, t0, 80, WHITE)
    small(im, "Prices can change a lot at the open", 620, GOLD, 42)
    pill(im, W / 2, 800, "Check any % move in 5 seconds", t, t0 + .6, GOLD, INK, 46)
    small(im, "calcsouq.com/percentage-calculator", 920, WHITE, 44)
    small(im, "Education only · not investment advice", 1500, (170, 175, 195), 34)
    chart_up(d, 300, 1340, 480, 280, ease(seg(t, t0, t0 + 1.5)), GREEN)
    return im

DUR = {"nvda": 22.0, "ai": 21.0}

def nvda(t):
    if t < 6.0:
        im = scene_bg(t, "night", 71); rays(im, W / 2, 640, t, GREEN, 26); d = ImageDraw.Draw(im)
        kinetic(im, "Nvidia before the bell", 360, t, -0.3, 82, WHITE)
        v = count(0, 29, t, 0.6, 2.4); d.text((W / 2, 580), f"+{v:.0f}%", font=F("k", 250), fill=GREEN, anchor="mm")
        pill(im, W / 2, 790, "Premarket · Mon 23 Nov", t, 2.4, WHITE, INK, 46)
        chip(im, W / 2, 1220, 1.1 * back(seg(t, .2, .9)), glow=seg(t, 2.4, 3.2))
        return punch(im, t, 2.4)
    if t < 12.0:
        im = scene_bg(t, "night", 72); d = ImageDraw.Draw(im)
        kinetic(im, "Why?", 360, t, 6.0, 120, GOLD)
        small(im, "Nvidia's board brought back", 520, WHITE, 52) if t > 6.6 else None
        if t > 7.2: d.text((W / 2, 620), "Jensen Huang as CEO", font=F("k", 84), fill=WHITE, anchor="mm")
        pill(im, W / 2, 780, "Effective immediately", t, 8.2, GREEN, INK, 48)
        row(im, 1000, "Friday", "−14%", t, 9.2, RED)
        row(im, 1160, "Friday close", "$125.53", t, 10.0, WHITE)
        return im
    if t < 17.0:
        im = scene_bg(t, "night", 73); d = ImageDraw.Draw(im)
        kinetic(im, "Back to the top?", 380, t, 12.0, 90, WHITE)
        small(im, "Not yet", 490, GOLD, 56) if t > 12.6 else None
        row(im, 680, "Oct high → Friday", "≈ −50%", t, 13.0, RED)
        row(im, 840, "Friday → back to high", "+100%", t, 14.0, GOLD)
        if t > 15.2: pill(im, W / 2, 1040, "−50% needs +100%", t, 15.2, WHITE, INK, 54)
        return shake(im, t, 14.0, 12)
    return tail(t, 17.0)

def ai(t):
    if t < 5.5:
        im = scene_bg(t, "night", 61); rays(im, W / 2, 640, t, GREEN, 22); d = ImageDraw.Draw(im)
        kinetic(im, "AI stocks bounce", 360, t, -0.3, 96, WHITE)
        kinetic(im, "before the bell", 480, t, 0.1, 80, GOLD)
        v = count(0, 3, t, 1.0, 2.4); d.text((W / 2, 680), f"+{v:.0f}%", font=F("k", 200), fill=GREEN, anchor="mm")
        pill(im, W / 2, 860, "Nasdaq 100 futures · premarket", t, 2.4, WHITE, INK, 44)
        chip(im, W / 2, 1260, 0.9 * back(seg(t, .3, 1.0)), glow=seg(t, 2.4, 3.0))
        return punch(im, t, 2.4)
    if t < 14.0:
        im = scene_bg(t, "night", 62); d = ImageDraw.Draw(im)
        kinetic(im, "Early premarket moves", 340, t, 5.5, 74, WHITE)
        small(im, "Mon 23 Nov · approximate", 430, GOLD, 40)
        for i, (lab, v, t0) in enumerate([("Nvidia", "+25–29%", 6.0), ("Arm", "≈ +9%", 7.2), ("AMD", "≈ +7%", 8.4), ("TSMC (US shares)", "≈ +7%", 9.6), ("Micron", "≈ +6%", 10.8)]):
            row(im, 580 + i * 150, lab, v, t, t0, GREEN)
        return im
    if t < 18.0:
        im = scene_bg(t, "night", 63); d = ImageDraw.Draw(im)
        kinetic(im, "After a rough week", 420, t, 14.0, 84, WHITE)
        pill(im, W / 2, 600, "Nasdaq: worst week since 2020", t, 14.6, RED, WHITE, 50)
        small(im, "Big drops, then big bounces", 760, GOLD, 50) if t > 15.6 else None
        return im
    return tail(t, 18.0)

def story(out):
    im = scene_bg(3.0, "night", 71); rays(im, W / 2, 700, 3.0, GREEN, 26); d = ImageDraw.Draw(im)
    d.text((W / 2, 300), "NVIDIA · PREMARKET", font=F("k", 70), fill=WHITE, anchor="mm")
    d.text((W / 2, 560), "+29%", font=F("k", 300), fill=GREEN, anchor="mm")
    d.text((W / 2, 780), "Jensen Huang back as CEO", font=F("k", 66), fill=WHITE, anchor="mm")
    d.text((W / 2, 870), "AI chip stocks up 6–10% before the bell", font=F("b", 46), fill=GOLD, anchor="mm")
    chip(im, W / 2, 1240, 1.0, 1.0)
    d = ImageDraw.Draw(im); d.text((W / 2, 1620), "Premarket prices move fast · education only", font=F("b", 38), fill=(180, 185, 200), anchor="mm")
    d.text((W / 2, 1700), "calcsouq.com", font=F("k", 52), fill=GOLD, anchor="mm")
    im.convert("RGB").save(out, quality=92)

if __name__ == "__main__":
    name = sys.argv[1]
    if name == "story": story(sys.argv[2]); sys.exit()
    fn = {"nvda": nvda, "ai": ai}[name]
    if len(sys.argv) > 2:
        for x in sys.argv[2].split(","): fn(float(x)).convert("RGB").save(f"/tmp/{name}_{x}.png")
        sys.exit()
    out = f"/tmp/{name}_v.mp4"; tmp = out + ".tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for i in range(int(DUR[name] * FPS)): p.stdin.write(fn(i / FPS).convert("RGB").tobytes())
    p.stdin.close(); assert p.wait() == 0; os.replace(tmp, out); print(out)
