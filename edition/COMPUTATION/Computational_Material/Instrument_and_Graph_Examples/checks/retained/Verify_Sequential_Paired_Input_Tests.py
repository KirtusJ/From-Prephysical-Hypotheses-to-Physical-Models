"""Algebraic checks for the paired-input sequential working note.
Research direction and responsibility: Kirtus Justus, 7 November 2026, Vancouver.
Uses exact rational calculations and explicit two-dimensional matrix checks.
No device records, sampling, calibration or operating power are estimated.
"""
from fractions import Fraction as Q
from math import comb, log, sqrt
import numpy as np


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def verify_envelopes():
    delta = Q(7, 25)
    z = Q(2)  # exponential of the prespecified bet
    a, b = z - 1, 1 - 1 / z
    scalar = 1 + (a - b * (1 - delta)) / 2
    require(scalar == Q(33,25), "scalar-null corner")
    for p0,p1 in [(0,0),(delta,0),(1,1-delta),(1,1),(0,1)]:
        require(1 + (a*p0-b*p1)/2 <= scalar, "scalar-null vertex")
    c = Q(24,25)
    discriminant = (a-b)**2 + 4*a*b*(1-c*c)
    quantum = 1 + (a-b + sqrt(discriminant))/4
    x = np.array([1.,0.])
    y = np.array([float(c), float(delta)])
    # Optimizing projection on two pure states with overlap c.
    matrix = float(a)*np.outer(x,x) - float(b)*np.outer(y,y)
    eig, vectors = np.linalg.eigh(matrix)
    effect = np.outer(vectors[:,-1], vectors[:,-1])
    p0, p1 = x@effect@x, y@effect@y
    require(abs(1+(a*p0-b*p1)/2-quantum) < 2e-15, "quantum equality witness")
    require(abs(sqrt(p0*p1)+sqrt((1-p0)*(1-p1))-float(c)) < 2e-15,
            "witness classical fidelity")
    lower, upper = Q('1.2844521871910'), Q('1.2844521871911')
    require((4*(lower-1)-(a-b))**2 < discriminant < (4*(upper-1)-(a-b))**2,
            "quantum outward bounds")
    print("Scalar exponential moment 33/25; fidelity moment in (1.2844521871910, 1.2844521871911).")


def verify_selection_control():
    successes = (Q(9,200), Q(1,200), Q(39,40), Q(39,40))
    pstar = sum(successes)/4
    g0, g1 = [x/pstar for x in successes[:2]]
    require((g0,g1,pstar) == (Q(9,100),Q(1,100), Q(1,2)), "relative rates")
    # Difference of the square roots of the first two normalized Kraus amplitudes.
    deficit = (Q(3,10)-Q(1,10))**2 / 8
    require(1-deficit == Q(199,200), "local Choi weight")
    positive = successes[0]/sum(successes[:2])
    require(positive == Q(9,10), "selected arm imbalance")
    moment = Q(33,25)
    n=20
    total=Q(0)
    for k in range(n+1):
        exponent=2*k-n
        statistic=(Q(2)**exponent + Q(2)**(-exponent))/(2*moment**n)
        if statistic>=20:
            total+=comb(n,k)*positive**k*(1-positive)**(n-k)
    require(total == Q(43352333828283669431,50000000000000000000),
            "invalid selected-only test at twenty successes")
    require((2*positive-1)*log(2)>log(moment), "almost-sure growth under invalid selection")
    print("Selected-only rule exceeds 20 at the twentieth success with exact-model probability",float(total))


def linear_score(x, y, t):
    return sum((1-v)*xi + (1-1/v)*yi for xi,yi,v in zip(x,y,t))


def verification_factors(x, y, pstar, eps, t, two_arm=False):
    """Enumerate all arm and outcome possibilities, including every failure."""
    probs = (Q(1,3),)*3 if not two_arm else (Q(1,2),)*2
    eta = Q(1,8)
    total=Q(0)
    for i,prob in enumerate(probs):
        if i<2:
            joint = (x,y)[i]
            coefficients = [1-v if i==0 else 1-1/v for v in t]
            if two_arm:
                coefficients = [d-2*eps for d in coefficients]
            outcomes = list(zip(joint,coefficients))+[(1-sum(joint),Q(0))]
        else:
            outcomes=[(pstar,-8*eps),(1-pstar,Q(0))]
        for mass,value in outcomes:
            require(mass>=0,"invalid outcome probability")
            score = value/prob - (4*eps if two_arm else 0)
            factor = 1 + eta*score
            require(factor>=0,"negative factor")
            total+=prob*mass*factor
    bound=2*eps*(sum(x)+sum(y)+2) if two_arm else 8*eps*pstar
    require(total == 1+eta*(linear_score(x,y,t)-bound),"one-step expectation identity")
    return total


def verify_factor_controls():
    eps=Q(1,100)
    t=(Q(1,2),Q(2))
    # Equal first marginals on the postselection control; ordered outcomes are click, no click.
    x=(Q(9,200),Q(0)); y=(Q(1,200),Q(0))
    for two_arm in (False, True):
        require(verification_factors(x,y,Q(1,2),eps,t,two_arm)<=1,"null control")
        require(verification_factors((Q(1,2),Q(0)),(Q(0),Q(1,2)),Q(1,2),eps,t,two_arm)>1,
                "separating control")
    # When outputs are known only in one projective basis, a rational equality case.
    # r0=(9,4)/100, r1=(4,9)/100 have squared root-distance 2/100.
    x=(Q(9,100),Q(4,100));y=x[::-1];t=(Q(2,3),Q(3,2))
    require(linear_score(x,y,t)==Q(1,50),"support attainment")
    require(verification_factors(x,y,Q(1,4),eps,t)==1,"attained null expectation")
    projected_eps = Q(1,226)
    pstar_max = (sum(x) + sum(y) + 2) / 4
    require(linear_score(x,y,t) == 8*pstar_max*projected_eps, "projected support boundary")
    require(verification_factors(x,y,pstar_max,projected_eps,t,True) == 1,
            "two-input boundary expectation")
    print("Both all-attempt scores checked by exact enumeration; each has an attained mean-one boundary factor.")


if __name__ == "__main__":
    verify_envelopes()
    verify_selection_control()
    verify_factor_controls()
