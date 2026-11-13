#!/usr/bin/env python3
"""Part E of the computations for edition Z2 (cited by papers G7 and G8). Constructed trial GH-1: finite gain graphs (graphs with a group-valued
transport on edges, up to switching) and gauge-invariant additive set functions on walks.
All quantities are finite enumerations; integer or exact where stated, otherwise double precision."""
import json, itertools, math
import numpy as np
rng = np.random.default_rng(2026111203)
R, ok = {}, {}

# ---------------- finite groups as matrix groups (faithful unitary representation) with irreducible characters ----------------
class Grp:
    def __init__(s, name, mats, irreps):
        s.name, s.mats, s.irreps = name, mats, irreps          # mats: list of faithful matrices; irreps: list of lists of matrices aligned with mats
        s.n = len(mats)
        key = lambda M: tuple(np.round(M.flatten(), 6))
        s.index = {key(M): i for i, M in enumerate(mats)}
        s.mul = np.array([[s.index[key(mats[i] @ mats[j])] for j in range(s.n)] for i in range(s.n)])
        s.inv = np.array([int(np.where(s.mul[i] == s.index[key(np.eye(mats[0].shape[0]))])[0][0]) for i in range(s.n)])
        s.e = s.index[key(np.eye(mats[0].shape[0]))]
        s.chars = np.array([[np.trace(rep[i]) for i in range(s.n)] for rep in irreps])
def cyclic(n):
    mats = [np.array([[np.exp(2j * math.pi * k / n)]]) for k in range(n)]
    irreps = [[np.array([[np.exp(2j * math.pi * j * k / n)]]) for k in range(n)] for j in range(n)]
    return Grp(f"Z_{n}", mats, irreps)
def closure(gens):
    key = lambda M: tuple(np.round(M.flatten(), 6)); els = {key(np.eye(gens[0].shape[0])): np.eye(gens[0].shape[0], dtype=complex)}
    fr = list(els.values())
    while fr:
        nw = []
        for M in fr:
            for g in gens:
                P = M @ g
                if key(P) not in els: els[key(P)] = P; nw.append(P)
        fr = nw
    return list(els.values())
def q8():
    i = np.array([[1j, 0], [0, -1j]]); j = np.array([[0, 1], [-1, 0]], complex)
    mats = closure([i, j])
    triv = [np.eye(1) for _ in mats]
    def sign_rep(kill):   # one-dimensional characters: kernel contains a chosen generator
        out = []
        for M in mats:
            # express M = +-1, +-i, +-j, +-k ; character by images i->a, j->b
            a, b = kill
            if np.allclose(abs(M[0, 0]), 1) and np.allclose(M[0, 0].imag, 0): v = 1            # +-1
            elif np.allclose(abs(M[0, 0]), 1): v = a                                           # +-i
            elif np.allclose(M[0, 1].imag, 0): v = b                                           # +-j
            else: v = a * b                                                                    # +-k
            out.append(np.array([[v]], complex))
        return out
    return Grp("Q_8", mats, [triv, sign_rep((1, -1)), sign_rep((-1, 1)), sign_rep((-1, -1)), mats])
def s3():
    c, s = math.cos(2 * math.pi / 3), math.sin(2 * math.pi / 3)
    r = np.array([[c, -s], [s, c]], complex); f = np.array([[1, 0], [0, -1]], complex)
    mats = closure([r, f])
    return Grp("S_3", mats, [[np.eye(1) for _ in mats], [np.array([[np.linalg.det(M).real]], complex) for M in mats], mats])

# ---------------- gain graphs ----------------
def random_gain_graph(nv, extra, G):
    edges = [(i, int(rng.integers(0, i))) for i in range(1, nv)]             # random spanning tree
    while len(edges) < nv - 1 + extra:
        a, b = sorted(rng.choice(nv, 2, replace=False))
        if (b, a) not in edges and (a, b) not in edges: edges.append((int(b), int(a)))
    gain = {}
    for (a, b) in edges:
        g = int(rng.integers(0, G.n)); gain[(a, b)] = g; gain[(b, a)] = int(G.inv[g])    # gain of the reversed edge is the inverse
    return gain
