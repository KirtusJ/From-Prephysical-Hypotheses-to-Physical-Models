#!/usr/bin/env python3
"""Director B second-stage independent checks, 2026-11-12.

Scope: conditional quantum geometry, *representation* equivalence under global
complex conjugation, and approximate homogeneity of finite nets. No physical
ontological selection or empirical verification is inferred.

Every deterministic numerical trial is retained, including extremal / rank-drop
cases. No filtering based on residuals. Uses fresh implementations rather than
importing Director A, G or B1 checkers.
"""
from __future__ import annotations
import json,csv,math,hashlib
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.spatial import cKDTree

ROOT=Path(__file__).resolve().parent
DATA=ROOT/'raw_trials'
DATA.mkdir(exist_ok=True)
TAU=2*math.pi

def json_dump(path,obj):
    Path(path).write_text(json.dumps(obj,indent=2,ensure_ascii=False,sort_keys=True)+'\n')

def rows_csv(path,rows):
    with Path(path).open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader();writer.writerows(rows)

def unit(v): return np.asarray(v,complex)/np.linalg.norm(v)

def gram_triple(phi):
    """Three explicit unit vectors in C^3 with fixed pairwise probs 1/4."""
    a=np.array([1.,0.,0.],complex)
    b=np.array([.5,math.sqrt(3)/2,0.],complex)
    c=np.array([.5*np.exp(-1j*phi), (1-.5*np.exp(-1j*phi))/math.sqrt(3), math.sqrt(max(0.,(1+math.cos(phi))/3))],complex)
    return np.stack((a,b,c))

def bargmann(V):
    return np.vdot(V[0],V[1])*np.vdot(V[1],V[2])*np.vdot(V[2],V[0])

def geo_arc(a,b):
    c=np.vdot(a,b)
    if abs(c)<1e-9: raise ValueError('projective orthogonal pair')
    aligned=b*np.exp(-1j*np.angle(c))
    ct=np.clip(np.vdot(a,aligned).real,-1,1)
    angle=math.acos(ct)
    if angle<1e-8: raise ValueError('coincident rays')
    tang=(aligned-ct*a)/math.sin(angle)
    def path(s):
        w=math.cos(s*angle)*a+math.sin(s*angle)*tang
        dw=angle*(-math.sin(s*angle)*a+math.cos(s*angle)*tang)
        z=w[1:]/w[0]
        dz=(dw[1:]*w[0]-w[1:]*dw[0])/(w[0]*w[0])
        return z,dz
    return path

def chart_guard(V,seed=74011):
    """Choose a chart avoiding affine-patch poles along the ENTIRE polygon.

    This retains the exact phi=+/-pi edge cases instead of discarding them.
    A geodesic can cross the initial chart boundary even when its endpoints do
    not. A deterministic unitary basis change fixes that numerical coordinate
    singularity without changing rays, pair probabilities or holonomy.
    """
    def margin(W):
        low=1.
        for a,b in zip(W,np.roll(W,-1,axis=0)):
            c=np.vdot(a,b)
            b=b*np.exp(-1j*np.angle(c))
            theta=math.acos(float(np.clip(np.vdot(a,b).real,-1.,1.)))
            tang=(b-math.cos(theta)*a)/math.sin(theta)
            for t in np.linspace(0.,1.,21):
                first=math.cos(theta*t)*a[0]+math.sin(theta*t)*tang[0]
                low=min(low,abs(first))
        return low
    chosen=V;best=margin(V)
    if best>=.17:return chosen,best,False
    rng=np.random.default_rng(seed)
    for i in range(250):
        Z=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3))
        Q,R=np.linalg.qr(Z)
        W=V@Q.T
        score=margin(W)
        if score>best:chosen,best=W,score
        if best>=.24:break
    if best<.075:raise ArithmeticError('could not find a non-singular affine chart')
    return chosen,best,True

