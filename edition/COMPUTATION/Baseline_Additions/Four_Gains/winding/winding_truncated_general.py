"""Truncated consistency system on the ring of 3 sites with three winding classes (s = 3).

Carrier: N = 3, A = Z2 x Z9, a = (0,1), b = c = (0,0), d = (1,8); delta = (1,0), r = 2, B = (0,7),
beta = B^3 = (0,3), Delta_N = <delta, beta> of order 6, s = 3, H = A. Unknown: one real function f on
the classes, under translation by H, of the multisets of gains that occur at a vertex of a position
product event of length at most T (this uses F_R o T_h = F_R and F_L = F_R o T_c, which hold on the
multisets that occur; here c is trivial). Equations: the one-site equation for every pair (U, V)
that occurs at one site at a length below T. Arithmetic modulo the prime 1000003; the nullity
modulo a prime is at least the nullity over the rationals.

FOLLOW-UP of winding_truncated.py, whose predicate Q2 FAILED (result_truncated_T10.json, kept): its test
for "three different cosets of <delta>" reduced the second coordinate modulo 3, which is constant at a vertex;
the cosets of <delta> = Z2 x 0 are the nine values of the second coordinate. Only that test is changed here.
DISCLOSURE: an exploratory run of this same code (T = 7 and T = 10) preceded the wording of the
predicates below; they were not fixed before the first run.
PREDICATES for T = 10:
 Q1  the restriction of the solution space to the multisets first seen by length 6 has dimension 3
     (the count and the two squares |sigma_chi|^2 of Theorem thm:fgsolve for Delta_N).
 Q2  coverage: among the classes first seen by length 6 at least one has walks in three different
     cosets of <delta> (so that Q1 concerns multisets beyond two classes); the number is reported.
GENERAL variant (controls): ring of N sites, A = Z2 x Z_K, a = (0,1), b = c = 0, d = (1,-1); delta = (1,0),
B = (0,-2), beta = B^M. Exploratory; no predicate; the column classes_with_three_cosets counts classes with
three or more values of the second coordinate.
Usage: python3 winding_truncated_general.py T RESULT.json N K   (refuses to overwrite).
"""

import sys, collections, itertools
T=int(sys.argv[1]); OUT=sys.argv[2]; N=int(sys.argv[3]); K=int(sys.argv[4])
import os, json
assert not os.path.exists(OUT), "refusing to overwrite"
REP={"argv":sys.argv[1:],"N":N,"K":K,"prime":1000003,"restricted":[]}; P=1000003
A=[(i,j) for i in range(2) for j in range(K)]
def add(g,h): return ((g[0]+h[0])%2,(g[1]+h[1])%K)
a=(0,1%K); b=(0,0); c=(0,0); d=(1,(-1)%K)
masks=[frozenset(s) for k in range(1,N+1) for s in itertools.combinations(range(N),k)]
def step(field,mask):
    new=collections.Counter()
    for (x,r,g),n in field:
        y=(x+1)%N
        if y in mask: new[(y,0,add(g,a if r==0 else c))]+=n
        y=(x-1)%N
        if y in mask: new[(y,1,add(g,b if r==0 else d))]+=n
    return frozenset(new.items())
def canon(ms):  # ms: dict gain->count
    if not ms: return ()
    return min(tuple(sorted((add(g,h),n) for g,n in ms.items())) for h in A)
def tr(ms,h): return {add(g,h):n for g,n in ms.items()}
def plus(u,v):
    r=dict(u)
    for g,n in v.items(): r[g]=r.get(g,0)+n
    return r
level={frozenset({((0,0,(0,0)),1)})}; seen=set(level); idx={}; first={}; eqs=set()
def var(ms,t):
    k=canon(ms)
    if k==(): return None
    if k not in idx: idx[k]=len(idx); first[idx[k]]=t
    return idx[k]
var({(0,0):1},0)
for t in range(1,T+1):
    nxt=set()
    for f in level:
        for m in masks:
            g=step(f,m)
            if g and g not in seen: seen.add(g); nxt.add(g)
    level=nxt
    for f in level:
        by=collections.defaultdict(lambda:[{},{}])
        for (x,r,g),n in f: by[x][r][g]=n
        for x,(U,V) in by.items():
            vu=var(U,t); vv=var(V,t)
            if t<T:
                row=collections.Counter()
                for v,cf in ((var(plus(tr(U,a),tr(V,c)),t+1),1),(var(plus(tr(U,b),tr(V,d)),t+1),1),(vu,-2),(vv,-2)):
                    if v is not None: row[v]+=cf
                eqs.add(tuple(sorted((k,v) for k,v in row.items() if v)))
n=len(idx); REP["unknowns"]=n; REP["equations"]=len(eqs)
# sparse elimination mod P, pivot on the variable of latest first-time (eliminate late unknowns first)
order=sorted(range(n),key=lambda v:(-first[v],v)); rank_of={v:i for i,v in enumerate(order)}
piv={}
for e in eqs:
    row={k:v%P for k,v in e}
    while row:
        p=min(row,key=lambda k:rank_of[k])
        if p in piv:
            pr=piv[p]; f=row[p]
            for k,v in pr.items():
                nv=(row.get(k,0)-f*v)%P
                if nv: row[k]=nv
                else: row.pop(k,None)
        else:
            inv=pow(row[p],P-2,P); piv[p]={k:v*inv%P for k,v in row.items()}; break
REP["rank"]=len(piv); REP["nullity"]=n-len(piv)
keys={v:k for k,v in idx.items()}
for T0 in range(1,T+1):
    early=[v for v in range(n) if first[v]<=T0]
    # dimension of restriction of solution space to early = |early| - rank of equations supported in early after eliminating late vars
    # rows whose pivot is early involve only vars not earlier-in-order => only early vars (late eliminated first)
    r=sum(1 for p in piv if first[p]<=T0)
    three=sum(1 for v in early if len({g[1] for g,_ in keys[v]})>=3)
    REP["restricted"].append({"T0":T0,"classes":len(early),"classes_with_three_cosets":three,"solution_dim":len(early)-r})
if False:
    e6=REP["restricted"][5]; REP["predicates"]={"Q1":"PASS" if e6["solution_dim"]==3 else "FAIL","Q2":"PASS" if e6["classes_with_three_cosets"]>0 else "FAIL"}
json.dump(REP,open(OUT,"x"),indent=1,sort_keys=True); print(json.dumps(REP.get("predicates")), REP["restricted"])
