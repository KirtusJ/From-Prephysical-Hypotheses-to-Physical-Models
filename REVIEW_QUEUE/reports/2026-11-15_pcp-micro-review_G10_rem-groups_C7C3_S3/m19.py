# Predicates (fixed before run): P0 control = #classes S3 (expect 3). Per case: H(hyp) entries generate C, d>=2;
# U computed from rho(B)^*rho(B)=d; formula dim = 1 + real d(d+1)/2 + quat d(d-1)/2 + complex-pair d^2;
# N1 nullity of polynomial ansatz (deg<=2, no const) exact via sympy rank; N2 nullity of raw multiset system, sizes<=S. PASS iff all equal.
def rk(M):
    # exact rank: rational via sympy for small, else mod two large primes (integer matrix; agreement reported)
    import numpy as _np
    A0=_np.array(M.tolist(),dtype=object) if hasattr(M,'tolist') else _np.array(M,dtype=object)
    res=[]
    for p in (2147483629,2147483587):
        A=[[int(x)%p for x in row] for row in A0.tolist()]; r=0; ncol=len(A[0]) if A else 0
        for col in range(ncol):
            piv=next((i for i in range(r,len(A)) if A[i][col]),None)
            if piv is None: continue
            A[r],A[piv]=A[piv],A[r]; iv=pow(A[r][col],p-2,p); A[r]=[x*iv%p for x in A[r]]
            for i in range(len(A)):
                if i!=r and A[i][col]:
                    f=A[i][col]; A[i]=[(x-f*y)%p for x,y in zip(A[i],A[r])]
            r+=1
        res.append(r)
    assert res[0]==res[1]; return res[0]
import itertools, random, numpy as np, sympy as sp
from collections import Counter
def mul(p,q): return tuple(p[q[i]] for i in range(len(q)))  # p after q
def inv(p): r=[0]*len(p); [r.__setitem__(p[i],i) for i in range(len(p))]; return tuple(r)
def closure(gens):
    G={tuple(range(len(gens[0])))}; fr=list(G)
    while fr:
        nf=[]
        for g in fr:
            for s in gens:
                h=mul(s,g)
                if h not in G: G.add(h); nf.append(h)
        fr=nf
    return sorted(G)
def nclasses(G): return len({frozenset(mul(mul(x,g),inv(x)) for x in G) for g in G})
S3=closure([(1,2,0),(1,0,2)]); print("CONTROL:",nclasses(S3))
# C7:C3 on 7 points: a: i->i+1, b: i->2i
a=tuple((i+1)%7 for i in range(7)); b=tuple((2*i)%7 for i in range(7)); G21=closure([a,b])
def irreps(G,gens,genimgs):
    # build rep by BFS words
    R={tuple(range(len(G[0]))):np.eye(genimgs[0].shape[0],dtype=complex)}; fr=list(R)
    while fr:
        nf=[]
        for g in fr:
            for s,M in zip(gens,genimgs):
                h=mul(s,g)
                if h not in R: R[h]=M@R[g]; nf.append(h)
        fr=nf
    return R
w=np.exp(2j*np.pi/3); z=np.exp(2j*np.pi/7)
c,t=(1,2,0),(1,0,2)
S3reps={'triv':irreps(S3,[c,t],[np.eye(1),np.eye(1)]),'sign':irreps(S3,[c,t],[np.eye(1),-np.eye(1)]),
 'std':irreps(S3,[c,t],[np.array([[w,0],[0,w.conjugate()]]),np.array([[0,1],[1,0]])])}
P=np.array([[0,0,1],[1,0,0],[0,1,0]]).T
G21reps={'triv':irreps(G21,[a,b],[np.eye(1),np.eye(1)]),'l1':irreps(G21,[a,b],[np.eye(1),w*np.eye(1)]),
 'l2':irreps(G21,[a,b],[np.eye(1),w.conjugate()*np.eye(1)]),
 'r3':irreps(G21,[a,b],[np.diag([z,z**2,z**4]),P]),'r3b':irreps(G21,[a,b],[np.diag([z**6,z**5,z**3]),P])}
def check_reps(G,reps):
    assert sum(next(iter(R.values())).shape[0]**2 for R in reps.values())==len(G)
    for R in reps.values():
        for g in G:
            for h in G: assert np.allclose(R[mul(g,h)],R[g]@R[h])
def fs(G,R): return round(sum(np.trace(R[mul(g,g)]) for g in G).real/len(G))
def U_and_formula(G,reps,B):
    d=len(B); tot=1; U=[]; seenc=set()
    for n,R in reps.items():
        ok=all(np.allclose(sum(R[B[zz][y]].conj().T@R[B[zz][yp]] for zz in range(d)),0) for y in range(d) for yp in range(d) if y!=yp)
        if ok:
            k=R[G[0]].shape[0]; f=fs(G,R); U.append((n,k,f))
            if f==1: tot+=k*(k+1)//2
            elif f==-1: tot+=k*(k-1)//2
            else: tot+=k*k/2   # each member of the pair contributes half of d^2
    return U,tot
