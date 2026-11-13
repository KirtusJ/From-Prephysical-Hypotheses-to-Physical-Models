#!/usr/bin/env python3
"""Director G independent exact/numerical checks for a two-qubit composite family.

All systems and operational effects here are stipulated as *mathematical controls*.
No prephysical structure, quantum mechanics, or classical mechanics is derived.
Source A/B codes are NOT imported. Run with python3 verify_composite_selection.py.
"""
from __future__ import annotations
from fractions import Fraction
import json, math
from pathlib import Path
import numpy as np
import sympy as sp

TOL=2e-12
I2=np.eye(2,dtype=complex)
Z=np.diag([1.,-1.]).astype(complex)
X=np.array([[0.,1.],[1.,0.]],complex)
Y=np.array([[0.,-1.j],[1.j,0.]],complex)
ket0=np.array([1.,0.],complex)
ket1=np.array([0.,1.],complex)
ketplus=(ket0+ket1)/math.sqrt(2)
keti=(ket0+1j*ket1)/math.sqrt(2)
project=lambda v: np.outer(v,v.conj())
phi=(np.kron(ket0,ket0)+np.kron(ket1,ket1))/math.sqrt(2)
P=project(phi)
sigma=project(np.kron(ket0,ket0))
assert abs(np.trace(sigma@P).real-.5)<TOL
assert abs(np.trace(P@P).real-1)<TOL

# Local tomography: 16 product states are a basis for Hermitian 4x4 matrices.
pauli=[I2,X,Y,Z]
local_probes=[project(ket0),project(ket1),project(ketplus),project(keti)]
two_probes=[np.kron(a,b) for a in local_probes for b in local_probes]
two_pauli=[np.kron(a,b) for a in pauli for b in pauli]
span=np.array([[np.trace(p@q).real/4 for q in two_pauli] for p in two_probes])
assert np.linalg.matrix_rank(span,tol=1e-11)==16

# CNOT in control-first convention.
CNOT=np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],complex)
assert np.linalg.norm(CNOT.conj().T@CNOT-np.eye(4))<TOL
assert np.linalg.norm(CNOT@np.kron(ketplus,ket0)-phi)<TOL

A0,A1=Z,X
B0=(Z+X)/math.sqrt(2)
B1=(Z-X)/math.sqrt(2)
CHSH=np.kron(A0,B0+B1)+np.kron(A1,B0-B1)
assert abs(np.trace(CHSH@P).real-2*math.sqrt(2))<TOL
assert abs(np.trace(CHSH@sigma).real-math.sqrt(2))<TOL

# Four-party witness E = I - (I-P_12) \otimes (I-P_34).
I4=np.eye(4,dtype=complex)
E=np.eye(16,dtype=complex)-np.kron(I4-P,I4-P)
assert np.linalg.norm(E@E-E)<TOL
assert abs(np.linalg.eigvalsh(E).min())<TOL
assert abs(np.linalg.eigvalsh(E).max()-1)<TOL

# Independent construction of each state and the 4-party witness.
trials=[]
for j in range(101):
 t=j/100
 rho=(1-t)*sigma+t*P
 assert abs(np.trace(rho).real-1)<TOL
 assert np.linalg.eigvalsh(rho).min()>-TOL
 fidelity=float(np.trace(P@rho).real)
 # exact sup of Bell effect over K_t = (1+t)/2 (proved in report)
 expected_fidelity=(1+t)/2
 assert abs(fidelity-expected_fidelity)<TOL
 double=np.kron(rho,rho)
 acceptance=float(np.trace(E@double).real)
 predicted_acceptance=1-(1-t)**2/4
 assert abs(acceptance-predicted_acceptance)<TOL
 # Any rho in naive K_t^(4) = (1-t) Sep_4 + t Q_4 must obey E <= 3/4+t/4.
 naive_bound=.75+t/4
 gap=acceptance-naive_bound
 predicted_gap=t*(1-t)/4
 assert abs(gap-predicted_gap)<TOL
 if j not in (0,100): assert gap>0
 chsh=float(np.trace(CHSH@rho).real)
 assert abs(chsh-math.sqrt(2)*(1+t))<TOL
 pt=rho.reshape(2,2,2,2).transpose(0,3,2,1).reshape(4,4)
 pt_min=float(np.linalg.eigvalsh(pt).min())
 assert abs(pt_min + t/2)<TOL
 trials.append({'t':t,'Bell_effect_acceptance':fidelity,'CHSH_fixed_settings':chsh,
                'partial_transpose_min_eigenvalue':pt_min,'four_party_E_acceptance':acceptance,'naive_family_E_upper_bound':naive_bound,
                'naive_family_violation':gap})

