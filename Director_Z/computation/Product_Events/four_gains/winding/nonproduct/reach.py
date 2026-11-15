#!/usr/bin/env python3
"""Which three-coset multisets have their rule value forced by coincidences m*P = g*(Q1*Q2)?
Usage: python3 -B reach.py OUT.json MAXM MAXP MAXQ   (OUT opened with mode 'x'; no randomness)

Group C2 x C3 (delta of order 2, beta of order 3, trivial twist: s = 3, r = 2, sigma = +1); cosets C_i = beta^i <delta>.
For a multiset m meeting all three cosets, size <= MAXM, and two-coset factors P in M(C0 u C1), size <= MAXP, test
whether some g in the group and Q1, Q2 in M(C0 u C1) (sizes <= MAXQ) give g*m*P = Q1*Q2. Each success gives one row
(|P|, p0^2+p1^2, p0 p1), p = (eps0(P), eps1(P)), of the linear system for (alpha_m, q_m, c_m) in Theorem 5.70's clause
for a fixed multiset m.
PREDICATES (fixed before the first run):
 R0 control: Session B's m_e = 1 + b + 2db + db^2 has row rank 3 (B's three factors are found).
 R1 (reported, no claim): for each m up to translation and delta-swap... no symmetry reduction is used; the number of m
    with rank 3, rank < 3, and the list of rank < 3 cases.
 R2 (claimed): whenever rank 3, the forced value F(m) = alpha_m + q_m + c_m * 0 ... (computed: F(m) = alpha_m + q_m*s(1,0) ...)
    is checked against count + q(sum eps_j^2) + c(eps0 eps1 + eps1 eps2 + eps2 eps0) with symbolic alpha, q, c:
    the system is solved exactly and F(m) = alpha_m*1 + q_m*(1^2+0^2) + c_m*0 (P = e_1) compared.
Hypothesis counted: the number of m meeting three cosets; occurrence on a ring is NOT tested (see note in output).
"""
import sys, json, itertools
from fractions import Fraction as Fr
OUT, MAXM, MAXP, MAXQ = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
fout = open(OUT, 'x')
G = [(i, j) for i in range(2) for j in range(3)]
def mul(A, B):
    R = {}
    for a, x in A.items():
        for b, y in B.items():
            k = ((a[0]+b[0]) % 2, (a[1]+b[1]) % 3); R[k] = R.get(k, 0) + x*y
    return R
def key(A): return tuple(sorted((k, v) for k, v in A.items() if v))
def multisets(elems, n):
    for size in range(1, n+1):
        for comb in itertools.combinations_with_replacement(elems, size):
            d = {}
            for e in comb: d[e] = d.get(e, 0) + 1
            yield d
two = [e for e in G if e[1] in (0, 1)]
Qs = list(multisets(two, MAXQ))
prod = {}
for i, a in enumerate(Qs):
    for b in Qs[i:]:
        prod.setdefault(key(mul(a, b)), (a, b))
def eps(A, j): return sum(v * (-1)**k[0] for k, v in A.items() if k[1] == j)
def val(A, al, q, c):  # count + squares rule, s = 3, sigma = +1
    e = [eps(A, j) for j in range(3)]
    return al*sum(A.values()) + q*sum(x*x for x in e) + c*(e[0]*e[1] + e[1]*e[2] + e[2]*e[0])
Ps = list(multisets(two, MAXP))
res = {"command": " ".join(sys.argv), "rank3": 0, "rank_lt3": [], "R2_fail": [], "n_m": 0}
import sympy as sp
al, q, c = sp.symbols('al q c')
for m in multisets(G, MAXM):
    if len({k[1] for k in m}) < 3: continue
    res["n_m"] += 1
    rows = []; rhs = []
    for P in Ps:
        mp = mul(m, P)
        for g in G:
            k = key(mul({g: 1}, mp))
            if k in prod:
                Q1, Q2 = prod[k]
                p0, p1 = eps(P, 0), eps(P, 1)
                rows.append([sum(P.values()), p0*p0 + p1*p1, p0*p1])
                rhs.append(val(dict(k), al, q, c)); break
    M_ = sp.Matrix(rows) if rows else sp.zeros(0, 3)
    rk = M_.rank() if rows else 0
    mk = [[list(k), v] for k, v in key(m)]
    if rk < 3: res["rank_lt3"].append([mk, rk, len(rows)]); continue
    res["rank3"] += 1
    sol = sp.linsolve((M_, sp.Matrix(rhs)), sp.symbols('A Qm Cm'))
    (A_, Q_, C_), = list(sol)
    forced = sp.simplify(A_ + Q_*(eps(m,0)**0) - Q_ + val(m, al, q, c) - val(m, al, q, c))  # placeholder
    Fm = A_ + Q_  # P = e_1: |P| = 1, p = (1, 0)
    if sp.simplify(Fm - val(m, al, q, c)) != 0: res["R2_fail"].append(mk)
ctrl = {((0,0)):1, (0,1):1, (1,1):2, (1,2):1}
res["R0_control_rank3"] = not any(r[0] == [[list(k), v] for k, v in key(ctrl)] for r in res["rank_lt3"])
res["note"] = "occurrence on a ring is not tested; rank 3 forces F(m) only for m that occur alone on R (Lemma 5.66 and 5.59)."
json.dump(res, fout, indent=1); fout.close()
print({k: (v if not isinstance(v, list) else len(v)) for k, v in res.items()})
