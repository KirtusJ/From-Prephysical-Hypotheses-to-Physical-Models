"""Task 3(i). Certificate search: is the parallelogram expression
   D(a,b) = f(a+b)+f(a-b)-2f(a)-2f(b)   (a,b generic: formal symbols f[alpha a+beta b], (alpha,beta) in R^2 modulo units +-zeta^k)
a rational combination of instances V(x,y), x,y in a window W = {alpha a + beta b : alpha,beta in S}, S = elements of R with T<=Ts?
Only f(eps x)=f(x) for units eps = +-zeta^k and f(0)=0 are used (no conjugation, no modulus).
PREDICATE: C3: D is in the rational span of the window instances (reported per case; failures kept).
A certificate found is verified exactly (integer identity of formal sums) before being written.
usage: t3_cert.py q "k1,k2,.." Ts
"""
import sys, os, json, itertools, math
import numpy as np, sympy as sp
from fractions import Fraction
q=int(sys.argv[1]); ks=[int(x) for x in sys.argv[2].split(',')]; Ts=int(sys.argv[3]); m=len(ks)
x=sp.symbols('x'); Phi=sp.Poly(sp.cyclotomic_poly(q,x),x); n=Phi.degree()
def vec(k):
    r=sp.Poly(x**(k%q),x).rem(Phi); c=[0]*n
    for (d,),cc in r.terms(): c[d]=int(cc)
    return c
Z=[vec(k) for k in range(q)]
def Mk(k): return np.array([vec(j+k) for j in range(n)],dtype=np.int64)
assert not np.any(sum(np.array(Z[k]) for k in ks))
tr=[int(round(sum(math.cos(2*math.pi*k*i/q) for k in range(1,q+1) if math.gcd(k,q)==1))) for i in range(q)]
def T(c): return sum(c[j]*c[l]*tr[(j-l)%q] for j in range(n) for l in range(n))
L=int(math.isqrt(Ts))+2
S=[np.array(c,dtype=np.int64) for c in itertools.product(range(-L,L+1),repeat=n) if T(c)<=Ts]
S.sort(key=lambda c:(T(c),tuple(c)))
units=[s*Mk(k) for k in range(q) for s in (1,-1)]
def canon(v):   # v = (alpha,beta) concatenated, length 2n
    best=None
    for U in units:
        w=tuple(int(t) for t in np.concatenate([v[:n]@U,v[n:]@U]))
        if best is None or w>best: best=w
    return best
MU=[Mk(k) for k in ks]
W=[np.concatenate([al,be]) for al in S for be in S]
W.sort(key=lambda v:(T(v[:n])+T(v[n:]),tuple(v)))
sym={}
def sid(v):
    c=canon(v)
    if c not in sym: sym[c]=len(sym)
    return sym[c]
zero=tuple([0]*(2*n))
def instance(xv,yv):
    row={}
    def add(v,cf):
        c=canon(v)
        if c==zero: return
        i=sid(v); row[i]=row.get(i,0)+cf
        if row[i]==0: del row[i]
    for U in MU: add(xv+np.concatenate([yv[:n]@U,yv[n:]@U]),1)
    add(xv,-m); add(yv,-m)
    return row
one=np.array(Z[0],dtype=np.int64); zr=np.zeros(n,dtype=np.int64)
a=np.concatenate([one,zr]); b=np.concatenate([zr,one])
target={}
for v,cf in ((a+b,1),(a-b,1),(a,-2),(b,-2)):
    i=sid(v); target[i]=target.get(i,0)+cf
rows=[]; seen=set(); meta=[]
for xv in W:
    if canon(xv)!=tuple(int(t) for t in xv) : continue      # x up to units
    for yv in W:
        r=instance(xv,yv)
        if not r: continue
        key=tuple(sorted(r.items()))
        if key in seen: continue
        seen.add(key); rows.append(r); meta.append((tuple(int(t) for t in xv),tuple(int(t) for t in yv)))
ncol=len(sym); p=1048573
print('window',len(S),'instances',len(rows),'symbols',ncol,flush=True)
# incremental elimination mod p with combination tracking (sparse dict rows)
piv={}   # col -> (rowdict mod p, combo dict)
def reduce(r,combo):
    r=dict(r); combo=dict(combo)
    while r:
        c=min(r)
        if c not in piv: return r,combo
        pr,pc=piv[c]; f=r[c]
        for k,v in pr.items():
            nv=(r.get(k,0)-f*v)%p
            if nv: r[k]=nv
            else: r.pop(k,None)
        for k,v in pc.items():
            nv=(combo.get(k,0)-f*v)%p
            if nv: combo[k]=nv
            else: combo.pop(k,None)
    return r,combo
found=None
tgt={k:v%p for k,v in target.items()}
for i,r in enumerate(rows):
    rr,cc=reduce({k:v%p for k,v in r.items()},{i:1})
    if rr:
        c=min(rr); inv=pow(rr[c],p-2,p)
        piv[c]=({k:v*inv%p for k,v in rr.items()},{k:v*inv%p for k,v in cc.items()})
        if i%50==0 or True:
            tr_,tc=reduce(tgt,{})
            if not tr_:
                found=sorted(tc); break
res={'q':q,'u':ks,'Ts':Ts,'instances':len(rows),'symbols':ncol,'rank_mod_p':len(piv),'C3_in_span_mod_p':found is not None}
if found:
    # exact solve on support rows
    sup=found; cols=sorted(set(k for i in sup for k in rows[i])|set(target))
    A=sp.Matrix([[rows[i].get(c,0) for i in sup] for c in cols]); tv=sp.Matrix([target.get(c,0) for c in cols])
    lam=sp.symbols('l0:%d'%len(sup))
    sol=sp.linsolve((A,tv),*lam)
    sol=list(sol)
    if sol:
        s=[sp.nsimplify(t.subs({l:0 for l in lam})) for t in sol[0]]
        chk={}
        for i,cf in zip(sup,s):
            for k,v in rows[i].items(): chk[k]=chk.get(k,0)+cf*v
        ok=all(sp.simplify(chk.get(k,0)-target.get(k,0))==0 for k in set(chk)|set(target))
        res['exact_certificate_verified']=bool(ok)
        res['certificate']=[{'coef':str(cf),'x':meta[i][0],'y':meta[i][1]} for i,cf in zip(sup,s) if cf!=0]
        res['certificate_size']=len(res['certificate'])
    else: res['exact_certificate_verified']=False
fn=f"t3_q{q}_u{'-'.join(map(str,ks))}_Ts{Ts}.json"
assert not os.path.exists(fn)
json.dump(res,open(fn,'w'),indent=1)
print({k:v for k,v in res.items() if k!='certificate'})
if found and res.get('certificate_size',99)<=12:
    for c in res['certificate']: print(c)
