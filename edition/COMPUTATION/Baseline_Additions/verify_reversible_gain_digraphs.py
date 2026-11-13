#!/usr/bin/env python3
"""Checks for paper G9 (reversible steps on gain digraphs) and the constructed trial GH-2.
Writes Reversible_Gain_Digraphs_Results.json.  Numeric values are double precision, not enclosures.  Seeds are fixed and reported."""
import itertools, json, math
import numpy as np
from reversible_walk_lib import ring_step, polar_structure, dispersion
R = {}; ok = lambda name, val, **info: R.__setitem__(name, dict(passed=bool(val), **info))
SQ2 = math.sqrt(2)

# ---------------- R1: exhaustive search, out-degree 2, unit gains, A*A = 2
def search(n, gains):
    """count all n x n matrices with entries in gains or 0, exactly two nonzero entries per column and pairwise orthogonal columns,
    and count those that are block structured: columns fall into pairs with equal support {y,y'}, the supports partition the vertices,
    and every pair has zigzag gain a_yx conj(a_yx') a_y'x' conj(a_y'x) = -1"""
    opts = [(pair, g) for pair in itertools.combinations(range(n), 2) for g in itertools.product(gains, repeat=2)]
    m = len(opts)
    def inner(i, j):
        (p, g), (q, h) = opts[i], opts[j]; t = 0
        for a, ga in zip(p, g):
            for b, hb in zip(q, h):
                if a == b: t += np.conj(ga) * hb
        return t
    compat = [[abs(inner(i, j)) < 1e-12 for j in range(m)] for i in range(m)]
    def zig(i, j):
        (p, g), (q, h) = opts[i], opts[j]
        return p == q and abs(g[0] * np.conj(h[0]) * h[1] * np.conj(g[1]) + 1) < 1e-12
    count = 0; blocked = 0
    def structured(ch):
        cls = {}
        for i in ch: cls.setdefault(opts[i][0], []).append(i)
        if any(len(v) != 2 for v in cls.values()): return False
        if sorted(y for p in cls for y in p) != list(range(n)): return False
        return all(zig(v[0], v[1]) for v in cls.values())
    stack = [[i] for i in range(m)]
    while stack:
        ch = stack.pop()
        if len(ch) == n:
            count += 1; blocked += structured(ch); continue
        for j in range(m):
            if all(compat[i][j] for i in ch): stack.append(ch + [j])
    return count, blocked
tab = []
for n, gains, name in [(2, (1, -1), "Z2"), (3, (1, -1), "Z2"), (4, (1, -1), "Z2"), (5, (1, -1), "Z2"), (6, (1, -1), "Z2"), (4, (1, 1j, -1, -1j), "Z4"), (3, (1, 1j, -1, -1j), "Z4"),
                       (4, (1, np.exp(2j * math.pi / 3), np.exp(4j * math.pi / 3)), "Z3"), (6, (1, np.exp(2j * math.pi / 3), np.exp(4j * math.pi / 3)), "Z3")]:
    cnt_, blk_ = search(n, gains); tab.append(dict(vertices=n, gains=name, solutions=cnt_, all_block_structured=(cnt_ == blk_)))
ok("R1_degree_two_reversible_gain_digraphs_are_block_structured", all(r["all_block_structured"] for r in tab), table=tab,
   universe="all simple digraphs with loops allowed, out-degree 2 at every vertex, gains as listed; solutions are matrices with pairwise orthogonal columns")
ok("R1_none_on_odd_vertex_sets_and_none_without_minus_one", all(r["solutions"] == 0 for r in tab if r["vertices"] % 2 or r["gains"] == "Z3") and all(r["solutions"] > 0 for r in tab if r["vertices"] % 2 == 0 and r["gains"] != "Z3"))
# ---------------- R2: non-negative gains: norm-preserving 0/1 matrices are permutation matrices
cnt = 0; bad = 0
for n in (2, 3, 4):
    for bits in itertools.product((0, 1), repeat=n * n):
        A = np.array(bits).reshape(n, n); G = A.T @ A
        if G[0, 0] > 0 and np.array_equal(G, G[0, 0] * np.eye(n, dtype=int)):
            cnt += 1; bad += not (G[0, 0] == 1 and (A.sum(0) == 1).all() and (A.sum(1) == 1).all())
