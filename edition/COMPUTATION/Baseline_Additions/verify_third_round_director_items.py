#!/usr/bin/env python3
"""Independent recomputation of the decisive statements in the packets A3, B3 and G3 of LLM Directors A, B and G
(12 November 2026).  Nothing is imported from those packets.  Exact arithmetic (sympy) unless marked numeric.
Writes Third_Round_Director_Items_Results.json.  Each predicate is a boolean; a False is kept, not hidden."""
import itertools, json, math
import numpy as np, sympy as sp
from scipy.optimize import linprog
R = {}; ok = lambda name, val, **info: R.__setitem__(name, dict(passed=bool(val), **info))
t, x = sp.symbols('t x', positive=True)
k0 = sp.Matrix([1, 0]); k1 = sp.Matrix([0, 1]); kron = sp.kronecker_product
ket = lambda *b: kron(*[k1 if i else k0 for i in b])
proj = lambda v: v * v.H
PhiP = (ket(0, 0) + ket(1, 1)) / sp.sqrt(2); PsiP = (ket(0, 1) + ket(1, 0)) / sp.sqrt(2)
I2 = sp.eye(2)

# ---- H1 (Director A, A3-01): one-sided filter on rho_t = (1-t)|00><00| + t|Phi+><Phi+|
rho = (1 - t) * proj(ket(0, 0)) + t * proj(PhiP)
F = kron(sp.diag(x, 1), I2); rel = {x**2: t / (2 - t)}       # x > 0 with x^2 = t/(2-t)
out = F * rho * F.H; succ_x = sp.expand(out.trace()); num_x = sp.expand((PhiP.H * out * PhiP)[0])
succ = sp.simplify(succ_x.subs(rel)); ok("H1_A3_filter_success_is_t", sp.simplify(succ - t) == 0,
   first_run="a first version took x = sqrt(t/(2-t)) as an expression; sympy left an unevaluated adjoint for t < 2 and the predicate returned False although the value is t (0.1, 0.5, 0.9 at t = 0.1, 0.5, 0.9). Failure of the checking program, not of the statement; restated with x a positive symbol and x^2 = t/(2-t)")
# fidelity: num/succ with num = (1-t) x^2/2 + t (x+1)^2/4 ; claim (1+x)/2
ok("H1_A3_filter_fidelity_is_(1+x)/2", sp.simplify(sp.expand(num_x - t * (1 + x) / 2).subs(rel)) == 0)
xs = sp.sqrt(t / (2 - t)); gapA = (xs - t) / 2
ok("H1_A3_gap_positive_on_(0,1)", sp.simplify((t / (2 - t) - t**2) - t * (1 - t)**2 / (2 - t)) == 0, gap="(sqrt(t/(2-t)) - t)/2", at_half=float(gapA.subs(t, sp.Rational(1, 2))),
   note="x > t on (0,1) because x^2 - t^2 = t (1-t)^2/(2-t) > 0")
# largest Bell fidelity on K_t: separable states have <Phi+|s|Phi+> <= 1/2 (largest Schmidt coefficient squared)
# ---- H2 (Director B, B3-01): two-sided filter on (1-t)|00><00| + t|Psi+><Psi+|
rhoB = (1 - t) * proj(ket(0, 0)) + t * proj(PsiP)
e = sp.symbols('e', positive=True); FB = kron(sp.diag(e, 1), sp.diag(e, 1))
outB = FB * rhoB * FB.H; sB = sp.simplify(outB.trace()); fB = sp.simplify((PsiP.H * outB * PsiP)[0] / sB)
X = e**2
ok("H2_B3_success", sp.simplify(sB - X * (t + (1 - t) * X)) == 0)
ok("H2_B3_fidelity", sp.simplify(fB - t / (t + (1 - t) * X)) == 0)
gB = sp.simplify(fB - (1 + t) / 2); ok("H2_B3_gap_formula", sp.simplify(gB - (1 - t) * (t - (1 + t) * X) / (2 * (t + (1 - t) * X))) == 0)
half = {t: sp.Rational(1, 2), e: sp.Rational(1, 2)}
nB = (outB / sB).subs(half); sx = sp.Matrix([[0, 1], [1, 0]]); sy = sp.Matrix([[0, -sp.I], [sp.I, 0]]); sz = sp.diag(1, -1)
corr = [sp.simplify((kron(s, s) * nB).trace()) for s in (sx, sy, sz)]
ok("H2_B3_control_values", (sB.subs(half), fB.subs(half), gB.subs(half), corr) == (sp.Rational(5, 32), sp.Rational(4, 5), sp.Rational(1, 20), [sp.Rational(4, 5), sp.Rational(4, 5), sp.Rational(-3, 5)]),
   success=str(sB.subs(half)), fidelity=str(fB.subs(half)), excess=str(gB.subs(half)), XX_YY_ZZ=[str(c) for c in corr])
