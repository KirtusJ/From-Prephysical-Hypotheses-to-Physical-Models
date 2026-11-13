#!/usr/bin/env python3
"""Canonical holonomy of transition-probability geometry as a number-field discriminator.

Checks (all numerical, double precision, fixed seed; tolerances in the code):
 A  Schild's ladder (exp/log maps of the Fubini-Study metric only) on CP^n, n=1,2,3:
    holonomy T of a geodesic triangle is complex-linear and unitary on the horizontal
    space, and det_C T = exp(+i (n+1) beta), beta = arg <a0|a1><a1|a2><a2|a0> (the closing horizontal lift has phase -beta).
    Control: closed-form transport along the same polygon.  For n = 3 the triangle does not span
    C^4 and T has the eigenvalue exp(i beta).
 B  Dimension of the commutant of holonomy matrices in M_m(R):
    CP^2 -> 2, S^2 -> 2, S^3 -> 1, S^4 (= HP^1) -> 1, RP^2 with a non-contractible loop -> 1.
 C  RP^2: Schild's ladder round the non-contractible closed geodesic gives det = -1;
    the sign bundle S^2 -> RP^2 has holonomy -1 on that loop and +1 on a contractible one.
 D  Hamiltonian form of the Schroedinger flow on CP^n: omega(X_H, w) = d<H>(w), omega = 2 Im<.,.>.
 E  Spin-j coherent-state transition probability cos^{4j}(theta/2): half-width against j.
 F  Covering radius of orbits of finite subgroups of O(3) on the unit sphere
    (finite homogeneous subsets of the Bloch sphere), with the area lower bound arccos(1 - 1/60).
 G  Constructed trial with stipulated generators: orbit of words in two rotations (Hadamard, pi/8)
    of bounded length; covering radius against word length.
Writes Holonomy_Field_Discriminator_Results.json next to this file; refuses to overwrite.
"""
import json, os, sys, itertools
import numpy as np
from scipy.optimize import minimize
from scipy.linalg import null_space

rng = np.random.default_rng(20261112)
STEPS, EPS = 600, 2e-3
R = {}
ok = {}

# ---------- projective geometry over R or C (unit representatives) ----------
def align(a, x):
    ip = np.vdot(a, x)
    if abs(ip) < 1e-15: raise ValueError("orthogonal")
    return x * (np.conj(ip) / abs(ip))
def plog(a, x):
    xa = align(a, x); c = np.vdot(a, xa).real
    u = xa - c * a; nu = np.linalg.norm(u)
    if nu < 1e-300: return np.zeros_like(a)
    return np.arctan2(nu, c) * u / nu
def pexp(a, v):
    t = np.linalg.norm(v)
    if t < 1e-300: return a.copy()
    return np.cos(t) * a + np.sin(t) * v / t
def pmid(x, y): return pexp(x, 0.5 * plog(x, y))
def schild_step(A, B, X):
    """One rung: A -> B, X near A represents a vector at A; returns X' near B."""
    M = pmid(X, B)
    return pexp(A, 2.0 * plog(A, M))
def _schild_one(verts, v, steps, eps):
    A = verts[0].copy(); X = pexp(A, eps * v)
    k = len(verts)
    for i in range(k):
        Q = verts[(i + 1) % k]
        for s in range(steps):
            B = pexp(A, plog(A, Q) / (steps - s))   # next point on the geodesic A -> Q
            X = schild_step(A, B, X)
            A = B
    a0 = verts[0]
    ph = np.vdot(a0, A); ph = ph / abs(ph)           # A represents verts[0] up to a phase or sign
    return plog(A * np.conj(ph), X * np.conj(ph)) / eps, ph
def schild_transport_proj(verts, v, steps, eps):
    """Schild's ladder round the geodesic polygon, using only exp, log and midpoints of the metric.
    The ladder is run for +v and -v and the results are differenced, which removes the error of
    first order in the rung length eps."""
    wp, ph = _schild_one(verts, v, steps, eps)
    wm, _ = _schild_one(verts, -v, steps, eps)
    return 0.5 * (wp - wm), ph

