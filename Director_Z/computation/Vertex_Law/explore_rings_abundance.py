"""Exploration: does the hypothesis of G10 Corollary 5.23 (every gain reaches every vertex at one length, in abundance) hold on
the program's carriers?  Signed arc digraph of a ring of N sites; B_q.  Prints periods of D and of the derived digraph, and at a
few lengths the number of (vertex, gain) pairs reached from one start and the least count."""
from math import gcd
def ring(N):
    V=[(x,s) for x in range(N) for s in "RL"]; arcs=[]
    for (x,s) in V:
        arcs.append(((x,s),((x+1)%N,"R"),0)); arcs.append(((x,s),((x-1)%N,"L"),1 if s=="L" else 0))
    return V,arcs,2
def Bq(q):
    V=[0,1]; arcs=[(0,0,0),(0,1,0),(1,0,1),(1,1,(1+q//2)%q)]; return V,arcs,q
def analyse(name,V,arcs,q):
    idx={v:i for i,v in enumerate(V)}; n=len(V)
    out={i:[] for i in range(n)}
    for a,b,g in arcs: out[idx[a]].append((idx[b],g))
    cnt={(0,0):1}; res=[]
    def period(nodes,succ):
        # gcd of level differences via BFS
        start=next(iter(nodes)); lev={start:0}; st=[start]; g=0
        while st:
            u=st.pop()
            for w in succ(u):
                if w in lev: g=gcd(g,lev[u]+1-lev[w])
                else: lev[w]=lev[u]+1; st.append(w)
        return g,len(lev)
    r0,reach0=period(set(range(n)),lambda u:[b for b,_ in out[u]])
    r,reach=period({(i,g) for i in range(n) for g in range(q)},lambda u:[(b,(u[1]+g)%q) for b,g in out[u[0]]])
    for L in range(1,41):
        new={}
        for (y,g),c in cnt.items():
            for b,h in out[y]: new[(b,(g+h)%q)]=new.get((b,(g+h)%q),0)+c
        cnt=new
        if L in (12,13,24,25,40): res.append((L,len(cnt),min(cnt.values())))
    print(f"{name}: |V|={n} q={q} period(D)={r0} period(Dhat)={r} Dhat reached {reach}/{n*q}; (length, pairs reached of {n*q}, least count): {res}")
for N in (3,4,5,6,8): analyse(f"ring {N}",*ring(N))
for q in (2,4,6,8): analyse(f"B_{q}",*Bq(q))
