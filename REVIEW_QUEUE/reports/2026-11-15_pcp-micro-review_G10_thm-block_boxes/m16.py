import sys, itertools, random, math, numpy as np
sys.path.insert(0,'/home/user/From-Prephysical-Hypotheses-to-Physical-Models/REVIEW_QUEUE/lib')
from pcplib import Ring
print("CONTROL:", sum(1 for k in range(1,11) if math.gcd(k,10)==1))
P=2147483629
def rankmod(M):
    M=M.copy()%P; r=0; piv=[]
    for c in range(M.shape[1]):
        nz=np.nonzero(M[r:,c])[0]
        if len(nz)==0: continue
        i=r+nz[0]; M[[r,i]]=M[[i,r]]
        M[r]=M[r]*pow(int(M[r,c]),P-2,P)%P
        o=np.nonzero(M[:,c])[0]
        for j in o:
            if j!=r: M[j]=(M[j]-M[j,c]*M[r])%P
        piv.append(c); r+=1
        if r==M.shape[0]: break
    return M[:r],piv
def run(name,q,B,L,r,nsamp=None,expect=None,seed=1):
    R=Ring(q); n=R.n; d=len(B)
    els=list(itertools.product(range(-L,L+1),repeat=n)); idx={e:i for i,e in enumerate(els)}
    # hypothesis: B*B=d numerically
    import cmath; z=cmath.exp(2j*math.pi/q); Bc=np.array([[z**k for k in row] for row in B])
    hyp=np.allclose(Bc.conj().T@Bc,d*np.eye(d)); g=math.gcd(q,*[k for row in B for k in row]); qB=q//g
    rows=[]
    src=els if nsamp is None else None
    rnd=random.Random(seed)
    inner=[e for e in els if max(map(abs,e))<=max(1,L//2)]
    it=itertools.product(els,repeat=d) if nsamp is None else ( [rnd.choice(inner) for _ in range(d)] for _ in range(nsamp))
    for beta in it:
        out=[]
        ok=True
        for z_ in range(d):
            s=R.zero()
            for y in range(d): s=R.add(s,R.mulz(beta[y],B[z_][y]))
            if max(map(abs,s))>L: ok=False;break
            out.append(s)
        if not ok: continue
        v=np.zeros(len(els),dtype=np.int64)
        for s in out: v[idx[s]]+=1
        for b in beta: v[idx[b]]-=d
        rows.append(v%P)
    A=np.array(rows,dtype=np.int64)
    E,piv=rankmod(A)
    N=len(els); free=[c for c in range(N) if c not in set(piv)]
    # nullspace basis
    basis=[]
    for f in free:
        x=np.zeros(N,dtype=np.int64); x[f]=1
        for k,c in enumerate(piv): x[c]=(-E[k,f])%P
        basis.append(x)
    I=[idx[e] for e in els if max(map(abs,e))<=r]
    dimI=len(rankmod(np.array(basis)[:,I])[1]) if basis else 0
    print(f"{name}: q={q} d={d} qB={qB} hyp B*B=d:{hyp} L={L} unknowns={N} eqs={len(rows)} nullity={len(free)} interior(r={r},{len(I)} pts) dim={dimI} expected={expect} ->",'PASS' if dimI==expect else 'FAIL',flush=True)
F4=[[(z*y)%4 for y in range(4)] for z in range(4)]
H4=[[0,0,0,0],[0,2,0,2],[0,0,2,2],[0,2,2,0]]
B6=[[0,0,3],[0,2,1],[0,4,5]]  # -1=z^3, -w^2=z^(4+3)=z, -w=z^5
F5=[[(z*y)%5 for y in range(5)] for z in range(5)]
mode=sys.argv[1]
if mode=='c':
  for L,r in [(2,1),(3,2)]: run('B6 d=3 order 6',6,B6,L,r,nsamp=None if L==2 else 60000,expect=1)
elif mode=='a':
  for L,r in [(2,1),(3,2)]:
    run('Fourier d=4',4,F4,L,r,nsamp=None if L==2 else 60000,expect=1)
    run('Hadamard d=4 q=4 (subgroup control)',4,H4,L,r,nsamp=None if L==2 else 60000,expect=3)
    run('B6 d=3 order 6',6,B6,L,r,nsamp=None if L==2 else 60000,expect=1)
else:
  for L,r in [(2,1),(3,1)]:
    run('Fourier d=5 order 5',5,F5,L,r,nsamp=30000 if L==2 else 60000,expect=2)
