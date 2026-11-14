"""Challenger program B and C for THEOREM_T (own program; predicates fixed before first run). Exact arithmetic.

Walks from (0,R); move '+' goes to (x+1,R), gain unchanged; move '-' goes to (x-1,L), gain flips iff current vertex is L.
Ext S = all one-step continuations of walks of S, computed by enumerating walks (not by the lemma's formula).

PREDICATES
 B1 (rings N=3..8; also N=1,2 reported): for the four-equation subsystem of (iii) at fixed m with Jm != m, written L v = k v
    (v = (A_x,A'_x,B_x,B'_x)_x, L a 0/1 matrix), every column sum of L is 2 (exact). Consequence: sum(v)(2-k)=0.
 B2: exact characteristic polynomial of L (sympy); list of real roots; k=2 is a root and the constant vector is an eigenvector.
 B3: for every real eigenvalue k != 2 (numerical, numpy), every vector of a basis of ker(L-k) has entry sum 0 up to
    1e-9 (basis: double precision times conditioning; the smallest |sum| among k=2 vectors is reported for separation),
    hence no non-negative non-zero eigenvector. Measured.
 B4: same B1 for the subsystem with Jm = m (v=(A_x,B_x)).
 C-a1: line, F_y=x(p+q): mu(Ext S)=2 mu(S) for all events T<=4 (all subsets), and samples T=5,6.
 C-a2: line, F_(x,R)=(p-q)lam^x, F_(x,L)=(p-q)lam^(x-1), lam=(1+sqrt5)/2 and (1-sqrt5)/2, in Z[lam]: same.
 C-a3: neither a1 nor a2 is bounded below in x at m=(1,0) or (0,1) (checked on |x|<=40: values strictly decreasing along a direction, measured) and neither is of the form a(p+q)+c(p-q)^2 (value depends on x).
 C-b: line, F_y=lam^x(p+q), lam=2 and 1/3: mu(Ext S)=(lam+1/lam) mu(S), same event sets.
 C-c: F_R=p-q, F_L=(sqrt2-1)(p-q) in Z[sqrt2]: (E0) with factor sqrt2 for all U,V in [0..6]^2; and mu(Ext S)=sqrt2 mu(S) on the same event sets (stronger than claimed).
 C-iv: rings N=1..6 and line, all events (all subsets of the walks of length T) T=0..4: mu(Ext S)=2mu(S) for (a,c)=(1,0) and (0,1).
 Samples for T=5,6: 20000 random subsets and 20000 random position product events each, seed 20261114.
Result file resultBC.txt, mode 'x'.
"""
import itertools, random
from fractions import Fraction as Fr
import numpy as np, sympy as sp
out=open('resultBC.txt','x')
def W_(s):
    print(s); out.write(s+'\n'); out.flush()
cnt={'met':0,'failed':0,'measured':0}
def verdict(name,ok,extra='',measured=False):
    cnt['measured' if measured else ('met' if ok else 'failed')]+=1
    W_(f'{name}: {"MEASURED " if measured else ""}{"MET" if ok else "FAILED"} {extra}')
