"""CONTROL by brute enumeration of words. Z/5, chi(a)=1,chi(b)=i,chi(c)=1,chi(d)=-i, start 3/5|0,R>+4i/5|0,L>,
no mask, port (3,1,R). Gaussian rationals as (re,im) Fractions."""
from fractions import Fraction as F
from itertools import product
def mul(x,y): return (x[0]*y[0]-x[1]*y[1], x[0]*y[1]+x[1]*y[0])
g={('R','R'):(F(1),F(0)),('R','L'):(F(0),F(1)),('L','R'):(F(1),F(0)),('L','L'):(F(0),F(-1))}
start={'R':(F(3,5),F(0)),'L':(F(0),F(4,5))}
amp=[F(0),F(0)]
for r0 in 'RL':
    for w in product('RL',repeat=3):
        x=0;prev=r0;z=start[r0]
        for s in w:
            z=mul(z,g[(prev,s)]); x+= 1 if s=='R' else -1; prev=s
        if x%5==1 and prev=='R':
            print(r0,''.join(w),z); amp[0]+=z[0]; amp[1]+=z[1]
print('P =',(amp[0]**2+amp[1]**2)/8)
