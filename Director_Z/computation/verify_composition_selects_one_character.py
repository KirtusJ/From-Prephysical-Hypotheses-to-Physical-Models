#!/usr/bin/env python3
"""Seventh edition check.  Claim under test (fixed before the run): a rule phi(|alpha|) = sum_j c_j |sigma_j(alpha)|^2 on Z[zeta_q] is
multiplicative on products of carriers, mu(S1 x S2) = mu(S1) mu(S2) with mu(S) = sum_y phi(|v_S(y)|) and v_{S1 x S2} = v_{S1} (x) v_{S2},
exactly when c has one entry 1 and the others 0 (or is zero); and phi >= 0 on all moduli exactly when every c_j >= 0.
Predicates (q = 8, 10, 12; event vectors with two components drawn from Z[zeta], coefficients in -3..3):
 P1  the functions M_j(S) = sum_y |sigma_j(v_S(y))|^2 are linearly independent over the sampled events (rank phi(q)/2);
 P2  for c = (1, 0) and c = (0, 1) the largest multiplicativity defect over 2000 sampled pairs of events is below 1e-9 relative;
 P3  for c = (1/2, 1/2), (1, 1), (2, 0) and (1, -1) it is above 1e-3 relative;
 P4  for c = (1, -0.2) some sampled modulus has phi < 0, and for c = (1, 0.2) none has.
Writes Composition_Selects_One_Character_Results.json; refuses to overwrite.  Seed fixed and reported."""
import cmath, json, math, os, sys
from math import gcd
import numpy as np
OUT = "Composition_Selects_One_Character_Results.json"
if os.path.exists(OUT): sys.exit("refusing to overwrite " + OUT)
R = {}; ok = lambda name, val, **info: R.__setitem__(name, dict(passed=bool(val), **info))
SEED = 20261116; rng = np.random.default_rng(SEED)
def units(q): return [j for j in range(1, q // 2 + 1) if gcd(j, q) == 1]
rows = []
for q in (8, 10, 12):
    J = units(q); assert len(J) == 2
    def elem():                                           # integer coefficient vector of an element of Z[zeta]
        return rng.integers(-3, 4, q)
    def N(v):                                             # (|sigma_j(alpha)|^2)_j
        return np.array([abs(sum(int(v[k]) * cmath.exp(2j * math.pi * j * k / q) for k in range(q))) ** 2 for j in J])
    events = [[N(elem()), N(elem())] for _ in range(400)]                 # an event vector with two components; M_j = sum over components
    M = np.array([e[0] + e[1] for e in events]); rank = int(np.linalg.matrix_rank(M))
    def defect(c):
        c = np.array(c, dtype=float); worst = 0.0
        for _ in range(2000):
            a, b = events[int(rng.integers(0, 400))], events[int(rng.integers(0, 400))]
            prod = sum(float(c @ (x * y)) for x in a for y in b)           # sum over pairs of components of phi(|x y|): N_j is multiplicative
            sep = float(c @ (a[0] + a[1])) * float(c @ (b[0] + b[1]))
            worst = max(worst, abs(prod - sep) / max(abs(prod), abs(sep), 1e-12))
        return worst
    pure = {str(c): defect(c) for c in ((1, 0), (0, 1))}; mixed = {str(c): defect(c) for c in ((0.5, 0.5), (1, 1), (2, 0), (1, -1))}
    allN = np.array([e[i] for e in events for i in (0, 1)])
    neg = float((allN @ np.array([1, -0.2])).min()); pos = float((allN @ np.array([1, 0.2])).min())
    rows.append(dict(q=q, conjugate_characters=J, rank_of_M=rank, defect_pure=pure, defect_mixed=mixed, smallest_phi_for_c_1_minus_0p2=neg, smallest_phi_for_c_1_plus_0p2=pos))
    print(rows[-1], flush=True)
ok("P1_conjugate_measures_are_independent", all(r["rank_of_M"] == 2 for r in rows))
ok("P2_single_character_is_multiplicative", all(v < 1e-9 for r in rows for v in r["defect_pure"].values()))
ok("P3_mixtures_and_other_normalizations_are_not", all(v > 1e-3 for r in rows for v in r["defect_mixed"].values()))
ok("P4_positivity_needs_non_negative_weights", all(r["smallest_phi_for_c_1_minus_0p2"] < 0 and r["smallest_phi_for_c_1_plus_0p2"] >= 0 for r in rows), rows=rows, seed=SEED)
R["_summary"] = dict(predicates=sum(1 for k in R if not k.startswith("_")), passed=sum(1 for k, v in R.items() if not k.startswith("_") and v["passed"]), seed=SEED, numpy=np.__version__)
json.dump(R, open(OUT, "w"), indent=1, default=str)
for k, v in R.items():
    if not k.startswith("_"): print(("PASS " if v["passed"] else "FAIL ") + k)
print(R["_summary"])