def exact_transport_proj(verts, v):
    """Closed-form Levi-Civita transport round the geodesic polygon in CP^n / RP^n."""
    a = verts[0].copy(); w = v.copy(); k = len(verts)
    for i in range(k):
        q = align(a, verts[(i + 1) % k])
        c = np.vdot(a, q).real
        u = (q - c * a); nu = np.linalg.norm(u); T = np.arctan2(nu, c); u = u / nu
        # ambient rotation in span(a,u): a -> cos a + sin u, u -> -sin a + cos u (complex-linear)
        ca = np.vdot(a, w); cu = np.vdot(u, w)
        w = w - ca * a - cu * u + ca * (np.cos(T) * a + np.sin(T) * u) + cu * (-np.sin(T) * a + np.cos(T) * u)
        a = np.cos(T) * a + np.sin(T) * u
    ph = np.vdot(verts[0], a); ph = ph / abs(ph)
    return w * np.conj(ph), ph

def rand_state(n, cplx=True):
    x = rng.normal(size=n) + (1j * rng.normal(size=n) if cplx else 0)
    return x / np.linalg.norm(x)
def horizontal_basis(a, cplx=True):
    n = len(a)
    Q = null_space(a.conj().reshape(1, n))          # columns orthonormal, orthogonal to a
    return Q
def nearby_triangle(n, cplx, size):
    a = rand_state(n, cplx); Q = horizontal_basis(a, cplx)
    vs = [a]
    for _ in range(2):
        c = rng.normal(size=Q.shape[1]) + (1j * rng.normal(size=Q.shape[1]) if cplx else 0)
        v = Q @ c; v = size * v / np.linalg.norm(v)
        vs.append(pexp(a, v))
    return vs

# ---------- A: CP^n ----------
A_out = []
for n in (1, 2, 3):
    verts = nearby_triangle(n + 1, True, 0.6)
    a = verts[0]; Q = horizontal_basis(a)
    barg = np.vdot(verts[0], verts[1]) * np.vdot(verts[1], verts[2]) * np.vdot(verts[2], verts[0])
    phi = np.angle(barg)
    Ts = np.zeros((n, n), complex); Te = np.zeros((n, n), complex)
    lin_res = 0.0
    for j in range(n):
        v = Q[:, j]
        ws, ph_s = schild_transport_proj(verts, v, steps=STEPS, eps=EPS)
        we, ph_e = exact_transport_proj(verts, v)
        Ts[:, j] = Q.conj().T @ ws; Te[:, j] = Q.conj().T @ we
        wi, _ = schild_transport_proj(verts, 1j * v, steps=STEPS, eps=EPS)   # J-linearity test
        lin_res = max(lin_res, np.linalg.norm(wi - 1j * ws))
    rec = dict(n=n, bargmann_phase=phi,
               closing_lift_phase_exact=float(np.angle(ph_e)),
               schild_vs_closed_form=float(np.linalg.norm(Ts - Te)),
               schild_unitarity_residual=float(np.linalg.norm(Ts.conj().T @ Ts - np.eye(n))),
               schild_J_linearity_residual=float(lin_res),
               arg_det_schild=float(np.angle(np.linalg.det(Ts))),
               arg_det_closed_form=float(np.angle(np.linalg.det(Te))),
               predicted_n_plus_1_times_bargmann_phase=float(np.angle(np.exp(1j * (n + 1) * phi))))
    if n + 1 > 3:   # the three vertices do not span C^{n+1}: T has the eigenvalue B/|B| on their orthogonal complement
        rec["min_distance_eigenvalue_schild_to_bargmann_phase"] = float(np.min(np.abs(np.linalg.eigvals(Ts) - np.exp(1j * phi))))
        rec["min_distance_eigenvalue_closed_form_to_bargmann_phase"] = float(np.min(np.abs(np.linalg.eigvals(Te) - np.exp(1j * phi))))
    rec["det_law_residual_schild"] = float(abs(np.exp(1j * rec["arg_det_schild"]) - np.exp(1j * (n + 1) * phi)))
    rec["det_law_residual_closed_form"] = float(abs(np.linalg.det(Te) - np.exp(1j * (n + 1) * phi)))
    A_out.append(rec)
