"""Task 2. Exact linear system (V) on R=Z[zeta_q].
Unknowns: f(kappa), kappa = a*conj(a) (exact element of Z[zeta], coefficient vector mod Phi_q), kappa != 0,
 for all a in R with T(a) <= Tmax, where T(a) = sum over all phi(q) embeddings |sigma(a)|^2 (= 2|a|^2 when phi(q)=2).
Equations: (V) for every pair (a,b), a,b != 0, with T(a),T(b),T(a+u_z b) <= Tmax for all z (a taken up to units).
Method: rows selected by elimination mod p=1048573 (selection only), then exact integer elimination over the
 selected rows with columns ordered by decreasing T; dim of {solutions restricted to T<=T0} = #keys(T<=T0) - #pivots(T<=T0).
 Using a subset of rows can only enlarge the solution space, and |sigma_j a|^2 (j=1..phi/2) are always solutions,
 so a computed dimension equal to phi(q)/2 is exact.
PREDICATE (fixed before run), for every (q,u,Tmax) in the run list:
   P2: dim of the solution space restricted to keys with T <= Tmax/4 equals phi(q)/2
       (hence it is spanned by the conjugate rules |sigma_j(a)|^2; for phi(q)=2, proportional to N).
Also reported, not a predicate: T*, the largest T0 such that the restricted dimension is phi(q)/2 for T0.
usage: t2_lattice.py q "k1,k2,..." Tmax     (u_z = zeta_q^{k_z})
"""
import sys, os, json, itertools, math
import numpy as np, sympy as sp
q=int(sys.argv[1]); ks=[int(x) for x in sys.argv[2].split(',')]; Tmax=int(sys.argv[3])
m=len(ks)
x=sp.symbols('x'); Phi=sp.Poly(sp.cyclotomic_poly(q,x),x); n=Phi.degree()
def vec(k):
    r=sp.Poly(x**(k%q),x).rem(Phi); c=[0]*n
    for (d,),cc in r.terms(): c[d]=int(cc)
    return c
Z=np.array([vec(k) for k in range(q)],dtype=np.int64)       # zeta^k
assert not np.any(sum(Z[k] for k in ks)), "multiset does not sum to zero"
# multiplication by zeta^k : matrix Mk with (c @ Mk) = coefficients of zeta^k * c
def Mk(k): return np.array([vec(j+k) for j in range(n)],dtype=np.int64)
MU=[Mk(k) for k in ks]
# key: a*conj(a) = sum_{j,l} c_j c_l zeta^{j-l}
G=np.zeros((n,n,n),dtype=np.int64)
for j in range(n):
    for l in range(n): G[j,l,:]=Z[(j-l)%q]
tr=np.array([sum(int(round((sp.exp(2*sp.pi*sp.I*sp.Rational(k*i,q))).evalf().as_real_imag()[0]*1e6))/1e6 for k in range(1,q+1) if math.gcd(k,q)==1) for i in range(n)])
tr=np.rint(tr).astype(np.int64)                                # Tr(zeta^i)
def keys(C): return np.einsum('aj,al,jli->ai',C,C,G)
def Tof(C): return keys(C)@tr
Qf=np.einsum('jli,i->jl',G,tr).astype(float)
lam=np.linalg.eigvalsh((Qf+Qf.T)/2)[0]; L=int(math.isqrt(int(Tmax/lam)))+1
rng=np.arange(-L,L+1)
E=np.array(list(itertools.product(rng,repeat=n)),dtype=np.int64)
TE=Tof(E); E=E[(TE<=Tmax)]; TE=Tof(E)
nz=np.any(E!=0,axis=1); E=E[nz]; TE=TE[nz]
KE=keys(E)
B=4*Tmax+7
def code(K):
    c=np.zeros(len(K),dtype=np.int64)
    for i in range(n): c=c*B+(K[:,i]+2*Tmax+3)
    return c
ucodes,idx=np.unique(code(KE),return_index=True)
ncol=len(ucodes); Tcol=TE[idx]; Kcol=KE[idx]
order=np.argsort(-Tcol,kind='stable')        # column position -> key id, decreasing T
pos=np.empty(ncol,dtype=np.int64); pos[order]=np.arange(ncol)
# canonical a up to units +-zeta^k: lexicographically largest in orbit
units=[s*Mk(k) for k in range(q) for s in (1,-1)]
def canon_mask(C):
    best=np.ones(len(C),dtype=bool)
    for U in units:
        D=C@U
        # is C >= D lexicographically?
        gt=np.zeros(len(C),dtype=bool); eq=np.ones(len(C),dtype=bool)
        for i in range(n):
            gt|= eq&(C[:,i]>D[:,i]); lt=eq&(C[:,i]<D[:,i]); eq&=(C[:,i]==D[:,i]); best&=~lt
    return best
