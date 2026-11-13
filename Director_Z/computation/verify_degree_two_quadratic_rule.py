#!/usr/bin/env python3
"""Fifth edition check.  Claim under test (fixed before the run): on every finite connected signed gain digraph that is norm-preserving of
degree two (the arc digraph of a connected digraph with two arcs into and out of every node, zigzag sign -1 at every node), a rule
mu(S) = sum_y phi(|v_S(y)|), phi(0) = 0, consistent under continuation with factor 2 has phi(n) = n^2 phi(1) on the moduli that occur.
Predicates:
 Q1  for 40 random carriers (base digraphs on 1 to 6 nodes built from two random permutations, random signs with zigzag -1 at each node,
     kept if connected) the consistency equations over sampled events have a one-dimensional solution space spanned by n^2;
 Q2  the two vertices of every block are reached from the start vertex at the same lengths (all lengths 6..14 checked), which the proof uses;
 Q3  control: on the same carriers with all signs +1, phi(n) = n satisfies every equation and phi(n) = n^2 does not;
 Q4  gains of order four (entries in {1, i, -1, -i}, unitary blocks): the equations over sampled events force phi(|z|) = |z|^2 phi(1)
     on the Gaussian moduli that occur (10 carriers).
Writes Degree_Two_Quadratic_Rule_Results.json; refuses to overwrite.  Seed fixed and reported."""
import json, os, sys
import numpy as np
OUT = "Degree_Two_Quadratic_Rule_Results.json"
if os.path.exists(OUT): sys.exit("refusing to overwrite " + OUT)
R = {}; ok = lambda name, val, **info: R.__setitem__(name, dict(passed=bool(val), **info))
SEED = 20261113; rng = np.random.default_rng(SEED)
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
rows = []; q2 = True
for t in range(40):
    n = int(rng.integers(1, 7)); A = carrier(n, [1, -1]); M, keys = equations(A); good, dim, nk = one_dim_quadratic(M, keys)
    # Q2: block partners share their reachable lengths
    B = (np.abs(A) > 0).astype(int); same = True
    partners = [(x, xp) for x in range(2 * n) for xp in range(x + 1, 2 * n) if np.any(B[:, x] & B[:, xp])]
    P = np.eye(2 * n, dtype=int)
    for L in range(1, 15):
        P = ((B @ P) > 0).astype(int)
        if L >= 6: same &= all(P[x, 0] == P[xp, 0] for x, xp in partners)
    q2 &= same
    # Q3 control
    A0 = np.abs(A); M0, keys0 = equations(A0); lin = np.sqrt(np.array(keys0, dtype=float)); quad = np.array(keys0, dtype=float)
    rows.append(dict(base_nodes=n, moduli_squared=nk, solution_dimension=dim, quadratic=bool(good), partners_same_lengths=bool(same),
                     trivial_gains_linear_defect=float(np.abs(M0 @ lin).max()), trivial_gains_quadratic_defect=float(np.abs(M0 @ quad).max())))
ok("Q1_consistent_modulus_rule_is_quadratic_on_40_degree_two_signed_carriers", all(r["quadratic"] for r in rows), rows=rows, seed=SEED)
ok("Q2_block_partners_are_reached_at_the_same_lengths", q2)
ok("Q3_control_trivial_gains_accept_the_count_and_reject_the_square", all(r["trivial_gains_linear_defect"] < 1e-9 and r["trivial_gains_quadratic_defect"] > 0.5 for r in rows))
rows4 = []
for t in range(10):
    n = int(rng.integers(1, 5)); A = carrier(n, [1, 1j, -1, -1j]); M, keys = equations(A, trials=3000); good, dim, nk = one_dim_quadratic(M, keys)
    rows4.append(dict(base_nodes=n, moduli_squared=nk, solution_dimension=dim, quadratic=bool(good), has_non_real_gain=bool(np.any(np.abs(A.imag) > 0.5))))
ok("Q4_gains_of_order_four_force_the_square_on_gaussian_moduli", all(r["quadratic"] for r in rows4) and any(r["has_non_real_gain"] for r in rows4), rows=rows4)
R["_summary"] = dict(predicates=sum(1 for k in R if not k.startswith("_")), passed=sum(1 for k, v in R.items() if not k.startswith("_") and v["passed"]), seed=SEED, numpy=np.__version__)
json.dump(R, open(OUT, "w"), indent=1, default=str)
for k, v in R.items():
    if not k.startswith("_"): print(("PASS " if v["passed"] else "FAIL ") + k)
print(R["_summary"])