def switch(gain, h, G):          # g_e -> h_t g_e h_s^{-1}; path gain w: x->y becomes h_y g_w h_x^{-1}
    return {(a, b): int(G.mul[h[b]][G.mul[g][G.inv[h[a]]]]) for (a, b), g in gain.items()}
def walks(gain, x, k, G):
    """all walks of length k from x: list of (end vertex, gain, vertex sequence); gain of a walk = product of edge gains, later edges on the left"""
    nb = {}
    for (a, b) in gain: nb.setdefault(a, []).append(b)
    out = [(x, G.e, (x,))]
    for _ in range(k):
        out = [(b, int(G.mul[gain[(v, b)]][g]), seq + (b,)) for (v, g, seq) in out for b in nb.get(v, [])]
    return out
def D(S1, S2, f, G):             # bi-additive function: sum over coterminous pairs of f(g_w g_w'^{-1})
    return sum(f[G.mul[g1][G.inv[g2]]] for (y1, g1, _) in S1 for (y2, g2, _) in S2 if y1 == y2)

# ============ E1 gauge behaviour ============
E1 = []
for G in (cyclic(4), cyclic(5), s3(), q8()):
    gain = random_gain_graph(6, 4, G); h = [int(rng.integers(0, G.n)) for _ in range(6)]; gain2 = switch(gain, h, G)
    W = walks(gain, 0, 5, G); W2 = walks(gain2, 0, 5, G)
    assert [w[2] for w in W] == [w[2] for w in W2]
    f = (G.chars[-1]).copy()                                   # a character (class function)
    idx = rng.choice(len(W), min(40, len(W)), replace=False); S = [W[i] for i in idx]; S2 = [W2[i] for i in idx]
    inv_pair = abs(D(S, S, f, G) - D(S2, S2, f, G))
    # single-walk gains are not invariant; coterminous pair gains are invariant up to conjugation; non-coterminous pair products are not
    single_changed = sum(w[1] != w2[1] for w, w2 in zip(W, W2))
    nonclass = rng.normal(size=G.n)                            # a function on the group that is not a class function
    viol = abs(D(S, S, nonclass, G) - D(S2, S2, nonclass, G))  # same set twice: only f(x) + f(x^-1) enters
    half = len(S) // 2
    viol2 = abs(D(S[:half], S[half:], nonclass, G) - D(S2[:half], S2[half:], nonclass, G))   # two different sets
    E1.append(dict(group=G.name, walks=len(W), single_walk_gains_changed=int(single_changed), class_function_pair_sum_change=float(inv_pair),
                   non_class_function_measure_change=float(viol), non_class_function_two_set_change=float(viol2), abelian=bool((G.mul == G.mul.T).all())))
R["E1_gauge"] = E1
ok["E1_pair_sums_of_class_functions_are_switching_invariant"] = all(r["class_function_pair_sum_change"] < 1e-9 and r["single_walk_gains_changed"] > 0 for r in E1)
ok["E1_non_class_functions_fail_for_nonabelian_gains_on_two_sets"] = all(r["non_class_function_two_set_change"] > 1e-6 for r in E1 if not r["abelian"])
# retained observation: for Q_8 the measure of a single set did not change under a non-class weight. Every element of Q_8 is conjugate only to itself
# or its inverse, so f(x) + f(x^-1), the only combination entering D(S,S), is a class function there.
R["E1_note_Q8"] = "D(S,S) with a non-class weight was unchanged for Q_8 (change 0.0): in Q_8 each conjugacy class is {x, x^-1}, so the symmetrized weight is a class function"

# ============ E2 positivity: f positive definite on the group  <=>  nonnegative combination of irreducible characters ============
E2 = []
for G in (cyclic(2), cyclic(4), cyclic(5), cyclic(6), s3(), q8()):
    agree = 0; trials = 3000; npos = 0
    classes = {}
    for g in range(G.n): classes.setdefault(tuple(np.round(G.chars[:, g], 6)), []).append(g)       # conjugacy classes separated by characters
    for _ in range(trials):
        coef = rng.normal(size=len(G.irreps)) * (rng.random(len(G.irreps)) < 0.8)
        if rng.random() < 0.5: coef = np.abs(coef)
        f = (coef[:, None] * G.chars).sum(0)                                                       # class function with real coefficients
        K = np.array([[f[G.mul[a][G.inv[b]]] for b in range(G.n)] for a in range(G.n)])
        herm = np.allclose(K, K.conj().T)
        psd = herm and np.linalg.eigvalsh((K + K.conj().T) / 2).min() > -1e-9
        cpos = (coef > -1e-12).all()
        agree += (psd == cpos); npos += psd
    E2.append(dict(group=G.name, trials=trials, positive_definite=int(npos), agreement=int(agree)))
