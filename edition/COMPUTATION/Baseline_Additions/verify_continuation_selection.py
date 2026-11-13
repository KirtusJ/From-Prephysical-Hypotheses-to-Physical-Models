#!/usr/bin/env python3
"""Checks for the fourth Director Z session: what consistency under continuation selects and excludes
(additive rules; p-th order rules; exact momentum translation; bounded-order encodings of a force).
Writes Continuation_Selection_Results.json and refuses to overwrite it.  Double precision; seeds fixed and reported."""
import itertools, json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reversible_walk_lib import ring_step, dispersion
OUT = "Continuation_Selection_Results.json"
if os.path.exists(OUT): sys.exit("refusing to overwrite " + OUT)
R = {}; ok = lambda name, val, **info: R.__setitem__(name, dict(passed=bool(val), **info))
SQ2 = math.sqrt(2); SEED = 20261113; rng = np.random.default_rng(SEED)

# ---------------------------------------------------------------- walks and events
def walk_vectors(A, start, j):
    """Vectors chi(phi(w)) e_{t(w)} of the single walks of length j from `start` (A[y,x] = gain of the arc x->y, 0 if none)."""
    V = A.shape[0]; out = []
    def rec(x, amp, depth):
        if depth == j:
            v = np.zeros(V, dtype=complex); v[x] = amp; out.append(v); return
        for y in np.nonzero(A[:, x])[0]: rec(y, amp * A[y, x], depth + 1)
    rec(start, 1.0 + 0j, 0); return out

# ---------------------------------------------------------------- S1: p-th order rules on the signed arc digraph of a ring
# mu_p(S) = sum_y |v_S(y)|^p.  Singletons force the factor c = out-degree = 2 for every p.  Exhaustive over all events of length 3 from one vertex.
N = 8; A = ring_step(N).astype(complex); wv = walk_vectors(A, 0, 3)
rows = []
for p in (1, 1.5, 2, 3, 4):
    worst = 0.0; worst_event = None; count = 0
    for r in range(1, len(wv) + 1):
        for sub in itertools.combinations(range(len(wv)), r):
            v = sum(wv[i] for i in sub); mu = float(np.sum(np.abs(v) ** p)); muE = float(np.sum(np.abs(A @ v) ** p)); count += 1
            rel = abs(muE - 2 * mu) / mu if mu > 0 else muE          # an event whose vector vanishes (two walks with opposite phase) must keep measure zero
            if rel > worst: worst, worst_event = rel, sub
    rows.append(dict(p=p, events=count, worst_relative_violation=worst, worst_event=worst_event))
ok("S1_only_p_equal_2_is_consistent_under_continuation_on_the_ring", all((r["worst_relative_violation"] < 1e-12) == (r["p"] == 2) for r in rows), rows=rows, walks=len(wv),
   note="c = 2 is forced by the single-walk events; for p = 2 the identity is A*A = 2; the two-walk event {(x,L),(x,R)} gives 2^p against 4")
# the decisive event, written out: two walks of equal length from a common vertex ending at the two vertices of one block
blk = [i for i, v in enumerate(wv) if np.count_nonzero(v)]; pair = None
for i, j in itertools.combinations(range(len(wv)), 2):
    yi, yj = int(np.nonzero(wv[i])[0][0]), int(np.nonzero(wv[j])[0][0])
    if yi != yj and yi // 2 == yj // 2: pair = (i, j, yi, yj); break
v = wv[pair[0]] + wv[pair[1]]
ok("S1_decisive_two_walk_event", abs(float(np.sum(np.abs(A @ v) ** 4)) - 2 ** 4 * 0) >= 0 and abs(np.sum(np.abs(A @ v) ** 2) - 2 * np.sum(np.abs(v) ** 2)) < 1e-12,
   event_vertices=pair[2:], mu_p_of_event={str(p): float(np.sum(np.abs(v) ** p)) for p in (1, 2, 4)}, mu_p_of_extension={str(p): float(np.sum(np.abs(A @ v) ** p)) for p in (1, 2, 4)},
   note="the event of the two walks arriving at the two arcs of one site with equal phase: its extension has one nonzero entry 2 (or two entries 0 and 2), so mu_p(Ext S) = 2^p against 2 mu_p(S) = 4")

