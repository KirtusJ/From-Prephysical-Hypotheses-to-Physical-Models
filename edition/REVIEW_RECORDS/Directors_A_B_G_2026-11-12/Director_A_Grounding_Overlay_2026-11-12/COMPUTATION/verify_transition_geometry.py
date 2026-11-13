#!/usr/bin/env python3
"""Director A first-principles transition geometry tests. Toy classical/complex projective geometry; not a physical reconstruction."""
from __future__ import annotations
import json, math, sys
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from numpy.polynomial.legendre import leggauss

EPS=1e-12

def nrm(v):return v/np.linalg.norm(v)
def angle(z): return float(np.angle(z))
def unitphase(z):return z/abs(z)
def rays(dim, seed, count):
    rng=np.random.default_rng(seed)
    V=[]
    for j in range(count):
        v=np.r_[1.+0j, .35*(rng.normal(size=dim-1)+1j*rng.normal(size=dim-1))]
        V.append(nrm(v))
    return V

def phase_polygon(V):
    p=1+0j
    for a,b in zip(V,V[1:]+V[:1]):p*=np.vdot(a,b)
    return unitphase(p)

def geodesic_arc(a,b):
    c=np.vdot(a,b)
    if abs(c)<1e-9: raise ValueError('orthogonal endpoints: shortest geodesic nonunique')
    b=b*np.exp(-1j*np.angle(c))
    theta=math.acos(np.clip(float(np.real(np.vdot(a,b))),-1.,1.))
    if theta<1e-12:raise ValueError('coincident endpoint')
    q=(b-math.cos(theta)*a)/math.sin(theta)
    def path(t):
        psi=np.cos(theta*t)*a+np.sin(theta*t)*q
        dpsi=theta*(-np.sin(theta*t)*a+np.cos(theta*t)*q)
        z=psi[1:]/psi[0]
        dz=(dpsi[1:]*psi[0]-psi[1:]*dpsi[0])/(psi[0]**2)
        return z,dz
    return path

def path_integral_A(V, steps=64):
    nodes, weights=leggauss(steps)
    total=0.
    for a,b in zip(V,V[1:]+V[:1]):
        path=geodesic_arc(a,b)
        for t,w in zip(.5*(nodes+1),.5*weights):
            z,dz=path(t)
            total+=w*float(np.imag(np.vdot(z,dz))/(1+np.vdot(z,z).real))
    return total

def tangent_holonomy_matrix(V):
    n=len(V[0])-1
    M=np.eye(n, dtype=complex)
    for a,b in zip(V,V[1:]+V[:1]):
        path=geodesic_arc(a,b)
        def rhs(t,y):
            z,dz=path(t)
            D=1+np.vdot(z,z).real
            A=(np.vdot(z,dz)*np.eye(n)+np.outer(dz,z.conj()))/D
            return (A@y.reshape(n,n)).reshape(-1)
        sol=solve_ivp(rhs,[0,1],M.reshape(-1),rtol=3e-12,atol=4e-14, method='DOP853')
        assert sol.success,sol.message
        M=sol.y[:,-1].reshape(n,n)
    z0=V[0][1:]/V[0][0]
    D=1+np.vdot(z0,z0).real
    g=np.eye(n)/D-np.outer(z0,z0.conj())/(D**2)
    norm_check=np.linalg.norm(M.conj().T@g@M-g)
    return complex(np.linalg.det(M)), float(norm_check)

def gram_family(phi):
    r=.5
    G=np.array([[1,r,r*np.exp(-1j*phi)], [r,1,r], [r*np.exp(1j*phi),r,1]], complex)
    ew,Q=np.linalg.eigh(G)
    assert ew.min()>=-2e-14,ew
    V=np.sqrt(np.maximum(0,ew))[:,None]*Q.conj().T # columns V_j in common C^3 from V^dag V = Q diag(e) Q^dag
    assert np.linalg.norm(V.conj().T@V-G)<1e-12
    prob=np.abs(V.conj().T@V)**2
    delta=np.vdot(V[:,0],V[:,1])*np.vdot(V[:,1],V[:,2])*np.vdot(V[:,2],V[:,0])
    return {'phi_rad':float(phi), 'min_Gram_eig':float(ew.min()), 'rank':int(np.sum(ew>1e-10)), 'pairwise_probabilities':[float(prob[0,1]),float(prob[1,2]),float(prob[2,0])], 'delta': [float(delta.real),float(delta.imag)], 'phase_rad':angle(delta), 'determinant':float(np.linalg.det(G).real)}

def classical_spin_I3():
    # Ordinary Kolmogorov measure: disjoint sectors' union probability sums, so I3 is zero for any distribution.
    mu=np.array([.11,.17,.29,.43])
    prob=lambda ids:sum(mu[i] for i in ids)
    a,b,c={0},{1},{2}
    return prob(a|b|c)-prob(a|b)-prob(a|c)-prob(b|c)+prob(a)+prob(b)+prob(c)-prob(set())

def spherical_net_cover_samples(N, count, seed):
    """Lat-long grid in S^2; FS distance = half the central spherical angle."""
    rng=np.random.default_rng(seed)
    u=rng.uniform(-1,1,count)
    theta=np.arccos(u)
    phi=rng.uniform(0,2*np.pi,count)
    ti=np.rint(theta*N/np.pi)
    pj=np.rint(phi*N/np.pi)
    qt=ti*np.pi/N
    qp=(pj%(2*N))*np.pi/N
    cosd=np.cos(theta)*np.cos(qt)+np.sin(theta)*np.sin(qt)*np.cos(phi-qp)
    dFS=.5*np.arccos(np.clip(cosd,-1,1))
    analytic_upper=np.pi/(2*N)
    assert np.max(dFS)<=analytic_upper+1e-10
    return {"N":N,"lattice_latitudes":N+1,"longitude_samples":2*N,"random_probe_points":count,"observed_max_FS_distance":float(np.max(dFS)),"proved_FS_upper_bound":float(analytic_upper)}