# ---------- B
for N in range(1,9):
    n=4*N; ix=lambda t,x:4*(x%N)+t  # t:0 A,1 A',2 B,3 B'
    L=sp.zeros(n,n)
    for x in range(N):
        L[ix(0,x),ix(0,x+1)]+=1; L[ix(0,x),ix(2,x-1)]+=1
        L[ix(1,x),ix(1,x+1)]+=1; L[ix(1,x),ix(3,x-1)]+=1
        L[ix(2,x),ix(0,x+1)]+=1; L[ix(2,x),ix(3,x-1)]+=1
        L[ix(3,x),ix(1,x+1)]+=1; L[ix(3,x),ix(2,x-1)]+=1
    cs=[sum(L[:,j]) for j in range(n)]
    verdict(f'B1 N={N}',all(c==2 for c in cs),f'column sums {set(cs)}')
    lam=sp.symbols('k'); cp=sp.factor(L.charpoly(lam).as_expr())
    one=sp.ones(n,1)
    reals=sorted(set(sp.real_roots(sp.Poly(L.charpoly(lam).as_expr(),lam))),key=lambda r:float(r))
    verdict(f'B2 N={N}',(L*one==2*one) and 2 in reals,f'charpoly {cp}; real roots {[sp.nsimplify(r) if r.is_rational else round(float(r),6) for r in reals]}')
    Ln=np.array(L.tolist(),dtype=float)
    worst=0.0; sep=None
    for r in reals:
        k=float(r)
        u,s,vt=np.linalg.svd(Ln-k*np.eye(n))
        basis=vt[s<1e-9]
        sums=[abs(b.sum()) for b in basis]
        if abs(k-2)<1e-12: sep=max(sums) if sums else None
        else: worst=max([worst]+sums)
    verdict(f'B3 N={N}',worst<1e-9,f'max |entry sum| over eigenvectors with real k!=2: {worst:.2e}; at k=2: {sep}',measured=True)
    n2=2*N; L2=sp.zeros(n2,n2); j=lambda t,x:2*(x%N)+t
    for x in range(N):
        for t in (0,1):
            L2[j(t,x),j(0,x+1)]+=1; L2[j(t,x),j(1,x-1)]+=1
    cs=[sum(L2[:,c]) for c in range(n2)]
    verdict(f'B4 N={N}',all(c==2 for c in cs),f'column sums {set(cs)}')
# ---------- quadratic ring Z[w], w^2 = u*w+v, coefficients Fractions
class Q:
    def __init__(s,a,b,u,v): s.a,s.b,s.u,s.v=Fr(a),Fr(b),u,v
    def __add__(s,o):
        if not isinstance(o,Q): o=Q(o,0,s.u,s.v)
        return Q(s.a+o.a,s.b+o.b,s.u,s.v)
    __radd__=__add__
    def __mul__(s,o):
        if not isinstance(o,Q): return Q(s.a*o,s.b*o,s.u,s.v)
        return Q(s.a*o.a+s.b*o.b*s.v, s.a*o.b+s.b*o.a+s.b*o.b*s.u, s.u,s.v)
    __rmul__=__mul__
    def __eq__(s,o):
        if not isinstance(o,Q): o=Q(o,0,s.u,s.v)
        return s.a==o.a and s.b==o.b
# golden: w^2=w+1 (both roots satisfy it: identity in Z[w] proves both). 1/w = w-1.
g=Q(0,1,1,1); ginv=Q(-1,1,1,1); assert g*ginv==1
def gpow(x):
    r=Q(1,0,1,1)
    for _ in range(abs(x)): r=r*(g if x>0 else ginv)
    return r
GP={x:gpow(x) for x in range(-9,9)}
r2=Q(0,1,0,2)  # w^2=2
def step(v,mv):
    x,s,gn=v
    if mv: return (x+1,'R',gn)
    return (x-1,'L',-gn if s=='L' else gn)
def walks(T,N=None):
    res=[]
    for mvs in itertools.product((1,0),repeat=T):
        v=(0,'R',1); pos=[]
        for mv in mvs:
            v=step(v,mv)
            if N: v=(v[0]%N,v[1],v[2])
            pos.append(v[0])
        res.append((mvs,v,tuple(pos)))
    return res
def mS(ws):
    m={}
    for (mvs,v,pos) in ws:
        y=(v[0],v[1]); p,q=m.get(y,(0,0))
        m[y]=(p+1,q) if v[2]==1 else (p,q+1)
    return m
def mu(m,F):
    t=0
    for y,(p,q) in m.items(): t=t+F(y,p,q)
    return t