R["E2_bochner"] = E2
ok["E2_positive_definite_iff_nonnegative_character_coefficients"] = all(r["agreement"] == r["trials"] for r in E2)

# Born form: for an irreducible character chi_rho, D(S,S) = || sum_w rho(g_w) ||_HS^2
E2b = []
for G in (cyclic(4), s3(), q8()):
    gain = random_gain_graph(6, 5, G); W = walks(gain, 0, 6, G); S = [W[i] for i in rng.choice(len(W), 50, replace=False)]
    for r_i, rep in enumerate(G.irreps):
        lhs = D(S, S, G.chars[r_i], G)
        rhs = 0.0
        for y in set(w[0] for w in S):
            A = sum(rep[w[1]] for w in S if w[0] == y); rhs += np.linalg.norm(A) ** 2
        E2b.append(dict(group=G.name, irrep=r_i, dim=int(rep[0].shape[0]), D=float(np.real(lhs)), sum_of_squared_norms=float(rhs)))
R["E2b_born_form"] = E2b
ok["E2b_measure_equals_squared_norm_of_summed_representation_matrices"] = all(abs(r["D"] - r["sum_of_squared_norms"]) < 1e-8 for r in E2b)

# strong positivity on walk sets, on a graph whose walk gains realize the whole group: a non-positive-definite class function gives a negative measure
G = s3(); gain = random_gain_graph(5, 5, G)
for tries in range(200):
    W = walks(gain, 0, 6, G)
    by_end = {}
    for w in W: by_end.setdefault(w[0], set()).add(w[1])
    if any(len(v) == G.n for v in by_end.values()): break
    gain = random_gain_graph(5, 5, G)
y_full = [y for y, v in by_end.items() if len(v) == G.n][0]
reps = {}
for w in W:
    if w[0] == y_full: reps.setdefault(w[1], w)
atoms = [reps[g] for g in range(G.n)]
fbad = G.chars[0] - 0.8 * G.chars[2] / 2 + 0.5 * G.chars[1]     # coefficient of the two-dimensional character negative
M = np.array([[D([a], [b], fbad, G) for b in atoms] for a in atoms]); ev, evec = np.linalg.eigh((M + M.conj().T) / 2)
R["E2c_negative_measure"] = dict(min_eigenvalue_of_atom_matrix=float(ev.min()))
ok["E2c_non_positive_definite_weight_violates_strong_positivity"] = ev.min() < -1e-6

# ============ E3 order of interference ============
G = cyclic(4); gain = random_gain_graph(6, 5, G); W = [w for w in walks(gain, 0, 6, G) if w[0] == 0]
chi = G.chars[1]
amp = lambda S: sum(chi[w[1]] for w in S)
mu2 = lambda S: abs(amp(S)) ** 2; mu1 = lambda S: len(S); mu4 = lambda S: abs(amp(S)) ** 4
perm = rng.permutation(len(W)); parts = [[W[i] for i in perm[j::5]][:6] for j in range(5)]
def I(mu, sets):                 # Sorkin interference term of order len(sets)
    n = len(sets); tot = 0
    for r in range(1, n + 1):
        for c in itertools.combinations(range(n), r):
            S = [w for i in c for w in sets[i]]; tot += (-1) ** (n - r) * mu(S)
    return tot
first_draw = dict(part_amplitudes=[str(amp(p)) for p in parts], level4=[float(I(mu4, parts[:k])) for k in (2, 3, 4, 5)])
while min(abs(amp(p)) for p in parts) < 1e-9 or abs(I(mu4, parts[:4])) < 1e-9:      # redraw until every part has nonzero summed amplitude and I4 is not accidentally zero
    perm = rng.permutation(len(W)); parts = [[W[i] for i in perm[j::5]][:6] for j in range(5)]
