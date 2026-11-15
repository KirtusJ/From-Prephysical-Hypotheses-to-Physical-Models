#!/usr/bin/env python3
"""search_relations.py S SIGMA K B OUT      (no randomness; the enumeration is exhaustive in its box, so no seed is used)

Setting (draft subsection "total positivity of the winding, and products of multisets", thm:fgprod):
a product of k two-level factors has level-resolved signed sums pi(X) = prod_i (p_i + q_i X), (p_i,q_i) in Z^2,
and the rule is count + G(pi), G(pi) = sum_d c_d sum_i pi_i pi_{i+d}.  SIGMA = (-1)^{k_0}, S = number of classes.
A SIGN RELATION is a pair of such products with  cA*piA == eps * cB * X^j * piB  mod (X^S - SIGMA), eps = +-1,
cA,cB positive integers.  h0 = cA^2 |piA|^2 - cB^2 |piB|^2 as a polynomial in w = z + 1/z.
m(w) = squarefree part of C_S(w) - 2 SIGMA  (C_n(z+1/z) = z^n + z^-n): its roots are the w of the roots of X^S = SIGMA.

Box: all multisets of k <= K factors (p + qX), (p,q) primitive, |p|,|q| <= B, q != 0 (constants and the factor X are
covered by cA, cB and the shift j), first non-zero of (q,p) positive (sign covered by eps).

PREDICATES, fixed before the first run:
 P1  every relation reported is re-verified exactly: the remainder of cA*piA - eps*cB*X^j*piB on division by X^S - SIGMA is 0.
     (hypothesis check: counted per relation; a relation failing P1 is a bug and is kept in the file as FAILED.)
 P2  every h0 is divisible by m(w).  (Must hold by theory; a failure is kept.)
 P3  the gcd in Q[w] of all non-zero h0 found equals m(w) up to a constant.  (This is the question; either answer is a result.)
 P4  some single relation has h0 = const * m(w), const != 0 (one relation then suffices).  Either answer is a result.
Counts reported: products enumerated per k, classes with >= 2 different |pi|^2, relations with h0 != 0.
The result file OUT is opened with mode 'x' and is never overwritten.
"""
import sys, itertools, json
from math import gcd
from functools import reduce
import sympy as sp

S=int(sys.argv[1]); SIG=int(sys.argv[2]); K=int(sys.argv[3]); B=int(sys.argv[4]); OUT=sys.argv[5]
assert SIG in (1,-1) and S>=2
out=open(OUT,'x')
w=sp.symbols('w'); X=sp.symbols('X')

def cheb(n):
    a,b=sp.Integer(2),w
    if n==0: return a
    for _ in range(n-1): a,b=b,sp.expand(w*b-a)
    return b
CH=[cheb(n) for n in range(0,6*K+S+5)]
mfull=sp.expand(CH[S]-2*SIG)
m=sp.Poly(mfull,w); m=sp.Poly(sp.prod([f for f,_ in sp.factor_list(mfull)[1]]),w).monic()

def polymul(a,b):
    r=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b): r[i+j]+=x*y
    return r
