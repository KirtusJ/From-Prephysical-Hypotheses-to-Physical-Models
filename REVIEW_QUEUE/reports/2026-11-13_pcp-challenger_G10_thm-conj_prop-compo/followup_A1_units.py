#!/usr/bin/env python3
"""Follow-up to the FAILED predicate A1 of challenge_thm_conj_prop_compo.py (kept, not edited).

A1 failed for q=16 on 50 weight vectors of the boundary kind c = (1,..,-1e-3,..,1): the search region
(coefficients up to 40 along random directions) contained no lattice element with phi < 0.  The
proposition's proof says one exists (density of lattice rays).  This follow-up looks for one
constructively, among products of Galois conjugates of the unit u = 1 + zeta + zeta^2 of Z[zeta_16].

PREDICATE A1b (fixed before the run): for q = 16 and each k in 0..3, with c_j = 1 for j != k and
c_k = -1e-3, some element alpha = prod_{i in (1,3,5,7)} sigma_i(u)^{e_i}, 0 <= e_i <= 6, computed
exactly in Z[zeta_16], has sum_j c_j |sigma_j(alpha)|^2 < 0, where the float value is used only when
|value| > 1e-6 * (sum_j |sigma_j(alpha)|^2) (relative rounding of the embedding sums is < 1e-10 for
integer coefficients below 1e5; larger coefficients are not used).  Report the element found.
Also A1c: the same for q = 8, 10, 12 with c_k = -1e-6 (harder boundary), exponents 0..12, unit
u = 1 + zeta + zeta^2 for q = 8, 10 and u = 1 + zeta for q = 12, coefficient limit 1e9.
Result file followup_A1_units_results.json, never overwritten.
"""
import json, os, sys, itertools, importlib.util, math
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "followup_A1_units_results.json")
if os.path.exists(OUT): sys.exit("result file exists; refusing to overwrite")
# reuse only the exact ring class of the first program (same author), without running it
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "challenge_thm_conj_prop_compo.py")).read()
ns = {}
exec(src[src.index("class Ring:"):src.index("def Bq(q)")], {"np": __import__("numpy"), "math": math, "Poly": __import__("sympy").Poly,
     "cyclotomic_poly": __import__("sympy").cyclotomic_poly, "x": __import__("sympy").symbols("x")}, ns)
Ring = ns["Ring"]
def sigma(R, a, i):  # Galois conjugate as exact element
    out = R.zero()
    for t, c in enumerate(a):
        if c:
            p = R.pw[(i * t) % R.q]; out = R.add(out, tuple(c * v for v in p))
    return out
def powr(R, a, e):
    r = R.one()
    for _ in range(e): r = R.mul(r, a)
    return r
def search(q, ucoef, eps, emax, lim):
    R = Ring(q); u = R.zero()
    for k in ucoef: u = R.add(u, R.pw[k])
    units = [k for k in range(1, q) if math.gcd(k, q) == 1 and k < q // 2] or [1]
    conj = [sigma(R, u, i) for i in units]
    normprod = R.one()
    for i in range(1, q):
        if math.gcd(i, q) == 1: normprod = R.mul(normprod, sigma(R, u, i))
    pows = [[powr(R, c, e) for e in range(emax + 1)] for c in conj]
    out = {"unit_norm": list(normprod), "J": R.J}
    for k in range(len(R.J)):
        c = [1.0] * len(R.J); c[k] = -eps; best = None
        for es in itertools.product(range(emax + 1), repeat=len(conj)):
            al = R.one()
            for i, e in enumerate(es): al = R.mul(al, pows[i][e])
            if max(map(abs, al)) > lim: continue
            Ns = [R.Nj(al, j) for j in R.J]; val = sum(ci * n for ci, n in zip(c, Ns))
            if val < -1e-6 * sum(Ns) and (best is None or max(map(abs, al)) < max(map(abs, best[0]))): best = (al, val, Ns, es)
        out[f"k={k}"] = None if best is None else dict(alpha=list(best[0]), phi=best[1], N=best[2], exponents=list(best[3]))
    out["met"] = all(out[f"k={k}"] is not None for k in range(len(R.J)))
    return out
res = {"A1b_q16": search(16, (0, 1, 2), 1e-3, 6, 1e5)}
res["A1c"] = {q: search(q, uc, 1e-6, 12, 1e9) for q, uc in ((8, (0, 1, 2)), (10, (0, 1, 2)), (12, (0, 1)))}
res["A1b_met"] = res["A1b_q16"]["met"]; res["A1c_met"] = all(v["met"] for v in res["A1c"].values())
json.dump(res, open(OUT, "w"), indent=1, default=str)
print(json.dumps(res, default=str)[:3000])
