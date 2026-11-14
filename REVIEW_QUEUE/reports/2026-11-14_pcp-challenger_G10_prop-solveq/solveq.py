"""Challenger program for G10 Prop 5.35 (prop:solveq). Exact arithmetic only.

Unknowns: F_R(m), F_L(m) for m in N^C, 1 <= |m| <= B (F(0)=0 imposed).
Equations: F_R(U+V)+F_L(U+TV)-2F_R(U)-2F_L(V)=0 for ALL (U,V) with |U|+|V|<=B,
(Tm)[j]=m[j-1 mod q].  Interior I_r = unknowns with |m|<=r.  The dimension of the
solution space restricted (projected) to I_r is |I_r| - #(echelon pivots of
degree <= r), with columns eliminated in order of DEcreasing |m| (so the rows
with pivot of degree <= r span exactly the consequences that involve I_r only).
d(q)=1 for q odd, 2 for q even.

PREDICATES (fixed before first run):
 H  (hypothesis, per instance): number of equations == C(B+2q,2q) (every pair
    in the box present); T1=1; |Tm|=|m| for all m in box; q even: eps(Tm)=-eps(m).
 C  (converse): |m| (and eps^2 for q even), with F_R=F_L, satisfy every box
    equation exactly; their restrictions to I_r have rank d(q) for r=floor(B/2).
 P1 projected dimension on I_r, r=floor(B/2), equals d(q).  (B>=4.)
 P2 projected dimension on the whole box (r=B) equals d(q).  [expected by me to
    be at risk: edge unknowns]
 P3 the projected dimension on I_r, r=floor(B/2), is the same for the two box
    sizes run for each q.
Field: Fraction (exact, Q) unless 'modp' given (GF(2^61-1): then rank is only a
lower bound for the rational rank, and it is labelled so).
"""
import sys, time, json
from fractions import Fraction
from itertools import combinations_with_replacement
from math import comb

def msets(q, B):
    out = []
    for n in range(0, B+1):
        for c in combinations_with_replacement(range(q), n):
            m = [0]*q
            for j in c: m[j] += 1
            out.append(tuple(m))
    return out
def T(m): return m[-1:]+m[:-1]
def add(a, b): return tuple(x+y for x, y in zip(a, b))
def eps(m): return sum((-1)**j*m[j] for j in range(len(m)))

def run(q, B, modp):
    t0 = time.time(); P = (1 << 61)-1
    ms = msets(q, B); deg = {m: sum(m) for m in ms}
    bydeg = {}
    for m in ms: bydeg.setdefault(deg[m], []).append(m)
    # column order: decreasing degree; index = (m, side)
    cols = [(m, s) for m in sorted(ms, key=lambda m: -deg[m]) if deg[m] > 0 for s in 'RL']
    idx = {c: i for i, c in enumerate(cols)}
    cdeg = [deg[c[0]] for c in cols]
    H = True
    one = tuple([1]*q); H &= (T(one) == one)
    for m in ms:
        H &= (sum(T(m)) == sum(m))
        if q % 2 == 0: H &= (eps(T(m)) == -eps(m))
    sols = [lambda m: sum(m)] + ([lambda m: eps(m)**2] if q % 2 == 0 else [])
    d = len(sols)
    piv = {}; neq = 0; Cok = True
    for a in range(0, B+1):
        for b in range(0, B-a+1):
            for U in bydeg[a]:
                for V in bydeg[b]:
                    neq += 1
                    for f in sols:
                        Cok &= (f(add(U, V))+f(add(U, T(V))) == 2*f(U)+2*f(V))
                    row = {}
                    for m, s, c in ((add(U, V), 'R', 1), (add(U, T(V)), 'L', 1), (U, 'R', -2), (V, 'L', -2)):
                        if deg[m] == 0: continue
                        i = idx[(m, s)]; row[i] = row.get(i, 0)+c
                    row = {i: (v % P if modp else Fraction(v)) for i, v in row.items() if v != 0}
                    while row:
                        i = min(row)
                        if i not in piv:
                            v = row[i]
                            if modp:
                                inv = pow(v, P-2, P); row = {k: x*inv % P for k, x in row.items()}
                            else:
                                row = {k: x/v for k, x in row.items()}
                            piv[i] = row; break
                        pr = piv[i]; v = row[i]
                        for k, x in pr.items():
                            y = row.get(k, 0)-v*x
                            if modp: y %= P
                            if y == 0: row.pop(k, None)
                            else: row[k] = y
                    if time.time()-t0 > 170: return dict(q=q, B=B, aborted='time>170s')
    H &= (neq == comb(B+2*q, 2*q))
    rank = len(piv); n = len(cols)
    proj = {}
    for r in range(1, B+1):
        nI = sum(1 for x in cdeg if x <= r)
        pI = sum(1 for i in piv if cdeg[i] <= r)
        proj[r] = nI-pI
    r0 = B//2
    # rank of candidate solutions on I_r0 (exact, tiny)
    vecs = [[Fraction(f(m)) for m in ms if 0 < deg[m] <= r0] for f in sols]
    if d == 1: srank = int(any(vecs[0]))
    else:
        srank = 0
        if any(vecs[0]):
            srank = 1
            j = next(k for k, x in enumerate(vecs[0]) if x); t = vecs[1][j]/vecs[0][j]
            if any(y-t*x for x, y in zip(vecs[0], vecs[1])): srank = 2
    return dict(q=q, B=B, field='GF(2^61-1) (rank is lower bound for Q)' if modp else 'Q',
                unknowns=n, equations=neq, rank=rank, nullity_whole_box=n-rank, d_claimed=d,
                proj_dim_by_r=proj, r0=r0, H=bool(H), C=bool(Cok and srank == d),
                P1=(proj[r0] == d), P2=(proj[B] == d), seconds=round(time.time()-t0, 1))

if __name__ == '__main__':
    q, B = int(sys.argv[1]), int(sys.argv[2]); modp = len(sys.argv) > 3
    res = run(q, B, modp)
    with open('result_q%d_B%d%s.json' % (q, B, '_modp' if modp else ''), 'x') as f:
        json.dump(res, f, indent=1)
    print(json.dumps(res))