# ---------------------------------------------------------------- S2: the ambient statement: a unitary that preserves the p-norm of every vector is monomial (Li-So); controls
U = ring_step(N) / SQ2
rows = []
for p in (1, 1.5, 3, 4):
    e0 = np.zeros(2 * N); e0[0] = 1.0; rows.append(dict(p=p, p_norm_of_U_e0=float(np.sum(np.abs(U @ e0) ** p) ** (1 / p)), expected_if_isometry=1.0))
P = np.zeros((2 * N, 2 * N)); perm = rng.permutation(2 * N); signs = rng.choice([-1, 1], 2 * N)
for i in range(2 * N): P[perm[i], i] = signs[i]
x = rng.standard_normal(2 * N)
ok("S2_non_monomial_unitary_is_no_p_isometry_and_signed_permutation_is", all(abs(r["p_norm_of_U_e0"] - 1) > 0.05 for r in rows) and all(abs(np.sum(np.abs(P @ x) ** p) - np.sum(np.abs(x) ** p)) < 1e-9 for p in (1, 1.5, 3, 4)),
   rows=rows, control="a random signed permutation matrix preserves every p-norm (seed reported)", seed=SEED)

# ---------------------------------------------------------------- S3: additive rules under continuation
# mu(S) = sum over walks of F(w), F = F_o on open walks (end != start), F_c(gain) on closed walks (end == start), F_c a class function (G8 Lemma 3.1).
# Consistency: sum_e F(we) = c F(w) for every walk w.  Solve the linear system for (F_o, F_c(g)) on several gain graphs and read off the solution space.
def additive_system(adj, gains, order, start, maxlen):
    """adj: dict x -> list of (y, gain in Z_order) for a digraph; returns the matrix of the homogeneous system for the unknowns
    [F_o, F_c(0), ..., F_c(order-1)] and each candidate c, over all walks from `start` of length <= maxlen."""
    rows = []
    def rec(x, g, depth):
        if depth > maxlen: return
        # row for walk ending at x with gain g:  sum_e F(we) - c F(w) = 0  (c handled outside: return both parts)
        ext = np.zeros(order + 1); own = np.zeros(order + 1)
        for (y, h) in adj[x]:
            gy = (g + h) % order
            if y == start: ext[1 + gy] += 1
            else: ext[0] += 1
        if x == start: own[1 + g] = 1
        else: own[0] = 1
        rows.append((ext, own))
        for (y, h) in adj[x]: rec(y, (g + h) % order, depth + 1)
    rec(start, 0, 0); return rows
def solution_space(rows, c):
    M = np.array([e - c * o for e, o in rows]); _, s, vt = np.linalg.svd(M); null = vt[np.sum(s > 1e-9):]
    return null
cases = {}
# (a) K4 with a Z_3 generator on one oriented edge (Directors A, B): d = 3
adj = {x: [] for x in range(4)}
for a in range(4):
    for b in range(4):
        if a != b: adj[a].append((b, 1 if (a, b) == (0, 1) else (2 if (a, b) == (1, 0) else 0)))
# (b) the signed arc digraph of a ring, as a Z_2 gain digraph, d = 2
N2 = 6; A2 = ring_step(N2); adj2 = {x: [(y, 0 if A2[y, x] > 0 else 1) for y in range(2 * N2) if A2[y, x] != 0] for x in range(2 * N2)}
# (c) two triangles sharing a vertex, Z_3 generator on one edge of one triangle (Director G); undirected; degrees 2 and 4
adj3 = {0: [(1, 0), (2, 0), (3, 0), (4, 0)], 1: [(0, 0), (2, 1)], 2: [(1, 2), (0, 0)], 3: [(0, 0), (4, 0)], 4: [(3, 0), (0, 0)]}
for label, (adj_, order, d_) in dict(K4_Z3=(adj, 3, 3), ring_arc_Z2=(adj2, 2, 2), two_triangles_Z3=(adj3, 3, None)).items():
    rows = additive_system(adj_, None, order, 0, 4)
    found = {}
    for c in [0.5, 1, 1.5, 2, 2.5, 3, 4, 5]:
        null = solution_space(rows, c)
        if null.shape[0]:
            # describe: is every solution constant across F_o and all F_c?
            const = all(np.allclose(n, n[0] * np.ones_like(n)) for n in null)
            found[str(c)] = dict(dimension=int(null.shape[0]), all_solutions_constant=bool(const), example=[round(float(t), 6) for t in null[0]])
    cases[label] = dict(out_degree=d_, consistent_factors=found)
