#!/usr/bin/env python3
"""Exact-rational operational-gauge and two-copy quantum-channel verification.
"""
import json, hashlib, sys
from pathlib import Path
from math import comb
from fractions import Fraction
from sympy import (Matrix, eye, I as im, Rational as R, zeros,
                    kronecker_product as kp)

HERE=Path(__file__).parent

def verify(condition,label):
    if not condition:
        raise RuntimeError('failed verification: '+label)
I=eye(2);X=Matrix([[0,1],[1,0]]);Y=Matrix([[0,-im],[im,0]]);Z=Matrix([[1,0],[0,-1]])
paulis=[I,X,Y,Z]; basis=[kp(a,b) for a in paulis for b in paulis]
wts=[int(i>0)+int(j>0) for i in range(4) for j in range(4)]
CNOT=Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
lam=R(3,2); p=R(63,100)

def bloch_gauge(A, factor):
    return sum(((T*A).trace()*factor**wt*T/R(4) for T,wt in zip(basis,wts)), zeros(4))

def cnot_gauge(A):
    return bloch_gauge(CNOT*bloch_gauge(A,1/lam)*CNOT.T,lam)

def depolarized(A, mapped=False):
    G = cnot_gauge(A) if mapped else CNOT*A*CNOT.T
    return (1-p)*G+p*eye(4)*A.trace()/4

def choi(mapfn):
    C=zeros(16)
    for i in range(4):
        for j in range(4):
            Eij=zeros(4);Eij[i,j]=1
            C+=kp(Eij,mapfn(Eij))
    return C

Jbare=choi(cnot_gauge)
verify(Jbare.eigenvals()=={R(25,6):1,R(5,12):4,R(-5,12):4,R(0):6,R(-1,6):1},"source check 41")
Jprime=choi(lambda M: depolarized(M,True))
Joriginal=choi(lambda M: depolarized(M,False))
expected={R(1,300):4,R(63,400):6,R(187,600):4,R(2039,1200):1,R(23,240):1}
verify(Jprime.eigenvals()==expected,"source check 45")
verify(Joriginal.is_positive_definite and Jprime.is_positive_definite,"source check 46")
verify(Jprime.trace()==4 and Joriginal.trace()==4,"source check 47")
verify(choi(lambda A: (1-R(5,8))*cnot_gauge(A)+R(5,8)*eye(4)*A.trace()/4).is_positive_semidefinite,"source check 48")
verify(not choi(lambda A: (1-R(3,5))*cnot_gauge(A)+R(3,5)*eye(4)*A.trace()/4).is_positive_semidefinite,"source check 49")

rho_pure=kp((I+X)/2,(I+Z)/2)

def partial_transpose_second(A):
    out=zeros(4)
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    out[2*i+l,2*k+j]=A[2*i+j,2*k+l]
    return out

ppt_original=partial_transpose_second(depolarized(rho_pure,False)).eigenvals()
ppt_prime=partial_transpose_second(depolarized(rho_pure,True)).eigenvals()
verify(ppt_original=={R(137,400):3, -R(11,400):1},"source check 64")
verify(ppt_prime=={R(87,200):1,R(137,400):2,-R(3,25):1},"source check 65")

# Same *labeled* actually accessible product preparations give separable vs entangled outputs.
accessible_A=kp((I+R(1,2)*X)/2,(I+R(1,2)*Z)/2)
accessible_B=kp((I+R(3,4)*X)/2,(I+R(3,4)*Z)/2)
verify(bloch_gauge(accessible_A,lam)==accessible_B,"source check 70")
ppt_accessible_A=partial_transpose_second(depolarized(accessible_A,False)).eigenvals()
ppt_accessible_B=partial_transpose_second(depolarized(accessible_B,True)).eigenvals()
verify(min(ppt_accessible_A.keys())>=0,"source check 73")
verify(min(ppt_accessible_B.keys())==-R(13,1280),"source check 74")

# Verify all six by six local preparations and effects. Local gate physicality is by construction.
source_axes=[(P,sgn) for P in [X,Y,Z] for sgn in [1,-1]]
for P,s in source_axes:
  rho_A=(I+s*R(1,2)*P)/2
  rho_B=(I+s*R(3,4)*P)/2
  verify(rho_B==R(0)*I+rho_B,"source check 81")
  verify(rho_B==sum(((B*rho_A).trace()*R(3,2)**wt*B/2 for B,wt in zip(paulis,[0,1,1,1])),zeros(2)),"source check 82")

