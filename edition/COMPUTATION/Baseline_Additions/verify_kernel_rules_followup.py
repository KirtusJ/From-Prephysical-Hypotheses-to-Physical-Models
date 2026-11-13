#!/usr/bin/env python3
"""Follow-up to verify_kernel_rules.py, three of whose four predicates failed and are kept.
Diagnosis.  K1 and K2 failed on 2 of 24 carriers (q = 8 and q = 12, solution dimensions 4 and 5): random carriers whose gains lie in a proper
subgroup, so that the hypothesis of the claim (the differences of the gains of walks to the two vertices of a block take every value of
the group) does not hold; the predicates did not test the hypothesis.  K3 failed through its threshold: the residuals of the even characters
were between 0.038 and 2.0 of the largest coefficient, against at most 7.5e-15 for the odd characters, and the threshold 0.1 had no basis.
Predicates fixed before this run (new seed; q = 4, 6, 8, 10, 12; 8 random carriers on 1 to 3 base nodes for each q; walks of length 9 from
arc 0; 1500 events each).  H(carrier): for some pair of vertices with common successors, the differences of the gains of the walks of
length 9 to the two vertices take every value of the group.
 K1b  on every carrier with H the solution space has dimension ceil(q/4) and every solution satisfies f(h - d) = -f(d) (defect below 1e-9);
 K1c  on every carrier without H the solution space has dimension above ceil(q/4), and at least one carrier of each kind occurs in the run;
 K3b  on every carrier, with or without H, the kernels of the odd characters leave a residual below 1e-9 of the largest coefficient, and on
      every carrier with H every even character leaves a residual above 1e-3: a separation of six orders (threshold chosen after seeing the
      first run).
Writes Kernel_Rules_Followup_Results.json; refuses to overwrite.  Seed fixed and reported."""
import json, math, os, sys
import numpy as np
OUT = "Kernel_Rules_Followup_Results.json"
if os.path.exists(OUT): sys.exit("refusing to overwrite " + OUT)
R = {}; ok = lambda name, val, **info: R.__setitem__(name, dict(passed=bool(val), **info))
SEED = 20261119; rng = np.random.default_rng(SEED)
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
def hypothesis(K, q, ws):
    V = K.shape[0]; reach = {}
    for b, g in ws: reach.setdefault(int(b), set()).add(g)
    for a in range(V):
        for a2 in range(a + 1, V):
            if np.array_equal(K[:, a] >= 0, K[:, a2] >= 0) and a in reach and a2 in reach:
                if len({(g2 - g1) % q for g1 in reach[a] for g2 in reach[a2]}) == q: return True
    return False
def corr(n, q): return np.array([int((n * np.roll(n, -d, axis=1)).sum()) for d in range(q)], dtype=object)
def equations(K, q, ws, trials=1500):
    V = K.shape[0]; h = q // 2; rows = []
    for _ in range(trials):
        pick = rng.random(len(ws)) < rng.uniform(0.01, 0.5); n = np.zeros((V, q), dtype=np.int64)
        for (b, g), p in zip(ws, pick):
            if p: n[b, g] += 1
        if not n.any(): continue
        n2 = np.zeros_like(n)
        for a in range(V):
            for b in np.nonzero(K[:, a] >= 0)[0]: n2[b] += np.roll(n[a], int(K[b, a]))
        e = corr(n2, q) - 2 * corr(n, q); row = [0] * (h + 1)
        for d in range(q): row[min(d, q - d)] += int(e[d])
        rows.append(row)
    return np.array(rows, dtype=float)
fold = lambda q, j: np.array([math.cos(2 * math.pi * j * d / q) for d in range(q // 2 + 1)])
rows = []
for q in (4, 6, 8, 10, 12):
    for t in range(8):
        K = random_base(int(rng.integers(1, 4)), q); ws = walks(K, q, 9); H = hypothesis(K, q, ws); E = equations(K, q, ws)
        _, s, vt = np.linalg.svd(E); rank = int(np.sum(s > 1e-9 * s[0])); null = vt[rank:]; scale = float(np.abs(E).max())
        rows.append(dict(q=q, arcs=int(K.shape[0]), hypothesis=H, solution_dimension=int(null.shape[0]), expected_with_hypothesis=math.ceil(q / 4),
                         oddness_defect=max((float(np.abs(v + v[::-1]).max()) for v in null), default=0.0),
                         residual_of_odd_characters=max(float(np.abs(E @ fold(q, j)).max()) / scale for j in range(1, q, 2)),
                         least_residual_of_even_characters=min(float(np.abs(E @ fold(q, j)).max()) / scale for j in range(0, q, 2))))
        print(rows[-1], flush=True)
withH = [r for r in rows if r["hypothesis"]]; without = [r for r in rows if not r["hypothesis"]]
ok("K1b_with_the_hypothesis_the_consistent_kernels_are_the_odd_ones", all(r["solution_dimension"] == r["expected_with_hypothesis"] and r["oddness_defect"] < 1e-9 for r in withH), carriers_with_hypothesis=len(withH))
ok("K1c_without_the_hypothesis_more_kernels_are_consistent", len(withH) > 0 and len(without) > 0 and all(r["solution_dimension"] > r["expected_with_hypothesis"] for r in without), carriers_without_hypothesis=len(without))
ok("K3b_odd_characters_in_even_characters_out", all(r["residual_of_odd_characters"] < 1e-9 for r in rows) and all(r["least_residual_of_even_characters"] > 1e-3 for r in withH), rows=rows, seed=SEED)
R["_summary"] = dict(predicates=3, passed=sum(1 for k, v in R.items() if not k.startswith("_") and v["passed"]), seed=SEED, numpy=np.__version__)
json.dump(R, open(OUT, "w"), indent=1, default=str)
for k, v in R.items():
    if not k.startswith("_"): print(("PASS " if v["passed"] else "FAIL ") + k)
print(R["_summary"])