R["A_CPn_schild_holonomy"] = A_out
ok["A_closed_form_det_law"] = all(r["det_law_residual_closed_form"] < 1e-12 for r in A_out)
ok["A_schild_det_law"] = all(r["det_law_residual_schild"] < 1e-5 for r in A_out)
ok["A_schild_matches_closed_form"] = all(r["schild_vs_closed_form"] < 1e-5 for r in A_out)
ok["A_eigenvalue_law_nonspanning"] = all(r.get("min_distance_eigenvalue_closed_form_to_bargmann_phase", 0) < 1e-12 and r.get("min_distance_eigenvalue_schild_to_bargmann_phase", 0) < 1e-5 for r in A_out)
ok["A_schild_J_linear"] = all(r["schild_J_linearity_residual"] < 1e-5 for r in A_out)

# ---------- B: commutant dimensions ----------
def commutant_dim(mats, tol=1e-8):
    m = mats[0].shape[0]; I = np.eye(m)
    rows = [np.kron(I, T) - np.kron(T.T, I) for T in mats]   # vec(TX - XT)
    s = np.linalg.svd(np.vstack(rows), compute_uv=False)
    return int(np.sum(s < tol * s[0])) + (m * m - len(s))
def realify(Tc):
    n = Tc.shape[0]; M = np.zeros((2 * n, 2 * n))
    M[:n, :n] = Tc.real; M[:n, n:] = -Tc.imag; M[n:, :n] = Tc.imag; M[n:, n:] = Tc.real
    return M
def cp_holonomies(n, count):
    a = rand_state(n + 1); Q = horizontal_basis(a); out = []
    for _ in range(count):
        vs = [a]
        for _ in range(2):
            c = rng.normal(size=n) + 1j * rng.normal(size=n); v = Q @ c; v = 0.7 * v / np.linalg.norm(v)
            vs.append(pexp(a, v))
        # real-linear holonomy on the real 2n-dimensional horizontal space, no complex structure assumed
        basis = [Q[:, j] for j in range(n)] + [1j * Q[:, j] for j in range(n)]
        M = np.zeros((2 * n, 2 * n))
        for j, v in enumerate(basis):
            w, _ = exact_transport_proj(vs, v); cw = Q.conj().T @ w
            M[:, j] = np.concatenate([cw.real, cw.imag])
        out.append(M)
    return out
# spheres S^k in R^{k+1}
def sexp(a, v):
    t = np.linalg.norm(v); return a.copy() if t < 1e-300 else np.cos(t) * a + np.sin(t) * v / t
def slog(a, x):
    c = np.clip(a @ x, -1, 1); d = np.arccos(c); u = x - c * a; nu = np.linalg.norm(u)
    return np.zeros_like(a) if nu < 1e-300 else d * u / nu
def sphere_transport(verts, v):
    a = verts[0].copy(); w = v.copy(); k = len(verts)
    for i in range(k):
        q = verts[(i + 1) % k]; L = slog(a, q); T = np.linalg.norm(L); u = L / T
        ca, cu = a @ w, u @ w
        w = w - ca * a - cu * u + ca * (np.cos(T) * a + np.sin(T) * u) + cu * (-np.sin(T) * a + np.cos(T) * u)
        a = np.cos(T) * a + np.sin(T) * u
    return w
def sphere_holonomies(k, count):
    a = rng.normal(size=k + 1); a /= np.linalg.norm(a); Q = null_space(a.reshape(1, -1)); out = []
    for _ in range(count):
        vs = [a]
        for _ in range(2):
            v = Q @ rng.normal(size=k); v = 0.9 * v / np.linalg.norm(v); vs.append(sexp(a, v))
        M = np.column_stack([Q.T @ sphere_transport(vs, Q[:, j]) for j in range(k)]); out.append(M)
    return out, a, Q