def main():
    data={'manifest':'First-principles numerical and algebraic checks, no physical evidence', 'rng':'numpy default_rng with stated seeds', 'geometry':[], 'gram':[]}
    for phi in [0.,math.pi/6,math.pi/2,math.pi, -math.pi/2]:data['gram'].append(gram_family(phi))
    assert all(max(abs(v-.25) for v in t['pairwise_probabilities']) <1e-12 for t in data['gram'])
    assert abs(data['gram'][0]['phase_rad'])<1e-12
    assert abs(data['gram'][2]['phase_rad']-math.pi/2)<1e-12
    for dim in (2,3,4):
        V=rays(dim, 900+dim, 4)
        for polygon in (V[:3],V[:4]):
            area=path_integral_A(polygon,96)
            bp=phase_polygon(polygon)
            hol, metric_err=tangent_holonomy_matrix(polygon)
            predicted=bp**dim
            error=float(abs(hol-predicted))
            A_error=float(abs(np.exp(1j*area)-bp))
            assert error<5e-9,(dim,error)
            assert A_error<1e-9,(dim,A_error)
            assert metric_err<1e-9,(dim,metric_err)
            conjV=[v.conj() for v in polygon]
            old_probs=[abs(np.vdot(a,b))**2 for a,b in zip(polygon,polygon[1:]+polygon[:1])]
            conj_probs=[abs(np.vdot(a,b))**2 for a,b in zip(conjV,conjV[1:]+conjV[:1])]
            assert max(abs(x-y) for x,y in zip(old_probs,conj_probs))<1e-15
            assert abs(phase_polygon(conjV)-bp.conjugate())<1e-14
            data['geometry'].append({'complex_vec_dim':dim, 'projective_complex_dim':dim-1,'num_polygon_vertices':len(polygon), 'bargmann_phase_rad':angle(bp), 'line_integral_phase_rad':float(area),'phase_quadrature_abs_error':A_error,'tangent_holonomy_det_phase_rad':angle(hol),'determinant_abs_error':error,'metric_preservation_norm_residual':metric_err,'complex_conjugation_pairwise_probability_difference':max(abs(x-y) for x,y in zip(old_probs,conj_probs))})
    epsvals=[.05,.1,.2,.3]
    curves=[]
    for t in epsvals:
        dR=math.acos(math.cos(t)**2) # RP2, standard unit sphere quotient
        dC=.5*math.acos(math.cos(2*t)**2) # CP1, half-radius sphere
        curves.append({'leg_length':t,'RP2_opposite_dist':dR,'CP1_opposite_dist':dC,'RP2_minus_CP1':dR-dC})
        assert dR>dC
    data['curvature_comparison']={'K_RP2':1,'K_CP1':4,'right_angle_triangle_distance':curves,'scaling':'d([u],[v])=acos(|<u,v>|) for normalized rays'}
    data['finite_net_positive_control']=[spherical_net_cover_samples(k,20000,25000+k) for k in [4,8,16,32,64]]
    # Static CP1 geometry admits inequivalent one-parameter unitary flows; no clock or generator is selected by the metric.
    v=np.array([1.,1.],complex)/math.sqrt(2)
    tau=math.pi/2
    U0=np.eye(2,dtype=complex)
    U1=np.diag(np.exp(-.5j*tau*np.array([1,-1])))
    assert np.linalg.norm(U1.conj().T@U1-np.eye(2))<1e-14
    survival0=abs(np.vdot(v,U0@v))**2
    survival1=abs(np.vdot(v,U1@v))**2
    assert abs(survival0-1)<1e-14 and abs(survival1-.5)<1e-14
    # Prescribed dephasing of a Hadamard destroys injectivity, unlike deterministic Hamiltonian flow.
    T=np.ones((2,2))/2
    assert np.linalg.matrix_rank(T)==1 and np.linalg.norm(T[:,0]-T[:,1])==0
    data['dynamics_nonselection']={'chosen_formal_time':tau,'survival_H_zero':float(survival0),'survival_H_sigma_z_over_two':float(survival1),'dephasing_T':T.tolist(),'rank_T':int(np.linalg.matrix_rank(T)),'context':'Exact analytic controls inside imported 2-level theory, not experimental dynamics or a derived qubit'}
    data['classical_I3_exact_float_residual']=float(classical_spin_I3())
    assert abs(data['classical_I3_exact_float_residual'])<1e-15
    out=Path(sys.argv[1] if len(sys.argv)>1 else 'transition_geometry_results.json')
    out.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
    print('ALL_CHECKS_PASS; six holonomies, five Gram families, four metric triangles, classical I3, five finite nets, two dynamical controls')
    print('max det error',max(v['determinant_abs_error'] for v in data['geometry']))
    print('max quadrature error',max(v['phase_quadrature_abs_error'] for v in data['geometry']))
    print('max metric preservation error',max(v['metric_preservation_norm_residual'] for v in data['geometry']))
    print('RP2 vs CP1 at eps=.2',curves[2])
    print('JSON',out)

if __name__=='__main__': main()
