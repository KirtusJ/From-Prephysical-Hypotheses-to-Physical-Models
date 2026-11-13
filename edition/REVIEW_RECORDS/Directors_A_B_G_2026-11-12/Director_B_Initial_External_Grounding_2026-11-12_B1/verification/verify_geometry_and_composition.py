#!/usr/bin/env python3
"""Independent local mathematical checks. Standard numpy/sympy; no network, no physics claims.

Scope: CP^1 triangles and antiunitary ambiguity, RP^2 monodromy matrix,
quantum-vs-minimal-tensor Bell witness, and finite-orbit area lower bound.
Analytic CP^n determinant bundle proof and O(3) orbit classification are
separately in the research report; THIS SCRIPT DOES NOT PROVE THOSE THEOREMS.
"""
import json
from math import acos, degrees, pi, sqrt
from pathlib import Path
import numpy as np

rng = np.random.default_rng(20261112)


def normalized(x):
    return x/np.linalg.norm(x)


def bloch(v):
    a,b=v
    ab=np.conjugate(a)*b
    return np.array([2*ab.real, 2*ab.imag, (abs(a)**2-abs(b)**2)],float)


def bargmann(vs):
    a,b,c=vs
    return np.vdot(a,b)*np.vdot(b,c)*np.vdot(c,a)


def solid_angle(u,v,w):
    return 2*np.arctan2(np.dot(u,np.cross(v,w)),1+np.dot(u,v)+np.dot(v,w)+np.dot(w,u))


triangle_count=1000
max_overlap_error=0.0
max_geometry_error=0.0
max_conjugation_error=0.0
min_abs_B=1.0
sign_witness=None
for k in range(triangle_count):
    vs=[normalized(rng.normal(size=2)+1j*rng.normal(size=2)) for _ in range(3)]
    P=bargmann(vs)
    if abs(P)<1e-10: continue
    n=[bloch(x) for x in vs]
    for i in range(3):
        for j in range(i):
            p=abs(np.vdot(vs[i],vs[j]))**2
            p_geom=(1+np.dot(n[i],n[j]))/2
            max_overlap_error=max(max_overlap_error,abs(p-p_geom))
    Om=solid_angle(*n)
    helix=np.exp(1j*Om)
    predicted=(P/abs(P))**2
    max_geometry_error=max(max_geometry_error,abs(helix-predicted))
    Bmirror=bargmann([v.conjugate() for v in vs])
    max_conjugation_error=max(max_conjugation_error,abs(Bmirror-np.conjugate(P)))
    min_abs_B=min(min_abs_B,abs(P))
    if k==0:
        sign_witness={'B_real':float(P.real),'B_imag':float(P.imag),
                      'B_phase_radians':float(np.angle(P)),
                      'oriented_solid_angle':float(Om),
                      'wrong_exponent_one_error':float(abs(helix-P/abs(P)))}
assert max_overlap_error<2e-14
assert max_geometry_error<5e-13
assert max_conjugation_error<5e-14
assert sign_witness['wrong_exponent_one_error']>1e-3

# RP^2 one-sided geodesic lifting: parallel T, e_y from north to south,
# then deck derivative of antipodal A to identify south tangent with north.
# T_pi=-e_x -> dA(T_pi)=+e_x; e_y -> dA(e_y)=-e_y.
monodromy=np.diag([1.,-1.]); assert abs(np.linalg.det(monodromy)+1)<1e-15
# The commutant of all SO(2) rotations = a I + b J; commute also with
# reflection diag(1,-1) forces b=0.
J=np.array([[0.,-1.],[1.,0.]])
assert np.max(abs(monodromy@J-J@monodromy))>1

# Bell witness: separable-state alternative agrees on every single-qubit
# preparation, state and effect but not on bipartite accessible states.
I=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],complex)
Z=np.diag([1,-1]).astype(complex)
phi=normalized(np.array([1,0,0,1],complex))
rho=np.outer(phi,phi.conjugate())
A0,A1=Z,X
B0=(Z+X)/sqrt(2);B1=(Z-X)/sqrt(2)
Bell=np.kron(A0,B0+B1)+np.kron(A1,B0-B1)
chsh=float(np.trace(rho@Bell).real)
assert abs(chsh-2*sqrt(2))<1e-13
partial_transpose=rho.reshape(2,2,2,2).transpose(0,3,2,1).reshape(4,4)
pt_eig=np.linalg.eigvalsh(partial_transpose)
assert abs(pt_eig.min()+0.5)<1e-14
# numeric product states cannot exceed 2, plus analytic proof from locality.
max_sep_witness=0.
for _ in range(10000):
    v=normalized(rng.normal(size=2)+1j*rng.normal(size=2))
    w=normalized(rng.normal(size=2)+1j*rng.normal(size=2))
    prod=np.kron(v,w)
    val=float(np.vdot(prod,Bell@prod).real)
    max_sep_witness=max(max_sep_witness,abs(val))
assert max_sep_witness<=2+1e-12

# For |S|<=120, 120 equal spherical caps cannot cover S^2 if radius < acos(59/60).
# Does not verify the classification or the axial (cyclic/dihedral) group argument.
cap_lower=degrees(acos(59/60))
assert 10.47<cap_lower<10.48

out={
 'scope':'Computed checks on exact specified mathematical toy objects only, no physics or independent peer review',
 'seed':20261112,
 'cp1_triangles':triangle_count,
 'cp1_probability_metric_max_abs_error':max_overlap_error,
 'cp1_det_holonomy_vs_Bargmann_squared_max_abs_error':max_geometry_error,
 'cp1_conjugation_max_abs_error':max_conjugation_error,
 'cp1_min_B_magnitude':min_abs_B,
 'wrong_exponent_negative_control':sign_witness,
 'rp2_nontrivial_monodromy_matrix':monodromy.tolist(),
 'rp2_monodromy_determinant':float(np.linalg.det(monodromy)),
 'bell_state_CHSH':chsh,
 'bell_state_partial_transpose_eigenvalues':pt_eig.tolist(),
 'max_abs_CHSH_10000_random_product_states':max_sep_witness,
 'spherical_cap_lower_bound_degrees_for_N_le_120':cap_lower,
 'local_checks':'PASS',
 'limitations':['CP^n n>1 determinant identity is analytic not verified by this script',
                'Finite-subgroup O(3) classification is an external mathematical theorem, not checked computationally',
                '1000 random triangles and 10000 random product states are checks, not universal proofs']
}
fp=Path(__file__).with_name('geometry_and_composition_results.json')
fp.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print('PASS_LOCAL_GEOMETRY_COMPOSITION_TESTS')
print('CP1 geometry error',max_geometry_error,'CP1 sign control',sign_witness['wrong_exponent_one_error'])
print('CHSH',chsh, 'PPT min',float(pt_eig.min()), 'cap lower degrees',cap_lower)
