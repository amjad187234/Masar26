"""Eigene Hintergrundmusik für die Reels (selbst erzeugt, daher ohne Rechte Dritter).
Moderner, freundlicher Beat: 118 BPM, Akkorde Am–F–C–G, Bass, Pluck-Arpeggio, Kick/Clap/Hi-Hat, Ein- und Ausblenden.
Aufruf: python3 tools/video/musik.py <ausgabe.wav> [sekunden] [variante 0..2]
"""
import sys, wave
import numpy as np

SR = 44100
ziel = sys.argv[1]; DAUER = float(sys.argv[2]) if len(sys.argv) > 2 else 15.1; VAR = int(sys.argv[3]) if len(sys.argv) > 3 else 0
BPM = [118, 112, 122][VAR % 3]; BEAT = 60 / BPM
N = int(SR * DAUER); t_all = np.arange(N) / SR
mix = np.zeros(N)
rng = np.random.default_rng(7 + VAR)

def lowpass(x, cut):
    a = np.exp(-2 * np.pi * cut / SR); y = np.empty_like(x); s = 0.0
    for i, v in enumerate(x): s = (1 - a) * v + a * s; y[i] = s
    return y

def put(sig, start):
    i = int(start * SR)
    if i >= N: return
    j = min(N, i + len(sig)); mix[i:j] += sig[:j - i]

def env(n, att, dec):
    e = np.ones(n); a = max(1, int(att * SR)); e[:a] = np.linspace(0, 1, a)
    return e * np.exp(-np.arange(n) / (dec * SR))

def ton(f, dauer, form='saw', att=.005, dec=.3, vol=.2):
    n = int(dauer * SR); t = np.arange(n) / SR
    if form == 'saw': w = 2 * ((t * f) % 1) - 1
    elif form == 'tri': w = 2 * np.abs(2 * ((t * f) % 1) - 1) - 1
    else: w = np.sin(2 * np.pi * f * t)
    return w * env(n, att, dec) * vol

def note(n): return 440 * 2 ** ((n - 69) / 12)

PROG = [[[57, 60, 64], 45], [[53, 57, 60], 41], [[48, 52, 55], 36], [[55, 59, 62], 43]]  # Am F C G
if VAR == 1: PROG = [[[50, 53, 57], 38], [[46, 50, 53], 34], [[53, 57, 60], 41], [[48, 52, 55], 36]]  # Dm Bb F C
if VAR == 2: PROG = [[[52, 55, 59], 40], [[48, 52, 55], 36], [[55, 59, 62], 43], [[50, 54, 57], 38]]  # Em C G D
takt = 4 * BEAT
nb = int(DAUER / BEAT) + 1
for b in range(nb):
    t0 = b * BEAT; akk, root = PROG[(b // 4) % 4]
    # Kick
    n = int(.35 * SR); tt = np.arange(n) / SR; f = 50 + 70 * np.exp(-tt * 30)
    put(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 9) * .9, t0)
    # Clap auf 2 und 4
    if b % 2 == 1:
        n = int(.2 * SR); z = rng.standard_normal(n); z = z - lowpass(z, 900)
        put(z * np.exp(-np.arange(n) / (.05 * SR)) * .28, t0)
    # Hi-Hat Achtel
    for k in (0, .5):
        n = int(.06 * SR); z = rng.standard_normal(n); z = z - lowpass(z, 6000)
        put(z * np.exp(-np.arange(n) / (.012 * SR)) * (.12 if k else .07), t0 + k * BEAT)
    # Bass (Achtel)
    for k in (0, .5):
        put(lowpass(ton(note(root), BEAT * .48, 'saw', dec=.18, vol=.32), 700), t0 + k * BEAT)
    # Pluck-Arpeggio (Sechzehntel)
    for k in range(4):
        nn = akk[(b * 4 + k) % 3] + 12
        put(lowpass(ton(note(nn), .25, 'saw', dec=.09, vol=.09), 2800), t0 + k * BEAT / 4)
# Pad je Takt
for m in range(int(DAUER / takt) + 1):
    akk, _ = PROG[m % 4]
    for nn in akk:
        put(lowpass(ton(note(nn), takt, 'tri', att=.25, dec=3.0, vol=.07), 1500), m * takt)

mix = np.tanh(mix * 1.1)
fi, fo = int(.3 * SR), int(1.6 * SR)
mix[:fi] *= np.linspace(0, 1, fi); mix[-fo:] *= np.linspace(1, 0, fo)
mix = mix / (np.max(np.abs(mix)) + 1e-9) * .85
st = np.stack([mix, np.roll(mix, int(.012 * SR)) * .97], 1)  # leichte Stereo-Breite
with wave.open(ziel, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype('<i2').tobytes())
print(ziel, DAUER, 's', BPM, 'BPM')
