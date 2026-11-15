"""Micro-review of cor:maskorbit. Predicates fixed before first run:
P0 control: N=6 -> M=3, {zeta^-2} = exponents {0,2,4} of e^(2pi i/6).
P1 for N=3..12: {zeta^-2 : zeta^N=1} == {M-th roots}, M=N/gcd(N,2).
P2 each map as written preserves |.|=1 and a'd'=-b'c' and sends u to u,u,zeta^-2 u,conj u (exact, angles in Q/Z).
P3 converse: for all qualifying coin pairs on a grid with Re(u^M) equal, the stated sequence reaches coin 2 exactly.
P4 N=4: u=1 and u=-1 coins (+-1 entries) equal P on all masks t<=3 (numeric brute force); no map with phases in {+-1} connects them; zeta=i does.
P5 rail phase with beta!=0 changes P for some mask (so sharpness needed); maps preserve P from sharp start alpha=1 (numeric).
Exact arithmetic: unit numbers stored as angles (Fraction mod 1). Hypothesis tested per coin."""
from fractions import Fraction as F
from math import gcd
import itertools, cmath, random
def m1(x): return x % 1
def M_(N): return N//gcd(N,2)
fails=[]
# P0
s={m1(F(-2*k,6)) for k in range(6)}; print("P0", M_(6), sorted(x*6 for x in s)); 
if not(M_(6)==3 and s=={F(0),F(1,3),F(2,3)}): fails.append("P0")
# P1
for N in range(3,13):
    M=M_(N); s={m1(F(-2*k,N)) for k in range(N)}; t={F(j,M) for j in range(M)}
    if s!=t: fails.append(("P1",N))
print("P1 done")
def qual(c): a,b,cc,d=c; return m1(a+d)==m1(b+cc+F(1,2))
def u(c): a,b,cc,d=c; return m1(b+cc-2*a)
grid=[F(k,8) for k in range(8)]
coins=[(a,b,c,m1(b+c+F(1,2)-a)) for a in grid for b in grid for c in grid]
nq=sum(qual(c) for c in coins); print("P2 coins",len(coins),"qualify",nq)
for c in coins:
  for g in grid:
    a,b,cc,d=c
    for name,img,exp in [("common",tuple(m1(x+g) for x in c),u(c)),
                         ("rail",(a,m1(b-g),m1(cc+g),d),u(c)),
                         ("conj",tuple(m1(-x) for x in c),m1(-u(c)))]:
        if not qual(img) or u(img)!=exp: fails.append(("P2",name,c,g))
    for N in range(3,9):
      for k in range(N):
        z=F(k,N); img=(m1(a+z),m1(b-z),m1(cc+z),m1(d-z))
        if not qual(img) or u(img)!=m1(u(c)-2*z): fails.append(("P2site",c,N,k))
print("P2 done")
# P3 converse as written
def reach(c1,c2,N):
    M=M_(N)
    if m1(M*u(c1))!=m1(M*u(c2)):
        if m1(-M*u(c1))!=m1(M*u(c2)): return None  # Re differ
        c1=tuple(m1(-x) for x in c1)
    ks=[k for k in range(N) if m1(u(c1)-2*F(k,N))==u(c2)]
    if not ks: return False
    z=F(ks[0],N); a,b,c,d=c1; c1=(m1(a+z),m1(b-z),m1(c+z),m1(d-z))
    g=m1(c2[0]-c1[0]); c1=tuple(m1(x+g) for x in c1)
    lam=m1(c2[2]-c1[2]); a,b,c,d=c1; c1=(a,m1(b-lam),m1(c+lam),d)
    return c1==c2
random.seed(1); cnt=0; ok=0
sub=coins[::7]
for N in (3,4,5,6,8):
  for c1 in sub:
    for c2 in sub:
      r=reach(c1,c2,N)
      if r is None: continue
      cnt+=1; ok+= r is True
      if r is not True: fails.append(("P3",N,c1,c2))
print("P3 pairs with equal Re(u^M):",cnt,"reached:",ok)
# numeric P
def P(coin,N,masks,x,rho,alpha=1,beta=0):
    a,b,c,d=[cmath.exp(2j*cmath.pi*float(v)) for v in coin]
    t=len(masks); tot=0
    for start,amp0 in (("R",alpha),("L",beta)):
      if amp0==0: continue
      S=0
      for w in itertools.product("RL",repeat=t):
        pos=0; r=start; gain=1; okw=True
        for j,s in enumerate(w):
          gain*= {("R","R"):a,("R","L"):b,("L","R"):c,("L","L"):d}[(r,s)]
          pos=(pos+(1 if s=="R" else -1))%N; r=s
          if pos not in masks[j]: okw=False;break
        if okw and pos==x and r==rho: S+=gain
      tot+=amp0*S
    return abs(tot)**2/2**t
def maxdiff(c1,c2,N,T,**kw):
    subsets=[frozenset(s) for k in range(N+1) for s in itertools.combinations(range(N),k) if s]
    md=0
    for t in range(1,T+1):
      for masks in itertools.product(subsets,repeat=t):
        for x in range(N):
          for rho in "RL":
            md=max(md,abs(P(c1,N,masks,x,rho,**kw)-P(c2,N,masks,x,rho,**kw)))
    return md
h=F(1,2)
cp=(F(0),F(0),F(0),h); cm=(F(0),F(0),h,F(0))  # (1,1,1,-1) u=1 ; (1,1,-1,1) u=-1
print("P4 qualify",qual(cp),qual(cm),"u",u(cp),u(cm))
d4=maxdiff(cp,cm,4,3); print("P4 maxdiff u=1 vs u=-1, N=4,t<=3:",d4)
if d4>1e-12: fails.append(("P4",d4))
ci=(F(0),F(0),F(1,4),F(3,4)); print("P4 ctrl u=i qual",qual(ci),"maxdiff vs u=1:",maxdiff(cp,ci,4,3))
pm=[F(0),h]; con=False
for z in [F(0),h,F(1,4),F(3,4)]:
  a,b,c,d=cp; im=(m1(a+z),m1(b-z),m1(c+z),m1(d-z))
  for g in pm:
    for l in pm:
      for cj in (0,1):
        x=tuple(m1(v+g) for v in im); x=(x[0],m1(x[1]-l),m1(x[2]+l),x[3])
        if cj: x=tuple(m1(-v) for v in x)
        if x==cm: print("P4 connect zeta angle",z,"g",g,"lam",l,"conj",cj); con=True
# P5 rail phase with beta != 0, N=3
c0=(F(0),F(1,8),F(3,8),m1(F(1,8)+F(3,8)+h)); a,b,c,d=c0; l=F(1,4); cr=(a,m1(b-l),m1(c+l),d)
print("P5 sharp rail maxdiff",maxdiff(c0,cr,3,3))
print("P5 beta!=0 rail maxdiff",maxdiff(c0,cr,3,2,alpha=2**-.5,beta=2**-.5))
z=F(1,3); cs=(m1(a+z),m1(b-z),m1(c+z),m1(d-z)); print("P5 sharp site maxdiff N=3",maxdiff(c0,cs,3,3))
print("P5 sharp conj maxdiff",maxdiff(c0,tuple(m1(-v) for v in c0),3,3))
print("FAILS",len(fails),fails[:5])