# ---- H3 (Director A, A3-04): four-party weight s.  E = 1 - (1-P)x(1-P), P = Bell projector
s = sp.symbols('s')
lhs = 1 - ((1 - t) / 2)**2                      # Tr E rho_t x rho_t with <P> = (1+t)/2
# bound on fully separable states: product pure states give (1-<P>_12)(1-<P>_34) >= 1/4, so E <= 3/4; all states E <= 1
need = sp.solve(sp.Eq(lhs, sp.Rational(3, 4) * (1 - s) + s), s)[0]
ok("H3_A3_parallel_preparation_needs_s_ge_2t-t^2", sp.simplify(need - (2 * t - t**2)) == 0)
ok("H3_A3_incompatible_with_s_le_t_inside_(0,1)", sp.simplify((2 * t - t**2) - t - t * (1 - t)) == 0)
rng = np.random.default_rng(2026111231); P4 = np.array(proj(PhiP)).astype(float); best = 0.0
for _ in range(20000):                           # numeric: product pure states of four qubits
    v = [rng.normal(size=2) + 1j * rng.normal(size=2) for _ in range(4)]; v = [u / np.linalg.norm(u) for u in v]
    a = np.kron(v[0], v[1]); b = np.kron(v[2], v[3]); pa = np.real(a.conj() @ P4 @ a); pb = np.real(b.conj() @ P4 @ b)
    best = max(best, 1 - (1 - pa) * (1 - pb))
ok("H3_product_state_bound_3/4_numeric", best <= 0.75 + 1e-12, largest_sampled=best, samples=20000)
# ---- H4 (Director A, A3-07): GHZ fidelity of states that are a product across a cut 1|23 is at most 1/2
ghz = np.zeros(8); ghz[0] = ghz[7] = 1 / math.sqrt(2)
sv = np.linalg.svd(ghz.reshape(2, 4), compute_uv=False)
ok("H4_GHZ_fidelity_bound_across_a_cut", abs(sv[0]**2 - 0.5) < 1e-14, largest_squared_Schmidt_coefficient=float(sv[0]**2))
# ---- H5 (A3-09, B3-02): a diagonal filter takes a|00>+b|11> to c|00>+d|11>
a_, b_, c_, d_, kap = sp.symbols('a b c d kappa', positive=True)
seed = a_ * ket(0, 0) + b_ * ket(1, 1); Fd = kron(sp.diag(kap * c_ / a_, kap * d_ / b_), I2); o5 = Fd * seed
ok("H5_filter_reaches_target_Schmidt_vector", sp.simplify(o5 - kap * (c_ * ket(0, 0) + d_ * ket(1, 1))) == sp.zeros(4, 1))
# ---- H6 (B3-03, G3 section 3.5): cycles
def cyc(n):
    P = np.zeros((n, n)); [P.__setitem__(((i + 1) % n, i), 1) for i in range(n)]; return P
rows = []
for n in range(3, 13):
    P = cyc(n); C = P - P.T; Q = np.eye(n) - np.ones((n, n)) / n
    rk = np.linalg.matrix_rank(C); row = dict(n=n, rank=int(rk))
    if n % 2:
        w, V = np.linalg.eigh(-C @ C); inv = V @ np.diag([0 if abs(u) < 1e-9 else u**-0.5 for u in w]) @ V.T
        J = C @ inv; S = np.eye(n)[::-1]
        row.update(J2_plus_Q=float(np.abs(J @ J + Q).max()), reversal=float(np.abs(S @ J @ S + J).max()))
        # commutant of rotation and reflection on the zero-sum space: solve XP=PX, XS=SX, X=QXQ
        basis = []
        for i in range(n):
            for j in range(n):
                E = np.zeros((n, n)); E[i, j] = 1; basis.append(E)
        M = np.array([np.concatenate([(B @ P - P @ B).ravel(), (B @ S - S @ B).ravel(), (B - Q @ B @ Q).ravel()]) for B in basis]).T
        ns = n * n - np.linalg.matrix_rank(M); row["dihedral_commutant_dim_on_zero_sum"] = int(ns)
    rows.append(row)
