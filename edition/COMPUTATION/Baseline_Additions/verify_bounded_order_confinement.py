#!/usr/bin/env python3
"""Follow-up to verify_continuation_selection.py, whose predicates S5 (drift of the period-64 staircase; nonzero superlattice band velocity) failed:
the staircase of order-4 gains did not move and its bands were flat to 1e-6.  Hypothesis fixed before this run: a block of constant gain exp(-i phi)
shifts every eigenphase of the step by -phi; the eigenphases of branch 1 fill [-pi/4, pi/4] and of branch 2 [3 pi/4, 5 pi/4] (G9 Lemma 6.1), each an
interval of width pi/2; a step of the gain by delta between adjacent blocks lets a wave pass within its branch only if |delta| < pi/2 (mod 2 pi) and
into the other branch only if |delta - pi| < pi/2.  So gains of order 4 (delta = pi/2) and of order 2 and 3 confine or reverse, and a weak force
needs a step much smaller than the bandwidth pi/2.  Criteria fixed before the run: (C1) largest superlattice band velocity below 1e-4 for
orders 2, 3, 4 and above 1e-2 for orders 8, 12, 24; (C2) transmission through one interface below 0.05 for delta = pi/2 and above 0.3 for
delta = pi/6.  Writes Bounded_Order_Confinement_Results.json; refuses to overwrite."""
import json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reversible_walk_lib import dispersion
OUT = "Bounded_Order_Confinement_Results.json"
if os.path.exists(OUT): sys.exit("refusing to overwrite " + OUT)
R = {}; ok = lambda name, val, **info: R.__setitem__(name, dict(passed=bool(val), **info))
SQ2 = math.sqrt(2)
def step_factory(N, V):
    g = np.exp(-1j * V) / SQ2
    def step(psi):
        s = (psi[:, 0] + psi[:, 1]) * g; dlt = (psi[:, 0] - psi[:, 1]) * g
        out = np.empty_like(psi); out[:, 0] = np.roll(s, 1); out[:, 1] = np.roll(dlt, -1); return out
    return step
def branch_vector(q):
    Uk = np.array([[np.exp(-1j * q), np.exp(-1j * q)], [np.exp(1j * q), -np.exp(1j * q)]]) / SQ2
    lam, vec = np.linalg.eig(Uk); j = int(np.argmin(np.abs(lam - np.exp(-1j * math.asin(math.sin(q) / SQ2))))); v = vec[:, j] / np.linalg.norm(vec[:, j]); return v * np.exp(-1j * np.angle(v[0]))
