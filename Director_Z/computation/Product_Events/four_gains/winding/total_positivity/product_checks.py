#!/usr/bin/env python3
"""Checks for the product theorem (three classes of winding).  Exact; no randomness.

Usage: python3 -B product_checks.py OUT.json      (OUT opened with mode 'x')

PREDICATES (fixed before the first run).
 A1 (algebra): for k = 1..5, the pull-backs G(pi(p)) of the (k+1)(k+2)/2 monomials pi_i pi_j, where
    pi = coefficients of prod_{i<=k} (p_i0 + p_i1 x), are linearly independent polynomials in the 2k variables
    (rank of the coefficient matrix = (k+1)(k+2)/2 = dim Sym^k of a 3-space = C(k+2,2)).
 A2 (coincidence): in the semiring N[x,d]/(d^r = 1, x^3 = d^kk), for r in {2,4,6} and kk in 0..r-1:
    x * A == B  with A = (4 + d^-kk + d^-kk x)(1 + x),  B = (1 + 2x)(1 + (2 + d^-kk) x),
    all coefficients of A and B being non-negative integers (multisets).
 A3 (the coincidence separates): with eps = evaluation d -> -1 and sigma = (-1)^kk, for every d from 2 to 8 and
    C = (1+x)^(d-2):  pi_A = eps(A) C and pi_B = eps(B) C have degree d and pi_A[0] pi_A[d] != pi_B[0] pi_B[d];
    and phi(pi_B) = phi(x pi_A) in Z[x]/(x^3 - sigma).
 A4 (the periodic form is constant on the fibres of phi): for the form
    Qbar(e) = q(e0^2+e1^2+e2^2) + c(e0 e1 + e1 e2 + sigma e2 e0), Qbar(phi(x pi)) == Qbar(phi(pi)) identically
    (symbolic, generic pi of degree 6, both sigma).
 A5 (control, must FAIL to be an identity): the non-periodic form  sum_i pi_i pi_{i+2}  takes different values
    at pi_A and pi_B for d = 2 (so the coincidence does detect a form that is not periodic).
"""
import sys, json, itertools
import sympy as sp
OUT = sys.argv[1]; fout = open(OUT, 'x'); res = {"command": " ".join(sys.argv)}
x = sp.symbols('x')
# A1
a1 = {}
for k in range(1, 6):
    ps = sp.symbols('p0:%d' % (2 * k))
    prod = sp.Integer(1)
    for i in range(k): prod = sp.expand(prod * (ps[2 * i] + ps[2 * i + 1] * x))
    pi = [sp.Poly(prod, x).coeff_monomial(x ** j) for j in range(k + 1)]
    polys = [sp.Poly(sp.expand(pi[i] * pi[j]), *ps) for i in range(k + 1) for j in range(i, k + 1)]
    mons = sorted({m for p in polys for m in p.monoms()})
    mat = sp.Matrix([[p.coeff_monomial(m) for m in mons] for p in polys])
    a1[k] = [mat.rank(), (k + 1) * (k + 2) // 2]
res["A1"] = {"rank_vs_dim": a1, "holds": all(v[0] == v[1] for v in a1.values())}
# semiring elements: dict (level, exponent) -> count, reduced by x^3 = d^kk when asked
def mul(P, Q, r):
    out = {}
    for (i, e), c in P.items():
        for (j, f), c2 in Q.items():
            key = (i + j, (e + f) % r); out[key] = out.get(key, 0) + c * c2
    return out
def fold(P, r, kk):
    out = {}
    for (i, e), c in P.items():
        key = (i % 3, (e + kk * (i // 3)) % r); out[key] = out.get(key, 0) + c
    return {k: v for k, v in out.items() if v}
def eps(P, deg):
    v = [0] * (deg + 1)
    for (i, e), c in P.items(): v[i] += c * (-1) ** e
    return v
a2 = {}; a3 = {}; a5 = {}
for r in (2, 4, 6):
    for kk in range(r):
        mk = (-kk) % r
        A = mul({(0, 0): 4, (0, mk): 1, (1, mk): 1} if mk else {(0, 0): 5, (1, 0): 1}, {(0, 0): 1, (1, 0): 1}, r)
        B = mul({(0, 0): 1, (1, 0): 2}, ({(0, 0): 1, (1, 0): 2, (1, mk): 1} if mk else {(0, 0): 1, (1, 0): 3}), r)
        xA = {(i + 1, e): c for (i, e), c in A.items()}
        ok = fold(xA, r, kk) == fold(B, r, kk) and all(c > 0 for c in list(A.values()) + list(B.values()))
        a2["r%d_k%d" % (r, kk)] = ok
        sigma = (-1) ** kk
        eA = sp.Poly(list(reversed(eps(A, 2))), x); eB = sp.Poly(list(reversed(eps(B, 2))), x)
        good = True; vals = []
        for d in range(2, 9):
            C = sp.Poly((1 + x) ** (d - 2), x)
            pA = (eA * C).all_coeffs()[::-1]; pB = (eB * C).all_coeffs()[::-1]
            def phi(p):
                e = [0, 0, 0]
                for i, cc in enumerate(p): e[i % 3] += cc * sigma ** (i // 3)
                return e
            cond = len(pA) == d + 1 and len(pB) == d + 1 and pA[0] * pA[d] != pB[0] * pB[d] and phi(pB) == phi([0] + pA)
            vals.append([d, int(pA[0] * pA[d]), int(pB[0] * pB[d]), bool(cond)]); good = good and cond
        a3["r%d_k%d" % (r, kk)] = {"holds": bool(good), "R_d": vals}
        pA = eA.all_coeffs()[::-1]; pB = eB.all_coeffs()[::-1]
        a5["r%d_k%d" % (r, kk)] = [int(pA[0] * pA[2]), int(pB[0] * pB[2])]
res["A2"] = {"cases": a2, "holds": all(a2.values())}
res["A3"] = {"cases": a3, "holds": all(v["holds"] for v in a3.values())}
res["A5_control_values_differ"] = {"cases": a5, "differ_everywhere": all(v[0] != v[1] for v in a5.values())}
# A4
q, c = sp.symbols('q c'); pis = sp.symbols('s0:7'); a4 = {}
for sigma in (1, -1):
    def phi(p):
        e = [0, 0, 0]
        for i, cc in enumerate(p): e[i % 3] += cc * sigma ** (i // 3)
        return e
    def Qb(e): return q * (e[0] ** 2 + e[1] ** 2 + e[2] ** 2) + c * (e[0] * e[1] + e[1] * e[2] + sigma * e[2] * e[0])
    a4[str(sigma)] = sp.expand(Qb(phi([0] + list(pis))) - Qb(phi(list(pis)))) == 0
res["A4"] = {"cases": a4, "holds": all(a4.values())}
json.dump(res, fout, indent=1); fout.close()
print({k: (v["holds"] if isinstance(v, dict) and "holds" in v else v.get("differ_everywhere")) for k, v in res.items() if k != "command"}); print(a1)
