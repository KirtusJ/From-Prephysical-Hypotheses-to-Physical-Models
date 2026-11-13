#!/usr/bin/env python3
"""Independent cross-review test of 'Reversing the field during preparation'.

Model (real space, written from the task statement, not from the author's code):
  step(s): a_c(x) *= exp(-i s h x); (r,l) -> ((r+l),(r-l))/sqrt2; R moves x+1, L moves x-1.
  preparation: site 0, direction d0; m blocks of two steps with sign s_j; after block j
  keep only direction d_j = (-1)^j d0 (unnormalized).
  flight: h = pi/M, delta=(pi/M)^(1/4), sign + for steps < round(0.75/delta^3), then -;
  reads after round(t/delta^3) steps, t in (1.4, 2.3, 3.0): project on x<0 (L) / x>=0 (R).

PREDICATES (fixed before first run; failures are kept, never edited):
 P1  Eq.(1): for 60 random sign words (m in 1..9, both d0, h in {0.37,0.017,1.1}) the
     literal Fourier sum of the retained channel equals
     (-i)^m exp(-ikD-ihC) prod sin(k+h a_j) at 41 momenta, max abs residual < 1e-12,
     and the other channel is < 1e-13.
 P2  Eq.(2): psi_alt(x) = exp(-ih(d0 m + s_m x)) psi_0(x) for m in {1,2,5,8,13}, both d0,
     h in {0.37, 0.017}; max abs residual < 1e-12.
 P3  Table of moments: (abar, v, C) for constant (m=1..40), quartered (m=4..40 step 4),
     alternating (m=1..40), both d0, equal the closed forms to 1e-9.
 P4  Hoelder bound: every sign word of length 2..8, h in {0.37, 0.05}: p_s <= p_0(1+1e-12);
     words that are not alternating have p_s/p_0 < 1 - 1e-9; alternating words have
     |p_s/p_0 - 1| < 1e-12.  Also at h = pi/2 every word of length 2..5 has ratio 1 (1e-12).
 P5  Reproduce all 24 table numbers (M=127,509,2039,8191; yield ratio and
     P(LLR)+P(RRL) for constant/quartered/alternating) to |diff| < 6e-6, and
     P(LLR)=0.14412, P(RRL)=0.14815 for alternating M=8191 to 6e-6.
 P6  Unreported M in {1000, 32749, 131071}: (a) alternating yield ratio within 1e-9 of 1;
     (b) LLR+RRL < 0.5 for all three schedules; (c) quartered LLR+RRL > alternating LLR+RRL
     (the note's 'slightly more' pattern, claimed only at its four M: extension test);
     (d) |log(p_s/p_0)| <= 2E for constant and quartered, E = m h^2 v (the O(E) claim,
     constant 2 chosen by me); (e) partition error of the 8 words < 1e-10.
 P7  Normalised-state claim: for constant and quartered at all 7 M values, the L2 distance
     between the normalised output and the normalised reference
     (-i)^m exp(-ikD-ihC) sin^m(k+h abar) is <= E.
 P8  Trend: alternating LLR+RRL is strictly increasing over M = 127,509,2039,8191,32749,131071.
 P9  (quoted Z data, exploratory) quartered preparation, constant + field in flight,
     delta = 0.1, h = delta^4, m = 316, read at round(2/delta^3) steps: conditional half-line
     means of delta^2 x equal (-1.94994, 1.99657) to 0.01.

RUN LOG: run 1 crashed before writing any JSON (my p0() overflowed in floating point at
 m=772); p0 now uses exact rationals. No predicate was changed.
FOLLOW-UP F1 (added after run 1, exploratory): M=524287 (delta~0.0495), same sub-tests as
 P6 a-e, and switch mass larger than at M=131071 for alternating.
"""
import json, os, sys, itertools, math, time
from fractions import Fraction
import numpy as np

OUT = sys.argv[1] if len(sys.argv) > 1 else None
RS2 = 1.0 / math.sqrt(2.0)


class Walk:
    def __init__(self, half, h, nb=1):
        self.half = half
        self.x = np.arange(-half, half + 1)
        self.h = h
        self.ph = {+1: np.exp(-1j * h * self.x), -1: np.exp(1j * h * self.x)}
        self.R = np.zeros((nb, 2 * half + 1), complex)
        self.L = np.zeros((nb, 2 * half + 1), complex)

    def step(self, s):
        p = self.ph[s]
        r = self.R * p
        l = self.L * p
        nr = (r + l) * RS2
        nl = (r - l) * RS2
        assert not nr[:, -1].any() and not nl[:, 0].any(), "cone hit array edge"
        self.R[:, 1:] = nr[:, :-1]
        self.R[:, 0] = 0
        self.L[:, :-1] = nl[:, 1:]
        self.L[:, -1] = 0


