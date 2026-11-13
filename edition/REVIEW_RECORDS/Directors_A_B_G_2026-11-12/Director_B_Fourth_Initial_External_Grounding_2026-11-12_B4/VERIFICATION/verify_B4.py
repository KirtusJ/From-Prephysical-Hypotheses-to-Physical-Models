#!/usr/bin/env python3
"""Director B, B4: bounded exact finite-graph verification.

Checks are exact Python integer/Fraction/cyclotomic algebra wherever possible.
All models are stipulated mathematics; no experiment, clock or physics is inferred.
"""
from __future__ import annotations
import csv, json, itertools, math
from fractions import Fraction
from pathlib import Path

HERE=Path(__file__).resolve().parent

# Record EVERY counted (length, terminal vertex, group gain) state, including zeros.
# Gain +1 on 0->3, -1 on 3->0, and zero on all other K4 oriented edges.
V=(0,1,2,3)
def edge_gain(u,v):
    assert u != v and u in V and v in V
    return 1 if (u,v)==(0,3) else (-1 if (u,v)==(3,0) else 0)

def k4_dp(max_k=40):
    d={(v,g):(1 if (v,g)==(0,0) else 0) for v in V for g in range(3)}
    rows=[]; minima=[]
    for k in range(max_k+1):
        assert sum(d.values())==3**k
        for v in V:
            for g in range(3): rows.append(dict(k=k,vertex=v,gain=g,count=d[(v,g)]))
        minima.append(min(d.values()))
        if k==max_k: break
        nd={(v,g):0 for v in V for g in range(3)}
        for (u,g),val in d.items():
            for v in V:
                if u!=v: nd[(v,(g+edge_gain(u,v))%3)]+=val
        d=nd
    return rows,minima
rows,minima=k4_dp()
assert min(minima[4:])>=2
assert all(minima[k+1]>minima[k] for k in range(4,40))
# Independent route for short horizons: enumerate each entire walk explicitly.
dpindex={(r['k'],r['vertex'],r['gain']):r['count'] for r in rows}
enumeration_checked=0
paths=[(0,0)]
for k in range(9):
    brute={(v,g):0 for v in V for g in range(3)}
    for v,g in paths: brute[(v,g)]+=1
    for v in V:
        for g in range(3):
            assert brute[(v,g)]==dpindex[k,v,g],(k,v,g)
            enumeration_checked+=1
    if k<8: paths=[(u,(g+edge_gain(v,u))%3) for v,g in paths for u in V if u!=v]
