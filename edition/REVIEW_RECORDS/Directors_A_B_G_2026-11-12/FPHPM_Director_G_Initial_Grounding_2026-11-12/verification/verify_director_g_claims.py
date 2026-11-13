#!/usr/bin/env python3
"""Director G: bounded checks for source-grounded mathematical claims.

No ACR host integration; one implementation, not independent certification.
Outputs include ALL deterministic numerical cases, without filtering outliers.
"""
import csv, json, math, sys
from pathlib import Path
from fractions import Fraction

import numpy as np
import sympy as sp

ROOT=Path(__file__).resolve().parent
I=sp.I
sqrt3=sp.sqrt(3)
X=sp.Matrix([1,0]); Y=sp.Matrix([sqrt3/2,sp.Rational(1,2)]); Z=sp.Matrix([sqrt3/2,I/2]); Zbar=Z.conjugate()

def dot(u,v): return sp.expand((u.conjugate().T*v)[0])
def prob(u,v): return sp.simplify(dot(u,v)*dot(v,u))
def B(u,v,w): return sp.simplify(dot(u,v)*dot(v,w)*dot(w,u))

def check(expr, value):
    return sp.simplify(expr-value)==0

b=B(X,Y,Z); bc=B(X,Y,Zbar)
pair_probs=[prob(X,Y), prob(Y,Z), prob(Z,X)]
pair_probs_conj=[prob(X,Y),prob(Y,Zbar),prob(Zbar,X)]
assert b==(9+3*I)/16, (b,'unexpected B')
assert bc==(9-3*I)/16
assert pair_probs == pair_probs_conj == [sp.Rational(3,4), sp.Rational(5,8), sp.Rational(3,4)]
assert sp.im(b)!=0

# 2013 Gelander comparison applies to finite homogeneous metric spaces and CP^n, n>=1 (non-torus).
# Finite-orbit cap bound from cap surface area and finite subgroup classification; only numeric evaluation here.
r60=math.degrees(math.acos(29/30))
r120=math.degrees(math.acos(59/60))
assert r60>14.8 and r120>10.4 and r60>r120
# Direct closed-form classical countermodel: same classical barycentre, different allowed effect.
u=sp.symbols('u',real=True)
assert sp.integrate(u, (u,-1,1))/2==0
assert sp.integrate(u*u, (u,-1,1))/2 == sp.Rational(1,3)
assert sp.Rational(1,2)*(1*1 + (-1)*(-1))==1

# Curvature discriminator with identical projective-transition distance normalization.
# CP^1: stereographic metric g=(1+x^2+y^2)^(-2) (sphere radius 1/2).
# RP^2: quotient of unit sphere, local stereographic metric 4g (sphere radius 1).
x,y=sp.symbols('x y',real=True)
q=1+x*x+y*y

def curvature(conformal_factor):
    log_sqrt=sp.log(conformal_factor)/2
    K=-((sp.diff(log_sqrt,x,2)+sp.diff(log_sqrt,y,2))/conformal_factor)
    return sp.simplify(K)
K_CP1=curvature(q**(-2))
K_RP2=curvature(4*q**(-2))
assert K_CP1==4 and K_RP2==1, (K_CP1,K_RP2)

# Pointwise CP1 Berry phase / SO3 spherical Levi-Civita parallel transport along geodesic edges.
def bloch(psi):
    psi=np.asarray(psi,dtype=complex)
    psi=psi/np.linalg.norm(psi)
    a,c=psi
    return np.array([2*np.real(np.conj(a)*c), 2*np.imag(np.conj(a)*c), abs(a)**2-abs(c)**2],float)

def Rodrigues(axis,theta):
    axis=axis/np.linalg.norm(axis)
    x,y,z=axis
    K=np.array([[0,-z,y],[z,0,-x],[-y,x,0]],float)
    return np.eye(3)+np.sin(theta)*K+(1-np.cos(theta))*K@K

def parallel_geodesic(a,b):
    axis=np.cross(a,b); mag=np.linalg.norm(axis)
    if mag<1e-12: raise ValueError('nearly degenerate geodesic')
    theta=math.atan2(mag,float(np.dot(a,b)))
    return Rodrigues(axis,theta)

def wrapped(z): return math.atan2(math.sin(z),math.cos(z))

def phase_check(a,b,c):
    a=np.asarray(a,dtype=complex);b=np.asarray(b,dtype=complex);c=np.asarray(c,dtype=complex)
    a=a/np.linalg.norm(a);b=b/np.linalg.norm(b);c=c/np.linalg.norm(c)
    ba=np.vdot(a,b)*np.vdot(b,c)*np.vdot(c,a)
    r0,r1,r2=[bloch(w) for w in (a,b,c)]
    mats=[parallel_geodesic(r0,r1),parallel_geodesic(r1,r2),parallel_geodesic(r2,r0)]
    hol=mats[2]@mats[1]@mats[0]
    t=np.cross(r0,np.array([1.,0.,0.]))
    if np.linalg.norm(t)<.01: t=np.cross(r0,np.array([0.,1.,0.]))
    t/=np.linalg.norm(t)
    jt=np.cross(r0,t)
    transported=hol@t
    actual=math.atan2(float(jt@transported),float(t@transported))
    target=2*np.angle(ba)
    return wrapped(actual-target), float(np.linalg.norm(hol@r0-r0)), float(abs(ba)), float(actual),float(target)