def prepare(signs, h, d0, extra=0):
    m = len(signs)
    w = Walk(2 * m + 2 + extra, h)
    (w.R if d0 == 1 else w.L)[0, w.half] = 1.0
    d = d0
    for s in signs:
        w.step(s)
        w.step(s)
        d = -d
        if d == 1:
            w.L[:] = 0
        else:
            w.R[:] = 0
    return w, d


def sched(name, m):
    if name == "constant":
        return [1] * m
    if name == "alternating":
        return [(-1) ** j for j in range(m)]
    if name == "quartered":
        q = m // 4
        assert m == 4 * q
        return [1] * q + [-1] * (2 * q) + [1] * q
    raise ValueError


def offsets(signs, d0):
    m = len(signs)
    S = [sum(signs[j + 1:]) for j in range(m)]
    a = np.array([2 * S[j] + signs[j] for j in range(m)], float)
    dj = [d0 * (-1) ** (j + 1) for j in range(m)]
    D = sum(dj)
    C = 2 * sum(dj[j] * S[j] for j in range(m))
    return a, D, C


def formula1(signs, h, d0, k):
    a, D, C = offsets(signs, d0)
    m = len(signs)
    out = (-1j) ** m * np.exp(-1j * k * D - 1j * h * C)
    for aj in a:
        out = out * np.sin(k + h * aj)
    return out


def fourier(w, arr, k):
    return np.exp(-1j * np.outer(k, w.x)) @ arr


def p0(m):
    return float(Fraction(math.comb(2 * m, m), 4 ** m))  # run-1 crash fix (float overflow at m=772)


res = {"predicates": {}, "data": {}}
rng = np.random.default_rng(20261113)

# ---- P1
k = np.linspace(-3.1, 3.1, 41) + 0.0123
worst = 0.0
worst_other = 0.0
for trial in range(60):
    m = int(rng.integers(1, 10))
    signs = [int(v) for v in rng.choice([-1, 1], m)]
    d0 = int(rng.choice([-1, 1]))
    h = [0.37, 0.017, 1.1][trial % 3]
    w, d = prepare(signs, h, d0)
    keep, other = (w.R[0], w.L[0]) if d == 1 else (w.L[0], w.R[0])
    worst = max(worst, np.abs(fourier(w, keep, k) - formula1(signs, h, d0, k)).max())
    worst_other = max(worst_other, np.abs(other).max())
res["predicates"]["P1"] = bool(worst < 1e-12 and worst_other < 1e-13)
res["data"]["P1"] = {"max_residual": worst, "other_channel": worst_other}

# ---- P2
worst = 0.0
for m in (1, 2, 5, 8, 13):
    for d0 in (1, -1):
        for h in (0.37, 0.017):
            sg = sched("alternating", m)
            wa, d = prepare(sg, h, d0)
            wz, _ = prepare(sg, 0.0, d0)
            A = wa.R[0] if d == 1 else wa.L[0]
            Z = wz.R[0] if d == 1 else wz.L[0]
            pred = np.exp(-1j * h * (d0 * m + sg[-1] * wa.x)) * Z
            worst = max(worst, np.abs(A - pred).max())
res["predicates"]["P2"] = bool(worst < 1e-12)
res["data"]["P2"] = {"max_residual": worst}

