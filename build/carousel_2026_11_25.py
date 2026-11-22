"""Sunday-planned carousel for Wed 2026-11-25 13:30 Dubai: "EMI on ₹10 lakh at 5 rates".
7 slides, 1080x1350 JPEG -> build/static/media/ig/2026-11-25-emi-10-lakh-<n>.jpg
Figures are pure maths (standard reducing-balance EMI, monthly rests). They are computed here by two
independent methods (closed-form formula and an amortisation-schedule bisection) and the script stops
if they disagree by more than ₹1.
"""
import os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_fx import F, INK, GOLD, WHITE, GREEN, RED

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static/media/ig/")
W, H = 1080, 1350
P = 1_000_000
RATES = (8, 9, 10, 11, 12)
YEARS = (5, 10, 20)
GREY = (170, 172, 178); CARD = (32, 35, 40); LINE = (52, 56, 62)


def emi_formula(p, r, n):
    i = r / 1200; N = n * 12
    return p * i * (1 + i) ** N / ((1 + i) ** N - 1)


def emi_schedule(p, r, n):
    i = r / 1200; N = n * 12; lo, hi = 0.0, float(p)
    for _ in range(200):
        m = (lo + hi) / 2; b = float(p)
        for _ in range(N): b = b * (1 + i) - m
        lo, hi = (m, hi) if b > 0 else (lo, m)
    return m


D = {}
for n in YEARS:
    for r in RATES:
        a, b = emi_formula(P, r, n), emi_schedule(P, r, n)
        assert abs(a - b) < 1, (n, r, a, b)
        D[n, r] = (round(a), a * n * 12 - P)


def inr(v):  # Indian digit grouping
    s = str(int(round(v))); head, tail = s[:-3], s[-3:]
    out = ""
    if head:
        parts = []
        while len(head) > 2: parts.insert(0, head[-2:]); head = head[:-2]
        if head: parts.insert(0, head)
        out = ",".join(parts) + ","
    return "₹" + out + tail


def lakh(v): return f"₹{v / 1e5:.2f} lakh"


def base(k, n=7):
    im = Image.new("RGB", (W, H), INK); d = ImageDraw.Draw(im)
    d.rounded_rectangle((80, 90, 145, 155), 16, fill=GOLD)
    d.text((112.5, 122.5), "c", font=F("k", 44), fill=INK, anchor="mm")
    d.text((165, 122), "CalcSouq", font=F("b", 40), fill=WHITE, anchor="lm")
    d.text((1000, 1280), f"{k}/{n}", font=F("s", 30), fill=GREY, anchor="rm")
    return im, d