# General tensor gauge cancellation, using local Born effects at radius b_A=3/4 and b_B=1/2.
for Pa,sa in source_axes:
 for Pb,sb in source_axes:
  rhoA=kp((I+sa*R(1,2)*Pa)/2,(I+sb*R(1,2)*Pb)/2)
  rhoB=kp((I+sa*R(3,4)*Pa)/2,(I+sb*R(3,4)*Pb)/2)
  verify(bloch_gauge(rhoA,lam)==rhoB,"source check 89")
  OA=depolarized(rhoA,False);OB=depolarized(rhoB,True)
  verify(bloch_gauge(OA,lam)==OB,"source check 91")
  for Pc,sc in source_axes:
   for Pd,sd in source_axes:
    EA=kp((I+sc*R(3,4)*Pc)/2,(I+sd*R(3,4)*Pd)/2)
    EB=kp((I+sc*R(1,2)*Pc)/2,(I+sd*R(1,2)*Pd)/2)
    verify((EA*OA).trace()==(EB*OB).trace(),"source check 96")

# Calibrated joint-gate witness: cross-weight Pauli transfer; perfect CNOT not positive under nontrivial gauge.
XI=kp(X,I); XX=kp(X,X)
verify(cnot_gauge(XI)==lam*XX and cnot_gauge(XX)==XI/lam,"source check 100")

# Untrusted SWAP detector counterexample (model A projective, B biased)
SWAP=zeros(4)
for i in range(2):
 for j in range(2):SWAP[2*i+j,2*j+i]=1
EA=(eye(4)+SWAP)/2
EB=R(23,36)*eye(4)+R(2,9)*SWAP
verify(EA.is_positive_semidefinite and (eye(4)-EA).is_positive_semidefinite,"source check 108")
verify(EB.is_positive_semidefinite and (eye(4)-EB).is_positive_semidefinite,"source check 109")
for P,sp in source_axes:
 for Q,sq in source_axes:
  rhoA=kp((I+sp*R(1,2)*P)/2,(I+sq*R(1,2)*Q)/2)
  rhoB=kp((I+sp*R(3,4)*P)/2,(I+sq*R(3,4)*Q)/2)
  verify((EA*rhoA).trace()==(EB*rhoB).trace(),"source check 114")

verify(R(1,2)*(1+R(1,2)**2)==R(5,8),"source check 116")
verify(R(1,2)*(1+R(3,4)**2)==R(25,32),"source check 117")
verify((eye(4)*R(0) + EA).trace()==3,"source check 118")

# Statistical exact rational Bayes risk, computed via monotone binomial likelihood.
def binomial_bayes(n,p0,p1):
    p0=Fraction(p0.p,p0.q);p1=Fraction(p1.p,p1.q)
    return sum(min(Fraction(comb(n,k))*p0**k*(1-p0)**(n-k),
                   Fraction(comb(n,k))*p1**k*(1-p1)**(n-k)) for k in range(n+1))/2

def minimum_n(p0,p1,target=Fraction(1,10),upper=1500):
    for n in range(1,upper+1):
        if binomial_bayes(n,p0,p1)<=target:return n
    raise RuntimeError('no crossing')

p_swap_A=R(13,16);p_swap_B=R(57,64)
p_cnot_A=R(41,64);p_cnot_B=R(19,32)
n_swap=133; n_cnot=706
verify(binomial_bayes(n_swap-1,p_swap_A,p_swap_B)>Fraction(1,10),"source check 134")
verify(binomial_bayes(n_swap,p_swap_A,p_swap_B)<=Fraction(1,10),"source check 135")
verify(binomial_bayes(n_cnot-1,p_cnot_A,p_cnot_B)>Fraction(1,10),"source check 136")
verify(binomial_bayes(n_cnot,p_cnot_A,p_cnot_B)<=Fraction(1,10),"source check 137")

out={
  'date':'2026-11-07',
  'model':'qubit Bloch gauge lambda=3/2; noisy CNOT p=63/100',
  'untransformed_CNOT_choi_eigenvalues':{str(k):v for k,v in Jbare.eigenvals().items()},
  'transformed_noisy_CNOT_choi_eigenvalues':{str(k):v for k,v in Jprime.eigenvals().items()},
  'transformed_choi_min':str(min(Jprime.eigenvals().keys())),
  'CPTP_threshold_p':str(R(5,8)),
  'PPT_original':{str(k):v for k,v in ppt_original.items()},
  'PPT_transformed':{str(k):v for k,v in ppt_prime.items()},
  'PPT_accessible_A':{str(k):v for k,v in ppt_accessible_A.items()},
  'PPT_accessible_B':{str(k):v for k,v in ppt_accessible_B.items()},
  'single_copy_state_purity_A':str(R(5,8)),
  'single_copy_state_purity_B':str(R(25,32)),
  'trusted_SWAP_sym_A':str(p_swap_A),'trusted_SWAP_sym_B':str(p_swap_B),
  'trusted_CNOT_parity_A':str(p_cnot_A),'trusted_CNOT_parity_B':str(p_cnot_B),
  'minimum_2_copy_trials_trusted_SWAP':n_swap,
  'minimum_2_copy_trials_trusted_CNOT':n_cnot,
  'exact_product_input_output_comparisons':36*36,
  'uncalibrated_SWAP_equalities':36,
}
text=json.dumps(out,indent=2,sort_keys=True)+'\n'
(HERE/'exact_results.json').write_text(text)
print(text)
