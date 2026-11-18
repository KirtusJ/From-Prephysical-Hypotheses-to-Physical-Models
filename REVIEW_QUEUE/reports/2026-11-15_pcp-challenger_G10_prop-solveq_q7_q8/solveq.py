"""Challenger check of G10 Prop 5.35 (prop:solveq). Predicates fixed before first run:
P0 control: rank_Q [[1,2,3],[4,5,6],[7,8,9]] == 2.
P1 (per q in {7,8}, box entries<=B): unknowns F_R(m),F_L(m) for m in {0..B}^q, F(0)=0 imposed.
   Hypothesis test per case: an equation (U,V) qualifies iff U+V and U+TV lie in the box; count reported.
   Truncated solution dim (= #vars - rank, mod p1 and p2, ranks must agree) equals 1 (q odd) / 2 (q even).
   Upper bound from qualifying equations; lower bound = rank of claimed solutions restricted to box.
P2 claimed solutions (|m|, eps(m)^2) satisfy every qualifying equation exactly (integers).
P3 F_R==F_L forced: every null vector has equal R and L parts.
Seed 20261115 (row sampling for B=2, if used)."""
import itertools, sys, random, numpy as np
random.seed(20261115)
def rank_mod(M,p):
    M=M.copy()%p; r=0; rows,cols=M.shape
    for c in range(cols):
        piv=np.nonzero(M[r:,c])[0]
        if len(piv)==0: continue
        i=r+piv[0]; M[[r,i]]=M[[i,r]]
        M[r]=(M[r]*pow(int(M[r,c]),p-2,p))%p
        nz=np.nonzero(M[:,c])[0]; nz=nz[nz!=r]
        M[nz]=(M[nz]-np.outer(M[nz,c],M[r]))%p
        r+=1
        if r==rows: break
    return r, M[:r]
out=open(sys.argv[1],'x')
def W(s): print(s); out.write(s+'\n')
import fractions, sympy
W("P0 control rank=%d"%sympy.Matrix([[1,2,3],[4,5,6],[7,8,9]]).rank())
P1,P2=1000003,998244353
for q,B in [(7,1),(8,1),(7,2)]:
    box=list(itertools.product(range(B+1),repeat=q)); idx={m:i for i,m in enumerate(box)}; n=len(box)
    T=lambda m: m[-1:]+m[:-1]   # (Tm)(h^j)=m(h^{j-1})
    rows=[]; qual=0; tot=0
    pairs=itertools.product(box,box) if B==1 else ((random.choice(box),random.choice(box)) for _ in range(60000))
    p2fail=0
    for U,V in pairs:
        tot+=1
        s=tuple(a+b for a,b in zip(U,V)); t=tuple(a+b for a,b in zip(U,T(V)))
        if max(s)>B or max(t)>B: continue
        qual+=1
        r={}
        def add(k,v): r[k]=r.get(k,0)+v
        add(idx[s],1); add(n+idx[t],1); add(idx[U],-2); add(n+idx[V],-2)
        rows.append(r)
        e=lambda m: sum((-1)**j*m[j] for j in range(q))
        for f in (sum, lambda m:e(m)**2):
            if f(s)+f(t)!=2*f(U)+2*f(V): p2fail+=1
    # F(0)=0
    z=idx[tuple([0]*q)]; rows.append({z:1}); rows.append({n+z:1})
    M=np.zeros((len(rows),2*n),dtype=np.int64)
    for i,r in enumerate(rows):
        for k,v in r.items(): M[i,k]=v
    rk=[rank_mod(M,p)[0] for p in (P1,P2)]
    dim=2*n-rk[0]
    e=lambda m: sum((-1)**j*m[j] for j in range(q))
    S=np.array([[sum(m) for m in box]*2,[e(m)**2 for m in box]*2],dtype=np.int64)
    lb=rank_mod(S if q%2==0 else S[:1],P1)[0]
    exp=1 if q%2 else 2
    # P3: add F_R-F_L=0 rows, dim should not change
    D2=np.hstack([np.eye(n,dtype=np.int64),-np.eye(n,dtype=np.int64)])
    dim3=2*n-rank_mod(np.vstack([M,D2]),P1)[0]
    W(f"q={q} B={B} vars={2*n} pairs tried={tot} qualifying={qual} rank p1={rk[0]} p2={rk[1]} dim={dim} lower={lb} expected={exp} P1={'PASS' if rk[0]==rk[1] and dim==exp==lb else 'FAIL'} P2fails={p2fail} P3={'PASS' if dim3==dim else 'FAIL'}")
