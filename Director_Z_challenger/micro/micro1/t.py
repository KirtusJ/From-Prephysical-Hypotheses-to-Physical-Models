import cmath, itertools, math
def lift(arcs,nv,q):
    h=q//2; L={}
    for (x,y,k) in arcs:
        for s in range(h):
            e=(s+k)%q; t=e%h; sg=-1 if e>=h else 1
            assert ((x,s),(y,t)) not in L
            L[((x,s),(y,t))]=sg
    return L
def check(name,arcs,nv,q,maxlen=4):
    h=q//2
    # base norm-preserving check (float)
    z=cmath.exp(2j*math.pi/q)
    A=[[0]*nv for _ in range(nv)]
    for x,y,k in arcs: A[y][x]=z**k
    okb=all(abs(sum(A[r][a].conjugate()*A[r][b] for r in range(nv))-(2 if a==b else 0))<1e-9 for a in range(nv) for b in range(nv))
    L=lift(arcs,nv,q)
    V=[(y,s) for y in range(nv) for s in range(h)]
    out={v:[(w,g) for (u,w),g in L.items() if u==v] for v in V}
    deg=all(len(out[v])==2 for v in V)
    indeg=all(sum(1 for (u,w) in L if w==v)==2 for v in V)
    ata=all(sum(L.get((a,r),0)*L.get((b,r),0) for r in V)==(2 if a==b else 0) for a in V for b in V)
    loops=sum(1 for (u,w) in L if u==w)
    # components
    par={v:v for v in V}
    def f(v):
        while par[v]!=v: v=par[v]
        return v
    for (u,w) in L: par[f(u)]=f(w)
    comps=len({f(v) for v in V})
    # events: all walks of length j from x0, subsets; compare
    oa={x:[(y,k) for (a,y,k) in arcs if a==x] for x in range(nv)}
    bad=0;n=0;cancel=0
    for x0 in range(nv):
      for j in range(1,maxlen+1):
        ws=[(x0,0)]
        for _ in range(j): ws=[(y,(k+kk)%q) for (x,k) in ws for (y,kk) in oa[x]]
        # lift walks from (x0,0): track independently
        lw=[((x0,0),1)]
        for _ in range(j): lw=[(w,g*gg) for (u,g) in lw for (w,gg) in out[u]]
        subsets=[range(len(ws))]+[c for r in (1,2,3) for c in itertools.combinations(range(len(ws)),r)]
        for S in subsets:
            nn={}; ll={}
            for i in S:
                y,k=ws[i]; t=k%h; sg=-1 if k>=h else 1
                nn[(y,t)]=nn.get((y,t),0)+sg
                u,g=lw[i]; ll[u]=ll.get(u,0)+g
            if {a:b for a,b in nn.items() if b}!={a:b for a,b in ll.items() if b}: bad+=1
            lhs=sum(v*v for v in nn.values())
            rhs=0
            for jj in range(1,q,2):
                for y in range(nv):
                    rhs+=abs(sum(nn.get((y,s),0)*z**(jj*s) for s in range(h)))**2
            rhs*=2/q
            n+=1
            if abs(lhs-rhs)>1e-8: bad+=1
            if len(S)==2 and lhs==0: cancel+=1
    print(name,'q',q,'baseNP',okb,'|V~|',len(V),'out2',deg,'in2',indeg,'AtA=2',ata,'loops',loops,'comps',comps,'events',n,'bad',bad,'full-cancel 2-walk events',cancel)
def Bq(k): return [(0,0,0),(0,1,0),(1,0,k),(1,1,k)]  # col x: A[0][x],A[1][x]
def B(q,k): return [(0,0,0),(0,1,0),(1,0,k),(1,1,(k+q//2)%q)]
for q in (2,4,6,8): check('B_q(loop,1block)',B(q,1),2,q)
for q in (4,6,8): check('B gains +-1 only',B(q,0),2,q)
check('B gain i in q=8',B(8,2),2,8)
check('B gain z^2 q=12',B(12,2),2,12,3)
# two-block ring, no loops: {0,1}->{2,3}->{0,1}
def ring(q,a,b):
    h=q//2
    return [(0,2,0),(0,3,0),(1,2,a),(1,3,(a+h)%q),(2,0,0),(2,1,0),(3,0,b),(3,1,(b+h)%q)]
for q,a,b in ((2,0,0),(4,1,0),(6,1,2),(6,2,4),(4,0,2)): check('ring a=%d b=%d'%(a,b),ring(q,a,b),4,q)
# (d)
for q in (2,4,6,8,10,12):
    h=q//2; z=cmath.exp(2j*math.pi/q)
    if h>=3:
        print('q',q,[(j,round(abs(1+z**j)**2,6),round(abs(1+z**(2*j))**2,6)) for j in range(1,q,2)])
    else:
        ok=all(abs(abs(sum(c*z**(j*s) for s,c in enumerate(n)))**2-sum(c*c for c in n))<1e-9 for j in range(1,q,2) for n in itertools.product(range(-4,5),repeat=h))
        print('q',q,'|sigma_j|^2 == sum n_s^2 on box:',ok)