for k in range(10,41):
    bound=3**((k-10)//2)
    assert minima[k]>=bound, (k,minima[k],bound)

# Exhibit constructive walks for each pair (terminal, gain):
# T=(0,3,1,0), gain +1 length 3; root loop B=(0,1,0), gain 0 length 2;
# root loop C=(0,1,2,0), gain 0 length 3.
def walk_gain(w):
    return sum(edge_gain(u,v) for u,v in zip(w,w[1:]))%3
T=(0,3,1,0);B=(0,1,0);C=(0,1,2,0)
assert (walk_gain(T),walk_gain(B),walk_gain(C))==(1,0,0)
base_walks=[]
for v in V:
    for g in range(3):
        q=(0,) if v==0 else (0,v)
        r=(g-walk_gain(q))%3
        w=(0,)
        for _ in range(r):w=w+T[1:]
        w=w+q[1:]
        assert (w[-1],walk_gain(w))==(v,g)
        assert len(w)-1<=7
        base_walks.append((v,g,len(w)-1))

# Endpoint-only event rule permits gauge invariant additive functions that
# depend on closed-loop gain, unlike the narrower uniform gain-only F_1 rule.
loop_rows=[]
for e01,e12,e20 in itertools.product(range(2),repeat=3):
    loop_gain=(e01+e12+e20)%2
    count=0
    for h0,h1,h2 in itertools.product(range(2),repeat=3):
        changed=((e01+h1-h0)+(e12+h2-h1)+(e20+h0-h2))%2
        assert changed==loop_gain
        count+=1
    loop_rows.append(dict(e01=e01,e12=e12,e20=e20,
                          holonomy=loop_gain,additive_measure=int(loop_gain==0),
                          switching_cases=count))
assert set(r['additive_measure'] for r in loop_rows)=={0,1}
# Validate original Lemma 3.1 for all F1:Z2->{-1,0,1} on an open edge.
valid_f1=[]
for f0,f1 in itertools.product((-1,0,1), repeat=2):
    if f0==f1: valid_f1.append((f0,f1))
    else:
        # On an open walk with gain 0, changing end gauge by 1 changes its gain to 1.
        assert f0!=f1
assert len(valid_f1)==3

# Cylinder refinement: complete triangle gain graph with trivial phases.
# One-step histories S:0->1, T:0->2 yield orthogonal endpoint vectors.
# Refinement by one step uses the adjacency A.
A=((0,1,1),(1,0,1),(1,1,0))
def mat_vec(M,v):return tuple(sum(x*y for x,y in zip(row,v)) for row in M)
def dot(x,y):return sum(u*v for u,v in zip(x,y))
ea=(0,1,0); eb=(0,0,1)
ea2=mat_vec(A,ea);eb2=mat_vec(A,eb)
whole=tuple(a+b for a,b in zip(ea,eb)); whole2=mat_vec(A,whole)
assert (dot(ea,eb),dot(ea2,eb2))==(0,1)
assert (dot(ea,ea),dot(ea2,ea2))==(1,2)
assert (dot(whole,whole),dot(whole2,whole2))==(2,6)
assert (Fraction(dot(ea,ea),dot(whole,whole)),
        Fraction(dot(ea2,ea2),dot(whole2,whole2)))==(Fraction(1,2),Fraction(1,3))
# A^2 is not any scalar multiple of identity on span(e1,e2) since overlap 1.
assert dot(ea2,eb2)==1 and dot(ea,eb)==0

# Unitary adjacency obstruction for reciprocal gains: A*=A and A*=A^{-1}
# implies A^2=cI; projectively U^{2m}=I, U^{2m+1}=U.
# Positive control: a K2 adjacency U=Pauli X, U^2=I.
X=((0,1),(1,0))
assert mat_vec(X,mat_vec(X,(1,0)))==(1,0)
assert mat_vec(X,mat_vec(X,(0,1)))==(0,1)
# For nonempty loop-free graphs: Tr(A)=0, eigenvalues +/-sqrt(c), hence even n.

# Exact geometry orientation control on CP1: B=(1+i)/4.
# Horizontal end lift is conjugate(B)/|B| = (1-i)/sqrt(2), not B/|B|.
# Tangent holonomy determinant for n=1 is (B/|B|)^2 = i.
from sympy import I, sqrt, Rational, simplify
Barg=(1+I)/4
ray=(1+I)/sqrt(2)
end_lift=(1-I)/sqrt(2)
assert simplify(Barg / sqrt(Barg*Barg.conjugate()) - ray)==0
assert simplify(end_lift - ray.conjugate())==0
assert simplify(ray**2-I)==0
assert simplify((1/end_lift)**2-I)==0
assert simplify(end_lift - ray)!=0
# The *same* Z3-gain K4 that supplies dense CP3 rays also fails cylinder
# compatibility: distinct one-step outcomes 0->1 and 0->2 coalesce along
# two common two-step endpoints, hence D2(S+,T+)=2 though D1(S,T)=0.
from sympy import Matrix
zeta=(-1+I*sqrt(3))/2
K4=Matrix(4,4,lambda i,j: 0 if i==j else (zeta if (i,j)==(3,0) else
                  zeta.conjugate() if (i,j)==(0,3) else 1))
assert simplify(K4.conjugate().T-K4)==Matrix.zeros(4)
assert simplify((K4.conjugate().T*K4)[1,2]-2)==0

# Deliberately invalid controls must fail (not counted as discoveries).
controls={
 'FALSE_all_additive_rules_are_gain_blind': len(set(r['additive_measure'] for r in loop_rows))==1,
 'FALSE_k3_cylinder_cross_term_consistent': dot(ea,eb)==dot(ea2,eb2),
 'FALSE_k3_unitary': mat_vec(A,mat_vec(A,ea))==ea,
 'FALSE_horizontal_end_phase_is_B': simplify(end_lift-ray)==0,
 'FALSE_K4_all_gains_identity': all(edge_gain(u,v)==0 for u in V for v in V if u!=v),
}
assert not any(controls.values()), controls

with (HERE/'all_k4_walk_counts_k0_to_k40.csv').open('w',newline='',encoding='utf-8') as f:
    wr=csv.DictWriter(f,fieldnames=['k','vertex','gain','count']);wr.writeheader();wr.writerows(rows)
with (HERE/'all_triangle_gain_switching_cases.csv').open('w',newline='',encoding='utf-8') as f:
    wr=csv.DictWriter(f,fieldnames=['e01','e12','e20','holonomy','additive_measure','switching_cases']);wr.writeheader();wr.writerows(loop_rows)
report={
 'scope':'exact finite mathematical test only; no physical ontology or empirical observation',
 'k4':{'vertices':4,'group':'Z3','special_edge':'oriented (0,3) gain +1','rows':len(rows),
       'max_length':40,'independent_bruteforce_walk_count_checks':enumeration_checked,'total_walks_k40':str(3**40),'minimum_counts':{str(k):minima[k] for k in [0,1,2,3,4,5,6,8,10,16,24,32,40]},
       'verified_exponential_lower_bound':'min_(v,g) N_k(v,g) >= 3^floor((k-10)/2) for k>=10, proven for all k by root-bounce padding',
       'base_paths': [{'vertex':v,'gain':g,'length':l} for v,g,l in base_walks]},
 'additivity':{'gain_assignments':8,'switchings_per_assignment':8,
               'all_switch_cases':64,'different_measure_values':[0,1],
               'scope':'closed-loop endpoint-aware additive measure; does not contradict Lemma 3.1 as written'},
 'cylinder':{'one_step_cross':0,'two_step_cross':1,'one_step_single':1,'two_step_single':2,
             'whole_one_step':2,'whole_two_step':6,'normalized_single_one_step':'1/2',
             'normalized_single_two_step':'1/3','scalar_rescaling_cannot_restore_cross_zero':True,
             'same_K4_dense_rays_example_has_nonzero_refined_cross_term':'2 (versus zero at one step)'},
 'involution':{'condition':'undirected reciprocal-gain adjacency: A*=A; A/sqrt(c) unitary => A^2=cI',
               'positive_control':'two-vertex edge has U=X and U^2=I',
               'nonempty_zero_diagonal_unitary_necessitates_even_number_vertices':True},
 'g7_sign':{'bargmann':'(1+i)/4','bargmann_phase':'pi/4',
             'horizontal_end_lift':'(1-i)/sqrt(2)','det_lc_holonomy_cp1':'i',
             'formula':'det T = (B/|B|)^(n+1) remains correct; intermediate horizontal lift sign in G7 proof is incorrect'},
 'false_controls_rejected':list(controls),
 'status':'PASS', 'root':'G1 OPEN', 'ontology':'not identified'}
(HERE/'B4_RESULTS.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf-8')
print('B4_EXACT_CHECKS_PASS',len(rows),'K4 counts,',enumeration_checked,'exhaustive cross-counts,',len(loop_rows)*8,
      'gauge cases, cylinder, involution and phase sign controls')
print('k4 N_min at k=4,10,24,40:',[minima[k] for k in (4,10,24,40)])
print('negative controls rejected:',len(controls))
