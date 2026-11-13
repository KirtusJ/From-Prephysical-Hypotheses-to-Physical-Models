#!/usr/bin/env python3
"""Ninth edition check.  Claim under test (fixed before the run).  Let q be even, h = q/2, C the cyclic group of order q written
additively, and D a gain digraph with gains in C that is norm-preserving of degree two in a faithful character.  A pair rule with kernel f
(a real function on C with f(-d) = f(d)) assigns to a set S of walks of one length from one vertex
        mu_f(S) = sum over pairs (w, w') in S x S with a common end vertex of f(gain(w') - gain(w)).
Claim: mu_f is consistent under continuation (with factor 2) exactly when f(d + h) = -f(d) for all d: the kernel changes sign under the
central element.  The consistent kernels form a space of dimension ceil(q/4), spanned by the kernels cos(2 pi j d/q) of the characters with
j odd; it contains the kernel of the lift rule (1 at 0, -1 at h, 0 elsewhere) and no kernel of a character with j even.
Predicates (q = 2, 4, 6, 8, 10, 12; for each q the digraph B_q and 3 random carriers on 1 to 3 base nodes; 1500 events of walks of length 9,
integer arithmetic for the equations):
 K1  the solution space of the consistency equations in the unknowns f(0), ..., f(h) has dimension ceil(q/4) for all 24 carriers;
 K2  every solution satisfies f(h - d) = -f(d) (largest defect below 1e-9 for a basis of unit vectors);
 K3  the kernels of the odd characters and of the lift rule satisfy the equations exactly (integer residual 0 after scaling for the lift
     rule; below 1e-9 relative for the characters), and the kernel of every even character, the constant kernel among them, leaves a
     residual above 0.1 relative on every carrier;
 K4  for B_q and each q: at some length up to 40 the differences of the gains of walks to the two vertices of the block take every value.
Writes Kernel_Rules_Results.json; refuses to overwrite.  Seed fixed and reported."""
import json, math, os, sys
import numpy as np
OUT = "Kernel_Rules_Results.json"
if os.path.exists(OUT): sys.exit("refusing to overwrite " + OUT)
R = {}; ok = lambda name, val, **info: R.__setitem__(name, dict(passed=bool(val), **info))
SEED = 20261118; rng = np.random.default_rng(SEED)
def base_Bq(q): h = q // 2; return np.array([[0, 1 % q], [0, (1 + h) % q]])
def random_base(n, q):
    h = q // 2
    while True:
        p1, p2 = rng.permutation(n), rng.permutation(n)
        head = {2 * k: int(p1[k]) for k in range(n)}; head.update({2 * k + 1: int(p2[k]) for k in range(n)})
        K = -np.ones((2 * n, 2 * n), dtype=int)
        for node in range(n):
            inc = [a for a in range(2 * n) if head[a] == node]; out = [2 * node, 2 * node + 1]
            k0, k1, k2 = (int(t) for t in rng.integers(0, q, 3)); blk = [[k0, k1], [k2, (k2 + k1 - k0 + h) % q]]
            for i, b in enumerate(out):
                for j, a in enumerate(inc): K[b, a] = blk[i][j]
        reach = np.linalg.matrix_power((K >= 0).astype(float) + np.eye(2 * n), 2 * n)
        if np.all(reach > 0): return K
def walks(K, q, L):
    ws = [(0, 0)]
    for _ in range(L): ws = [(b, (g + int(K[b, a])) % q) for a, g in ws for b in np.nonzero(K[:, a] >= 0)[0]]
    return ws
def corr(n, q):                                   # sum over vertices of the autocorrelation of the integer vector n[y, :]
    return np.array([int((n * np.roll(n, -d, axis=1)).sum()) for d in range(q)], dtype=object)
