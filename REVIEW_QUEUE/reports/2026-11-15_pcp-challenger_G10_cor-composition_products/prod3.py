"""Product carriers, G10 Cor 5.28 extension. Group C=Z8 (additive), chars chi_k(g)=exp(2pi i k g/8).
Carrier: dict vertex-> list of (succ, gain); x0 = first vertex.
Rerun 3: nullity now taken modulo coefficient vectors vanishing on all sampled events (duplicate columns sigma_{-k}=conj sigma_k). Rerun after bug fix in class count (string compare of rounded complex) and more rows (120/length); predicates unchanged.
Predicates fixed before run:
P1 hyp per carrier: <=1 arc per ordered pair, outdeg d>=2 constant, derived digraph strongly connected (reported).
P2 U(D1xD2) == U(D1) & U(D2)  (claim: A1(x)A2 norm-preserving iff both are).
P3 nullity of consistency equations (vertex-independent real quadratic rules in sigma_psi plus |m|),
   on random events of product carrier lengths 3..5, equals 1 + #(U|C0 / ~) of Thm 5.26 for the product.
P4 count and ||v^psi||^2 (psi in U1&U2) consistent on product-carrier events, factor d1 d2.
P5 (different carriers) the mixture (||v^1||^2+||v^3||^2)/2 is multiplicative on product events S1xS2
   for D1 where chi1,chi3 agree on events and D2 where they do not, and consistent on both.
P6 the representative choice: on D1xD1 events, ||v^1||^2 vs ||v^3||^2 differ (rule ambiguity) -- reported.
"""
import itertools, random, cmath, numpy as np, os, sys
random.seed(1); Q=8
def ch(k,g): return cmath.exp(2j*cmath.pi*k*g/Q)
def check(D):
    V=list(D); ds={len(D[v]) for v in V}
    ok1=all(len({z for z,_ in D[v]})==len(D[v]) for v in V) and len(ds)==1 and min(ds)>=2
    N=[(v,g) for v in V for g in range(Q)]
    adj={u:[(z,(u[1]+a)%Q) for z,a in D[u[0]]] for u in N}
    def reach(s,a):
        seen={s};st=[s]
        while st:
            u=st.pop()
            for w in a[u]:
                if w not in seen: seen.add(w);st.append(w)
        return seen
    radj={u:[] for u in N}
    for u in N:
        for w in adj[u]: radj[w].append(u)
    s=(V[0],0); sc=len(reach(s,adj))==len(N)==len(reach(s,radj))
    # kappa / period
    dist={s:0};fr=[s]
    while fr:
        nf=[]
        for u in fr:
            for w in adj[u]:
                if w not in dist: dist[w]=dist[u]+1;nf.append(w)
        fr=nf
    import math; r=0
    for u in N:
        for w in adj[u]:
            if w in dist: r=math.gcd(r,dist[u]+1-dist[w])
    C0=[g for g in range(Q) if (V[0],g) in dist and (dist[(V[0],g)]%r==0)]
    idx={v:i for i,v in enumerate(V)}; d=ds.pop()
    U=[]
    for k in range(Q):
        A=np.zeros((len(V),len(V)),complex)
        for y in V:
            for z,a in D[y]: A[idx[z],idx[y]]=ch(k,a)
        if np.allclose(A.conj().T@A,d*np.eye(len(V))): U.append(k)
    cls=set()
    for k in U:
        res=tuple((k*g)%Q for g in C0); inv=tuple((-k*g)%Q for g in C0); cls.add(min(res,inv))
    return dict(ok1=ok1,sc=sc,d=d,r=r,C0=C0,U=U,ncls=len(cls))
def prod(D1,D2):
    return {(a,b):[((z1,z2),(g1+g2)%Q) for z1,g1 in D1[a] for z2,g2 in D2[b]] for a in D1 for b in D2}
def walks_end(D,n):
    x0=list(D)[0]; W=[(x0,0)]
    for _ in range(n): W=[(z,(g+a)%Q) for (y,g) in W for z,a in D[y]]
    return W
def ext(D,S): return [(z,(g+a)%Q) for (y,g) in S for z,a in D[y]]
def feats(S,V):
    # per-vertex sigma_k; features: |m|, Re/Im sum_y s_k conj s_l for k<=l
    sig={y:np.zeros(Q,complex) for y in V}; cnt=0
    for y,g in S:
        cnt+=1
        for k in range(Q): sig[y][k]+=ch(k,g)
    f=[cnt]
    for k in range(Q):
        for l in range(k,Q):
            t=sum(sig[y][k]*sig[y][l].conjugate() for y in V)
            f+= [t.real] + ([t.imag] if l!=k else [])
    return np.array(f)