def pill(d, x, y, text, bg=GOLD, fg=INK, size=30):
    w = d.textlength(text, font=F("b", size))
    d.rounded_rectangle((x, y, x + w + 80, y + size + 30), (size + 30) // 2, fill=bg)
    d.text((x + 40, y + (size + 30) / 2), text, font=F("b", size), fill=fg, anchor="lm")


def table(im, d, n, k):
    pill(d, 80, 230, f"{n} YEARS · {n * 12} EMIs")
    d.text((80, 320), f"₹10 lakh over {n} years", font=F("k", 66), fill=WHITE)
    top = 450
    d.rounded_rectangle((80, top, 1000, top + 640), 28, fill=CARD)
    cols = (130, 520, 950)
    for x, t, a in zip(cols, ("Rate", "EMI / month", "Total interest"), ("lm", "rm", "rm")):
        d.text((x, top + 55), t, font=F("s", 30), fill=GREY, anchor=a)
    for j, r in enumerate(RATES):
        y = top + 150 + j * 105
        d.line((120, y - 52, 960, y - 52), fill=LINE, width=2)
        emi, intr = D[n, r]
        d.text((cols[0], y), f"{r}%", font=F("b", 46), fill=WHITE, anchor="lm")
        d.text((cols[1], y), inr(emi), font=F("k", 46), fill=GOLD, anchor="rm")
        d.text((cols[2], y), lakh(intr), font=F("b", 42), fill=WHITE, anchor="rm")
    lo, hi = D[n, 8][1], D[n, 12][1]
    d.text((80, 1150), f"8% → 12% adds {lakh(hi - lo)} of interest.", font=F("s", 36), fill=WHITE)
    d.text((80, 1205), "Reducing balance, monthly rests, before fees.", font=F("r", 28), fill=GREY)


slides = []

im, d = base(1)
pill(d, 80, 300, "SAVE THIS · LOAN CHEAT SHEET")
for i, (t, c) in enumerate((("EMI on", WHITE), ("₹10 lakh", GOLD), ("at 5 rates", WHITE))):
    d.text((80, 400 + i * 135), t, font=F("k", 124), fill=c)
d.text((80, 840), "8% to 12% · 5, 10 and 20 years", font=F("r", 42), fill=(215, 215, 220))
d.text((80, 900), "Plus a shortcut for any loan amount. Swipe →", font=F("r", 42), fill=(215, 215, 220))
slides.append(im)

for k, n in ((2, 5), (3, 10), (4, 20)):
    im, d = base(k); table(im, d, n, k); slides.append(im)

# 5: the 20-year trap
im, d = base(5)
pill(d, 80, 230, "THE LONG-LOAN TRAP", RED, WHITE)
d.text((80, 320), "Same ₹10 lakh at 10%", font=F("k", 66), fill=WHITE)
rows = [(n, D[n, 10][0], D[n, 10][0] * n * 12) for n in YEARS]
mx = rows[-1][2]
for j, (n, emi, tot) in enumerate(rows):
    y = 500 + j * 210
    d.text((80, y), f"{n} years · EMI {inr(emi)}", font=F("b", 40), fill=WHITE)
    bw = int(840 * tot / mx)
    d.rounded_rectangle((80, y + 70, 80 + bw, y + 130), 14, fill=GOLD if n == 5 else (RED if n == 20 else (200, 160, 40)))
    d.text((80 + bw - 20, y + 100), f"pay back {lakh(tot)}", font=F("b", 32), fill=INK, anchor="rm")
d.text((80, 1150), f"20 years: EMI is {inr(D[5, 10][0] - D[20, 10][0])} lower than 5 years,", font=F("s", 36), fill=WHITE)
d.text((80, 1200), f"but you pay {lakh(D[20, 10][1] - D[5, 10][1])} more interest.", font=F("s", 36), fill=GOLD)
slides.append(im)

# 6: per ₹1 lakh shortcut
im, d = base(6)
pill(d, 80, 230, "SHORTCUT FOR ANY AMOUNT")
d.text((80, 320), "EMI per ₹1 lakh", font=F("k", 72), fill=WHITE)
top = 450
d.rounded_rectangle((80, top, 1000, top + 610), 28, fill=CARD)
xs = (130, 480, 715, 950)
for x, t, a in zip(xs, ("Rate", "5 yrs", "10 yrs", "20 yrs"), ("lm", "rm", "rm", "rm")):
    d.text((x, top + 55), t, font=F("s", 30), fill=GREY, anchor=a)
for j, r in enumerate(RATES):
    y = top + 150 + j * 100
    d.line((120, y - 50, 960, y - 50), fill=LINE, width=2)
    d.text((xs[0], y), f"{r}%", font=F("b", 44), fill=WHITE, anchor="lm")
    for x, n in zip(xs[1:], YEARS):
        d.text((x, y), inr(D[n, r][0] / 10), font=F("b", 44), fill=GOLD, anchor="rm")
d.text((80, 1110), f"₹25 lakh at 9% for 20 years: 25 × {inr(D[20, 9][0] / 10)} ≈ {inr(round(25 * D[20, 9][0] / 10, -2))}", font=F("s", 36), fill=WHITE)
d.text((80, 1165), f"Multiply by your loan in lakh (exact EMI: {inr(emi_formula(2_500_000, 9, 20))}).", font=F("r", 28), fill=GREY)
slides.append(im)

# 7: end card
im, d = base(7)
d.text((80, 380), "Your loan,", font=F("k", 110), fill=WHITE)
d.text((80, 510), "your numbers", font=F("k", 110), fill=GOLD)
for i, t in enumerate(("Any amount, rate and tenure", "EMI, total interest, total paid", "Rupees, dirhams and more", "Free · no sign-up")):
    d.text((80, 720 + i * 70), "✓  " + t, font=F("s", 40), fill=WHITE)
pill(d, 80, 1060, "Link in bio → Loan EMI calculator", GOLD, INK, 36)
d.text((80, 1185), "Save this post for your next loan quote.", font=F("r", 32), fill=GREY)
slides.append(im)

if __name__ == "__main__":
    for k, im in enumerate(slides, 1):
        im.save(OUT + f"2026-11-25-emi-10-lakh-{k}.jpg", quality=92)
    for n in YEARS:
        print(n, [(r, D[n, r][0], round(D[n, r][1])) for r in RATES])
