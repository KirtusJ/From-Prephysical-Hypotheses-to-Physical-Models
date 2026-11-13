import numpy as np, sympy as sp, sys, math, random
from math import gcd
def setup(q):
    x=sp.symbols('x'); Phi=sp.Poly(sp.cyclotomic_poly(q,x),x); n=Phi.degree()
    red=np.array([[int(c) for c in reversed(sp.Poly(sp.rem(x**e,Phi.as_expr(),x),x).all_coeffs()+[] )]+[0]*n for e in range(q)],dtype=object)
    red=np.array([list(row[:n])+[0]*0 for row in [ (list(r)+[0]*n)[:n] for r in [[int(c) for c in reversed(sp.Poly(sp.rem(x**e,Phi.as_expr(),x),x).all_coeffs())] for e in range(q)]]],dtype=np.int64)
    return red
def normkey(c,q,red):  # c: length-q int vector, coefficients of zeta^e
    p=np.zeros(q,dtype=np.int64)
    for e in np.nonzero(c)[0]:
        p+=c[e]*np.roll(c[::-1],e+1)   # c * conj(c) mod x^q-1
    return tuple(p@red)
def carrier(d,q,m,rng,overlap=False):
    # m blocks; vertices b*d+y ; successor lists succ[b][z]
    V=m*d
    perm=list(range(V)); rng.shuffle(perm)
    succ=[perm[b*d:(b+1)*d] for b in range(m)]
    if overlap: succ=overlap
    arcs={}  # (x)->list of (y,gainexp)
    for b in range(m):
        rho=[rng.randrange(q) for _ in range(d)]; kap=[rng.randrange(q) for _ in range(d)]
        for y in range(d):
            arcs[b*d+y]=[(succ[b][z],(rho[z]+kap[y]+(q//d)*z*y)%q) for z in range(d)]
    return V,arcs
def hyp(V,arcs,q,start,d):
    # reachable (vertex,gain) sets by length; check stabilises to all pairs for block 0, counts grow
    cnt=np.zeros((V,q),dtype=object); cnt[start,0]=1
    for L in range(60):
        new=np.zeros((V,q),dtype=object)
        for x in range(V):
            for (y,g) in arcs[x]:
                new[y]+=np.roll(cnt[x],g)
        cnt=new
        if L>=8 and all(cnt[v,g]>=50 for v in range(d) for g in range(q)): return True
    return False
def run(d,q,m,seed,L=None,nev=30000,overlap=False):
    rng=random.Random(seed); red=setup(q)
    V,arcs=carrier(d,q,m,rng,overlap)
    ok=hyp(V,arcs,q,0,d)
    # A*A check
    z=np.exp(2j*np.pi/q); A=np.zeros((V,V),complex)
    for x in arcs:
        for (y,g) in arcs[x]: A[y,x]=z**g
    npres=np.allclose(A.conj().T@A,d*np.eye(V))
    if L is None: L=max(3,int(math.ceil(math.log(3000)/math.log(d))))
    walks=[(0,0)]
    for _ in range(L): walks=[(y,(g+h)%q) for (x,g) in walks for (y,h) in arcs[x]]
    keys={}; rows=[]
    def kid(c):
        k=normkey(c,q,red)
        if k not in keys: keys[k]=(len(keys),c.copy())
        return keys[k][0]
    kid(np.zeros(q,dtype=np.int64))
    nw=len(walks)
    for _ in range(nev):
        sz=rng.choice([1,2,2,3,3,4,5,6])
        if rng.random()<0.5:
            S=rng.sample(range(nw),sz)
        else: # bias towards few end vertices
            tv=set(rng.sample(range(V),min(V,2)))
            pool=[i for i in rng.sample(range(nw),min(nw,400)) if walks[i][0] in tv]
            S=pool[:sz]
            if not S: continue
        v=np.zeros((V,q),dtype=np.int64)
        for i in S: v[walks[i][0],walks[i][1]]+=1
        w=np.zeros((V,q),dtype=np.int64)
        for x in range(V):
            if v[x].any():
                for (y,g) in arcs[x]: w[y]+=np.roll(v[x],g)
        row={}
        for y in range(V):
            i=kid(w[y]); row[i]=row.get(i,0)+1
            i=kid(v[y]); row[i]=row.get(i,0)-d
        rows.append(row)
    n=len(keys); M=np.zeros((len(rows)+1,n))
    for r,row in enumerate(rows):
        for i,c in row.items(): M[r,i]=c
    M[-1,0]=1
    M=np.unique(M,axis=0)
    u,s,vt=np.linalg.svd(M,full_matrices=True)
    rank=int((s>1e-9*s[0]).sum()); N=vt[rank:].T   # n x nullity
    # well-constrained unknowns: appear in many equations
    occ=(M!=0).sum(0); good=np.argsort(-occ)[:min(n,40)]
    pr=np.linalg.svd(N[good],compute_uv=False) if N.shape[1] else np.array([])
    pdim=int((pr>1e-7).sum())
    # conjugate rules
    reps=[None]*n
    for k,(i,c) in keys.items(): reps[i]=c
    J=[j for j in range(1,q) if gcd(j,q)==1 and j<=q-j] if q>2 else [1]
    C=np.array([[abs(sum(c[e]*z**(j*e) for e in range(q)))**2 for j in J] for c in reps])
    resid=np.linalg.norm(M@C)
    # is conj span inside projection & equal?
    cg=C[good]; both=np.linalg.svd(np.hstack([N[good],cg]),compute_uv=False)
    jdim=int((both>1e-7).sum()); cdim=np.linalg.matrix_rank(cg,tol=1e-7)
    phi=len(J)
    print(f"d={d} q={q} m={m} seed={seed} hyp={ok} A*A=d:{npres} L={L} unknowns={n} eqs={len(M)} nullity={N.shape[1]} projdim(top40)={pdim} conjdim={cdim} joint={jdim} phi/2={phi} conj_resid={resid:.1e}",flush=True)
    return pdim,phi,ok,npres
if __name__=="__main__":
    bad=[]
    for (d,q) in [(3,3),(3,9),(5,5),(5,10),(4,8),(6,12),(7,7),(2,6),(3,6),(4,4),(3,12),(2,10)]:
        for m in (1,2):
            for seed in range(3):
                p,phi,ok,npres=run(d,q,m,seed,nev=12000)
                if ok and p!=phi: bad.append((d,q,m,seed,p,phi))
    print("MISMATCH among hyp-true:",bad)