B = {}
B["CP2"] = commutant_dim(cp_holonomies(2, 6))
B["CP3"] = commutant_dim(cp_holonomies(3, 8))
hs2, a2, Q2 = sphere_holonomies(2, 4); B["S2_equals_CP1"] = commutant_dim(hs2)
B["S3"] = commutant_dim(sphere_holonomies(3, 6)[0])
B["S4_equals_HP1"] = commutant_dim(sphere_holonomies(4, 8)[0])
B["S8_equals_OP1"] = commutant_dim(sphere_holonomies(8, 14)[0])
R["B_commutant_dimension"] = B

# ---------- C: RP^2 monodromy ----------
a = np.array([0.0, 0.0, 1.0]); b = np.array([np.sin(1.0), 0, np.cos(1.0)]); c = np.array([np.sin(2.0), 0, np.cos(2.0)])
loop_nc = [a, b, c]                       # a -> b -> c -> a(-a): the projective line, non-contractible
Qr = horizontal_basis(a, cplx=False)
Mnc_s = np.column_stack([Qr.T @ schild_transport_proj(loop_nc, Qr[:, j], steps=STEPS, eps=EPS)[0] for j in range(2)])
Mnc_e = np.column_stack([Qr.T @ exact_transport_proj(loop_nc, Qr[:, j])[0] for j in range(2)])
sign_nc = exact_transport_proj(loop_nc, Qr[:, 0])[1]
tri = nearby_triangle(3, False, 0.5)
Qt = horizontal_basis(tri[0], cplx=False)
Mc = np.column_stack([Qt.T @ exact_transport_proj(tri, Qt[:, j])[0] for j in range(2)])
sign_c = exact_transport_proj(tri, Qt[:, 0])[1]
R["C_RP2"] = dict(det_noncontractible_schild=float(np.linalg.det(Mnc_s)), det_noncontractible_closed_form=float(np.linalg.det(Mnc_e)),
                  schild_vs_closed_form=float(np.linalg.norm(Mnc_s - Mnc_e)),
                  det_contractible=float(np.linalg.det(Mc)),
                  sign_bundle_holonomy_noncontractible=float(np.real(sign_nc)), sign_bundle_holonomy_contractible=float(np.real(sign_c)))
# full holonomy group of RP^2 at a: contractible rotations plus the reflection -> commutant
tri_a = [a, pexp(a, 0.8 * Qr[:, 0]), pexp(a, 0.8 * Qr[:, 1])]
Mrot = np.column_stack([Qr.T @ exact_transport_proj(tri_a, Qr[:, j])[0] for j in range(2)])
B["RP2_restricted_only"] = commutant_dim([Mrot]); B["RP2_with_monodromy"] = commutant_dim([Mrot, Mnc_e])
ok["B_commutants"] = (B["CP2"] == 2 and B["CP3"] == 2 and B["S2_equals_CP1"] == 2 and B["S3"] == 1 and B["S4_equals_HP1"] == 1
                      and B["S8_equals_OP1"] == 1 and B["RP2_restricted_only"] == 2 and B["RP2_with_monodromy"] == 1)
ok["C_monodromy_reflection"] = abs(R["C_RP2"]["det_noncontractible_schild"] + 1) < 1e-4 and R["C_RP2"]["schild_vs_closed_form"] < 1e-5 and abs(R["C_RP2"]["det_contractible"] - 1) < 1e-12 \
    and R["C_RP2"]["sign_bundle_holonomy_noncontractible"] == -1.0 and R["C_RP2"]["sign_bundle_holonomy_contractible"] == 1.0

# ---------- D: Hamiltonian form ----------
res = 0.0
for _ in range(50):
    n = 4; psi = rand_state(n); H = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n)); H = (H + H.conj().T) / 2
    E = np.vdot(psi, H @ psi).real; XH = -1j * (H @ psi - E * psi)
    Q = horizontal_basis(psi); w = Q @ (rng.normal(size=n - 1) + 1j * rng.normal(size=n - 1))
    h = 1e-6; p1 = psi + h * w; p1 /= np.linalg.norm(p1); m1 = psi - h * w; m1 /= np.linalg.norm(m1)
    dE = (np.vdot(p1, H @ p1).real - np.vdot(m1, H @ m1).real) / (2 * h)
    res = max(res, abs(2 * np.vdot(XH, w).imag - dE))
