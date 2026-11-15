# Abundance test for G10 Cor 5.23: exists length t with every (vertex,gain) count >= NREQ, start vertex 0. Lengths <= LMAX.
import sys; sys.path.insert(0,'/home/user/From-Prephysical-Hypotheses-to-Physical-Models/REVIEW_QUEUE/lib')
from pcplib import ring_carrier, lift, walk_counts, period, strongly_connected
NREQ, LMAX = 10, 200
print("CONTROL 4-cycle period:", period([[1],[2],[3],[0]])[0])
def test(name, E, mod):
    idx, S = lift(E, mod); W = walk_counts(S, 0, LMAX); n = len(S)
    hit = next(((t, min(W[t].get(i,0) for i in range(n))) for t in range(1,LMAX+1) if min(W[t].get(i,0) for i in range(n)) >= NREQ), None)
    if hit: print(f"{name}: HOLDS t={hit[0]} min={hit[1]}"); return
    reach = set().union(*[set(w) for w in W[1:]])
    sc = strongly_connected(S); p = period(S)[0] if sc else None
    gains0 = sorted({g for (y,g),i in idx.items() if y==0 and i in reach})
    print(f"{name}: FAILS reached {len(reach)}/{n} lifted, lift SC={sc} period={p}, gains at start={gains0}")
for N in range(3,11): test(f"ring{N}", ring_carrier(N), (2,))
for q in range(2,13):
    m = q if q%2==0 else 2*q; z = m//q
    E = [[(0,),(z%m,)],[(0,),((z+m//2)%m,)]]; test(f"B_{q} (mod {m})", E, (m,))
for M in range(3,7):
    n=4*M; E=[[None]*(2*n) for _ in range(2*n)]
    for x in range(n):
        g=(x//2)%M
        for s in (0,1):
            E[2*((x+1)%n)][2*x+s]=(0,g); E[2*((x-1)%n)+1][2*x+s]=(1 if s==1 else 0,g)
    test(f"staircase M={M}", E, (2,M))
