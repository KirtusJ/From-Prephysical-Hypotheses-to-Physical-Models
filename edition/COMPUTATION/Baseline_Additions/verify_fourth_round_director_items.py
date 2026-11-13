#!/usr/bin/env python3
"""Independent recomputation of the decisive statements in the packets A4, B4 and G4 of LLM Directors A, B and G
(12 November 2026).  Nothing is imported from those packets.  Writes Fourth_Round_Director_Items_Results.json."""
import itertools, json, math
import numpy as np, sympy as sp
R = {}; ok = lambda name, val, **info: R.__setitem__(name, dict(passed=bool(val), **info))
w3 = sp.Rational(-1, 2) + sp.sqrt(3) * sp.I / 2

def gain_matrix(n, edges, chi):
    """edges: (a, b, g) means the oriented edge a->b has gain g; entry [b, a] = chi(g), entry [a, b] = conj"""
    A = sp.zeros(n, n)
    for a, b, g in edges: A[b, a] = chi(g); A[a, b] = sp.conjugate(chi(g))
    return A
K4 = lambda special: [(a, b, 1 if (a, b) == special else 0) for a in range(4) for b in range(a + 1, 4)]
chi3 = lambda g: w3**g
# ---- G1 (A4-02, B4-02): extension of events by all continuations
A = gain_matrix(4, K4((2, 3)), chi3); e = lambda i: sp.Matrix([1 if j == i else 0 for j in range(4)])
v1, v2 = e(1), e(2)                                   # one-step events from vertex 0 ending at 1 and at 2
D1 = (v2.H * v1)[0]; D2 = sp.simplify(((A * v2).H * (A * v1))[0])
masses = [sp.simplify(((A**k * e(0)).H * (A**k * e(0)))[0]) for k in range(3)]
ok("G1_A4_extension_changes_a_vanishing_cross_term", D1 == 0 and sp.simplify(sp.Abs(D2)**2 - 1) == 0, D1=str(D1), D2=str(D2), total_masses=[str(m) for m in masses])
ok("G1_A4_total_masses_1_3_15", masses == [1, 3, 15])
AB = gain_matrix(4, K4((0, 3)), chi3); DB = sp.simplify(((AB * e(2)).H * (AB * e(1)))[0])
ok("G1_B4_cross_term_0_to_2", DB == 2, value=str(DB), note="Director B places the gain on the edge (0,3); extensions of the one-step events ending at 1 and 2")
# criterion: consistency under continuation (up to one factor per length) on the reachable span is A*A = c there
AA = sp.simplify(A.H * A); ok("G1_criterion_AstarA_not_scalar_for_K4_with_one_gain", AA != AA[0, 0] * sp.eye(4), diagonal=[str(AA[i, i]) for i in range(4)])
# K4: no signing is consistent (exhaustive over the 64 signings); a Hermitian assignment of gains of order 4 is, and its normalized step is an involution (B4-03)
pairs = [(a, b) for a in range(4) for b in range(a + 1, 4)]; nsign = 0
for sg in itertools.product((1, -1), repeat=6):
    M = sp.zeros(4, 4)
    for (a_, b_), s_ in zip(pairs, sg): M[a_, b_] = M[b_, a_] = s_
    nsign += (M * M == 3 * sp.eye(4))
H4 = sp.Matrix([[0, 1, 1, 1], [1, 0, sp.I, -sp.I], [1, -sp.I, 0, sp.I], [1, sp.I, -sp.I, 0]])
ok("G1_K4_no_consistent_signing_one_with_order_4_gains", nsign == 0 and H4.H == H4 and H4 * H4 == 3 * sp.eye(4), consistent_signings_of_K4=int(nsign),
   first_run="a first version asserted a signing of K4 with square 3; the matrix written was not symmetric and the predicate returned False. The assertion was wrong: no signing of K4 has square 3. Restated")
# ---- G2 (A4-03, B4-04, DG4-02): additive rules.  Weight F_open(g) on open walks and F_closed(g) on closed walks.
def switch_test(group, mul, inv, Fo, Fc, trials, rng):
    """largest change of the weight of a single walk under random switching on a triangle with a pendant vertex"""
    worst = 0.0; els = group
    for _ in range(trials):
        g = [els[rng.integers(len(els))] for _ in range(4)]         # gains on 0->1, 1->2, 2->0, 0->3
        h = [els[rng.integers(len(els))] for _ in range(4)]
        closed = mul(g[2], mul(g[1], g[0])); openw = g[3]
        closed_s = mul(h[0], mul(closed, inv(h[0]))); open_s = mul(h[3], mul(openw, inv(h[0])))
        worst = max(worst, abs(Fc(closed) - Fc(closed_s)), abs(Fo(openw) - Fo(open_s)))
    return worst
