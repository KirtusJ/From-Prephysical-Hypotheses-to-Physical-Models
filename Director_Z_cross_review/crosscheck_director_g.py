#!/usr/bin/env python3
"""Director Z cross-check of two results of Director G (pull request 2, commit b626c0d): the field-embedding classification of
Probability_from_record_composition.md and the spinor bound and position law of Forced_envelope_and_classical_motion.md.
Nothing is imported from Director G's programs.  Routes: exact linear algebra over Q for the classification; a real-space walk on a ring
(not a fibre recursion) for the bound.  Predicates fixed before the run:
 X1  for M = 3, 5, 7, 9 the symmetric Q-bilinear forms B on K = Q(zeta_M, sqrt 2) with B(zeta x, y) = B(x, conj(zeta) y) and
     B(sqrt2 x, y) = B(x, sqrt2 y) form a space of dimension phi(M) (exact rational nullspace), and the forms Re(conj(sigma x) sigma y) of the
     phi(M) embeddings of the real subfield lie in it (residual below 1e-9) and are independent;
 X2  for M = 5: W = sum c_sigma |sigma(a)|^2 is multiplicative on 300 sampled pairs exactly when c is a unit vector (unit vectors: defect below
     1e-9; five other weight vectors: defect above 1e-3);
 X3  for M = 5 the amplitude (zeta^2 + zeta^-2)/sqrt 8 has squared modulus (3 + sqrt5)/16 in the ordinary embedding and (3 - sqrt5)/16 under
     zeta -> zeta^2 (to 1e-12), and s = q + sqrt2 - 2 with q = zeta + 1/zeta has |s| < 1 in exactly one of the four embeddings of the real subfield;
 X4  inputs of the bound: |w(k* + q) - w(k*) - q^2/2| <= q^4/6 for |q| <= 1 (grid of 4001 points); the section u(k) = P+(k) u* / |P+(k) u*| has
     |u'(k)| <= 2 for |k - k*| <= 1; the plus-band projector has Bloch vector (cos k, sin k, cos k)/sqrt(1 + cos^2 k);
 X5  bound (1): for three real-space runs the L2 distance between the walk and the encoded envelope is at most E(t) at every sampled time;
 X6  position law: for the two runs with epsilon = delta the characteristic function of the scaled lattice position at xi = 1 is within
     sqrt(eps) (|g'| + t |s g|) + 2 E(t) + 4 delta L of exp(i xi Y_c(t)), for one of the two orientations of the position axis, the same in both runs.
Writes Crosscheck_Director_G_Results.json; refuses to overwrite."""
import cmath, itertools, json, math, os, sys
from fractions import Fraction as Fr
from math import gcd
import numpy as np
import sympy as sp
OUT = "Crosscheck_Director_G_Results.json"
if os.path.exists(OUT): sys.exit("refusing to overwrite " + OUT)
R = {}; ok = lambda name, val, **info: R.__setitem__(name, dict(passed=bool(val), **info))
SEED = 20261117; rng = np.random.default_rng(SEED)

# ------------------------------------------------------------------ X1: exact nullspace
def field(M):
    """K = Q(zeta_M, sqrt2) with basis zeta^a s^b, a < phi(M), b in {0,1}; returns multiplication matrices of zeta and sqrt2 (sympy, rational)."""
    x = sp.symbols("x"); cp = sp.Poly(sp.cyclotomic_poly(M, x), x); d = cp.degree(); co = cp.all_coeffs()[::-1]   # co[i] x^i, monic
    Z = sp.zeros(d, d)
    for a in range(d - 1): Z[a + 1, a] = 1
    for i in range(d): Z[i, d - 1] = -co[i]
    I2 = sp.eye(2); S2 = sp.Matrix([[0, 2], [1, 0]])                                       # sqrt2 on basis (1, s)
    return sp.kronecker_product(Z, I2), sp.kronecker_product(sp.eye(d), S2), d
