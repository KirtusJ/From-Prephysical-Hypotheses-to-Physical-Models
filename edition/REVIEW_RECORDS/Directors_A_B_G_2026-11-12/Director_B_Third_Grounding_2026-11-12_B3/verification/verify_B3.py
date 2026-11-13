#!/usr/bin/env python3
"""Director B B3: independent symbolic + numerical control checks.

All quantum two-level systems below are STIPULATED mathematical systems, not derived
physical qubits. No inference about nature, PCP efficacy, or physical ontology.
"""
from pathlib import Path
from fractions import Fraction
import csv, json, math, hashlib
import numpy as np
import sympy as sp
from mpmath import mp

OUT=Path(__file__).resolve().parent
sp_t, sp_x = sp.symbols('t x', real=True)
A=sp.eye(2)
zero=sp.Matrix([1,0]); one=sp.Matrix([0,1]); I=sp.I
K = sp.kronecker_product
proj=lambda v: v*v.conjugate().T
psi=(K(zero,one)+K(one,zero))/sp.sqrt(2)
Ppsi=sp.simplify(proj(psi)); P00=proj(K(zero,zero))
rho=(1-sp_t)*P00+sp_t*Ppsi
assert sp.simplify(sp.trace(rho)-1)==0
F=sp.diag(sp.sqrt(sp_x),1)
F2=K(F,F)
unnormalized=sp.simplify(F2*rho*F2)
success=sp.factor(sp.trace(unnormalized))
assert sp.simplify(success - sp_x*(sp_t+(1-sp_t)*sp_x))==0
rhoprime=sp.simplify(unnormalized/success)
post_bell_fidelity=sp.simplify(sp.trace(Ppsi*rhoprime))
assert sp.simplify(post_bell_fidelity - sp_t/(sp_t+(1-sp_t)*sp_x))==0
witness_gap=sp.factor(post_bell_fidelity-(1+sp_t)/2)
assert sp.factor(witness_gap - (1-sp_t)*(sp_t-(1+sp_t)*sp_x)/(2*(sp_t+(1-sp_t)*sp_x)))==0
x_half=sp_t/(2*(1+sp_t))
assert sp.simplify(witness_gap.subs(sp_x,x_half) -(1-sp_t**2)/(2*(3+sp_t)))==0
assert sp.simplify(success.subs(sp_x,x_half)-sp_t**2*(3+sp_t)/(4*(1+sp_t)**2))==0

# The separating operator is reconstructible from *product Pauli measurements*.
X=sp.Matrix([[0,1],[1,0]]);Y=sp.Matrix([[0,-sp.I],[sp.I,0]]);Z=sp.diag(1,-1)
assert sp.simplify((K(A,A)+K(X,X)+K(Y,Y)-K(Z,Z))/4-Ppsi)==sp.zeros(4)

# Exact finite counterexample t=1/2, epsilon=1/2, x=epsilon^2=1/4.
sub={sp_t:sp.Rational(1,2),sp_x:sp.Rational(1,4)}
initial=sp.simplify(rho.subs(sub))
post=sp.simplify(rhoprime.subs(sub))
assert sp.simplify(success.subs(sub))==sp.Rational(5,32)
assert sp.simplify(post_bell_fidelity.subs(sub))==sp.Rational(4,5)
assert sp.simplify(witness_gap.subs(sub))==sp.Rational(1,20)
assert post == sp.Rational(1,5)*P00+sp.Rational(4,5)*Ppsi
assert sp.simplify(sp.trace(K(X,X)*post))==sp.Rational(4,5)
assert sp.simplify(sp.trace(K(Y,Y)*post))==sp.Rational(4,5)
assert sp.simplify(sp.trace(K(Z,Z)*post))==-sp.Rational(3,5)

# Physical local Kraus completion when F=diag(eps,1), each branch is product Kraus.
# C0=F\otimes F; C1=G\otimes I; C2=F\otimes G, G=sqrt(I-F^2)
G=sp.diag(sp.sqrt(1-sp_x),0)
K0=K(F,F);K1=K(G,A);K2=K(F,G)
assert sp.simplify(K0.T*K0+K1.T*K1+K2.T*K2-sp.eye(4))==sp.zeros(4)

