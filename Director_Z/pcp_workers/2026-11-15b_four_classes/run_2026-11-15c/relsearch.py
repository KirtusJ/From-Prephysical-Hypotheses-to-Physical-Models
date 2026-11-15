#!/usr/bin/env python3
"""relsearch.py S SIGMA BF BL NREL OUT   (deterministic; random.seed(20261113) set but unused)

Multiplicative relations among the elements p + qX of Q[X]/(X^S - SIGMA) modulo <Q*, -1, X>, by index calculus.
Components: Q(zeta_d), d | S (SIGMA=+1) or d | 2S, d not | S (SIGMA=-1).  Forms: (p,q) coprime, 1 <= q <= BF, |p| <= BF,
no component norm zero, all component norms BL-smooth.  Unknowns: exponents e_f and t_l = v_l(c).  Constraints:
valuations at degree-one primes (l = 1 mod d: one coordinate per root a of Phi_d mod l, value v_l(N_d) if l | p+qa),
t_l = 0 if some component has no degree-one prime over l (l not | d, l != 1 mod d), and for l | d the norm constraint
sum e v_l(N_d) = phi(d) t_l (exact here: for every d used, a ramified l has a single prime of degree one or none).
Integer kernel (flint), then LLL on unit logarithms (mpmath, 60 digits) to get zero-log combinations.
Each candidate is then VERIFIED EXACTLY in Z[X]/(X^S - SIGMA); a candidate whose torsion is not of the form +-X^j is
squared and re-verified.

PREDICATES fixed before the first run:
 Q1 every relation used is exactly verified: cA*prod_A == eps*cB*X^j*prod_B mod X^S - SIGMA (else counted as FAILED, kept).
 Q2 every h0 = cA^2|piA|^2 - cB^2|piB|^2 (unreduced pi, polynomial in w) is divisible by m(w).
 Q3a gcd over the verified relations with j = 0 mod S (realisable by multisets, Step 4 (c')) of their h0, compared with m.
 Q3b the same gcd after replacing every verified relation R by R^(S/gcd(j,S)) (so j = 0): compared with m.
 Q3c gcd over all verified relations ignoring j (only meaningful if j-relations are realisable): compared with m.
 Q4 whether some single verified j=0 relation has h0 = const*m.
Hypothesis per case: a form is used only if all its component norms are non-zero and BL-smooth; the number qualifying is
reported.  Result file opened with mode 'x'.
"""
import sys, json, random
from math import gcd
import flint, mpmath
from sympy import factorint, totient, divisors, primerange, cyclotomic_poly, Poly, symbols, nroots
random.seed(20261113)
S=int(sys.argv[1]); SIG=int(sys.argv[2]); BF=int(sys.argv[3]); BL=int(sys.argv[4]); NREL=int(sys.argv[5]); OUT=sys.argv[6]
out=open(OUT,'x'); mpmath.mp.dps=60
Xs=symbols('X')
comps=[d for d in divisors(S)] if SIG==1 else [d for d in divisors(2*S) if S%d]
phi={d:int(totient(d)) for d in comps}
Phi={d:[int(c) for c in Poly(cyclotomic_poly(d,Xs),Xs).all_coeffs()[::-1]] for d in comps}  # low->high
def normd(d,p,q):  # prod_k (p+q zeta^k) = sum_i Phi_i (-p)^i q^(phi-i) * (-1)^phi ... computed via homogenisation
    f=Phi[d]; n=phi[d]
    # prod (p + q z_k) = (-q)^n * Phi(-p/q) = (-1)^n sum_i f_i (-p)^i q^(n-i)
    return (-1)**n*sum(f[i]*(-p)**i*q**(n-i) for i in range(n+1))
primes=list(primerange(2,BL+1))
def vl(n,l):
    k=0
    while n%l==0: n//=l; k+=1
    return k
def smooth(n):
    n=abs(n)
    for l in primes:
        while n%l==0: n//=l
    return n==1
