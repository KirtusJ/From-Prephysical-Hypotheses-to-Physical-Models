"""Deterministic exact checks of a proposed four-preparation, attempt-level e-process.

No synthetic trials and no physical-device records are used.
Scientific research direction: Kirtus Justus; verification support: ChatGPT.
"""
from fractions import Fraction as Q
from math import comb, exp, log, sqrt
import numpy as np


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def squared_hellinger(x, y):
    return sum((sqrt(float(a))-sqrt(float(b)))**2 for a,b in zip(x,y))


def score_expectation(arms, t, eps, pi=(Q(1,4),)*4):
    """Return exact expected score, enumerate outcomes (including failure)."""
    d0=[1-u for u in t]
    d1=[1-1/u for u in t]
    total=Q(0)
    mins=[]
    for i in range(4):
        r=arms[i]
        s=sum(r)
        require(Q(0) <= s <= Q(1), 'invalid per-attempt success rate')
        for y in range(2):
            dy = d0[y] if i==0 else d1[y] if i==1 else Q(0)
            value = (dy-2*eps)/pi[i]
            total += pi[i]*r[y]*value
            mins.append(value)
        # Failure remains an eligible attempt and has multiplicative factor 1.
        mins.append(Q(0))
    dual=sum(d0[y]*arms[0][y]+d1[y]*arms[1][y] for y in range(2))
    expected=dual-2*eps*sum(sum(a) for a in arms)
    require(total==expected,'four-arm expectation identity failed')
    return total, min(mins), dual


def factor_check(arms,t,eps,pi=(Q(1,4),)*4):
    ex,minimum,dual=score_expectation(arms,t,eps,pi)
    require(ex<=0,'not a valid null population')
    # eta is fixed before preparation choice; all possible factors positive.
    eta=Q(1,2)*(1/(Q(1)+abs(minimum)))
    require(1+eta*minimum>=0,'negative one-step factor')
    require(1+eta*ex<=1,'not a supermartingale factor')
    return ex,1+eta*ex,dual


def check_boundary_branch():
    """One exact-form Kraus construction saturating the four-arm population null."""
    raw = [[Q(9,100),Q(4,100)], [Q(4,100),Q(9,100)]]
    # K[e,output,input].  The two tested inputs have opposite second-output flags.
    K=np.zeros((3,4,4),dtype=complex)
    for i in range(2):
        for y in range(2):
            K[y,2*y+i,i]=sqrt(float(raw[i][y]))
    K[2,0,2]=1.0
    K[2,1,3]=1.0
    E=sum(k.conj().T@k for k in K)
    s=[sum(v) for v in raw]+[Q(1),Q(1)]
    require(np.allclose(E,np.diag([float(x) for x in s]),atol=1e-14),'branch effect inconsistent')
    pstar=float(sum(s)/4)
    w=sum(np.linalg.norm(k[::2,::2]+k[1::2,1::2])**2 for k in K)/(8*pstar)
    require(abs(w-float(1-Q(1,226)))<2e-14,'Kraus witness does not saturate population null')
    for i in range(2):
        for y in range(2):
            event=sum(np.linalg.norm(k[2*y:2*y+2,i])**2 for k in K)
            require(abs(event-float(raw[i][y]))<2e-14,'wrong measured Kraus raw rate')
    print('QUANTUM BOUNDARY WITNESS: valid CP-TNI Kraus map, w=1-1/226, four-arm null equality')


def main():
    eps=Q(1,226)
    # Exact equality of dual and squared-Hellinger constraints; all four inputs tested.
    arms=[(Q(9,100),Q(4,100)),(Q(4,100),Q(9,100)),(Q(1),Q(0)),(Q(1),Q(0))]
    t=(Q(2,3),Q(3,2))
    ex,ef,dual=factor_check(arms,t,eps)
    require(dual==Q(1,50) and ex==0 and ef==1,'attainable null boundary')
    print('FOUR-INPUT BOUNDARY: exact dual Hellinger = 1/50; expected e-factor = 1')

    check_boundary_branch()

    # Exact trace-decreasing selection example; all successful outputs click.
    successes=(Q(9,200),Q(1,200),Q(39,40),Q(39,40))
    require(sum(successes)/4==Q(1,2),'wrong mean branch success')
    require(successes[0]/(successes[0]+successes[1])==Q(9,10),'wrong selected arm distribution')
    require(Q(1)-((Q(3,10)-Q(1,10))**2)/8==Q(199,200),'wrong local Choi population')
    arms2=[(v,Q(0)) for v in successes]
    ex2, ef2, dual2=factor_check(arms2,(Q(1,3),Q(1)),Q(1,100))
    require(dual2==Q(1,50) and ex2==Q(-1,50),'bad rare-selection attempt-level comparison')
    print('RARE-SUCCESS CONTROL: success rates 0.045, 0.005, 0.975, 0.975; E[X] = -1/50')
    print('RARE-SUCCESS CONTROL: attempt-level e-factor expectation =',f'{ef2.numerator}/{ef2.denominator}')

    # Check the original invalid success-only test at n=20.
    n=20
    bad=Q(0)
    crossing=[]
    for k in range(n+1):
        M=(Q(2)**(2*k-n)+Q(2)**(n-2*k))/(2*(Q(33,25)**n))
        if M>=20:
            bad+=comb(n,k)*Q(9,10)**k*Q(1,10)**(n-k)
            crossing.append(k)
    require(crossing==[0,1,2,3,17,18,19,20],'bad crossing region')
    require(bad==Q(43352333828283669431,50000000000000000000),'bad selected-only rejection')
    print('INVALID SELECTED-ONLY REJECTION AT 20 SUCCESSES:',bad,format(float(bad),'.16f'))

    # Independent exponential-moment arithmetic from the published proof.
    A=exp(log(2))-1
    B=1-exp(-log(2))
    c=.96
    Fc=1+(A-B+sqrt((A-B)**2+4*A*B*(1-c*c)))/4
    Fdelta=(exp(log(2))+(1-.28)*exp(-log(2))+.28)/2
    require(abs(Fc-1.2844521871910197)<1e-13 and abs(Fdelta-1.32)<1e-13,'bad moment bounds')
    print('EXPONENTIAL MOMENT: fidelity constrained',format(Fc,'.15f'),'scalar',format(Fdelta,'.2f'))
    print('All checks passed without optimization-sensitive assertions.')


if __name__=='__main__':
    main()