# ---- P3
ok = True
bad = []
for d0 in (1, -1):
    for m in range(1, 41):
        for name in ("constant", "alternating", "quartered"):
            if name == "quartered" and m % 4:
                continue
            a, D, C = offsets(sched(name, m), d0)
            ab, v = a.mean(), a.var()
            if name == "constant":
                exp = (m, (m * m - 1) / 3, -2 * d0 * (m // 2))
            elif name == "quartered":
                exp = (0, (m * m / 4 - 1) / 3, 0)
            else:
                exp = ((-1) ** (m - 1), 0, 2 * d0 * (m // 2))
            if max(abs(ab - exp[0]), abs(v - exp[1]), abs(C - exp[2])) > 1e-9:
                ok = False
                bad.append([name, m, d0, ab, v, C])
            if D != (0 if m % 2 == 0 else -d0):
                ok = False
                bad.append(["D", name, m, d0, D])
res["predicates"]["P3"] = ok
res["data"]["P3"] = {"violations": bad[:10]}

# ---- P4
ok = True
info = {"max_ratio_nonalt": 0.0, "max_dev_alt": 0.0, "max_dev_halfturn": 0.0, "words": 0}
for h in (0.37, 0.05):
    for m in range(2, 9):
        for signs in itertools.product([1, -1], repeat=m):
            w, d = prepare(list(signs), h, 1)
            ps = (np.abs(w.R) ** 2 + np.abs(w.L) ** 2).sum()
            ratio = ps / p0(m)
            info["words"] += 1
            alt = all(signs[j] + signs[j + 1] == 0 for j in range(m - 1))
            if ratio > 1 + 1e-12:
                ok = False
            if alt:
                info["max_dev_alt"] = max(info["max_dev_alt"], abs(ratio - 1))
                ok &= abs(ratio - 1) < 1e-12
            else:
                info["max_ratio_nonalt"] = max(info["max_ratio_nonalt"], ratio)
                ok &= ratio < 1 - 1e-9
for m in range(2, 6):
    for signs in itertools.product([1, -1], repeat=m):
        w, d = prepare(list(signs), math.pi / 2, 1)
        ratio = (np.abs(w.R) ** 2 + np.abs(w.L) ** 2).sum() / p0(m)
        info["max_dev_halfturn"] = max(info["max_dev_halfturn"], abs(ratio - 1))
ok &= info["max_dev_halfturn"] < 1e-12
res["predicates"]["P4"] = bool(ok)
res["data"]["P4"] = info


# ---- flights
def flight(M, name, reads=(1.4, 2.3, 3.0), tsw=0.75):
    delta = (math.pi / M) ** 0.25
    h = math.pi / M
    m = 4 * int(round(delta ** -2.5 / 4))
    nsw = int(round(tsw / delta ** 3))
    rs = [int(round(t / delta ** 3)) for t in reads]
    signs = sched(name, m)
    w, d = prepare(signs, h, 1, extra=rs[-1] + 2)
    psucc = float((np.abs(w.R) ** 2 + np.abs(w.L) ** 2).sum())
    a, D, C = offsets(signs, 1)
    E = m * h * h * a.var()
    # normalised-state distance to translated sin^m reference, via Parseval on an FFT grid
    N = 1 << int(math.ceil(math.log2(8 * m + 16)))
    kk = 2 * math.pi * np.arange(N) / N
    xs = np.arange(-2 * m, 2 * m + 1)
    seg = w.R[0, w.half - 2 * m: w.half + 2 * m + 1]
    refk = (-1j) ** m * np.exp(-1j * kk * D - 1j * h * C) * np.sin(kk + h * a.mean()) ** m
    refx = np.array([(refk * np.exp(1j * kk * x)).mean() for x in xs]) if m <= 200 else \
        (np.exp(1j * np.outer(xs, kk)) @ refk) / N
    dist = float(np.linalg.norm(seg / np.linalg.norm(seg) - refx / np.linalg.norm(refx)))
    # branches
    w.R /= math.sqrt(psucc)
    w.L /= math.sqrt(psucc)
    neg = w.x < 0
    labels = [""]
    n = 0
    for r in rs:
        while n < r:
            w.step(1 if n < nsw else -1)
            n += 1
        R2 = np.concatenate([w.R * neg, w.R * ~neg])
        L2 = np.concatenate([w.L * neg, w.L * ~neg])
        labels = [l + "L" for l in labels] + [l + "R" for l in labels]
        w.R, w.L = R2, L2
    probs = (np.abs(w.R) ** 2 + np.abs(w.L) ** 2).sum(axis=1)
    words = {l: float(p) for l, p in zip(labels, probs)}
    return {"M": M, "delta": delta, "m": m, "schedule": name, "yield_ratio": psucc / p0(m),
            "E": E, "state_distance": dist, "words": words,
            "switch_mass": words["LLR"] + words["RRL"],
            "partition_error": abs(sum(words.values()) - 1), "switch_step": nsw, "read_steps": rs}


TABLE = {127: (12, (0.69167, 0.91431, 1.00000), (0.05567, 0.14111, 0.14013)),
         509: (24, (0.83580, 0.95644, 1.00000), (0.11245, 0.18177, 0.18153)),
         2039: (56, (0.86912, 0.96559, 1.00000), (0.15933, 0.23105, 0.23094)),
         8191: (136, (0.88353, 0.96953, 1.00000), (0.20916, 0.29231, 0.29227))}
NAMES = ("constant", "quartered", "alternating")
runs = {}
for M in (127, 509, 2039, 8191, 1000, 32749, 131071):
    for nm in NAMES:
        t0 = time.time()
        runs[(M, nm)] = flight(M, nm)
        runs[(M, nm)]["seconds"] = time.time() - t0
        print(M, nm, runs[(M, nm)]["m"], round(runs[(M, nm)]["yield_ratio"], 6),
              round(runs[(M, nm)]["switch_mass"], 6), round(time.time() - t0, 1), flush=True)
res["data"]["flights"] = list(runs.values())

maxd = 0.0
ok = True
for M, (m, ys, ws) in TABLE.items():
    for i, nm in enumerate(NAMES):
        r = runs[(M, nm)]
        ok &= r["m"] == m
        maxd = max(maxd, abs(r["yield_ratio"] - ys[i]), abs(r["switch_mass"] - ws[i]))
w8 = runs[(8191, "alternating")]["words"]
maxd = max(maxd, abs(w8["LLR"] - 0.14412), abs(w8["RRL"] - 0.14815))
res["predicates"]["P5"] = bool(ok and maxd < 6e-6)
res["data"]["P5"] = {"max_abs_diff_from_table": maxd, "m_match": bool(ok)}

p6 = {}
NEW = (1000, 32749, 131071)
p6["a"] = all(abs(runs[(M, "alternating")]["yield_ratio"] - 1) < 1e-9 for M in NEW)
p6["b"] = all(runs[(M, nm)]["switch_mass"] < 0.5 for M in NEW for nm in NAMES)
p6["c"] = all(runs[(M, "quartered")]["switch_mass"] > runs[(M, "alternating")]["switch_mass"] for M in NEW)
p6["d"] = all(abs(math.log(runs[(M, nm)]["yield_ratio"])) <= 2 * runs[(M, nm)]["E"]
              for M in NEW for nm in ("constant", "quartered"))
p6["e"] = all(runs[(M, nm)]["partition_error"] < 1e-10 for M in NEW for nm in NAMES)
res["predicates"]["P6"] = p6
res["predicates"]["P7"] = all(r["state_distance"] <= r["E"] for r in runs.values()
                              if r["schedule"] != "alternating")
seq = [runs[(M, "alternating")]["switch_mass"] for M in (127, 509, 2039, 8191, 32749, 131071)]
res["predicates"]["P8"] = all(b > a for a, b in zip(seq, seq[1:]))
res["data"]["P8"] = seq

# ---- P9
delta = 0.1
h = delta ** 4
m = 316
n = int(round(2 / delta ** 3))
w, d = prepare(sched("quartered", m), h, 1, extra=n + 2)
for _ in range(n):
    w.step(1)
pr = np.abs(w.R[0]) ** 2 + np.abs(w.L[0]) ** 2
neg = w.x < 0
Y = delta ** 2 * w.x
means = (float((pr * Y)[neg].sum() / pr[neg].sum()), float((pr * Y)[~neg].sum() / pr[~neg].sum()))
res["data"]["P9"] = {"means": means, "mass_neg": float(pr[neg].sum() / pr.sum())}
res["predicates"]["P9"] = bool(abs(means[0] + 1.94994) < 0.01 and abs(means[1] - 1.99657) < 0.01)

f1 = {}
for nm in NAMES:
    t0 = time.time()
    runs[(524287, nm)] = flight(524287, nm)
    runs[(524287, nm)]["seconds"] = time.time() - t0
    print(524287, nm, runs[(524287, nm)]["m"], runs[(524287, nm)]["yield_ratio"],
          runs[(524287, nm)]["switch_mass"], round(time.time() - t0, 1), flush=True)
res["data"]["flights_F1"] = [runs[(524287, nm)] for nm in NAMES]
Mx = 524287
f1["a"] = abs(runs[(Mx, "alternating")]["yield_ratio"] - 1) < 1e-9
f1["b"] = all(runs[(Mx, nm)]["switch_mass"] < 0.5 for nm in NAMES)
f1["c"] = runs[(Mx, "quartered")]["switch_mass"] > runs[(Mx, "alternating")]["switch_mass"]
f1["d"] = all(abs(math.log(runs[(Mx, nm)]["yield_ratio"])) <= 2 * runs[(Mx, nm)]["E"] for nm in ("constant", "quartered"))
f1["e"] = all(runs[(Mx, nm)]["partition_error"] < 1e-10 for nm in NAMES)
f1["trend"] = runs[(Mx, "alternating")]["switch_mass"] > runs[(131071, "alternating")]["switch_mass"]
f1["state_distance_le_E"] = all(runs[(Mx, nm)]["state_distance"] <= runs[(Mx, nm)]["E"] for nm in ("constant", "quartered"))
res["predicates"]["F1"] = {k: bool(v) for k, v in f1.items()}
res["predicates"]["P6"] = {k: bool(v) for k, v in res["predicates"]["P6"].items()}
res["predicates"]["P7"] = bool(res["predicates"]["P7"]); res["predicates"]["P8"] = bool(res["predicates"]["P8"])
print(json.dumps(res["predicates"], indent=1))
if OUT:
    with open(OUT, "x") as f:   # 'x' refuses to overwrite
        json.dump(res, f, indent=1)
    print("wrote", OUT)