def phi(M): return sum(1 for j in range(1, M + 1) if gcd(j, M) == 1)
rows = []
for M in (3, 5, 7, 9):
    MZ, MS, d = field(M); n = 2 * d
    idx = {}; syms = []
    for i in range(n):
        for j in range(i, n): idx[(i, j)] = len(syms); syms.append(sp.Symbol(f"b{i}_{j}"))
    B = sp.Matrix(n, n, lambda i, j: syms[idx[(min(i, j), max(i, j))]])
    eqs = list(MZ.T * B * MZ - B) + list(MS.T * B - B * MS)
    A = sp.Matrix([[sp.Poly(e, *syms).coeff_monomial(s) if e != 0 else 0 for s in syms] for e in eqs if e != 0])
    dim = len(syms) - A.rank()
    # embeddings of the real subfield: zeta -> zeta^j (j up to sign), sqrt2 -> +-sqrt2
    forms = []
    for j in [j for j in range(1, M // 2 + 1) if gcd(j, M) == 1]:
        for sg in (1, -1):
            vec = np.array([cmath.exp(2j * math.pi * j * a / M) * (sg * math.sqrt(2)) ** b for a in range(d) for b in (0, 1)])       # sigma of each basis element
            forms.append(np.real(np.outer(np.conj(vec), vec)))
    MZn = np.array(MZ.tolist(), dtype=float); MSn = np.array(MS.tolist(), dtype=float)
    res = max(max(np.abs(MZn.T @ Bf @ MZn - Bf).max(), np.abs(MSn.T @ Bf - Bf @ MSn).max()) for Bf in forms)
    rank = int(np.linalg.matrix_rank(np.array([Bf.reshape(-1) for Bf in forms]), tol=1e-9))
    rows.append(dict(M=M, field_degree=n, unknowns=len(syms), solution_dimension=int(dim), euler_phi=phi(M), embeddings=len(forms), largest_residual_of_embedding_forms=float(res), rank_of_embedding_forms=rank))
    print(rows[-1], flush=True)
ok("X1_invariant_forms_are_spanned_by_the_embeddings", all(r["solution_dimension"] == r["euler_phi"] == r["embeddings"] == r["rank_of_embedding_forms"] and r["largest_residual_of_embedding_forms"] < 1e-9 for r in rows), rows=rows)

# ------------------------------------------------------------------ X2, X3: M = 5
M = 5; emb = [(j, sg) for j in (1, 2) for sg in (1, -1)]
def sigma(coeffs, j, sg): return sum(c * cmath.exp(2j * math.pi * j * a / M) * (sg * math.sqrt(2)) ** b for (a, b), c in coeffs.items())
def rand_elem(): return {(a, b): int(rng.integers(-2, 3)) for a in range(4) for b in (0, 1)}
def mult(u, v):
    out = {}
    for (a, b), c in u.items():
        for (a2, b2), c2 in v.items():
            aa = (a + a2) % 5; bb = b + b2; coef = c * c2 * (2 if bb == 2 else 1); bb %= 2
            if aa == 4:                                   # zeta^4 = -(1 + zeta + zeta^2 + zeta^3)
                for a3 in range(4): out[(a3, bb)] = out.get((a3, bb), 0) - coef
            else: out[(aa, bb)] = out.get((aa, bb), 0) + coef
    return out
pairs = [(rand_elem(), rand_elem()) for _ in range(300)]
def defect(c):
    W = lambda u: sum(ci * abs(sigma(u, j, sg)) ** 2 for ci, (j, sg) in zip(c, emb)); worst = 0.0
    for u, v in pairs:
        a, b, p = W(u), W(v), W(mult(u, v)); worst = max(worst, abs(p - a * b) / max(abs(p), abs(a * b), 1e-12))
    return worst
unit = {str(c): defect(c) for c in ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))}
other = {str(c): defect(c) for c in ((0.5, 0.5, 0, 0), (0.5, 0, 0.5, 0), (0.25, 0.25, 0.25, 0.25), (2, 0, 0, 0), (1, 0, 0, 1))}
ok("X2_multiplicative_exactly_for_single_embeddings", all(v < 1e-9 for v in unit.values()) and all(v > 1e-3 for v in other.values()), unit_weights=unit, other_weights=other, seed=SEED)
amp = lambda j: (cmath.exp(2j * math.pi * 2 * j / 5) + cmath.exp(-2j * math.pi * 2 * j / 5)) / math.sqrt(8)
v1, v2 = abs(amp(1)) ** 2, abs(amp(2)) ** 2
svals = {str((j, sg)): (2 * math.cos(2 * math.pi * j / 5) + sg * math.sqrt(2) - 2) for j, sg in emb}
ok("X3_five_sheet_values_and_discriminator", abs(v1 - (3 + math.sqrt(5)) / 16) < 1e-12 and abs(v2 - (3 - math.sqrt(5)) / 16) < 1e-12 and sum(1 for v in svals.values() if abs(v) < 1) == 1 and abs(svals["(1, 1)"]) < 1,
   ordinary=v1, conjugate=v2, s_under_each_embedding=svals)

