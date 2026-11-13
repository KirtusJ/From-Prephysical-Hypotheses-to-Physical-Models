#!/usr/bin/env python3
"""Exact algebra and fully retained finite trials for a scoped mathematical model.
Does not test physical predictions, source validity, ontological emergence, or any ACR efficacy.
"""
from __future__ import annotations
from pathlib import Path
import csv, json, math, sys
import numpy as np
import sympy as sp

ROOT=Path(__file__).resolve().parent
P=sp.Matrix([[0,0,1],[1,0,0],[0,1,0]])
R=sp.Matrix([[0,1,0],[1,0,0],[0,0,1]])
C=P-P.T
Q=sp.eye(3)-sp.ones(3)/3
V=sp.Matrix([[1,0],[-1,1],[0,-1]])
assert P**3==sp.eye(3)
assert C**2==-3*Q
assert R*P*R==P**2
assert R*C*R==-C
assert (C.T+C)==sp.zeros(3)
assert C*Q==C and Q*C==C

# Restrict to the canonical zero-sum plane; all entries are rational.
left=(V.T*V).inv()*V.T
Pr=sp.simplify(left*P*V)
Cr=sp.simplify(left*C*V)
Rr=sp.simplify(left*R*V)
assert Cr**2==-3*sp.eye(2)
assert Pr**2+Pr+sp.eye(2)==sp.zeros(2)
assert Rr*Cr*Rr.inv()==-Cr

# Commutant of rotation on R^2 is two dimensional, adjoining reflection collapses it to scalars.
a,b,c,d=sp.symbols('a b c d', real=True)
T=sp.Matrix([[a,b],[c,d]])
sol_rot=sp.linsolve(list(T*Pr-Pr*T),[a,b,c,d])
sol_full=sp.linsolve(list(T*Pr-Pr*T)+list(T*Rr-Rr*T),[a,b,c,d])
rot=next(iter(sol_rot)); full=next(iter(sol_full))
assert len(rot)==4 and full[0]==full[3] and full[1]==0 and full[2]==0

# Phase data are derived only AFTER adding two real copies, real completion,
# an inner product, complex projectivization and a stipulated squared-overlap rule.
omega=(-sp.Integer(1)+sp.I*sp.sqrt(3))/2
B_from_cycle=sp.simplify((1+omega)/4)
assert sp.simplify(B_from_cycle-(1+sp.I*sp.sqrt(3))/8)==0
assert sp.simplify(sp.Abs(1+omega)**2-1)==0
pairs=(sp.Rational(1,2),sp.Rational(1,4),sp.Rational(1,2))
assert sp.simplify(sp.Abs(B_from_cycle)**2-sp.prod(pairs))==0

# General 3-ray Gram phase feasibility: det(G)=1-sum(p)+2 sqrt(prod(p))cos(phi).
def gram(p12,p23,p31,phase):
 a,b,c=np.sqrt([p12,p23,p31])
 t=c*np.exp(1j*phase)
 return np.array([[1.,a,np.conjugate(t)],[a,1.,b],[t,b,1.]], dtype=np.complex128)

seed=2026111202
rng=np.random.default_rng(seed)
angles=[-math.pi,-2.5,-2.,-1.5,-1.,-math.pi/3,-.01,0.,.01,math.pi/3,1.,1.5,2.,2.5,math.pi]
angles += rng.uniform(-math.pi,math.pi,256).tolist()
records=[]
for i,phi in enumerate(angles):
 G=gram(.25,.25,.25,phi)
 ev=np.linalg.eigvalsh(G)
 determinant=float(np.linalg.det(G).real)
 predicted=(1+math.cos(phi))/4
 # bounded floating-point validation, not rigorous enclosures
 assert abs(determinant-predicted)<3e-14
 assert ev[0]>-3e-14
 assert max(abs(np.abs(G[0,1])**2-.25),abs(np.abs(G[1,2])**2-.25),abs(np.abs(G[2,0])**2-.25))<3e-14
 records.append(dict(trial=i,phi_rad=phi,det_observed=determinant,det_formula=predicted,abs_det_residual=abs(determinant-predicted),min_eigenvalue=float(ev[0]),max_eigenvalue=float(ev[-1]),phase_real=float(math.cos(phi)),phase_imag=float(math.sin(phi))))

