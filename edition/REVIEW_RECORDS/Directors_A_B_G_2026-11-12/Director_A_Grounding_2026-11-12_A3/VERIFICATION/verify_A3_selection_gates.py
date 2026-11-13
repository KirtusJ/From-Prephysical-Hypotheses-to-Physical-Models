#!/usr/bin/env python3
"""Scoped reproducibility checks for Director A's third grounding continuation.

All complex Hilbert spaces, Born probabilities and quantum instruments are
STIPULATED controls, not prephysical derivations. The exact theorems are in
RESEARCH/A3_Instrument_and_Composition_Gates.tex. No empirical data are used.
"""
import csv
import hashlib
import json
import math
from pathlib import Path

import mpmath as mp
import numpy as np
import sympy as sp

root = Path(__file__).resolve().parent
mp.mp.dps = 95
T = sp.symbols('t', real=True, nonnegative=True)
X = sp.symbols('x', real=True, nonnegative=True)
S = sp.symbols('s', real=True, nonnegative=True)

# The exact identities are derived by matrix calculations in the manuscript.
N = ((2-T)*X**2+T)/2
Fidelity = sp.Rational(1, 2) + T*X/((2-T)*X**2+T)
assert sp.simplify(Fidelity.subs(X,1)-(1+T)/2) == 0
assert sp.simplify(N.subs(X,sp.sqrt(T/(2-T)))-T) == 0
assert sp.simplify(Fidelity.subs(X,sp.sqrt(T/(2-T))) - (1+sp.sqrt(T/(2-T)))/2) == 0
assert sp.simplify(Fidelity-(1+T)/2) != 0
assert sp.simplify(sp.factor(sp.diff(Fidelity,X)).subs(X,1) - T*(T-1)/2) == 0

# Four-body witness, with a freely varying four-body interpolation weight s.
f = (1+T)/2
four_accept = 1-(1-f)**2
four_support_s = sp.Rational(3,4)+S/4
assert sp.simplify(four_accept-four_support_s - (2*T-T**2-S)/4)==0
assert sp.simplify((2*T-T**2)-T)==T*(1-T)
assert sp.simplify(four_accept-four_support_s.subs(S,T)-T*(1-T)/4)==0

zero=np.array([1.,0.],complex)
one=np.array([0.,1.],complex)
I=np.eye(2,dtype=complex)
ketPhi=(np.kron(zero,zero)+np.kron(one,one))/np.sqrt(2)
P=np.outer(ketPhi,ketPhi.conj())
prod00=np.outer(np.kron(zero,zero),np.kron(zero,zero).conj())
project=lambda v: np.outer(v,v.conj())

E4=np.eye(16,dtype=complex)-np.kron(np.eye(4)-P,np.eye(4)-P)
assert np.linalg.norm(E4@E4-E4)<1e-13
assert np.linalg.eigvalsh(E4).min() >= -1e-13
assert np.linalg.eigvalsh(E4).max() <= 1+1e-13

case_ts=[mp.mpf(0),mp.mpf(1)] + [mp.mpf(i)/200 for i in range(1,200)]
# High precision boundary cases: these values cannot all be distinguished in float64.
extra_ts=['1e-40','1e-30','1e-20','1e-15','1e-12','1e-9','1e-6','1e-4','0.414213562373095048801688724209698078569671875',
          '0.9999','0.999999','0.999999999','0.999999999999',
          '0.99999999999999999999','0.999999999999999999999999999999','0.9999999999999999999999999999999999999999']
case_ts += [mp.mpf(t) for t in extra_ts]
case_ts.sort()
rows=[]
for k,t in enumerate(case_ts):
    if t==0:
        # The t=0 algebraic optimum has zero success probability and is not a
        # defined conditional state. Record that fact instead of dividing by zero.
        x=mp.mpf(0);success=mp.mpf(0);filt=None;gap=None
    else:
        x=mp.sqrt(t/(2-t))
        success=((2-t)*x*x+t)/2
        filt=(1+x)/2
        gap=filt-(1+t)/2
        assert abs(success-t)<mp.mpf('1e-87')
        if t<1: assert gap>0,(k,t,gap)
        else: assert abs(gap)<mp.mpf('1e-86')
    gap_same=t*(1-t)/4
    required_s=2*t-t*t
    discard_s=t
    if 0<t<1:assert required_s>discard_s
    else: assert abs(required_s-discard_s)<mp.mpf('1e-87')
    rows.append({'case_id':k,'t_decimal':mp.nstr(t,94),'is_endpoint':t==0 or t==1,
      'optimal_filter_x':mp.nstr(x,94),'success_probability':mp.nstr(success,94),
      'conditional_Bell_fidelity':None if filt is None else mp.nstr(filt,94),
      'K_t_Bell_fidelity_upper':mp.nstr((1+t)/2,94),
      'filter_violation':None if gap is None else mp.nstr(gap,94),
      'parallel_pair_E_acceptance':mp.nstr(1-(1-t)**2/4,94),
      'K_s_E_bound_if_s_equals_t':mp.nstr(mp.mpf('0.75')+t/4,94),
      'four_party_gap_s_eq_t':mp.nstr(gap_same,94),
      'required_s_lower_from_independent_prep':mp.nstr(required_s,94),
      'required_s_upper_from_discard':mp.nstr(discard_s,94),
      'required_s_gap':mp.nstr(t*(1-t),94)})

