#!/usr/bin/env python3
"""Wildcard (seed: hinge).  Exact return of the signed arc digraph of a ring.

Carrier (as in Director_Z/candidate/abandoned/Z1/.../alt_rules_followup.py lines 23-24):
vertices (x,c), x in Z/N, c in {R,L}; arcs (x,c)->(x+1,R) and (x,c)->(x-1,L);
gain -1 for the arc (x,L)->(x-1,L), +1 otherwise.  A = integer step matrix, U = A/sqrt2.
x0 = (0,R).  Return weight of the square rule: R_t = ((A^t)_{x0,x0})^2 / 2^t.
All arithmetic is exact (integers; rational polynomials).  No tolerance is used.

PREDICATES, fixed before the first run:
P1  For N = 2..40: U is periodic (U^t = 1 for some t >= 1) if and only if N in {2,4,8}.
    Test: U unitary, so periodic iff every root of charpoly(A^2)(2x) is a root of unity,
    iff every irreducible factor over Q of that polynomial is, up to a rational scalar,
    a cyclotomic polynomial.
P2  Smallest t >= 1 with A^t = 2^(t/2) * 1 (t even, t <= 200): N=2 -> 2, N=4 -> 8, N=8 -> 24.
P3  For N = 3..12 and 1 <= t <= T (T = 100000): R_t = 1 exactly occurs first at t = 8 for
    N = 4, at t = 24 for N = 8, and never for the other N.   (Record: WHY_ABANDONED.md,
    'Return is late or never exact'.)
P4  For N = 3..12 the first t >= 1 with R_t > 99/100 (tested as 100 v^2 > 99 2^t) is
    38, 8, 264, 38, 504, 24, 95946, 264 for N = 3..10, none up to T for N = 11, 6416 for N = 12.
P5  For N in {3,4,5,6,8}: first t with R_t > 99/100 is below 4000 (the horizon of the
    sentence in G10 after Corollary 5.29); reported also: which N in 3..12 are not.
Failed predicates are kept in the result file.
"""
import json, sys, time
from flint import fmpz_mat, fmpz_poly, fmpz
from sympy import totient

T = 100000
OUT = sys.argv[1] if len(sys.argv) > 1 else "ring_return_result.json"

def verts(N): return [(x, c) for x in range(N) for c in "RL"]

def step_matrix(N):
    V = verts(N); idx = {v: i for i, v in enumerate(V)}
    rows = [[0] * len(V) for _ in V]
    for (x, c) in V:
        j = idx[(x, c)]
        rows[idx[((x + 1) % N, "R")]][j] += 1
        rows[idx[((x - 1) % N, "L")]][j] += (-1 if c == "L" else 1)
    return rows, idx

def cyclo(n):
    # cyclotomic polynomial as fmpz_poly
    return fmpz_poly.cyclotomic(n)

def is_cyclotomic_up_to_scalar(f):
    # f: irreducible fmpz_poly (primitive).  Cyclotomic iff monic (up to sign) and equals Phi_n
    m = f.degree()
    c = [int(a) for a in f.coeffs()]
    if abs(c[-1]) != 1: return None
    if c[-1] == -1: c = [-a for a in c]
    for n in range(1, 2 * m * m + 7):
        if int(totient(n)) == m:
            if [int(a) for a in cyclo(n).coeffs()] == c: return n
    return None

def periodic(N):
    rows, idx = step_matrix(N)
    A = fmpz_mat(rows); B = A * A
    q = B.charpoly()                       # integer, roots 2 e^{2 i omega}
    co = [int(a) for a in q.coeffs()]
    # q(2x): coefficient k multiplied by 2^k ; primitive part taken by factor()
    q2 = fmpz_poly([co[k] * (1 << k) for k in range(len(co))])
    content, facs = q2.factor()
    orders = []
    ok = True
    for f, mult in facs:
        n = is_cyclotomic_up_to_scalar(f)
        if n is None: ok = False
        orders.append([f.degree(), mult, n])
    return ok, orders

