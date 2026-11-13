# micro-review thm:periodic. Predicates fixed before run:
# P1 r=1 two-vertex: r=1,C0=C,U={sign},nullity(S<=3)=2
# P2 trivial group bipartite: r=2,U empty,nullity=1
# P3 ring N=4 (and N=2): r=r0=2,C0=C,U={sign},nullity=2; parity-dependent constants violate an actual event
# P4 g*[[1,1],[1,1]] q=2,4: hat D strongly connected, r=q,r0=1,C0 trivial,U empty,nullity=1
# P5 four-vertex q=4: all walks to y at each length 1..7 in one C0-coset; two families agree on mu, both consistent
import itertools, random, math
from math import gcd
from flint import fmpq_mat
from collections import deque
def analyse(V, arcs, q, x0=0):
    # arcs: list (tail, head, exp)
    out={y:[] for y in V}
    for t,h,e in arcs: out[t].append((h,e%q))
    H=[(y,g) for y in V for g in range(q)]
    def bfs(s):
        dist={s:0}; dq=deque([s])
        while dq:
            u=dq.popleft()
            for z,e in out[u[0]]:
                v=(z,(u[1]+e)%q)
                if v not in dist: dist[v]=dist[u]+1; dq.append(v)
        return dist
    dist=bfs((x0,0))
    sc = len(dist)==len(H) and all(len(bfs(u))==len(H) for u in H)
    r=0
    for u in dist:
        for z,e in out[u[0]]:
            v=(z,(u[1]+e)%q); r=gcd(r,dist[u]+1-dist[v])
    # r0
    def bfsD(s):
        d={s:0}; dq=deque([s])
        while dq:
            u=dq.popleft()
            for z,e in out[u]:
                if z not in d: d[z]=d[u]+1; dq.append(z)
        return d
    dd=bfsD(x0); r0=0
    for u in dd:
        for z,e in out[u]: r0=gcd(r0,dd[u]+1-dd[z])
    kap={u:dist[u]%r for u in dist}
    fib={(i,y):sorted(g for g in range(q) if kap[(y,g)]==i) for i in range(r) for y in V}
    C0=fib[(0,x0)]
    # U(D) exact via integer polynomial in omega mod cyclotomic: use complex check with q|4 exact else float
    U=[]
    import cmath
    for j in range(q):
        ok=True
        for y in V:
            for y1 in V:
                s=0
                for z,e in out[y]:
                    for z1,e1 in out[y1]:
                        if z==z1: s+=cmath.exp(2j*cmath.pi*j*(e1-e)/q)
                tgt=len(out[y]) if y==y1 else 0
                if abs(s-tgt)>1e-9: ok=False
        if ok: U.append(j)
    return out,sc,r,r0,kap,fib,C0,U
def multisets(support,S):
    res=[]
    for n in range(0,S+1):
        for c in itertools.combinations_with_replacement(support,n): res.append(c)
    return res
def nullity(V,out,q,r,fib,S,d):
    # unknowns F_y(m), m fibre-supported nonzero size<=S
    idx={}
    for (i,y),f in fib.items():
        if f:
            for m in multisets(f,S):
                if m: idx.setdefault((y,m),len(idx))
    rows=[]
    for i in range(r):
        slots=[(y,g) for y in V for g in fib[(i,y)]]
        for n in range(1,S+1):
            for fam in itertools.combinations_with_replacement(slots,n):
                row={}
                my={}
                for y,g in fam: my.setdefault(y,[]).append(g)
                w={}
                for y,gs in my.items():
                    k=(y,tuple(sorted(gs))); row[idx[k]]=row.get(idx[k],0)-d
                    for z,e in out[y]:
                        w.setdefault(z,[]).extend((g+e)%q for g in gs)
                for z,gs in w.items():
                    k=(z,tuple(sorted(gs))); row[idx[k]]=row.get(idx[k],0)+1
                rows.append(row)
    M=fmpq_mat(len(rows),len(idx))
    for a,row in enumerate(rows):
        for b,v in row.items(): M[a,b]=v
    return len(idx)-M.rank(), len(idx), len(rows)
def report(name,V,arcs,q,S=3,d=2):
    out,sc,r,r0,kap,fib,C0,U=analyse(V,arcs,q)
    nl=nullity(V,out,q,r,fib,S,d)
    Ures=sorted(set(tuple(sorted({(j*g)%q for g in C0})) and tuple((j*g)%q for g in C0) for j in U))
    cls=set()
    for t in Ures:
        inv=tuple((-a)%q for a in t); cls.add(min(t,inv))
    print(name,'hatD_sc',sc,'r',r,'r0',r0,'C0',C0,'U',U,'U|C0 classes',len(cls),'nullity,unknowns,eqs',nl,'expected dim',1+len(cls))
    print('   fibres',{k:v for k,v in fib.items()})
    return out,r,fib,C0,U