forms=[]; nall=0
for q in range(1,BF+1):
    for p in range(-BF,BF+1):
        if gcd(abs(p),q)!=1: continue
        nall+=1
        ns={d:normd(d,p,q) for d in comps}
        if any(v==0 for v in ns.values()): continue
        if all(smooth(v) for v in ns.values()): forms.append((p,q,ns))
roots={}
for d in comps:
    for l in primes:
        if d%l and (l-1)%d==0:
            roots[(d,l)]=[a for a in range(l) if sum(c*pow(a,i,l) for i,c in enumerate(Phi[d]))%l==0]
rows=[]; tidx={l:len(forms)+i for i,l in enumerate(primes)}; nv=len(forms)+len(primes)
for d in comps:
    for l in primes:
        if d%l==0:
            r=[0]*nv
            for i,(p,q,ns) in enumerate(forms): r[i]=vl(ns[d],l)
            r[tidx[l]]=-phi[d]; rows.append(r)
        elif (l-1)%d==0:
            for a in roots[(d,l)]:
                r=[0]*nv
                for i,(p,q,ns) in enumerate(forms):
                    if (p+q*a)%l==0: r[i]=vl(ns[d],l)
                r[tidx[l]]=-1; rows.append(r)
        else:
            r=[0]*nv; r[tidx[l]]=1; rows.append(r)