ok("R2_trivial_gains_reversible_means_permutation", bad == 0 and cnt == 2 + 6 + 24, matrices_found=cnt)
# ---------------- R3: polar complex structure of an orthogonal map
rng = np.random.default_rng(2026111233); rows = []
for n in (6, 7, 8, 9):
    Q, _ = np.linalg.qr(rng.normal(size=(n, n))); J, E1, C, K = polar_structure(Q)
    th = np.arccos(np.clip(np.linalg.eigvalsh(E1 @ C @ E1 + (np.eye(n) - E1) * 5), -1, 1)); th = th[np.isfinite(th)]
    w, V = np.linalg.eigh(C); Th = V @ np.diag(np.arccos(np.clip(w, -1, 1))) @ V.T
    # exp(J Theta) = cos Theta + J sin Theta on the complement; on ker K, U = C
    recon = V @ np.diag(np.clip(w, -1, 1)) @ V.T + J @ (V @ np.diag(np.sqrt(np.clip(1 - w * w, 0, None))) @ V.T)
    Jr, _, _, _ = polar_structure(Q.T)
    rows.append(dict(n=n, dim_kernel=int(round(n - np.trace(E1))), J2_plus_E1=float(np.abs(J @ J + E1).max()), commutes_with_U=float(np.abs(J @ Q - Q @ J).max()),
                     U_minus_cosTheta_plus_JsinTheta=float(np.abs(recon - Q).max()), reversal_J_plus_Jrev=float(np.abs(J + Jr).max())))
ok("R3_polar_structure_of_random_orthogonal_maps", all(max(r["J2_plus_E1"], r["commutes_with_U"], r["U_minus_cosTheta_plus_JsinTheta"], r["reversal_J_plus_Jrev"]) < 1e-9 for r in rows), rows=rows, seed=2026111233)
# uniqueness: reverse J on one spectral plane of U; the result is a complex structure commuting with U for which U = cos T' + J' sin T' needs sin T' < 0 there
th = 0.0
Q, _ = np.linalg.qr(rng.normal(size=(6, 6)))
if np.linalg.det(Q) < 0: Q[:, 0] = -Q[:, 0]                      # determinant +1: generically no eigenvalue +-1 in even dimension
J, E1, C, K = polar_structure(Q); assert round(6 - np.trace(E1)) == 0
w, V = np.linalg.eigh(C); plane = V[:, :2] @ V[:, :2].T          # eigenvalues of C come in equal pairs; the lowest pair spans a plane invariant under U
Jp = J - 2 * plane @ J @ plane; S = -Jp @ K                       # S would have to be sin(Theta') >= 0
ok("R3_other_commuting_structures_have_a_negative_generator", abs(w[0] - w[1]) < 1e-9 and np.abs(Jp @ Jp + np.eye(6)).max() < 1e-9 and np.abs(Jp @ Q - Q @ Jp).max() < 1e-9 and np.linalg.eigvalsh((S + S.T) / 2).min() < -1e-6,
   smallest_eigenvalue_of_minus_Jprime_K=float(np.linalg.eigvalsh((S + S.T) / 2).min()),
   first_run="the first version reversed J on the span of the two lowest eigenvectors of (U+U^T)/2 of a matrix that had eigenvalues +1 and -1; that span was not invariant and the predicate returned False (smallest eigenvalue -2.8e-16). Failure of the checking program; restated for a matrix of determinant +1, which has no eigenvalue +-1. A second version looped without end: the orthogonal factor returned by the QR routine for a 6 x 6 matrix always had determinant -1")
# cycles: the polar structure of the cyclic permutation is C (-C^2)^(-1/2) on the zero-sum space for odd n; for even n the alternating vector is in the kernel
rows = []
for n in range(3, 11):
    P = np.zeros((n, n)); [P.__setitem__(((i + 1) % n, i), 1) for i in range(n)]
    J, E1, C, K = polar_structure(P); rows.append(dict(n=n, dim_kernel=int(round(n - np.trace(E1)))))