def fold(a):
    r=[0]*S
    for i,x in enumerate(a):
        r[i%S]+=x*(SIG**(i//S))
    return r
def shifts(r):
    # all eps * X^j * r mod X^S - SIG, j=0..S-1, eps=+-1
    res=[]
    cur=list(r)
    for j in range(S):
        res.append((j,1,tuple(cur))); res.append((j,-1,tuple(-x for x in cur)))
        cur=[SIG*cur[-1]]+cur[:-1]
    return res
def canon(r):
    g=reduce(gcd,[abs(x) for x in r])
    if g==0: return None,0
    r=[x//g for x in r]
    return max(t for _,_,t in shifts(r)), g
def autocorr(a):
    n=len(a)
    return tuple(sum(a[i]*a[i+d] for i in range(n-d)) for d in range(n))
def hpoly(ac):
    return sp.expand(sum(ac[d]*(CH[d] if d else 1) for d in range(len(ac))))

facs=[]
for q in range(0,B+1):
    for p in range(-B,B+1):
        if q==0: continue
        if gcd(abs(p),q)!=1: continue
        facs.append((p,q))
classes={}
nprod={}
for k in range(1,K+1):
    cnt=0
    for combo in itertools.combinations_with_replacement(range(len(facs)),k):
        pi=[1]
        for i in combo: pi=polymul(pi,list(facs[i]))
        c,g=canon(fold(pi))
        cnt+=1
        if c is None: continue
        classes.setdefault(c,[]).append((tuple(facs[i] for i in combo),g))
    nprod[k]=cnt
log={'argv':sys.argv,'S':S,'sigma':SIG,'K':K,'B':B,'m':str(m.as_expr()),'deg_m':m.degree(),'products_per_k':nprod,
     'classes':len(classes)}
rels=[]; G=None; single=[]; p1fail=0; p2fail=0; nclass2=0
for c,lst in classes.items():
    if len(lst)<2: continue
    # normalised |pi|^2 / g^2 as key
    seen={}
    for fl,g in lst:
        pi=[1]
        for f in fl: pi=polymul(pi,list(f))
        ac=autocorr(pi)
        # scaled: compare ac/g^2 -> use cross-multiplication key via Fraction tuple
        key=tuple(sp.Rational(x,g*g) for x in ac if True)
        key=tuple(list(key)+[0]*(K+1-len(key)))
        seen.setdefault(key,(fl,g,pi))
    if len(seen)<2: continue
    nclass2+=1
    items=list(seen.values())
    fa,ga,pa=items[0]
    for fb,gb,pb in items[1:]:
        # cA*pa == eps*cB*X^j*pb : cA=gb/gg, cB=ga/gg
        gg=gcd(ga,gb); cA=gb//gg; cB=ga//gg
        ra=[cA*x for x in fold(pa)]; found=None
        for j,eps,t in shifts([cB*x for x in fold(pb)]):
            if list(t)==ra: found=(j,eps); break
        ok1=False
        if found:
            j,eps=found
            PA=sp.Poly(sum(cA*x*X**i for i,x in enumerate(pa)),X)
            PB=sp.Poly(sum(eps*cB*x*X**(i+j) for i,x in enumerate(pb)),X)
            ok1=(sp.rem(PA-PB,sp.Poly(X**S-SIG,X))).is_zero
        if not ok1: p1fail+=1
        h0=sp.expand(cA*cA*hpoly(autocorr(pa))-cB*cB*hpoly(autocorr(pb)))
        H=sp.Poly(h0,w)
        ok2=sp.rem(H,m).is_zero
        if not ok2: p2fail+=1
        if H.is_zero: continue
        G=H if G is None else sp.gcd(G,H)
        one=(H.degree()==m.degree())
        rec={'A':fa,'cA':cA,'B':fb,'cB':cB,'j':found[0] if found else None,'eps':found[1] if found else None,
             'P1':ok1,'P2':ok2,'h0':str(h0),'deg_h0':H.degree(),'single_suffices':one}
        rels.append(rec)
        if one: single.append(rec)
log['classes_with_two_different_abs2']=nclass2
log['relations_h0_nonzero']=len(rels)
log['P1_failures']=p1fail; log['P2_failures']=p2fail
if G is not None:
    Gm=G.monic(); log['gcd_h0']=str(Gm.as_expr()); log['P3_gcd_equals_m']=bool(Gm==m)
    log['gcd_over_m']=str(sp.factor(sp.div(Gm,m)[0].as_expr()))
else:
    log['gcd_h0']=None; log['P3_gcd_equals_m']=False
log['P4_single_relation_suffices']=len(single)>0
rels.sort(key=lambda r:(r['deg_h0'],len(r['A'])+len(r['B']),max(abs(x) for f in r['A']+r['B'] for x in f)))
log['first_single']=single[:3] if single else []
log['smallest_relations']=rels[:12]
json.dump(log,out,indent=1,default=str); out.write('\n'); out.close()
print(json.dumps({k:v for k,v in log.items() if k not in('smallest_relations','first_single')},default=str))