# Symbolic algebra (independent from the floating point comparisons).
t=sp.symbols('t',real=True)
F=sp.simplify((1-t)*sp.Rational(1,2)+t)
p4=sp.simplify(1-(1-F)**2)
B4=sp.Rational(3,4)+t/4
gap_symbolic=sp.factor(p4-B4)
assert sp.simplify(gap_symbolic-t*(1-t)/4)==0
assert sp.factor(F-(1+t)/2)==0
assert sp.simplify(gap_symbolic.subs(t,sp.Rational(1,2)))==sp.Rational(1,16)

# Every two-qubit pure state is reachable with local unitaries and one CNOT.
# Schmidt factorization: M = U diag(s) Vh, vectorization convention columns.
rng=np.random.default_rng(20261112)
errors=[]
for _ in range(200):
 psi=rng.normal(size=4)+1j*rng.normal(size=4)
 psi/=np.linalg.norm(psi)
 U,s,Vh=np.linalg.svd(psi.reshape(2,2))
 # [s0, s1] is prepared from |0>; CNOT then creates Schmidt vector.
 R=np.array([[s[0],-s[1]],[s[1],s[0]]],complex)
 V=Vh.T
 result=np.kron(U,V)@CNOT@np.kron(R@ket0,ket0)
 err=float(np.linalg.norm(result-psi))
 errors.append(err)
 assert err < 1e-12

# Negative control: the non-closed naive family would require gap<=0 at t=1/2.
invalid_closure_claim_detected=trials[50]['naive_family_violation']>0.06
assert invalid_closure_claim_detected

report={
 'research_stage':'Initial External Grounding / G1 OPEN',
 'ontology_selected':False,
 'evidence_level':'Conditional mathematical construction and reproducible calculations, no experimental emergence',
 'mathematical_claims':{
    'two_party_family':'K_t=(1-t)Sep_2 + t Quantum_2, t in [0,1]',
    'Bell_effect_supremum_over_K_t':'(1+t)/2',
    'uniform_naive_extension':'K_t^(4)=(1-t)Sep_4 + t Quantum_4',
    'four_party_witness_E':'I_16-(I_4-P_Bell)_12 tensor (I_4-P_Bell)_34',
    'four_party_E_upper_bound_for_naive_extension':'3/4 + t/4',
    'four_party_counterexample_E_value':'1-(1-t)^2/4',
    'strict_violation_for_0<t<1':'t(1-t)/4',
    'fixed_settings_CHSH_of_extremal_rho_t':'sqrt(2)*(1+t), exceeds 2 iff t>sqrt(2)-1',
    'partial_transpose_min_eigenvalue_of_extremal_rho_t':'-t/2',
    'conditional_CNOT_selection':'All single-qubit pure states + local unitaries + CNOT + convex mixing + state subset of Quantum_2 imply Quantum_2'},
 'checks':{
     'local_tomographic_product_probe_span':int(np.linalg.matrix_rank(span)),
     'max_schmidt_CNOT_construction_error':max(errors),
     'num_random_pure_targets':len(errors),
     'num_retained_parameter_cases':len(trials),
     'num_positive_gap_cases':sum(r['naive_family_violation']>1e-12 for r in trials),
     't_half_exact_gap':'1/16',
     'CHSH_violation_threshold':math.sqrt(2)-1,
     'sympy_gap_factorization':str(gap_symbolic),
     'max_gap':max(trials,key=lambda a:a['naive_family_violation']),
     'invalid_closure_claim_detected':invalid_closure_claim_detected,
 },
 'retained_trials':trials,
 'limitations':[
    'Pairwise K_t is a finite-dimensional operational toy family, not a prephysical substrate.',
    'The uniform multipartite K_t extension is disproved; valid multipartite extension needs separate justification.',
    'The CNOT reconstruction imports a complex quantum operator state representation and a specified gate.',
    'No quantum-to-classical limit, empirical map, calibrated time or space was produced.',
    'Reproducing scripts are single-actor calculations, not independent agents or experimental replication.'
 ]
}
out=Path(__file__).with_name('composition_results.json')
out.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
print('PASS_DIRECTOR_G_COMPOSITE_SELECTION')
print('all',len(trials),'parameter samples retained, exact gap t(1-t)/4')
print('t=0.5 4-party violation', trials[50]['naive_family_violation'])
print('single-system tomography span',report['checks']['local_tomographic_product_probe_span'])
print('one CNOT Schmidt synthesis max error',max(errors))
print('JSON',out)