fixed=phase_check(np.array([1,0],complex),np.array([np.sqrt(3)/2,1/2],complex),np.array([np.sqrt(3)/2,1j/2],complex))
assert abs(fixed[0])<1e-12, fixed
assert abs(fixed[1])<1e-12, fixed

rng=np.random.default_rng(20261112)
rows=[]; errors=[]; anchor_errors=[]
for i in range(96):
    v=rng.normal(size=(3,2))+1j*rng.normal(size=(3,2))
    v=v/np.linalg.norm(v,axis=1)[:,None]
    err,anchor,mag,actual,target=phase_check(*v)
    rows.append({'trial':i,'phase_error_rad':f'{err:.17g}','anchor_error':f'{anchor:.17g}',
      'bargmann_modulus':f'{mag:.17g}','holonomy_phase_rad':f'{actual:.17g}',
      'twice_bargmann_arg_rad':f'{target:.17g}', 'status':'retained'})
    errors.append(abs(err));anchor_errors.append(anchor)
assert len(rows)==96
assert max(errors)<2e-12 and max(anchor_errors)<2e-12,(max(errors),max(anchor_errors))
with open(ROOT/'ALL_96_SPHERE_HOLONOMY_TRIALS.csv','w',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)

# Deliberately false candidate must be rejected (fault-injection control).
positive_control=check(b,(9+3*I)/16)
negative_control_rejected=not check(b,(9-3*I)/16)
assert positive_control and negative_control_rejected

result={
 'status':'PASS_SCOPED_ARITHMETIC_AND_NUMERIC_CHECKS_NOT_PROOF_OR_PHYSICAL_VALIDATION',
 'participants':'one AI assistant; one code implementation; no independent assessment',
 'exact_three_ray_witness':{
    'states':'X=(1,0); Y=(sqrt(3)/2,1/2); Z=(sqrt(3)/2,i/2)',
    'probabilities_XY_YZ_ZX':[str(x) for x in pair_probs],
    'bargmann':str(b),'bargmann_conjugate':str(bc),
    'metric_same_under_conjugation':True,
    'phase_radians':float(sp.arg(b)),'conjugate_phase_radians':float(sp.arg(bc)),
    'note':'Complex rays and standard inner product are stipulated for this conditional counterexample.'},
 'classical_spin_countermodel':{
    'pure_state_geometry':'(S^2,round metric,signed area symplectic form)',
    'classical_mixed_states':'Borel probability measures on S^2',
    'two_distributions_same_mean':True,
    'effect_nz_squared_antipodal':1.,'effect_nz_squared_uniform':1/3,
    'higher_order_interference':'classical disjoint filters obey finite additivity; no nontrivial I_k for k>=2'},
 'sphere_transport':{
    'method':'exact great-circle ambient rotations (Rodrigues), NOT a Schild-ladder algorithm',
    'fixed_phase_error_rad':fixed[0], 'random_seed':20261112,'num_trials':len(rows),
    'max_phase_error_rad':max(errors),'max_loop_anchor_error':max(anchor_errors),
    'all_trials_file':'ALL_96_SPHERE_HOLONOMY_TRIALS.csv',
    'note':'Conventional CP1/S2 geometry is input, not derived. Monte Carlo checks do not prove any general identity.'},
 'finite_group_cover_radius_lower_bounds':{
    'SO3_icosahedral_max_orbit_60_degrees':r60,
    'O3_icosahedral_max_orbit_120_degrees':r120,
    'SO3_exact_cosine_upper_bound':'29/30',
    'O3_exact_cosine_upper_bound':'59/60',
    'proof_dependencies':'classification of finite subgroups of SO(3), axis normality for cyclic/dihedral, spherical cap area'},
 'local_curvature_discriminator':{'CP1_FS_constant_gaussian_curvature':int(K_CP1), 'RP2_real_projective_constant_gaussian_curvature':int(K_RP2), 'normalization':'d([u],[v]) = arccos |<u,v>|, both diameters pi/2', 'scope':'Intrinsic 2D Riemannian geometry under transition-probability metric. Only-by-monodromy is not literal across all tests.'},
 'orientation_under_opposite_complex_structure':{
    'real_orientation_multiplier_by_complex_dimension':{str(n):(-1)**n for n in range(1,7)},
    'even_n_same_real_orientation_J_versus_negative_J':True},
 'checker_controls':{'valid_control_accepted':positive_control,'known_false_conjugated_B_rejected':negative_control_rejected},
 'boundaries':['no actual experiment','no G7/Z1 manuscript access','no independent reviewers','not a physical bridge',
 'finite classical spin model is infinite-dimensional as convex state space; classification theorems imposing finite-dimensionality require separate assessment']
}
with open(ROOT/'RESULTS.json','w') as f: json.dump(result,f,indent=2,ensure_ascii=False)
print(result['status'])
print('B =',b,'P =',[str(x) for x in pair_probs],'sphere holonomy max_err',max(errors))
print('cap bounds: SO3',r60,'O3',r120)
print('controls',result['checker_controls'])
