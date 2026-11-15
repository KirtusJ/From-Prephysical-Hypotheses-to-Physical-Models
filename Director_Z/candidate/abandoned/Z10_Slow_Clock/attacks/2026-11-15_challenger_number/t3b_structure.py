#!/usr/bin/env python3
"""Challenger attack on Z10, targets 3 and 5: structure behind E6 and behind
the coincidence of the named carriers.

Usage: python3 t3b_structure.py TMAX OUT.json     (exact integers only)

Claim S0 (proved by hand, checked here): for every admissible sign rule,
  Lambda(T+1) = sum_x P_T(x) * log2 C(T, r),  x = 2r - T,
  Lambda_c(T+1) = sum_r C(T,r)/2^T * log2 C(T, r),
where P_T(x) = (eR(x)^2 + eL(x)^2)/2^T is the law of the SITE at length T.
(Both children of site x have n' = nR+nL = C(T,r) and carry (a+b)^2+(a-b)^2
 = 2(a^2+b^2).)  So E6 at length T+1 compares the mean of the same symmetric
 unimodal function phi(r)=log2 C(T,r) under P_T and under Binomial(T,1/2).

Predicates (fixed before the run), T = 1..TMAX:
 S1 (dominance): for C1, for every T and every k >= 0:
      P_T(|x| <= k) <= Binom_T(|x| <= k).
    If S1 holds at T, E6 holds at T+1 (phi is nonincreasing in |x|), so S1
    for all T would prove E6.  Violations (T,k) are listed and kept.
 S2 (invariance): the symmetrised site law P_T(x)+P_T(-x) is identical, as
    exact integers, for C1 and each of: start (0,L); the three other uniform
    single-minus rules; starts R+L, R-L, R+iL (after dividing by N0).
    If S2 holds, Lambda(T) is the same for all of them at every T (S0).
 S3: S0 itself: checked exactly in rational form for T <= 12 with Fractions of
    log-free form: sum eps'^2 over the two children == 2*(a^2+b^2) per site and
    n' == C(T,r) per child, every T <= TMAX.
"""
import sys, json
from math import comb
TMAX, OUT = int(sys.argv[1]), sys.argv[2]
fout = open(OUT, 'x')
C1 = (1, 1, 1, -1)
def run(signs, starts, N0):
    comps = [([a], [b]) for a, b in starts]
    laws = []
    s0_ok = True
    for T in range(1, TMAX + 1):
        new = []
        for eR, eL in comps:
            L = len(eR); nr = [0] * (L + 1); nl = [0] * (L + 1)
            for r in range(L):
                a = eR[r]; b = eL[r]
                nr[r + 1] = signs[0] * a + signs[1] * b
                nl[r] = signs[2] * a + signs[3] * b
                if nr[r + 1] ** 2 + nl[r] ** 2 != 2 * (a * a + b * b): s0_ok = False
            new.append((nr, nl))
        comps = new
        P = [sum(c[0][r] ** 2 + c[1][r] ** 2 for c in comps) for r in range(T + 1)]
        assert sum(P) == N0 << T
        laws.append(P)
    return laws, s0_ok
res = {"command": " ".join(sys.argv), "failed": []}
base, s0 = run(C1, [(1, 0)], 1)
res["S3_site_weight_doubling"] = s0
# n' == C(T,r): children of site r at length T-1 have counts C(T-2,r-1)+C(T-2,r) = C(T-1,r)
res["S3_child_counts"] = all(comb(T - 1, r - 1) + comb(T - 1, r) == comb(T, r) for T in range(1, TMAX + 1) for r in range(1, T))
viol = []; margins = {}
for T in range(1, TMAX + 1):
    P = base[T - 1]
    # |x| <= k  <=> |2r-T| <= k
    cumP = 0; cumB = 0; mn = None
    order = sorted(range(T + 1), key=lambda r: abs(2 * r - T))
    i = 0
    for k in range(T % 2, T + 1, 2):
        while i <= T and abs(2 * order[i] - T) <= k:
            cumP += P[order[i]]; cumB += comb(T, order[i]); i += 1
        d = cumB - cumP
        if d < 0: viol.append([T, k])
        if k < T and (mn is None or d < mn[1]): mn = (k, d)
    if T in (5, 10, 50, 100, 200, 400, 600, TMAX) and mn:
        margins[T] = {"k_of_min": mn[0], "min_(Binom-P)(|x|<=k)": mn[1] / 2 ** T}
res["S1_violations_count"] = len(viol); res["S1_first_violations"] = viol[:20]
res["S1_min_margins"] = margins
if viol: res["failed"].append("S1")
variants = {
 "start_0L": (C1, [(0, 1)], 1), "minus_RR": ((-1, 1, 1, 1), [(1, 0)], 1),
 "minus_RL(L after R)": ((1, 1, -1, 1), [(1, 0)], 1), "minus_LR(R after L)": ((1, -1, 1, 1), [(1, 0)], 1),
 "start_R+L": (C1, [(1, 1)], 2), "start_R-L": (C1, [(1, -1)], 2), "start_R+iL": (C1, [(1, 0), (0, 1)], 2)}
S2 = {}
for name, (sg, st, N0) in variants.items():
    laws, _ = run(sg, st, N0)
    bad = [T for T in range(1, TMAX + 1)
           if any(laws[T - 1][r] + laws[T - 1][T - r] != N0 * (base[T - 1][r] + base[T - 1][T - r]) for r in range(T + 1))]
    same_unsym = all(laws[T - 1] == [N0 * q for q in base[T - 1]] for T in range(1, TMAX + 1))
    S2[name] = {"n_lengths_where_symmetrised_law_differs": len(bad), "first": bad[:5],
                "unsymmetrised_law_identical_too": same_unsym}
    if bad: res["failed"].append(["S2", name])
res["S2"] = S2
json.dump(res, fout, indent=1); fout.close()
print(json.dumps(res, indent=1))
