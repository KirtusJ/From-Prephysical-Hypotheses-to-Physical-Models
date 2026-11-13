# exploratory (no predicate): identify the two extra solutions for q0=12, u = {1, z, -1, -z}
import itertools, numpy as np
z=np.exp(2j*np.pi/12); s3=np.sqrt(3.0); Z1=z**np.arange(4); Z5=z**(5*np.arange(4))
T=np.array([[0,0,0,-1],[1,0,0,0],[0,1,0,1],[0,0,1,0]],dtype=np.int64)
def mulz(c,e): return c@np.linalg.matrix_power(T,e%12).T
def key(c):
    n1=np.abs(c@Z1)**2; n5=np.abs(c@Z5)**2; return np.rint((n1+n5)/2).astype(np.int64), np.rint((n1-n5)/(2*s3)).astype(np.int64)
A=np.array(list(itertools.product(range(-3,4),repeat=4)),dtype=np.int64); B=np.array(list(itertools.product(range(-2,3),repeat=4)),dtype=np.int64)
cols=[]
for e in (0,1,6,7):
    p,q=key((A[:,None,:]+mulz(B,e)[None,:,:]).reshape(-1,4)); cols.append(p*100003+q)
pa,qa=key(A); pb,qb=key(B)
rows=np.unique(np.concatenate([np.sort(np.stack(cols,1),1),np.repeat(pa*100003+qa,len(B))[:,None],np.tile(pb*100003+qb,len(A))[:,None]],1),axis=0)
allk=np.unique(rows); ix={int(k):i for i,k in enumerate(allk)}; n=len(allk); G=np.zeros((n,n))
for r in rows:
    row={}
    for k in r[:4]: row[ix[int(k)]]=row.get(ix[int(k)],0)+1
    for k in r[4:]: row[ix[int(k)]]=row.get(ix[int(k)],0)-4
    js=[j for j,v in row.items() if v]
    if js: vs=np.array([row[j] for j in js],float); G[np.ix_(js,js)]+=np.outer(vs,vs)
G[ix[0],ix[0]]+=1
ev,U=np.linalg.eigh(G); W=U[:,:4]
P=np.array([(k+50000)//100003 for k in allk]); Q=allk-P*100003
# express null space in terms of low keys: solve for basis with values at 4 chosen keys
print("eigs",ev[:6])
for deg in (1,2,3,4):
    mons=[(i,j) for i in range(deg+1) for j in range(deg+1-i)]
    X=np.stack([P.astype(float)**i*Q.astype(float)**j for i,j in mons],1)
    c,res,rk,sv=np.linalg.lstsq(X,W,rcond=None); print("deg",deg,"residual of null space vs polynomials in (p,q):",np.linalg.norm(X@c-W))
for m in (2,3,4,6):
    cls=(P%m)*m+(Q%m); X=np.concatenate([np.stack([(cls==c)*1.0,(cls==c)*P,(cls==c)*Q],1) for c in np.unique(cls)],1)
    c,res,rk,sv=np.linalg.lstsq(X,W,rcond=None); print("mod",m,"residual vs residue-class-wise linear in (p,q):",np.linalg.norm(X@c-W), "rank",rk)
np.save("extra_keys.npy",np.stack([P,Q],1)); np.save("extra_W.npy",W)