rng = np.random.default_rng(2026111241)
Z3 = [0, 1, 2]; m3 = lambda a, b: (a + b) % 3; i3 = lambda a: (-a) % 3
nu_c = lambda g: 1 + math.cos(2 * math.pi * g / 3)
ok("G2_closed_walk_rule_is_invariant_and_sees_holonomy", switch_test(Z3, m3, i3, lambda g: 1.0, nu_c, 2000, rng) < 1e-12 and abs(nu_c(0) - 2) < 1e-12 and abs(nu_c(1) - 0.5) < 1e-12,
   weights_of_closed_walk_with_gain_0_and_1=[nu_c(0), nu_c(1)])
ok("G2_open_walk_rule_must_be_constant", switch_test(Z3, m3, i3, nu_c, nu_c, 2000, rng) > 0.5)
perms = list(itertools.permutations(range(3))); pm = lambda a, b: tuple(a[b[i]] for i in range(3)); pinv = lambda a: tuple(sorted(range(3), key=lambda i: a[i]))
fixp = lambda a: float(sum(1 for i in range(3) if a[i] == i)); nonclass = lambda a: float(a[0])
ok("G2_S3_class_function_invariant_nonclass_not", switch_test(perms, pm, pinv, lambda g: 1.0, fixp, 2000, rng) == 0 and switch_test(perms, pm, pinv, lambda g: 1.0, nonclass, 2000, rng) > 0)
# ---- G3 (A4-01, B4-01, DG4-01): growth witnesses in terms of the gain augmented by length parity
def aug_holonomy(n, edges, m):
    nb = {}
    for a, b, g in edges: nb.setdefault(a, []).append((b, g % m)); nb.setdefault(b, []).append((a, (-g) % m))
    pot = {0: (0, 0)}; st = [0]; gens = set()
    while st:
        a = st.pop()
        for b, g in nb[a]:
            new = ((pot[a][0] + g) % m, (pot[a][1] + 1) % 2)
            if b not in pot: pot[b] = new; st.append(b)
            else: gens.add(((new[0] - pot[b][0]) % m, (new[1] - pot[b][1]) % 2))
    H = {(0, 0)}
    while True:
        H2 = H | {((a + c) % m, (b + d) % 2) for (a, b) in H for (c, d) in gens}
        if H2 == H: return H
        H = H2
def cover(n, edges, m):
    B = np.zeros((n * m, n * m), dtype=object)
    for a, b, g in edges:
        for s in range(m): B[b * m + (s + g) % m, a * m + s] += 1; B[a * m + s, b * m + (s + g) % m] += 1
    return B
bow = [(0, 1, 0), (1, 2, 0), (2, 0, 0), (0, 3, 0), (3, 4, 0), (4, 0, 1)]
wit = {"K4, gain on 2->3 (A)": (4, K4((2, 3))), "K4, gain on 0->3 (B)": (4, K4((0, 3))), "two triangles at a vertex (G)": (5, bow)}
rows = []
for name, (n, ed) in wit.items():
    H = aug_holonomy(n, ed, 3); B = cover(n, ed, 3); P = np.eye(n * 3, dtype=object).astype(object); mins = {}
    for k in range(1, 25):
        P = B.dot(P); mins[k] = int(min(P[:, 0]))
    rows.append(dict(witness=name, augmented_holonomy_order=len(H), least_count_from_base=mins))