def projective_tangent_holonomy(V):
    """Solve Levi-Civita connection in complex affine chart, not Berry shortcut.
       For Fubini-Study: Gamma^k_ij=-(delta^k_i zbar_j + delta^k_j zbar_i)/q.
    """
    V,chart_margin,chart_rotated=chart_guard(V)
    n=V.shape[1]-1
    frame=np.eye(n,dtype=complex)
    for a,b in zip(V,np.roll(V,-1,axis=0)):
        path=geo_arc(a,b)
        def rhs(s,flat):
            z,dz=path(s)
            q=1+np.vdot(z,z).real
            connection=(np.outer(dz,np.conj(z))+np.vdot(z,dz)*np.eye(n))/q
            return (connection@flat.reshape(n,n)).reshape(-1)
        sol=solve_ivp(rhs,(0.,1.),frame.ravel(),rtol=2.e-11,atol=1.e-13,method='DOP853')
        if not sol.success: raise RuntimeError(sol.message)
        frame=sol.y[:,-1].reshape(n,n)
    return np.linalg.det(frame),chart_margin,chart_rotated

# C2: one determinant-holonomy scalar does not invert (n+1)-th phase power.
phases=sorted(set(np.linspace(-math.pi,math.pi,257).tolist()+[0.,2*math.pi/3,-2*math.pi/3]))
gram_rows=[]
for phi in phases:
    V=gram_triple(phi)
    gram=V.conj()@V.T
    expected=np.array([[1,.5,.5*np.exp(-1j*phi)],[.5,1,.5],[.5*np.exp(1j*phi),.5,1]],complex)
    probs=[abs(np.vdot(V[i],V[(i+1)%3]))**2 for i in range(3)]
    B=bargmann(V)
    w=np.linalg.eigvalsh(gram)
    assert np.max(abs(gram-expected))<3e-13
    assert np.max(abs(np.asarray(probs)-.25))<5e-13
    assert abs(abs(B)-1/8)<5e-13
    assert w[0]>-2e-12
    row=dict(phi_rad=float(phi),B_real=float(B.real),B_imag=float(B.imag),
        Gram_det=float(np.linalg.det(gram).real), Gram_min_eigenvalue=float(w.min()),
        rank=int(np.sum(w>1e-9)),max_fixed_probability_error=float(np.max(abs(np.array(probs)-.25))),
        hol_det_via_analytic_identity_real=float(((B/abs(B))**3).real),
        hol_det_via_analytic_identity_imag=float(((B/abs(B))**3).imag))
    gram_rows.append(row)
rows_csv(DATA/'all_259_fixed_probability_phase_trials.csv',gram_rows)
assert len(phases)==259,len(phases)
V0=gram_triple(0)
V2=gram_triple(2*math.pi/3)
B0,B2=bargmann(V0),bargmann(V2)
assert abs(B0-1/8)<1e-12
assert abs(B2-np.exp(2j*math.pi/3)/8)<1e-12
assert abs((B0/abs(B0))**3-(B2/abs(B2))**3)<1e-12
# Both determinants = 1, both have all three pair probabilities 1/4.
# Independent direct Fubini-Study connection integration checks the two cases.
hol_rows=[]
for phi in [0., 2*math.pi/3,-2*math.pi/3,math.pi/3,math.pi,-math.pi,0.373,-1.127]:
    V=gram_triple(phi)
    h,chart_margin,chart_rotated=projective_tangent_holonomy(V)
    target=(bargmann(V)/abs(bargmann(V)))**3
    hol_rows.append(dict(phi_rad=phi,holonomy_real=float(h.real),holonomy_imag=float(h.imag),
      target_real=float(target.real),target_imag=float(target.imag),error=float(abs(h-target)),norm_error=float(abs(abs(h)-1)),
      chart_margin=float(chart_margin),rotated_chart=bool(chart_rotated)))
assert max(r['error'] for r in hol_rows)<2e-9
rows_csv(DATA/'all_8_direct_cp2_tangent_holonomy_trials.csv',hol_rows)
# Known false control: substituting phase exponent 2 for 3 must be rejected.
wrong_exp_2=abs((B2/abs(B2))**2-1)
assert wrong_exp_2>1

# C1: Every finite adaptive Kraus-instrument probability is invariant under
# simultaneous conjugation of the *whole* model and not under state-only conjugation.
def instrument(rng, n, nout=2):
    A=[rng.normal(size=(n,n))+1j*rng.normal(size=(n,n)) for _ in range(nout)]
    S=sum((a.conj().T@a for a in A),np.zeros((n,n),complex))
    ew,Q=np.linalg.eigh(S)
    assert ew.min()>1e-10
    Sminushalf=Q@np.diag(ew**(-.5))@Q.conj().T
    K=[a@Sminushalf for a in A]
    assert np.linalg.norm(sum((k.conj().T@k for k in K),np.zeros((n,n),complex))-np.eye(n))<1e-12
    return K