# Source-independent G four-system witness and convex support bound, symbolic.
Phi=(K(zero,zero)+K(one,one))/sp.sqrt(2)
PPhi=sp.simplify(proj(Phi));
rho_g=(1-sp_t)*P00+sp_t*PPhi
fg=sp.simplify(sp.trace(PPhi*rho_g))
assert sp.simplify(fg-(1+sp_t)/2)==0
assert sp.simplify(1-(1-fg)**2-(sp.Rational(3,4)+sp_t/4) - sp_t*(1-sp_t)/4)==0

# Continuity/closure theorem: filtered states approach Ppsi for t>0.
assert sp.Matrix(4,4,lambda i,j: sp.simplify(sp.limit(rhoprime[i,j],sp_x,0,dir='+')-Ppsi[i,j]))==sp.zeros(4)
# After obtaining Ppsi, a local unitary I \otimes X transforms it to PPhi.
assert K(A,X)*Ppsi*K(A,X).T==PPhi
# A local diagonal filter on PPhi prepares arbitrary Schmidt vector with nonzero success:
a,b=sp.symbols('a b',nonnegative=True,real=True)
H=sp.diag(a,b);tmp=K(H,A)*PPhi*K(H,A)
assert sp.simplify(tmp*2 - proj(a*K(zero,zero)+b*K(one,one)))==sp.zeros(4)

# Exact extreme-parameter trials; preserve endpoints with status rather than drop.
fractions=[Fraction(k,100) for k in range(101)]
fractions += [Fraction(1,10**k) for k in range(1,51)]
fractions += [Fraction(10**k-1,10**k) for k in range(1,51)]
fractions += [Fraction(1,2**k) for k in range(1,31)]
fractions += [Fraction(2**k-1,2**k) for k in range(1,31)]
# retain duplicate preparations as independent probes and label each record
mp.dps=90
r=[]
for j,t in enumerate(fractions):
 if t==0:
  r.append(dict(trial=j,t=str(t),x='N/A',success='N/A',bell_fidelity='N/A',K_bound=str(Fraction(1,2)),gap='N/A',status='ENDPOINT_NO_SUCCESS_FOR_CHOSEN_X'))
  continue
 x=t/(2*(1+t))
 p=x*(t+(1-t)*x)
 q=t/(t+(1-t)*x)
 bound=(1+t)/2
 gap=q-bound
 if not (p>0 and 0<x<1):raise AssertionError((j,t,p,x))
 if t<1 and not gap>0:raise AssertionError((j,t,gap))
 if t==1 and gap!=0:raise AssertionError((j,t,gap))
 expected=(1-t*t)/(2*(3+t))
 assert gap==expected
 r.append(dict(trial=j,t=str(t),x=str(x),success=str(p),bell_fidelity=str(q),K_bound=str(bound),gap=str(gap),status='STRICT_FILTER_ESCAPE' if t<1 else 'ENDPOINT_FULL_QUANTUM'))
# Independently reconstruct one full example using numerical 4x4 matrices.
ket_0=np.array([1.,0],complex);ket_1=np.array([0.,1],complex)
psi_np=(np.kron(ket_0,ket_1)+np.kron(ket_1,ket_0))/np.sqrt(2)
Pr=np.outer(psi_np,psi_np.conj()); rr=.5*np.outer(np.kron(ket_0,ket_0),np.kron(ket_0,ket_0).conj())+.5*Pr
kf=np.kron(np.diag([.5,1.]),np.diag([.5,1.]))
tr=np.trace(kf@rr@kf).real
rr2=(kf@rr@kf)/tr
assert abs(tr-.15625)<1e-14
assert abs(np.trace(Pr@rr2).real-.8)<1e-14