E3 = dict(level1=[I(mu1, parts[:k]) for k in (2, 3)], level2=[float(I(mu2, parts[:k])) for k in (2, 3, 4)], level4=[float(I(mu4, parts[:k])) for k in (2, 3, 4, 5)],
          part_amplitudes=[str(amp(p)) for p in parts], retained_first_draw=first_draw)
R["E3_interference_orders"] = E3
ok["E3_counting_is_additive"] = E3["level1"] == [0, 0]
ok["E3_pair_measure_has_I2_nonzero_I3_zero"] = abs(E3["level2"][0]) > 1e-9 and abs(E3["level2"][1]) < 1e-9 and abs(E3["level2"][2]) < 1e-9
ok["E3_quartic_measure_has_I3_I4_nonzero_I5_zero"] = abs(E3["level4"][1]) > 1e-9 and abs(E3["level4"][2]) > 1e-9 and abs(E3["level4"][3]) < 1e-6

# ============ E4 composition: categorical product of gain graphs ============
G = cyclic(4)
g1 = random_gain_graph(4, 2, G); g2 = random_gain_graph(4, 3, G)
def adj(gain, nv, chi): 
    A = np.zeros((nv, nv), complex)
    for (a, b), g in gain.items(): A[b, a] = chi[g]            # A[end, start]
    return A
A1, A2 = adj(g1, 4, chi), adj(g2, 4, chi)
prod = {((a, u), (b, v)): int(G.mul[ga][gb]) for (a, b), ga in g1.items() for (u, v), gb in g2.items()}
vid = {(a, u): 4 * a + u for a in range(4) for u in range(4)}
A12 = np.zeros((16, 16), complex)
for (s, t), g in prod.items(): A12[vid[t], vid[s]] = chi[g]
k = 4
E4 = dict(adjacency_is_kronecker=float(np.abs(A12 - np.kron(A1, A2)).max()),
          amplitude_factorizes=float(np.abs(np.linalg.matrix_power(A12, k) - np.kron(np.linalg.matrix_power(A1, k), np.linalg.matrix_power(A2, k))).max()),
          hermitian=bool(np.allclose(A1, A1.conj().T)))
# a set of pairs of walks that is not a product set: its summed amplitude is not a product vector (Schmidt rank 2)
W1 = walks(g1, 0, k, G); W2 = walks(g2, 0, k, G)
ends1 = sorted(set(w[0] for w in W1)); ends2 = sorted(set(w[0] for w in W2))
a_, b_ = [w for w in W1 if w[0] == ends1[0]][0], [w for w in W1 if w[0] == ends1[-1]][0]
c_, d_ = [w for w in W2 if w[0] == ends2[0]][0], [w for w in W2 if w[0] == ends2[-1]][0]
vec = np.zeros((4, 4), complex)
for (w, v) in ((a_, c_), (b_, d_)): vec[w[0], v[0]] += chi[w[1]] * chi[v[1]]
E4["schmidt_rank_of_two_correlated_walk_pairs"] = int(np.linalg.matrix_rank(vec))
R["E4_composition"] = E4
ok["E4_product_graph_gives_tensor_product"] = E4["adjacency_is_kronecker"] < 1e-12 and E4["amplitude_factorizes"] < 1e-9
ok["E4_correlated_walk_sets_give_non_product_vectors"] = E4["schmidt_rank_of_two_correlated_walk_pairs"] == 2

# ============ E5 limits: walk length is not a unitary evolution ============
E5 = {}
sv = []
for _ in range(200):
    g = random_gain_graph(6, int(rng.integers(1, 8)), cyclic(4)); A = adj(g, 6, cyclic(4).chars[1]); s = np.linalg.svd(A, compute_uv=False); sv.append(s.min() / s.max())
E5["random_Z4_gain_graphs_min_over_max_singular_value"] = dict(max=float(max(sv)), median=float(np.median(sv)))
ok["E5_random_gain_graphs_are_not_proportional_to_unitaries"] = max(sv) < 0.999
hu = []
A = np.array([[0, 1], [1, 0]], float)
for n in range(1, 8):
    hu.append(float(np.abs(A @ A - n * np.eye(len(A))).max()))
    A = np.block([[A, np.eye(len(A))], [np.eye(len(A)), -A]])
