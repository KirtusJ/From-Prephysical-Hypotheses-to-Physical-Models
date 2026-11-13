import itertools, random, cmath, math, sys
from fractions import Fraction
import numpy as np

class Grp:
    def __init__(s, mods):
        s.mods=tuple(mods); s.els=list(itertools.product(*[range(m) for m in mods])); s.idx={g:i for i,g in enumerate(s.els)}
        s.n=len(s.els)
    def mul(s,a,b): return tuple((x+y)%m for x,y,m in zip(a,b,s.mods))
    def inv(s,a): return tuple((-x)%m for x,m in zip(a,s.mods))
    def chars(s): return s.els
    def ev(s,ch,g): return cmath.exp(2j*math.pi*sum(c*x/m for c,x,m in zip(ch,g,s.mods)))

def rank(rows):
    rows=[[Fraction(x) for x in r] for r in rows]; r=0
    if not rows: return 0
    nc=len(rows[0])
    for c in range(nc):
        p=next((i for i in range(r,len(rows)) if rows[i][c]!=0),None)
        if p is None: continue
        rows[r],rows[p]=rows[p],rows[r]
        for i in range(len(rows)):
            if i!=r and rows[i][c]!=0:
                t=rows[i][c]/rows[r][c]; rows[i]=[a-t*b for a,b in zip(rows[i],rows[r])]
        r+=1
        if r==len(rows): break
    return r

# D: dict x -> dict y -> gain
def analyse(G, D, L=None):
    V=list(D); d=len(D[V[0]]); assert all(len(D[x])==d for x in V)
    e=G.els[0]
    # reachable pair states (y1,y2,g) per start; g = phi(w2)/phi(w1)
    reach=set()
    for x0 in V:
        cur={(x0,x0,e)}; seen=set()
        for _ in range(L or 200):
            nxt=set()
            for (a,b,g) in cur:
                for za,ua in D[a].items():
                    for zb,ub in D[b].items():
                        nxt.add((za,zb,G.mul(g,G.mul(ub,G.inv(ua)))))
            fz=frozenset(nxt)
            if fz in seen: break
            seen.add(fz); cur=nxt
            reach|={(x0,)+s for s in nxt}   # includes w1==w2 states (a,a,e): harmless
    # hypothesis
    pairs=[(a,b) for a in V for b in V if a!=b and set(D[a])&set(D[b])]
    def hyp_pair(a,b):
        for x0 in V:
            if len({g for (s,p,q,g) in reach if s==x0 and p==a and q==b})==G.n: return True
        return False
    hyp=all(hyp_pair(a,b) for a,b in pairs)
    # equations with c=d : for different ends sum_z f(g r_z)=0 ; same ends trivial
    # unknowns: f on orbits {g,g^-1}
    orb={};reps=[]
    for g in G.els:
        r=min(g,G.inv(g))
        if r not in orb: orb[r]=len(reps); reps.append(r)
    eqs=set()
    for (s,a,b,g) in reach:
        if a==b: continue
        Z=set(D[a])&set(D[b])
        if not Z: continue
        row=[0]*len(reps)
        for z in Z:
            h=G.mul(g,G.mul(D[b][z],G.inv(D[a][z]))); row[orb[min(h,G.inv(h))]]+=1
        eqs.add(tuple(row))
    soldim=len(reps)-rank(list(eqs))
    # X(D)
    X=[]
    for ch in G.chars():
        A=np.zeros((len(V),len(V)),complex); ix={v:i for i,v in enumerate(V)}
        for x in V:
            for y,u in D[x].items(): A[ix[y],ix[x]]=G.ev(ch,u)
        if np.allclose(A.conj().T@A, d*np.eye(len(V)),atol=1e-9): X.append(ch)
    xdim=len({min(c,G.inv(c)) for c in X})
    # containment: Re chi for chi in X satisfies eqs
    ok=True
    for ch in X:
        fv=[G.ev(ch,r).real for r in reps]
        for row in eqs:
            if abs(sum(a*b for a,b in zip(row,fv)))>1e-8: ok=False
    return dict(hyp=hyp,soldim=soldim,xdim=xdim,contain=ok,X=X,npairs=len(pairs),d=d)

def rand_digraph(G,n,d,rng):
    return {x:{y:rng.choice(G.els) for y in rng.sample(range(n),d)} for x in range(n)}

