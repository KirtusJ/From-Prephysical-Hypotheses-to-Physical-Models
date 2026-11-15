#!/usr/bin/env python3
"""S3 check (thm:fgadj), own program of the reviewer. Seed not used (exhaustive). 
Command line: python3 s3_adjacent.py OUTFILE   (OUTFILE opened with mode 'x')
Arithmetic: ranks modulo the prime p = 2^31-1.  Nullity mod p >= nullity over Q >= rank of the
integer theory vectors; equality mod p therefore proves equality of the spaces over Q.

Setting per case: Delta = Z_n1 x Z_n2, delta, beta with Delta = <delta,beta>, r = ord(delta),
s = least j>=1 with j*beta in <delta>, s*beta = k*delta.  C_i = i*beta + <delta>.
Unknown f on Delta-orbits of non-empty multisets of size <= n lying in two adjacent cosets
(f(empty)=0).  Equations f(u+v)+f(u+T_delta v)=2f(u)+2f(v) ONLY at
 (A_i) u in M(C_i u C_{i+1}), v in M(C_{i+1});  (B_i) u in M(C_i), v in M(C_i u C_{i+1}), all i mod s.

PREDICATES (fixed before the first run):
 H0 (hypothesis, per case): Delta=<delta,beta>, Delta/<delta> cyclic of order s; reported s, r, k.
 P1 theory functions well defined on orbits: count; for r even Q=eps_i^2+eps_{i+1}^2 and
    X=c_i eps_i eps_{i+1}, c_i=1 (i<=s-2), c_{s-1}=(-1)^k. (s>=3 only.)
 P1c CONTROL, expected to FAIL when k odd and pass when k even: X with c_{s-1}=+1 always.
 P2 theory functions satisfy every equation (integer check).
 P3 dim of solution space projected to multisets of size <= n-1 equals 1 (r odd) / 3 (r even), s>=3.
 P4 that projection equals the theory span (follows from P2,P3 and independence of theory vectors).
 P5 (s=3, r even) the two squares |sigma_chi|^2 restricted give independent (q,c): (1,2Re z), z^3=(-1)^k.
 C2 CONTROL s=2 (thm:fgtwo, known answer): projected dim = 3 if r even,k even; 2 if r even,k odd; 1 if r odd.
Every failed predicate is written to the result file.
"""
import sys, itertools, json
import numpy as np
P=2147483647
def rref(A):
    A=A.copy()%P; piv=[]; r=0; m,n=A.shape
    for c in range(n):
        nz=np.nonzero(A[r:,c])[0]
        if len(nz)==0: continue
        i=r+nz[0]
        if i!=r: A[[r,i]]=A[[i,r]]
        A[r]=(A[r]*pow(int(A[r,c]),P-2,P))%P
        col=A[:,c].copy(); col[r]=0
        idx=np.nonzero(col)[0]
        if len(idx): A[idx]=(A[idx]-(col[idx,None]*A[r][None,:])%P)%P
        piv.append(c); r+=1
        if r==m: break
    return A[:r],piv
def rank(A):
    if A.size==0: return 0
    return len(rref(A)[1])
