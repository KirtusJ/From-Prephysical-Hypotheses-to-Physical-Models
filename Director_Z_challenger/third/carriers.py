"""Challenger program B (actual events on carriers with non-Fourier blocks). Predicates fixed before first run:
Carrier: d vertices, step matrix A = H (complex Hadamard with entries q-th roots), start vertex 0, y1=0,y2=1.
HYP (per carrier): A*A = d exactly (numerically <1e-9, entries are roots of unity), y1,y2 share a successor, and at
     length L every q-th root is the gain of >= NHYP=3 walks to y1 and to y2 (finite stand-in for 'every N').
PB1: for carriers passing HYP: solution space of consistency equations (factor d) over sampled events of length L,
     unknowns = phi at exact norm classes, restricted to classes occurring in >= 5 equations... measured as:
     dimension of null space projected on the classes of |alpha|^2 realised by alpha with coefficient sum <=3 (small moduli)
     equals phi(q)/2 (1 for q=2), and each conjugate rule satisfies every sampled equation (resid < 1e-8 relative; floats
     only for this check, the equations themselves are exact integer rows).
PB2: directed events (a at y1, b at y2, nothing else) built from actual walks reproduce eq (V) rows with u_z = conj(A_z,y1) A_z,y2.
Seed 20261113."""
import itertools, random, cmath, numpy as np, sys
from math import gcd
sys.path.insert(0,'.')
from box import ring, norm_key, rank_mod, phi, P
random.seed(20261113)
def carrier(name,E,q,L,log,nev=4000):
    d=len(E); n,red=ring(q)
    z=cmath.exp(2j*cmath.pi/q); A=np.array([[z**e for e in row] for row in E])
    aa=np.abs(A.conj().T@A-d*np.eye(d)).max()
    # A[y][x] = gain exponent E[y][x] for arc x->y
    # enumerate walks of length L from vertex 0: (end, gain exponent)
    walks=[(0,0)]
    for _ in range(L): walks=[(y,(g+E[y][x])%q) for (x,g) in walks for y in range(d)]
    cnt={}
    for (y,g) in walks: cnt[(y,g)]=cnt.get((y,g),0)+1
    NH=3
    hyp=aa<1e-9 and all(cnt.get((y,g),0)>=NH for y in (0,1) for g in range(q))
    by={}
    for i,(y,g) in enumerate(walks): by.setdefault((y,g),[]).append(i)
    keys={}
    def K(v):
        k=norm_key(tuple(v),n,red,q)
        if k not in keys: keys[k]=len(keys)
        return keys[k]
    zero=K([0]*n)
    def vec(S):
        v=[[0]*n for _ in range(d)]
        for i in S:
            y,g=walks[i]; r=red[g]
            for j in range(n): v[y][j]+=r[j]
        return v
    def step(v):
        out=[[0]*n for _ in range(d)]
        for y in range(d):
            for x in range(d):
                r=v[x]
                if any(r):
                    # multiply by z^E[y][x]
                    for i,c in enumerate(r):
                        if c:
                            rr=red[(i+E[y][x])%q]
                            for j in range(n): out[y][j]+=c*rr[j]
        return out
    rows=[]
    def addev(S):
        v=vec(S); w=step(v); row={}
        for c in w: k=K(c); row[k]=row.get(k,0)+1
        for c in v: k=K(c); row[k]=row.get(k,0)-d
        row.pop(zero,None)
        rows.append({k:x for k,x in row.items() if x})
    # random events
    for _ in range(nev):
        s=random.randint(1,7); addev(random.sample(range(len(walks)),s))
    # directed events at y1,y2
    pb2=True
    for _ in range(nev):
        S=[]
        for y in (0,1):
            for g in range(q):
                S+=random.sample(by[(y,g)],random.randint(0,min(2,len(by.get((y,g),[]))))) if (y,g) in by else []
        v=vec(S); addev(S)
        # compare with (V): moduli of a+u_z b
        a=sum(c*z**i for i,c in enumerate(v[0])); b=sum(c*z**i for i,c in enumerate(v[1]))
        w=step(v)
        for zz in range(d):
            m1=abs(sum(c*z**i for i,c in enumerate(w[zz]))); u=np.conj(A[zz,0])*A[zz,1]
            if abs(m1-abs(a+u*b))>1e-9: pb2=False
    N=len(keys); M=np.zeros((len(rows),N),dtype=np.int64)
    for i,r in enumerate(rows):
        for k,x in r.items(): M[i,k]=x
    M=np.unique(M,axis=0)
    rk,piv,R=rank_mod(M); ps=set(piv)
    free=[c for c in range(N) if c not in ps and c!=zero]
    B=np.zeros((len(free),N),dtype=np.int64)
    for i,fc in enumerate(free):
        B[i,fc]=1
        for ri,pc in enumerate(piv): B[i,pc]=(-R[ri,fc])%P
    small=set()
    for co in itertools.product(range(4),repeat=q):
        if 0<sum(co)<=3:
            v=[0]*n
            for g,c in enumerate(co):
                for j in range(n): v[j]+=c*red[g][j]
            k=norm_key(tuple(v),n,red,q)
            if k in keys and keys[k]!=zero: small.add(keys[k])
    small=sorted(small)
    rdim=rank_mod(B[:,small])[0] if len(free) else 0
    exp=phi(q)//2 if q>2 else 1
    inv={v:k for k,v in keys.items()}
    conj_ok=True
    for j in range(1,q+1):
        if gcd(j,q)!=1: continue
        zj=cmath.exp(2j*cmath.pi*j/q)
        val=np.array([abs(sum(c*zj**((i-0)) for i,c in enumerate([0]*0)) ) for _ in range(0)])
        # |sigma_j(alpha)|^2 = sigma_j(norm key)
        vals=np.array([sum(c*zj**i for i,c in enumerate(inv[k])).real for k in range(N)])
        res=np.abs(M@vals).max()
        if res>1e-7*max(1,np.abs(vals).max()): conj_ok=False
    us=[(E[zz][1]-E[zz][0])%q for zz in range(d)]
    line=f"{name}: d={d} q={q} L={L} |A*A-d|={aa:.1e} HYP={hyp} minwalks(y1,y2;gain)={min(cnt.get((y,g),0) for y in (0,1) for g in range(q))} u_exponents={us} classes={N} eqs={len(M)} nullity={len(free)} small_classes={len(small)} dim_on_small={rdim} expected={exp} conj_ok={conj_ok} PB2={pb2} PB1={'PASS' if hyp and rdim==exp and conj_ok else ('NOT-QUALIFIED' if not hyp else 'FAIL')}"
    print(line); log.write(line+"\n"); log.flush()