def packet(N, k0, sigma, x0=0.0):
    ks = 2 * math.pi * np.fft.fftfreq(N); psi_k = np.zeros((N, 2), dtype=complex)
    for i, kk in enumerate(ks):
        d = (kk - k0 + math.pi) % (2 * math.pi) - math.pi
        psi_k[i] = math.exp(-d * d / (4 * sigma ** 2)) * np.exp(-1j * kk * x0) * branch_vector(kk)
    psi = np.fft.ifft(psi_k, axis=0); psi = np.roll(psi, N // 2, axis=0); return psi / np.linalg.norm(psi)
def supercell_U(Vc, K):
    cell = len(Vc); M = np.zeros((2 * cell, 2 * cell), dtype=complex); g = np.exp(-1j * Vc) / SQ2
    for x in range(cell):
        xp, xm = (x + 1) % cell, (x - 1) % cell; fp = np.exp(-1j * K) if x == cell - 1 else 1.0; fm = np.exp(1j * K) if x == 0 else 1.0
        M[2 * xp + 0, 2 * x + 0] += g[x] * fp; M[2 * xp + 0, 2 * x + 1] += g[x] * fp
        M[2 * xm + 1, 2 * x + 0] += g[x] * fm; M[2 * xm + 1, 2 * x + 1] -= g[x] * fm
    return M
# ---- band velocities of staircases of order q with block length L
L = 16; rows = []
for q in (2, 3, 4, 6, 8, 12, 24):
    cell = q * L; Vc = (2 * math.pi / q) * np.floor(np.arange(cell) / L); h = 1e-5; speeds = []
    for K in np.linspace(-math.pi, math.pi, 17, endpoint=False):
        ph = np.sort(np.angle(np.linalg.eigvals(supercell_U(Vc, K)))); ph2 = np.sort(np.angle(np.linalg.eigvals(supercell_U(Vc, K + h))))
        speeds.extend((((ph2 - ph + math.pi) % (2 * math.pi) - math.pi) / h / cell).tolist())
    speeds = np.array(speeds); rows.append(dict(order=q, step_delta=2 * math.pi / q, supercell_sites=cell, largest_band_velocity=float(np.max(np.abs(speeds))), rms_band_velocity=float(np.sqrt(np.mean(speeds ** 2)))))
    print(rows[-1], flush=True)
ok("C1_bands_flat_for_orders_2_3_4_and_dispersive_for_8_12_24", all((r["largest_band_velocity"] < 1e-4) == (r["order"] <= 4) for r in rows) and all(r["largest_band_velocity"] > 1e-2 for r in rows if r["order"] >= 8),
   rows=rows, block_length=L, note="sorted eigenphases differentiated numerically; a crossing can lower a computed velocity, not create one. Order 6 (delta = pi/3 < pi/2) is reported, not part of the criterion")
# ---- spread of a localized start under each staircase over 1024 steps (positions relative to the start; the walk never reaches the far side of the ring)
N = 4096; xs = np.arange(N) - N // 2; rows2 = []
for q in (2, 3, 4, 6, 8, 12, 24):
    V = (2 * math.pi / q) * np.floor(xs / L); st = step_factory(N, V); psi = np.zeros((N, 2), dtype=complex); psi[N // 2, 0] = 1.0; cur = psi; rec = []
    for t in range(1, 1025):
        cur = st(cur)
        if t in (64, 256, 1024): p = (np.abs(cur) ** 2).sum(1); rec.append(dict(t=t, rms_distance=float(np.sqrt((p * xs ** 2).sum())), mean=float((p * xs).sum())))
    rows2.append(dict(order=q, rows=rec))
ok("C1b_localized_start_stays_bounded_for_orders_2_3_4", all(r["rows"][-1]["rms_distance"] < 3 * L for r in rows2 if r["order"] <= 4) and all(r["rows"][-1]["rms_distance"] > 10 * L for r in rows2 if r["order"] >= 12), rows=rows2)
# ---- transmission through one interface: gain 0 for x < 0 and exp(-i delta) for x >= 0 (and 0 again far away, at |x| >= N/4)
N = 8192; xs = np.arange(N) - N // 2; rows3 = []
for delta in (math.pi / 12, math.pi / 6, math.pi / 4, math.pi / 3, math.pi / 2, 2 * math.pi / 3, math.pi):
    V = np.where((xs >= 0) & (xs < N // 4), delta, 0.0); st = step_factory(N, V)
    cur = packet(N, 0.3, 0.03, x0=-120.0); p0 = (np.abs(cur) ** 2).sum(1); vel = float(dispersion(np.array(0.3))[1])
    # direction convention: run 20 steps and see which way the packet moves; if it moves left, start it on the right instead
    probe = cur.copy()
    for _ in range(20): probe = st(probe)
    moved = float((((np.abs(probe) ** 2).sum(1)) * xs).sum() - (p0 * xs).sum())
    if moved < 0:
        V = np.where((xs <= 0) & (xs > -N // 4), delta, 0.0); st = step_factory(N, V); cur = packet(N, 0.3, 0.03, x0=120.0)
    for _ in range(400): cur = st(cur)
    p = (np.abs(cur) ** 2).sum(1)
    transmitted = float(p[xs > 0].sum()) if moved >= 0 else float(p[xs < 0].sum())
    rows3.append(dict(delta=delta, delta_over_pi=delta / math.pi, transmitted_probability=transmitted, packet_speed=abs(vel), moved_right=moved >= 0))
    print(rows3[-1], flush=True)
T = {round(r["delta_over_pi"], 4): r["transmitted_probability"] for r in rows3}
ok("C2_transmission_vanishes_at_half_bandwidth_step", T[0.5] < 0.05 and T[round(1 / 6, 4)] > 0.3, rows=rows3,
   note="branch-1 packet at k0 = 0.3, width 0.03 in k, 400 steps; the interface step delta is the gain ratio between the two regions. Eigenphase intervals: branch 1 [-pi/4, pi/4], branch 2 [3 pi/4, 5 pi/4] (G9 Lemma 6.1): within-branch passage needs |delta| < pi/2, cross-branch passage |delta - pi| < pi/2")
R["_summary"] = dict(predicates=sum(1 for k in R if not k.startswith("_")), passed=sum(1 for k, v in R.items() if not k.startswith("_") and v["passed"]), numpy=np.__version__)
json.dump(R, open(OUT, "w"), indent=1, default=str)
for k, v in R.items():
    if not k.startswith("_"): print(("PASS " if v["passed"] else "FAIL ") + k)
print(R["_summary"])
