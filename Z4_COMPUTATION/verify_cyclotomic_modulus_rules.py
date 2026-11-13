#!/usr/bin/env python3
"""Sixth edition check.  Claim under test (fixed before the run).  Let q be even, zeta = exp(2 pi i / q), and let B_q be the gain digraph
on two vertices with step matrix A = [[1, zeta], [1, -zeta]] (A*A = 2; gains in the q-th roots of unity).  A rule
mu(S) = sum_y phi(|v_S(y)|), phi(0) = 0, is consistent under continuation with factor 2 exactly when
        phi(|alpha|) = sum_j c_j |sigma_j(alpha)|^2      for alpha in Z[zeta],
where sigma_j (zeta -> zeta^j, j prime to q, j and -j identified) are the conjugate characters and the c_j are real.
So the space of consistent rules has dimension phi(q)/2, and the rule is unique up to a factor exactly for q in {2, 4, 6}.
Predicates:
 H   hypothesis used in the proof: for q in (2, 4, 6, 8, 10, 12) and each vertex, at some length every group element is the gain of
     at least 3 walks from vertex 0;
 D   for each q in (2, 4, 6, 8, 10, 12): the solution space of the consistency equations over sampled amplitude pairs, with |alpha|^2 handled
     exactly in Z[zeta], has dimension phi(q)/2 and contains every conjugate squared modulus;
 U   the dimension is 1 exactly for q in (2, 4, 6);
 X   control: for q = 8 the conjugate rule sigma_3 differs from the squared modulus on the sampled moduli (largest relative difference above 0.5),
     and the fourth power of the modulus violates the equations.
Writes Cyclotomic_Modulus_Rules_Results.json; refuses to overwrite.  Seed fixed and reported."""
import cmath, json, math, os, sys
from math import gcd
import numpy as np
OUT = "Cyclotomic_Modulus_Rules_Results.json"
if os.path.exists(OUT): sys.exit("refusing to overwrite " + OUT)
R = {}; ok = lambda name, val, **info: R.__setitem__(name, dict(passed=bool(val), **info))
SEED = 20261115; rng = np.random.default_rng(SEED)
# exact arithmetic in the group ring Z[Z_q] modulo the relations of zeta: an element is an integer vector of length q (coefficients of zeta^k).
# Two vectors represent the same number iff their difference lies in the kernel; a canonical key is obtained from the exact values of the
# element under every embedding, which determine it: we use the integer vector reduced with the relation zeta^(k + q/2) = -zeta^k (q even)
# and, for the remaining relations, the tuple of its conjugates rounded at 1e-9 after exact integer evaluation of the traces.
def reduce_half(v, q):
    h = q // 2; return tuple(int(v[k] - v[k + h]) for k in range(h))           # uses zeta^(q/2) = -1; exact
def mul(a, b, q):
    c = np.zeros(q, dtype=np.int64)
    for i in np.nonzero(a)[0]:
        for j in np.nonzero(b)[0]: c[(i + j) % q] += a[i] * b[j]
    return c
def conj(a, q):
    c = np.zeros(q, dtype=np.int64)
    for i in np.nonzero(a)[0]: c[(-i) % q] += a[i]
    return c