log=open("carrier_results.txt","x")
# real Hadamard 4x4 (Sylvester) with rows permuted and columns negated; q=2 exponents
H4=[[0,0,0,0],[0,1,0,1],[0,0,1,1],[0,1,1,0]]
H4p=[H4[i] for i in (2,0,3,1)]; H4p=[[ (e+(1 if x in (1,3) else 0))%2 for x,e in enumerate(r)] for r in H4p]
carrier("H4 real permuted/negated q=2",H4p,2,7,log)
# same entries seen as 4th roots, with one column times i and one row times i (not Fourier F4 pattern)
H4c=[[(2*e+(1 if x==2 else 0)+(1 if y==1 else 0))%4 for x,e in enumerate(r)] for y,r in enumerate(H4p)]
carrier("H4 Sylvester-type with i-phases q=4",H4c,4,7,log)
carrier("H4 Sylvester-type with phases q=8",[[(4*e+(1 if x==2 else 0)+(3 if y==1 else 0))%8 for x,e in enumerate(r)] for y,r in enumerate(H4p)],8,7,log)
# BH(6,3) (not Fourier: F6 needs 6th roots)
B63=[[0,0,0,0,0,0],[0,0,1,1,2,2],[0,1,0,2,2,1],[0,1,2,0,1,2],[0,2,2,1,0,1],[0,2,1,2,1,0]]
carrier("BH(6,3) q=3",B63,3,5,log,nev=3000)
carrier("BH(6,3) as 6th roots, col negated q=6",[[(2*e+(3 if x==4 else 0))%6 for x,e in enumerate(r)] for r in B63],6,5,log,nev=3000)
# Dita-type 6x6 from F3: [[F3, F3 D1],[F3, -F3 D1]] with D1=diag(1,z6,z6^2) columns: x<3: F3 col; x>=3: phase
F3=[[0,0,0],[0,2,4],[0,4,2]]
D=[0,1,5]
dita=[[F3[y%3][x%3]+ (0 if x<3 else D[x-3]) + (3 if (y>=3 and x>=3) else 0) for x in range(6)] for y in range(6)]
dita=[[e%6 for e in r] for r in dita]
carrier("Dita-type 6x6 q=6",dita,6,5,log,nev=3000)
# control: not norm-preserving
bad=[r[:] for r in H4p]; bad[0][0]=(bad[0][0]+1)%2
carrier("control H4 with one sign flipped (A*A != d)",bad,2,7,log)
