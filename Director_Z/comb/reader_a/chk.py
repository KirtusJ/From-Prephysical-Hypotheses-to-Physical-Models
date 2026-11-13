"""Predicates fixed before run.
P1 K4, one arc-pair gain w (order 3): ratios of (addcons) on length-2 walks; assignment A: a=1,F(1)=2,F(w^+-1)=1/2 ; B: a=1,F(1)=1,F(w)=2,F(w^-1)=1/2. Expect set {1.5,2.5,4} under one of them.
P2 signed line: S of thm:quad has v_S = a@(a-1,R),1@(a-1,L); Ext: a+1@(a,R), a-1@(a-2,L), a=1..6.
P4 B_q: A*A=2; pair digraph strongly connected; q=2..12 even.
P5 (2/5)(3+r5)/16+(2/5)(3-r5)/16+(1/5)(1/2)==1/4 exactly.
P6 #classes{j,-j}, j odd mod q == ceil(q/4), even q<=60.
P7 lift identity (c) on random integer vectors, q=2..12; (d) values differ for q>=6 all odd j; kernel (c) f=(2/q)sum chi_j equals 1,-1,0.
P8 lift of B_q: At A = 2I, q=2..12.
P9 kernel solution space dim on B_q == ceil(q/4), with hypothesis (all quotients at block pair, one length) tested.
P10 gains of B_4 contain -1? (paper line 101 claims needed)
P11 thm:power h(p)<2m p<2, >2m p>2 on random vanishing sums of roots of unity.
"""
import itertools, cmath, math, random, fractions
import numpy as np, sympy as sp
random.seed(1); F=fractions.Fraction
res={}
# P1
def k4(assign):
    V=range(4); gain={}  # exponent mod 3
    for x in V:
        for y in V:
            if x!=y: gain[(x,y)]=0
    gain[(0,1)]=1; gain[(1,0)]=2
    out=set()
    for start in V:
        for y in V:
            if y==start: continue
            for z in V:
                if z==y: continue
                g=(gain[(start,y)]+gain[(y,z)])%3
                Fw = assign[g] if z==start else F(1)
                tot=F(0)
                for t in V:
                    if t==z: continue
                    g2=(g+gain[(z,t)])%3
                    tot+= assign[g2] if t==start else F(1)
                out.add(float(tot/Fw))
    return sorted(out)
res['P1_A']=k4({0:F(2),1:F(1,2),2:F(1,2)}); res['P1_B']=k4({0:F(1),1:F(2),2:F(1,2)})
# P2
def step(v):
    o={}
    for (x,c),val in v.items():
        o[(x+1,'R')]=o.get((x+1,'R'),0)+val
        o[(x-1,'L')]=o.get((x-1,'L'),0)+(-val if c=='L' else val)
    return {k:v for k,v in o.items() if v!=0}
ok=True
for a in range(1,7):
    vS={}
    for pos in range(a+1):
        seq=['R']*(a+1); seq[pos]='L'
        x,c,g=0,'R',1
        for s in seq:
            if s=='R': x,c=x+1,'R'
            else:
                if c=='L': g=-g
                x,c=x-1,'L'
        vS[(x,c)]=vS.get((x,c),0)+g
    e=step(vS)
    exp={(a,'R'):a+1,(a-2,'L'):a-1}; exp={k:v for k,v in exp.items() if v}
    ok&= vS=={(a-1,'R'):a,(a-1,'L'):1} and e==exp
res['P2']=ok
# P4,P8,P9
def Bq(q):
    z=cmath.exp(2j*math.pi/q); return np.array([[1,z],[1,-z]])
