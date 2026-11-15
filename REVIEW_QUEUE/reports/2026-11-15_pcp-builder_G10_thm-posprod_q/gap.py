"""Predicates fixed before first run.
CONTROL: number of +-1 walks of length 8 from 0 never below 0 (expected 70).
P1 (gap rings N in {3,6}, q in 3..6, lengths<=L): consider all realizable position-product
configurations (vertex -> gain multiset) from (0,R); impose mu(Ext S)=2 mu(S) with site-independent
F_R,F_L (unknown per multiset). Hypothesis check per case: count states, count states with walks.
Predicate: dimension of the solution space projected on coordinates with |m|<=b equals
nominal (1 for q odd, 2 for q even) and nominal solutions lie in it (rank check).
Seed 20261113 (unused, enumeration exhaustive). Exact rational arithmetic.
"""
import sys, itertools, random
from fractions import Fraction
random.seed(20261113)
def control():
    c=0
    for s in itertools.product([1,-1],repeat=8):
        p=0;ok=True
        for t in s:
            p+=t
            if p<0: ok=False;break
        c+=ok
    return c
def rank(rows,ncols):
    rows=[dict(r) for r in rows if r]; piv={}; r=0
    basis=[]
    for row in rows:
        row={k:Fraction(v) for k,v in row.items() if v}
        for p,(prow) in piv.items():
            pass
        # reduce
        changed=True
        while row:
            k=min(row)
            if k in piv:
                f=row[k]; pr=piv[k]
                for kk,vv in pr.items():
                    nv=row.get(kk,0)-f*vv
                    if nv: row[kk]=nv
                    else: row.pop(kk,None)
            else:
                f=row[k]; row={kk:vv/f for kk,vv in row.items()}; piv[k]=row; break
    return len(piv)
def run(N,q,L,b):
    # vertex (x,d) d=0 R,1 L; config: frozenset of ((x,d),gaintuple)
    def ext(cfg,A):
        new={}
        for (x,d),m in cfg:
            for (y,e,sh) in (((x+1)%N,0,0),((x-1)%N,1,1 if d==1 else 0)):
                if y not in A: continue
                mm=m[-sh:]+m[:-sh] if sh else m
                old=new.get((y,e),(0,)*q)
                new[(y,e)]=tuple(a+c for a,c in zip(old,mm))
        return frozenset(new.items())
    start=frozenset({((0,0),(1,)+(0,)*(q-1))})
    subsets=[frozenset(s) for r in range(1,N+1) for s in itertools.combinations(range(N),r)]
    allsites=frozenset(range(N))
    level={start}; states=set()
    for t in range(L):
        nl=set()
        for c in level:
            for A in subsets:
                n=ext(c,A)
                if n: nl.add(n)
        level=nl; states|=nl
    idx={}
    def var(d,m):
        return idx.setdefault((d,m),len(idx))
    rows=[]
    for c in states:
        e=ext(c,allsites); row={}
        for (y,m) in e: v=var(y[1],m); row[v]=row.get(v,0)+1
        for (y,m) in c: v=var(y[1],m); row[v]=row.get(v,0)-2
        rows.append(row)
    n=len(idx); r0=rank(rows,n)
    small=[v for (d,m),v in idx.items() if sum(m)<=b]
    r1=rank(rows+[{v:1} for v in small],n)
    projdim=(n-r0)-(n-r1)
    nominal=1 if q%2 else 2
    # check nominal in solution: |m| and eps^2 with F_R=F_L
    def chk(f):
        return all(sum(c*f(k) for k,c in row.items())==0 for row in rows)
    inv={v:k for k,v in idx.items()}
    ok1=chk(lambda v: sum(inv[v][1]))
    ok2=True if q%2 else chk(lambda v: sum((-1)**j*inv[v][1][j] for j in range(q))**2)
    return len(states),n,projdim,nominal,ok1,ok2
if __name__=="__main__":
    out=open(sys.argv[1],'x')
    print("CONTROL:",control(),file=out,flush=True)
    for N in (3,6):
        for q in (3,4,5,6):
            L=7 if N==3 else 6
            res=run(N,q,L,2)
            print(N,q,"L",L,"states,unknowns,projdim(|m|<=2),nominal,nomOK:",res,"PASS" if res[2]==res[3] and res[4] and res[5] else "FAIL",file=out,flush=True)