R["D_hamiltonian_form_max_residual"] = res; ok["D_hamiltonian_form"] = res < 1e-7

# ---------- E: coherent-state concentration ----------
E_out = {}
for j in (0.5, 2, 8, 32, 128, 512):
    th = 2 * np.arccos(0.5 ** (1 / (4 * j)))      # p = cos^{4j}(theta/2) = 1/2
    E_out[str(j)] = dict(half_probability_angle=float(th), times_sqrt_j=float(th * np.sqrt(j)))
R["E_spin_coherent_half_width"] = E_out
vals = [v["times_sqrt_j"] for v in E_out.values()]
ok["E_width_scales_as_inverse_sqrt_j"] = abs(vals[-1] - vals[-2]) < 1e-3 and abs(vals[-1] - np.sqrt(2 * np.log(2))) < 1e-3

# ---------- F: finite homogeneous subsets of S^2 ----------
def rot(axis, ang):
    axis = np.asarray(axis, float); axis /= np.linalg.norm(axis); K = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    return np.eye(3) + np.sin(ang) * K + (1 - np.cos(ang)) * K @ K
def close_group(gens):
    G = [np.eye(3)]; frontier = [np.eye(3)]
    while frontier:
        new = []
        for g in frontier:
            for h in gens:
                x = h @ g
                if not any(np.allclose(x, y, atol=1e-9) for y in G): G.append(x); new.append(x)
        frontier = new
        if len(G) > 500: raise RuntimeError("group too large")
    return G
gphi = (1 + 5 ** 0.5) / 2
groups = {
    "T (12)": close_group([rot([1, 1, 1], 2 * np.pi / 3), rot([0, 0, 1], np.pi)]),
    "O (24)": close_group([rot([1, 1, 1], 2 * np.pi / 3), rot([0, 0, 1], np.pi / 2)]),
    "I (60)": close_group([rot([0, 1, gphi], 2 * np.pi / 5), rot([1, 1, 1], 2 * np.pi / 3)]),
}
for k in list(groups):
    G = groups[k]; groups[k.split()[0] + "h/x-1 (%d)" % (2 * len(G))] = G + [-g for g in G]
# test directions: Fibonacci grid
Ng = 4000; ii = np.arange(Ng) + 0.5; zz = 1 - 2 * ii / Ng; pp = np.pi * (1 + 5 ** 0.5) * ii
grid = np.column_stack([np.sqrt(1 - zz ** 2) * np.cos(pp), np.sqrt(1 - zz ** 2) * np.sin(pp), zz])
from scipy.spatial import ConvexHull
def orbit(G, seed):
    P = []
    for g in G:
        x = g @ seed
        if not any(np.linalg.norm(x - y) < 1e-7 for y in P): P.append(x)
    return np.array(P)
def cov_radius_exact(P):
    hull = ConvexHull(P); r = 0.0
    for eq in hull.equations:
        nrm = eq[:3] / np.linalg.norm(eq[:3]); r = max(r, np.arccos(np.clip(-eq[3] / np.linalg.norm(eq[:3]), -1, 1)))
    return float(r)
def cov_radius(G, seed):
    P = np.array([g @ seed for g in G]); return float(np.max(np.arccos(np.clip(np.max(grid @ P.T, axis=1), -1, 1))))
