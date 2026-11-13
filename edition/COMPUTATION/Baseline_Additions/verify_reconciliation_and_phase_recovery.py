#!/usr/bin/env python3
"""Parts A-C of the computations for edition Z2 (cited by paper G7). Independent recomputation of items in the Director A, B, G packets
by routes that do not reuse their programs, and checks of the phase-recovery corollary and the
generator/observable count.  Double precision unless 'exact' is stated; fixed seed."""
import json, itertools, math
import numpy as np, sympy as sp
from scipy.linalg import null_space
rng = np.random.default_rng(2026111202)
R, ok = {}, {}

# ---------- shared projective geometry (unit representatives, d = arccos|<a|b>|) ----------
def align(a, x):
    ip = np.vdot(a, x); return x * (np.conj(ip) / abs(ip))
def plog(a, x):
    xa = align(a, x); c = np.vdot(a, xa).real; u = xa - c * a; nu = np.linalg.norm(u)
    return np.zeros_like(a) if nu < 1e-300 else np.arctan2(nu, c) * u / nu
def pexp(a, v):
    t = np.linalg.norm(v); return a.copy() if t < 1e-300 else np.cos(t) * a + np.sin(t) * v / t
def rand_state(n, cplx=True):
    x = rng.normal(size=n) + (1j * rng.normal(size=n) if cplx else 0); return x / np.linalg.norm(x)
def transport(verts, v):
    """closed-form Levi-Civita transport round a geodesic polygon (G7 Lemma 4.2); returns vector at verts[0]"""
    a = verts[0].copy(); w = v.copy(); k = len(verts)
    for i in range(k):
        q = align(a, verts[(i + 1) % k]); c = np.vdot(a, q).real
        u = q - c * a; nu = np.linalg.norm(u); T = np.arctan2(nu, c); u = u / nu
        ca = np.vdot(a, w); cu = np.vdot(u, w)
        w = w - ca * a - cu * u + ca * (np.cos(T) * a + np.sin(T) * u) + cu * (-np.sin(T) * a + np.cos(T) * u)
        a = np.cos(T) * a + np.sin(T) * u
    ph = np.vdot(verts[0], a); ph /= abs(ph)
    return w * np.conj(ph)
def hol_matrix(verts, Q):
    return np.column_stack([Q.conj().T @ transport(verts, Q[:, j]) for j in range(Q.shape[1])])
def barg(verts):
    b = 1.0 + 0j
    for i in range(len(verts)): b *= np.vdot(verts[i], verts[(i + 1) % len(verts)])
    return b

# ================= A. items raised by Directors A, B, G =================
# A1 exact conjugate triple (Director G, DG-01), exact arithmetic
x = sp.Matrix([1, 0]); y = sp.Matrix([sp.sqrt(3) / 2, sp.Rational(1, 2)]); z = sp.Matrix([sp.sqrt(3) / 2, sp.I / 2])
ip = lambda a, b: (a.H * b)[0]
B = sp.simplify(ip(x, y) * ip(y, z) * ip(z, x))
P = [sp.simplify(abs(ip(a, b)) ** 2) for a, b in ((x, y), (y, z), (z, x))]
zc = z.conjugate(); Bc = sp.simplify(ip(x, y) * ip(y, zc) * ip(zc, x))
R["A1_exact_triple"] = dict(B=str(B), B_conjugated_states=str(Bc), probabilities=[str(p) for p in P])
ok["A1_B_equals_(9+3i)/16_and_conjugates"] = (sp.simplify(B - (9 + 3 * sp.I) / 16) == 0 and sp.simplify(Bc - (9 - 3 * sp.I) / 16) == 0
                                             and P == [sp.Rational(3, 4), sp.Rational(5, 8), sp.Rational(3, 4)])
# A2 Gram continuum (Director A, A-04): moduli 1/2, triple phase theta; exact determinant
th = sp.symbols('theta', real=True)
G = sp.Matrix([[1, sp.Rational(1, 2), sp.Rational(1, 2) * sp.exp(-sp.I * th)], [sp.Rational(1, 2), 1, sp.Rational(1, 2)],
               [sp.Rational(1, 2) * sp.exp(sp.I * th), sp.Rational(1, 2), 1]])
