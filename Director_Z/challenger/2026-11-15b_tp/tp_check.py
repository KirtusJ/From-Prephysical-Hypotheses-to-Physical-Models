#!/usr/bin/env python3
"""Challenger check of thm:tp and cor:tp (G10 draft subsection on winding products).

Usage: python3 tp_check.py OUTFILE NMIN NMAX TMAX CAP

Setting (from the draft): ring Z_N, walks from site 0, step R: x->x+1, step L: x->x-1,
lambda = number of L steps. A position product event of length T has masks A_1..A_T.
The state after s steps is the multiset of (site, lambda) of surviving walks; it determines
the future. We explore all states reachable with arbitrary masks, keeping only states in
which every site carries at most CAP walks (BOUND: states exceeding CAP are dropped, so
events whose intermediate totals exceed CAP are not seen), up to T-1 = TMAX-1 steps; then
for the last step every site x is taken as the end site (A_T = {x}).
At the end site x: u_j = #walks ending at (x,R) with lambda = l0 + jM, v_j likewise at (x,L),
l0 = least lambda at x (all lambda at x are congruent mod M; checked as predicate P0),
w_{2j} = v_j, w_{2j+1} = u_j, M = N/gcd(N,2).

PREDICATES, fixed before the first run:
P0 (hypothesis/setting): all lambda at x congruent mod M.  Instances = (N, state, x) with
   at least one walk ending at x; distinct w-sequences deduplicated per N.
P1 all minors of order 1,2,3 of the array (w_{c-2i}) on a window that covers every nonzero
   entry pattern (rows 0..D, columns kmin-1 .. kmax+2D+1, D = span/2 + 2) are >= 0 (exact ints).
P2 u and v are each zero or have only real roots, none positive (exact: sympy count_roots
   of the polynomial with X^min divided out, real-root count == degree; positive-root count 0).
P3 interlacing form of cor:tp(iii) when u != 0 != v: with g = gcd(u,v), roots of u/g and
   v/g real, simple, non-positive, and in decreasing order they alternate beginning with v/g.
P4 W(Y) = v(Y^2) + Y u(Y^2) has no root with positive real part: reported as the maximum
   real part over roots computed by mpmath polyroots at 60 digits (a measured value; no
   threshold is used to decide, the value is printed); also exact Routh-free check: none.
P5 (gcd condition, extra): g has only real non-positive roots.
Hypothesis count per predicate is printed. Failures are written, never suppressed.
The result file is opened with mode 'x' and is never overwritten.
"""
import sys, itertools
from math import gcd
import sympy as sp
import mpmath as mp

X = sp.Symbol('X')

def det(m):
    n = len(m)
    if n == 1: return m[0][0]
    if n == 2: return m[0][0]*m[1][1]-m[0][1]*m[1][0]
    a,b,c = m[0]; d,e,f = m[1]; g,h,i = m[2]
    return a*(e*i-f*h)-b*(d*i-f*g)+c*(d*h-e*g)

def explore(N, TMAX, CAP):
    start = ((0, 0, 1),)  # (site, lambda, count) after 0 steps, lambda normalised min 0
    seen = {start}
    layer = {start}
    allstates = [start]
    for s in range(1, TMAX):  # states after s steps, s <= TMAX-1
        new = set()
        for st in layer:
            nxt = {}
            for (y, l, c) in st:
                nxt[((y+1) % N, l)] = nxt.get(((y+1) % N, l), 0) + c
                nxt[((y-1) % N, l+1)] = nxt.get(((y-1) % N, l+1), 0) + c
            sites = sorted({k[0] for k in nxt})
            for r in range(1, len(sites)+1):
                for keep in itertools.combinations(sites, r):
                    ks = set(keep)
                    items = [(y, l, c) for (y, l), c in nxt.items() if y in ks]
                    tot = {}
                    for y, l, c in items: tot[y] = tot.get(y, 0) + c
                    if max(tot.values()) > CAP: continue
                    m = min(l for _, l, _ in items)
                    key = tuple(sorted((y, l-m, c) for y, l, c in items))
                    if key not in seen:
                        seen.add(key); new.add(key); allstates.append(key)
        layer = new
    return allstates

def endsite(st, N, x):
    R, L = {}, {}
    for (y, l, c) in st:
        if (y+1) % N == x: R[l] = R.get(l, 0) + c
        if (y-1) % N == x: L[l+1] = L.get(l+1, 0) + c
    return R, L

def realroots_ok(coeffs):
    """coeffs low->high, nonneg ints. Return (zero, ok)."""
    if all(c == 0 for c in coeffs): return True
    while coeffs[0] == 0: coeffs = coeffs[1:]
    p = sp.Poly(list(reversed(coeffs)), X)
    d = p.degree()
    if d == 0: return True
    rr = sp.real_roots(p)  # with multiplicity (v1 used count_roots, which counts distinct roots: bug)
    return len(rr) == d and all(r <= 0 for r in rr)

