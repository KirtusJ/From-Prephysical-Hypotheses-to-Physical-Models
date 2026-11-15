"""P5 follow-up: explicit counterfeit under per-tag-branch power reading (outside the note's model).
Predicate fixed first: find nonnegative weights over modes with q!=1 (c in [0,1]) whose means equal
(x,t)=(187/512, 11/256) exactly in fair-arm X' and pi-arm Y. Exact Fractions for integer q and +-inf."""
import sys, os
from fractions import Fraction as F
from itertools import combinations
out = sys.argv[1]
if os.path.exists(out): sys.exit("refuse overwrite")
s=F(5,16); g=s*(1-2*s)**2; b=4*s*(1-s)**2; cr=4*s*(1-2*s)*(1-s)
def R(q,z):
    if q=="inf": return F(0) if z<F(1,2) else F(1)
    if q=="-inf": return F(1) if z<F(1,2) else F(0)
    return z**q/(z**q+(1-z)**q)
modes=[]
for q in [0,2,3,-1,-2,"inf","-inf"]:
    for c in [F(0),F(1,2),F(1)]:
        y=1-(g+b+cr*c); z=1-(g+b-cr*c)
        modes.append((q,c,(R(q,y)+R(q,z))/2,R(q,y)))
x,t=F(187,512),F(11,256); sols=[]
for (m1,m2,m3) in combinations(modes,3):
    # solve w1+w2+w3=1, sum w X = x, sum w Y = t
    a=[[1,1,1],[m1[2],m2[2],m3[2]],[m1[3],m2[3],m3[3]]]; rhs=[F(1),x,t]
    import copy
    M=[row[:]+[r] for row,r in zip(a,rhs)]
    try:
        for i in range(3):
            p=next(k for k in range(i,3) if M[k][i]!=0); M[i],M[p]=M[p],M[i]
            for k in range(3):
                if k!=i:
                    f=M[k][i]/M[i][i]; M[k]=[u-f*v for u,v in zip(M[k],M[i])]
        w=[M[i][3]/M[i][i] for i in range(3)]
    except StopIteration: continue
    if all(v>=0 for v in w): sols.append([(str(m[0]),str(m[1]),str(v)) for m,v in zip((m1,m2,m3),w)])
with open(out,"x") as fh:
    fh.write(f"{len(sols)} solutions\n"); [fh.write(repr(s_)+"\n") for s_ in sols[:20]]
print(len(sols)); print(sols[:3])
