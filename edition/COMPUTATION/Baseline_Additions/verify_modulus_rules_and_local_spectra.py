#!/usr/bin/env python3
"""Fourth Director Z session.  Predicates fixed before the run, after the failures recorded in Continuation_Selection_Results.json (S5) and
Bounded_Order_Confinement_Results.json (C1, C1b), whose band-velocity computation is discarded as an instrument (it returned velocities above 1
and below the directly observed spread).
 M1  On the signed arc digraph of a ring, a rule mu(S) = sum_y phi(|v_S(y)|), phi(0) = 0, consistent under continuation has phi(n) = n^2 phi(1):
     the linear consistency equations over sampled events have a one-dimensional solution space spanned by n^2.
 M2  Achievability used in the proof: for a = 1..6 there are a length and a site at which at least a walks of gain +1 arrive from the left and
     at least one walk of gain +1 arrives from the right.
 L1  The spectrum of the free step lies on the two arcs |theta| <= pi/4 and |theta - pi| <= pi/4 (G9 Lemma 6.1).
 L2  Exact (rational arithmetic, degrees): the intersection of the q rotations of the two arcs by multiples of 360/q is the whole set for q = 1, 2,
     four points for q = 4, and empty for q = 3 and 5 <= q <= 48.
 L3  Staircases of gains of order q with block length L: for q in (3, 4, 6) and L in (4, 16, 64) a walk from one vertex has root-mean-square
     distance below 1.5 L (q/4 + 1) + 5 after 2048 steps; for q = 2 and L = 16 it exceeds 100 after 1024 steps.  L = 1, 2 are recorded only.
Writes Modulus_Rules_and_Local_Spectra_Results.json; refuses to overwrite.  Seed fixed and reported."""
import json, math, os, sys
from fractions import Fraction as Fr
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reversible_walk_lib import ring_step
OUT = "Modulus_Rules_and_Local_Spectra_Results.json"
if os.path.exists(OUT): sys.exit("refusing to overwrite " + OUT)
R = {}; ok = lambda name, val, **info: R.__setitem__(name, dict(passed=bool(val), **info))
SQ2 = math.sqrt(2); SEED = 20261113; rng = np.random.default_rng(SEED)