# CP1 versus CP2 qutrit witness with same pairwise transition probabilities.
for phi in (0, math.pi, math.pi/2):
 G=gram(.25,.25,.25,phi)
 rank=int((np.linalg.eigvalsh(G)>1e-11).sum())
 assert rank == (2 if phi==math.pi else 3)

# Director G's exact qubit triple and its conjugate, using an independent symbolic computation.
x=sp.Matrix([1,0]);y=sp.Matrix([sp.sqrt(3)/2,sp.Rational(1,2)]);z=sp.Matrix([sp.sqrt(3)/2,sp.I/2]);
inner=lambda u,v:(sp.conjugate(u).T*v)[0]
B=sp.simplify(inner(x,y)*inner(y,z)*inner(z,x))
assert B==sp.Rational(9,16)+3*sp.I/16
assert sp.simplify(inner(x,y)*inner(y,z)*inner(z,x) - sp.conjugate(inner(sp.conjugate(x),sp.conjugate(y))*inner(sp.conjugate(y),sp.conjugate(z))*inner(sp.conjugate(z),sp.conjugate(x))))==0

# Explicit numerical mutation guards: sign reversal, wrong cycle square, CP1/qutrit rank.
controls={'valid_cycle_identity':C**2==-3*Q,
          'false_cycle_identity_rejected':C**2!=-Q,
          'orientation_reversal_detected':R*C*R==-C and R*C*R!=C,
          'false_qubit_phase_rank_rejected':np.linalg.matrix_rank(gram(.25,.25,.25,0),tol=1e-10)!=2,
          'valid_qubit_rank_accepted':np.linalg.matrix_rank(gram(.25,.25,.25,math.pi),tol=1e-10)==2}
assert all(controls.values())

with (ROOT/'ALL_GRAM_PHASE_TRIALS.csv').open('w',newline='') as f:
 writer=csv.DictWriter(f,fieldnames=records[0].keys()); writer.writeheader();writer.writerows(records)
results={'status':'PASS_SCOPED_ALGEBRA_AND_FLOATING_POINT_CONTROLS','participant':'single AI assistant with source inspection; no independent expert',
  'cycle':{'P':str(P),'C':str(C),'P_restricted':str(Pr),'C_restricted':str(Cr),'reflection_restricted':str(Rr),
   'identities':['P^3=I','C^2=-3Q','RPR=P^2','RCR=-C'],
   'commutant_C3':str(rot),'commutant_S3':str(full),'symplectic_pairing_on_lattice_basis':str((V[:,0].T*C*V[:,1])[0]),
   'field_isomorphism':'Q[C|V] is Q[t]/(t^2+3), isomorphic to Q(sqrt(-3)); selected linearization functor required'},
  'phase_after_extra_assumptions':{'root_of_unity':str(omega),'B':str(B_from_cycle),'probabilities':list(map(str,pairs)),
    'assumed_completion':'two copies V_R, Euclidean metric, diagonal J, normalized rays, Born-style squared overlaps, Hopf quotient'},
  'director_G_exact_witness':str(B),
  'gram':{'seed':seed,'trial_count':len(records),'max_abs_det_residual':max(x['abs_det_residual'] for x in records),
          'min_recorded_eigenvalue':min(x['min_eigenvalue'] for x in records),'full_trials_file':'ALL_GRAM_PHASE_TRIALS.csv',
          'equal_probabilities_example':'p12=p23=p31=1/4: det=(1+cos(phi))/4, CP2 all phases, CP1 only phase pi'},
  'mutation_controls':{k:bool(v) for k,v in controls.items()},
  'scientific_limitations':['not independent source verification','not quantum emergence','not a physical observation',
       'no time, frequency, Born probability, composite dynamics or classical Hamiltonian mechanics derived']}
(ROOT/'RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
print(results['status'], 'cycle',results['cycle']['identities'],'trials',len(records),'max determinant residual',results['gram']['max_abs_det_residual'])
