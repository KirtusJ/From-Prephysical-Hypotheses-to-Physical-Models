"""Challenger program for the block law.  Predicates fixed before first run:
P1  R=Z, B=[[1,1],[1,-1]]: inner-window solution dim = 1.
P2  R=Z[i], B=[[1,i],[1,-i]]: inner dim = 1.
P2b R=Z[i], B=[[1,1],[1,-1]]: inner dim = 3.
P3  R=Z[w], Fourier 3, all inputs: inner dim = 1.
P3b same, only two-input events: inner dim > 1.
P4  globally defined functions, quadratic polynomial per coset of dR (independent per coset, with linear and constant parts):
    solution dims 1,1,3,1 for the four blocks (exact rank mod p on random beta, no boundary).
Hypothesis B*B=d is tested per block. Inner window = box of half size N//2 (floor); 0 belongs to the window.
Ranks are mod p=2^31-1: nullity mod p >= nullity over Q, so a dim equal to the known lower bound is exact.
"""
import numpy as np, itertools, random, sys
p=2147483647
def rref(M):
    M=M.copy()%p; m,n=M.shape; piv=[]; r=0
    for c in range(n):
        nz=np.nonzero(M[r:,c])[0]
        if len(nz)==0: continue
        i=r+nz[0]; M[[r,i]]=M[[i,r]]
        M[r]=M[r]*pow(int(M[r,c]),p-2,p)%p
        f=M[:,c].copy(); f[r]=0
        idx=np.nonzero(f)[0]
        if len(idx): M[idx]=(M[idx]-f[idx,None]*M[r][None,:])%p
        piv.append(c); r+=1
        if r==m: break
    return M[:r],piv
def nullspace(M,n):
    Rm,piv=rref(M); free=[c for c in range(n) if c not in piv]
    N=np.zeros((len(free),n),dtype=np.int64)
    for k,f in enumerate(free):
        N[k,f]=1
        for r,c in enumerate(piv): N[k,c]=(-Rm[r,f])%p
    return N
def rank(M): return len(rref(M)[1]) if M.size else 0
# rings: elements as integer tuples; mult by unit given as matrix
class Ring:
    def __init__(s,name,rk,mulz): s.name=name; s.rk=rk; s.mulz=np.array(mulz)  # matrix of mult by zeta
    def unit(s,t): return np.linalg.matrix_power(s.mulz,t)
Z=Ring('Z(q=2)',1,[[-1]])
Zi=Ring('Z[i](q=4)',2,[[0,-1],[1,0]])
Zw=Ring('Z[w](q=3)',2,[[0,-1],[1,-1]])   # w*(a+bw)= -b + (a-b)w
def conjmat(R,q):  # conj of zeta^t is zeta^(q-t)
    return lambda t: R.unit((q-t)%q)
def check_hyp(R,q,E):
    d=len(E)
    for y in range(d):
        for y2 in range(d):
            s=sum(R.unit((E[z][y2]-E[z][y])%q) for z in range(d))
            want=d*np.eye(R.rk,dtype=int) if y==y2 else 0*np.eye(R.rk,dtype=int)
            if not (s==want).all(): return False
    return True
def apply(R,E,beta,q):
    d=len(E); out=[]
    for z in range(d):
        v=np.zeros(R.rk,dtype=int)
        for y in range(d): v=v+R.unit(E[z][y]%q)@np.array(beta[y])
        out.append(tuple(int(x) for x in v))
    return out
def box_solve(R,q,E,N,inputs=None,tag=''):
    d=len(E); pts=list(itertools.product(range(-N,N+1),repeat=R.rk)); ix={a:i for i,a in enumerate(pts)}
    n=len(pts); rows=set(); zero=(0,)*R.rk
    supp=inputs or [tuple(range(d))]
    for S in supp:
        for vals in itertools.product(pts,repeat=len(S)):
            beta=[zero]*d
            for y,v in zip(S,vals): beta[y]=v
            out=apply(R,E,beta,q)
            if any(o not in ix for o in out): continue
            row={}
            for o in out: row[ix[o]]=row.get(ix[o],0)+1
            for b in beta: row[ix[b]]=row.get(ix[b],0)-d
            rows.add(tuple(sorted((k,v) for k,v in row.items() if v)))
    rows.discard(())
    M=np.zeros((len(rows),n),dtype=np.int64)
    for r,row in enumerate(rows):
        for k,v in row: M[r,k]=v%p
    NS=nullspace(M,n); w=N//2
    win=[i for a,i in ix.items() if all(abs(x)<=w for x in a)]
    inner=rank(NS[:,win]) if len(NS) else 0
    print(f'{tag} {R.name} N={N} unknowns={n} eqs={len(rows)} full_dim={len(NS)} inner_window(|x|<={w})_dim={inner}',flush=True)
    return inner
def coset_family(R,q,E,tag,trials=None):
    d=len(E); rk=R.rk; cos=list(itertools.product(range(d),repeat=rk)); ci={c:i for i,c in enumerate(cos)}
    mons=[()]+[(i,) for i in range(rk)]+[(i,j) for i in range(rk) for j in range(i,rk)]
    npar=len(cos)*len(mons)
    def vec(a,coef):
        v=np.zeros(npar,dtype=object); c=ci[tuple(x%d for x in a)]
        for k,m in enumerate(mons):
            t=1
            for i in m: t*=a[i]
            v[c*len(mons)+k]+=coef*t
        return v
    rng=random.Random(12345); rows=[]
    for _ in range(trials or 40*npar):
        beta=[tuple(rng.randint(-9,9) for _ in range(rk)) for _ in range(d)]
        out=apply(R,E,beta,q)
        v=sum(vec(o,1) for o in out)+sum(vec(b,-d) for b in beta)
        rows.append([int(x)%p for x in v])
    M=np.array(rows,dtype=np.int64); dim=npar-rank(M)
    print(f'{tag} {R.name} coset-quadratic family: params={npar} cosets={len(cos)} solution_dim={dim}',flush=True)
    return dim
res={}
H2=[[0,0],[0,1]]          # exponents: Z: (-1)^t
blocks=[('P1',Z,2,[[0,0],[0,1]],1,[6,10,20,40]),
        ('P2',Zi,4,[[0,1],[0,3]],1,[2,4,6]),
        ('P2b',Zi,4,[[0,0],[0,2]],3,[2,4,6]),
        ('P3',Zw,3,[[0,0,0],[0,1,2],[0,2,1]],1,[2,3,4])]
qual=0
for tag,R,q,E,exp,Ns in blocks:
    ok=check_hyp(R,q,E); qual+=ok; print(tag,'hypothesis B*B=d:',ok)
    if not ok: continue
    for N in Ns:
        got=box_solve(R,q,E,N,tag=tag); print(f'  predicate {tag} (dim={exp}):', 'PASS' if got==exp else 'FAIL')
    got=coset_family(R,q,E,'P4/'+tag); print(f'  predicate P4/{tag} (dim={exp}):','PASS' if got==exp else 'FAIL')
print('qualifying blocks:',qual,'of',len(blocks))
F3=[[0,0,0],[0,1,2],[0,2,1]]
for N in [2,3,4,6]:
    got=box_solve(Zw,3,F3,N,inputs=[(0,1),(0,2),(1,2)],tag='P3b two-input'); print('  predicate P3b (dim>1):','PASS' if got>1 else 'FAIL')