ok("R3_cycle_kernel_dimension_1_odd_2_even", all(r["dim_kernel"] == (1 if r["n"] % 2 else 2) for r in rows), rows=rows)
# ---------------- R4: the signed arc digraph of a ring; walk sums
N = 9; A = ring_step(N); U = A / SQ2
ok("R4_ring_step_norm_preserving", np.abs(A.T @ A - 2 * np.eye(2 * N)).max() < 1e-12)
# explicit enumeration of walks of length k from arc 0
def walks(A, start, k):
    n = A.shape[0]; nxt = [np.nonzero(A[:, v])[0] for v in range(n)]
    out = [(start, 1.0)]
    for _ in range(k): out = [(y, g * A[y, v]) for v, g in out for y in nxt[v]]
    return out
k = 10; W = walks(A, 0, k); v = np.zeros(2 * N); cntv = np.zeros(2 * N)
for y, g in W: v[y] += g; cntv[y] += 1
ok("R4_walk_sum_equals_matrix_power", np.abs(v - np.linalg.matrix_power(A, k)[:, 0]).max() < 1e-9, walks=len(W))
ok("R4_total_pair_measure_is_2^k", abs((v ** 2).sum() - 2 ** k) < 1e-6, total=float((v ** 2).sum()), counting_total=float(cntv.sum()),
   note="pair measure of all walks of length k by end vertex sums to 2^k, as does the number of walks; the two distributions differ")
ok("R4_pair_measure_differs_from_counting", np.abs(v ** 2 / 2 ** k - cntv / 2 ** k).max() > 0.01, largest_difference=float(np.abs(v ** 2 / 2 ** k - cntv / 2 ** k).max()))
# two switching classes of signings: minus on a straight continuation, minus on a turn
A2 = ring_step(N, block=((1, -1), (1, 1)))
bounce = lambda A: A[2 * ((0 - 1) % N) + 1, 0] * A[0, 2 * ((0 - 1) % N) + 1]      # R at site 0 -> L at site -1 -> R at site 0
ev1 = np.sort(np.angle(np.linalg.eigvals(A / SQ2))); ev2 = np.sort(np.angle(np.linalg.eigvals(A2 / SQ2)))
ok("R4_two_classes_of_block_signings", bounce(A) == 1 and bounce(A2) == -1 and np.abs(A2.T @ A2 - 2 * np.eye(2 * N)).max() < 1e-12,
   bounce_gain=[float(bounce(A)), float(bounce(A2))], eigenphases_class1=[round(float(a), 6) for a in ev1], eigenphases_class2=[round(float(a), 6) for a in ev2],
   note="closed walk of length 2 has gain +1 in the first signing and -1 in the second, so they are not switching equivalent")
# ---------------- R5: the polar structure against the records
rows = []
for N in (5, 6, 7, 8):
    A = ring_step(N); U = A / SQ2; n = 2 * N; J, E1, C, K = polar_structure(U)
    Pv = np.zeros((n, n)); Pv[0, 0] = 1                              # record: one vertex of the digraph (one arc)
    Ps = np.zeros((n, n)); Ps[0, 0] = Ps[1, 1] = 1                   # record: one site
    # commutant of U and all vertex projections / all site projections
    def commutant_dim(gens):
        basis = np.eye(n * n).reshape(n * n, n, n)
        M = np.concatenate([np.array([(B @ g - g @ B).ravel() for B in basis]).T for g in gens])
        sv = np.linalg.svd(M, compute_uv=False); return int((sv < 1e-9).sum())
    vproj = [np.diag(np.eye(n)[i]) for i in range(n)]; sproj = [np.diag(np.eye(n)[2 * x] + np.eye(n)[2 * x + 1]) for x in range(N)]
    rows.append(dict(sites=N, dim_kernel=int(round(n - np.trace(E1))), comm_J_vertex_projection=float(np.linalg.norm(J @ Pv - Pv @ J, 2)), comm_J_site_projection=float(np.linalg.norm(J @ Ps - Ps @ J, 2)),
                     commutant_dim_step_and_vertex_records=commutant_dim([U] + vproj), commutant_dim_step_and_site_records=commutant_dim([U] + sproj)))
