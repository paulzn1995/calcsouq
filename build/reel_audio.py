"""Original, royalty-free soundtrack generator for CalcSouq reels.

Usage (CLI):
  python3 build/reel_audio.py in.mp4 out.mp4 --cues "0:hit,2.2:whoosh,3.4:tick*12,9.6:ding" [--bpm 104] [--mood bright|calm|tense] [--seed 1]

Everything is synthesised here (no samples, no copyrighted music), so it is safe to publish anywhere.
Cue types: hit (soft impact), whoosh (scene change), tick (count-up step; tick*N spreads N ticks over 1.2 s),
ding (reveal/answer), pop (button/badge appears).
"""
import sys, argparse, subprocess, tempfile, os
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter

SR = 44100


def _env(n, a=0.01, r=0.3):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / max(r, 1e-4))
    return e


def _lp(x, f):
    b, a = butter(2, f / (SR / 2), "low"); return lfilter(b, a, x)


def _hp(x, f):
    b, a = butter(2, f / (SR / 2), "high"); return lfilter(b, a, x)


def note(freq, dur, kind="pad"):
    n = int(dur * SR); t = np.arange(n) / SR
    if kind == "pad":
        x = sum(np.sin(2 * np.pi * freq * m * t + m) / m for m in (1, 2, 3)) + 0.5 * np.sin(2 * np.pi * freq * 1.003 * t)
        e = np.minimum(1, t / 0.4) * np.minimum(1, (dur - t) / 0.4).clip(0, 1)
        return _lp(x * e, 1800) * 0.18
    if kind == "pluck":
        x = np.sin(2 * np.pi * freq * t) + 0.3 * np.sin(4 * np.pi * freq * t)
        return x * _env(n, 0.003, 0.22) * 0.22
    if kind == "bass":
        x = np.tanh(1.5 * np.sin(2 * np.pi * freq * t))
        return _lp(x * _env(n, 0.005, 0.35), 400) * 0.35


def drums(dur, bpm, rng):
    n = int(dur * SR); out = np.zeros(n); beat = 60 / bpm
    for k in range(int(dur / beat * 2) + 1):
        i = int(k * beat / 2 * SR)
        if i >= n: break
        if k % 4 == 0:  # kick
            m = int(0.25 * SR); t = np.arange(m) / SR
            kick = np.sin(2 * np.pi * (50 + 90 * np.exp(-t * 30)) * t) * np.exp(-t * 12)
            out[i:i + m] += kick[: n - i] * 0.55
        if k % 4 == 2:  # snap/clap
            m = int(0.18 * SR); s = _hp(rng.standard_normal(m), 1500) * np.exp(-np.arange(m) / SR * 25)
            out[i:i + m] += s[: n - i] * 0.18
        m = int(0.05 * SR); h = _hp(rng.standard_normal(m), 7000) * np.exp(-np.arange(m) / SR * 80)  # hat every 8th
        out[i:i + m] += h[: n - i] * (0.07 if k % 2 else 0.04)
    return out


SCALES = {
    "bright": [(261.6, 329.6, 392.0), (220.0, 261.6, 329.6), (174.6, 220.0, 261.6), (196.0, 246.9, 293.7)],  # C Am F G
    "calm": [(220.0, 261.6, 329.6), (174.6, 220.0, 261.6), (261.6, 329.6, 392.0), (196.0, 246.9, 293.7)],    # Am F C G
    "tense": [(220.0, 261.6, 329.6), (233.1, 293.7, 349.2), (220.0, 261.6, 329.6), (207.7, 261.6, 311.1)],  # Am Bb Am G#aug
}


def music(dur, bpm=104, mood="bright", seed=1):
    rng = np.random.default_rng(seed); n = int(dur * SR); out = np.zeros(n)
    bar = 4 * 60 / bpm; chords = SCALES.get(mood, SCALES["bright"])
    for b in range(int(dur / bar) + 1):
        start = int(b * bar * SR); ch = chords[b % len(chords)]
        if start >= n: break
        for f in ch:
            x = note(f, bar + 0.3, "pad"); out[start:start + len(x)] += x[: n - start]
        x = note(ch[0] / 2, bar * 0.9, "bass"); out[start:start + len(x)] += x[: n - start]
        for s in range(8):  # arpeggio plucks
            i = start + int(s * bar / 8 * SR)
            if i >= n: break
            x = note(ch[s % 3] * 2, 0.3, "pluck"); out[i:i + len(x)] += x[: n - i] * (0.8 if s % 2 == 0 else 0.5)
    out += drums(dur, bpm, rng)
    fade = int(0.6 * SR); out[-fade:] *= np.linspace(1, 0, fade); out[:int(0.05 * SR)] *= np.linspace(0, 1, int(0.05 * SR))
    return out


def sfx(kind, rng):
    if kind == "whoosh":
        m = int(0.45 * SR); t = np.arange(m) / SR; x = rng.standard_normal(m)
        e = np.sin(np.pi * t / t[-1]) ** 2; y = _lp(_hp(x, 400), 3500) * e; return y * 0.35
    if kind == "hit":
        m = int(0.6 * SR); t = np.arange(m) / SR
        y = np.sin(2 * np.pi * (60 + 120 * np.exp(-t * 20)) * t) * np.exp(-t * 6) + _lp(rng.standard_normal(m), 900) * np.exp(-t * 18) * 0.4
        return y * 0.6
    if kind == "tick":
        m = int(0.04 * SR); t = np.arange(m) / SR; return np.sin(2 * np.pi * 2200 * t) * np.exp(-t * 120) * 0.18
    if kind == "pop":
        m = int(0.12 * SR); t = np.arange(m) / SR; return np.sin(2 * np.pi * (500 + 900 * t / t[-1]) * t) * np.exp(-t * 30) * 0.3
    if kind == "ding":
        m = int(1.2 * SR); t = np.arange(m) / SR
        return sum(np.sin(2 * np.pi * f * t) / k for k, f in enumerate((1318.5, 1975.5, 2637.0), 1)) * np.exp(-t * 3.5) * 0.25
    return np.zeros(1)


def soundtrack(dur, cues, bpm=104, mood="bright", seed=1):
    rng = np.random.default_rng(seed + 7)
    out = music(dur, bpm, mood, seed) * 0.8; n = len(out)
    for c in cues.split(","):
        if ":" not in c: continue
        ts, kind = c.split(":"); count = 1
        if "*" in kind: kind, count = kind.split("*"); count = int(count)
        for j in range(count):
            t0 = float(ts) + (1.2 * j / max(count, 1) if count > 1 else 0)
            x = sfx(kind.strip(), rng); i = int(t0 * SR)
            if i < n: out[i:i + len(x)] += x[: n - i]
    out /= max(1e-6, np.max(np.abs(out))) / 0.89
    return out


def mux(video_in, video_out, cues, bpm=104, mood="bright", seed=1):
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video_in]).decode().strip())
    a = soundtrack(dur, cues, bpm, mood, seed)
    with tempfile.TemporaryDirectory() as d:
        wav = os.path.join(d, "a.wav"); wavfile.write(wav, SR, (a * 32767).astype(np.int16))
        tmp = video_out + ".tmp.mp4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", video_in, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                        "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", tmp], check=True)
        os.replace(tmp, video_out)


if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("inp"); p.add_argument("out"); p.add_argument("--cues", default="")
    p.add_argument("--bpm", type=float, default=104); p.add_argument("--mood", default="bright"); p.add_argument("--seed", type=int, default=1)
    a = p.parse_args(); mux(a.inp, a.out, a.cues, a.bpm, a.mood, a.seed)
