#!/usr/bin/env python3
"""Eleventh edition check.  Claim under test (fixed before the run): on arc digraphs whose d x d blocks of gains are rho_z kappa_y w^(z y),
w a primitive d-th root of unity, for d = 3 (gains in the third or sixth roots of unity; amplitudes in Z[omega]) and d = 4 (gains in the
fourth roots of unity; amplitudes in Z[i]), a rule mu(S) = sum over end vertices of phi(|v_S(y)|), phi(0) = 0, is consistent under
continuation with factor d only if phi is a multiple of the squared modulus.
Carriers: base digraphs on 1 or 2 nodes with d arcs out of and into every node; rho, kappa random gains.  Events: 6000 random sets of
one to five walks of length 7 (d = 3) or 6 (d = 4) from arc 0.  Squared moduli are computed exactly as integer norms.
Predicates:
 D3   for 4 carriers with gains in the third roots and 4 with gains in the sixth roots of unity: the solution space of the consistency
      equations, in the unknowns phi at the norms that occur with a nonzero coefficient, is one-dimensional and proportional to the norm;
 D4   the same for 4 carriers of degree four with gains in the fourth roots of unity;
 DC   control: on each carrier the squared modulus satisfies every equation exactly (integer residual 0) and the modulus to the fourth
      power does not.
Recorded without a predicate: the number of distinct norms and the largest norm on each carrier.
Writes Record_Sum_Higher_Degree_Results.json; refuses to overwrite.  Seed fixed and reported."""
import json, os, sys
import numpy as np
OUT = "Record_Sum_Higher_Degree_Results.json"
if os.path.exists(OUT): sys.exit("refusing to overwrite " + OUT)
R = {}; ok = lambda name, val, **info: R.__setitem__(name, dict(passed=bool(val), **info))
SEED = 20261124; rng = np.random.default_rng(SEED)
class Ring:
    """Z[zeta_q] for q in (3, 6) (basis 1, omega with omega^2 = -1 - omega) or q = 4 (basis 1, i).  Elements are integer pairs."""
    def __init__(self, q):
        self.q = q
        if q in (3, 6):
            om = (0, 1); self.mul = lambda a, b: (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0] - a[1] * b[1]); self.norm = lambda a: a[0] * a[0] - a[0] * a[1] + a[1] * a[1]
            z = om if q == 3 else (-om[0] - 1 - (-1), 0)        # placeholder, replaced below
            # sixth root: zeta_6 = -omega^2 = 1 + omega
            self.gen = om if q == 3 else (1, 1)
        else:
            self.mul = lambda a, b: (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]); self.norm = lambda a: a[0] * a[0] + a[1] * a[1]; self.gen = (0, 1)
        self.pow = [(1, 0)]
        for _ in range(q - 1): self.pow.append(self.mul(self.pow[-1], self.gen))
        assert self.mul(self.pow[-1], self.gen) == (1, 0)
def carrier(ring, d, n):
    q = ring.q; perms = [rng.permutation(n) for _ in range(d)]; V = n * d; K = [[None] * V for _ in range(V)]
    for node in range(n):
        inc = [k * d + i for i in range(d) for k in range(n) if perms[i][k] == node]; out = [node * d + i for i in range(d)]
        rho = rng.integers(0, q, d); kap = rng.integers(0, q, d)
        for z, b in enumerate(out):
            for y, a in enumerate(inc): K[b][a] = int(rho[z] + kap[y] + (q // d) * z * y) % q
    return K
def run(q, d, L, n):
    ring = Ring(q); K = carrier(ring, d, n); V = len(K); ws = [(0, 0)]
    for _ in range(L): ws = [(b, (g + K[b][a]) % q) for a, g in ws for b in range(V) if K[b][a] is not None]
    eqs = []
    for _ in range(6000):
        idx = rng.choice(len(ws), size=int(rng.integers(1, 6)), replace=False); v = {}
        for i in idx:
            b, g = ws[int(i)]; p = ring.pow[g]; cur = v.get(b, (0, 0)); v[b] = (cur[0] + p[0], cur[1] + p[1])
        w = {}
        for a, val in v.items():
            for b in range(V):
                if K[b][a] is None: continue
                t = ring.mul(val, ring.pow[K[b][a]]); cur = w.get(b, (0, 0)); w[b] = (cur[0] + t[0], cur[1] + t[1])
        row = {}
        for val in w.values():
            nn = ring.norm(val)
            if nn: row[nn] = row.get(nn, 0) + 1
        for val in v.values():
            nn = ring.norm(val)
            if nn: row[nn] = row.get(nn, 0) - d
        row = {k: c for k, c in row.items() if c}
        if row: eqs.append(row)
    keys = sorted({k for r in eqs for k in r}); col = {k: i for i, k in enumerate(keys)}; M = np.zeros((len(eqs), len(keys)))
    for i, r in enumerate(eqs):
        for k, c in r.items(): M[i, col[k]] = c
    _, s, vt = np.linalg.svd(M); rank = int(np.sum(s > 1e-9 * s[0])); null = vt[rank:]; ref = np.array(keys, dtype=float); ref /= np.linalg.norm(ref)
    prop = null.shape[0] == 1 and min(np.linalg.norm(null[0] - ref), np.linalg.norm(null[0] + ref)) < 1e-8
    sq_res = max(abs(sum(c * k for k, c in r.items())) for r in eqs); quart = max(abs(sum(c * k * k for k, c in r.items())) for r in eqs)
    return dict(order=q, degree=d, vertices=V, equations=len(eqs), norms=len(keys), largest_norm=int(keys[-1]), solution_dimension=int(null.shape[0]), proportional_to_norm=bool(prop),
                integer_residual_of_square=int(sq_res), largest_residual_of_fourth_power=int(quart))
rows = []
for q, d, L in ((3, 3, 7), (6, 3, 7), (4, 4, 6)):
    for t in range(4): rows.append(run(q, d, L, int(rng.integers(1, 3)))); print(rows[-1], flush=True)
ok("D3_degree_three_forces_the_square", all(r["proportional_to_norm"] for r in rows if r["degree"] == 3))
ok("D4_degree_four_forces_the_square", all(r["proportional_to_norm"] for r in rows if r["degree"] == 4))
ok("DC_square_exact_fourth_power_not", all(r["integer_residual_of_square"] == 0 and r["largest_residual_of_fourth_power"] > 0 for r in rows), rows=rows, seed=SEED)
R["_summary"] = dict(predicates=3, passed=sum(1 for k, v in R.items() if not k.startswith("_") and v["passed"]), seed=SEED, numpy=np.__version__)
json.dump(R, open(OUT, "w"), indent=1, default=str)
for k, v in R.items():
    if not k.startswith("_"): print(("PASS " if v["passed"] else "FAIL ") + k)
print(R["_summary"])
