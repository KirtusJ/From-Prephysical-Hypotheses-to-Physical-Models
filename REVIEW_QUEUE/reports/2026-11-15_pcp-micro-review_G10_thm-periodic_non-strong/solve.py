import sys, itertools, cmath
from fractions import Fraction
sys.path.insert(0,'/home/user/From-Prephysical-Hypotheses-to-Physical-Models/REVIEW_QUEUE/lib')
from pcplib import lift, strongly_connected, period, gadd, group
print("CONTROL:", "yes" if strongly_connected([[1],[0,2],[]]) else "no")
def rref_null(rows, n):
    piv=[]; R=[]
    for r in rows:
        r=[Fraction(x) for x in r]
        for (c,pr) in zip(piv,R):
            if r[c]: f=r[c]; r=[a-f*b for a,b in zip(r,pr)]
        nz=[i for i,x in enumerate(r) if x]
        if not nz: continue
        c=nz[0]; f=r[c]; r=[x/f for x in r]
        for k in range(len(R)):
            if R[k][c]: g=R[k][c]; R[k]=[a-g*b for a,b in zip(R[k],r)]
        piv.append(c); R.append(r)
    free=[i for i in range(n) if i not in piv]; B=[]
    for f in free:
        v=[Fraction(0)]*n; v[f]=Fraction(1)
        for c,pr in zip(piv,R): v[c]=-pr[f]
        B.append(v)
    return B
def rank(rows):
    return len(rows[0])-len(rref_null(rows,len(rows[0]))) if rows else 0
def run(name,E,mod,L=3,x0=0):
    n=len(E); d=sum(E[z][x0] is not None for z in range(n))
    idx,S=lift(E,mod); sc=strongly_connected(S)
    G=group(mod)
    U=[]
    for k in G:  # character exponent tuple
        A=[[0 if E[z][y] is None else cmath.exp(2j*cmath.pi*sum(a*b/m for a,b,m in zip(k,E[z][y],mod))) for y in range(n)] for z in range(n)]
        ok=all(abs(sum(A[z][y].conjugate()*A[z][yy] for z in range(n))-(d if y==yy else 0))<1e-9 for y in range(n) for yy in range(n))
        if ok: U.append(k)
    cls=set(frozenset([k,tuple((-a)%m for a,m in zip(k,mod))]) for k in U)
    walks={0:[(x0,G[0])]}
    for t in range(1,L+2):
        walks[t]=[(z,gadd(g,E[z][y],mod)) for (y,g) in walks[t-1] for z in range(n) if E[z][y] is not None]
    var={}
    def fam(ws):
        D={}
        for y,g in ws: D.setdefault(y,[]).append(g)
        return [ (y,tuple(sorted(v))) for y,v in D.items()]
    def vec(ws):
        v={}
        for key in fam(ws):
            j=var.setdefault(key,len(var)); v[j]=v.get(j,0)+1
        return v
    eqs=[]; evs=[]
    for t in range(0,L+1):
        W=walks[t]
        for mask in range(1,1<<len(W)):
            sel=[W[i] for i in range(len(W)) if mask>>i&1]
            cont=[(z,gadd(g,E[z][y],mod)) for (y,g) in sel for z in range(n) if E[z][y] is not None]
            a=vec(sel); b=vec(cont); e={}
            for j,c in b.items(): e[j]=e.get(j,0)+c
            for j,c in a.items(): e[j]=e.get(j,0)-d*c
            eqs.append(e); evs.append(a)
    N=len(var)
    B=rref_null([[e.get(j,0) for j in range(N)] for e in eqs],N)
    M=[[sum(c*b[j] for j,c in ev.items()) for ev in evs] for b in B]
    print(f"{name}: Dhat SC={sc} |Dhat|={len(S)} d={d} U(D)={U} 1+#(U/~)={1+len(cls)} unknownsF={N} dimF={len(B)} dim_on_events(len<={L})={rank(M) if M else 0}")
    return B,var
Z=None
run("a1 Z2 all gains 0, K2+loops",[[(0,),(0,)],[(0,),(0,)]],(2,))
run("a2 Z4 gains in {0,2}, Hadamard",[[(0,),(0,)],[(0,),(2,)]],(4,))
run("a3 Z3 gains 0, 3-cycle-ish",[[Z,(0,),(0,)],[(0,),Z,(0,)],[(0,),(0,),Z]],(3,))
def two(gA,gB,mod):
    E=[[Z]*5 for _ in range(5)]
    o=tuple(0 for _ in mod)
    E[1][0]=o;E[2][0]=o
    E[1][1]=o;E[3][1]=o;E[1][3]=o;E[3][3]=gA
    E[2][2]=o;E[4][2]=o;E[2][4]=o;E[4][4]=gB
    return E
run("b1 trivial C, two terminal classes",two((0,),(0,),(1,)),(1,))
run("b2 Z2, both terminal blocks Hadamard",two((1,),(1,),(2,)),(2,))
run("b3 Z2, one Hadamard one trivial",two((1,),(0,),(2,)),(2,))
