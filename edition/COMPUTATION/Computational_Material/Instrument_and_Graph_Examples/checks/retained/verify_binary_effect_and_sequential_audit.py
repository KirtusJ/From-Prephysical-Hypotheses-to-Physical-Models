#!/usr/bin/env python3
"""Deterministic verification of a selection counterexample and a calibrated qubit effect.
No hardware records, random samples, or invented observations. Python standard library.
Research direction: Kirtus Justus. Mathematical/computational assistance: ChatGPT (OpenAI).
7 November 2026, Vancouver, BC, UTC-7.
"""
from fractions import Fraction as F
from math import comb, sqrt


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def success_only_statistic(n,k):
    null_mgf=F(33,25)
    return (F(2)**(2*k-n) + F(2)**(n-2*k))/(2*null_mgf**n)


def stopping_probabilities():
    prob=F(9,10)
    n=20
    terminal=sum(F(comb(n,k))*prob**k*(1-prob)**(n-k)
                 for k in range(n+1) if success_only_statistic(n,k)>=20)
    require(terminal == F(43352333828283669431,50000000000000000000), "terminal crossing")
    alive={0:F(1)}
    hit=F(0)
    first_hits={}
    for n in range(1,21):
        next_alive={}
        new=F(0)
        for k,mass in alive.items():
            for dk,branch_prob in ((0,1-prob),(1,prob)):
                new_k=k+dk
                amount=mass*branch_prob
                if success_only_statistic(n,new_k)>=20:
                    new+=amount
                else:
                    next_alive[new_k]=next_alive.get(new_k,F(0))+amount
        alive=next_alive
        hit+=new
        if new>0:
            first_hits[n]=new
    require(hit==F(449300191961080193,500000000000000000),"cumulative crossing")
    require(set(first_hits)=={9,13,16,19},"first crossing dates")
    require(sum(first_hits.values())==hit,"first-hit partition")
    print('Terminal 20 =',terminal,'=',format(float(terminal),'.16f'))
    print('Cumulative through 20 =',hit,'=',format(float(hit),'.16f'))
    print('First hitting successes =',','.join(map(str,sorted(first_hits))))


def calibrated_effect(L,U,s0,s1,z0,z1):
    require(F(0)<=L<U<=F(1),"effect spectrum")
    gap=U-L
    vs=[]
    for s,z in ((s0,z0),(s1,z1)):
        require(F(0)<=s<=F(1) and L*s<=z<=U*s,"probability feasibility")
        plus=(z-L*s)/gap
        minus=(U*s-z)/gap
        require(plus>=0 and minus>=0 and plus+minus==s,"inversion")
        vs.append((plus,minus))
    return vs


def d_hellinger(x,y):
    return sum((sqrt(float(a))-sqrt(float(b)))**2 for a,b in zip(x,y))


def calibrated_detector_demo():
    # Purely mathematical negative control. Different experimental instruments are not claimed.
    L,U=F(1,5),F(4,5)
    hidden0=(F(7,10),F(3,10))
    hidden1=hidden0[::-1]
    successes=(F(1),F(1))
    clicks=[L*hidden[1]+U*hidden[0] for hidden in (hidden0,hidden1)]
    v0,v1=calibrated_effect(L,U,*successes,*clicks)
    require(v0==hidden0 and v1==hidden1,"correct spectral inversion")
    d_spec=d_hellinger(v0,v1)
    d_raw=d_hellinger((clicks[0],1-clicks[0]),(clicks[1],1-clicks[1]))
    require(d_spec>0.08>d_raw,"spectral data should separate but raw data should not")
    # An input-dependent detector can create the same apparent contrast from identical |0> states.
    L0,U0=L,U
    z0=U0  # effect diag(U,L), output state |0><0|
    z1=L0  # effect diag(L,U), same output state
    v0,v1=calibrated_effect(L,U,F(1),F(1),z0,z1)
    require(v0==(F(1),F(0)) and v1==(F(0),F(1)),"rotated-effect negative control")
    print('Effect eigenvalues =',L,U,'spectral gap =',U-L)
    print('Common-effect population demo: raw rates',clicks, 'D_raw',format(d_raw,'.12f'), 'D_spectral',format(d_spec,'.12f'))
    print('At pstar=1 and w0=.99, threshold=.08: raw discrepancy passes; calibrated discrepancy rejects.')
    print('Different effects with identical eigenvalues and identical states can falsely imply D_spectral=2.')
    # Sharp equality check at equal successful rates s=pstar=1 and w0=0.99.
    w0=F(99,100)
    bound_squared=F(1)-(F(1)-4*(1-w0))**2  # delta_max^2 = (7/25)^2
    require(bound_squared==F(49,625), "equal-success sharp gap")
    v0=(F(16,25),F(9,25));v1=v0[::-1]
    z0=L*v0[1]+U*v0[0];z1=L*v1[1]+U*v1[0]
    require(z0-z1==(U-L)*F(7,25)==F(21,125),"sharp observed click separation")
    require(abs(d_hellinger(v0,v1)-float(8*(1-w0)))<1e-14,"attained Hellinger boundary")
    print('At equal success s=pstar=1 and w0=.99, sharp common-effect click difference:',z0-z1,
          '(as decimal',format(float(z0-z1),'.6f')+')')
    # Identity channel on two qubits makes both first-qubit outputs |0>.
    # Input-dependent effects diag(U,L) and diag(L,U) then give U and L clicks;
    # their spectra agree but the common-effect premise is false.
    require(U-L>F(21,125),"input-dependent effect counterexample")
    print('The identity channel plus input-dependent effects has click difference',U-L,
          'despite identical detector spectra. This is not a common-effect test.')

    # Exact score identity in each tested arm using t+ = 2/3, t- = 3/2.
    tplus,tminus=F(2,3),F(3,2)
    for i,(s,z) in enumerate(((successes[0],clicks[0]),(successes[1],clicks[1]))):
        dp=(1-tplus) if i==0 else (1-F(1)/tplus)
        dm=(1-tminus) if i==0 else (1-F(1)/tminus)
        def score(y):
            return dm+(F(y)-L)*(dp-dm)/(U-L)
        left=score(1)*z+score(0)*(s-z)
        plus,minus=(hidden0,hidden1)[i]
        right=dp*plus+dm*minus
        require(left==right,"attempt-level score identity")
    print('Spectral-score expectation equals observed-bit-score expectation exactly.')
    print('Score click-minus-no-click factor = 1/(U-L) times the spectral coefficient difference.')


if __name__=='__main__':
    stopping_probabilities()
    calibrated_detector_demo()
    print('All deterministic checks passed.')