rules={
 'a1':(lambda y,p,q:y[0]*(p+q), 2),
 'a2':(lambda y,p,q:(p-q)*GP[y[0] if y[1]=='R' else y[0]-1], 2),
 'b_lam2':(lambda y,p,q:Fr(2)**y[0]*(p+q), Fr(5,2)),
 'b_lam1/3':(lambda y,p,q:Fr(1,3)**y[0]*(p+q), Fr(10,3)),
 'c':(lambda y,p,q:(p-q)*(Q(1,0,0,2) if y[1]=='R' else Q(-1,1,0,2)), r2),
 'iv_a':(lambda y,p,q:p+q,2),'iv_c':(lambda y,p,q:(p-q)**2,2)}
def check(ws,ext_by_prefix,S_idx,names,bad):
    S=[ws[i] for i in S_idx]
    E=[w for i in S_idx for w in ext_by_prefix[ws[i][0]]]
    m1,m2=mS(S),mS(E)
    for nm in names:
        F,k=rules[nm]
        if not (mu(m2,F)==k*mu(m1,F)): bad[nm]+=1
random.seed(20261114)
def run(N,Tmax_all,names,sample_T=()):
    bad={nm:0 for nm in names}; nev=0
    W={T:walks(T,N) for T in range(0,max((Tmax_all,)+tuple(sample_T))+2)}
    for T in list(range(0,Tmax_all+1))+list(sample_T):
        ws=W[T]; ext={}
        for w in W[T+1]: ext.setdefault(w[0][:-1],[]).append(w)
        assert all(len(v)==2 for v in ext.values())
        n=len(ws)
        if T<=Tmax_all:
            for mask in range(1<<n):
                check(ws,ext,[i for i in range(n) if mask>>i&1],names,bad); nev+=1
        else:
            for _ in range(20000):
                check(ws,ext,[i for i in range(n) if random.random()<0.5],names,bad); nev+=1
            sites=sorted({p for w in ws for p in w[2]})
            for _ in range(20000):
                A=[{s for s in sites if random.random()<0.7} for _ in range(T)]
                check(ws,ext,[i for i in range(n) if all(ws[i][2][t] in A[t] for t in range(T))],names,bad); nev+=1
    return nev,bad
nev,bad=run(None,4,['a1','a2','b_lam2','b_lam1/3','c','iv_a','iv_c'],sample_T=(5,6))
for nm,b in bad.items():
    verdict(f'C line rule {nm}',b==0,f'events {nev} (all subsets T=0..4: {sum(2**(2**T) for T in range(5))}; samples T=5,6: 80000), violations {b}')
# second golden root: identity in Z[w]/(w^2-w-1) covers both roots (noted); explicit numeric sanity not needed.
# C-a3
lamp=(1+5**0.5)/2; lamm=(1-5**0.5)/2
a3=all(x*(1+0)<(x+1) for x in range(-40,40)) and all(-(lamp**(x+1))<-(lamp**x) for x in range(-40,40)) and all((lamm**(2*x+1))<0 for x in range(-20,20)) and all(abs(lamm**(2*x-1))>abs(lamm**(2*x+1)) for x in range(-20,20))
verdict('C-a3',a3,'x(1,0)->-inf as x->-inf; -(lam+^x) at m=(0,1) ->-inf as x->+inf; lam-^x at odd x negative, growing as x->-inf',measured=True)
# C-c E0 directly
badc=0;nc=0
FR=lambda p,q:(p-q)*Q(1,0,0,2); FL=lambda p,q:(p-q)*Q(-1,1,0,2)
for U in itertools.product(range(7),repeat=2):
    for V in itertools.product(range(7),repeat=2):
        nc+=1
        lhs=FR(U[0]+V[0],U[1]+V[1])+FL(U[0]+V[1],U[1]+V[0])
        rhs=r2*(FR(*U)+FL(*V))
        if not lhs==rhs: badc+=1
verdict('C-c E0 factor sqrt2',badc==0,f'pairs {nc}, violations {badc}')
for N in range(1,7):
    nev,bad=run(N,4,['iv_a','iv_c'])
    verdict(f'C-iv ring N={N}',all(b==0 for b in bad.values()),f'events {nev}, violations {bad}')
W_(f'COUNTS {cnt}')
out.close()