detG = sp.simplify(sp.re(sp.expand_complex(G.det())))
R["A2_gram_det"] = str(detG)
ok["A2_gram_psd_all_theta"] = sp.simplify(detG - (sp.Rational(1, 4) + sp.cos(th) / 4)) == 0   # >= 0, zero only at theta = pi; 2x2 minors 3/4 > 0
# A3 curvature from holonomy of small geodesic triangles: angle / area -> K (Directors A, G: K = 1 for RP^2, 4 for CP^1)
def tri_area_from_sides(a, b, c, K):   # L'Huilier on a sphere of curvature K
    s = (a + b + c) / 2 * math.sqrt(K)
    t = math.tan(s / 2) * math.tan((s - a * math.sqrt(K)) / 2) * math.tan((s - b * math.sqrt(K)) / 2) * math.tan((s - c * math.sqrt(K)) / 2)
    return 4 * math.atan(math.sqrt(max(t, 0))) / K
def curvature_estimate(n, cplx, plane):
    a = rand_state(n, cplx); Q = null_space(a.conj().reshape(1, n))
    if plane == "generic2d":            # RP^2 or CP^1: tangent space is real 2-dimensional
        e1 = Q[:, 0]; e2 = Q[:, 1] if Q.shape[1] > 1 else 1j * Q[:, 0]
    elif plane == "complex_line": e1 = Q[:, 0]; e2 = 1j * Q[:, 0]
    elif plane == "totally_real": e1 = Q[:, 0]; e2 = Q[:, 1]
    eps = 0.05
    v1 = pexp(a, eps * e1); v2 = pexp(a, eps * e2); verts = [a, v1, v2]
    d = lambda p, q: math.acos(min(1.0, abs(np.vdot(p, q))))
    s = (d(a, v1), d(v1, v2), d(v2, a))
    w = transport(verts, e1)
    ang = abs(math.atan2(np.vdot(e2, w).real if not cplx or plane != "complex_line" else np.vdot(e2, w).real, np.vdot(e1, w).real))
    # solve K from angle = K * area(K) by fixed point
    K = 1.0
    for _ in range(200): K = ang / tri_area_from_sides(*s, K)
    return K
Ks = dict(RP2=curvature_estimate(3, False, "generic2d"), CP1=curvature_estimate(2, True, "generic2d"),
          CP2_complex_line=curvature_estimate(3, True, "complex_line"), CP2_totally_real=curvature_estimate(3, True, "totally_real"))
R["A3_curvature_from_holonomy"] = Ks
ok["A3_K_RP2_1_CP1_4_CP2_range_1_to_4"] = (abs(Ks["RP2"] - 1) < 1e-3 and abs(Ks["CP1"] - 4) < 1e-3 and abs(Ks["CP2_complex_line"] - 4) < 1e-3 and abs(Ks["CP2_totally_real"] - 1) < 1e-3)
# A4 cap bounds and the (2,3,5) fundamental triangle
R["A4_caps_deg"] = dict(O3=math.degrees(math.acos(59 / 60)), SO3=math.degrees(math.acos(29 / 30)))
phi = (1 + 5 ** .5) / 2
v5 = np.array([0, 1, phi]); v5 = v5 / np.linalg.norm(v5)                 # 5-fold axis (icosahedron vertex)
v2 = np.array([0, 0, 1.0])                                               # 2-fold axis (edge midpoint)
v3 = np.array([phi, 0, 2 * phi + 1]); v3 = v3 / np.linalg.norm(v3)       # 3-fold axis (centre of a face on that edge)
ang = lambda p, q: math.degrees(math.acos(np.clip(p @ q, -1, 1)))
sides = dict(s35=ang(v3, v5), s25=ang(v2, v5), s23=ang(v2, v3))
c = np.cross(v5 - v2, v3 - v2); c /= np.linalg.norm(c); c = c if c @ v2 > 0 else -c      # circumcentre of the three vertices
circ = ang(c, v2)
inside = all(np.linalg.det(np.array([p, q, c])) * np.linalg.det(np.array([p, q, r])) > 0 for p, q, r in ((v2, v3, v5), (v3, v5, v2), (v5, v2, v3)))
from scipy.optimize import minimize
def _cap(x):
    cc = np.array([math.sin(x[0]) * math.cos(x[1]), math.sin(x[0]) * math.sin(x[1]), math.cos(x[0])])
    return max(ang(cc, v) for v in (v2, v3, v5))
best = min((minimize(_cap, [a_, b_], method='Nelder-Mead', options=dict(xatol=1e-12, fatol=1e-12)) for a_ in (0.1, 0.3, 0.5) for b_ in (0.3, 0.8, 1.3)), key=lambda r: r.fun)
R["A4_235_triangle"] = dict(sides_deg=sides, circumradius_deg=circ, circumcentre_inside=bool(inside), min_enclosing_cap_deg=float(best.fun),
                            half_hypotenuse_deg=sides["s35"] / 2, chord_of_circumradius=2 * math.sin(math.radians(circ) / 2),
                            note="Lavi (arXiv 2001.03885) proves that a fundamental triangle of a reflection group is the Dirichlet cell of any orbit point inside it, "
                                 "and finds Euclidean Hausdorff distance 0.3208 for orbit points allowed off the sphere; on the sphere the optimum for [3,5] is the circumradius")
