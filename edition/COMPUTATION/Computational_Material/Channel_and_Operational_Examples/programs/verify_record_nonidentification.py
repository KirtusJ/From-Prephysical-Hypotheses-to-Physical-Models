#!/usr/bin/env python3
"""Exact bounded checks for an analytic nonidentification result.

This is a fresh finite arithmetic check, not empirical data or a universal proof.
All checks remain active under Python optimization. No third-party dependencies.
"""
from fractions import Fraction as F
from itertools import product
import json

checks = []
def check(name, cond):
    if not cond:
        raise RuntimeError(name)
    checks.append(name)

def dot(v,w):
    return sum((a*b for a,b in zip(v,w)),F(0))
def tensor(v,w):
    return [a*b for a in v for b in w]
def det2(a):
    return a[0][0]*a[1][1]-a[0][1]*a[1][0]

def classical_distribution(n,g):
    # Direct enumeration of independent sign flips, separate from the closed form.
    p = [F(0),F(0)]
    for flips in product((0,1), repeat=n):
        weight=F(1)
        for x in flips:
            weight *= (1+g)/2 if x==0 else (1-g)/2
        p[sum(flips)%2] += weight
    return p

for g in (F(0),F(1,5),F(3,5),F(1)):
    for n in range(9):
        p=classical_distribution(n,g)
        check(f'classical_normalization_g{g}_n{n}',sum(p)==1)
        check(f'classical_parity_mean_g{g}_n{n}',p[0]-p[1]==g**n)
        for c in (F(-1),F(-3,5),F(0),F(3,5),F(1)):
            out=p[0]*(1+c)/2+p[1]*(1-c)/2
            check(f'classical_readout_g{g}_n{n}_c{c}',out==(1+g**n*c)/2)
            check(f'classical_probability_g{g}_n{n}_c{c}',0<=out<=1)

# Exact product vs correlated branch construction at gamma=3/5, s=4/5.
g,s=F(3,5),F(4,5)
w=[g,s]
p2=tensor(w,w)
c2=p2[:]; c2[3]=-c2[3]  # CZ_{12}; same environment-only unitary on both branches.
check('product_branch_unit',dot(p2,p2)==1)
check('correlated_branch_unit',dot(c2,c2)==1)
check('same_branch_overlap',p2[0]==c2[0]==g**2)
check('product_schmidt_minor',det2([p2[:2],p2[2:]])==0)
check('correlated_schmidt_minor',det2([c2[:2],c2[2:]])==-F(288,625))

def marginal_first(v):
    half=len(v)//2
    a,b=v[:half],v[half:]
    return [[dot(a,a),dot(a,b)],[dot(b,a),dot(b,b)]]

for n in range(2,7):
    vp,vc=p2[:],c2[:]
    for _ in range(n-2):
        vp=tensor(vp,w); vc=tensor(vc,w)
    rp,rc=marginal_first(vp),marginal_first(vc)
    check(f'unit_product_n{n}',dot(vp,vp)==1)
    check(f'unit_correlated_n{n}',dot(vc,vc)==1)
    check(f'same_global_overlap_n{n}',vp[0]==vc[0]==g**n)
    check(f'product_marginal_pure_n{n}',det2(rp)==0)
    check(f'correlated_marginal_mixed_n{n}',det2(rc)==F(82944,390625))
    pp=(1+2*rp[0][1])/2
    pc=(1+2*rc[0][1])/2
    check(f'product_x_readout_n{n}',pp==F(49,50))
    check(f'correlated_x_readout_n{n}',pc==F(457,1250))
    check(f'positive_intervention_gap_n{n}',pp-pc==F(384,625))

# Positive boundary controls: no entanglement is asserted at gamma=0 or 1.
for g,s in ((F(0),F(1)),(F(1),F(0))):
    v=tensor([g,s],[g,s]); v[3]=-v[3]
    check(f'endpoint_det_g{g}',det2([v[:2],v[2:]])==0)

report={
 'status':'PASS',
 'exact_predicates':len(checks),
 'coverage':{
  'classical_law':'Four gamma values, N=0..8, five rational values of cos(phi); independent path enumeration.',
  'environment_pair':'gamma=3/5; two rational branch vectors; N=2..6 by appending unchanged product fragments.',
  'positive_controls':'gamma=0,1 gives zero entanglement minor.'
 },
 'exact_witness':{
  'gamma':'3/5','product_branch_N2':[str(x) for x in p2],
  'correlated_branch_N2':[str(x) for x in c2],
  'shared_overlap':'9/25','correlated_schmidt_determinant':'-288/625',
  'P_Xplus_product_given_branch1':'49/50',
  'P_Xplus_correlated_given_branch1':'457/1250',
  'difference':'384/625'
 },
 'limits':[
  'Universal N and phase identity follows from the analytic proof, not finite enumeration.',
  'Classical simulator covers the specified final binary output experiment family, not all quantum operations or Bell-local physics.',
  'Environment ambiguity requires environment fragments not to be accessed or recoupled after the common unitary.',
  'The added branch-conditioned X readout assumes independently anchored preparation/conditioning and calibrated local effects.',
  'No physical observations, foundational derivation or novelty priority established.'
 ]
}
print(json.dumps(report,indent=2,sort_keys=True))
