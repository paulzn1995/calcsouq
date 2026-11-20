"""Original, royalty-free soundtrack generator for CalcSouq reels (everything synthesised; no samples, no copyrighted music).

CLI:
  python3 build/reel_audio.py in.mp4 out.mp4 --style pop|lofi|cinematic|electro|funk|desi|random \
      --cues "0:boom,2.2:whoosh,3.4:tick*12,6:coin*5,8.5:ding,9:cash,10:sparkle" [--bpm 0=auto] [--seed N]
  (--mood is accepted as an alias of --style; bright->pop, calm->lofi, tense->cinematic)

Styles differ in tempo, drums, instruments and chord progressions; key and progression are picked by seed,
so give each reel a different seed (e.g. date+slot) for variety.
SFX cues: hit, boom, whoosh, swoosh, riser (put it ~1 s before a reveal), tick (tick*N over 1.2 s), pop, pop2,
ding, coin (coin*N), cash, sparkle, type (type*N), fail, success.
"""
import argparse, subprocess, tempfile, os
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter

SR = 44100

def _lp(x, f): b, a = butter(2, min(f, SR / 2 - 100) / (SR / 2), "low"); return lfilter(b, a, x)
def _hp(x, f): b, a = butter(2, f / (SR / 2), "high"); return lfilter(b, a, x)
def _bp(x, lo, hi): return _lp(_hp(x, lo), hi)
def _t(d): return np.arange(int(d * SR)) / SR
def _env(n, a=0.005, r=0.3): t = np.arange(n) / SR; return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / max(r, 1e-4))
def _add(out, x, i):
    if i < 0: x = x[-i:]; i = 0
    if i >= len(out): return
    m = min(len(x), len(out) - i); out[i:i + m] += x[:m]
def hz(midi): return 440 * 2 ** ((midi - 69) / 12)

# ---------------- instruments ----------------
def pad(f, d, bright=1800):
    t = _t(d); x = sum(np.sin(2 * np.pi * f * m * t * (1 + .002 * m)) / m for m in (1, 2, 3, 4)) + .5 * np.sin(2 * np.pi * f * 1.004 * t)
    e = np.minimum(1, t / .35) * np.clip((d - t) / .35, 0, 1); return _lp(x * e, bright) * .12
def pluck(f, d=.35, tone=1.0):
    t = _t(d); x = np.sin(2 * np.pi * f * t) + .4 * tone * np.sin(4 * np.pi * f * t) + .15 * tone * np.sin(6 * np.pi * f * t); return x * _env(len(t), .002, .18) * .2
def epiano(f, d=.8):
    t = _t(d); x = np.sin(2 * np.pi * f * t + 1.2 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t * 3)); return x * _env(len(t), .004, .45) * .17
def saw(f, d=.25, cut=2500):
    t = _t(d); x = 2 * ((f * t) % 1) - 1 + 2 * ((f * 1.007 * t) % 1) - 1; return _lp(x * _env(len(t), .003, .16), cut) * .09
def bass(f, d, drive=1.5, cut=380):
    t = _t(d); x = np.tanh(drive * np.sin(2 * np.pi * f * t) + .3 * np.sin(4 * np.pi * f * t)); return _lp(x * _env(len(t), .004, d * .6), cut) * .32
def sitar(f, d=.6):  # plucked string with buzzy bridge (original synthesis)
    t = _t(d); x = np.sin(2 * np.pi * f * t + 2.5 * np.sin(2 * np.pi * f * t) * np.exp(-t * 6)); x = np.tanh(2 * x); return _bp(x, 200, 5000) * _env(len(t), .002, .35) * .16
def flute(f, d=.5, rng=None):
    t = _t(d); vib = 1 + .01 * np.sin(2 * np.pi * 5.5 * t); x = np.sin(2 * np.pi * f * vib * t) + .2 * np.sin(4 * np.pi * f * t)
    n = rng.standard_normal(len(t)) * .05 if rng is not None else 0; e = np.minimum(1, t / .06) * np.clip((d - t) / .1, 0, 1); return (x + n) * e * .14

def kick(punch=1.0):
    t = _t(.3); return np.sin(2 * np.pi * (45 + 110 * punch * np.exp(-t * 32)) * t) * np.exp(-t * 11) * .6
def snare(rng, tone=190):
    t = _t(.22); return (_hp(rng.standard_normal(len(t)), 1200) * np.exp(-t * 18) * .5 + np.sin(2 * np.pi * tone * t) * np.exp(-t * 25) * .4) * .4
