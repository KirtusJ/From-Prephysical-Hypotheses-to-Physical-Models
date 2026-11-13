#!/usr/bin/env python3
"""Follow-up to verify_fourier_blocks_any_degree.py, whose predicates A1 and A3 failed on 2 of 22 carriers and are kept: one carrier
with (d, q) = (3, 12) and one with (4, 8) had only 8 distinct squared moduli and a solution space of dimension 1.  Diagnosis: their gains
generate a proper subgroup, so the amplitudes lie in a subring on which the conjugate rules coincide; the hypothesis of the claim (every
q-th root of unity is the gain of walks to the vertices of a block) fails, and the predicates did not test it.  This is the same defect of
a predicate as in three earlier programs of the session.
This run: the same cases, three carriers each, a new seed.  H(carrier): every q-th root of unity is the gain of some walk of the sampled
length to every vertex.  Predicates fixed before the run:
 A1b  on every carrier with H the solution space has dimension phi(q)/2;
 A1c  at least 25 of the 33 carriers satisfy H;
 A2b  on every carrier every conjugate squared modulus satisfies every equation (residual below 1e-7);
 A3b  on every carrier with H and phi(q)/2 >= 2 a second conjugate rule differs from the squared modulus by more than 10 percent on a
      sampled value; on every carrier the fourth power leaves a residual above 1e-3.
Writes Fourier_Blocks_Any_Degree_Followup_Results.json; refuses to overwrite.  Seed fixed and reported."""
import cmath, json, math, os, sys
from math import gcd
import numpy as np
OUT = "Fourier_Blocks_Any_Degree_Followup_Results.json"
if os.path.exists(OUT): sys.exit("refusing to overwrite " + OUT)
R = {}; ok = lambda name, val, **info: R.__setitem__(name, dict(passed=bool(val), **info))
SEED = 20261126; rng = np.random.default_rng(SEED)
def run(d, q):
    J = [j for j in range(1, q // 2 + 1) if gcd(j, q) == 1] if q > 2 else [1]; n = int(rng.integers(1, 3)); V = n * d
    perms = [rng.permutation(n) for _ in range(d)]; K = [[None] * V for _ in range(V)]
    for node in range(n):
        inc = [k * d + i for i in range(d) for k in range(n) if perms[i][k] == node]; out = [node * d + i for i in range(d)]; rho = rng.integers(0, q, d); kap = rng.integers(0, q, d)
        for z, b in enumerate(out):
            for y, a in enumerate(inc): K[b][a] = int(rho[z] + kap[y] + (q // d) * z * y) % q
    L = max(2, int(math.log(4000) / math.log(d))); ws = [(0, 0)]
    for _ in range(L): ws = [(b, (g + K[b][a]) % q) for a, g in ws for b in range(V) if K[b][a] is not None]
    E = np.array([[cmath.exp(2j * math.pi * j * k / q) for k in range(q)] for j in J])          # embeddings of the group elements
    reach = {}
    for b, g in ws: reach.setdefault(b, set()).add(g)
    H = len(reach) == V and all(len(reach[b]) == q for b in range(V))
    keys = {}; eqs = []
    def key(vec):
        vals = np.abs(E @ vec) ** 2
        if vals[0] < 1e-9: return None
        k = tuple(np.round(vals, 7)); keys.setdefault(k, vals); return k
    for _ in range(8000):
        idx = rng.choice(len(ws), size=int(rng.integers(1, 5)), replace=False); v = {}
        for i in idx:
            b, g = ws[int(i)]; v.setdefault(b, np.zeros(q))[g] += 1
        w = {}
        for a, vec in v.items():
            for b in range(V):
                if K[b][a] is not None: w.setdefault(b, np.zeros(q)); w[b] += np.roll(vec, K[b][a])
        row = {}
        for vec in w.values():
            k = key(vec)
            if k is not None: row[k] = row.get(k, 0) + 1
        for vec in v.values():
            k = key(vec)
            if k is not None: row[k] = row.get(k, 0) - d
        row = {k: c for k, c in row.items() if c}
        if row: eqs.append(row)
    order = sorted({k for r in eqs for k in r}); col = {k: i for i, k in enumerate(order)}; M = np.zeros((len(eqs), len(order)))
    for i, r in enumerate(eqs):
        for k, c in r.items(): M[i, col[k]] = c
    conj = np.array([keys[k] for k in order]); _, s, _ = np.linalg.svd(M); rank = int(np.sum(s > 1e-8 * s[0])); dim = len(order) - rank
    res = float(np.abs(M @ conj).max()) / (float(np.abs(M).max()) * float(conj.max()))
    quart = float(np.abs(M @ (conj[:, 0] ** 2)).max()) / (float(np.abs(M).max()) * float((conj[:, 0] ** 2).max()))
    diff = float(np.max(np.abs(conj[:, 1] - conj[:, 0]) / conj[:, 0])) if len(J) > 1 else None
    return dict(hypothesis=bool(H), degree=d, order=q, vertices=V, walk_length=L, values=len(order), equations=len(eqs), expected_dimension=len(J), solution_dimension=dim,
                residual_of_conjugate_rules=res, residual_of_fourth_power=quart, largest_relative_difference_of_second_conjugate=diff)
rows = []
for d, q in ((3, 3), (3, 6), (3, 9), (3, 12), (4, 4), (4, 8), (4, 12), (5, 5), (5, 10), (6, 6), (6, 12)):
    for t in range(3): rows.append(run(d, q)); print(rows[-1], flush=True)
wH = [r for r in rows if r["hypothesis"]]
ok("A1b_dimension_with_the_hypothesis", all(r["solution_dimension"] == r["expected_dimension"] for r in wH))
ok("A1c_coverage", len(wH) >= 25, carriers_with_hypothesis=len(wH))
ok("A2b_conjugate_rules_are_consistent", all(r["residual_of_conjugate_rules"] < 1e-7 for r in rows))
ok("A3b_controls", all(r["residual_of_fourth_power"] > 1e-3 for r in rows) and all(r["largest_relative_difference_of_second_conjugate"] > 0.1 for r in wH if r["expected_dimension"] >= 2), rows=rows, seed=SEED)
R["_summary"] = dict(predicates=4, passed=sum(1 for k, v in R.items() if not k.startswith("_") and v["passed"]), seed=SEED, numpy=np.__version__)
json.dump(R, open(OUT, "w"), indent=1, default=str)
for k, v in R.items():
    if not k.startswith("_"): print(("PASS " if v["passed"] else "FAIL ") + k)
print(R["_summary"])
