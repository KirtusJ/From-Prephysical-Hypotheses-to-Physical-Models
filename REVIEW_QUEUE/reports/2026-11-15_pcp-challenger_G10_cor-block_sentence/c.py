"""Predicates fixed before run:
P0 control: count 2x2 {+-1} matrices with orthogonal columns (expect 8).
P1 every generated carrier satisfies A^*A=2 (hypothesis test per carrier).
P2 (claim of the sentence) every finite norm-preserving deg-2 carrier is abundant in the corollary's sense
   (some block, some length L in 40..120, every q-th root gain of >=5 walks to both block vertices, from vertex 0). Expected to FAIL on some.
P3 on abundant carriers the abundance gains = all q (trivially by def); report counts by q.
"""
import itertools,random,cmath
random.seed(16)
c=sum(1 for a,b,cc,d in itertools.product([1,-1],repeat=4) if a*b+cc*d==0); print("CONTROL",c)
def carrier(nb,q):
    perm=list(range(nb)); random.shuffle(perm); arcs=[]
    for b in range(nb):
        k1,k2,k3=[random.randrange(q) for _ in range(3)]; k4=(k3-k1+k2+q//2)%q
        x,xp=2*b,2*b+1; y,yp=2*perm[b],2*perm[b]+1
        arcs+= [(x,y,k1),(xp,y,k2),(x,yp,k3),(xp,yp,k4)]
    return arcs
def nphyp(arcs,n,q):
    z=[cmath.exp(2j*cmath.pi*k/q) for k in range(q)]
    A=[[0]*n for _ in range(n)]
    for s,t,k in arcs: A[t][s]+=z[k]
    return all(abs(sum(A[r][i].conjugate()*A[r][j] for r in range(n))-(2 if i==j else 0))<1e-9 for i in range(n) for j in range(n))
def abundant(arcs,n,q,N=5):
    cnt={(0,0):1}
    for L in range(1,121):
        new={}
        for (v,g),c in cnt.items():
            for s,t,k in arcs:
                if s==v: new[(t,(g+k)%q)]=new.get((t,(g+k)%q),0)+c
        cnt=new
        if L>=40:
            for b in range(n//2):
                if all(cnt.get((x,g),0)>=N for x in (2*b,2*b+1) for g in range(q)): return True
    return False
res={}
for q in (2,4,6,8):
  for t in range(60):
    nb=random.randint(1,4); a=carrier(nb,q); n=2*nb
    h=nphyp(a,n,q); ab=abundant(a,n,q) if h else None
    r=res.setdefault(q,[0,0,0]); r[0]+=1; r[1]+=h; r[2]+=bool(ab)
# ring with signs: periodic example, even sites, built as blocks? record separately
with open("results.txt","x") as f:
  for q,r in res.items(): s=f"q={q} carriers={r[0]} hyp={r[1]} abundant={r[2]}"; print(s); f.write(s+"\n")
  f.write(f"P0 {c==8} P1 {all(r[0]==r[1] for r in res.values())} P2 {all(r[1]==r[2] for r in res.values())}\n")
print(open("results.txt").read())