M=flint.fmpz_mat(rows)
K,nul=M.nullspace()
Kb=[[int(K[i,j]) for i in range(nv)] for j in range(nul)]
Kb=[[x//max(1,abs(gcd(*v))) if any(v) else 0 for x in v] for v in Kb]
Kl=flint.fmpz_mat(Kb).lll() if Kb else None
Kb=[[int(Kl[i,j]) for j in range(nv)] for i in range(Kl.nrows())] if Kb else []
# unit logs
def logvec(v):
    L=[]
    lc=sum(v[tidx[l]]*mpmath.log(l) for l in primes)
    for d in comps:
        ks=[k for k in range(1,d+1) if gcd(k,d)==1 and 2*k<=d] if d>2 else [1]
        for k in ks:
            z=mpmath.exp(2j*mpmath.pi*k/d)
            L.append(sum(v[i]*mpmath.log(abs(p+q*z)) for i,(p,q,ns) in enumerate(forms) if v[i])-lc)
    return L
LV=[logvec(v) for v in Kb]
SC=mpmath.mpf(10)**40
nlog=len(LV[0]) if LV else 0
B=[[1 if i==j else 0 for j in range(len(Kb))]+[int(mpmath.nint(SC*x)) for x in LV[i]] for i in range(len(Kb))]
Bl=flint.fmpz_mat(B).lll() if B else None
cands=[]
for i in range(Bl.nrows() if B else 0):
    row=[int(Bl[i,j]) for j in range(len(Kb)+nlog)]
    if max(abs(x) for x in row[len(Kb):])<10**12:
        coef=row[:len(Kb)]
        v=[sum(coef[t]*Kb[t][k] for t in range(len(Kb))) for k in range(nv)]
        if any(v[:len(forms)]): cands.append(v)
def pmul(a,b):
    r=[0]*S
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):
                if y:
                    k=i+j
                    if k>=S: r[k-S]+=SIG*x*y
                    else: r[k]+=x*y
    return r
def ppow(a,e):
    r=[1]+[0]*(S-1)
    for _ in range(e): r=pmul(r,a)
    return r
def sides(v,pw):
    A=[1]+[0]*(S-1); Bp=[1]+[0]*(S-1); cA=1; cB=1
    for i,(p,q,ns) in enumerate(forms):
        e=v[i]*pw
        f=[p,q]+[0]*(S-2)
        if e>0: A=pmul(A,ppow(f,e))
        elif e<0: Bp=pmul(Bp,ppow(f,-e))
    for l in primes:
        t=v[tidx[l]]*pw
        if t<0: cA*=l**(-t)
        elif t>0: cB*=l**t
    return A,Bp,cA,cB
def shiftX(r):
    return [SIG*r[-1]]+r[:-1]
def verify(v,pw):
    A,Bp,cA,cB=sides(v,pw)
    lhs=[cA*x for x in A]; cur=[cB*x for x in Bp]
    for j in range(S):
        if lhs==cur: return (j,1)
        if lhs==[-x for x in cur]: return (j,-1)
        cur=shiftX(cur)
    return None
W=flint.fmpq_poly([0,1])
def wpoly(v,pw,sign):
    P=flint.fmpq_poly([1])
    for i,(p,q,ns) in enumerate(forms):
        e=v[i]*pw*sign
        if e>0: P*=flint.fmpq_poly([p*p+q*q,p*q])**e
    c=1
    for l in primes:
        t=-v[tidx[l]]*pw*sign
        if t>0: c*=l**t
    return P*c*c
# m(w)
def cheb(n):
    a,b=flint.fmpq_poly([2]),W
    if n==0: return a
    for _ in range(n-1): a,b=b,W*b-a
    return b
mf=cheb(S)-2*SIG
mm=mf//mf.gcd(mf.derivative())
mm=mm/mm.coeffs()[-1]
rels=[]; failed=0
for v in cands[:NREL]:
    r=verify(v,1); pw=1
    if r is None:
        r=verify(v,2); pw=2
    if r is None: failed+=1; continue
    j,eps=r
    h0=wpoly(v,pw,1)-wpoly(v,pw,-1)
    t=S//gcd(j,S)
    h0b=wpoly(v,pw*t,1)-wpoly(v,pw*t,-1)
    rels.append(dict(v=v,pw=pw,j=j,eps=eps,h0=h0,h0b=h0b,deg=h0.degree(),Q2=(h0%mm==0 and h0b%mm==0)))
def g(L):
    G=flint.fmpq_poly([0])
    for h in L: G=G.gcd(h)
    return G
G3a=g([r['h0'] for r in rels if r['j']==0]); G3b=g([r['h0b'] for r in rels]); G3c=g([r['h0'] for r in rels])
def desc(G):
    if G==0: return 'no relations'
    return dict(gcd=str(G/G.coeffs()[-1]),deg=G.degree(),equals_m=(G.degree()==mm.degree() and G%mm==0))
single=[dict(forms=[(forms[i][0],forms[i][1],r['v'][i]*r['pw']) for i in range(len(forms)) if r['v'][i]],
             c={l:r['v'][tidx[l]]*r['pw'] for l in primes if r['v'][tidx[l]]},j=r['j'],eps=r['eps'],h0=str(r['h0']))
        for r in rels if r['j']==0 and r['h0']!=0 and r['h0'].degree()==mm.degree()]
smallest=sorted(rels,key=lambda r:sum(abs(x) for x in r['v'][:len(forms)])*r['pw'])[:5]
res=dict(argv=sys.argv,comps=comps,m=str(mm),deg_m=mm.degree(),forms_tested=nall,forms_qualifying=len(forms),
 kernel_rank=nul,log_constraints=nlog,candidates=len(cands),tried=min(NREL,len(cands)),Q1_verified=len(rels),Q1_failed=failed,
 Q2_all=all(r['Q2'] for r in rels),j_values=sorted(set(r['j'] for r in rels)),
 Q3a=desc(G3a),Q3b=desc(G3b),Q3c=desc(G3c),Q4_single=single[:3],
 smallest=[dict(forms=[(forms[i][0],forms[i][1],r['v'][i]*r['pw']) for i in range(len(forms)) if r['v'][i]],
   c={l:r['v'][tidx[l]]*r['pw'] for l in primes if r['v'][tidx[l]]},j=r['j'],eps=r['eps'],deg_h0=r['deg']) for r in smallest])
json.dump(res,out,indent=1,default=str); out.close()
print(json.dumps({k:v for k,v in res.items() if k not in('smallest','Q4_single')},default=str)); print('nsingle',len(single))
