#!/usr/bin/env python3
"""Tenth edition check.  Claim under test (fixed before the run).  Let C be a finite abelian group, D a gain digraph with gains in C in
which every vertex has d successors, and for a character chi of C let A_chi be the step matrix.  Put X(D) = {chi : A_chi* A_chi = d}.
A pair rule with real kernel f on C, f(-g) = f(g),
        mu_f(S) = sum over pairs (w, w') in S x S with a common end vertex of f(gain(w') - gain(w)),
is consistent under continuation with factor d if f is a real combination of the characters in X(D) (always), and only if it is one,
provided (H): for every two distinct vertices with a common successor, the quotients of the gains of walks of one common length to the
two vertices take every value of C.
Carriers: arc digraphs of random base digraphs on 1 or 2 nodes with d arcs out of and into every node; at a node the d x d block of gains
is rho_z + kappa_y + B[z][y] with rho, kappa random in C and B one of
 F1  d = 2, C = Z_q, q = 4, 6, 8, 12, B = [[0, 0], [0, q/2]]           (expected X: the characters j odd)
 F2  d = 2, C = Z_3 x Z_3 x Z_2, B = [[0, 0], [0, (0, 0, 1)]]          (expected X: the characters that are -1 on (0, 0, 1))
 F3  d = 3, C = Z_q, q = 3, 6, 9, 12, B[z][y] = (q/3) z y              (expected X: the characters j not divisible by 3)
 F4  d = 4, C = Z_8, B[z][y] = 2 z y                                   (expected X: the characters j odd)
Four carriers for each family and order (40 in all).  Events: 1200 random sets of walks of length 9 (d = 2), 6 (d = 3) or 5 (d = 4) from
arc 0; equations in integer arithmetic.
Predicates:
 G1  on every carrier the real part of every character in X(D) satisfies every equation (residual below 1e-9 of the largest coefficient);
 G2  on every carrier with (H), tested at the sampled length for the vertices reached, the solution space has dimension equal to the
     number of pairs {chi, conj chi} in X(D);
 G3  X(D), computed from the matrices A_chi, is the expected set on every carrier;
 G4  every family has at least three carriers with (H).
Recorded without a predicate: the solution dimension on carriers without (H).
Writes Kernel_Rules_General_Results.json; refuses to overwrite.  Seed fixed and reported."""
import itertools, json, math, os, sys
import numpy as np
OUT = "Kernel_Rules_General_Results.json"
if os.path.exists(OUT): sys.exit("refusing to overwrite " + OUT)
R = {}; ok = lambda name, val, **info: R.__setitem__(name, dict(passed=bool(val), **info))
SEED = 20261121; rng = np.random.default_rng(SEED)
class Group:
    def __init__(self, mods): self.mods = tuple(mods); self.elems = list(itertools.product(*[range(m) for m in mods])); self.index = {g: i for i, g in enumerate(self.elems)}; self.n = len(self.elems)
    def add(self, a, b): return tuple((x + y) % m for x, y, m in zip(a, b, self.mods))
    def neg(self, a): return tuple((-x) % m for x, m in zip(a, self.mods))
    def mul(self, k, a): return tuple((k * x) % m for x, m in zip(a, self.mods))
    def chi(self, j, g): return np.exp(2j * math.pi * sum(jj * gg / m for jj, gg, m in zip(j, g, self.mods)))
    def rand(self): return tuple(int(rng.integers(0, m)) for m in self.mods)
def carrier(G, d, B, n):
    perms = [rng.permutation(n) for _ in range(d)]; V = n * d; K = [[None] * V for _ in range(V)]          # K[b][a]: gain of arc a -> b
    for node in range(n):
        inc = [k * d + i for i in range(d) for k in range(n) if perms[i][k] == node]; out = [node * d + i for i in range(d)]
        rho = [G.rand() for _ in range(d)]; kap = [G.rand() for _ in range(d)]
        for z, b in enumerate(out):
            for y, a in enumerate(inc): K[b][a] = G.add(G.add(rho[z], kap[y]), B[z][y])
    return K
def chars_X(G, K, d):
    V = len(K); X = []
    for j in G.elems:
        A = np.zeros((V, V), dtype=complex)
        for b in range(V):
            for a in range(V):
                if K[b][a] is not None: A[b, a] = G.chi(j, K[b][a])
        if np.allclose(A.conj().T @ A, d * np.eye(V), atol=1e-9): X.append(j)
    return X
def walks(G, K, L):
    V = len(K); ws = [(0, G.elems[0])]
    for _ in range(L): ws = [(b, G.add(g, K[b][a])) for a, g in ws for b in range(V) if K[b][a] is not None]
    return ws