def main():
    out, NMIN, NMAX, TMAX, CAP = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    f = open(out, 'x')
    def P(*a):
        s = ' '.join(str(t) for t in a); print(s); f.write(s+'\n'); f.flush()
    P('cmd', ' '.join(sys.argv))
    mp.mp.dps = 60
    for N in range(NMIN, NMAX+1):
        M = N // gcd(N, 2)
        states = explore(N, TMAX, CAP)
        cnt = dict(inst=0, p0fail=0, seqs=0, p1m=0, p1fail=0, p2n=0, p2fail=0, p3n=0, p3fail=0,
                   p4n=0, p5fail=0)
        maxre = -mp.inf
        seqs = set()
        for st in states:
            for x in range(N):
                R, L = endsite(st, N, x)
                lams = list(R) + list(L)
                if not lams: continue
                cnt['inst'] += 1
                l0 = min(lams)
                if any((l - l0) % M for l in lams):
                    cnt['p0fail'] += 1; P('P0 FAIL', N, st, x); continue
                J = max(lams)
                jmax = (J - l0)//M
                u = [R.get(l0 + j*M, 0) for j in range(jmax+1)]
                v = [L.get(l0 + j*M, 0) for j in range(jmax+1)]
                seqs.add((tuple(u), tuple(v)))
        cnt['seqs'] = len(seqs)
        for (u, v) in sorted(seqs):
            u = list(u); v = list(v)
            w = {}
            for j in range(len(u)):
                w[2*j] = v[j]; w[2*j+1] = u[j]
            kmin, kmax = 0, 2*len(u)-1
            D = (kmax-kmin)//2 + 2
            rows = list(range(0, D+1))
            cols = list(range(kmin-1, kmax+2*D+2))
            A = lambda i, c: w.get(c-2*i, 0)
            bad = None
            for k in (1, 2, 3):
                for ri in itertools.combinations(rows, k):
                    if ri[0] != 0: continue  # row shift by 1 = column shift by 2 (window covers)
                    for ci in itertools.combinations(cols, k):
                        dv = det([[A(i, c) for c in ci] for i in ri])
                        cnt['p1m'] += 1
                        if dv < 0 and bad is None: bad = (ri, ci, dv)
            if bad: cnt['p1fail'] += 1; P('P1 FAIL', N, 'u', u, 'v', v, bad)
            for poly in (u, v):
                cnt['p2n'] += 1
                if not realroots_ok(list(poly)):
                    cnt['p2fail'] += 1; P('P2 FAIL', N, 'u', u, 'v', v, 'poly', poly)
            # P3, P5
            if any(u) and any(v):
                cnt['p3n'] += 1
                pu = sp.Poly(list(reversed(u)), X); pv = sp.Poly(list(reversed(v)), X)
                g = sp.gcd(pu, pv)
                qu = sp.quo(pu, g); qv = sp.quo(pv, g)
                ok = True; roots = []
                for q, tag in ((qu, 'u'), (qv, 'v')):
                    d = q.degree()
                    if d > 0:
                        if sp.gcd(q, q.diff(X)).degree() > 0 or q.count_roots(-sp.oo, 0) != d:
                            ok = False
                        roots += [(sp.N(r, 50), tag) for r in sp.real_roots(q)]
                if ok:
                    roots.sort(key=lambda t: -t[0])
                    tags = [t for _, t in roots]
                    if tags and tags[0] != 'v': ok = False
                    if any(tags[i] == tags[i+1] for i in range(len(tags)-1)): ok = False
                if not ok: cnt['p3fail'] += 1; P('P3 FAIL', N, 'u', u, 'v', v, 'g', g.as_expr())
                if g.degree() > 0 and not (len(sp.real_roots(g)) == g.degree() and all(r <= 0 for r in sp.real_roots(g))):
                    cnt['p5fail'] += 1; P('P5 FAIL', N, 'u', u, 'v', v, 'g', g.as_expr())
            # P4
            coeffs = [w.get(k, 0) for k in range(kmax+1)]
            while coeffs and coeffs[-1] == 0: coeffs.pop()
            lo = 0
            while coeffs[lo] == 0: lo += 1
            cz = coeffs[lo:]
            if len(cz) > 1:
                cnt['p4n'] += 1
                PW = sp.Poly(list(reversed(cz)), X)
                mr = -mp.inf
                for fac, _e in sp.factor_list(PW)[1]:  # irreducible factors: simple roots, converges
                    if fac.degree() == 0: continue
                    for r in fac.nroots(n=40, maxsteps=500):
                        mr = max(mr, mp.mpf(str(sp.re(r))))
                if mr > maxre: maxre = mr
        P('N', N, 'M', M, 'states', len(states), cnt, 'P4 max Re root of W (zero roots removed):', mp.nstr(maxre, 8))
    f.close()

if __name__ == '__main__':
    main()
