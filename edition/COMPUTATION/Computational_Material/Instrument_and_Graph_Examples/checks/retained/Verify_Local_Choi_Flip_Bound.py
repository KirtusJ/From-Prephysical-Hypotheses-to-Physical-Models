"""Verification for Local Choi Population and Qubit Flip Probability.
Research direction and responsibility: Kirtus Justus, 7 November 2026.
Equality and interval checks are exact or outward-rounded. Seeded isometry
examples are supplemental numerical diagnostics. They do not simulate trials.
Requires Python 3, NumPy, and mpmath.
"""
from fractions import Fraction as F
import math
import mpmath as mp
import numpy as np

def need(ok):
    if not ok:
        raise ArithmeticError("Choi/flip bound verification failed")

def local_weight(kraus):
    n=0
    for K in kraus:
        A=K[::2,::2]; D=K[1::2,1::2]; H=(A+D)/2
        n+=np.vdot(H,H).real*2/4
    return n

def test_kraus(kraus, equality=False):
    need(np.allclose(sum(K.conj().T@K for K in kraus),np.eye(4),rtol=0,atol=1e-13))
    beta=sum(np.linalg.norm(K[1::2,0])**2 for K in kraus)
    w=local_weight(kraus)
    delta=4*(1-w)-beta-(1-math.sqrt(max(0,1-beta)))**2/2
    need(abs(delta)<1e-13 if equality else delta>=-1e-13)

# Rational unit-amplitude examples of saturating channels, including extremal beta.
for t in [F(0),F(1,20),F(7,17),F(1)]:
    x=(1-t*t)/(1+t*t); y=2*t/(1+t*t); beta=y*y
    # sum Tr((A+D)^*(A+D))/8, or directly (3+x)^2/16+(1-x)^2/16.
    w=F(1,4)*((1+x)**2/2+2)
    need(4*(1-w)==beta+(1-x)**2/2 and x*x+y*y==1)
    jump=np.zeros((4,4)); jump[1,0]=float(y)
    test_kraus([np.diag([float(x),1,1,1]),jump],True)
# Generic complex isometry examples, always using trace-preserving channels.
rng=np.random.default_rng(42)
for n in (1,2,6):
    for k in range(12):
        a=rng.normal(size=(4*n,4))+1j*rng.normal(size=(4*n,4))
        q,_=np.linalg.qr(a,mode='reduced');test_kraus(list(q.reshape(n,4,4)))
iv=mp.iv;iv.dps=50;s=iv.mpf(131)/320;h=iv.mpf(99)/100;q=iv.mpf(81711338569043)/224995905216000
a=s+(iv.sqrt(s*h)-iv.sqrt(q))**2/(1-h)+6*iv.mpf('0.01')/13
beta=1-(iv.sqrt(iv.mpf('3.92'))-1)**2
m=a+beta
H=(9+6*m+m*m+(1-m)**2)/16
for val,lo,hi in [(beta,'0.0397979746446661','0.0397979746446662'),(H,'0.8078263982873538','0.8078263982873539')]:
    need(val.a>iv.mpf(lo) and val.b<iv.mpf(hi))
print('Exact equality checks, complex isometry checks and outward decimal enclosures passed.')
