"""Exploration: complete reverse search in the abstract packet model, counts only.
state: cyclic sequence of nonempty packets (multisets of levels). Reverse move (un-copy):
 (a) adjacent packets P_i=y+z, P_{i+1}=z+x (cyclic, wrap lowers level by 1), z nonempty -> (y,z,x), empties dropped
 (b) one packet P=y+z+z+x -> (y,z,x)
 k=1 wrap handled by also allowing a plain split when k==1.
Reducible iff reaches a single walk."""
import sys, itertools
from collections import Counter
sys.setrecursionlimit(100000)
def canon(s):
    k=len(s);best=None
    for i in range(k):
        rot=list(s[i:])+[tuple(l-1 for l in p) for p in s[:i]]
        m=min(l for p in rot for l in p)
        rot=tuple(tuple(sorted(l-m for l in p)) for p in rot)
        if best is None or rot<best: best=rot
    return best
def submultisets(c, nonempty=True):
    keys=sorted(c)
    for choice in itertools.product(*[range(c[k]+1) for k in keys]):
        z=tuple(l for k,n in zip(keys,choice) for l in [k]*n)
        if z or not nonempty: yield z
def sub(p,z):
    c=Counter(p); c.subtract(z); return tuple(sorted(c.elements()))
memo={}
def red(s):
    if s in memo: return memo[s]
    n=sum(len(p) for p in s)
    if n==1: memo[s]=True; return True
    memo[s]=False
    k=len(s); res=False
    cands=[]
    if k==1:
        p=s[0]
        for z in submultisets(Counter(p)):
            if len(z)<len(p): cands.append((z,sub(p,z)))
    for rot in range(k if k>1 else 0):
        t=list(s[rot:])+[tuple(l-1 for l in p) for p in s[:rot]]
        a,b=Counter(t[0]),Counter(t[1])
        common=a&b
        for z in submultisets(common):
            y=sub(t[0],z); x=sub(t[1],z)
            cands.append(tuple(q for q in (y,z,x) if q)+tuple(t[2:]))
    for i in range(k):
        p=Counter(s[i]); half=Counter({l:c//2 for l,c in p.items() if c>=2})
        for z in submultisets(half):
            rest=Counter(p); rest.subtract(z); rest.subtract(z); rest=+rest
            for y in submultisets(rest,nonempty=False):
                x=sub(tuple(sorted(rest.elements())),y)
                cands.append(s[:i]+tuple(q for q in (y,z,x) if q)+s[i+1:])
    for c in cands:
        if red(canon(c)): res=True; break
    memo[s]=res; return res
def from_w(w):
    P=tuple(sorted(l for l in range((len(w)+1)//2) for _ in range(w[2*l])))
    Q=tuple(sorted(l for l in range(len(w)//2) for _ in range(w[2*l+1])))
    return tuple(p for p in (P,Q) if p)
if __name__=="__main__":
    for w in [(1,2,3,5,1),(1,2,3,3,2),(2,3,3,2,1),(1,2,2,1),(3,5,2,3),(1,1,2,1),(1,0,3,0,1),(1,0,1,0,1),(1,0,2,0,1)]:
        print(w, red(canon(from_w(w))), len(memo))