def run(n1,n2,delta,beta,n,out):
    els=[(a,b) for a in range(n1) for b in range(n2)]; ix={e:i for i,e in enumerate(els)}
    add=lambda x,y:((x[0]+y[0])%n1,(x[1]+y[1])%n2)
    def mul(j,x):
        z=(0,0)
        for _ in range(j): z=add(z,x)
        return z
    D=[(0,0)]
    while add(D[-1],delta)!=(0,0): D.append(add(D[-1],delta))
    r=len(D)
    s=1
    while mul(s,beta) not in D: s+=1
    k=D.index(mul(s,beta))
    gen={add(mul(j,beta),d) for j in range(s) for d in D}
    H0 = (len(gen)==len(els)) and s*r==len(els)
    cos={}; sgn={}
    for j in range(s):
        for nn,d in enumerate(D):
            g=ix[add(mul(j,beta),d)]; cos[g]=j; sgn[g]=(-1)**nn
    tr=[[ix[add(els[g],els[h])] for g in range(len(els))] for h in range(len(els))]
    di=ix[delta]
    def T(h,m): return tuple(sorted(tr[h][g] for g in m))
    def canon(m): return min(T(h,m) for h in range(len(els)))
    def adj(J):
        J=sorted(J)
        if len(J)<=1: return True
        if len(J)>2: return False
        return (J[1]-J[0])%s in (1,s-1)
    C=[[g for g in range(len(els)) if cos[g]==j] for j in range(s)]
    cols={}; size=[]
    def col(m):
        c=canon(m)
        if c not in cols: cols[c]=len(cols); size.append(len(c))
        return cols[c]
    rows=set()
    def ms(elems,a): return itertools.combinations_with_replacement(elems,a)
    for i in range(s):
        two=sorted(set(C[i]+C[(i+1)%s]))
        for kind,(EU,EV) in (('A',(two,C[(i+1)%s])),('B',(C[i],two))):
            for a in range(1,n):
                for b in range(1,n-a+1):
                    for u in ms(EU,a):
                        for v in ms(EV,b):
                            row={}
                            for m,c in ((tuple(sorted(u+v)),1),(tuple(sorted(u+T(di,v))),1),(u,-2),(v,-2)):
                                j=col(m); row[j]=row.get(j,0)+c
                            row=tuple(sorted((j,c) for j,c in row.items() if c))
                            if row: rows.add(row)
    # all orbits of two-adjacent-coset multisets up to n (some may be in no equation)
    for i in range(s):
        two=sorted(set(C[i]+C[(i+1)%s]))
        for a in range(1,n+1):
            for m in ms(two,a): col(m)
    nc=len(cols); A=np.zeros((len(rows),nc),dtype=np.int64)
    for ri,row in enumerate(rows):
        for j,c in row: A[ri,j]=c
    R,piv=rref(A); free=[c for c in range(nc) if c not in piv]
    NS=np.zeros((len(free),nc),dtype=np.int64)
    for fi,f in enumerate(free):
        NS[fi,f]=1
        for pr,pc in enumerate(piv): NS[fi,pc]=(-R[pr,f])%P
    small=[c for c in range(nc) if size[c]<=n-1]
    dim_full=len(free); dim_proj=rank(NS[:,small]) if len(free) else 0
    res=dict(group=[n1,n2],delta=delta,beta=beta,n=n,r=r,s=s,k=k,H0=bool(H0),unknowns=nc,equations=len(rows),dim_full=dim_full,dim_proj=dim_proj)
    fails=[]
    # theory
    def eps(m):
        e=[0]*s
        for g in m: e[cos[g]]+=sgn[g]
        return e
    def theory(m,ctrl=False):
        J=sorted({cos[g] for g in m}); e=eps(m)
        if r%2: return (len(m),)
        if len(J)==1: return (len(m),e[J[0]]**2,0)
        a,b=J
        i=a if (b-a)%s==1 else b
        if s==2: i=0
        ci=1 if (i<=s-2 or ctrl) else (-1)**k
        return (len(m),e[i]**2+e[(i+1)%s]**2,ci*e[i]*e[(i+1)%s])
    if s>=3:
        for ctrl in (False,True):
            bad=None
            for c in cols:
                vals={theory(T(h,c),ctrl) for h in range(len(els))}
                if len(vals)>1: bad=[list(c),sorted(vals)]; break
            name='P1c_control_wrongsign_welldefined' if ctrl else 'P1_welldefined'
            res[name]=bad is None
            if not ctrl and bad: fails.append(('P1',bad))
            if ctrl: res['P1c_expected']= (k%2==0) or (r%2==1); 
            if ctrl and res[name]!=res['P1c_expected']: fails.append(('P1c control not as expected',bad))
        TV=np.zeros((len(theory(next(iter(cols)))),nc),dtype=np.int64)
        for c,j in cols.items():
            for t,val in enumerate(theory(c)): TV[t,j]=val
        resid=A.dot(TV.T)
        res['P2_theory_solves']=bool((resid==0).all())
        if not res['P2_theory_solves']: fails.append(('P2',int(np.count_nonzero(resid))))
        tr_rank=rank(TV[:,small]%P); res['theory_rank_proj']=tr_rank
        exp=1 if r%2 else 3
        res['P3_dim_proj_expected']=exp; res['P3']=(dim_proj==exp)
        if not res['P3']: fails.append(('P3',dict(dim_proj=dim_proj,expected=exp,theory_rank_proj=tr_rank)))
        res['P4_equal_span']=bool(res['P2_theory_solves'] and dim_proj==tr_rank)
        if not res['P4_equal_span']: fails.append(('P4',dict(dim_proj=dim_proj,theory_rank_proj=tr_rank)))
        if s==3 and r%2==0:
            import cmath,math
            zs=[cmath.exp(1j*math.pi*(2*t+ (k%2))/3) for t in range(3)]
            pairs=sorted({(1,round(2*z.real,9)) for z in zs})
            det=None
            if len(pairs)>=2: det=pairs[0][0]*pairs[1][1]-pairs[1][0]*pairs[0][1]
            res['P5_pairs']=pairs; res['P5']=bool(len(pairs)==2 and abs(det)>1e-6)
            if not res['P5']: fails.append(('P5',pairs))
    else:
        exp=1 if r%2 else (3 if k%2==0 else 2)
        res['C2_expected']=exp; res['C2']=(dim_proj==exp)
        if not res['C2']: fails.append(('C2',dict(dim_proj=dim_proj,expected=exp)))
    res['failed']=fails
    out.write(json.dumps(res)+'\n'); out.flush(); print(res)
CASES=[ # n1,n2,delta,beta,list of n
 (2,1,(1,0),(0,0),[]),
 (4,1,(2,0),(1,0),[3,4,5,6,7]),      # control s=2 r=2 k=1
 (2,2,(1,0),(0,1),[3,4,5,6,7]),      # control s=2 r=2 k=0
 (6,1,(3,0),(1,0),[3,4,5,6,7]),      # s=3 r=2 k=1
 (6,1,(3,0),(2,0),[3,4,5,6,7]),      # s=3 r=2 k=0
 (8,1,(4,0),(1,0),[3,4,5,6,7]),      # s=4 r=2 k=1
 (2,4,(1,0),(0,1),[3,4,5,6,7]),      # s=4 r=2 k=0
 (10,1,(5,0),(1,0),[3,4,5,6]),       # s=5 r=2 k=1
 (2,5,(1,0),(0,1),[3,4,5,6]),        # s=5 r=2 k=0
 (12,1,(3,0),(1,0),[3,4,5,6]),       # s=3 r=4 k=1
 (12,1,(3,0),(2,0),[3,4,5,6]),       # s=3 r=4 k=2
 (4,3,(1,0),(0,1),[3,4,5,6]),        # s=3 r=4 k=0
 (3,1,(0,0),(1,0),[3,4,5,6,7]),      # s=3 r=1
 (9,1,(3,0),(1,0),[3,4,5,6]),        # s=3 r=3 k=1
 (4,1,(0,0),(1,0),[3,4,5,6]),        # s=4 r=1
 (12,1,(4,0),(1,0),[3,4,5]),         # s=4 r=3
]
if __name__=='__main__':
    with open(sys.argv[1],'x') as out:
        for n1,n2,d,b,ns in CASES:
            for n in ns: run(n1,n2,d,b,n,out)
