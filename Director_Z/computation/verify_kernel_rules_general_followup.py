#!/usr/bin/env python3
"""Follow-up to verify_kernel_rules_general.py, whose predicate G4 failed and is kept: of the four carriers of the family F2 (degree two,
gains in Z_3 x Z_3 x Z_2, two registers and a sign) only two satisfied the hypothesis (H), and the predicate had asked for three in every
family.  The other three predicates were met.  This run adds twelve carriers of the family F2 on a new seed, with the same definitions.
Predicates fixed before the run:
 G2b  at least six of the twelve carriers satisfy (H), and on each of them the solution space has dimension 5, the number of pairs
      {chi, conj chi} among the nine characters that are -1 on the sign;
 G1b  on all twelve carriers X(D) is that set of nine characters and each of their real parts satisfies every equation (residual below
      1e-9 of the largest coefficient);
 G5   on every carrier without (H) the solution space has dimension above 5.
Writes Kernel_Rules_General_Followup_Results.json; refuses to overwrite.  Seed fixed and reported."""
import itertools, json, math, os, sys
import numpy as np
OUT = "Kernel_Rules_General_Followup_Results.json"
if os.path.exists(OUT): sys.exit("refusing to overwrite " + OUT)
R = {}; ok = lambda name, val, **info: R.__setitem__(name, dict(passed=bool(val), **info))
SEED = 20261122; rng = np.random.default_rng(SEED)
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
G = Group((3, 3, 2)); rows = []
for t in range(12):
    K = carrier(G, 2, Bfam(G, "F2", 3), int(rng.integers(1, 3))); X = chars_X(G, K, 2); ws = walks(G, K, 9); H = hypothesis(G, K, ws); E, dim, scale, reps = solve(G, K, 2, ws)
    res = max(float(np.abs(E @ np.array([G.chi(j, g).real for g in reps])).max()) / scale for j in X)
    rows.append(dict(vertices=len(K), hypothesis=H, X_as_expected=sorted(X) == sorted(expected(G, "F2", 3)), solution_dimension=dim, residual_of_X=res)); print(rows[-1], flush=True)
withH = [r for r in rows if r["hypothesis"]]; without = [r for r in rows if not r["hypothesis"]]
ok("G2b_two_registers_with_the_hypothesis", len(withH) >= 6 and all(r["solution_dimension"] == 5 for r in withH), carriers_with_hypothesis=len(withH))
ok("G1b_two_registers_sufficiency", all(r["X_as_expected"] and r["residual_of_X"] < 1e-9 for r in rows), rows=rows, seed=SEED)
ok("G5_without_the_hypothesis_more_kernels", all(r["solution_dimension"] > 5 for r in without), carriers_without_hypothesis=len(without))
R["_summary"] = dict(predicates=3, passed=sum(1 for k, v in R.items() if not k.startswith("_") and v["passed"]), seed=SEED, numpy=np.__version__)
json.dump(R, open(OUT, "w"), indent=1, default=str)
for k, v in R.items():
    if not k.startswith("_"): print(("PASS " if v["passed"] else "FAIL ") + k)
print(R["_summary"])