ok("H6_cycle_rank_parity", all(r["rank"] == (r["n"] - 1 if r["n"] % 2 else r["n"] - 2) for r in rows), rows=rows)
ok("H6_odd_cycle_polar_structure_and_reversal", all(r.get("J2_plus_Q", 0) < 1e-12 and r.get("reversal", 0) < 1e-12 for r in rows))
ok("H6_no_complex_structure_commuting_with_rotation_and_reflection", all(r["dihedral_commutant_dim_on_zero_sum"] == (r["n"] - 1) // 2 for r in rows if r["n"] % 2),
   note="commutant dimension (n-1)/2 = number of real two-dimensional irreducible constituents, each of real type")
# addition made here: the polar complex structure of the three-cycle does not commute with the compressed vertex projection
P3 = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]]); C3 = P3 - P3.T; Q3 = sp.eye(3) - sp.ones(3, 3) / 3; J3 = C3 / sp.sqrt(3)
ok("H6_three_cycle_C2_is_-3Q", C3 * C3 + 3 * Q3 == sp.zeros(3, 3))
E1 = Q3 * sp.diag(1, 0, 0) * Q3; com = sp.simplify(E1 * J3 - J3 * E1)
ok("H6_addition_vertex_projection_not_J_linear", com != sp.zeros(3, 3), commutator_Frobenius_norm=str(sp.nsimplify(sp.sqrt(sum(c**2 for c in com)))))
# ---- H7 (Director G, G3): the cubic Veronese model K_3 = conv{ n (x) n (x) n }
def v3(n): return np.einsum('i,j,k->ijk', n, n, n)
rng = np.random.default_rng(2026111232); pts = rng.normal(size=(400, 3)); pts /= np.linalg.norm(pts, axis=1)[:, None]
rank3 = np.linalg.matrix_rank(np.array([v3(n).ravel() for n in pts]))
ok("H7_K3_spans_ten_dimensions", rank3 == 10, rank=int(rank3))
tau = lambda T: np.einsum('ijj->i', T)
ok("H7_contraction_returns_n", max(np.abs(tau(v3(n)) - n).max() for n in pts) < 1e-12)
north, south = np.array([0, 0, 1.0]), np.array([0, 0, -1.0]); eq = [np.array([math.cos(a), math.sin(a), 0.0]) for a in (0, 2 * math.pi / 3, 4 * math.pi / 3)]
Tanti = (v3(north) + v3(south)) / 2; Ttri = sum(v3(n) for n in eq) / 3; ex = np.array([1.0, 0, 0])
Ecub = lambda m, T: (1 + np.einsum('ijk,i,j,k->', T, m, m, m)) / 2
ok("H7_equal_Bloch_means_different_cubic_effect", np.abs(tau(Tanti)).max() < 1e-12 and np.abs(tau(Ttri)).max() < 1e-12 and abs(Ecub(ex, Tanti) - 0.5) < 1e-12 and abs(Ecub(ex, Ttri) - 0.625) < 1e-12,
   E_x=[float(Ecub(ex, Tanti)), float(Ecub(ex, Ttri))])
# kernel of all tests F_m: tensors with zero contraction, inside the 10-dimensional symmetric space
symbasis = []
for idx in itertools.combinations_with_replacement(range(3), 3):
    T = np.zeros((3, 3, 3))
    for p in set(itertools.permutations(idx)): T[p] = 1
    symbasis.append(T)
kdim = 10 - np.linalg.matrix_rank(np.array([tau(T) for T in symbasis]))
ok("H7_kernel_of_projective_tests_has_dimension_7", kdim == 7, kernel_dimension=int(kdim))
# addition made here.  An affine effect on K_3 is n -> c + q(n), q a cubic form.  e(n) = 1/2 + (x^3 - 3 x y^2)/2 is an effect:
# |x^3 - 3xy^2| = r^3 |cos 3 phi| <= 1 on the unit sphere.  It is 1 at azimuth 0 and 0 at azimuth 60 degrees on the equator.
th, ph = sp.symbols('theta phi', real=True); xx = sp.sin(th) * sp.cos(ph); yy = sp.sin(th) * sp.sin(ph)
ok("H7_addition_harmonic_cubic_is_r^3_cos3phi", sp.simplify(xx**3 - 3 * xx * yy**2 - sp.sin(th)**3 * sp.cos(3 * ph)) == 0)
eh = lambda n: 0.5 + 0.5 * (n[0]**3 - 3 * n[0] * n[1]**2)
n60 = np.array([0.5, math.sqrt(3) / 2, 0.0])
ok("H7_addition_states_at_Bloch_angle_60deg_perfectly_distinguished", abs(eh(ex) - 1) < 1e-15 and abs(eh(n60)) < 1e-15 and all(-1e-12 <= eh(n) <= 1 + 1e-12 for n in pts),
   effect_values=[float(eh(ex)), float(eh(n60))], qubit_value_at_60deg=0.75,
   note="with every affine effect admitted, the pure states of K_3 at Bloch angle 60 degrees are perfectly distinguishable; the qubit transition probability there is 3/4")