def hypothesis(G, K, ws):
    V = len(K); reach = {}
    for b, g in ws: reach.setdefault(b, set()).add(g)
    found = False
    for a in range(V):
        for a2 in range(a + 1, V):
            if any(K[b][a] is not None and K[b][a2] is not None for b in range(V)) and a in reach and a2 in reach:
                found = True
                if len({G.add(g2, G.neg(g1)) for g1 in reach[a] for g2 in reach[a2]}) < G.n: return False
    return found
def solve(G, K, d, ws, trials=1200):
    V = len(K); orbit = {}; reps = []
    for g in G.elems:
        key = min(g, G.neg(g))
        if key not in orbit: orbit[key] = len(reps); reps.append(key)
    col = [orbit[min(g, G.neg(g))] for g in G.elems]; rows = []
    def corr(n):                                       # c[g] = sum_y sum_a n[y, a] n[y, a + g]
        c = [0] * G.n
        for y in range(V):
            nz = [(i, int(n[y, i])) for i in range(G.n) if n[y, i]]
            for i, x in nz:
                for i2, x2 in nz: c[G.index[G.add(G.elems[i2], G.neg(G.elems[i]))]] += x * x2
        return c
    for _ in range(trials):
        pick = rng.random(len(ws)) < rng.uniform(0.01, 0.4); n = np.zeros((V, G.n), dtype=np.int64)
        for (b, g), p in zip(ws, pick):
            if p: n[b, G.index[g]] += 1
        if not n.any(): continue
        n2 = np.zeros_like(n)
        for a in range(V):
            for b in range(V):
                if K[b][a] is None: continue
                for i in np.nonzero(n[a])[0]: n2[b, G.index[G.add(G.elems[int(i)], K[b][a])]] += n[a, i]
        c1, c2 = corr(n), corr(n2); row = [0] * len(reps)
        for i in range(G.n): row[col[i]] += c2[i] - d * c1[i]
        rows.append(row)
    E = np.array(rows, dtype=float); _, s, vt = np.linalg.svd(E); rank = int(np.sum(s > 1e-9 * s[0])); scale = float(np.abs(E).max())
    return E, len(reps) - rank, scale, reps
def Bfam(G, fam, q):
    if fam == "F1": return [[(0,), (0,)], [(0,), (q // 2,)]]
    if fam == "F2": return [[(0, 0, 0), (0, 0, 0)], [(0, 0, 0), (0, 0, 1)]]
    if fam == "F3": return [[((q // 3) * z * y % q,) for y in range(3)] for z in range(3)]
    if fam == "F4": return [[(2 * z * y % 8,) for y in range(4)] for z in range(4)]
def expected(G, fam, q):
    if fam in ("F1", "F4"): return [j for j in G.elems if j[0] % 2 == 1]
    if fam == "F2": return [j for j in G.elems if j[2] == 1]
    if fam == "F3": return [j for j in G.elems if j[0] % 3 != 0]
rows = []; g1 = g2 = g3 = True; countH = {}
for fam, mods_list, d, L in (("F1", [(4,), (6,), (8,), (12,)], 2, 9), ("F2", [(3, 3, 2)], 2, 9), ("F3", [(3,), (6,), (9,), (12,)], 3, 6), ("F4", [(8,)], 4, 5)):
    for mods in mods_list:
        G = Group(mods); q = mods[0]
        for t in range(4):
            K = carrier(G, d, Bfam(G, fam, q), int(rng.integers(1, 3))); X = chars_X(G, K, d); ws = walks(G, K, L); H = hypothesis(G, K, ws); E, dim, scale, reps = solve(G, K, d, ws)
            res = max((float(np.abs(E @ np.array([G.chi(j, g).real for g in reps])).max()) / scale for j in X), default=0.0)
            classes = len({min(j, G.neg(j)) for j in X}); exp_ok = sorted(X) == sorted(expected(G, fam, q))
            g1 &= res < 1e-9; g3 &= exp_ok; countH[fam] = countH.get(fam, 0) + int(H)
            if H: g2 &= dim == classes
            rows.append(dict(family=fam, group=list(mods), degree=d, vertices=len(K), hypothesis=H, characters_in_X=len(X), classes_in_X=classes, X_as_expected=exp_ok, solution_dimension=dim, residual_of_X=res))
            print(rows[-1], flush=True)
ok("G1_characters_under_which_the_step_is_norm_preserving_are_consistent", g1)
ok("G2_with_the_hypothesis_no_other_kernel_is_consistent", g2)
ok("G3_X_is_the_expected_set", g3, rows=rows, seed=SEED)
ok("G4_at_least_three_carriers_with_the_hypothesis_in_each_family", all(v >= 3 for v in countH.values()), carriers_with_hypothesis=countH)
R["_summary"] = dict(predicates=4, passed=sum(1 for k, v in R.items() if not k.startswith("_") and v["passed"]), seed=SEED, numpy=np.__version__)
json.dump(R, open(OUT, "w"), indent=1, default=str)
for k, v in R.items():
    if not k.startswith("_"): print(("PASS " if v["passed"] else "FAIL ") + k)
print(R["_summary"])
