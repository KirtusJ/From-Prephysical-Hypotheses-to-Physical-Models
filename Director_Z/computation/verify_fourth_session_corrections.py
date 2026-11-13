#!/usr/bin/env python3
"""Fourth Director Z session: corrected predicates after two failures in Modulus_Rules_and_Local_Spectra_Results.json, which is kept.
 M1 failed there through the checking program: the unknowns phi(9..12) occurred in no equation, so the solution space had spurious dimensions.
    Here the unknowns are the moduli that occur.
 L3 failed there on the substance: staircases with block length 4 are not confined (root-mean-square distance 160, 102 and 27 sites after
    2048 steps for the orders 3, 4, 6), and block lengths 1 and 2 spread ballistically.  Criteria fixed before this run:
    N1  block length 1 (the linear gain of order q = 3, 4, 6): the distance doubles between 1024 and 2048 steps (ratio in (1.9, 2.1));
    N2  block lengths 16 and 64, orders 3, 4, 6: the distance at 2048 steps is below 1.5 L (q/4 + 1) + 5 (as observed before; restated);
    N3  a staircase of order 4 does not follow the field of its mean slope: for L = 16, 64, 256 the displacement of a packet after an eighth of
        the period of the mean field is less than 0.8 of the displacement under the linear gain.  L = 256 was not computed before.
Writes Fourth_Session_Corrections_Results.json; refuses to overwrite."""
import json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reversible_walk_lib import ring_step
OUT = "Fourth_Session_Corrections_Results.json"
if os.path.exists(OUT): sys.exit("refusing to overwrite " + OUT)
R = {}; ok = lambda name, val, **info: R.__setitem__(name, dict(passed=bool(val), **info))
SQ2 = math.sqrt(2); SEED = 20261113; rng = np.random.default_rng(SEED)
# ---------------- M1 corrected
N = 40; A = ring_step(N); V = 2 * N; start = 2 * (N // 2)
pos = np.zeros(V, dtype=np.int64); neg = np.zeros(V, dtype=np.int64); pos[start] = 1
Ap = (A > 0).astype(np.int64); An = (A < 0).astype(np.int64)
for j in range(12): pos, neg = Ap @ pos + An @ neg, Ap @ neg + An @ pos
raw = []
for trial in range(4000):
    amp = np.zeros(V, dtype=np.int64)
    for x in rng.choice(N, size=rng.integers(1, 4), replace=False):
        for c in (0, 1):
            v = 2 * x + c; amp[v] = rng.integers(0, min(int(pos[v]), 4) + 1) - rng.integers(0, min(int(neg[v]), 4) + 1)
    if amp.any(): raw.append((np.abs(A.astype(np.int64) @ amp), np.abs(amp)))
K = max(int(e.max()) for e, a in raw); rows = []
for e, a in raw:
    row = np.zeros(K + 1)
    for m in e: row[m] += 1
    for m in a: row[m] -= 2
    rows.append(row[1:])
M = np.array(rows); occurring = [m for m in range(1, K + 1) if np.any(M[:, m - 1] != 0)]; M = M[:, [m - 1 for m in occurring]]
_, s, vt = np.linalg.svd(M); rank = int(np.sum(s > 1e-9)); null = vt[rank:]
sq = np.array(occurring, dtype=float) ** 2; sq /= np.linalg.norm(sq)
ok("M1_consistent_modulus_rule_is_quadratic", null.shape[0] == 1 and min(np.linalg.norm(null[0] - sq), np.linalg.norm(null[0] + sq)) < 1e-9, events_used=len(rows), moduli_occurring=occurring, rank=rank,
   solution_normalized_to_phi1=[float(t / null[0][0]) for t in null[0]] if null.shape[0] == 1 else None, seed=SEED,
   first_run="in verify_modulus_rules_and_local_spectra.py the unknowns ran to 12 although no modulus above 8 occurred; the predicate failed through the program, not the statement")
# controls: the same equations reject phi(n) = n and phi(n) = n^4, and for the trivial-gain ring digraph (counting) accept phi(n) = n
lin = np.array(occurring, dtype=float); qu = lin ** 4
ok("M1_controls_linear_and_quartic_rejected_on_the_signed_ring", np.abs(M @ lin).max() > 0.5 and np.abs(M @ qu).max() > 0.5, largest_defect_linear=float(np.abs(M @ lin).max()), largest_defect_quartic=float(np.abs(M @ qu).max()))
A0 = np.abs(A).astype(np.int64); rows0 = []
for e_, a_ in raw:
    amp = a_                                         # non-negative amplitudes: numbers of walks, trivial gains
    e0 = A0 @ amp; row = np.zeros(int(e0.max()) + 1)
    rows0.append((e0, amp))
defect = max(abs(int(e0.sum()) - 2 * int(a0.sum())) for e0, a0 in rows0)
ok("M1_control_counting_is_consistent_with_trivial_gains", defect == 0, note="with all gains +1 and phi(n) = n the rule is the number of walks: sum of (A0 v) equals 2 sum of v for every event")
# ---------------- N1, N2: spreads
def step_factory(Nn, Vv):
    g = np.exp(-1j * Vv) / SQ2
    def step(psi):
        s_ = (psi[:, 0] + psi[:, 1]) * g; d_ = (psi[:, 0] - psi[:, 1]) * g
        out = np.empty_like(psi); out[:, 0] = np.roll(s_, 1); out[:, 1] = np.roll(d_, -1); return out
    return step
Nn = 8192; xs = np.arange(Nn) - Nn // 2; rows = []
for q in (3, 4, 6):
    for L in (1, 16, 64):
        st = step_factory(Nn, (2 * math.pi / q) * np.floor(xs / L)); cur = np.zeros((Nn, 2), dtype=complex); cur[Nn // 2, 0] = 1.0; rec = {}
        for t in range(1, 2049):
            cur = st(cur)
            if t in (1024, 2048): pr = (np.abs(cur) ** 2).sum(1); rec[t] = float(np.sqrt((pr * xs ** 2).sum()))
        rows.append(dict(order=q, block_length=L, rms_distance=rec, ratio=rec[2048] / rec[1024], bound=1.5 * L * (q / 4 + 1) + 5))
ok("N1_linear_gain_of_order_3_4_6_spreads_ballistically", all(1.9 < r["ratio"] < 2.1 for r in rows if r["block_length"] == 1), rows=[r for r in rows if r["block_length"] == 1],
   note="rational field: ballistic propagation with revivals (Cedzich et al. 2013, proved there); G9 Section 6.2 reports the bounded distance over four periods only")
ok("N2_long_blocks_confine_up_to_2048_steps", all(r["rms_distance"][2048] < r["bound"] for r in rows if r["block_length"] in (16, 64)), rows=[r for r in rows if r["block_length"] != 1],
   note="an observation over 2048 steps; the gains are periodic in position, so exact confinement is not expected at all times")
# ---------------- N3: staircase against the linear gain of its mean slope
def branch_vector(qq):
    Uk = np.array([[np.exp(-1j * qq), np.exp(-1j * qq)], [np.exp(1j * qq), -np.exp(1j * qq)]]) / SQ2
    lam, vec = np.linalg.eig(Uk); jx = int(np.argmin(np.abs(lam - np.exp(-1j * math.asin(math.sin(qq) / SQ2))))); v = vec[:, jx] / np.linalg.norm(vec[:, jx]); return v * np.exp(-1j * np.angle(v[0]))
def packet(Nn, k0, sigma):
    ks = 2 * math.pi * np.fft.fftfreq(Nn); psi_k = np.zeros((Nn, 2), dtype=complex)
    for i, kk in enumerate(ks):
        d = (kk - k0 + math.pi) % (2 * math.pi) - math.pi
        if abs(d) < 12 * sigma: psi_k[i] = math.exp(-d * d / (4 * sigma ** 2)) * branch_vector(kk)
    psi = np.fft.ifft(psi_k, axis=0); psi = np.roll(psi, Nn // 2, axis=0); return psi / np.linalg.norm(psi)
def mean_pos(psi): return float((((np.abs(psi) ** 2).sum(1)) * xs).sum())
rows = []; psi0 = packet(Nn, 0.3, 0.03); c0 = mean_pos(psi0)
for L in (16, 64, 256):
    Phi = math.pi / (2 * L); T = L // 2
    a = psi0.copy(); b = psi0.copy(); sa = step_factory(Nn, (math.pi / 2) * np.floor(xs / L)); sb = step_factory(Nn, Phi * xs.astype(float))
    for _ in range(T): a = sa(a); b = sb(b)
    pa = (np.abs(a) ** 2).sum(1)
    rows.append(dict(block_length=L, steps=T, staircase_displacement=mean_pos(a) - c0, linear_gain_displacement=mean_pos(b) - c0, ratio=(mean_pos(a) - c0) / (mean_pos(b) - c0),
                     fraction_on_the_far_side_of_the_start=float(pa[(xs - c0) * np.sign(mean_pos(b) - c0) < -5].sum())))
ok("N3_order_4_staircase_falls_short_of_its_mean_field", all(r["ratio"] < 0.8 for r in rows), rows=rows,
   note="packet at k0 = 0.3 on branch 1, width 0.03 in k (about 17 sites in position); the instances L = 16 and 64 repeat G9 Section 6.2 with the mean position in place of the circular centroid")
R["_summary"] = dict(predicates=sum(1 for k in R if not k.startswith("_")), passed=sum(1 for k, v in R.items() if not k.startswith("_") and v["passed"]), seed=SEED, numpy=np.__version__)
json.dump(R, open(OUT, "w"), indent=1, default=str)
for k, v in R.items():
    if not k.startswith("_"): print(("PASS " if v["passed"] else "FAIL ") + k, {kk: vv for kk, vv in v.items() if kk in ("rows", "solution_normalized_to_phi1", "moduli_occurring")})
print(R["_summary"])