ok("G3_all_three_witnesses_have_full_augmented_holonomy", all(r["augmented_holonomy_order"] == 6 for r in rows), rows=[dict(witness=r["witness"], order=r["augmented_holonomy_order"], least_count_at_5_10_18_24=[r["least_count_from_base"][k] for k in (5, 10, 18, 24)]) for r in rows])
ok("G3_B4_bound_3^floor((k-10)/2)", all(rows[1]["least_count_from_base"][k] >= 3 ** ((k - 10) // 2) for k in range(10, 25)))
ok("G3_G4_bound_2^(k-5)", all(rows[2]["least_count_from_base"][k] >= 2 ** (k - 5) for k in range(5, 25)), least_at_5=rows[2]["least_count_from_base"][5])
# ---- G4 (DG4-03): synchronized product of two four-cycles
C4 = np.zeros((4, 4), dtype=complex); z = np.exp(2j * math.pi / 3)
for a in range(4):
    g = z if a == 3 else 1.0; b = (a + 1) % 4; C4[b, a] = g; C4[a, b] = np.conj(g)
def reach(k):                     # span of event vectors at length k from vertex 0: coordinates of reachable end vertices (holonomy group is all of Z_3, counts large)
    return np.nonzero(np.abs(np.linalg.matrix_power(np.abs(C4), k)[:, 0]) > 0)[0]
single = set(); sync = set()
for k in range(1, 12):
    r = reach(k); single |= set(r.tolist()); sync |= {(a, b) for a in r for b in r}
ok("G4_synchronized_product_reaches_8_of_16_endpoint_pairs", len(single) == 4 and len(sync) == 8, single=len(single), synchronized=len(sync),
   note="at a fixed common length the product space is the tensor product (G8 Proposition 6.1); the union over lengths is smaller than the tensor product of the unions when both factors are bipartite")
amp = sum(np.conj(C4[2, m]) * 0 + C4[2, m] * C4[m, 0] for m in (1, 3))
ok("G4_holonomy_present_in_the_four_cycle", abs(abs(amp) ** 2 - 1) < 1e-12, squared_modulus_of_two_path_sum=float(abs(amp) ** 2))
# ---- G5 (A4-04, B4-05): the determinant law of G7; lift phase and tangent determinant for the two control triangles
def lift_and_det(vs):
    a = [np.array(v, dtype=complex) / np.linalg.norm(v) for v in vs]; k = len(a); a.append(a[0])
    B = np.prod([np.vdot(a[j], a[j + 1]) for j in range(k)])
    lift = a[0].copy(); cur = a[0].copy(); U = np.eye(2, dtype=complex)
    for j in range(k):
        nxt = a[j + 1] * np.exp(-1j * np.angle(np.vdot(cur, a[j + 1])))           # phase with <cur|nxt> > 0
        c = np.real(np.vdot(cur, nxt)); u = nxt - c * cur; u /= np.linalg.norm(u); t = math.acos(min(1.0, c))
        Rt = np.eye(2, dtype=complex) + (math.cos(t) - 1) * (np.outer(cur, cur.conj()) + np.outer(u, u.conj())) + math.sin(t) * (np.outer(u, cur.conj()) - np.outer(cur, u.conj()))
        U = Rt @ U; cur = nxt
    phase_lift = np.vdot(a[0], cur)                                                # cur = phase_lift * a0
    wperp = np.array([-np.conj(a[0][1]), np.conj(a[0][0])])
    T = np.vdot(wperp, np.conj(phase_lift) * (U @ wperp))                          # tangent (a0, w) ~ (cur, U w) ~ (a0, conj(phase) U w)
    return B, phase_lift, T
rows = []
for name, vs in (("Director A", [(1, 0), (math.sqrt(3) / 2, 0.5), (math.sqrt(3) / 2, 0.5j)]), ("Director B", [(1, 0), (1, 1), (1, 1j)])):
    B, ph, T = lift_and_det(vs); rows.append(dict(control=name, B=str(np.round(B, 12)), lift_phase=str(np.round(ph, 12)), conj_B_over_modulus=str(np.round(np.conj(B) / abs(B), 12)), det_T=str(np.round(T, 12)), B_over_modulus_squared=str(np.round((B / abs(B)) ** 2, 12)),
                                              ok=bool(abs(ph - np.conj(B) / abs(B)) < 1e-12 and abs(T - (B / abs(B)) ** 2) < 1e-12)))
ok("G5_lift_phase_is_conj(B)/|B|_and_det_T_is_(B/|B|)^2", all(r["ok"] for r in rows), rows=rows,
   note="the printed proof of G7 Proposition 4.3 defines theta by exp(i theta) = conj(B)/|B|; with that definition its lift phase exp(i theta) and its T = exp(-i theta) U agree with these values. The overline is present in the typeset page and in the source and is lost by text extraction of the PDF")
# ---- G6 (DG4-05): optimum of the unnormalized filter witness
t, x = sp.symbols('t x', positive=True); W = (1 - t) * x * (t - (1 + t) * x) / 2; xs = sp.solve(sp.diff(W, x), x)[0]
ok("G6_G4_filter_optimum", sp.simplify(xs - t / (2 * (1 + t))) == 0 and sp.simplify(W.subs(x, xs) - t**2 * (1 - t) / (8 * (1 + t))) == 0)
# ---- G7 (DG4-04): exp(-isH) is unitary for the Hermitian represented adjacency although no multiple of H is
Hb = np.array(gain_matrix(5, bow, chi3).evalf()).astype(complex); wv, V = np.linalg.eigh(Hb); Us = V @ np.diag(np.exp(-0.7j * wv)) @ V.conj().T
X = np.array([[0, 1], [1, 0]], dtype=complex); psi = np.zeros(4, dtype=complex); psi[0] = 1
def evol(Hm, s): wv, V = np.linalg.eigh(Hm); return V @ np.diag(np.exp(-1j * s * wv)) @ V.conj().T @ psi
conc = lambda p: 2 * abs(p[0] * p[3] - p[1] * p[2])
ok("G7_G4_formal_exponential_controls", np.abs(Us.conj().T @ Us - np.eye(5)).max() < 1e-12 and [round(float(np.real(d))) for d in np.diag(Hb @ Hb)] == [4, 2, 2, 2, 2] and abs(conc(evol(np.kron(X, X), math.pi / 4)) - 1) < 1e-12 and conc(evol(np.kron(X, np.eye(2)) + np.kron(np.eye(2), X), math.pi / 4)) < 1e-12,
   note="the imaginary unit, the continuous parameter and the choice between the two product generators are inputs")
R["_summary"] = dict(predicates=sum(1 for k in R if not k.startswith("_")), passed=sum(1 for k, v in R.items() if not k.startswith("_") and v["passed"]), seed=2026111241)
json.dump(R, open("Fourth_Round_Director_Items_Results.json", "w"), indent=1, default=str)
for k, v in R.items():
    if not k.startswith("_"): print(("PASS " if v["passed"] else "FAIL ") + k, {a: b for a, b in v.items() if a not in ("passed", "rows", "note")})
print(R["_summary"])