# Cycle family: keep all n, including even/degenerate exceptions.
cycle=[]
for n in range(3,32):
 P=sp.zeros(n)
 for j in range(n):P[(j+1)%n,j]=1
 C=P-P.T
 Q=sp.eye(n)-sp.ones(n)/n
 R=sp.zeros(n)
 for j in range(n):R[(-j)%n,j]=1
 assert P**n==sp.eye(n)
 assert R*P*R.T==P.T
 assert R*C*R.T==-C
 rank=C.rank()
 assert rank==(n-1 if n%2 else n-2)
 if n==3: assert C**2==-3*Q
 if n%2:
  Cf=np.asarray(C,float)
  M=-Cf@Cf
  w,V=np.linalg.eigh(M)
  # remove exactly one constant mode by eigenvalue near zero
  mask=w>1.e-10
  assert np.count_nonzero(mask)==n-1
  Minvhalf=(V[:,mask]/np.sqrt(w[mask]))@V[:,mask].T
  J=Cf@Minvhalf
  Qf=np.asarray(Q,float)
  residual=float(np.linalg.norm(J@J+Qf,ord='fro'))
  assert residual < 1.e-9
  # any odd n>3 must have >=2 distinct nonzero sin^2
  svals=np.unique(np.round(np.abs(np.linalg.eigvals(Cf)),12))
  if n>3:assert len(svals)>2, (n,svals)
  cycle.append({'n':n,'parity':'odd','rank_C':rank,'contrast_dim':n-1,'symplectic_nondegenerate':True,'max_j2_fro_residual':residual,'note':'derived real J imports counting metric and positive square root'})
 else:
  cycle.append({'n':n,'parity':'even','rank_C':rank,'contrast_dim':n-1,'symplectic_nondegenerate':False,'max_j2_fro_residual':'N/A','note':'contrast kernel contains alternating vector'})

with (OUT/'ALL_FILTER_TRIALS.csv').open('w',newline='') as f:
 wr=csv.DictWriter(f,fieldnames=r[0].keys());wr.writeheader();wr.writerows(r)
with (OUT/'ALL_CYCLE_TRIALS.csv').open('w',newline='') as f:
 wr=csv.DictWriter(f,fieldnames=cycle[0].keys());wr.writeheader();wr.writerows(cycle)
report={
 'research_stage':'Initial External Grounding / G1 OPEN', 'ontology_selected':False,
 'scope':'exact mathematical counterexample conditional on stipulated complex two-level systems and allowed postselected local filters',
 'exact_half_example': {'t':'1/2','epsilon':'1/2','postselection_success':'5/32','post_bell_fidelity':'4/5','K_t_max_bell_fidelity':'3/4','strict_gap':'1/20','XX':'4/5','YY':'4/5','ZZ':'-3/5'},
 'exact_formulas':{'p_success':'x*(t+(1-t)*x)','post_bell_fidelity':'t/(t+(1-t)*x)','max_Bell_fidelity_in_K_t':'(1+t)/2','violation_condition':'0<t<1 and 0<x<t/(1+t)','uniform_choice':'x=t/[2(1+t)]','uniform_violation':'(1-t^2)/[2(3+t)]','uniform_success':'t^2*(3+t)/[4*(1+t)^2]'},
 'under_test_assumptions':['K_t=(1-t)Sep_2+tD_2','exact conventional two-qubit quantum Hilbert representation supplied','all local single-site non-deterministic filters and classical postselection available','full set of local unitaries available','finite-dimensional state sets norm-closed for saturation theorem','convex mixing available'],
 'results':{'K_t_not_filter_closed_all_interior_t':True,'local_product_pauli_measurements_suffice_to_detect_violation':True,'filter_trace_preserving_completion_exists':True,'closed_filter_saturation_to_D2_for_any_t_positive':True,'odd_directed_cycle_contrast_skew_form_nondegenerate':True,'odd_directed_cycle_J_requires_real_metric_spectral_sqrt':True,'even_directed_cycle_contrast_skew_form_degenerate':True},
 'trial_counts':{'filter_parameter_rows_with_duplicates_retained':len(r),'distinct_filter_t':len(set(fractions)),'cycle_rows':len(cycle),'filter_extremes_max_denominator_digits':50},
 'failed_test_controls':{'C2_equals_minus3Q_only_n3':True,'case_t0_filter_output_undefined_recorded':True,'case_t1_no_violation_recorded':True},
 'cautions':['no new experiment','results do not derive local filters from finite relations','full-state-space selection requires operational filtering, closure, unitary and convex assumptions','failure of filter closure does not refute G pair model with restricted instrument set']}
(OUT/'B3_RESULTS.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
print('PASS_B3_EXACT_AND_NUMERIC',len(r),'filter trials',len(cycle),'cycle trials','example gap',str(witness_gap.subs(sub)))