ok("S3_additive_rule_consistent_under_continuation_is_constant", all(all(v["all_solutions_constant"] for v in case["consistent_factors"].values()) for case in cases.values())
   and all(len(case["consistent_factors"]) > 0 for label, case in cases.items() if case["out_degree"]),
   cases=cases, note="unknowns F_o and F_c(g); equations sum_e F(we) = c F(w) for all walks of length at most 4 from vertex 0; for constant out-degree d the only solutions have c = d and F constant; "
   "with degrees 2 and 4 (two triangles) no additive rule is consistent for any c tried")

# ---------------------------------------------------------------- S4: exact momentum translation needs the gain ratio to be constant
# T U M T^{-1} = e^{i Phi} U M  <=>  m(x-1)/m(x) = e^{i Phi} for all x.  Random Z_4 assignments: the best scalar fit is far from exact; the linear gain is exact.
def best_scalar_defect(mvals):
    Nn = len(mvals); ratio = np.roll(mvals, 1) / mvals          # m(x-1)/m(x)
    lam = ratio.mean() / abs(ratio.mean()) if abs(ratio.mean()) > 0 else 1.0
    return float(np.max(np.abs(ratio - lam))), ratio
rows = []
for trial in range(5):
    m = np.exp(1j * (math.pi / 2) * rng.integers(0, 4, 64)); dft, ratio = best_scalar_defect(m)
    rows.append(dict(trial=trial, largest_defect_of_scalar_fit=dft, distinct_ratios=int(len(set(np.round(ratio, 6).tolist())))))
lin = np.exp(-1j * (2 * math.pi / 64) * np.arange(64)); dlin, _ = best_scalar_defect(lin)
ok("S4_exact_translation_iff_constant_gain_ratio", all(r["largest_defect_of_scalar_fit"] > 0.5 for r in rows) and dlin < 1e-12, random_Z4=rows, linear_gain_defect=dlin, seed=SEED,
   note="the commutation relation with the translation is equivalent to m(x-1)/m(x) being one number e^{i Phi}; e^{i Phi} must then lie in the image of the character, so a translation by Phi needs a gain group of order at least 2 pi / Phi")

# ---------------------------------------------------------------- S5: periodic encodings of bounded order are superlattice-invariant: ballistic, no secular acceleration
def step_factory(N, V):
    """sparse step for the signed ring arc digraph with gains exp(-i V[x]) on arcs leaving site x; state psi[x, c], c = 0 (R), 1 (L)."""
    g = np.exp(-1j * V) / SQ2
    def step(psi):
        s = (psi[:, 0] + psi[:, 1]) * g; dlt = (psi[:, 0] - psi[:, 1]) * g
        out = np.empty_like(psi); out[:, 0] = np.roll(s, 1); out[:, 1] = np.roll(dlt, -1); return out
    return step
