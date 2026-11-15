"""Exhaustive reachability of (U,V) at site 0 on small rings of D_h.
Predicates fixed before first run:
 P0 control: number of +-1 walks of length 6 from 0 ending at 2 (expect computed).
 P1 for each ring N in {3,5,6,8,10} (D=3,5,3,4,5) and q in {1,2,3}: hypothesis check
    reports D=N/gcd(N,2) and that 3<=D<=5 (outside lemma's range); count qualifying.
 P2 for each such (N,q), BFS over all fields reachable by position masks (any subset of
    sites per step, start = single walk at (0,R) gain 0 before step 1), fields deduplicated,
    fields with total walk count > B=8 pruned (so 'not found' means not found within B).
    For every target (U,V) with |U|+|V|<=2, |U|+|V|>=1, report whether a field equal to
    U at (x,R), V at (x,L) and zero elsewhere is reached for some site x (rotation symmetric
    so x=0 suffices given ring translation? no: start fixed at 0; we accept any x and report).
Exact integers; seed 20261113 (unused, deterministic search).
"""
import itertools, sys, json, random
random.seed(20261113)
B=8
out=open(sys.argv[1],'x')
def ctrl():
    return sum(1 for w in itertools.product((1,-1),repeat=6) if sum(w)==2)
out.write("CONTROL %d\n"%ctrl())
def step(field,N,q):
    new={}
    for (x,r,j),c in field.items():
        for (y,r2,jj) in (((x+1)%N,'R',j),((x-1)%N,'L',(j+1)%q if r=='L' else j)):
            new[(y,r2,jj)]=new.get((y,r2,jj),0)+c
    return new
def targets(q):
    gs=list(range(q)); T=[]
    for n in (1,2):
        for combo in itertools.combinations_with_replacement([(r,g) for r in 'RL' for g in gs],n):
            T.append(tuple(sorted(combo)))
    return T
qual=0
for N in (3,5,6,8,10):
    D=N//(2 if N%2==0 else 1)
    hyp=3<=D<=5
    qual+=hyp
    for q in (1,2,3):
        start=frozenset({(0,'R',0):1}.items())
        seen={start}; frontier=[start]
        while frontier:
            nf=[]
            for f in frontier:
                full=step(dict(f),N,q)
                sites=sorted({k[0] for k in full})
                for k in range(1,len(sites)+1):
                    for A in itertools.combinations(sites,k):
                        g={kk:c for kk,c in full.items() if kk[0] in A}
                        if sum(g.values())>B: continue
                        fs=frozenset(g.items())
                        if fs not in seen: seen.add(fs); nf.append(fs)
            frontier=nf
        reach=set()
        for f in seen:
            d=dict(f)
            if f==start: continue
            xs={k[0] for k in d}
            if len(xs)==1:
                reach.add(tuple(sorted((r,j) for (x,r,j),c in d.items() for _ in range(c))))
        T=targets(q)
        miss=[t for t in T if t not in reach]
        out.write(json.dumps({"N":N,"D":D,"hyp_outside_lemma":hyp,"q":q,"states":len(seen),
          "targets":len(T),"reached":len(T)-len(miss),"missing":miss})+"\n")
        out.flush()
out.write("qualifying rings %d of 5\n"%qual)
