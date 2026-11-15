"""Predicates fixed before first run (seed 20261113, unused: exhaustive).
P1 counts (-5,2,2,-5,6) sum 0, autocorr (94,-76,29,29,-76).
P2 |c^(r)|^2 / K equals (235 -+105 sqrt5)/512 for r=1,2 for a single K (K reported).
P3 locality: for odd N, signed residues |a|<=u,|b|<=v, N | ab-1, N>uv+1 => a=b=+-1 (hypothesis N>uv+1 tested per instance; count qualifying).
P4 largest odd N with nontrivial reciprocal pair, budget B: even B -> B^2+1; odd B>=3 -> B(B-1)+1. B up to 15 (note's text; 13,15 extra).
P5 two-way degree: n=+-2^j unit mod all odd M; Lipschitz factor at M = min(a mod M, -a mod M) adjacent attained, M up to 41.
"""
import cmath,math,json,os
R={}
c=[-5,2,2,-5,6]; M=5
ac=[sum(c[y]*c[(y+k)%5] for y in range(5)) for k in range(5)]
R['P1']=sum(c)==0 and ac==[94,-76,29,29,-76]
F=[abs(sum(c[y]*cmath.exp(2j*math.pi*r*y/5) for y in range(5)))**2 for r in range(5)]
t={1:(235-105*5**.5)/512,2:(235+105*5**.5)/512}
K=[F[r]/t[r] for r in (1,2)]; R['P2_K']=K; R['P2']=abs(K[0]-K[1])<1e-9*K[0] and F[0]<1e-12
q=0;bad=[]
for N in range(3,80,2):
  for u in range(1,12):
    for v in range(1,12):
      if not N>u*v+1: continue
      q+=1
      for a in range(-u,u+1):
        for b in range(-v,v+1):
          if (a*b-1)%N==0 and not (a==b==1 or a==b==-1): bad.append((N,u,v,a,b))
R['P3']=not bad; R['P3_qualifying']=q
p4={}
for B in range(2,16):
  best=max([N for N in range(3,B*B+3,2) for a in range(-B,B+1) for b in range(-B,B+1) if (a*b-1)%N==0 and not(a==b==1 or a==b==-1)],default=None)
  p4[B]=(best, B*B+1 if B%2==0 else B*(B-1)+1)
R['P4']=all(x==y for x,y in p4.values()); R['P4_detail']=p4
ok=True
for M in range(3,42,2):
  for a in range(1,M):
    if math.gcd(a,M)!=1: continue
    d=lambda x:min(x%M,(-x)%M)
    L=max(d(a*k)/d(k) for k in range(1,M))
    ok&= L==d(a)
R['P5']=ok
# extra: event prob 47/8388608 = (1/65536)* mean over localized prior?
pr=sum(F)/5; R['Fsum']=F; 
json.dump(R,open(os.path.join(os.path.dirname(__file__),'own_result.json'),'x'),indent=1,default=str)
print(R)
