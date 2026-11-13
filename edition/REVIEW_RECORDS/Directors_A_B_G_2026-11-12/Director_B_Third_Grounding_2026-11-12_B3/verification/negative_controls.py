#!/usr/bin/env python3
"""Concretely computed expected-failure controls; no source mutation."""
from pathlib import Path
import json
import sympy as s
R=Path(__file__).resolve().parent
kr=s.kronecker_product
basis0=s.Matrix([1,0]);basis1=s.Matrix([0,1]);I=s.eye(2)
X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1)
psi=(kr(basis0,basis1)+kr(basis1,basis0))/s.sqrt(2)
Ppsi=s.simplify(psi*psi.conjugate().T)
p00=kr(basis0,basis0);P00=p00*p00.T
P4=s.zeros(4);P5=s.zeros(5)
for n,P in [(4,P4),(5,P5)]:
 for j in range(n):P[(j+1)%n,j]=1
C4=P4-P4.T;C5=P5-P5.T
Q4=s.eye(4)-s.ones(4)/4
F=s.diag(s.Rational(1,2),1)
G=s.diag(s.sqrt(3)/2,0)
K0=kr(F,F);K1=kr(G,I);K2=kr(F,G)
initial=s.Rational(1,2)*(P00+Ppsi)
unnormalized=K0*initial*K0
post=s.simplify(unnormalized/s.trace(unnormalized))
P_bad=(kr(I,I)+kr(X,X)-kr(Y,Y)-kr(Z,Z))/4
r0=K0*P00*K0
r0=s.simplify(r0/s.trace(r0))
checks={
 'false_even_cycle_contrast_full_rank_rejected':C4.rank()==2,
 'false_n4_three_cycle_identity_rejected':C4*C4!=-3*Q4,
 'false_all_odd_cycles_scalar_square_rejected':C5*C5 != -3*(s.eye(5)-s.ones(5)/5),
 'false_t0_local_filter_creates_Bell_state_rejected':r0==P00 and s.trace(Ppsi*r0)==0,
 'false_success_branch_is_deterministic_rejected':K0.T*K0!=s.eye(4),
 'correct_trace_preserving_local_completion':K0.T*K0+K1.T*K1+K2.T*K2==s.eye(4),
 'wrong_local_Pauli_Y_sign_rejected':P_bad!=Ppsi,
 'false_filtered_half_state_inside_K_rejected':s.simplify(s.trace(Ppsi*post))==s.Rational(4,5) and s.Rational(4,5)>s.Rational(3,4),
}
checks={k:bool(v) for k,v in checks.items()}
assert all(checks.values())
(R/'NEGATIVE_CONTROL_RESULTS.json').write_text(json.dumps({'status':'PASS_EXPECTED_FAILURE_CONTROLS','controls':checks,'pass_count':len(checks),'scope':'algebraic mutation controls, one reviewer, no external independent review'},indent=2,sort_keys=True)+'\n')
print('PASS_B3_NEGATIVE_CONTROLS',len(checks))