def outcomes(rho, tree, nstep):
    res=[]
    def walk(state,history,depth):
        if depth==nstep:
            res.append((history,float(np.trace(state).real),float(abs(np.trace(state).imag))))
            return
        for j,K in enumerate(tree[history]):walk(K@state@K.conj().T,history+(j,),depth+1)
    walk(rho,(),0)
    return res

gauge_rows=[]
for dim in (2,3,4):
    for seed in range(101,133):
        rng=np.random.default_rng(seed*29+dim)
        v=unit(rng.normal(size=dim)+1j*rng.normal(size=dim))
        w=unit(rng.normal(size=dim)+1j*rng.normal(size=dim))
        rho=.83*np.outer(v,v.conj())+.17*np.outer(w,w.conj())
        tree={}
        for depth in range(3):
            from itertools import product
            for path in product((0,1),repeat=depth):tree[path]=instrument(rng,dim)
        o1=outcomes(rho,tree,3)
        transformed={history:[K.conj() for K in Ks] for history,Ks in tree.items()}
        o2=outcomes(rho.conj(),transformed,3)
        assert [h for h,p,im in o1]==[h for h,p,im in o2]
        diff=max(abs(p-q) for ((_,p,_),(_,q,_)) in zip(o1,o2))
        assert abs(sum(p for _,p,_ in o1)-1)<3e-12
        assert abs(sum(p for _,p,_ in o2)-1)<3e-12
        assert diff<2e-12
        gauge_rows.append(dict(dim=dim,seed=seed,num_adaptive_sequences=len(o1),max_absolute_prob_diff=diff,
          original_prob_sum=sum(p for _,p,_ in o1),conjugate_prob_sum=sum(p for _,p,_ in o2)))
rows_csv(DATA/'all_96_adaptive_instrument_conjugation_trials.csv',gauge_rows)
# State-only conjugation can be operationally *detectable* with an unchanged reference.
v=np.array([1,1j])/math.sqrt(2)
rho=np.outer(v,v.conj())
ref_effect=rho.copy()
p_orig=float(np.trace(ref_effect@rho).real)
p_only_state=float(np.trace(ref_effect@rho.conj()).real)
p_all=float(np.trace(ref_effect.conj()@rho.conj()).real)
assert abs(p_orig-1)<1e-12 and abs(p_only_state)<1e-12 and abs(p_all-1)<1e-12

# C3: finite nonhomogeneous metric epsilon-nets inherit correspondence
# approximate homogeneity of a homogeneous compact ambient space.
def bloch_net(N):
    points=[]
    for j in range(N+1):
        th=j*math.pi/N
        if j in (0,N):
            points.append((math.sin(th),0.,math.cos(th)))
        else:
            for k in range(2*N):
                ph=k*math.pi/N
                points.append((math.sin(th)*math.cos(ph),math.sin(th)*math.sin(ph),math.cos(th)))
    return np.asarray(points,float)

def rotation_p_to_q(p,q):
    dot=float(np.clip(p@q,-1.,1.))
    if dot>1-1e-12: return np.eye(3)
    if dot<-1+1e-12:
        v=np.array([1.,0.,0.]) if abs(p[0])<.8 else np.array([0.,1.,0.])
        axis=np.cross(p,v);axis/=np.linalg.norm(axis)
        return 2*np.outer(axis,axis)-np.eye(3)
    c=np.cross(p,q);s=np.linalg.norm(c)
    k=np.array([[0,-c[2],c[1]],[c[2],0,-c[0]],[-c[1],c[0],0]])
    return np.eye(3)+k+k@k*((1-dot)/(s*s))

def FS_sphere(a,b): return .5*np.arccos(np.clip(np.sum(a*b,axis=-1),-1.,1.))

def closest_distances_degree(points):
    cosine=points@points.T
    d=FS_sphere(points[:,None,:],points[None,:,:])
    np.fill_diagonal(d,np.inf)
    near=d.min(axis=1)
    count=np.sum(abs(d-near[:,None])<1e-9,axis=1)
    return sorted(set(count.tolist())), sorted(set(np.round(near,8).tolist()))

