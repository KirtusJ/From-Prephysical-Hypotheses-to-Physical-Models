"""Predicates fixed before run.
P1: for N in {3,6}, q in {3,4,5}, BFS over reachable filtered states (counts per (site,chir,gainexp mod q)),
 states with total walks <= CAP kept (bounded). Report whether any state has a site x with
 exactly one walk at (x,R) gain h^a and exactly one at (x,L) gain h^(a+1), nothing else at x.
Hypothesis check: each state is reached from the initial (0,R,0) by Ext then site filter (a position product event).
Seed 20261113 (unused, deterministic)."""
import sys,itertools
def run(N,q,CAP):
    idx=lambda x,c,g:(x*2+c)*q+g
    M=2*N*q
    init=[0]*M; init[idx(0,0,0)]=1; init=tuple(init)
    seen={init}; fr=[init]; hits=[]
    while fr:
        nf=[]
        for s in fr:
            e=[0]*M
            for x in range(N):
                for c in range(2):
                    for g in range(q):
                        n=s[idx(x,c,g)]
                        if n:
                            e[idx((x+1)%N,0,g)]+=n
                            e[idx((x-1)%N,1,(g+c)%q)]+=n
            occ=[x for x in range(N) if any(e[idx(x,c,g)] for c in range(2) for g in range(q))]
            for r in range(1,len(occ)+1):
                for A in itertools.combinations(occ,r):
                    t=[0]*M
                    for x in A:
                        for c in range(2):
                            for g in range(q): t[idx(x,c,g)]=e[idx(x,c,g)]
                    if sum(t)>CAP: continue
                    t=tuple(t)
                    if t in seen: continue
                    seen.add(t); nf.append(t)
                    for x in A:
                        R=[t[idx(x,0,g)] for g in range(q)];L=[t[idx(x,1,g)] for g in range(q)]
                        if sum(R)==1 and sum(L)==1:
                            a=R.index(1); b=L.index(1)
                            if b==(a+1)%q: hits.append(t)
        fr=nf
    return len(seen),hits[:1]
CAP=int(sys.argv[1])
with open('res_cap%d.txt'%CAP,'x') as f:
  for N in (3,6):
    for q in (2,3,4,5):
        n,h=run(N,q,CAP); print(N,q,'states',n,'hit',h,file=f,flush=True)