def block2(G,eps,nb,rng,share=False):
    # nb blocks; block i has vertices (2i,2i+1); successor pairs = a perfect pairing of vertices permuted
    n=2*nb; perm=list(range(n)); rng.shuffle(perm)
    succ=[(perm[2*i],perm[2*i+1]) for i in range(nb)]
    if share: succ=[succ[0]]*nb
    D={}
    for i in range(nb):
        y,yp=succ[i]; u1,u2,u3=[rng.choice(G.els) for _ in range(3)]
        u4=G.mul(eps,G.mul(u2,G.mul(u3,G.inv(u1))))
        D[2*i]={y:u1,yp:u3}; D[2*i+1]={y:u2,yp:u4}
    return D

def block3(G,om,nb,rng):
    n=3*nb; perm=list(range(n)); rng.shuffle(perm)
    D={}
    def pw(g,k):
        r=G.els[0]
        for _ in range(k): r=G.mul(r,g)
        return r
    for i in range(nb):
        ys=perm[3*i:3*i+3]; rs=[rng.choice(G.els) for _ in range(3)]; cs=[rng.choice(G.els) for _ in range(3)]
        for y in range(3):
            D[3*i+y]={ys[z]:G.mul(pw(om,(z*y)%3),G.mul(rs[z],cs[y])) for z in range(3)}
    return D

if __name__=="__main__":
    rng=random.Random(int(sys.argv[1]) if len(sys.argv)>1 else 1)
    groups={ 'Z4':((4,),(2,)), 'Z6':((6,),(3,)), 'Z8':((8,),(4,)), 'Z12':((12,),(6,)), 'Z3x3x2':((3,3,2),(0,0,1)), 'Z2x2':((2,2),(1,0)), 'Z2x4':((2,4),(0,2))}
    stats={}
    def rec(tag,res,D,G):
        st=stats.setdefault(tag,dict(n=0,hyp=0,bad_hyp=0,bad_contain=0,bigger_nohyp=0,trivX_hyp=0))
        st['n']+=1
        if not res['contain']: st['bad_contain']+=1; print('CONTAIN FAIL',tag,D)
        if res['hyp']:
            st['hyp']+=1
            if res['npairs']>0 and res['soldim']!=res['xdim']:
                st['bad_hyp']+=1; print('COUNTEREXAMPLE',tag,res,D)
            if res['xdim']==0: st['trivX_hyp']+=1
        elif res['soldim']>res['xdim']: st['bigger_nohyp']+=1
        return res
    for name,(mods,eps) in groups.items():
        G=Grp(mods)
        for t in range(40):
            nb=rng.choice([1,2,3])
            D=block2(G,eps,nb,rng); r=rec(name+' block2',analyse(G,D),D,G)
            if r['hyp']:
                # corollary: X = chars with chi(eps)=-1
                Xc=[c for c in G.chars() if abs(G.ev(c,eps)+1)<1e-9]
                if sorted(Xc)!=sorted(r['X']): print('COROLLARY X MISMATCH',name,D)
            if len(mods)==1 and r['hyp'] and r['soldim']!=math.ceil(mods[0]/4): print('DIM MISMATCH',name,r)
        for t in range(40):
            n=rng.choice([2,3,4]); d=rng.choice([2,3]) if n>=3 else 2
            D=rand_digraph(G,n,d,rng); rec(name+' rand',analyse(G,D),D,G)
        for t in range(10):
            D=block2(G,eps,2,rng,share=True); r=analyse(G,D)
            Xc=[c for c in G.chars() if abs(G.ev(c,eps)+1)<1e-9]
            st=stats.setdefault(name+' shared-succ',dict(n=0,hyp=0,Xdiff=0,bad_hyp=0))
            st['n']+=1; st['hyp']+=r['hyp']; st['Xdiff']+= sorted(Xc)!=sorted(r['X']); st['bad_hyp']+= (r['hyp'] and r['soldim']!=r['xdim'])
        if 3 in mods or mods[0]%3==0:
            om=tuple((m//3 if (m%3==0 and i==0) else 0) for i,m in enumerate(mods))
            for t in range(20):
                D=block3(G,om,rng.choice([1,2]),rng); rec(name+' block3',analyse(G,D),D,G)
    for k,v in stats.items(): print(k,v)
