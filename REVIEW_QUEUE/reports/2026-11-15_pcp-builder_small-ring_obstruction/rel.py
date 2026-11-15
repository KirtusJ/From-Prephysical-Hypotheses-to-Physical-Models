"""Predicate fixed first: for N=3,q in (3,4), CAP=10, collect over reachable states with sites y and y+2 (=x-1,x+1 for x=y+1)
each holding exactly one walk the triple (c_y, c_{y+2}, g_{y+2}-g_y mod q). Also for N=6."""
import itertools,sys
exec(open('s.py').read().split('CAP=int')[0])
def run2(N,q,CAP):
    idx=lambda x,c,g:(x*2+c)*q+g; M=2*N*q
    init=[0]*M; init[idx(0,0,0)]=1; init=tuple(init); seen={init}; fr=[init]; rel=set()
    def lone(t,x):
        L=[(c,g) for c in range(2) for g in range(q) for _ in range(t[idx(x,c,g)])]
        return L[0] if len(L)==1 else None
    while fr:
        nf=[]
        for s in fr:
            for y in range(N):
                a=lone(s,y);b=lone(s,(y+2)%N)
                if a and b: rel.add((a[0],b[0],(b[1]-a[1])%q))
            e=[0]*M
            for x in range(N):
                for c in range(2):
                    for g in range(q):
                        n=s[idx(x,c,g)]
                        if n: e[idx((x+1)%N,0,g)]+=n; e[idx((x-1)%N,1,(g+c)%q)]+=n
            occ=[x for x in range(N) if any(e[idx(x,c,g)] for c in range(2) for g in range(q))]
            for r in range(1,len(occ)+1):
                for A in itertools.combinations(occ,r):
                    t=[0]*M
                    for x in A:
                        for i in range(2*q): t[x*2*q+i]=e[x*2*q+i]
                    if sum(t)>CAP: continue
                    t=tuple(t)
                    if t not in seen: seen.add(t); nf.append(t)
        fr=nf
    return sorted(rel)
with open('rel.txt','x') as f:
  for N,q in ((3,3),(3,4),(6,3)):
    print(N,q,run2(N,q,10),file=f,flush=True)