E5["signed_hypercube_A2_minus_nI"] = hu
ok["E5_signed_hypercube_squares_to_n"] = max(hu) < 1e-12
g = random_gain_graph(6, 6, cyclic(4)); A = adj(g, 6, cyclic(4).chars[1]); ev, evec = np.linalg.eigh(A)
order = np.argsort(-np.abs(ev)); top = evec[:, order[0]]; gap = abs(ev[order[1]]) / abs(ev[order[0]])
lim = []
for k in (2, 6, 20, 60, 200):
    col = np.linalg.matrix_power(A, k)[:, 0]; p = np.abs(col) ** 2; p /= p.sum(); lim.append(dict(k=k, total_variation_to_top_eigenvector=float(0.5 * np.abs(p - np.abs(top) ** 2).sum())))
E5["long_walk_limit"] = dict(modulus_ratio_second_to_first=float(gap), rows=lim)
ok["E5_long_walks_tend_to_dominant_eigenvector"] = lim[-1]["total_variation_to_top_eigenvector"] < 1e-3 or gap > 0.999
R["E5_limits"] = E5

# ============ E6 dependence on the choice of primitive character ============
E6 = []
for n in (3, 4, 5, 6, 7, 8, 12):
    G = cyclic(n); gain = random_gain_graph(6, 6, G); W = walks(gain, 0, 6, G)
    ends = sorted(set(w[0] for w in W))
    N = {y: np.zeros(n, int) for y in ends}                      # integer counts of coterminous pairs by holonomy class
    for y in ends:
        gs = [w[1] for w in W if w[0] == y]
        for a in gs:
            for b in gs: N[y][G.mul[a][G.inv[b]]] += 1
    units = [j for j in range(1, n) if math.gcd(j, n) == 1]
    probs = []
    for j in units:
        mu = np.array([sum(N[y][k] * math.cos(2 * math.pi * j * k / n) for k in range(n)) for y in ends]); probs.append(mu / mu.sum())
    spread = float(max(np.abs(p - probs[0]).max() for p in probs))
    E6.append(dict(n=n, primitive_characters=len(units), max_difference_of_normalized_measures=spread))
R["E6_character_choice"] = E6
ok["E6_measure_independent_of_primitive_character_iff_n_in_3_4_6"] = all((r["max_difference_of_normalized_measures"] < 1e-12) == (r["n"] in (3, 4, 6)) for r in E6)

# ============ E7 trees and records: at most one walk between endpoints -> the pair measure is the count ============
G = cyclic(4); gain = random_gain_graph(5, 4, G); k = 5; W = walks(gain, 0, k, G); chi = G.chars[1]
# unfolding: each walk ends at a distinct vertex of the tree of walks, so no two distinct walks are coterminous there
mu_tree = sum(1 for w in W for w2 in W if w[2] == w2[2])                 # pairs coterminous in the unfolding = identical walks
ends = sorted(set(w[0] for w in W))
count = {y: sum(1 for w in W if w[0] == y) for y in ends}
quad = {y: float(abs(sum(chi[w[1]] for w in W if w[0] == y)) ** 2) for y in ends}
# record factor: walk in G paired with its own lift in the unfolding; marginal over the record of the pair measure equals the count
marg = {y: sum(1 for w in W for w2 in W if w[0] == y and w2[0] == y and w[2] == w2[2]) for y in ends}
R["E7_records"] = dict(walks=len(W), pair_measure_on_unfolding=int(mu_tree), counts_by_endpoint=count, pair_measure_by_endpoint_without_record=quad, with_record=marg)
ok["E7_recorded_walks_give_counting_measure"] = marg == count and mu_tree == len(W) and any(abs(quad[y] - count[y]) > 1e-9 for y in ends)

R["ok"] = ok
json.dump(R, open("Gain_Graph_Pair_Measures_Results.json", "w"), indent=1, default=str)
for k_, v_ in ok.items(): print(("PASS " if v_ else "FAIL ") + k_)