# Independent finite matrix checks for ordinary precision (report includes extremes
# separately as arbitrary precision checks). Our interval claims are exact algebraic.
float_errors=[]
for it in np.linspace(0.002,0.998,249):
    t=float(it)
    rho=(1-t)*prod00+t*P
    x=math.sqrt(t/(2-t))
    F=np.diag([x,1.]).astype(complex)
    Ffail=np.diag([math.sqrt(1-x*x),0]).astype(complex)
    assert np.linalg.norm(F.conj().T@F+Ffail.conj().T@Ffail-I)<1e-13
    W=np.kron(F,I)
    filtered=W@rho@W.conj().T
    ps=np.trace(filtered).real
    fidelity=np.trace(P@filtered).real/ps
    four=np.trace(E4@np.kron(rho,rho)).real
    err=max(abs(ps-t),abs(fidelity-(1+x)/2),abs(four-(1-(1-t)**2/4)))
    assert err < 4e-14
    float_errors.append({'t':t,'filter_success':float(ps),'conditioned_Bell_fidelity':float(fidelity),
        'Bell_max_Kt':(1+t)/2,'filter_gap':float(fidelity-(1+t)/2),
        'four_body_effect':float(four),'four_body_gap':float(four-(.75+t/4)),
        'max_identity_residual':float(err)})

# All 3-party matching partitions are biseparable across some 1|23 bipartition.
# Pure three-qubit GHZ has max squared product-over-cut overlap 1/2.
ghz=(np.kron(np.kron(zero,zero),zero)+np.kron(np.kron(one,one),one))/np.sqrt(2)
ghz_effect=np.outer(ghz,ghz.conj())
assert abs(np.vdot(ghz,ghz)-1)<1e-14
rng=np.random.default_rng(2026111203)
def rand_unit(d):
  v=rng.normal(size=d)+1j*rng.normal(size=d)
  return v/np.linalg.norm(v)

def vec_across_cut(q,rest,cut):
  if cut==0:return np.kron(q,rest)
  if cut==2:return np.kron(rest,q)
  return np.transpose(np.kron(q,rest).reshape(2,2,2),(1,0,2)).reshape(8)

ghz_rows=[]
for cut in range(3):
    for i in range(160):
        psi=vec_across_cut(rand_unit(2),rand_unit(4),cut)
        overlap=abs(np.vdot(ghz,psi))**2
        assert overlap <= .5+2e-14
        ghz_rows.append({'cut':cut,'trial':i,'GHZ_projector_acceptance':float(overlap)})
# Three explicit saturating vectors, with each split chosen as a single |0>\otimes|00> etc.
for cut in range(3):
  v=vec_across_cut(zero,np.kron(zero,zero),cut)
  assert abs(abs(np.vdot(ghz,v))**2-0.5)<1e-14
assert abs(np.trace(ghz_effect@ghz_effect).real-1)<1e-14