def clap(rng):
    t = _t(.25); n = _bp(rng.standard_normal(len(t)), 900, 5000); e = np.zeros(len(t))
    for k in (0, .011, .022): i = int(k * SR); e[i:] += np.exp(-(np.arange(len(t) - i)) / SR * 22)
    return n * e * .18
def hat(rng, open_=False):
    t = _t(.25 if open_ else .05); return _hp(rng.standard_normal(len(t)), 7000) * np.exp(-t * (14 if open_ else 80)) * (.08 if open_ else .06)
def tabla(rng, high=True):
    t = _t(.35); f = (420 if high else 110) * (1 + .5 * np.exp(-t * 40)); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * (10 if high else 6)) * (.28 if high else .4) + _hp(rng.standard_normal(len(t)), 3000) * np.exp(-t * 60) * .05
def shaker(rng): t = _t(.08); return _hp(rng.standard_normal(len(t)), 5000) * np.sin(np.pi * t / t[-1]) * .05
def crackle(n, rng): x = np.zeros(n); idx = rng.integers(0, n, n // 1800); x[idx] = rng.uniform(-.3, .3, len(idx)); return _hp(x, 2000) * .5 + _lp(rng.standard_normal(n), 900) * .006

# ---------------- music ----------------
MAJ = [0, 2, 4, 5, 7, 9, 11]; MIN = [0, 2, 3, 5, 7, 8, 10]
PROGS_MAJ = [[0, 5, 3, 4], [0, 4, 5, 3], [3, 4, 0, 0], [0, 3, 4, 3], [5, 3, 0, 4]]
PROGS_MIN = [[0, 5, 2, 6], [0, 3, 4, 0], [0, 6, 5, 6], [0, 5, 6, 4]]
STYLE = {  # bpm range, scale, swing, instruments
    "pop": dict(bpm=(104, 122), scale="maj", lead="pluck", chords="pad", drums="pop"),
    "lofi": dict(bpm=(72, 88), scale="maj7", lead="epiano", chords="epiano", drums="lofi"),
    "cinematic": dict(bpm=(84, 100), scale="min", lead="pad", chords="pad", drums="cine"),
    "electro": dict(bpm=(118, 128), scale="min", lead="saw", chords="pad", drums="four"),
    "funk": dict(bpm=(96, 110), scale="min", lead="pluck", chords="epiano", drums="funk"),
    "desi": dict(bpm=(92, 108), scale="maj", lead="sitar", chords="pad", drums="tabla"),
}
ALIAS = {"bright": "pop", "calm": "lofi", "tense": "cinematic"}

def chord_notes(root, deg, scale, seven=False):
    sc = MIN if scale == "min" else MAJ
    idx = [deg, deg + 2, deg + 4] + ([deg + 6] if seven else [])
    return [root + sc[i % 7] + 12 * (i // 7) for i in idx]

def music(dur, style="pop", bpm=0, seed=1):
    rng = np.random.default_rng(seed); st = STYLE[style]
    bpm = bpm or float(rng.integers(*st["bpm"])); beat = 60 / bpm; bar = 4 * beat
    root = 57 + int(rng.integers(0, 7))  # A3..D#4
    minor = st["scale"] == "min"; prog = (PROGS_MIN if minor else PROGS_MAJ)[int(rng.integers(0, 4 if minor else 5))]
    seven = st["scale"] == "maj7" or style in ("lofi", "funk")
    n = int(dur * SR); out = np.zeros(n); swing = .12 if style in ("lofi", "funk") else 0
    for b in range(int(dur / bar) + 1):
        s0 = int(b * bar * SR); ch = chord_notes(root, prog[b % 4], "min" if minor else "maj", seven)
        if st["chords"] == "pad":
            for m in ch: _add(out, pad(hz(m), bar + .3, 2600 if style == "electro" else 1800), s0)
        else:
            for k in (0, 2.5):
                for m in ch: _add(out, epiano(hz(m), beat * 1.6), s0 + int(k * beat * SR))
        bl = beat * (1 if style in ("funk", "electro") else 2)
        for k in range(int(bar / bl)):
            octv = 12 if (style == "funk" and k % 2) else 0
            _add(out, bass(hz(ch[0] - 24 + octv), bl * .9, 2.2 if style == "electro" else 1.5), s0 + int(k * bl * SR))
        steps = 8 if style != "electro" else 16
        pattern = rng.permutation([0, 1, 2, 1, 0, 2, 1, 3])
        for k in range(steps):
            if style == "cinematic" and k % 4: continue
            if rng.random() < (.25 if style in ("lofi", "desi") else .1): continue
            i = s0 + int((k * bar / steps + (swing * beat / 2 if k % 2 else 0)) * SR)
            m = ch[int(pattern[k % 8]) % len(ch)] + 12 + (12 if style in ("pop", "electro") else 0)
            lead = st["lead"]
            x = {"pluck": lambda: pluck(hz(m)), "epiano": lambda: epiano(hz(m), .5), "saw": lambda: saw(hz(m)),
                 "sitar": lambda: sitar(hz(m - 12)), "pad": lambda: pluck(hz(m), .6, .3)}[lead]()
            _add(out, x * (.9 if k % 2 == 0 else .55), i)
        if style == "desi" and b % 2 == 1:
            for k in range(4): _add(out, flute(hz(ch[k % 3] + 12), beat * .9, rng), s0 + int(k * beat * SR))
    out += drums(dur, bpm, st["drums"], rng, swing)
    if style == "lofi": out += crackle(n, rng)
    f = int(.6 * SR); out[-f:] *= np.linspace(1, 0, f); out[:int(.04 * SR)] *= np.linspace(0, 1, int(.04 * SR))
    return out

def drums(dur, bpm, kind, rng, swing=0):
    n = int(dur * SR); out = np.zeros(n); beat = 60 / bpm
    for k in range(int(dur / beat * 4) + 1):  # 16th grid
        i = int((k * beat / 4 + (swing * beat / 2 if k % 2 else 0)) * SR)
        if i >= n: break
        p = k % 16
        if kind == "pop":
            if p in (0, 8, 10): _add(out, kick(), i)
            if p in (4, 12): _add(out, clap(rng), i); _add(out, snare(rng) * .5, i)
            if p % 2 == 0: _add(out, hat(rng, p % 8 == 6), i)
        elif kind == "lofi":
            if p in (0, 7, 10): _add(out, _lp(kick(.7), 2000), i)
            if p in (4, 12): _add(out, _lp(snare(rng, 170), 3500), i)
            if p % 2 == 0: _add(out, hat(rng) * .7, i)
        elif kind == "cine":
            if p in (0, 6): _add(out, kick(1.3) * 1.2, i)
            if p == 12: _add(out, snare(rng, 140) * 1.3, i)
            if p % 4 == 2: _add(out, shaker(rng), i)
        elif kind == "four":
            if p % 4 == 0: _add(out, kick(1.1), i)
            if p in (4, 12): _add(out, clap(rng), i)
            if p % 4 == 2: _add(out, hat(rng, True), i)
            elif p % 2: _add(out, hat(rng), i)
        elif kind == "funk":
            if p in (0, 3, 10): _add(out, kick(), i)
            if p in (4, 12): _add(out, snare(rng, 210), i)
            if p in (7, 15): _add(out, snare(rng) * .25, i)
            _add(out, hat(rng, p == 14) * (1 if p % 2 == 0 else .6), i)
        elif kind == "tabla":
            if p in (0, 6, 10): _add(out, tabla(rng, False), i)
            if p in (2, 4, 8, 12, 14): _add(out, tabla(rng, True), i)
            if p % 2: _add(out, shaker(rng), i)
    return out

# ---------------- SFX ----------------
def sfx(kind, rng):
    if kind == "whoosh": t = _t(.45); return _bp(rng.standard_normal(len(t)), 400, 3500) * np.sin(np.pi * t / t[-1]) ** 2 * .35
    if kind == "swoosh": t = _t(.3); fc = np.linspace(600, 6000, len(t)); x = rng.standard_normal(len(t)); return _hp(x, 800) * np.sin(np.pi * t / t[-1]) ** 3 * .25
    if kind == "riser": t = _t(1.1); x = sum(np.sin(2 * np.pi * np.cumsum(200 * (1 + 3 * t / t[-1]) * m) / SR) / m for m in (1, 2)); return (x * .12 + _hp(rng.standard_normal(len(t)), 2000) * .08) * (t / t[-1]) ** 2
    if kind == "hit": t = _t(.6); return (np.sin(2 * np.pi * (60 + 120 * np.exp(-t * 20)) * t) * np.exp(-t * 6) + _lp(rng.standard_normal(len(t)), 900) * np.exp(-t * 18) * .4) * .6
    if kind == "boom": t = _t(1.2); return (np.sin(2 * np.pi * (40 + 80 * np.exp(-t * 8)) * t) * np.exp(-t * 3) + _lp(rng.standard_normal(len(t)), 400) * np.exp(-t * 5) * .5) * .7
    if kind == "tick": t = _t(.04); return np.sin(2 * np.pi * 2200 * t) * np.exp(-t * 120) * .17
    if kind == "type": t = _t(.05); return _bp(rng.standard_normal(len(t)), 1500, 6000) * np.exp(-t * 90) * .2
    if kind == "pop": t = _t(.12); return np.sin(2 * np.pi * (500 + 900 * t / t[-1]) * t) * np.exp(-t * 30) * .3
    if kind == "pop2": t = _t(.1); return np.sin(2 * np.pi * (900 - 500 * t / t[-1]) * t) * np.exp(-t * 35) * .28
    if kind == "ding": t = _t(1.2); return sum(np.sin(2 * np.pi * f * t) / k for k, f in enumerate((1318.5, 1975.5, 2637.0), 1)) * np.exp(-t * 3.5) * .24
    if kind == "coin": t = _t(.35); return (np.sin(2 * np.pi * 1975 * t) * (t < .06) + np.sin(2 * np.pi * 2637 * t) * (t >= .06)) * np.exp(-t * 9) * .18
    if kind == "cash":
        t = _t(.9); bell = sum(np.sin(2 * np.pi * f * t) for f in (2093, 2637, 3136)) * np.exp(-t * 4) * .12
        clk = np.zeros(len(t)); m = int(.06 * SR); clk[:m] = _bp(rng.standard_normal(m), 800, 4000) * np.exp(-np.arange(m) / SR * 60) * .5; return bell + clk
    if kind == "sparkle":
        out = np.zeros(int(.9 * SR))
        for j in range(7): _add(out, np.sin(2 * np.pi * (2000 + 400 * j) * _t(.15)) * np.exp(-_t(.15) * 25) * .09, int(j * .09 * SR))
        return out
    if kind == "fail": t = _t(.7); return np.sin(2 * np.pi * np.cumsum(400 - 250 * t / t[-1]) / SR) * np.exp(-t * 2) * .2
    if kind == "success":
        out = np.zeros(int(.8 * SR))
        for j, f in enumerate((523.3, 659.3, 784.0, 1046.5)): _add(out, np.sin(2 * np.pi * f * _t(.4)) * np.exp(-_t(.4) * 6) * .16, int(j * .08 * SR))
        return out
    return np.zeros(1)

def soundtrack(dur, cues="", style="pop", bpm=0, seed=1):
    style = ALIAS.get(style, style)
    rng = np.random.default_rng(seed + 11)
    if style == "random": style = list(STYLE)[seed % len(STYLE)]
    out = music(dur, style, bpm, seed) * .75; n = len(out)
    for c in filter(None, cues.split(",")):
        ts, kind = c.split(":"); cnt = 1
        if "*" in kind: kind, cnt = kind.split("*"); cnt = int(cnt)
        for j in range(cnt):
            t0 = float(ts) + (1.2 * j / cnt if cnt > 1 else 0); _add(out, sfx(kind.strip(), rng), int(t0 * SR))
    out = np.tanh(out * 1.3) / np.tanh(1.3)
    return out / max(1e-6, np.max(np.abs(out))) * .89, style

def mux(video_in, video_out, cues="", style="pop", bpm=0, seed=1):
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video_in]).decode().strip())
    a, used = soundtrack(dur, cues, style, bpm, seed)
    with tempfile.TemporaryDirectory() as d:
        wav = os.path.join(d, "a.wav"); wavfile.write(wav, SR, (a * 32767).astype(np.int16)); tmp = video_out + ".tmp.mp4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", video_in, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", tmp], check=True)
        os.replace(tmp, video_out)
    return used

if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("inp"); p.add_argument("out"); p.add_argument("--cues", default="")
    p.add_argument("--style", default=None); p.add_argument("--mood", default=None); p.add_argument("--bpm", type=float, default=0); p.add_argument("--seed", type=int, default=1)
    a = p.parse_args(); print(mux(a.inp, a.out, a.cues, a.style or a.mood or "random", a.bpm, a.seed))