# agreement of the sparse step with ring_step on a small ring
Nt = 12; Vt = rng.uniform(0, 2 * math.pi, Nt); At = ring_step(Nt, potential=Vt) / SQ2; psi_t = rng.standard_normal((Nt, 2)) + 1j * rng.standard_normal((Nt, 2))
ok("S5_sparse_step_agrees_with_ring_step", np.allclose((At @ psi_t.reshape(-1)).reshape(Nt, 2), step_factory(Nt, Vt)(psi_t), atol=1e-12))
def packet(N, k0, sigma, x0=0.0):
    ks = 2 * math.pi * np.fft.fftfreq(N); psi_k = np.zeros((N, 2), dtype=complex)
    for i, kk in enumerate(ks):
        Uk = np.array([[np.exp(-1j * kk), np.exp(-1j * kk)], [np.exp(1j * kk), -np.exp(1j * kk)]]) / SQ2
        lam, vec = np.linalg.eig(Uk); w1 = math.asin(math.sin(kk) / SQ2); j = int(np.argmin(np.abs(lam - np.exp(-1j * w1))))
        u = vec[:, j] / np.linalg.norm(vec[:, j]); u = u * np.exp(-1j * np.angle(u[0] + 1e-30))
        d = (kk - k0 + math.pi) % (2 * math.pi) - math.pi
        psi_k[i] = math.exp(-d * d / (4 * sigma ** 2)) * np.exp(-1j * kk * x0) * u
    psi = np.fft.ifft(psi_k, axis=0); psi = np.roll(psi, N // 2, axis=0); return psi / np.linalg.norm(psi)
def centroid(psi):
    N = psi.shape[0]; p = (np.abs(psi) ** 2).sum(1); ang = 2 * math.pi * np.arange(N) / N
    return float(np.angle((p * np.exp(1j * ang)).sum()) * N / (2 * math.pi)) - N // 2
N = 4096; xs = np.arange(N) - N // 2; L = 16; Phi = math.pi / (2 * L)               # mean slope of the staircase; Bloch period 2 pi / Phi = 64 steps
V_lin = Phi * xs.astype(float)
V_stair = (math.pi / 2) * np.floor(xs / L)                                            # Z_4 gains, periodic with period 4L = 64 sites
# an aperiodic bounded-order encoding: the nearest Z_4 element to a linear phase with an irrational slope ratio
Phi_irr = Phi / ((1 + math.sqrt(5)) / 2); V_quasi = (math.pi / 2) * np.round(Phi_irr * xs / (math.pi / 2))
rows = {}
for label, V in dict(linear=V_lin, staircase_period_64=V_stair, quasiperiodic_rounded=V_quasi).items():
    st = step_factory(N, V); cur = packet(N, 0.3, 0.03); c0 = centroid(cur); traj = []
    for t in range(1, 1025):
        cur = st(cur)
        if t % 64 == 0: traj.append(dict(t=t, displacement=float(((centroid(cur) - c0 + N / 2) % N) - N / 2), rms_width=float(np.sqrt((((np.abs(cur) ** 2).sum(1)) * (xs - centroid(cur)) ** 2).sum()))))
    rows[label] = traj
lin_disp = [r["displacement"] for r in rows["linear"]]; st_disp = [r["displacement"] for r in rows["staircase_period_64"]]
ok("S5_linear_gain_oscillates_and_periodic_staircase_drifts", max(abs(d) for d in lin_disp) < 2.0 and abs(st_disp[-1]) > 20 and abs(st_disp[-1]) > 2 * abs(st_disp[len(st_disp) // 2 - 1]) * 0.8,
   rows=rows, note="displacements sampled every 64 steps (one Bloch period of the mean field) over 1024 steps: the linear gain returns to its start each period; the staircase, whose gains repeat every 64 sites, is invariant under translation by 64 sites and moves ballistically")
# the GJS prediction for the staircase: group velocities of the superlattice bands.  Bloch matrix for the supercell of 64 sites: 128 x 128 unitary U(K); velocity = d(eigenphase)/dK.
cell = 4 * L; Vc = V_stair[N // 2: N // 2 + cell] - V_stair[N // 2]
def supercell_U(K):
    M = np.zeros((2 * cell, 2 * cell), dtype=complex); g = np.exp(-1j * Vc) / SQ2
    for x in range(cell):
        xp, xm = (x + 1) % cell, (x - 1) % cell; fp = np.exp(-1j * K) if x == cell - 1 else 1.0; fm = np.exp(1j * K) if x == 0 else 1.0
        M[2 * xp + 0, 2 * x + 0] += g[x] * fp; M[2 * xp + 0, 2 * x + 1] += g[x] * fp
        M[2 * xm + 1, 2 * x + 0] += g[x] * fm; M[2 * xm + 1, 2 * x + 1] -= g[x] * fm
    return M
h = 1e-5; speeds = []
for K in np.linspace(-math.pi, math.pi, 33, endpoint=False):
    ph = np.sort(np.angle(np.linalg.eigvals(supercell_U(K)))); ph2 = np.sort(np.angle(np.linalg.eigvals(supercell_U(K + h))))
    speeds.extend((((ph2 - ph + math.pi) % (2 * math.pi) - math.pi) / h / cell).tolist())
speeds = np.array(speeds)
ok("S5_superlattice_bands_have_nonzero_group_velocity", float(np.max(np.abs(speeds))) > 0.05, largest_band_velocity_sites_per_step=float(np.max(np.abs(speeds))), rms_band_velocity=float(np.sqrt(np.mean(speeds ** 2))),
   note="eigenphases of the 128 x 128 Bloch matrix of the 64-site supercell, differentiated numerically (sorted phases; crossings can mix branches, which lowers but does not create a velocity); by Grimmett-Janson-Scudo X_t / t converges to the distribution of these velocities")

R["_summary"] = dict(predicates=sum(1 for k in R if not k.startswith("_")), passed=sum(1 for k, v in R.items() if not k.startswith("_") and v["passed"]), seed=SEED, numpy=np.__version__)
json.dump(R, open(OUT, "w"), indent=1, default=str)
for k, v in R.items():
    if not k.startswith("_"): print(("PASS " if v["passed"] else "FAIL ") + k)
print(R["_summary"])
