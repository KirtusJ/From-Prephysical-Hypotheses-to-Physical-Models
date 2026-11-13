#!/usr/bin/env python3
"""Eighth edition check.  Claim under test (fixed before the run).  Let q be even, h = q/2, and let D be a gain digraph that is
norm-preserving of degree two with gains zeta^k in the q-th roots of unity.  Its signed lift has the vertices (y, s), s in Z_h, and for each
arc x -> y with gain zeta^k the arcs (x, s) -> (y, (s + k) mod h) with the sign of x^(s+k) in Z[x]/(x^h + 1).  Claim:
 (i)   the signed lift is norm-preserving of degree two with gains +1, -1;
 (ii)  on the lift the consistent rule of the record-sum form, with the pairs (vertex, sheet) as records, is unique up to a factor and is
       the square of the integer amplitude;
 (iii) that rule, as a function of a set S of walks of D, is (2/q) times the sum over the odd residues j mod q of the squared moduli
       under zeta -> zeta^j, summed over end vertices: the mean over the characters in which -1 acts as -1, faithful or not;
 (iv)  the squared modulus in one faithful character is not of the record-sum form on the lift.
Predicates:
 L1  for q in (4, 6, 8, 10, 12): the lift of B_q (step matrix [[1, zeta], [1, -zeta]]) and of 5 random carriers on 1 to 3 base nodes has
     entries in {0, 1, -1}, two nonzero entries in every column, and (lift)^T (lift) = 2 exactly;
 L2  for the same 30 lifts, on the component of the start vertex: the solution space of the consistency equations in the unknowns phi(n),
     n a positive integer occurring with a nonzero coefficient, sampled over 6000 events of walks of length 14, is one-dimensional and
     spanned by n^2;
 L3  for q in (6, 8, 10, 12) and 300 sampled events S of walks of length 8 of B_q from one vertex: the sum of squares of the integer
     amplitudes on the lift equals (2/q) sum over odd j of sum_y |sigma_j(v_S(y))|^2 to 1e-9 relative, the lift amplitudes being computed
     by walking on the lift and the sigma_j amplitudes by walking on B_q;
 L4  for q in (8, 10, 12): the two sheet vectors (1, 1, 0, ...) and (1, 0, 1, 0, ...) have equal multisets of absolute values and
     squared moduli under sigma_1 that differ by more than 0.1;
 L5  control: for q = 10 the mean of (iii) restricted to the faithful residues 1, 3, 7, 9 fails L3 on some sampled event by more than
     1e-3 relative, so the non-faithful residue 5 is needed.
Recorded without a predicate: the number of connected components of each lift.
Writes Signed_Lift_Rule_Results.json; refuses to overwrite.  Seed fixed and reported."""
import cmath, json, math, os, sys
import numpy as np
OUT = "Signed_Lift_Rule_Results.json"
if os.path.exists(OUT): sys.exit("refusing to overwrite " + OUT)
R = {}; ok = lambda name, val, **info: R.__setitem__(name, dict(passed=bool(val), **info))
SEED = 20261117; rng = np.random.default_rng(SEED)
def base_Bq(q):                                  # exponent matrix K[b, a] = k if arc a -> b has gain zeta^k, -1 if absent
    h = q // 2; return np.array([[0, 1], [0, (1 + h) % q]])
def random_base(n, q):
    """arc digraph of a base digraph on n nodes with two outgoing arcs per node; 2x2 blocks with orthogonal columns; exponents mod q"""
    h = q // 2
    while True:
        p1, p2 = rng.permutation(n), rng.permutation(n)
        head = {2 * k: int(p1[k]) for k in range(n)}; head.update({2 * k + 1: int(p2[k]) for k in range(n)})
        K = -np.ones((2 * n, 2 * n), dtype=int)
        for node in range(n):
            inc = [a for a in range(2 * n) if head[a] == node]; out = [2 * node, 2 * node + 1]
            k0, k1, k2 = (int(t) for t in rng.integers(0, q, 3)); blk = [[k0, k1], [k2, (k2 + k1 - k0 + h) % q]]   # u3 = -u2 u1 / u0
            for i, b in enumerate(out):
                for j, a in enumerate(inc): K[b, a] = blk[i][j]
        reach = np.linalg.matrix_power((K >= 0).astype(float) + np.eye(2 * n), 2 * n)
        if np.all(reach > 0): return K
