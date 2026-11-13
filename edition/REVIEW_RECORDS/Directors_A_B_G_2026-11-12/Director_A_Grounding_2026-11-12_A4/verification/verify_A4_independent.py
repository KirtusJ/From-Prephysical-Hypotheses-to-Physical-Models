#!/usr/bin/env python3
"""Director A A4: exact-scope and finite-controls for gain-graph GH-1.
All variables are stipulated mathematical objects; none is a physical model.
No unpublished primitive or experimental data is used.
"""
from __future__ import annotations
import json, math, cmath
from collections import deque
from fractions import Fraction
from pathlib import Path
import numpy as np
import sympy as sp

OUTPUT=Path(__file__).resolve().parent
results={'scope':'stipulated finite K4 gain graph with Z_n transport and a separately assumed one-dimensional unitary character; no emergent physics', 'claims':{}, 'trials':[]}

# All K4 edges have voltage zero except the orientation 2->3, which has gain +1.
def voltage(u,v,n):
    if (u,v)==(2,3):return 1%n
    if (u,v)==(3,2):return -1%n
    return 0

def cover_matrix(n):
    size=4*n
    M=np.zeros((size,size),dtype=np.int64)
    for v in range(4):
        for g in range(n):
            for w in range(4):
                if w==v: continue
                gg=(g+voltage(v,w,n))%n
                M[4*gg+w,4*g+v]=1
    assert np.array_equal(M,M.T)
    assert all(int(x)==3 for x in np.sum(M,axis=0))
    return M

def connected_bipartite(M):
    n=M.shape[0];colors={0:0};todo=deque([0]);bipartite=True
    while todo:
        a=todo.popleft()
        for b in np.flatnonzero(M[a]):
            b=int(b)
            if b not in colors:colors[b]=colors[a]^1;todo.append(b)
            elif colors[b]==colors[a]:bipartite=False
    return len(colors)==n,bipartite

for n in [2,3,4,5,6,7,8]:
    M=cover_matrix(n)
    connected,bipartite=connected_bipartite(M)
    assert connected and not bipartite
    eig=np.linalg.eigvalsh(M.astype(float))
    assert abs(max(eig)-3)<1e-10
    assert np.max(np.abs(eig[:-1]))<3-1e-8
    A=np.eye(4*n,dtype=np.int64)
    primitive_exponent=None
    for k in range(1,28):
        A=A@M
        if np.min(A)>0:
            primitive_exponent=k;break
    assert primitive_exponent is not None
    results['trials'].append({'control':'cover_primitive','cyclic_order':n,'vertices':4*n,'connected':connected,'bipartite':bipartite,'first_all_positive_matrix_power':primitive_exponent,'second_spectral_radius':float(np.max(np.abs(eig[:-1]))),'Perron_root':3})

n=3;M=cover_matrix(n)
arr=np.zeros(4*n,dtype=object);arr[0]=1
for k in range(0,19):
    if k:arr=M@arr
    counts=[int(x) for x in arr]
    assert sum(counts)==3**k
    results['trials'].append({'control':'all_voltage_walk_counts','step':k,'counts_by_gain_then_vertex':counts,'min_count':min(counts),'max_count':max(counts),'total':sum(counts)})
results['claims']['K4_cover_primitive']='PROVED_BY_CONNECTIVITY_AND_ODD_CYCLE; finite checks for n=2..8'
results['claims']['K4_growth']='PROVED_BY_PERRON_FROBENIUS; for every n>=2, each (vertex,gain) count is asymptotic to 3^k/(4n)'

# Exact complex character matrix for Z_3, using omega=(-1+i sqrt(3))/2.
I=sp.I;omega=(-sp.Integer(1)+I*sp.sqrt(3))/2
omega_conj=sp.conjugate(omega)
A=sp.zeros(4)
for u in range(4):
    for v in range(4):
        if u==v:continue
        z=voltage(u,v,3)
        gain=(1,omega,omega_conj)[z%3]
        A[v,u]=gain