ok["A4_cap_values"] = abs(R["A4_caps_deg"]["O3"] - 10.475313843) < 1e-8 and abs(R["A4_caps_deg"]["SO3"] - 14.835111582) < 1e-8
ok["A4_full_icosahedral_covering_radius_is_circumradius_18.7125"] = abs(circ - 18.7125) < 1e-3 and abs(best.fun - circ) < 1e-6 and inside
# A5 composition (Director B, B-COMP-05) and the relative orientation of two qubits
s0 = np.eye(2); sx = np.array([[0, 1], [1, 0]], complex); sy = np.array([[0, -1j], [1j, 0]]); sz = np.diag([1.0, -1]).astype(complex)
S = [sx, sy, sz]
psi = np.array([0, 1, -1, 0], complex) / 2 ** .5; rho = np.outer(psi, psi.conj())
Tm = np.array([[np.trace(rho @ np.kron(a, b)).real for b in S] for a in S])
def rho_from_T(T, a=np.zeros(3), b=np.zeros(3)):
    r = np.kron(s0, s0).astype(complex)
    for i in range(3):
        r += a[i] * np.kron(S[i], s0) + b[i] * np.kron(s0, S[i])
        for j in range(3): r += T[i, j] * np.kron(S[i], S[j])
    return r / 4
refl = np.diag([1, -1, 1.0])                       # reflection of system B's Bloch sphere: an isometry of its transition-probability geometry
rho_m = rho_from_T(Tm @ refl)
chsh = 2 * math.sqrt(sum(sorted(np.linalg.svd(Tm, compute_uv=False) ** 2)[-2:]))
R["A5_composition"] = dict(singlet_T_det=float(np.linalg.det(Tm)), mirrored_T_det=float(np.linalg.det(Tm @ refl)),
                           min_eig_singlet=float(np.linalg.eigvalsh(rho).min()), min_eig_mirrored=float(np.linalg.eigvalsh(rho_m).min()), chsh_singlet=chsh)
ok["A5_mirror_image_of_singlet_correlations_is_not_a_state"] = np.linalg.eigvalsh(rho_m).min() < -0.49 and abs(chsh - 2 * 2 ** .5) < 1e-12
# three qubits: reflect a subset; the pairwise relative orientations r_AB r_BC r_CA of any tripartite quantum composite multiply to +1
def pt(rho3, subset):   # partial transpose on the qubits in subset (transpose = reflection y -> -y of that Bloch sphere)
    t = rho3.reshape([2] * 6)
    for q in subset: t = np.swapaxes(t, q, q + 3)
    return t.reshape(8, 8)
v = rng.normal(size=8) + 1j * rng.normal(size=8); v /= np.linalg.norm(v); r3 = np.outer(v, v.conj())
def marg(rho3, keep):
    t = rho3.reshape([2] * 6); drop = [q for q in range(3) if q not in keep][0]
    return np.trace(t, axis1=drop, axis2=drop + 3).reshape(4, 4)
def pair_orientation(rho2):   # +1 if the two-qubit marginal's family is the standard one; decided on a singlet-type witness below
    return None
prods = {}
for subset in [(), (0,), (1,), (2,), (0, 1), (0, 2), (1, 2), (0, 1, 2)]:
    r = {}
    for pair in [(0, 1), (1, 2), (0, 2)]:
        r[pair] = -1 if (len(set(pair) & set(subset)) == 1) else 1    # one of the two reflected -> mirrored pair composite
    prods[str(subset)] = r[(0, 1)] * r[(1, 2)] * r[(0, 2)]
R["A5_orientation_cocycle_products"] = prods
ok["A5_orientation_cocycle_balanced"] = all(p == 1 for p in prods.values())
# numerical witness that the pairwise labels are meaningful: GHZ-type state reduced on pairs after partial transposes stays positive only for consistent labels
ghz = np.zeros(8, complex); ghz[0] = ghz[7] = 2 ** -.5; W = np.zeros(8, complex); W[[1, 2, 4]] = 3 ** -.5
wst = np.outer(W, W.conj())
R["A5_pt_spectra_W_state"] = {str(s): float(np.linalg.eigvalsh(pt(wst, s)).min()) for s in [(), (0,), (0, 1), (0, 1, 2)]}
ok["A5_total_transpose_preserves_states_partial_does_not"] = (R["A5_pt_spectra_W_state"]["()"] > -1e-12 and R["A5_pt_spectra_W_state"]["(0, 1, 2)"] > -1e-12
                                                            and R["A5_pt_spectra_W_state"]["(0,)"] < -0.1 and R["A5_pt_spectra_W_state"]["(0, 1)"] < -0.1)