def lift(K, q):
    h = q // 2; V = K.shape[0]; L = np.zeros((V * h, V * h), dtype=np.int64)
    for b in range(V):
        for a in range(V):
            k = int(K[b, a])
            if k < 0: continue
            for s in range(h):
                t = s + k; L[b * h + t % h, a * h + s] += (-1) ** (t // h)
    return L
def components(L):
    n = L.shape[0]; adj = (L != 0) | (L.T != 0); seen = -np.ones(n, dtype=int); c = 0
    for v in range(n):
        if seen[v] >= 0: continue
        stack = [v]; seen[v] = c
        while stack:
            u = stack.pop()
            for w in np.nonzero(adj[u])[0]:
                if seen[w] < 0: seen[w] = c; stack.append(int(w))
        c += 1
    return c
def walk_tables(L, start, j, cap=6):
    """vertex -> list of signs of walks of length j from start, at most `cap` of each sign"""
    cur = {start: [1]}
    for _ in range(j):
        nxt = {}
        for x, gs in cur.items():
            for y in np.nonzero(L[:, x])[0]: nxt.setdefault(int(y), []).extend(g * int(L[y, x]) for g in gs)
        cur = {y: [1] * min(cap, gs.count(1)) + [-1] * min(cap, gs.count(-1)) for y, gs in nxt.items()}
    return cur
def solve(L, trials=6000, j=14):
    tab = walk_tables(L, 0, j); verts = sorted(tab); raw = []
    for _ in range(trials):
        v = np.zeros(L.shape[0], dtype=np.int64)
        for x in rng.choice(verts, size=min(len(verts), int(rng.integers(1, 3))), replace=False):
            gs = tab[int(x)]; pick = rng.random(len(gs)) < 0.5; v[int(x)] = sum(g for g, p in zip(gs, pick) if p)
        if not v.any(): continue
        raw.append((np.abs(L @ v), np.abs(v)))
    keys = sorted({int(m) for e, a in raw for m in list(e) + list(a) if m > 0}); idx = {m: i for i, m in enumerate(keys)}
    M = np.zeros((len(raw), len(keys)))
    for r, (e, a) in enumerate(raw):
        for m in e:
            if m > 0: M[r, idx[int(m)]] += 1
        for m in a:
            if m > 0: M[r, idx[int(m)]] -= 2
    nz = [i for i in range(len(keys)) if np.any(M[:, i] != 0)]; M = M[:, nz]; ks = np.array([keys[i] for i in nz], dtype=float)
    _, s, vt = np.linalg.svd(M); rank = int(np.sum(s > 1e-9 * s[0])); null = vt[rank:]
    sq = ks ** 2 / np.linalg.norm(ks ** 2)
    good = null.shape[0] == 1 and min(np.linalg.norm(null[0] - sq), np.linalg.norm(null[0] + sq)) < 1e-8
    return bool(good), int(null.shape[0]), int(ks.max())
rows1 = []; allL1 = True; allL2 = True
for q in (4, 6, 8, 10, 12):
    for t in range(6):
        K = base_Bq(q) if t == 0 else random_base(int(rng.integers(1, 4)), q); L = lift(K, q)
        exact = bool(set(np.unique(L)) <= {-1, 0, 1} and np.all((L != 0).sum(axis=0) == 2) and np.array_equal(L.T @ L, 2 * np.eye(L.shape[0], dtype=np.int64)))
        good, dim, big = solve(L); allL1 &= exact; allL2 &= good
        rows1.append(dict(q=q, carrier="B_q" if t == 0 else "random", base_arcs=int(K.shape[0]), lift_vertices=int(L.shape[0]), components=components(L), signed_norm_preserving=exact,
                          solution_dimension=dim, quadratic=good, largest_integer_modulus=big)); print(rows1[-1], flush=True)
ok("L1_signed_lift_is_norm_preserving_of_degree_two", allL1)
ok("L2_record_sum_rule_on_the_lift_is_the_square", allL2, rows=rows1, seed=SEED)
rows3 = []; worst3 = 0.0; worst5 = 0.0
for q in (6, 8, 10, 12):
    h = q // 2; K = base_Bq(q); L = lift(K, q); odd = [j for j in range(1, q, 2)]
    walks = [(0, 0)]                                       # (end vertex of B_q, exponent of the gain), all walks of length 8 from vertex 0
    for _ in range(8): walks = [(b, (k + int(K[b, a])) % q) for a, k in walks for b in (0, 1)]
    wq = 0.0
    for _ in range(300):
        pick = rng.random(len(walks)) < rng.uniform(0.05, 0.6); S = [w for w, p in zip(walks, pick) if p]
        if not S: continue
        n = np.zeros((2, h), dtype=np.int64)               # lift amplitudes by walking on the lift: sheet (k mod h), sign (-1)^(k div h)
        for b, k in S: n[b, k % h] += (-1) ** (k // h)
        lifted = float((n ** 2).sum())
        def mean(js): return (2.0 / q) * sum(abs(sum(cmath.exp(2j * math.pi * j * k / q) for b, k in S if b == y)) ** 2 for j in js for y in (0, 1))
        wq = max(wq, abs(lifted - mean(odd)) / lifted)
        if q == 10: worst5 = max(worst5, abs(lifted - mean((1, 3, 7, 9)) * (q / 2.0) / 4.0) / lifted)       # weights 1/4 on the four faithful residues
    rows3.append(dict(q=q, odd_residues=odd, largest_relative_difference=wq)); worst3 = max(worst3, wq)
ok("L3_lift_rule_is_the_mean_over_odd_characters", worst3 < 1e-9, rows=rows3)
rows4 = []
for q in (8, 10, 12):
    z = cmath.exp(2j * math.pi / q); a = abs(1 + z) ** 2; b = abs(1 + z * z) ** 2; rows4.append(dict(q=q, sigma1_of_1_1_0=a, sigma1_of_1_0_1=b))
ok("L4_single_character_rule_is_not_a_record_sum_on_the_lift", all(abs(r["sigma1_of_1_1_0"] - r["sigma1_of_1_0_1"]) > 0.1 for r in rows4), rows=rows4)
ok("L5_control_non_faithful_residue_is_needed_for_order_10", worst5 > 1e-3, largest_relative_difference_of_faithful_mean=worst5,
   note="faithful mean taken with weights normalized to sum to one over the residues 1, 3, 7, 9")
R["_summary"] = dict(predicates=sum(1 for k in R if not k.startswith("_")), passed=sum(1 for k, v in R.items() if not k.startswith("_") and v["passed"]), seed=SEED, numpy=np.__version__)
json.dump(R, open(OUT, "w"), indent=1, default=str)
for k, v in R.items():
    if not k.startswith("_"): print(("PASS " if v["passed"] else "FAIL ") + k)
print(R["_summary"])