def embed(v, q, j): return sum(int(v[k]) * cmath.exp(2j * math.pi * j * k / q) for k in range(q))
def units(q): return [j for j in range(1, q // 2 + 1) if gcd(j, q) == 1] if q > 2 else [1]
def key_of(norm_vec, q):
    """|alpha|^2 as an exact object: its values under all embeddings are real algebraic integers; the tuple of the power sums
    (traces of its powers), which are integers, identifies the multiset of conjugates; together with the value under sigma_1 rounded
    to 1e-9 it identifies the number.  Collisions would need two distinct elements of the real subfield within 1e-9 with equal traces."""
    vals = [embed(norm_vec, q, j).real for j in units(q)]
    traces = tuple(int(round(sum(v ** p for v in vals))) for p in range(1, len(vals) + 1))
    return (traces, round(vals[0], 9))
def euler_phi(q): return sum(1 for j in range(1, q + 1) if gcd(j, q) == 1)
def hypothesis(q, N=3, maxlen=40):
    h = q // 2                                              # gains: from vertex 0: 1 -> exponent 0 (to both); from vertex 1: zeta (to 0), -zeta (to 1)
    cnt = np.zeros((2, q), dtype=object); cnt[0, 0] = 1
    for L in range(1, maxlen + 1):
        new = np.zeros((2, q), dtype=object)
        for g in range(q):
            new[0, g] += cnt[0, g]; new[1, g] += cnt[0, g]                         # leaving vertex 0 with gain 1
            new[0, (g + 1) % q] += cnt[1, g]; new[1, (g + 1 + h) % q] += cnt[1, g]  # leaving vertex 1 with gain zeta, -zeta
        cnt = new
        if all(cnt[y, g] >= N for y in (0, 1) for g in range(q)): return L
    return None
rowsH = []; rowsD = []
for q in (2, 4, 6, 8, 10, 12):
    L = hypothesis(q); rowsH.append(dict(q=q, length_at_which_every_gain_has_3_walks_to_both_vertices=L))
    h = q // 2; one = np.zeros(q, dtype=np.int64); one[0] = 1; z = np.zeros(q, dtype=np.int64); z[1 % q] = 1; mz = np.zeros(q, dtype=np.int64); mz[(1 + h) % q] = 1
    def rand_elem():
        v = np.zeros(q, dtype=np.int64)
        for _ in range(int(rng.integers(0, 4))): v[int(rng.integers(0, q))] += 1          # a sum of at most three gains: achievable by the hypothesis
        return v
    keys = {}; raw = []
    for _ in range(6000):
        a, b = rand_elem(), rand_elem()
        if not a.any() and not b.any(): continue
        ey = a + mul(z, b, q); ey2 = a + mul(mz, b, q)                                  # components of A v at the two vertices
        terms = []
        for vec, coef in ((ey, 1), (ey2, 1), (a, -2), (b, -2)):
            nv = mul(vec, conj(vec, q), q)
            if abs(embed(nv, q, 1).real) < 1e-12: continue                                # modulus zero: phi(0) = 0
            k = key_of(nv, q)
            if k not in keys: keys[k] = [embed(nv, q, j).real for j in units(q)]
            terms.append((k, coef))
        raw.append(terms)
    order = sorted(keys, key=lambda k: k[1]); idx = {k: i for i, k in enumerate(order)}
    M = np.zeros((len(raw), len(order)))
    for r, terms in enumerate(raw):
        for k, coef in terms: M[r, idx[k]] += coef
    nz = [i for i in range(len(order)) if np.any(M[:, i] != 0)]; M = M[:, nz]; conjvals = np.array([keys[order[i]] for i in nz])      # columns: sigma_j(|alpha|^2)
    _, s, vt = np.linalg.svd(M); rank = int(np.sum(s > 1e-8 * s[0])); dim = M.shape[1] - rank
    contain = float(np.abs(M @ conjvals).max())
    rowsD.append(dict(q=q, euler_phi_over_2=max(1, euler_phi(q) // 2), moduli=len(nz), equations=len(raw), solution_dimension=dim, largest_defect_of_conjugate_rules=contain,
                      conjugate_characters=units(q)))
    if q == 8:
        rel = float(np.max(np.abs(conjvals[:, 1] - conjvals[:, 0]) / np.maximum(np.abs(conjvals[:, 0]), 1e-12)))
        quart = float(np.abs(M @ (conjvals[:, 0] ** 2)).max())
        ok("X_controls_for_order_8", rel > 0.5 and quart > 0.5, largest_relative_difference_of_sigma3_rule_from_squared_modulus=rel, largest_defect_of_fourth_power=quart)
    print(rowsD[-1], flush=True)
ok("H_every_gain_reached_with_multiplicity_on_both_vertices", all(r["length_at_which_every_gain_has_3_walks_to_both_vertices"] is not None for r in rowsH), rows=rowsH)
ok("D_solution_space_is_spanned_by_the_conjugate_squared_moduli", all(r["solution_dimension"] == r["euler_phi_over_2"] and r["largest_defect_of_conjugate_rules"] < 1e-7 for r in rowsD), rows=rowsD, seed=SEED)
ok("U_unique_rule_exactly_for_orders_2_4_6", all((r["solution_dimension"] == 1) == (r["q"] in (2, 4, 6)) for r in rowsD))
R["_summary"] = dict(predicates=sum(1 for k in R if not k.startswith("_")), passed=sum(1 for k, v in R.items() if not k.startswith("_") and v["passed"]), seed=SEED, numpy=np.__version__)
json.dump(R, open(OUT, "w"), indent=1, default=str)
for k, v in R.items():
    if not k.startswith("_"): print(("PASS " if v["passed"] else "FAIL ") + k)
print(R["_summary"])