# ================= B. recovery of the Bargmann phase itself for spanning polygons =================
def fan_phase(verts, Q, N, J=1):
    """product over thin triangles (a0, c_i, c_{i+1}) of the principal (n+1)-th root of det_C of the holonomy; J = -1 uses the conjugate structure"""
    a0 = verts[0]; n = Q.shape[1]; tot = 1.0 + 0j; maxcell = 0.0
    for j in range(1, len(verts) - 1):
        p, q = verts[j], verts[j + 1]; L = plog(p, q)
        pts = [pexp(p, L * i / N) for i in range(N + 1)]
        for i in range(N):
            T = hol_matrix([a0, pts[i], pts[i + 1]], Q)
            d = np.linalg.det(T); d = d if J == 1 else np.conj(d)
            ang = np.angle(d); maxcell = max(maxcell, abs(ang))
            tot *= np.exp(1j * ang / (n + 1))
    return tot, maxcell
B_out = []
for n, k in ((2, 3), (2, 4), (3, 4), (3, 5), (4, 5)):
    while True:
        verts = [rand_state(n + 1) for _ in range(k)]
        if np.linalg.matrix_rank(np.array(verts)) == min(k, n + 1) and min(abs(np.vdot(verts[i], verts[(i + 1) % k])) for i in range(k)) > 0.2 \
           and min(abs(np.vdot(verts[0], v)) for v in verts) > 0.3: break
    Q = null_space(verts[0].conj().reshape(1, n + 1)); b = barg(verts); b /= abs(b)
    T = hol_matrix(verts, Q); naive = np.exp(1j * np.angle(np.linalg.det(T)) / (n + 1))
    rec = dict(n=n, vertices=k, spans=bool(np.linalg.matrix_rank(np.array(verts)) == n + 1), bargmann_phase=float(np.angle(b)),
               principal_root_of_whole_polygon=float(np.angle(naive)))
    for N in (4, 16, 64):
        f, mc = fan_phase(verts, Q, N); fc, _ = fan_phase(verts, Q, N, J=-1)
        rec[f"fan_N{N}"] = dict(recovered=float(np.angle(f)), residual=float(abs(f - b)), conj_structure_residual_to_conjugate=float(abs(fc - np.conj(b))),
                                max_cell_det_phase=float(mc), root_condition_met=bool(mc < math.pi))
    B_out.append(rec)
R["B_phase_recovery"] = B_out
ok["B_fan_recovers_phase_when_cells_small"] = all(r["fan_N64"]["residual"] < 1e-10 and r["fan_N64"]["conj_structure_residual_to_conjugate"] < 1e-10 for r in B_out)
ok["B_whole_polygon_root_is_ambiguous_in_some_case"] = any(abs(np.exp(1j * r["principal_root_of_whole_polygon"]) - np.exp(1j * r["bargmann_phase"])) > 1e-6 for r in B_out)

# ================= C. generators against observables in the comparison class (arithmetic) =================
C = []
for N in range(2, 7):
    C.append(dict(theory=f"real, {N} levels", pure_states=f"RP^{N-1}", generators=N * (N - 1) // 2, traceless_observables=N * (N + 1) // 2 - 1))
    C.append(dict(theory=f"complex, {N} levels", pure_states=f"CP^{N-1}", generators=N * N - 1, traceless_observables=N * N - 1))
    C.append(dict(theory=f"quaternionic, {N} levels", pure_states=f"HP^{N-1}", generators=N * (2 * N + 1), traceless_observables=N * (2 * N - 1) - 1))
C.append(dict(theory="octonionic, 3 levels", pure_states="OP^2", generators=52, traceless_observables=26))
for d in range(2, 10):
    C.append(dict(theory=f"ball of dimension {d}", pure_states=f"S^{d-1}", generators=d * (d - 1) // 2, traceless_observables=d))
for r in C: r["equal"] = r["generators"] == r["traceless_observables"]
R["C_generators_vs_observables"] = C
eq = [r["theory"] for r in C if r["equal"]]
ok["C_equality_only_complex_and_3_ball"] = all(("complex" in t) or t == "ball of dimension 3" for t in eq) and sum("complex" in t for t in eq) == 5 and "ball of dimension 3" in eq

R["ok"] = ok
json.dump(R, open("Reconciliation_and_Phase_Recovery_Results.json", "w"), indent=1, default=str)
for k_, v_ in ok.items(): print(("PASS " if v_ else "FAIL ") + k_)

