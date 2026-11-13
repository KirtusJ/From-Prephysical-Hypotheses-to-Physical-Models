#!/usr/bin/env python3
"""Director Z cross-check of Director G's paper "Following one prepared walk with successive position readings" (pull request 2, commit
6bb2d14).  Nothing is imported from Director G's programs.  The model is this participant's reading of the papers: the real-space walk of
crosscheck_director_g_two_rays.py (phase exp(-i h x) before each step, Hadamard coin, shift), the direction-switch preparation with the field
on, then free flight with the field F(t) and three coherent readings of the side of the origin (projection on x >= 0 or on x < 0, sheets
and sites otherwise unread).  F = 1, readings at scaled times 1.4, 2.3, 3.0; delta = 0.1 and 0.05; h = delta^4, time step delta^3,
Y = delta^2 x.
Predicates, fixed before the run:
 S0  the sequential-projection inequality of step 4 of the paper: for 2000 random instances in dimension 12 (unit vector v, one to eight
     random orthogonal projections Q_j, v_K = Q_K ... Q_1 v, S = sum ||(1 - Q_j) v||^2, L = 1 - ||v_K||^2):
     1 - Re<v, v_K> <= sqrt(S L), ||v - v_K||^2 <= S and L <= 4 S, each with slack 1e-12;
 S1  constant field: at both scales the two side words that stay on one side carry at least 0.97 in total and each is within 0.03 of
     half of it;
 S2  field reversed at scaled time 0.75: at both scales the two side words of the limit rays -+A(t), A(t) = t^2/2 - (t - 0.75)^2, which
     are (+, +, -) and (-, -, +), carry less than 1/2 in total (the adverse finite control of the paper, at smaller scales), and the two
     side words of the rays with the preparation offset, -+(A(t) + t m h/delta), carry more than the two words of the limit rays.
Recorded without a predicate: all eight word probabilities in the four runs.
Writes Crosscheck_Director_G_Position_Records_Results.json; refuses to overwrite.  Seed fixed and reported (S0 only)."""
import json, math, os, sys
import numpy as np
OUT = "Crosscheck_Director_G_Position_Records_Results.json"
if os.path.exists(OUT): sys.exit("refusing to overwrite " + OUT)
R = {}; ok = lambda name, val, **info: R.__setitem__(name, dict(passed=bool(val), **info))
SEED = 20261120; rng = np.random.default_rng(SEED); RT2 = math.sqrt(2.0)
worst = dict(a=-1.0, b=-1.0, c=-1.0)
for _ in range(2000):
    n = 12; v = rng.normal(size=n) + 1j * rng.normal(size=n); v /= np.linalg.norm(v); w = v.copy(); Ssum = 0.0
    for _ in range(int(rng.integers(1, 9))):
        r = int(rng.integers(1, n)); q, _r = np.linalg.qr(rng.normal(size=(n, r)) + 1j * rng.normal(size=(n, r))); Q = q @ q.conj().T
        Ssum += float(np.linalg.norm(v - Q @ v) ** 2); w = Q @ w
    L = 1 - float(np.linalg.norm(w) ** 2)
    worst["a"] = max(worst["a"], 1 - float(np.vdot(v, w).real) - math.sqrt(max(Ssum * L, 0.0))); worst["b"] = max(worst["b"], float(np.linalg.norm(v - w) ** 2) - Ssum); worst["c"] = max(worst["c"], L - 4 * Ssum)
ok("S0_sequential_projection_inequality", all(x <= 1e-12 for x in worst.values()), largest_violation_of_each=worst, seed=SEED)
TIMES = (1.4, 2.3, 3.0); TAU = 0.75
def run(delta, reverse):
    h = delta ** 4; m = int(round(delta ** -2.5 / 2.0)) * 2; steps = [int(round(t / delta ** 3)) for t in TIMES]; sw = int(round(TAU / delta ** 3)) if reverse else None
    X = 2 * m + steps[-1] + 8; x = np.arange(-X, X + 1); ph = {1: np.exp(-1j * h * x), -1: np.exp(1j * h * x)}; pos = x >= 0
    def step(r, l, sgn):
        r = r * ph[sgn]; l = l * ph[sgn]; a = (r + l) / RT2; b = (r - l) / RT2; r2 = np.zeros_like(a); l2 = np.zeros_like(b); r2[1:] = a[:-1]; l2[:-1] = b[1:]; return r2, l2
    r = np.zeros(2 * X + 1, dtype=complex); l = np.zeros(2 * X + 1, dtype=complex); r[X] = 1.0; keep = "L"
    for _ in range(m):
        r, l = step(*step(r, l, 1), 1)
        if keep == "L": r[:] = 0
        else: l[:] = 0
        keep = "R" if keep == "L" else "L"
    p_word = float((np.abs(r) ** 2 + np.abs(l) ** 2).sum()); branches = {"": (r, l)}; n = 0
    for k, target in enumerate(steps):
        new = {}
        for word, (r, l) in branches.items():
            for i in range(n, target): r, l = step(r, l, -1 if (sw is not None and i >= sw) else 1)
            new[word + "+"] = (np.where(pos, r, 0), np.where(pos, l, 0)); new[word + "-"] = (np.where(pos, 0, r), np.where(pos, 0, l))
        branches = new; n = target
    probs = {w: float((np.abs(r) ** 2 + np.abs(l) ** 2).sum()) / p_word for w, (r, l) in branches.items()}
    A = [t * t / 2 - (max(t - TAU, 0.0) ** 2 if reverse else 0.0) for t in TIMES]; off = [a + t * m * h / delta for a, t in zip(A, TIMES)]
    word = lambda vals, s: "".join("+" if s * v >= 0 else "-" for v in vals)
    lim = {word(A, 1), word(A, -1)}; offw = {word(off, 1), word(off, -1)}
    return dict(delta=delta, reversed_field=reverse, blocks=m, total=sum(probs.values()), words=probs, limit_ray_words=sorted(lim), offset_ray_words=sorted(offw),
                mass_of_limit_ray_words=sum(probs[w] for w in lim), mass_of_offset_ray_words=sum(probs[w] for w in offw), scaled_positions_of_limit_ray=A, scaled_positions_of_offset_ray=off)
rows = []
for delta in (0.1, 0.05):
    for rev in (False, True): rows.append(run(delta, rev)); print({k: v for k, v in rows[-1].items() if k != "words"}, flush=True); print(rows[-1]["words"], flush=True)
const = [r for r in rows if not r["reversed_field"]]; rev = [r for r in rows if r["reversed_field"]]
ok("S1_constant_field_side_words_stay_on_one_side", all(r["mass_of_limit_ray_words"] >= 0.97 and abs(r["words"]["+++"] - r["mass_of_limit_ray_words"] / 2) <= 0.03 for r in const))
ok("S2_reversal_finite_control_follows_the_offset_rays", all(r["mass_of_limit_ray_words"] < 0.5 and r["mass_of_offset_ray_words"] > r["mass_of_limit_ray_words"] for r in rev), rows=rows)
R["_summary"] = dict(predicates=3, passed=sum(1 for k, v in R.items() if not k.startswith("_") and v["passed"]), seed=SEED, numpy=np.__version__)
json.dump(R, open(OUT, "w"), indent=1, default=str)
for k, v in R.items():
    if not k.startswith("_"): print(("PASS " if v["passed"] else "FAIL ") + k)
print(R["_summary"])
