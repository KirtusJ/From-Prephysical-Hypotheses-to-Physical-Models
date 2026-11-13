"""Challenger program A (box systems). Predicates fixed before first run:
PA1: for each (q, multiset u with sum 0 [hypothesis tested per instance]), the exact solution space of
     sum_z f(a+u_z b) = m f(a)+m f(b), f a function of |alpha|^2 (exact key), over all a,b with a,b,a+u_z b in box,
     restricted to classes with all coordinates of a representative in the inner box (radius r_in = r//2),
     has dimension phi(q)/2 (q>2) [rank computed mod prime p=2^31-1; nullity mod p >= nullity over Q,
     and the restricted dimension is computed mod p as well; if restricted dim == phi(q)/2 and conjugate rules lie in it, pass].
PA2: f=Re(a^4) on Z[i] satisfies (V) for (1,i,-1,-i) on box radius 8, is invariant under i, -1, conj; f(5)=625, f(3+4i)=-527.
PA3: the full nullity (not restricted) is reported; excess is recorded, not a failure.
Fixed seed not needed (deterministic)."""
import itertools, sys, numpy as np
from math import gcd
P=2**31-1
def phi(q): return sum(1 for k in range(1,q+1) if gcd(k,q)==1)
def ring(q):
    # basis 1,z,...,z^(n-1); reduce via cyclotomic polynomial
    import sympy
    x=sympy.symbols('x'); cp=sympy.Poly(sympy.cyclotomic_poly(q,x),x); n=cp.degree()
    red=[]
    for k in range(2*q):
        r=sympy.Poly(x**k,x).rem(cp); c=r.all_coeffs()[::-1]; c=c+[0]*(n-len(c)); red.append(tuple(int(v) for v in c))
    return n,red
def mulpow(v,k,n,red,q):
    out=[0]*n
    for i,c in enumerate(v):
        if c:
            r=red[(i+k)%q]
            for j in range(n): out[j]+=c*r[j]
    return tuple(out)
def norm_key(v,n,red,q):
    # |alpha|^2 = alpha*conj(alpha) as element of ring (exact)
    out=[0]*n
    for i,c in enumerate(v):
        for j,d in enumerate(v):
            if c and d:
                r=red[(i-j)%q]
                for t in range(n): out[t]+=c*d*r[t]
    return tuple(out)
def rank_mod(M):
    M=M.copy()%P; r=0; rows,cols=M.shape; piv=[]
    for c in range(cols):
        nz=np.nonzero(M[r:,c])[0]
        if len(nz)==0: continue
        p=r+nz[0]; M[[r,p]]=M[[p,r]]
        inv=pow(int(M[r,c]),P-2,P); M[r]=(M[r]*inv)%P
        f=M[:,c].copy(); f[r]=0
        idx=np.nonzero(f)[0]
        if len(idx): M[idx]=(M[idx]-np.outer(f[idx],M[r]))%P
        piv.append(c); r+=1
        if r==rows: break
    return r,piv,M[:r]