h4=[];h8=[];h9=[]
for q in range(2,13,2):
    h=q//2
    A=Bq(q); h4.append(np.allclose(A.conj().T@A,2*np.eye(2)))
    # arcs: from x to y exponent k
    arcs=[(0,0,0),(1,0,1%q),(0,1,0),(1,1,(1+h)%q)]  # (from,to,exp)
    # pair digraph strong connectivity
    nodes=[(x,g) for x in range(2) for g in range(q)]
    def reach(s,fw=True):
        seen={s};st=[s]
        while st:
            u=st.pop()
            for (a,b,k) in arcs:
                if fw and a==u[0]: w=(b,(u[1]+k)%q)
                elif (not fw) and b==u[0]: w=(a,(u[1]-k)%q)
                else: continue
                if w not in seen: seen.add(w);st.append(w)
        return seen
    h4[-1]&= len(reach((0,0)))==2*q and len(reach((0,0),False))==2*q
    # lift
    n=2*h; At=np.zeros((n,n))
    for (a,b,k) in arcs:
        for s in range(h):
            t=(s+k)%h; eps=(-1)**((s+k)//h)
            At[b*h+t,a*h+s]+=eps
    h8.append(np.array_equal(At.T@At,2*np.eye(n)))
    # P9 kernel: walks from vertex 0 length L with (end, gain)
    L=max(6,q+2)
    cnt={(0,0):1}; 
    walks=[(0,0)]
    for _ in range(L):
        walks=[(b,(g+k)%q) for (x,g) in walks for (a,b,k) in arcs if a==x]
    # hypothesis: quotients walks to vertex0 / vertex1 cover C
    g0={g for (x,g) in walks if x==0}; g1={g for (x,g) in walks if x==1}
    hyp= {(b-a)%q for a in g0 for b in g1}==set(range(q))
    def mu_row(ws):
        row=np.zeros(h+1)
        byv={}
        for (x,g) in ws: byv.setdefault(x,[]).append(g)
        for gs in byv.values():
            for a in gs:
                for b in gs:
                    d=(b-a)%q; d=min(d,q-d); row[d]+=1
        return row
    rows=[]
    for _ in range(300):
        S=random.sample(walks,random.randint(1,min(8,len(walks))))
        ext=[(b,(g+k)%q) for (x,g) in S for (a,b,k) in arcs if a==x]
        rows.append(mu_row(ext)-2*mu_row(S))
    M=np.array(rows); sv=np.linalg.svd(M,compute_uv=False)
    dim=(h+1)-np.linalg.matrix_rank(M)
    h9.append((q,hyp,int(dim),math.ceil(q/4),[round(x,3) for x in sv]))
res['P4']=h4;res['P8']=h8;res['P9']=h9
# P5
r5=sp.sqrt(5)
res['P5']=sp.simplify(sp.Rational(2,5)*(3+r5)/16+sp.Rational(2,5)*(3-r5)/16+sp.Rational(1,5)/2-sp.Rational(1,4))==0
# P6
res['P6']=all(len({frozenset({j,(-j)%q}) for j in range(1,q,2)})==math.ceil(q/4) for q in range(2,61,2))
# P7
ok7=True;d7=[];k7=True
for q in range(2,13,2):
    h=q//2; z=cmath.exp(2j*math.pi/q)
    for _ in range(50):
        n=[random.randint(-5,5) for _ in range(h)]
        lhs=sum(x*x for x in n)
        rhs=2/q*sum(abs(sum(n[s]*z**(j*s) for s in range(h)))**2 for j in range(1,q,2))
        ok7&=abs(lhs-rhs)<1e-9
    if q>=6:
        d7.append((q,min(abs(abs(1+z**j)**2-abs(1+z**(2*j))**2) for j in range(1,q,2))))
    for k in range(q):
        f=2/q*sum(z**(j*k) for j in range(1,q,2))
        exp=1 if k==0 else (-1 if k==h else 0)
        k7&=abs(f-exp)<1e-9
res['P7']=(ok7,d7,k7)
res['P10']=[-1 in {1,1j,-1j}]
# P11
bad=0;tot=0
for _ in range(2000):
    q=random.choice([2,3,4,5,6,8,12]); z=cmath.exp(2j*math.pi/q)
    m=random.randint(2,6)
    us=[z**random.randrange(q) for _ in range(m)]
    if abs(sum(us))>1e-9: continue
    tot+=1
    for p in (0.5,1,1.5,1.99,2.01,3,4,7):
        hp=sum(abs(1+u)**p for u in us)
        if (p<2 and not hp<2*m) or (p>2 and not hp>2*m): bad+=1
res['P11']=(tot,bad)
for k,v in res.items(): print(k,v)