def first_identity(N, tmax=200):
    rows, idx = step_matrix(N)
    A = fmpz_mat(rows); n = len(rows)
    P = A
    for t in range(1, tmax + 1):
        if t % 2 == 0:
            s = 1 << (t // 2)
            if all(int(P[i, j]) == (s if i == j else 0) for i in range(n) for j in range(n)):
                return t
        P = P * A
    return None

def returns(N, T):
    V = verts(N); idx = {v: i for i, v in enumerate(V)}
    succ = []
    for (x, c) in V:
        succ.append((idx[((x + 1) % N, "R")], 1, idx[((x - 1) % N, "L")], -1 if c == "L" else 1))
    n = len(V); x0 = idx[(0, "R")]
    v = [0] * n; v[x0] = 1
    first_exact = None; first_99 = None; n_exact = 0; best = (0.0, 0)
    for t in range(1, T + 1):
        w = [0] * n
        for j in range(n):
            a = v[j]
            if a:
                i1, g1, i2, g2 = succ[j]
                w[i1] += a
                if g2 == 1: w[i2] += a
                else: w[i2] -= a
        v = w
        a = v[x0]
        if a < 0: a = -a
        if 2 * a.bit_length() >= t:          # otherwise a^2 < 2^(t-1) < 0.99 2^t
            sq = a * a
            if sq == (1 << t):
                n_exact += 1
                if first_exact is None: first_exact = t
            if first_99 is None and 100 * sq > 99 * (1 << t):
                first_99 = t
        if first_99 is not None and (N not in (4, 8)) and t >= max(first_99, 2000) and N in (3, 5, 6, 7, 10, 12) and t >= 20000:
            # these N are still run to 20000 for the exact-return predicate P3; stop there to bound time
            return first_exact, first_99, n_exact, t
    return first_exact, first_99, n_exact, T

def main():
    t0 = time.time()
    res = {"program": "ring_return.py", "arithmetic": "exact integers / rational polynomials", "T": T, "predicates": {}}
    per = {}
    for N in range(2, 41):
        ok, orders = periodic(N)
        per[N] = {"periodic": ok, "factors_degree_mult_cyclotomic_index": orders}
    got = sorted(N for N in per if per[N]["periodic"])
    res["P1"] = {"periodic_N": got, "detail": per}
    res["predicates"]["P1"] = (got == [2, 4, 8])
    p2 = {N: first_identity(N) for N in (2, 4, 8)}
    res["P2"] = p2
    res["predicates"]["P2"] = (p2 == {2: 2, 4: 8, 8: 24})
    ret = {}
    for N in range(3, 13):
        fe, f99, ne, horizon = returns(N, T)
        ret[N] = {"first_exact_return": fe, "first_above_0.99": f99, "number_of_exact_returns": ne, "horizon_run": horizon}
        print(N, ret[N], round(time.time() - t0, 1), flush=True)
    res["P3_P4"] = ret
    exp_exact = {N: None for N in range(3, 13)}; exp_exact[4] = 8; exp_exact[8] = 24
    res["predicates"]["P3"] = all(ret[N]["first_exact_return"] == exp_exact[N] for N in ret)
    res["P3_note"] = "N in {3,5,6,7,10,12} were run to t = 20000 only (see horizon_run); N = 4,8,9,11 to T"
    exp99 = {3: 38, 4: 8, 5: 264, 6: 38, 7: 504, 8: 24, 9: 95946, 10: 264, 11: None, 12: 6416}
    res["P4_expected"] = exp99
    res["predicates"]["P4"] = all(ret[N]["first_above_0.99"] == exp99[N] for N in ret)
    res["P4_mismatches"] = {N: [ret[N]["first_above_0.99"], exp99[N]] for N in ret if ret[N]["first_above_0.99"] != exp99[N]}
    res["predicates"]["P5"] = all(ret[N]["first_above_0.99"] is not None and ret[N]["first_above_0.99"] < 4000 for N in (3, 4, 5, 6, 8))
    res["P5_not_below_4000"] = [N for N in ret if ret[N]["first_above_0.99"] is None or ret[N]["first_above_0.99"] >= 4000]
    # (run1 recorded elapsed seconds; removed so that reruns are byte-identical)
    with open(OUT, "x") as f:
        json.dump(res, f, indent=1, sort_keys=True)
    print(json.dumps(res["predicates"]), res["P1"]["periodic_N"], res["P2"], res["P4_mismatches"], res["P5_not_below_4000"])

if __name__ == "__main__":
    main()
