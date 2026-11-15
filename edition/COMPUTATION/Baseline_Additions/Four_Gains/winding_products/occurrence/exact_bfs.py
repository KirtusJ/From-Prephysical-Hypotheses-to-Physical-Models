"""Exact forward search, position product events without gains on Z_N, M = N/gcd(N,2).
Model (proved in PROOFS.md, Lemma 1): configuration n: Z -> N (walks of length t by lambda), start delta_0,
tick n' = 1_{B+MZ} (n + shift n), B any subset of Z_M. Profile at a site = restriction of n to two adjacent
classes rho-1, rho, listed w_{2j}=n(rho-1+jM), w_{2j+1}=n(rho+jM), shifted by an even amount so that the first
nonzero entry has index 0 or 1, trailing zeros removed.
Search: all configurations (up to translation) with total <= CAP and support width <= W reachable through such
configurations. Completeness in CAP is Lemma 2 (trimming); completeness in W is NOT proved: stabilisation in W is
reported (COMPUTED only).
Predicates fixed before the first run:
 H  (hypothesis, per target): target satisfies cor:tp (ii),(iii) (exact real roots, interlacing) -- reported.
 C  (control): (1,2,1) and (1,3,3,1)... (1,2,1) is found for every M run.  Expected TRUE.
 P1 for each M, W: targets (1,2,3,3,2), (2,3,3,2,1), (1,2,3,5,1) are not found.  Reported TRUE/FALSE.
 P2 profile set (total <= CAP) identical for the two largest W at each M (stabilisation).  Reported.
Usage: python3 exact_bfs.py CAP M1,M2,.. W-multipliers(comma) OUTFILE   (seed 20261113; no randomness used)"""
import sys, random
random.seed(20261113)
CAP=int(sys.argv[1]); Ms=[int(x) for x in sys.argv[2].split(',')]; Wm=[int(x) for x in sys.argv[3].split(',')]
out=open(sys.argv[4],'x')
TARGETS=[(1,2,3,3,2),(2,3,3,2,1),(1,2,3,5,1)]
CONTROL=(1,2,1)
def strip(m):
    i=0
    while i<len(m) and m[i]==0: i+=1
    j=len(m)
    while j>i and m[j-1]==0: j-=1
    return tuple(m[i:j])
def profiles(n,M):
    res=set()
    for rho in range(M):
        d={}
        for p,c in enumerate(n):
            if c==0: continue
            if (p-(rho-1))%M==0: d[2*((p-(rho-1))//M)]=c
            elif (p-rho)%M==0 and M>1: d[2*((p-rho)//M)+1]=c
        if not d: continue
        lo=min(d); lo-=lo%2; hi=max(d)
        res.add(tuple(d.get(i,0) for i in range(lo,hi+1)))
    return res
def search(M,W):
    start=(1,); seen={start}; front=[start]
    while front:
        nf=[]
        for n in front:
            m=[0]*(len(n)+1)
            for p,c in enumerate(n): m[p]+=c; m[p+1]+=c
            res=sorted({p%M for p,c in enumerate(m) if c})
            for mask in range(1,1<<len(res)):
                B={res[i] for i in range(len(res)) if mask>>i&1}
                s=strip([c if p%M in B else 0 for p,c in enumerate(m)])
                if sum(s)<=CAP and len(s)<=W and s not in seen:
                    seen.add(s); nf.append(s)
        front=nf
    prof=set()
    for n in seen: prof|=profiles(n,M)
    return seen,prof
# hypothesis test
import sympy as sp
Y=sp.symbols('Y')
def tp_ok(w):
    v=[w[i] for i in range(0,len(w),2)]; u=[w[i] for i in range(1,len(w),2)]
    U=sum(c*Y**j for j,c in enumerate(u)); V=sum(c*Y**j for j,c in enumerate(v))
    Wp=sp.Poly(sp.expand(V.subs(Y,Y**2)+Y*U.subs(Y,Y**2)),Y)
    roots=Wp.nroots(n=50,maxsteps=2000)
    ok=all(sp.re(r)<=sp.Rational(1,10**30) for r in roots)
    realu=all(abs(sp.im(r))<1e-30 and sp.re(r)<=0 for r in sp.Poly(U,Y).nroots(n=50,maxsteps=2000)) if U!=0 else True
    realv=all(abs(sp.im(r))<1e-30 and sp.re(r)<=0 for r in sp.Poly(V,Y).nroots(n=50,maxsteps=2000)) if V!=0 else True
    return ok and realu and realv
for t in TARGETS+[CONTROL]: print('H',t,'cor:tp(ii,iii) numerically (50 digits):',tp_ok(t),file=out,flush=True)
for M in Ms:
    last=None
    for k in Wm:
        W=k*M
        seen,prof=search(M,W)
        print(f'M={M} W={W} states={len(seen)} profiles={len(prof)} C={CONTROL in prof} '+
              ' '.join(f'{t}:{"FOUND" if t in prof else "absent"}' for t in TARGETS),file=out,flush=True)
        if last is not None: print(f'  P2 M={M} profiles equal to previous W: {prof==last}',file=out,flush=True)
        last=prof
    print('PROFILES',M,sorted(last),file=out,flush=True)