def run(q,us,r,log):
    n,red=ring(q)
    # us: list of (sign, exponent)
    pts=list(itertools.product(range(-r,r+1),repeat=n)); S=set(pts)
    # hypothesis: sum u = 0
    tot=[0]*n
    for s,k in us:
        v=red[k%q]
        for j in range(n): tot[j]+=s*v[j]
    hyp=all(t==0 for t in tot)
    keys={}; cls={}
    for p in pts:
        k=norm_key(p,n,red,q)
        if k not in keys: keys[k]=len(keys)
        cls[p]=keys[k]
    zero=cls[tuple([0]*n)]
    rows=set()
    for a in pts:
        for b in pts:
            ok=True; row={}
            for s,k in us:
                ub=mulpow(b,k,n,red,q); c=tuple(a[j]+s*ub[j] for j in range(n))
                if c not in S: ok=False;break
                row[cls[c]]=row.get(cls[c],0)+1
            if not ok: continue
            m=len(us)
            row[cls[a]]=row.get(cls[a],0)-m; row[cls[b]]=row.get(cls[b],0)-m
            t=tuple(sorted((k,v) for k,v in row.items() if v))
            if t: rows.add(t)
    N=len(keys); M=np.zeros((len(rows),N),dtype=np.int64)
    for i,t in enumerate(rows):
        for k,v in t: M[i,k]=v
    rk,piv,R=rank_mod(M)
    null=N-rk
    # restricted dimension: classes with rep in inner box
    rin=r//2
    inner=sorted({cls[p] for p in pts if max(abs(c) for c in p)<=rin})
    # nullspace basis mod P
    free=[c for c in range(N) if c not in set(piv)]
    B=np.zeros((len(free),N),dtype=np.int64)
    for i,fc in enumerate(free):
        B[i,fc]=1
        for ri,pc in enumerate(piv): B[i,pc]=(-R[ri,fc])%P
    rdim=rank_mod(B[:,inner])[0] if len(free) else 0
    exp=phi(q)//2 if q>2 else 1
    # conjugate rules in the solution space? check sigma_j norm satisfies all rows numerically
    import cmath
    conj_ok=True
    for j in range(1,q):
        if gcd(j,q)!=1: continue
        z=cmath.exp(2j*cmath.pi*j/q)
        val={}
        for p in pts: val[cls[p]]=abs(sum(c*z**i for i,c in enumerate(p)))**2
        res=max(abs(sum(v*val[k] for k,v in t)) for t in rows)
        if res>1e-7: conj_ok=False
    line=f"q={q} u={us} r={r} hyp_sum0={hyp} classes={N} eqs={len(rows)} nullity={null} restricted_dim(r_in={rin})={rdim} expected={exp} conj_rules_ok={conj_ok} PA1={'PASS' if (hyp and rdim==exp and conj_ok) else 'FAIL'}"
    print(line); log.write(line+"\n"); log.flush()
if __name__=="__main__":
    log=open("box_results.txt","x")
    # PA2
    ok=True
    f=lambda a: (a**4).real
    G=[complex(x,y) for x in range(-8,9) for y in range(-8,9)]
    mx=0
    for a in G:
        for b in G:
            mx=max(mx,abs(sum(f(a+u*b) for u in (1,1j,-1,-1j))-4*f(a)-4*f(b)))
    inv=max(max(abs(f(a)-f(1j*a)),abs(f(a)-f(-a)),abs(f(a)-f(a.conjugate()))) for a in G)
    line=f"PA2 maxresid={mx} maxinvdefect={inv} f(5)={f(5+0j)} f(3+4i)={f(3+4j)} {'PASS' if mx==0 and inv==0 and f(5+0j)==625 and f(3+4j)==-527 else 'FAIL'}"
    print(line); log.write(line+"\n")
    jobs=[
     (4,[(1,0),(1,1),(1,2),(1,3)],8),(4,[(1,0),(-1,0)],8),(4,[(1,0),(1,2),(1,1),(1,3),(1,0),(1,2)],7),
     (4,[(1,1),(-1,1),(1,0),(-1,0)],8),
     (3,[(1,0),(1,1),(1,2)],8),(3,[(1,0),(-1,0)],8),(3,[(1,0),(1,1),(1,2),(-1,0),(-1,1),(-1,2)],7),(3,[(1,0),(1,1),(1,2),(1,0),(-1,0)],7),
     (6,[(1,0),(1,2),(1,4)],8),(6,[(1,1),(1,3),(1,5),(1,0),(1,3)],7),
     (8,[(1,0),(1,4)],3),(8,[(1,0),(1,2),(1,4),(1,6)],3),(8,[(1,0),(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7)],3),(8,[(1,1),(1,5),(1,0),(1,4)],3),
     (8,[(1,0),(1,4)],4),(8,[(1,1),(1,5),(1,0),(1,4)],4),
     (5,[(1,0),(1,1),(1,2),(1,3),(1,4)],3),(5,[(1,0),(-1,0)],3),
     (12,[(1,0),(1,4),(1,8)],3),(12,[(1,0),(1,6),(1,1),(1,7)],3),
     (4,[(1,0),(1,1),(1,2)],6),  # control: sum != 0, hypothesis fails
    ]
    for q,us,r in jobs: run(q,us,r,log)
