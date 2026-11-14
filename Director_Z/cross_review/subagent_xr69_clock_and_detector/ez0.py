# helper: one concrete rail-blind (ez=0) coherent false pass and its behaviour under fair / biased terminal sign bit
from fractions import Fraction as F
def traj(a,s):
    v=(F(0),F(0),F(1)); o=[v]
    for _ in range(3): X,Y,Z=v; v=(a*Z+s*Y,s*Z-a*Y,X); o.append(v)
    return o
def resp(src,e,k):  # k = 1-2*pb multiplies coherence terms
    return [sum(w*(1+k*(e[0]*v[0]+e[1]*v[1])+e[2]*v[2])/2 for (a,s,w) in src for v in [traj(a,s)[t]]) for t in range(4)]
found=0
g=[F(i,5) for i in range(-5,6)]
for ex in g:
  for ey in g:
    if ex*ex+ey*ey>1: continue
    for w in [F(i,10) for i in range(1,10)]:
      for (n1,p1),(n2,p2) in [((a,b)) for a in PH for b in PH] if False else []: pass
PH={"1":(1,0),"-1":(-1,0),"i":(0,1),"-i":(0,-1)}
for n1 in PH:
  for n2 in PH:
    for w in [F(i,10) for i in range(1,10)]:
      for ex in g:
        for ey in g:
          if ex*ex+ey*ey>1 or found: continue
          src=[(F(PH[n1][0]),F(PH[n1][1]),w),(F(PH[n2][0]),F(PH[n2][1]),1-w)]
          r=resp(src,(ex,ey,F(0)),1); d=r[0]-r[1]
          if d==0: continue
          b2,b3=(r[2]-r[1])/d,(r[3]-r[1])/d
          if 1-b3+b2+F(1,4)==0 and 0<=2*r[1]-r[0]<=1 and all(min(r[0],2*r[1]-r[0])<=y<=max(r[0],2*r[1]-r[0]) for y in r[2:]):
            found=1; print("source",n1,w,n2,1-w,"effect bloch",(ex,ey,0),"resp",r,"b2,b3",b2,b3)
            for pb in (F(1,2),F(11,20),F(501,1000)):
              rr=resp(src,(ex,ey,F(0)),1-2*pb); dd=rr[0]-rr[1]
              print(" sign-bit prob",pb,"resp",rr,"d",dd,"W", None if dd==0 else 1-(rr[3]-rr[1])/dd+(rr[2]-rr[1])/dd+F(1,4))
