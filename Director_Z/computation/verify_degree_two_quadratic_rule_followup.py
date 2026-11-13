#!/usr/bin/env python3
"""Follow-up to verify_degree_two_quadratic_rule.py, whose predicate Q1 failed on 2 of 40 carriers (solution space of dimension two) and is kept.
Diagnosis (run separately, seed 7): on carriers with 5 or 6 base nodes and walks of length 10 a modulus occurred only in events in which its
terms cancel, leaving an unknown without an equation; with walks of length 16 the solution space was one-dimensional and quadratic in the four
cases examined.  This is the defect of the first M1 program again, not a counterexample.  Predicates fixed before this run:
 Q1b  40 new random signed carriers on 1 to 6 base nodes, walks of length 16, 6000 sampled events, unknowns restricted to the moduli that
      occur in at least one equation with a nonzero coefficient: the solution space is one-dimensional and spanned by n^2 for every carrier;
 Q4b  the same for 10 carriers with gains of order four.
Writes Degree_Two_Quadratic_Rule_Followup_Results.json; refuses to overwrite.  Seed fixed and reported."""
import json, os, sys
import numpy as np
OUT = "Degree_Two_Quadratic_Rule_Followup_Results.json"
if os.path.exists(OUT): sys.exit("refusing to overwrite " + OUT)
R = {}; ok = lambda name, val, **info: R.__setitem__(name, dict(passed=bool(val), **info))
SEED = 20261114; rng = np.random.default_rng(SEED)
def carrier(n, units):
    """Arc digraph of the base digraph with arcs k -> p1[k] (arc 2k) and k -> p2[k] (arc 2k+1); A[b, a] != 0 iff arc a ends where arc b begins.
    At each node the 2x2 block (two incoming arcs x two outgoing arcs) is a random unitary-up-to-sqrt2 matrix with entries in `units`."""
    while True:
        p1, p2 = rng.permutation(n), rng.permutation(n)
        head = {2 * k: int(p1[k]) for k in range(n)}; head.update({2 * k + 1: int(p2[k]) for k in range(n)})
        A = np.zeros((2 * n, 2 * n), dtype=complex)
        for node in range(n):
            inc = [a for a in range(2 * n) if head[a] == node]; out = [2 * node, 2 * node + 1]
            u = [units[i] for i in rng.integers(0, len(units), 3)]
            blk = np.array([[u[0], u[1]], [u[2], -u[2] * u[1] / u[0]]])              # columns orthogonal: conj(u0) u1 + conj(u2) u3 = 0
            for i, b in enumerate(out):
                for j, a in enumerate(inc): A[b, a] = blk[i, j]
        if not np.allclose(A.conj().T @ A, 2 * np.eye(2 * n)): continue
        reach = np.linalg.matrix_power((np.abs(A) > 0).astype(float) + np.eye(2 * n), 2 * n)
        if np.all(reach > 0): return A
def walk_tables(A, start, j):
    """dict vertex -> list of gains (complex) of the walks of length j from start, capped at 6 walks per vertex and gain value"""
    V = A.shape[0]; cur = {start: [1 + 0j]}
    for _ in range(j):
        nxt = {}
        for x, gs in cur.items():
            for y in np.nonzero(A[:, x])[0]:
                nxt.setdefault(int(y), []).extend(g * A[y, x] for g in gs)
        cur = {}
        for y, gs in nxt.items():
            keep = []; cnt = {}
            for g in gs:
                key = (round(g.real), round(g.imag)); cnt[key] = cnt.get(key, 0) + 1
                if cnt[key] <= 6: keep.append(complex(*key))
            cur[y] = keep
    return cur
def equations(A, trials=1500, j=10):
    tab = walk_tables(A, 0, j); verts = sorted(tab); raw = []
    for _ in range(trials):
        v = np.zeros(A.shape[0], dtype=complex)
        for x in rng.choice(verts, size=min(len(verts), int(rng.integers(1, 3))), replace=False):
            gs = tab[int(x)]; pick = rng.random(len(gs)) < 0.5; v[int(x)] = sum(g for g, p in zip(gs, pick) if p)
        if not np.any(v): continue
        e = A @ v; raw.append((np.round(np.abs(e) ** 2).astype(int), np.round(np.abs(v) ** 2).astype(int)))   # squared moduli are integers
    keys = sorted({int(m) for e, a in raw for m in list(e) + list(a) if m > 0}); idx = {m: i for i, m in enumerate(keys)}
    M = np.zeros((len(raw), len(keys)))
    for r, (e, a) in enumerate(raw):
        for m in e:
            if m > 0: M[r, idx[int(m)]] += 1
        for m in a:
            if m > 0: M[r, idx[int(m)]] -= 2
    return M, keys
def one_dim_quadratic(M, keys):
    _, s, vt = np.linalg.svd(M); rank = int(np.sum(s > 1e-9)); null = vt[rank:]
    sq = np.array(keys, dtype=float); sq /= np.linalg.norm(sq)                      # phi as a function of the squared modulus: quadratic rule = identity
    return null.shape[0] == 1 and min(np.linalg.norm(null[0] - sq), np.linalg.norm(null[0] + sq)) < 1e-8, null.shape[0], len(keys)

def solve(A, trials, j):
    M, keys = equations(A, trials=trials, j=j); nz = [i for i in range(len(keys)) if np.any(M[:, i] != 0)]
    return one_dim_quadratic(M[:, nz], [keys[i] for i in nz])
rows = []
for t in range(40):
    n = int(rng.integers(1, 7)); A = carrier(n, [1, -1]); good, dim, nk = solve(A, 6000, 16); rows.append(dict(base_nodes=n, moduli_squared=nk, solution_dimension=dim, quadratic=bool(good)))
ok("Q1b_consistent_modulus_rule_is_quadratic_on_40_degree_two_signed_carriers", all(r["quadratic"] for r in rows), rows=rows, seed=SEED, largest_modulus=max(r["moduli_squared"] for r in rows))
rows4 = []
for t in range(10):
    n = int(rng.integers(1, 5)); A = carrier(n, [1, 1j, -1, -1j]); good, dim, nk = solve(A, 6000, 12); rows4.append(dict(base_nodes=n, moduli_squared=nk, solution_dimension=dim, quadratic=bool(good), has_non_real_gain=bool(np.any(np.abs(A.imag) > 0.5))))
ok("Q4b_gains_of_order_four_force_the_square_on_gaussian_moduli", all(r["quadratic"] for r in rows4) and any(r["has_non_real_gain"] for r in rows4), rows=rows4)
R["_summary"] = dict(predicates=sum(1 for k in R if not k.startswith("_")), passed=sum(1 for k, v in R.items() if not k.startswith("_") and v["passed"]), seed=SEED, numpy=np.__version__)
json.dump(R, open(OUT, "w"), indent=1, default=str)
for k, v in R.items():
    if not k.startswith("_"): print(("PASS " if v["passed"] else "FAIL ") + k)
print(R["_summary"])