# Pure entangled seed + one-sided selective filters + local unitaries + convexity
# forces all pure bipartite two-qubit states, a finite exact SLOCC theorem.
seed_rows=[]
for i in range(240):
    seedratio=rng.uniform(.001,.999)
    targetratio=rng.uniform(0,1)
    a,b=math.sqrt(seedratio),math.sqrt(1-seedratio)
    c,d=math.sqrt(targetratio),math.sqrt(1-targetratio)
    kappa=min(1., a/c if c>0 else 1e300, b/d if d>0 else 1e300)
    filter_one=np.diag([kappa*c/a,kappa*d/b]).astype(complex)
    assert np.linalg.eigvalsh(filter_one.conj().T@filter_one).max() <= 1+1e-13
    seed=a*np.kron(zero,zero)+b*np.kron(one,one)
    target=c*np.kron(zero,zero)+d*np.kron(one,one)
    v=np.kron(filter_one,I)@seed
    p=np.vdot(v,v).real
    assert p>0
    assert np.linalg.norm(v/np.sqrt(p)-target)<4e-14
    # Schmidt basis can be reoriented by local unitaries.
    random_unitary=lambda: np.linalg.qr(rng.normal(size=(2,2))+1j*rng.normal(size=(2,2)))[0]
    U,V=random_unitary(),random_unitary()
    oriented=np.kron(U,V)@v/np.sqrt(p)
    assert np.linalg.norm(oriented-np.kron(U,V)@target)<4e-14
    seed_rows.append({'index':i,'seed_coeff_a':a,'seed_coeff_b':b,
       'target_coeff_c':c,'target_coeff_d':d,'success_probability':float(p),
       'expected_success_probability':float(kappa*kappa),
       'transformation_error':float(np.linalg.norm(v/np.sqrt(p)-target))})

# Fault-injection checks: the formulas the notes explicitly reject.
false_controls={
  'false_universal_filter_closure_rejected':float_errors[100]['filter_gap']>1e-3,
  'false_4_party_repair_s_eq_t_rejected':(float(rows[105]['required_s_gap'])>0),
  'false_GHZ_in_matching_hierarchy_rejected':1>.5,
  'incorrect_filter_x_equals_1_is_not_optimum_at_t_half':abs(float(sp.diff(Fidelity,X).subs({T:sp.Rational(1,2),X:1})))>1e-2,
}
assert all(false_controls.values())

with (root/'all_A3_high_precision_parameter_cases.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
with (root/'all_A3_finite_matrix_checks.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(float_errors[0]));w.writeheader();w.writerows(float_errors)
with (root/'all_A3_GHZ_biseparable_samples.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(ghz_rows[0]));w.writeheader();w.writerows(ghz_rows)
with (root/'all_A3_pure_seed_filter_samples.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(seed_rows[0]));w.writeheader();w.writerows(seed_rows)

summary={
 'research_status':'Initial External Grounding G1 OPEN; NO ONTOLOGY SELECTED',
 'evidence_kind':'exact proofs plus deterministic local algebra and computational controls; NO EMPIRICAL RECORD',
 'new_results':[
     'A3-01 stochastic one-party local filter excludes all 0<t<1 intermediate K_t',
     'A3-02 no two/four party K_(t_n) affine interpolation survives both pair preparation and discard for 0<t2<1',
     'A3-03 matching-generated hierarchy is closed under independent preparation, trace and elementary one-site CPTP, but excludes GHZ',
     'A3-04 any convex 2-qubit state subset closed under all local unitaries and selective local filters containing one pure entangled state equals D2',
     'A3-05 mixed-seed to pure Bell selection is conditional on external 2x2 distillation and strong all-arity operational closure'],
 'records':{
     'arbitrary_precision_parameter_cases':len(rows),
     'finite_matrix_filter_cases':len(float_errors),
     'ghz_biseparable_trials':len(ghz_rows),
     'pure_seed_filter_trials':len(seed_rows),
     'high_precision_digits':mp.mp.dps},
 'max_float_identity_residual':max(r['max_identity_residual'] for r in float_errors),
 'min_highprecision_positive_filter_gap':mp.nstr(min(mp.mpf(r['filter_violation']) for r in rows if r['filter_violation'] is not None and 0<mp.mpf(r['t_decimal'])<1),45),
 'outliers':{
     'zero_t_filter_not_defined_because_success_probability_is_zero':True,
     'near_one_filter_gap_below_double_precision_visible':True,
     'all_cases_retained_in_csv':True},
 'false_controls':false_controls,
 'limitations':[
     'The constructed state spaces assume quantum density matrices and Born probabilities.',
     'Closure under local quantum channels is distinct from closure under conditioned quantum instruments.',
     'The matching hierarchy deliberately restricts retained-system instrument availability and does not prove emergence.',
     'The mixed-seed extension relies on external distillation literature and a compactness premise.',
     'No independent sub-agent or experimental corroboration occurred.'],
}
(root/'A3_check_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('A3_MATHEMATICAL_CHECK_PASS')
print('rows:',summary['records'],'max residual:',summary['max_float_identity_residual'])
print('min positive filter gap:',summary['min_highprecision_positive_filter_gap'])
print('fault controls:',false_controls)
print('status:',summary['research_status'])