# ---------------- M1, M2: walk counts by end vertex and sign on a ring long enough that walks of length j do not wrap
N = 40; A = ring_step(N); V = 2 * N; start = 2 * (N // 2)
pos = np.zeros(V, dtype=np.int64); neg = np.zeros(V, dtype=np.int64); pos[start] = 1
Ap = (A > 0).astype(np.int64); An = (A < 0).astype(np.int64); counts = {}
for j in range(1, 15):
    pos, neg = Ap @ pos + An @ neg, Ap @ neg + An @ pos; counts[j] = (pos.copy(), neg.copy())
ach = {}
for a in range(1, 7):
    found = None
    for j in sorted(counts):
        p, n = counts[j]
        for x in range(N):
            if p[2 * x] >= a and p[2 * x + 1] >= 1: found = dict(length=j, site=x - N // 2, plus_walks_from_left=int(p[2 * x]), plus_walks_from_right=int(p[2 * x + 1])); break
        if found: break
    ach[a] = found
ok("M2_amplitudes_a_and_1_at_one_site_are_achievable", all(ach[a] is not None for a in ach), witnesses=ach)
# sampled events at length 12: choose for every end vertex numbers of + and - walks (0..count); amplitude = plus - minus.  Unknowns phi(1..K).
j = 12; p, n = counts[j]; K = 12; rows = []
for trial in range(4000):
    amp = np.zeros(V, dtype=np.int64)
    sites = rng.choice(N, size=rng.integers(1, 4), replace=False)
    for x in sites:
        for c in (0, 1):
            v = 2 * x + c; hi = min(int(p[v]), 4); lo = min(int(n[v]), 4)
            amp[v] = rng.integers(0, hi + 1) - rng.integers(0, lo + 1)
    if not amp.any(): continue
    ext = A.astype(np.int64) @ amp
    if max(np.abs(ext).max(), np.abs(amp).max()) > K: continue
    row = np.zeros(K + 1)
    for m in np.abs(ext): row[m] += 1
    for m in np.abs(amp): row[m] -= 2                                 # c = 2 from the single-walk events
    rows.append(row[1:])
M = np.array(rows); _, s, vt = np.linalg.svd(M); rank = int(np.sum(s > 1e-9)); null = vt[rank:]
sq = np.arange(1, K + 1) ** 2.0; sq /= np.linalg.norm(sq)
ok("M1_consistent_modulus_rule_is_quadratic", null.shape[0] == 1 and min(np.linalg.norm(null[0] - sq), np.linalg.norm(null[0] + sq)) < 1e-9,
   events_used=len(rows), unknowns=K, rank=rank, solution_normalized_to_phi1=[float(t / null[0][0]) for t in null[0]] if null.shape[0] == 1 else None, seed=SEED,
   note="equations sum_y phi(|(A v)(y)|) = 2 sum_y phi(|v(y)|) over sampled events of length 12 with integer amplitudes of modulus at most 12; every sampled amplitude vector is the vector of an event because it is bounded by the walk counts")

# ---------------- L1: spectrum of the free step
ev = np.linalg.eigvals(ring_step(64) / SQ2); th = np.angle(ev)
ok("L1_free_spectrum_on_two_arcs", bool(np.all((np.abs(th) <= math.pi / 4 + 1e-9) | (np.abs(np.abs(th) - math.pi) <= math.pi / 4 + 1e-9))), largest_modulus_defect=float(np.max(np.abs(np.abs(ev) - 1))))

# ---------------- L2: exact intersection of rotated arcs (degrees as fractions)
def arcs_rot(shift):                                  # closed arcs [lo, hi] mod 360 of the set rotated by `shift` degrees
    return [((Fr(-45) + shift) % 360, Fr(90)), ((Fr(135) + shift) % 360, Fr(90))]          # (start, length)
def contains(arcs, t):
    return any(((t - st) % 360) <= ln for st, ln in arcs)
def intersection_measure_and_points(q):
    # candidate breakpoints: all arc endpoints of all rotations; test midpoints of consecutive breakpoints and the breakpoints themselves
    sets = [arcs_rot(Fr(360 * jj, q)) for jj in range(q)]
    bps = sorted({(st + d) % 360 for arcs in sets for st, ln in arcs for d in (Fr(0), ln)})
    meas = Fr(0); pts = []
    for i, b in enumerate(bps):
        nb = bps[(i + 1) % len(bps)]; width = (nb - b) % 360 if len(bps) > 1 else Fr(360); mid = (b + width / 2) % 360
        if width > 0 and all(contains(arcs, mid) for arcs in sets): meas += width
        if all(contains(arcs, b) for arcs in sets): pts.append(b)
    return meas, pts
rows = []
for q in range(1, 49):
    meas, pts = intersection_measure_and_points(q); rows.append(dict(q=q, measure_degrees=str(meas), isolated_or_boundary_points=len(pts), points=[str(t) for t in pts][:8]))
by = {r["q"]: r for r in rows}
ok("L2_common_local_spectrum_only_for_orders_1_2_and_four_points_for_order_4",
   by[1]["measure_degrees"] == "180" and by[2]["measure_degrees"] == "180" and by[4]["measure_degrees"] == "0" and sorted(by[4]["points"]) == sorted(["45", "135", "225", "315"])
   and all(by[q]["measure_degrees"] == "0" and by[q]["isolated_or_boundary_points"] == 0 for q in range(3, 49) if q != 4), rows=rows,
   note="exact arithmetic in degrees; the set is the two closed arcs of half-width 45 about 0 and 180")

# ---------------- L3: spreads under staircases
def step_factory(Nn, Vv):
    g = np.exp(-1j * Vv) / SQ2
    def step(psi):
        s_ = (psi[:, 0] + psi[:, 1]) * g; d_ = (psi[:, 0] - psi[:, 1]) * g
        out = np.empty_like(psi); out[:, 0] = np.roll(s_, 1); out[:, 1] = np.roll(d_, -1); return out
    return step
Nn = 8192; xs = np.arange(Nn) - Nn // 2; rows = []
for q in (2, 3, 4, 6):
    for L in (1, 2, 4, 16, 64):
        Vv = (2 * math.pi / q) * np.floor(xs / L); st = step_factory(Nn, Vv); cur = np.zeros((Nn, 2), dtype=complex); cur[Nn // 2, 0] = 1.0; rec = {}
        for t in range(1, 2049):
            cur = st(cur)
            if t in (256, 1024, 2048): pr = (np.abs(cur) ** 2).sum(1); rec[t] = float(np.sqrt((pr * xs ** 2).sum()))
        rows.append(dict(order=q, block_length=L, rms_distance=rec, bound=1.5 * L * (q / 4 + 1) + 5)); print(rows[-1], flush=True)
ok("L3_staircases_of_order_3_4_6_confine_and_order_2_does_not",
   all(r["rms_distance"][2048] < r["bound"] for r in rows if r["order"] in (3, 4, 6) and r["block_length"] in (4, 16, 64))
   and all(r["rms_distance"][1024] > 100 for r in rows if r["order"] == 2 and r["block_length"] == 16), rows=rows,
   note="walk from one vertex on a ring of 8192 sites; block lengths 1 and 2 are recorded and are not part of the criterion; block length 1 is the linear gain of order q")
R["_summary"] = dict(predicates=sum(1 for k in R if not k.startswith("_")), passed=sum(1 for k, v in R.items() if not k.startswith("_") and v["passed"]), seed=SEED, numpy=np.__version__)
json.dump(R, open(OUT, "w"), indent=1, default=str)
for k, v in R.items():
    if not k.startswith("_"): print(("PASS " if v["passed"] else "FAIL ") + k)
print(R["_summary"])