# 1
report('P1 2-vertex C2',[0,1],[(0,0,0),(0,1,0),(1,0,0),(1,1,1)],2)
# 2
report('P2 trivial bipartite',[0,1,2,3],[(0,2,0),(0,3,0),(1,2,0),(1,3,0),(2,0,0),(2,1,0),(3,0,0),(3,1,0)],1,S=4)
# 3
def ring(N):
    V=list(range(2*N)) # (x,R)=2x,(x,L)=2x+1
    arcs=[]
    for x in range(N):
        for s in (0,1):
            arcs.append((2*x+s,2*((x+1)%N),0))
            arcs.append((2*x+s,2*((x-1)%N)+1,1 if s==1 else 0))
    return V,arcs
for N in (2,4):
    V,arcs=ring(N); out,r,fib,C0,U=report('P3 ring N=%d'%N,V,arcs,2)
def walks(out,q,n,x0=0):
    W=[(x0,0)]
    L=[W]
    ws=[((x0,),0)]
    for _ in range(n):
        ws=[(p+(z,),(g+e)%q) for p,g in ws for z,e in out[p[-1]]]
    return ws
def mu(F,S):
    my={}
    for p,g in S: my.setdefault(p[-1],[]).append(g)
    return sum(F(y,tuple(sorted(gs))) for y,gs in my.items())
def ext(out,q,S): return [(p+(z,),(g+e)%q) for p,g in S for z,e in out[p[-1]]]
V,arcs=ring(4); out=analyse(V,arcs,2)[0]
Fpar=lambda y,m:(1 if (y//2)%2==0 else 2)*(m.count(0)-m.count(1))**2
Fsame=lambda y,m:(m.count(0)-m.count(1))**2
found=None;bad_same=0
for n in range(1,6):
    ws=walks(out,2,n)
    for S in itertools.combinations(ws,2):
        S=list(S)
        if mu(Fsame,ext(out,2,S))!=2*mu(Fsame,S): bad_same+=1
        if found is None and mu(Fpar,ext(out,2,S))!=2*mu(Fpar,S):
            found=(n,S,mu(Fpar,S),mu(Fpar,ext(out,2,S)))
print('P3 violation of parity rule (c_even=1,c_odd=2): length,S,mu(S),mu(ExtS)',found,'; same-constant rule violations on pairs:',bad_same)
# 4
for q in (2,4):
    report('P4 g*J q=%d'%q,[0,1],[(0,0,1),(0,1,1),(1,0,1),(1,1,1)],q,S=3)
# 5
V=[0,1,2,3]; arcs=[(0,2,0),(0,3,1),(1,0,1),(1,1,3),(2,0,0),(2,1,0),(3,2,0),(3,3,3)]
out,r,fib,C0,U=report('P5 four-vertex q=4 (tail,head,exp)',V,arcs,4)
arcs2=[(h,t,e) for t,h,e in arcs]
try: report('P5alt (head,tail,exp)',V,arcs2,4)
except Exception as ex: print('alt fail',ex)
def sq(m): return (m.count(0)-m.count(2))**2+(m.count(1)-m.count(3))**2
onfib=lambda m: len({g%len([1]) for g in m})>=0 and len({g%2 for g in m})<=1
F1=lambda y,m:3*len(m)+5*sq(m)
F2=lambda y,m:F1(y,m)+(0 if onfib(m) else 7*(y+1)+len(m))
random.seed(10)
allcoset=True; diff=0; inc1=0; inc2=0; nev=0
for n in range(1,7):
    ws=walks(out,4,n)
    per={}
    for p,g in ws: per.setdefault(p[-1],set()).add(g%2)
    if any(len(s)>1 for s in per.values()): allcoset=False
    for _ in range(3000):
        S=[w for w in ws if random.random()<random.choice([.1,.5,.9])]
        nev+=1
        if mu(F1,S)!=mu(F2,S): diff+=1
        E=ext(out,4,S)
        if mu(F1,E)!=2*mu(F1,S): inc1+=1
        if mu(F2,E)!=2*mu(F2,S): inc2+=1
print('P5 C0=',C0,'one coset per vertex per length 1..6:',allcoset,'events',nev,'mu differ',diff,'inconsistent F1,F2',inc1,inc2,'F1 vs F2 on off-fibre m=(0,1) at y=0:',F1(0,(0,1)),F2(0,(0,1)))