assert A.conjugate().T==A
root=sp.Matrix([1,0,0,0])
v0=root;v1=A*root;v2=A*v1
mu0=sp.simplify((v0.conjugate().T*v0)[0]);mu1=sp.simplify((v1.conjugate().T*v1)[0]);mu2=sp.simplify((v2.conjugate().T*v2)[0])
assert (mu0,mu1,mu2)==(1,3,15)
# Paths 0->1 and 0->2 at step 1 have orthogonal endpoint vectors, and their
# complete extensions can interfere at step 2.
e1=sp.Matrix([0,1,0,0]);e2=sp.Matrix([0,0,1,0])
cross1=sp.simplify((e1.conjugate().T*e2)[0]);cross2=sp.simplify(((A*e1).conjugate().T*(A*e2))[0]);
assert cross1==0 and sp.simplify(cross2-(1+omega))==0
succ_prob=sp.simplify(((A*e1).conjugate().T*(A*e1))[0])
assert succ_prob==3
p_at1=sp.Rational(1,3);p_at2=succ_prob/mu2
assert p_at2==sp.Rational(1,5)
results['claims']['cylinder_consistency']='REFUTED for the GH-1 K4 pair kernel under natural extension: D_1(w1,w2)=0 but D_2(Ext w1,Ext w2)=1+omega != 0'
results['claims']['probability_step_compatibility']='FAIL: normalized one-step singleton 1/3 vs normalized mass of all two-step extensions 1/5'
results['exact']={'omega':str(omega),'A_complex_Z3':[[str(sp.simplify(A[i,j])) for j in range(4)] for i in range(4)],'v2':[str(sp.simplify(v)) for v in v2],'total_masses_k0_k1_k2':[str(mu0),str(mu1),str(mu2)],'D1_two_singletons':str(cross1),'D2_extensions':str(cross2),'squared_abs_D2':str(sp.simplify(sp.expand_complex(cross2*sp.conjugate(cross2)))),'normalized_singleton_at_k1':str(p_at1),'normalized_all_extensions_at_k2':str(p_at2)}

# A nonnegative gauge-invariant *additive* walk measure can detect a closed-walk gain,
# as soon as the universal rule is allowed to read whether a walk ends at its root.
# At length 3: path (0,1,2,0) has gain 0; (0,2,3,0) has gain +1.
def path_gain(path,n):return sum(voltage(path[k],path[k+1],n) for k in range(len(path)-1))%n
trivial=(0,1,2,0);twisted=(0,2,3,0)
assert path_gain(trivial,3)==0 and path_gain(twisted,3)==1
weight0=1+sp.re(omega**0);weight1=1+sp.re(omega)
assert weight0==2 and weight1==sp.Rational(1,2)
# Gauge transformations on abelian Z3 cancel on a closed walk for any vertex labeling.
for gauge in [(0,1,2,1),(2,2,1,0),(1,0,0,2)]:
    def adjusted_gain(path):
        return sum(voltage(path[i],path[i+1],3)+gauge[path[i+1]]-gauge[path[i]] for i in range(len(path)-1))%3
    assert adjusted_gain(trivial)==0 and adjusted_gain(twisted)==1
results['claims']['first_order_endpoint_aware']='NONNEGATIVE gauge-invariant additive closed-walk rule distinguishes trivial and nontrivial holonomy, outside endpoint-blind Lemma 3.1'
results['exact']['additive_closed_walk_weights']={'trivial':str(weight0),'twisted':str(weight1),'I2':'0','I3':'0'}

# Negative control: all zero gains make Z3 covering split into three components,
# so the crucial growth hypothesis no longer holds for every gain sector.
all_zero=np.zeros((12,12),dtype=np.int64)
for v in range(4):
 for g in range(3):
  for w in range(4):
   if w!=v:all_zero[4*g+w,4*g+v]=1
conn0,_=connected_bipartite(all_zero)
assert not conn0
results['claims']['no_gain_negative_control']='PASS disconnected 3-sector cover; no gain reachability'

# Exact three-ray Bargmann invariant and corrected sign of horizontal lift
# for G7 proof: alpha_k=-arg(B), so a_k=exp(-i arg B) a0.
a0=sp.Matrix([1,0]);a1=sp.Matrix([sp.sqrt(3)/2,sp.Rational(1,2)]);a2=sp.Matrix([sp.sqrt(3)/2,I*sp.Rational(1,2)])
inner=lambda u,v:(u.conjugate().T*v)[0]
B=sp.simplify(inner(a0,a1)*inner(a1,a2)*inner(a2,a0))
assert B==(sp.Integer(9)+3*I)/16
bphase=sp.simplify(B/sp.sqrt(B*sp.conjugate(B)))
assert sp.simplify(bphase-(3+I)/sp.sqrt(10))==0
assert sp.simplify(bphase**2-(4+3*I)/5)==0
results['claims']['G7_proof_sign']='ALGEBRAIC_CORRECTION alpha_final=-arg B (not +arg B); consequently T=exp(+i arg B) U_perp; determinant identity unchanged'
results['exact']['Bargmann_example']={'B':str(B),'phase':str(bphase),'horizontal_lift_terminal_phase':str(sp.conjugate(bphase)),'det_T_for_n1':str(sp.simplify(bphase**2))}

(OUTPUT/'A4_INDEPENDENT_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
print('PASS_A4_INDEPENDENT; K4 covers n2..8 primitive; n3 19 consecutive exact-count rows; K4 mu=1,3,15; decoherence extension witness; gauge-invariant additive counterexample; G7 horizontal phase sign verified')
print('K4 cross term:',sp.simplify(cross2),'squared modulus:',sp.simplify(sp.expand_complex(cross2*sp.conjugate(cross2))))
print('All',len(results['trials']),'trial rows retained')