# infimum over admitted effects certain on m of their value on n (numeric linear program on a grid of 2562+ directions)
def fib(N):
    i = np.arange(N) + 0.5; z = 1 - 2 * i / N; r = np.sqrt(1 - z * z); a = math.pi * (1 + 5**0.5) * i
    return np.stack([r * np.cos(a), r * np.sin(a), z], 1)
grid = fib(4000); mono = list(itertools.combinations_with_replacement(range(3), 3))
feat = lambda n: np.array([n[i] * n[j] * n[k] for i, j, k in mono])
Aub = np.vstack([np.hstack([np.ones((len(grid), 1)), np.array([feat(n) for n in grid])]), -np.hstack([np.ones((len(grid), 1)), np.array([feat(n) for n in grid])])])
bub = np.concatenate([np.ones(len(grid)), np.zeros(len(grid))]); tab = []
for deg in (20, 40, 60, 90, 120, 150):
    a = math.radians(deg); n = np.array([math.cos(a), math.sin(a), 0.0])
    res = linprog(np.concatenate([[1.0], feat(n)]), A_ub=Aub, b_ub=bub, A_eq=[np.concatenate([[1.0], feat(ex)])], b_eq=[1.0], bounds=[(None, None)] * 11)
    tab.append(dict(angle_deg=deg, infimum_numeric=round(float(res.fun), 6), qubit=round((1 + math.cos(a)) / 2, 6)))
ok("H7_addition_intrinsic_table_differs_from_qubit_table", all(r["infimum_numeric"] < r["qubit"] - 1e-3 for r in tab if r["angle_deg"] < 180), table=tab,
   note="numeric linear program, constraints on 4000 directions; not an enclosure")
# ---- H8 (Director G): adaptive words under the restricted instrument (test F_m, then prepare v(+-m))
def words_K3(T, ms):
    out = {}
    def rec(state_tau, i, pr, w):
        if i == len(ms): out[w] = pr; return
        for sgn in (1, -1):
            p = (1 + sgn * ms[i] @ state_tau) / 2
            rec(sgn * ms[i], i + 1, pr * p, w + ("+" if sgn > 0 else "-"))
    rec(tau(T), 0, 1.0, ""); return out
def words_qubit(r, ms):
    sig = [np.array([[0, 1], [1, 0]]), np.array([[0, -1j], [1j, 0]]), np.diag([1, -1])]
    rho0 = (np.eye(2) + sum(r[i] * sig[i] for i in range(3))) / 2; out = {}
    def rec(rho, i, w):
        if i == len(ms): out[w] = float(np.real(np.trace(rho))); return
        for sgn in (1, -1):
            Pm = (np.eye(2) + sgn * sum(ms[i][j] * sig[j] for j in range(3))) / 2; rec(Pm @ rho @ Pm, i + 1, w + ("+" if sgn > 0 else "-"))
    rec(rho0, 0, ""); return out
worst = 0.0
for _ in range(60):
    w = rng.dirichlet(np.ones(5)); ns = rng.normal(size=(5, 3)); ns /= np.linalg.norm(ns, axis=1)[:, None]; T = sum(wi * v3(n) for wi, n in zip(w, ns))
    ms = rng.normal(size=(3, 3)); ms /= np.linalg.norm(ms, axis=1)[:, None]
    a, b = words_K3(T, ms), words_qubit(tau(T), ms); worst = max(worst, max(abs(a[k] - b[k]) for k in a))
ok("H8_restricted_instrument_words_equal_qubit_words", worst < 1e-12, largest_difference=worst, cases=60, words_per_case=8,
   note="under the restricted instrument the outcome statistics depend on T through its contraction only: the operational quotient is the Bloch ball")
R["_summary"] = dict(predicates=sum(1 for k in R if not k.startswith("_")), passed=sum(1 for k, v in R.items() if not k.startswith("_") and v["passed"]), seeds=[2026111231, 2026111232])
json.dump(R, open("Third_Round_Director_Items_Results.json", "w"), indent=1, default=str)
for k, v in R.items():
    if not k.startswith("_"): print(("PASS " if v["passed"] else "FAIL ") + k)
print(R["_summary"])