net_rows=[]
for N in (4,8,16):
    points=bloch_net(N);num=len(points);tree=cKDTree(points)
    eps=math.pi/(2*N)
    degs,dists=closest_distances_degree(points)
    assert len(degs)>1, (N,degs) # proves nonhomogeneity for this particular net
    for trial in range(4):
        rng=np.random.default_rng(20261112+N*17+trial)
        ip,iq=rng.choice(num,size=2,replace=False)
        rot=rotation_p_to_q(points[ip],points[iq])
        assert np.linalg.norm(rot@points[ip]-points[iq])<1e-12
        targets=points@rot.T
        _,idx_forward=tree.query(targets)
        # inverse matching assures surjective correspondence to 2nd projection
        reverse_targets=points@rot
        _,idx_reverse=tree.query(reverse_targets)
        index_pairs=set((int(i),int(idx_forward[i])) for i in range(num))
        index_pairs|=set((int(idx_reverse[i]),int(i)) for i in range(num))
        index_pairs.add((int(ip),int(iq)))
        pairs=np.array(sorted(index_pairs),int)
        px=points[pairs[:,0]];py=points[pairs[:,1]]
        disp=FS_sphere(px@rot.T,py)
        assert float(np.max(disp))<=eps+2e-12,(N,float(np.max(disp)),eps)
        assert len(set(pairs[:,0]))==len(set(pairs[:,1]))==num
        picks=rng.integers(len(pairs),size=(12000,2))
        d1=FS_sphere(px[picks[:,0]],px[picks[:,1]])
        d2=FS_sphere(py[picks[:,0]],py[picks[:,1]])
        dis=float(np.max(abs(d1-d2)))
        assert dis<=2*eps+2e-12
        net_rows.append(dict(N=N,net_cardinality=num,eps_FS_proved=eps,distortion_limit_proved=2*eps,
          trial=trial,source_index=int(ip),target_index=int(iq),correspondence_pairs=len(pairs),
          max_FS_displacement=float(np.max(disp)),max_12000_sampled_pair_distortion=dis,
          nearest_neighbor_degree_values=';'.join(map(str,degs))))
rows_csv(DATA/'all_12_approximate_homogeneity_trials.csv',net_rows)

summary={'status':'PASS_SCOPED_MATHEMATICAL_CONSISTENCY_NOT_PHYSICAL_EMERGENCE',
 'date':'2026-11-12 B.C. Pacific Time',
 'research_participant':'one assistant, no independent subagents',
 'root_state':'INITIAL_EXTERNAL_GROUNDING_OPEN',
 'phase':{'grid_trials':len(phases),'direct_tangent_holonomy_trials':len(hol_rows),
 'max_direct_hol_error':max(r['error'] for r in hol_rows),
 'phi_counterexample_A':0.,'phi_counterexample_B':2*math.pi/3,
 'B_A':[float(B0.real),float(B0.imag)],'B_B':[float(B2.real),float(B2.imag)],
 'equal_det_holonomy':True,'all_three_pair_probabilities':[.25,.25,.25],
 'wrong_exponent_mutant_rejected':bool(wrong_exp_2>1),
 'root_recovery_caveat':'A continuous based family of loops can supply winding information beyond the endpoint determinant'},
 'conjugation':{'adaptive_tests':len(gauge_rows),'num_outcomes_per_test':8,
 'max_probability_residual':max(r['max_absolute_prob_diff'] for r in gauge_rows),
 'fixed_reference_original_p':p_orig,'fixed_reference_state_only_conjugated_p':p_only_state,
 'fixed_reference_whole_model_conjugated_p':p_all,
 'required_scope':'Simultaneously conjugate states, every instrument, transformations, effects, measurement reference and adaptive branch'},
 'finite_net':{'trials':len(net_rows),'N_values':[4,8,16],
 'GH_bound':'d_GH(X_epsilon,M)<=epsilon (extrinsic Hausdorff bound)',
 'approx_homogeneity_bound':'for any p,q in X there is a covering correspondence containing (p,q) with distortion <=2 epsilon',
 'source':'mathematical exact statement; finite Bloch-sphere nets import the ambient CP1 metric and isometry group'},
 'negative_controls':['wrong determinant exponent','state-only conjugation under fixed complex reference','nonhomogeneous net nearest-neighbor degree variation'],
 'externality':'No laboratory observations, prephysical dynamics, timing, probability origin or empirical error distributions'}
json_dump(ROOT/'RESULTS_B2.json',summary)
print(summary['status']);print('phase',summary['phase']);print('gauge max',summary['conjugation']['max_probability_residual']);print('net final',net_rows[-1]);print('all data files preserved:',[x.name for x in sorted(DATA.glob('*.csv'))])
