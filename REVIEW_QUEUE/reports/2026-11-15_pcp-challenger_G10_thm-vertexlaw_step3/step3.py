"""Challenger test of G10 Thm 5.22 Step 3 (claim: a solution of (GL) that vanishes on
multisets of size <N vanishes on size N, N>=3). Exact rational elimination.
Predicates fixed before first run:
 P0 control: (A^5)_{00}=11 for directed 3-cycle with loops (computed).
 P1 for every carrier passing hyp() (finite, abelian C, outdegree exactly d>=2, no parallel
    arcs): kernel of the total-size-3 equations in unknowns G_z(m), |m|=3, is 0.
 P2 same for N=4 on the small carriers.
 P3 hypothesis-failing carriers (d=1; parallel loops) have nonzero kernel.
Count of qualifying carriers reported. Result file opened mode 'x'.
"""
import itertools, random, sys
from fractions import Fraction
random.seed(20261115)
def grp(orders): return list(itertools.product(*[range(o) for o in orders]))
def add(a,b,orders): return tuple((x+y)%o for x,y,o in zip(a,b,orders))
def msets(G,n): return list(itertools.combinations_with_replacement(range(len(G)),n))
def rank(rows,ncol):
    rows=[dict(r) for r in rows if r]; piv={}; r=0
    for row in rows:
        row={k:Fraction(v) for k,v in row.items() if v}
        for c in sorted(piv):
            if c in row:
                f=row[c]; 
                for k,v in piv[c].items(): row[k]=row.get(k,0)-f*v
                row={k:v for k,v in row.items() if v}
        if row:
            c=min(row); f=row[c]; row={k:v/f for k,v in row.items()}
            for c2 in piv:
                if c in piv[c2]:
                    g=piv[c2][c]; piv[c2]={k:piv[c2].get(k,0)-g*row.get(k,0) for k in set(piv[c2])|set(row)}
                    piv[c2]={k:v for k,v in piv[c2].items() if v}
            piv[c]=row
    return len(piv)
def kernel(V,arcs,orders,N,Kmax=None):
    # arcs: list (y,z,gain) ; parallel allowed for P3
    G=grp(orders); gi={g:i for i,g in enumerate(G)}
    sizes=[N] if Kmax is None else list(range(N,Kmax+1))
    idx={}
    for z in range(V):
        for n in sizes:
            for m in msets(G,n): idx[(z,m)]=len(idx)
    outd=[sum(1 for a in arcs if a[0]==y) for y in range(V)]
    d=outd[0]
    rows=[]
    # families with total size N
    def comps(n,k):
        if k==1: yield (n,); return
        for i in range(n+1):
            for r in comps(n-i,k-1): yield (i,)+r
    for sz in comps(N,V):
        choices=[msets(G,s) for s in sz]
        for fam in itertools.product(*choices):
            row={}
            for z in range(V):
                w=[]
                for (y,zz,g) in arcs:
                    if zz==z: w+= [gi[add(G[h],g,orders)] for h in fam[y]]
                if len(w)>=N: k=(z,tuple(sorted(w))); row[idx[k]]=row.get(idx[k],0)+1
            for y in range(V):
                if len(fam[y])>=N: k=(y,fam[y]); row[idx[k]]=row.get(idx[k],0)-d
            rows.append(row)
    return len(idx)-rank(rows,len(idx))
def hyp(V,arcs):
    od=[sum(1 for a in arcs if a[0]==y) for y in range(V)]
    pairs=[(a[0],a[1]) for a in arcs]
    return len(set(od))==1 and od[0]>=2 and len(set(pairs))==len(pairs)
def rand_car(V,d,orders):
    G=grp(orders); arcs=[]
    for y in range(V):
        for z in random.sample(range(V),d): arcs.append((y,z,random.choice(G)))
    return arcs
out=open(sys.argv[1],'x'); P=lambda *a: (print(*a),print(*a,file=out))
# P0
A=[[1 if (j==i or j==(i+1)%3) else 0 for j in range(3)] for i in range(3)]
M=[[int(i==j) for j in range(3)] for i in range(3)]
for _ in range(5): M=[[sum(M[i][k]*A[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
P("CONTROL:",M[0][0],"P0",M[0][0]==11)
cars=[("d2 2-vertex Hadamard Z2",2,[(0,0,(0,)),(0,1,(0,)),(1,0,(0,)),(1,1,(1,))],[2]),
      ("d2 loop+tree-like into sink-ish",3,[(0,0,(0,)),(0,1,(1,)),(1,1,(0,)),(1,2,(1,)),(2,2,(1,)),(2,1,(0,))],[2]),
      ("d2 non-cyclic Z2xZ2",2,[(0,0,(0,1)),(0,1,(1,0)),(1,0,(1,1)),(1,1,(0,0))],[2,2]),
      ("d2 disconnected 2 copies",4,[(0,0,(0,)),(0,1,(0,)),(1,0,(0,)),(1,1,(1,)),(2,2,(0,)),(2,3,(0,)),(3,2,(0,)),(3,3,(1,))],[2]),
      ("d2 unreachable source vertex",3,[(0,1,(1,)),(0,2,(0,)),(1,1,(0,)),(1,2,(1,)),(2,1,(1,)),(2,2,(0,))],[3])]
for s in range(10):
    o=random.choice([[2],[3],[4],[2,2]]); V=random.choice([3,4]); d=random.choice([2,3]) if V>=3 else 2
    cars.append((f"random {s} V{V} d{d} C{o}",V,rand_car(V,d,o),o))
q=0; p1=True
for name,V,arcs,o in cars:
    h=hyp(V,arcs); k=kernel(V,arcs,o,3); q+=h
    P(name,"hyp",h,"ker3",k); p1&= (k==0) or not h
P("qualifying",q,"of",len(cars),"P1",p1)
p2=True
for name,V,arcs,o in cars[:3]:
    k=kernel(V,arcs,o,4); P(name,"ker4",k); p2&=k==0
P("P2",p2)
bad=[("d1 single loop",1,[(0,0,(0,))],[2],None),
     ("d1 3-cycle",3,[(0,1,(1,)),(1,2,(0,)),(2,0,(0,))],[2],None),
     ("parallel 2 loops gain0 (sizes 3..6)",1,[(0,0,(0,)),(0,0,(0,))],[2],6)]
p3=True
for name,V,arcs,o,K in bad:
    k=kernel(V,arcs,o,3,K); P(name,"hyp",hyp(V,arcs),"ker",k); p3&=k>0
P("P3",p3)
