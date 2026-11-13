"""Exact and explicit checks for four-input, two-outcome conditional operations.

All values are mathematical model data. No sampling trials, hardware observations,
or claims about physical apparatus. Scientific direction: Kirtus Justus.
analytical/computational assistance: ChatGPT (OpenAI).
"""
from fractions import Fraction as F
from math import sqrt
import numpy as np
import hashlib


def require(c, description):
    if not c:
        raise ArithmeticError(description)


def score_expectation(rows, slope, eps, pi):
    """Use exact rational arithmetic for the inverse-randomization dual score."""
    coeff = []
    for b in range(2):
        coeff.extend([[1-t for t in slope[b]], [1-1/t for t in slope[b]]])
    terms = []
    for i in range(4):
        for y in range(2):
            terms.append(pi[i] * rows[i][y] * (coeff[i][y]-2*eps)/pi[i])
    return sum(terms), coeff


def main():
    rows=[(F(9,100),F(4,100)),(F(4,100),F(9,100)),
          (F(16,100),F(9,100)),(F(9,100),F(16,100))]
    success=[sum(x) for x in rows]
    S=sum(success)
    gap=sum((sqrt(float(rows[2*b][y]))-sqrt(float(rows[2*b+1][y])))**2
            for b in range(2) for y in range(2))
    require(success==[F(13,100),F(13,100),F(1,4),F(1,4)], 'wrong success data')
    require(S==F(19,25), 'wrong total success')
    # Exact square roots here are 0.2, 0.3, 0.4. Hence 2*(.1)^2 per input pair.
    D01=F(1,50); D23=F(1,50)
    require(abs(gap - float(D01+D23)) < 1e-15, 'wrong Hellinger calculation')
    eps=(D01+D23)/(2*S)
    require(eps==F(1,38), 'wrong null boundary')
    wmax=1-eps
    require(wmax==F(37,38), 'wrong w maximum')
    w_older=1-D01/(2*S)
    require(w_older==F(75,76), 'wrong success-only w maximum')
    print('FOUR FULL OUTCOME LAWS: D01=1/50 D23=1/50 S=19/25')
    print(f'EXACT LOCAL WEIGHT MAXIMUM: w={wmax} (vs success-only {w_older})')

    # Construct CP trace-nonincreasing operation. K[e,output,input].
    # e=(first-input-bit, detector-outcome) ensures independent pair environments.
    K=np.zeros((4,4,4),dtype=complex)
    for i, row in enumerate(rows):
        b=i//2
        bit=i%2
        for y, weight in enumerate(row):
            K[2*b+y,2*y+bit,i]=sqrt(float(weight))
    effect=sum(k.conj().T @ k for k in K)
    require(np.max(np.abs(effect-np.diag(np.array(success,dtype=float))))<1e-14,
            'Kraus map does not have prescribed successes')
    require(np.linalg.eigvalsh(np.eye(4)-effect).min()>-1e-14,
            'Kraus map is not trace nonincreasing')
    for i, row in enumerate(rows):
        for y, weight in enumerate(row):
            observed=sum(np.linalg.norm(k[2*y:2*y+2,i])**2 for k in K)
            require(abs(observed-float(weight))<1e-14,
                    f'wrong probability for arm {i}, outcome {y}')
    # Sum of squared projections of all Kraus operators onto M_2 tensor I_2.
    w_from_kraus=sum(np.linalg.norm(k[::2,::2]+k[1::2,1::2])**2 for k in K)/(2*float(S))
    require(abs(w_from_kraus-float(wmax))<1e-14,'Kraus witness fails to attain bound')
    print('ATTAINMENT: explicit 4-Kraus CP-TNI branch, same first-output projective effect')

    # Exact dual scores, including unequal private randomization. In this example
    # the maximizing slopes are sqrt(r_odd/r_even) for each pair and outcome.
    slopes=[(F(2,3),F(3,2)),(F(3,4),F(4,3))]
    pi=(F(3,8),F(3,8),F(1,8),F(1,8))
    expect, d=score_expectation(rows,slopes,eps,pi)
    require(expect==0,'mean-zero boundary score not attained with unequal pi')
    eta=F(1,100)
    min_factor=min([F(1)] + [F(1)+eta*(d[i][y]-2*eps)/pi[i] for i in range(4) for y in range(2)])
    require(min_factor>0,'factor not nonnegative')
    print('ANYTIME NULL BOUNDARY: inverse-weighted mean score zero; all factors positive')

    # The marginal normalization used for a comparison based only on success rates.
    success_only_gap=(sqrt(float(success[2]))-sqrt(float(success[3])))**2
    extra=D23-F(0)
    require(abs(success_only_gap)<1e-15 and extra>0,'no gain from extra output?')
    print('INFORMATION GAIN: extra second-pair outcome discrepancy 1/50')

    # Shared-detector necessity: identity channel has w=1, but second-qubit
    # projective measurement distinguishes inputs 00 and 01 completely. It is
    # NOT a counterexample to first-qubit measurement theorem.
    K_id=np.eye(4,dtype=complex)
    w_id=(np.linalg.norm(K_id[::2,::2]+K_id[1::2,1::2])**2)/(2*4)
    require(abs(w_id-1)<1e-14,'identity channel local weight')
    outcomes0=(F(1),F(0));outcomes1=(F(0),F(1))
    D_bad=sum((sqrt(float(x))-sqrt(float(y)))**2 for x,y in zip(outcomes0,outcomes1))
    require(abs(D_bad-2)<1e-14,'wrong second-qubit diagnostic')
    print('SUBSYSTEM CONTROL: identity w=1, second-qubit readout discrepancy 2')
    print('ALL CHECKS PASSED')

if __name__=='__main__':
    main()