# ------------------------------------------------------------------ X4: inputs of the bound
SQ2 = math.sqrt(2); ks = -math.pi / 2
def Uk(k): return np.array([[np.exp(-1j * k), np.exp(-1j * k)], [np.exp(1j * k), -np.exp(1j * k)]]) / SQ2
def omega(k): return math.asin(math.sin(k) / SQ2)
def Pplus(k):
    lam, vec = np.linalg.eig(Uk(k)); j = int(np.argmin(np.abs(lam - np.exp(-1j * omega(k))))); v = vec[:, j] / np.linalg.norm(vec[:, j]); return np.outer(v, v.conj())
ustar = np.linalg.eig(Uk(ks))[1][:, int(np.argmin(np.abs(np.linalg.eig(Uk(ks))[0] - np.exp(-1j * omega(ks)))))]; ustar = ustar / np.linalg.norm(ustar)
def u(k):
    w = Pplus(k) @ ustar; return w / np.linalg.norm(w)
qs = np.linspace(-1, 1, 4001); worst_ratio = 0.0
for q in qs:
    if abs(q) < 1e-3: continue
    worst_ratio = max(worst_ratio, abs(omega(ks + q) - omega(ks) - q * q / 2) / (q ** 4 / 6))
du = max(np.linalg.norm(u(ks + q + 1e-5) - u(ks + q - 1e-5)) / 2e-5 for q in np.linspace(-1, 1, 401))
sig = [np.array([[0, 1], [1, 0]]), np.array([[0, -1j], [1j, 0]]), np.array([[1, 0], [0, -1]])]
def bloch(k): P = Pplus(k); return np.array([np.real(np.trace(P @ s)) for s in sig])
best = None
for perm in itertools.permutations(range(3)):
    for signs in itertools.product((1, -1), repeat=3):
        err = max(np.abs(bloch(k)[list(perm)] * np.array(signs) - np.array([math.cos(k), math.sin(k), math.cos(k)]) / math.sqrt(1 + math.cos(k) ** 2)).max() for k in np.linspace(-3, 3, 61))
        if best is None or err < best[0]: best = (float(err), perm, signs)
ok("X4_inputs_of_the_bound", worst_ratio <= 1 + 1e-9 and du <= 2 and best[0] < 1e-9, largest_ratio_of_band_remainder_to_q4_over_6=float(worst_ratio), largest_section_derivative=float(du),
   bloch_vector_matches_up_to_axis_convention=dict(residual=best[0], axis_permutation=best[1], signs=best[2]),
   note="the Bloch vector is compared up to a permutation and signs of the three axes, which is a choice of Pauli basis for the two channels")