A=E[canon_mask(E)]
p=1048573
basis=np.zeros((0,ncol)); piv=[]; sel=[]
neq=0
def lookup(C):
    c=code(keys(C)); j=np.searchsorted(ucodes,c); return pos[j]
posE=lookup(E)
for a in A:
    pa=lookup(a[None,:])[0]
    ok=np.ones(len(E),dtype=bool); cols=[]
    for U in MU:
        S=a[None,:]+E@U
        t=Tof(S); ok&=(t<=Tmax)
        cols.append(S)
    if not ok.any(): continue
    rows=np.zeros((int(ok.sum()),ncol),dtype=np.int64); r=np.arange(rows.shape[0])
    for S in cols:
        S=S[ok]; z0=~np.any(S!=0,axis=1)
        S2=S.copy(); S2[z0]=E[0]
        pp=lookup(S2)
        np.add.at(rows,(r[~z0],pp[~z0]),1)
    np.add.at(rows,(r,np.full(len(r),pa)),-m)
    np.add.at(rows,(r,posE[ok]),-m)
    rows=np.unique(rows,axis=0); neq+=len(rows)
    Rm=np.mod(rows,p).astype(float)
    if piv:
        Rm=np.mod(Rm-np.mod(Rm[:,piv]@basis,p),p)
    while True:
        nzr=np.nonzero(Rm.any(axis=1))[0]
        if len(nzr)==0: break
        i=nzr[0]; c=int(np.nonzero(Rm[i])[0][0])
        inv=pow(int(Rm[i,c]),p-2,p)
        v=np.mod(Rm[i]*inv,p)
        Rm=np.mod(Rm-np.outer(Rm[:,c],v),p)
        if len(piv): basis=np.mod(basis-np.outer(basis[:,c],v),p)
        basis=np.vstack([basis,v]); piv.append(c); sel.append([int(t) for t in rows[i]])
# exact echelon over selected rows, column order = decreasing T
rowsx=[r[:] for r in sel]; pivcols=[]
from math import gcd
from functools import reduce
ci=0
for c in range(ncol):
    pr=None
    for i in range(ci,len(rowsx)):
        if rowsx[i][c]!=0: pr=i;break
    if pr is None: continue
    rowsx[ci],rowsx[pr]=rowsx[pr],rowsx[ci]; P=rowsx[ci]
    for i in range(ci+1,len(rowsx)):
        e=rowsx[i][c]
        if e:
            Rr=rowsx[i]; g=gcd(P[c],e); f1=P[c]//g; f2=e//g
            Rr=[f1*xx-f2*yy for xx,yy in zip(Rr,P)]
            g2=reduce(gcd,Rr)
            if g2>1: Rr=[xx//g2 for xx in Rr]
            rowsx[i]=Rr
    pivcols.append(c); ci+=1
    if ci==len(rowsx): break
Ts=Tcol[order]                     # T by column position (decreasing)
pivT=sorted(int(Ts[c]) for c in pivcols)
allT=sorted(int(t) for t in Ts)
import bisect
exp_dim=n//2
prof={}
for T0 in sorted(set(allT)):
    prof[T0]=bisect.bisect_right(allT,T0)-bisect.bisect_right(pivT,T0)
Tq=Tmax//4
dq=bisect.bisect_right(allT,Tq)-bisect.bisect_right(pivT,Tq)
Tstar=0
for T0 in sorted(prof):
    if bisect.bisect_right(allT,T0)>=exp_dim and prof[T0]==exp_dim: Tstar=T0
    elif prof[T0]>exp_dim: break
res={'q':q,'u_exponents':ks,'m':m,'phi':n,'Tmax':Tmax,'elements':int(len(E)),'unknowns':int(ncol),'distinct_equations':int(neq),
     'rank_selected_exact':len(pivcols),'rank_mod_p':len(piv),'total_solution_dim':int(ncol-len(pivcols)),
     'keys_with_T<=Tmax/4':bisect.bisect_right(allT,Tq),'dim_restricted_T<=Tmax/4':dq,'expected':exp_dim,
     'P2_holds':bool(dq==exp_dim),'Tstar':Tstar,'profile_T0_dim':prof}
fn=f"t2_q{q}_u{'-'.join(map(str,ks))}_T{Tmax}.json"
assert not os.path.exists(fn), "refuse to overwrite"
json.dump(res,open(fn,'w'))
print({k:v for k,v in res.items() if k!='profile_T0_dim'})