def lmat(G,g): idx={h:i for i,h in enumerate(G)}; M=np.zeros((len(G),)*2,dtype=int); [M.__setitem__((idx[mul(g,h)],i),1) for i,h in enumerate(G)]; return M
def ansatz_nullity(G,B):
    n=len(G); d=len(B); Ps=[[lmat(G,B[zz][y]) for y in range(d)] for zz in range(d)]
    # linear: sum_z a P_zy = d a
    rows=[]
    for y in range(d):
        M=sum(Ps[zz][y].T for zz in range(d))-d*np.eye(n,dtype=int); rows+=list(M)
    rl=rk([list(map(int,r)) for r in rows]); nl=n-rl
    pairs=[(i,j) for i in range(n) for j in range(i,n)]; pid={p:k for k,p in enumerate(pairs)}
    def bvar(i,j): return pid[(min(i,j),max(i,j))]
    eqs=set()
    for y in range(d):
        for yp in range(d):
            # sum_z P_zy^T b P_zy' - d delta b = 0, entrywise (i,j)
            perm=[ [int(np.argmax(Ps[zz][y][:,i])) for i in range(n)] for zz in range(d)]
            permp=[ [int(np.argmax(Ps[zz][yp][:,i])) for i in range(n)] for zz in range(d)]
            for i in range(n):
                for j in range(n):
                    r=Counter()
                    for zz in range(d): r[bvar(perm[zz][i],permp[zz][j])]+=1
                    if y==yp: r[bvar(i,j)]-=d
                    r={k:v for k,v in r.items() if v}
                    if r: eqs.add(tuple(sorted(r.items())))
    M=sp.zeros(len(eqs),len(pairs))
    for e,r in enumerate(eqs):
        for k,v in r: M[e,k]=v
    return nl+len(pairs)-rk(M)
def raw_nullity(G,B,S):
    n=len(G); d=len(B); idx={h:i for i,h in enumerate(G)}
    ms=[tuple(sorted(c)) for s in range(S+1) for c in itertools.combinations_with_replacement(range(n),s)]
    mid={m:k for k,m in enumerate(ms)}
    rows=set()
    def tr(g,m): return tuple(sorted(idx[mul(g,G[i])] for i in m))
    def rec(y,cur,left):
        if y==d:
            r=Counter()
            for zz in range(d):
                tot=tuple(sorted(sum((tr(B[zz][yy],cur[yy]) for yy in range(d)),())))
                r[mid[tot]]+=1
            for m in cur: r[mid[m]]-=d
            r={k:v for k,v in r.items() if v}
            if r: rows.add(tuple(sorted(r.items())))
            return
        for m in ms:
            if len(m)<=left: rec(y+1,cur+[m],left-len(m))
    rec(0,[],S)
    M=sp.zeros(len(rows),len(ms))
    for e,r in enumerate(rows):
        for k,v in r: M[e,k]=v
    return len(ms)-rk(M)
def gen(G,B): return len(closure([x for row in B for x in row]))==len(G)
cases={}
cases['S3 d2 (paper)']=(S3,S3reps,[[S3[0],c],[S3[0],t]],3)
# S3 d=6: search B with B_zy^{-1}B_zy' uniform over S3 for y!=y'
random.seed(1)
def search():
    B=[[None]*6 for _ in range(6)]
    for zz in range(6): B[zz][0]=S3[0]
    cols=[[S3[0]]*6]
    def ok(col):
        return all(len({mul(inv(cols[k][zz]),col[zz]) for zz in range(6)})==6 for k in range(len(cols)))
    for y in range(1,6):
        for _ in range(200000):
            col=random.sample(S3,6)
            if ok(col): cols.append(col); break
        else: return None
    return [[cols[y][zz] for y in range(6)] for zz in range(6)]
# exhaustive: d=6, columns c0=e (WLOG by right mult), c1,c2 with all pair quotient multisets uniform
from collections import Counter as _C
def unif(c1,c2,k): q=_C(mul(inv(x),y) for x,y in zip(c1,c2)); return len(q)==6 and set(q.values())=={k}
e=S3[0]; cnt=0
for c1 in itertools.permutations(S3):
    if not unif([e]*6,c1,1): continue
    for c2 in itertools.permutations(S3):
        if unif([e]*6,c2,1) and unif(c1,c2,1): cnt+=1
print('d=6: triples of columns with uniform quotients:',cnt)
def search12(d=12,tries=4000):
    base=[x for x in S3 for _ in range(2)]
    for _ in range(tries):
        cols=[[e]*d]
        for y in range(1,d):
            for _ in range(3000):
                col=random.sample(base,d)
                if all(unif(cc,col,2) for cc in cols): cols.append(col); break
            else: break
        if len(cols)==d: return [[cols[y][zz] for y in range(d)] for zz in range(d)]
    return None
B12=search12(); print('d=12 found:',B12 is not None)
if B12: cases['S3 d12 sign+std']=(S3,S3reps,B12,None)
e21=G21[0]; bb=b
def pw(g,k):
    r=e21
    for _ in range(k): r=mul(g,r)
    return r
# d=3: B_zy = r_z bb^{zy}, r_0=e, r_1=a: 1-dim complex pair qualifies
B3=[[mul(rz,pw(bb,zz*y)) for y in range(3)] for zz,rz in enumerate([e21,a,e21])]
cases['C7:C3 d3 1-dim complex pair']=(G21,G21reps,B3,2)
# d=7: B_zy = a^{zy} s_y with s_1=b
B7=[[mul(pw(a,zz*y),(bb if y==1 else e21)) for y in range(7)] for zz in range(7)]
cases['C7:C3 d7 3-dim complex pair']=(G21,G21reps,B7,None)
check_reps(S3,S3reps); check_reps(G21,G21reps)
for name,(G,reps,B,S) in cases.items():
    U,f=U_and_formula(G,reps,B); h=gen(G,B)
    n1=ansatz_nullity(G,B); n2=raw_nullity(G,B,S) if S else 'skipped'
    print(name,'| H=C:',h,'| U:',U,'| formula:',f,'| ansatz nullity:',n1,'| raw multiset nullity size<=%s:'%S,n2, flush=True)