# ------------------------------------------------------------------ X5, X6: real-space walk
def bump(s): return np.where(np.abs(s) < 1, np.exp(-1.0 / np.maximum(1 - s * s, 1e-300)), 0.0)
def run(label, logN, delta, eps, p0, t_end, sample_every):
    N = 2 ** logN; h = 2 * math.pi / N; F = h / (eps * delta ** 3); dt = eps * delta ** 2; n_end = int(round(t_end / dt))
    kgrid = 2 * math.pi * np.fft.fftfreq(N); p = ((kgrid - ks + math.pi) % (2 * math.pi) - math.pi) / delta
    f = eps ** -0.25 * bump((p - p0) / math.sqrt(eps)); nz = np.nonzero(f)[0]
    dp = (2 * math.pi / N) / delta; f = f / math.sqrt((f ** 2).sum() * dp)                      # unit L2 norm in p
    # norms of g' and s g for the deviation bound (g = unit-norm bump in s = (p - p0)/sqrt eps)
    sgrid = np.linspace(-1, 1, 20001); g = bump(sgrid); g = g / math.sqrt((g ** 2).sum() * (sgrid[1] - sgrid[0])); gp = np.gradient(g, sgrid)
    ng1 = math.sqrt((gp ** 2).sum() * (sgrid[1] - sgrid[0])); nsg = math.sqrt(((sgrid * g) ** 2).sum() * (sgrid[1] - sgrid[0]))
    P = abs(p0) + math.sqrt(eps)
    A0 = np.zeros((N, 2), dtype=complex); usec = {}
    for m in nz: A0[m] = math.sqrt(dp) * f[m] * u(kgrid[m])
    psi = np.fft.ifft(A0, axis=0) * math.sqrt(N); x = np.arange(N); gph = np.exp(-1j * h * x) / SQ2
    xs_signed = np.where(x < N // 2, x, x - N)
    rows = []; worst_margin = -1e9
    for n in range(1, n_end + 1):
        s_ = (psi[:, 0] + psi[:, 1]) * gph; d_ = (psi[:, 0] - psi[:, 1]) * gph
        psi = np.empty_like(psi); psi[:, 0] = np.roll(s_, 1); psi[:, 1] = np.roll(d_, -1)
        if n % sample_every == 0 or n == n_end:
            t = n * dt; L = P + abs(F) * t; E = 2 * abs(F) * t * delta + t * delta ** 2 * L ** 4 / (6 * eps) + t * abs(F) * L * delta ** 2 / 2
            Afin = np.fft.fft(psi, axis=0) / math.sqrt(N)
            pred = np.zeros((N, 2), dtype=complex)
            for m in nz:
                pm = p[m]; ph = -(t * pm * pm / 2 - F * t * t * pm / 2 + F * F * t ** 3 / 6) / eps - n * omega(ks)
                m2 = (m - n) % N                                        # k -> k - n h, h = 2 pi / N
                pred[m2] = math.sqrt(dp) * f[m] * cmath.exp(1j * ph) * u(kgrid[m2])
            dist = float(np.linalg.norm(Afin - pred)); prob = (np.abs(psi) ** 2).sum(1)
            Yc = p0 * t - F * t * t / 2; dev = math.sqrt(eps) * (ng1 + t * nsg) + 2 * E + 4 * delta * L
            cf = {o: complex((prob * np.exp(1j * o * eps * delta * xs_signed)).sum()) for o in (1, -1)}        # xi = 1, two orientations of the axis
            rows.append(dict(t=t, steps=n, distance=dist, bound_E=E, within_bound=dist <= E, norm=float(prob.sum()), mean_scaled_position=float((prob * eps * delta * xs_signed).sum()), classical_Y=Yc,
                             charfn_error={str(o): abs(cf[o] - cmath.exp(1j * Yc)) for o in (1, -1)}, charfn_bound=dev))
            print(label, rows[-1], flush=True)
    return dict(label=label, sites=N, delta=delta, epsilon=eps, force_F=F, field_h=h, step_dt=dt, p0=p0, support_P=P, norm_g_prime=ng1, norm_s_g=nsg, rows=rows)
runs = [run("eps=1, delta=0.05", 16, 0.05, 1.0, 0.3, 1.0, 50), run("eps=delta=0.1", 16, 0.1, 0.1, 0.3, 1.0, 100), run("eps=delta=0.05", 20, 0.05, 0.05, 0.3, 0.5, 500)]
ok("X5_real_space_walk_within_the_spinor_bound", all(r["within_bound"] for rr in runs for r in rr["rows"]), runs=runs,
   largest_ratio_distance_to_bound=max(r["distance"] / r["bound_E"] for rr in runs for r in rr["rows"]),
   note="real-space step on a ring with the gain exp(-i h x) on arcs leaving site x; the envelope is encoded in the plus-band section built from the projector; distance in l2 over all fibres")
orient = None
for o in ("1", "-1"):
    if all(rr["rows"][-1]["charfn_error"][o] <= rr["rows"][-1]["charfn_bound"] for rr in runs[1:]): orient = o
fin = [dict(run=rr["label"], t=rr["rows"][-1]["t"], error=rr["rows"][-1]["charfn_error"], bound=rr["rows"][-1]["charfn_bound"], mean_scaled_position=rr["rows"][-1]["mean_scaled_position"], classical_Y=rr["rows"][-1]["classical_Y"]) for rr in runs[1:]]
ok("X6_position_characteristic_function_within_the_stated_chain_of_bounds", orient is not None, orientation_of_position_axis=orient, final_rows=fin,
   note="the bound is the sum of the three estimates of the paper: envelope deviation, 2 E(t), and 4 delta L for replacing the section by the constant spinor")
R["_summary"] = dict(predicates=sum(1 for k in R if not k.startswith("_")), passed=sum(1 for k, v in R.items() if not k.startswith("_") and v["passed"]), seed=SEED, numpy=np.__version__, sympy=sp.__version__)
json.dump(R, open(OUT, "w"), indent=1, default=str)
for k, v in R.items():
    if not k.startswith("_"): print(("PASS " if v["passed"] else "FAIL ") + k)
print(R["_summary"])