ok("R5_polar_structure_does_not_commute_with_records", all(r["comm_J_vertex_projection"] > 0.1 and r["comm_J_site_projection"] > 0.1 for r in rows), rows=rows)
ok("R5_commutant_of_step_and_records_is_real_scalars", all(r["commutant_dim_step_and_vertex_records"] == 1 and r["commutant_dim_step_and_site_records"] == 1 for r in rows),
   note="no real-linear complex structure commutes with the step and with the record projections")
# ---------------- R9: velocity as derivative of the eigenphase with respect to the holonomy round the ring
N = 12; h = 1e-5; rows = []
for theta in (0.3, 0.7, 1.9):
    e0 = np.linalg.eigvals(ring_step(N, twist=theta) / SQ2); e1 = np.linalg.eigvals(ring_step(N, twist=theta + h) / SQ2)
    w0 = -np.angle(e0); err = 0.0
    for lam in e0:
        lam1 = e1[np.argmin(np.abs(e1 - lam))]; dw = (-np.angle(lam1) + np.angle(lam)) / h
        # the eigenvalue is exp(-i w(k)) on one of two branches with k = k_j -+ theta/N ; velocity magnitude |cos k|/sqrt(1+cos^2 k)
        s2 = (math.sin(-np.angle(lam)) * SQ2) ** 2; cosk2 = max(0.0, 1 - min(1.0, s2)); vmag = math.sqrt(cosk2 / (1 + cosk2))
        err = max(err, abs(abs(N * dw) - vmag))
    rows.append(dict(theta=theta, largest_error=err))
ok("R9_velocity_is_N_times_d_eigenphase_d_holonomy", all(r["largest_error"] < 1e-3 for r in rows), rows=rows, sites=N,
   first_run="a first version included twist 0, where eigenvalues are degenerate and the finite-difference matching of eigenvalues failed (error 7.5e6); twist 0.7 gave 4.2e-7. Generic twists are used")
# ---------------- R10: signed hypercubes: parallel classes, anticommutation, type
sx = np.array([[0., 1.], [1., 0.]]); sz = np.diag([1., -1.]); I2 = np.eye(2)
def kron(*m):
    out = np.array([[1.0]])
    for a in m: out = np.kron(out, a)
    return out
rows = []
for k in range(1, 8):
    gam = [kron(*([sz] * i + [sx] + [I2] * (k - 1 - i))) for i in range(k)]
    signedperm = all((np.abs(g).sum(0) == 1).all() and (np.abs(g).sum(1) == 1).all() and np.array_equal(g, g.T) for g in gam)
    Aq = sum(gam); hyper = np.array_equal(np.abs(Aq), sum(kron(*([I2] * i + [sx] + [I2] * (k - 1 - i))) for i in range(k)))
    anti = all(np.abs(gam[i] @ gam[j] + gam[j] @ gam[i]).max() == 0 for i in range(k) for j in range(i))
    om = np.eye(2 ** k)
    for g in gam: om = om @ g
    central = all(np.abs(om @ g - g @ om).max() == 0 for g in gam)
    rows.append(dict(k=k, signed_matchings=bool(signedperm), support_is_hypercube=bool(hyper), anticommute=bool(anti), A2_is_k=bool(np.array_equal(Aq @ Aq, k * np.eye(2 ** k))),
                     volume_element_central=bool(central), volume_element_square=int(round((om @ om)[0, 0]))))
