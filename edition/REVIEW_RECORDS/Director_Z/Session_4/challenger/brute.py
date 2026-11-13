import random, math, itertools
from k import *
rng=random.Random(7)
def walks(D,x0,j,G):
    W=[((x0,),G.els[0])]
    for _ in range(j): W=[(p+(z,),G.mul(g,u)) for p,g in W for z,u in D[p[-1]].items()]
    return W
def mu(G,f,S):
    return sum(f[G.mul(g2,G.inv(g1))] for (p1,g1) in S for (p2,g2) in S if p1[-1]==p2[-1])
def ext(D,S,G): return [(p+(z,),G.mul(g,u)) for p,g in S for z,u in D[p[-1]].items()]
for mods,eps,kind in [((8,),(4,),2),((12,),(6,),2),((3,3,2),(0,0,1),2),((6,),(3,),3)]:
    G=Grp(mods); 
    while True:
        D=block2(G,eps,2,rng) if kind==2 else block3(G,(2,),1,rng)
        r=analyse(G,D)
        if r['hyp']: break
    d=r['d']
    for ch in G.chars():
        f={g:G.ev(ch,g).real for g in G.els}; bad=0
        for t in range(300):
            x0=rng.choice(list(D)); j=rng.randint(0,4); W=walks(D,x0,j,G)
            S=rng.sample(W,rng.randint(1,min(len(W),6)))
            if abs(mu(G,f,ext(D,S,G))-d*mu(G,f,S))>1e-8: bad+=1
        inX = ch in r['X']
        if inX != (bad==0): print('BRUTE MISMATCH',mods,ch,inX,bad)
    print(mods,'brute ok; X size',len(r['X']),'soldim',r['soldim'],'xdim',r['xdim'])
