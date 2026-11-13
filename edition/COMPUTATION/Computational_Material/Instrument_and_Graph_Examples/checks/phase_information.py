"""Verify the signed graph phase law and fidelity sample bounds."""
from fractions import Fraction as F
from itertools import combinations, product
from math import isqrt

import mpmath as mp
import sympy as sp


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def pair_weights(steps):
    """Project onto character eigenspaces of the Cayley graph on Z4 x Z4."""
    spectrum = {}
    for k, l in product(range(4), repeat=2):
        eig = 6-sum((sp.I**((k*a+l*b)%4) for a,b in steps))
        require(eig in (0,4,8), 'unexpected eigenvalue')
        spectrum.setdefault(int(eig), []).append((k,l))
    sites = list(product(range(4),repeat=2))
    weights = {}
    for i,j in combinations(sites,2):
        da,db = j[0]-i[0],j[1]-i[1]
        coefficients=[]
        for eig in (0,4,8):
            modes=spectrum[eig]
            off=sum(sp.I**((k*da+l*db)%4) for k,l in modes)
            require(off.is_real,'spectral projector has imaginary part')
            coefficients.append((F(len(modes),16),F(int(off),16)))
        weights[i,j]=coefficients
    return weights


def radical_interval(x, digits=12):
    scale=10**digits
    v=isqrt(x.numerator*scale**2//x.denominator)
    return F(v,scale),F(v+1,scale)


def certify_count(c, r, s, n):
    # Bound the exact affinity by rational endpoints; no rounded log or root.
    masses=[(a+c*b, x+c*y) for (a,b),(x,y) in zip(r,s)]
    parts=[radical_interval(x*y) for x,y in masses]
    lo=sum(p[0] for p in parts);hi=sum(p[1] for p in parts)
    require(lo**(2*(n-1))>F(19,100),'preceding N should violate necessary condition')
    require(hi**(2*n)<F(19,100),'at N the affinity inequality should cease excluding')
    return masses


def main():
    rook_steps={(a,0) for a in (1,2,3)}|{(0,b) for b in (1,2,3)}
    shri_steps={(1,0),(3,0),(0,1),(0,3),(1,1),(3,3)}
    rook,shri=pair_weights(rook_steps),pair_weights(shri_steps)
    diff=[k for k in rook if rook[k]!=shri[k]]
    require(len(diff)==32 and len(rook)-len(diff)==88,'phase-sensitive pair count')
    target=((0,0),(0,2))
    r,s=rook[target],shri[target]
    require([b for a,b in r]==[F(1,16),F(1,8),F(-3,16)],'rook interference')
    require([b for a,b in s]==[F(1,16),-F(1,8),F(1,16)],'Shrikhande interference')
    require(sum(abs(b-y) for (a,b),(x,y) in zip(r,s))/2==F(1,4),'spectral TV')
    for c,n in ((F(1,10),2380),(-F(1,10),2402)):
        certify_count(c,r,s,n)
    # Independent direct quadrature against the abs-density difference.
    mp.mp.dps=65
    f=lambda u,lam:4*u*lam**2*mp.exp(-2*lam*u)
    crossing=mp.log(4)/8
    tv=mp.quad(lambda u:abs(f(u,4)-f(u,8))/8,[0,crossing,mp.inf])
    target_tv=(3+4*mp.log(2))/64
    require(abs(tv-target_tv)<mp.mpf('1e-58'),'direct scale integral')
    c=sp.symbols('c',real=True)
    A=sum(sp.sqrt((sp.Rational(a)+c*sp.Rational(b))*(sp.Rational(x)+c*sp.Rational(y)))
          for (a,b),(x,y) in zip(r,s))
    require(sp.simplify(A.diff(c,2).subs(c,0)/2+sp.Rational(5,144))==0,'affinity expansion')
    print('Independent character sums: 32 distinguishing pairs; 88 equal for all phases under the fixed labelling.')
    print('TV per unit |cos(phi)|: spectrum 1/4; scale (3+4 log 2)/64.')
    print('Fraction of one-record spectral TV retained:',mp.nstr(4*tv,18))
    print('IID spectral affinity: 1-A(c) = (5/144)c^2 + O(c^3).')
    print('Certified necessary counts at c=+0.1 and c=-0.1: 2380 and 2402, respectively.')


if __name__=='__main__':
    main()