ok("R10_signed_hypercube_Clifford_relations", all(r["signed_matchings"] and r["support_is_hypercube"] and r["anticommute"] and r["A2_is_k"] for r in rows), rows=rows)
ok("R10_central_complex_structure_iff_k_is_3_mod_4", all((r["volume_element_central"] and r["volume_element_square"] == -1) == (r["k"] % 4 == 3) for r in rows))
# k = 3: algebra generated has dimension 8 and centre spanned by 1 and J; reversing the order of two classes reverses J
gam = [kron(*([sz] * i + [sx] + [I2] * (2 - i))) for i in range(3)]
prods = [np.eye(8)] + gam + [gam[0] @ gam[1], gam[0] @ gam[2], gam[1] @ gam[2], gam[0] @ gam[1] @ gam[2]]
dimalg = np.linalg.matrix_rank(np.array([p.ravel() for p in prods])); J3 = gam[0] @ gam[1] @ gam[2]
cen = [p for p in prods if all(np.abs(p @ g - g @ p).max() == 0 for g in gam)]
ok("R10_cube_algebra_is_eight_dimensional_with_centre_1_and_J", dimalg == 8 and len(cen) == 2 and np.array_equal(J3 @ J3, -np.eye(8)) and np.array_equal(gam[1] @ gam[0] @ gam[2], -J3))
# all-negative-squares signatures of the cube: one switching class
verts = list(itertools.product((0, 1), repeat=3)); edges = [(u, v) for u in verts for v in verts if u < v and sum(a != b for a, b in zip(u, v)) == 1]
faces = []
for i, j in ((0, 1), (0, 2), (1, 2)):
    l = 3 - i - j
    for c in (0, 1):
        vs = [v for v in verts if v[l] == c]; faces.append([e for e in edges if e[0] in vs and e[1] in vs])
count = 0
for signs in itertools.product((1, -1), repeat=12):
    sg = dict(zip(edges, signs))
    if all(np.prod([sg[e] for e in f]) == -1 for f in faces): count += 1
ok("R10_cube_signings_with_all_faces_negative_form_one_switching_class", count == 2 ** 7, signings=count, switching_orbit_size=2 ** 7)
# ladder transport on a rectagraph that is a Cayley graph of Z_2^m: folded 5-cube
def cayley(m, gens):
    vs = list(itertools.product((0, 1), repeat=m)); add = lambda a, b: tuple((x + y) % 2 for x, y in zip(a, b))
    return vs, {v: [add(v, g) for g in gens] for v in vs}
def rectagraph(vs, nb):
    for u in vs:
        for v in vs:
            if u < v:
                c = len(set(nb[u]) & set(nb[v]))
                if v in nb[u] and c != 0: return False
                if v not in nb[u] and c not in (0, 2): return False
    return True
def ladder_holonomy_trivial(vs, nb):
    """transport a neighbour c of a along the edge ab to the other common neighbour of b and c (and b itself to a);
    trivial holonomy is tested by transporting a labelling of the edges at a base vertex along a spanning tree and checking every edge"""
    base = vs[0]; lab = {base: {c: i for i, c in enumerate(nb[base])}}; stack = [base]
    def tr(a, b, c): return a if c == b else [d for d in nb[b] if d in nb[c] and d != a][0]
    while stack:
        a = stack.pop()
        for b in nb[a]:
            new = {tr(a, b, c): i for c, i in lab[a].items()}
            if b not in lab: lab[b] = new; stack.append(b)
            elif lab[b] != new: return False
    return True
g5 = [tuple(1 if i == j else 0 for i in range(4)) for j in range(4)] + [(1, 1, 1, 1)]
vsC, nbC = cayley(4, g5); vs4, nb4 = cayley(4, g5[:4])
ok("R10_ladder_transport_trivial_on_cube_and_folded_cube", rectagraph(vsC, nbC) and rectagraph(vs4, nb4) and ladder_holonomy_trivial(vsC, nbC) and ladder_holonomy_trivial(vs4, nb4),
   graphs=["4-cube", "folded 5-cube (16 vertices, valency 5)"])
