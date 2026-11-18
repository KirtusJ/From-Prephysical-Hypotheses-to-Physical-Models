"""Predicates fixed before first run. Seed 20261113.
P0 control: number of multisets of size 3 from 4 elements.
P1 (realization): on carriers D (random finite gain digraphs, C=Z_q) that contain a block
 x_0..x_{d-1} with common successor set y_0..y_{d-1}, one arc each (hypothesis H1 tested per case),
 and abundance at a length n (H2 tested per case: every gain >= N walks to each x_y),
 every random vector (m_y) with counts <= N is realized by an event S of length-n walks with
 m_S(x_y)=m_y, empty elsewhere, and the continuation has multiset sum_y B_zy.m_y at y_z, empty elsewhere.
P2 (infinite carrier, last sentence): signed / Z4 line, vertex k -> k-1,k+1, gains forming
 A^*A=2 for faithful chi of Z4 (H tested per window: (A^*A)_{kk'} over interior), random finite
 events (sets of walks from 0 of length n), rule F=a|m|+c|sigma_chi(m)|^2 in exact Gaussian ints:
 mu(cont S)=2 mu(S).  Report counts qualifying.
"""
import random, itertools
from collections import Counter
random.seed(20261113)
out=open('result.txt','x')
def w(s): out.write(s+'\n'); print(s)
w('CONTROL: %d'%len(list(itertools.combinations_with_replacement(range(4),3))))
# P1
q=4; tested=qual=ok=0
for trial in range(60):
    tested+=1
    V=6; d=2
    arcs={v:[] for v in range(V)}
    # block x=(0,1), y=(2,3) random gains; other vertices random 2 successors
    for x in (0,1):
        for y in (2,3): arcs[x].append((y,random.randrange(q)))
    for v in range(2,V):
        for s in random.sample(range(V),2): arcs[v].append((s,random.randrange(q)))
    # H1
    h1=all(sorted(t for t,_ in arcs[x])==[2,3] for x in (0,1))
    # walks from 0 of length n
    n=7; walks=[((0,),0)]
    for _ in range(n):
        walks=[(p+(t,),(g+h)%q) for p,g in walks for t,h in arcs[p[-1]]]
    cnt=Counter((p[-1],g) for p,g in walks)
    N=min(cnt[(x,h)] for x in (0,1) for h in range(q))
    if not(h1 and N>=1): continue
    qual+=1
    good=True
    for r in range(20):
        m={x:Counter({h:random.randint(0,N) for h in range(q)}) for x in (0,1)}
        S=[]
        for x in (0,1):
            for h in range(q):
                S+= [wk for wk in walks if wk[0][-1]==x and wk[1]==h][:m[x][h]]
        assert len(set(S))==len(S)
        mS=Counter((p[-1],g) for p,g in S)
        good&= all(mS[(x,h)]==m[x][h] for x in (0,1) for h in range(q)) and all(k[0] in (0,1) for k in mS)
        cont=[(p+(t,),(g+h)%q) for p,g in S for t,h in arcs[p[-1]]]
        mc=Counter((p[-1],g) for p,g in cont)
        B={(t,x):h for x in (0,1) for t,h in arcs[x]}
        pred=Counter()
        for x in (0,1):
            for h,c in m[x].items():
                for t in (2,3): pred[(t,(h+B[(t,x)])%q)]+=c
        good&= (+mc)==(+pred)
    ok+=good
w('P1 tested %d qualifying %d pass %d'%(tested,qual,ok))
# P2 line, Z4 gains: k->k+1 gain 0, k->k-1 gain g(k) ; chi(i)=i^k
I=[1,1j,-1,-1j]
tested=qual=ok=0
for trial in range(40):
    tested+=1
    # choose per-vertex gains: right arc gain r, left arc gain l; A^*A=2 needs at each pair k,k+2 sharing successor k+1:
    # chi(l_{k+2})conj... ; build by rule l=r+2 (Hadamard-like) with random r per vertex, shifted
    R=40; r={k:random.randrange(4) for k in range(-R,R+1)}
    sw=random.random()<0.25  # some cases deliberately violate H
    l={k:(r[k]+2+(random.randrange(4) if sw else 0))%4 for k in r}
    # H: (A^*A)_{k,k+2} = conj(chi(arc k->k+1)) chi(arc k+2->k+1) = 0? single common successor => never 0 unless ... 
    # common successors of k,k+2: only k+1 -> entry modulus 1. So line with out-degree 2 cannot satisfy A^*A=2.
    hyp=False
    if hyp: qual+=1
w('P2 note: on the line k->k+-1 vertices k,k+2 share exactly one successor, so A^*A=2 fails for every gain; 0 qualifying')
out.close()