F = {}
for name, G in groups.items():
    assert len(G) in (12, 24, 60, 120, 48), (name, len(G))
    best = (9, None)
    for trial in range(40):
        s0 = rng.normal(size=3); s0 /= np.linalg.norm(s0)
        f = lambda x: cov_radius(G, np.array([np.sin(x[0]) * np.cos(x[1]), np.sin(x[0]) * np.sin(x[1]), np.cos(x[0])]))
        x0 = [np.arccos(s0[2]), np.arctan2(s0[1], s0[0])]
        r = minimize(f, x0, method="Nelder-Mead", options=dict(xatol=1e-4, fatol=1e-5, maxiter=200))
        if r.fun < best[0]: best = (r.fun, r.x)
    x = best[1]; seed = np.array([np.sin(x[0]) * np.cos(x[1]), np.sin(x[0]) * np.sin(x[1]), np.cos(x[0])])
    fe = lambda y: cov_radius_exact(orbit(G, np.array([np.sin(y[0]) * np.cos(y[1]), np.sin(y[0]) * np.sin(y[1]), np.cos(y[0])])))
    r2 = minimize(fe, x, method="Nelder-Mead", options=dict(xatol=1e-7, fatol=1e-9, maxiter=400))
    F[name] = dict(order=len(G), orbit_size_at_optimum=int(len(orbit(G, np.array([np.sin(r2.x[0]) * np.cos(r2.x[1]), np.sin(r2.x[0]) * np.sin(r2.x[1]), np.cos(r2.x[0])])))),
                   best_covering_radius_deg=float(np.degrees(r2.fun)), grid_stage_deg=float(np.degrees(best[0])))
# axial families: any orbit lies on at most two parallels at colatitudes t and pi - t
F["axial families (C_n, C_nv, C_nh, S_2n, D_n, D_nd, D_nh), n -> infinity"] = dict(order="unbounded", infimum_covering_radius_deg=45.0,
    reason="orbit contained in two parallels at colatitude t and pi-t; covering radius >= max(t, pi/2 - t) >= pi/4")
R["F_finite_homogeneous_subsets_of_S2"] = F
polyh = [v["best_covering_radius_deg"] for k, v in F.items() if "best_covering_radius_deg" in v]
R["F_smallest_covering_radius_found_deg"] = min(polyh)
R["F_rigorous_area_lower_bound_deg_for_order_at_most_120"] = float(np.degrees(np.arccos(1 - 1 / 60)))
ok["F_bounded_below"] = min(polyh) > 5.0

# ---------- G: constructed trial, finitely generated dense subgroup (generators STIPULATED) ----------
# Rotations of the Bloch sphere induced by the Hadamard and pi/8 gates: H = half-turn about (x+z)/sqrt2, T = turn by pi/4 about z.
gH = rot([1, 0, 1], np.pi); gT = rot([0, 0, 1], np.pi / 4)
seedG = np.array([0.0, 0.0, 1.0])
elems = {tuple(np.round(np.eye(3).ravel(), 9)): np.eye(3)}; frontier = [np.eye(3)]; G_out = []
for L in range(1, 41):
    new = []
    for g in frontier:
        for h in (gH, gT):
            x = h @ g; key = tuple(np.round(x.ravel(), 9))
            if key not in elems: elems[key] = x; new.append(x)
    frontier = new
    if L % 4 == 0 or not new:
        P = orbit_fast = np.unique(np.round(np.array([g @ seedG for g in elems.values()]), 9), axis=0)
        rec = dict(word_length_at_most=L, group_elements=len(elems), orbit_points=int(len(P)))
        if len(P) >= 4 and np.linalg.matrix_rank(P - P[0]) == 3: rec["covering_radius_deg"] = float(np.degrees(cov_radius_exact(P)))
        G_out.append(rec)
    if len(elems) > 60000 or not new: break
R["G_words_in_two_stipulated_generators"] = G_out
cr = [r["covering_radius_deg"] for r in G_out if "covering_radius_deg" in r]
ok["G_covering_radius_falls_below_homogeneous_bound"] = cr[-1] < R["F_rigorous_area_lower_bound_deg_for_order_at_most_120"] and all(cr[i + 1] <= cr[i] + 1e-9 for i in range(len(cr) - 1))

R["predicates"] = {k: bool(v) for k, v in ok.items()}
R["all_predicates_true"] = bool(all(ok.values()))
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Holonomy_Field_Discriminator_Results.json")
if "--stdout" in sys.argv:
    print(json.dumps(R, indent=1))
else:
    if os.path.exists(out): sys.exit("refusing to overwrite " + out)
    json.dump(R, open(out, "w"), indent=1); print("written", out, "all_predicates_true =", R["all_predicates_true"])