# a rectagraph that is not a Cayley graph of an elementary abelian 2-group: incidence graph of the biplane with 7 points and blocks of size 4
fano = [{0, 1, 3}, {1, 2, 4}, {2, 3, 5}, {3, 4, 6}, {4, 5, 0}, {5, 6, 1}, {6, 0, 2}]; blocks = [set(range(7)) - f for f in fano]
vsB = [("p", i) for i in range(7)] + [("b", j) for j in range(7)]
nbB = {v: [] for v in vsB}
for j, bl in enumerate(blocks):
    for i in bl: nbB[("p", i)].append(("b", j)); nbB[("b", j)].append(("p", i))
def ladder_group(vs, nb):
    """group of permutations of the neighbours of the base vertex generated by ladder transport round the fundamental cycles of a spanning tree"""
    base = vs[0]; ident = {c: c for c in nb[base]}; frame = {base: ident}; stack = [base]; gens = set()
    def tr(a, b, c): return a if c == b else [d for d in nb[b] if d in nb[c] and d != a][0]
    order = []
    while stack:
        a = stack.pop()
        for b in nb[a]:
            new = {c0: tr(a, b, c) for c0, c in frame[a].items()}        # image at b of each neighbour c0 of the base
            if b not in frame: frame[b] = new; stack.append(b)
            else:
                inv = {v: k for k, v in frame[b].items()}; gens.add(tuple(inv[new[c0]] for c0 in nb[base]))
    idx = {c: i for i, c in enumerate(nb[base])}; gens = {tuple(idx[x] for x in g) for g in gens}
    G = {tuple(range(len(nb[base])))}
    while True:
        G2 = G | {tuple(g[h[i]] for i in range(len(h))) for g in G for h in gens}
        if G2 == G: return G
        G = G2
LG = ladder_group(vsB, nbB)
ok("R10_biplane_incidence_graph_is_a_rectagraph_with_nontrivial_ladder_holonomy", rectagraph(vsB, nbB) and len(LG) > 1 and len(ladder_group(vsC, nbC)) == 1 and len(ladder_group(vs4, nb4)) == 1,
   vertices=len(vsB), valency=4, order_of_ladder_holonomy_group=len(LG), note="14 vertices: not a power of two, so not a Cayley graph of an elementary abelian 2-group")
# does the folded 5-cube admit a signing with every square negative?  linear system over GF(2)
E = sorted({tuple(sorted((u, v))) for u in vsC for v in nbC[u]}); eidx = {e: i for i, e in enumerate(E)}
sq = set()
for a in vsC:
    for b, c in itertools.combinations(nbC[a], 2):
        d = [x for x in nbC[b] if x in nbC[c] and x != a][0]; sq.add(tuple(sorted([eidx[tuple(sorted(p))] for p in ((a, b), (b, d), (d, c), (c, a))])))
Mx = np.zeros((len(sq), len(E) + 1), dtype=np.uint8)
for r, s4 in enumerate(sorted(sq)):
    for e in s4: Mx[r, e] = 1
    Mx[r, -1] = 1
def gf2_consistent(M):
    M = M.copy(); r = 0
    for c in range(M.shape[1] - 1):
        piv = [i for i in range(r, M.shape[0]) if M[i, c]]
        if not piv: continue
        M[[r, piv[0]]] = M[[piv[0], r]]
        for i in range(M.shape[0]):
            if i != r and M[i, c]: M[i] ^= M[r]
        r += 1
    return not any(M[i, -1] and not M[i, :-1].any() for i in range(M.shape[0])), r
cons, rank = gf2_consistent(Mx)
ok("R10_folded_5_cube_all_squares_negative_recorded", True, edges=len(E), squares=len(sq), system_consistent=bool(cons), rank=int(rank),
   note="recorded, not a predicate: whether a signing with every 4-cycle negative exists on the folded 5-cube")
R["_summary"] = dict(predicates=sum(1 for k in R if not k.startswith("_")), passed=sum(1 for k, v in R.items() if not k.startswith("_") and v["passed"]), seeds=[2026111233])
json.dump(R, open("Reversible_Gain_Digraphs_Results.json", "w"), indent=1, default=str)
for k, v in R.items():
    if not k.startswith("_"): print(("PASS " if v["passed"] else "FAIL ") + k)
print(R["_summary"])
