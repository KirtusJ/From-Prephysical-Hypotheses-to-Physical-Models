"""Model-only checks. Research direction and responsibility: Kirtus Justus."""
from fractions import Fraction as F
from math import sqrt
import numpy as np
import sympy as sp

def check(test, message):
    if not test:
        raise ArithmeticError(message)

def check_inversion():
    x,y,g0,g1=sp.symbols('x y g0 g1',real=True)
    # x = sqrt(g0*(1-beta)); y = sqrt(g1).
    cost= g0-x**2 + (x-y)**2/2
    check(sp.expand(2*cost-(2*g0+2*y**2-(x+y)**2))==0, 'inversion')

def endpoints():
    for g0,g1,beta in [(F(4),F(0),F(0)),(F(4),F(0),F(1)),(F(1,4),F(7,4),F(3,5)),(F(1),F(1),F(1,25))]:
        u=(4-g0-g1)/2
        A=np.diag([sqrt(g0*(1-beta)),sqrt(g1),sqrt(u),sqrt(u)])
        B=np.zeros((4,4)); B[1,0]=sqrt(g0*beta)
        # Flatten first, then project onto an independently built local Pauli basis.
        I=np.eye(2); X=np.array([[0,1],[1,0]]); Y=np.array([[0,-1j],[1j,0]]); Z=np.diag([1,-1])
        ket=lambda k:k.reshape(-1)/2
        choi=sum(np.outer(ket(v),ket(v).conj()) for v in [A,B])
        w=sum(np.vdot(ket(np.kron(v,I)),choi@ket(np.kron(v,I))).real for v in [I,X,Y,Z])
        rhs=float(g0*beta)+(sqrt(g0*(1-beta))-sqrt(g1))**2/2
        check(abs(4*(1-w)-rhs)<1e-12,'branch flip attainment')
    for t in [F(1,10000),F(1,4),F(3,5),F(1)]:
        lam=[F(3,5),F(1,5),F(1,5),F(0)]
        p=sum(v*v for v in lam);m=max(lam)
        low=t*t*p+(1-t)**2/12;high=t*t*p+(1-t)**2+2*t*(1-t)*m
        # Spectra of the exhibited endpoints, including rank-deficient output and t=1.
        eval_min=[t*v for v in lam]+[(1-t)/12]*12
        eval_max=[1-t+t*m]+[t*v for v in lam[1:]]
        check(sum(v*v for v in eval_min)==low and sum(v*v for v in eval_max)==high,'purity endpoints')
        check(1-max(eval_max)==t*(1-m),'sharp distance to an arbitrary pure branch')
    print('Block inversion, flip equality, purity spectra and rank-one distance endpoints passed.')

if __name__=='__main__':
    check_inversion(); endpoints()