def equations(K, q, L=9, trials=1500):
    ws = walks(K, q, L); V = K.shape[0]; h = q // 2; rows = []
    for _ in range(trials):
        pick = rng.random(len(ws)) < rng.uniform(0.01, 0.5); n = np.zeros((V, q), dtype=np.int64)
        for (b, g), p in zip(ws, pick):
            if p: n[b, g] += 1
        if not n.any(): continue
        n2 = np.zeros_like(n)
        for a in range(V):
            for b in np.nonzero(K[:, a] >= 0)[0]: n2[b] += np.roll(n[a], int(K[b, a]))
        e = corr(n2, q) - 2 * corr(n, q); row = [0] * (h + 1)                 # fold f(d) = f(-d)
        for d in range(q): row[min(d, q - d)] += int(e[d])
        rows.append(row)
    return np.array(rows, dtype=object)
def fold(fun, q): return np.array([fun(d) for d in range(q // 2 + 1)], dtype=float)
rows = []; g1 = g2 = g3 = True
for q in (2, 4, 6, 8, 10, 12):
    h = q // 2
    for t in range(4):
        K = base_Bq(q) if t == 0 else random_base(int(rng.integers(1, 4)), q); E = equations(K, q); Ef = E.astype(float)
        _, s, vt = np.linalg.svd(Ef); rank = int(np.sum(s > 1e-9 * s[0])); null = vt[rank:]; dim = null.shape[0]
        odd_defect = max((float(np.abs(v + v[::-1]).max()) for v in null), default=0.0)                    # f(h - d) = -f(d)
        scale = float(np.abs(Ef).max())
        chars_odd = max(float(np.abs(Ef @ fold(lambda d, j=j: math.cos(2 * math.pi * j * d / q), q)).max()) / scale for j in range(1, q, 2))
        lift = [0] * (h + 1); lift[0] = 1; lift[h] = -1; lift_res = int(max(abs(int(sum(int(a) * b for a, b in zip(r, lift)))) for r in E))
        chars_even = min(float(np.abs(Ef @ fold(lambda d, j=j: math.cos(2 * math.pi * j * d / q), q)).max()) / scale for j in range(0, q, 2))
        rows.append(dict(q=q, carrier="B_q" if t == 0 else "random", arcs=int(K.shape[0]), equations=int(E.shape[0]), solution_dimension=dim, expected=math.ceil(q / 4),
                         oddness_defect=odd_defect, residual_of_odd_characters=chars_odd, integer_residual_of_lift_kernel=lift_res, least_residual_of_even_characters=chars_even))
        g1 &= dim == math.ceil(q / 4); g2 &= odd_defect < 1e-9; g3 &= chars_odd < 1e-9 and lift_res == 0 and chars_even > 0.1; print(rows[-1], flush=True)
ok("K1_dimension_of_consistent_kernels", g1)
ok("K2_consistent_kernels_change_sign_under_the_central_element", g2)
ok("K3_odd_characters_and_lift_kernel_in_even_characters_out", g3, rows=rows, seed=SEED)
rowsH = []
for q in (2, 4, 6, 8, 10, 12):
    K = base_Bq(q); found = None; cur = {(0, 0)}                              # reachable (vertex, gain) sets by length
    for L in range(1, 41):
        cur = {(b, (g + int(K[b, a])) % q) for a, g in cur for b in (0, 1)}
        d = {(g2_ - g1_) % q for b1, g1_ in cur if b1 == 0 for b2, g2_ in cur if b2 == 1}
        if len(d) == q: found = L; break
    rowsH.append(dict(q=q, length_at_which_differences_cover_the_group=found))
ok("K4_differences_of_gains_cover_the_group", all(r["length_at_which_differences_cover_the_group"] is not None for r in rowsH), rows=rowsH)
R["_summary"] = dict(predicates=sum(1 for k in R if not k.startswith("_")), passed=sum(1 for k, v in R.items() if not k.startswith("_") and v["passed"]), seed=SEED, numpy=np.__version__)
json.dump(R, open(OUT, "w"), indent=1, default=str)
for k, v in R.items():
    if not k.startswith("_"): print(("PASS " if v["passed"] else "FAIL ") + k)
print(R["_summary"])