def nsq(S,V,k):
    "V unused"
    s={}
    for y,g in S: s[y]=s.get(y,0)+ch(k,g)
    return sum(abs(x)**2 for x in s.values())
def rsub(W):
    return [w for w in W if random.random()<random.choice([0.1,0.3,0.6])] or W[:1]
Z=1  # zeta = gain 1
DA={0:[(0,1),(1,1)],1:[(0,1),(1,5)]}   # paper example zeta[[1,1],[1,-1]], -1 = 4
# search D2: 2 vertices, loops, chi1 and chi3 in U, C0=Z8
cands=[]
for g in itertools.product(range(Q),repeat=4):
    D={0:[(0,g[0]),(1,g[1])],1:[(0,g[2]),(1,g[3])]}
    c=check(D)
    if c['sc'] and c['ok1'] and len(c['C0'])==Q and 1 in c['U'] and 3 in c['U']: cands.append(D)
out=[]; P=lambda s: (out.append(s),print(s))
P(f"search D2 over Z8 2-vertex: {len(cands)} qualify")
DB=cands[0]; P(f"DB={DB}")
fails=[]
for name,D1,D2 in [("A x A",DA,DA),("A x B",DA,DB),("B x B",DB,DB)]:
    c1,c2=check(D1),check(D2); D=prod(D1,D2); c=check(D)
    P(f"{name}: D1 {c1} | D2 {c2} | prod {c}")
    p2= set(c['U'])==set(c1['U'])&set(c2['U']); P(f" P2 {p2}"); 
    if not p2: fails.append(name+" P2")
    V=list(D); rows=[]; frows=[]
    for n in range(3,6):
        W=walks_end(D,n)
        for _ in range(120):
            S=rsub(W); fS=feats(S,V); rows.append(feats(ext(D,S),V)-c['d']*fS); frows.append(fS)
    M=np.array(rows); sv=np.linalg.svd(M,compute_uv=False)
    tol=sv[0]*1e-9; sf=np.linalg.svd(np.array(frows),compute_uv=False); nf=M.shape[1]-int((sf>sf[0]*1e-9).sum()); null=M.shape[1]-int((sv>tol).sum())-nf
    pred=1+c['ncls'] if c['sc'] else None
    gap=(sv[sv>tol].min(), sv[sv<=tol].max() if (sv<=tol).any() else 0)
    P(f" P3 hyp(sc)={c['sc']} nullity={null} predicted={pred} sv gap {gap[0]:.3e} / {gap[1]:.3e} rows={len(rows)}")
    if c['sc'] and null!=pred: fails.append(name+" P3")
    # P4
    W=walks_end(D,4); bad=0
    for _ in range(20):
        S=rsub(W);E=ext(D,S)
        bad+= abs(len(E)-c['d']*len(S))>1e-9
        for k in c['U']: bad+= abs(nsq(E,V,k)-c['d']*nsq(S,V,k))>1e-6
    P(f" P4 violations {bad}"); 
    if bad: fails.append(name+" P4")
    # P6 representative
    W=walks_end(D,4); diff=max(abs(nsq(S,V,1)-nsq(S,V,3)) for S in [rsub(W) for _ in range(20)])
    P(f" P6 max | ||v1||^2-||v3||^2 | on product-carrier events: {diff:.3e}")
# P5
mu=lambda S,V,c: c[0]*len(S)+c[1]*nsq(S,V,1)+c[2]*nsq(S,V,3)
for coef in [(0,.5,.5),(0,2,-1),(0,1,0),(.5,.5,0)]:
    err=0;cons=0
    for n in (4,5):
        W1,W2=walks_end(DA,n),walks_end(DB,n)
        for _ in range(30):
            S1,S2=rsub(W1),rsub(W2)
            S12=[((y1,y2),(g1+g2)%Q) for y1,g1 in S1 for y2,g2 in S2]
            err=max(err,abs(mu(S12,None,coef)-mu(S1,None,coef)*mu(S2,None,coef))/max(1,abs(mu(S1,None,coef)*mu(S2,None,coef))))
            for D_,S in ((DA,S1),(DB,S2)): cons=max(cons,abs(mu(ext(D_,S),None,coef)-2*mu(S,None,coef)))
    P(f"P5 coef(a,c1,c3)={coef}: max rel mult err {err:.2e}, max consistency err {cons:.2e}")
P(f"FAILED predicates: {fails}")
with open("result3.txt","x") as f: f.write("\n".join(out)+"\n")
