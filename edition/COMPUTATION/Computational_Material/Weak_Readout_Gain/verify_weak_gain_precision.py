#!/usr/bin/env python3
"""Finite exact controls for Statistical Precision under Weak Readout Gain.

The program computes mathematical examples, not experimental measurements.
It uses rational arithmetic for probability decisions. Decimal square roots
are labelled displays, not outward-rounded numerical certificates.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
import math
from fractions import Fraction as F
from pathlib import Path


def frac(x):
    return {"numerator": str(x.numerator), "denominator": str(x.denominator)}


def bernoulli_weights(n, p):
    a, b = p.numerator, p.denominator
    den = b**n
    return [F(math.comb(n,k)*a**k*(b-a)**(n-k),den) for k in range(n+1)]


def source_tv(n,t):
    plus=bernoulli_weights(n,(1+t)/2)
    minus=bernoulli_weights(n,(1-t)/2)
    return sum(abs(a-b) for a,b in zip(plus,minus))/2, plus, minus


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path,default=Path(__file__).with_name('Weak_Gain_Precision_Results.json'))
    args=ap.parse_args()
    predicates=[]
    def check(name,condition):
        predicates.append({'predicate':name,'passed':bool(condition)})
        if not condition: raise AssertionError(name)
    rows=[]
    for n,t in itertools.product((1,2,5,20,80,320),(F(1,100),F(1,20),F(1,5),F(1,2))):
        tv,plus,minus=source_tv(n,t)
        lr=sum(plus[k]-minus[k] for k in range(n+1) if 2*k>n)
        symmetric=sum(plus[k] for k in range(n+1) if 2*k>n)-sum(plus[k] for k in range(n+1) if 2*k<n)
        affinity_square=(1-t*t)**n
        tag=f'N={n},t={t}'
        check(tag+':normalized',sum(plus)==sum(minus)==1)
        check(tag+':likelihood_ratio_sign',all((a-b>=0)==(2*k>=n) for k,(a,b) in enumerate(zip(plus,minus))))
        check(tag+':exact_TV_formula',tv==lr==symmetric)
        check(tag+':affinity_inequality',tv*tv<=1-affinity_square)
        check(tag+':sqrt_N_bound_squared',1-affinity_square<=n*t*t)
        check(tag+':coupling_bound',tv<=min(1,n*t))
        if n<=5:
            p=(1+t)/2;q=(1-t)/2
            direct=sum(abs(p**sum(x)*(1-p)**(n-sum(x))-q**sum(x)*(1-q)**(n-sum(x))) for x in itertools.product((0,1),repeat=n))/2
            check(tag+':ordered_sample_TV',direct==tv)
        rows.append({'N':n,'t':str(t),'exact_TV':frac(tv),'affinity_squared':frac(affinity_square),
                     'endpoint_probability_lower_at_alpha_1_20':frac(max(F(0),F(9,10)-tv)),
                     'coupling_probability_lower_at_alpha_1_20':frac(max(F(0),F(9,10)-n*t)),
                     'display_TV':float(tv),'display_affinity_upper':math.sqrt(float(1-affinity_square))})

    # An exact dependence counterexample with identical full reference laws.
    laws=[]
    for target in (0,1):
        law={}
        for z0,z1 in itertools.product((0,1),repeat=2):
            mass=(F(2,5) if z0 else F(3,5))*(F(3,5) if z1 else F(2,5))
            law[(z0 if target==0 else 1-z0,z0,z1)]=mass
        laws.append(law)
    joint_tv=sum(abs(laws[0].get(k,F(0))-laws[1].get(k,F(0))) for k in set(laws[0])|set(laws[1]))/2
    def margin(law,indices):
        result={}
        for key,mass in law.items():
            k=tuple(key[i] for i in indices);result[k]=result.get(k,F(0))+mass
        return result
    check('dependence:reference_laws_equal',margin(laws[0],(1,2))==margin(laws[1],(1,2)))
    check('dependence:source_probabilities',margin(laws[0],(0,))[(1,)]==F(2,5) and margin(laws[1],(0,))[(1,)]==F(3,5))
    check('dependence:joint_TV_one',joint_tv==1)

    # Both orientations can give a disconnected exact projection. The paper
    # supplies a continuum proof; these witnesses are only finite controls.
    witness_rows=[]
    for k in range(31):
        theta=F(k,30)
        if theta<=F(1,3):
            f=F(1,5)-F(3,5)*theta;s=f+F(3,5)
        elif theta>=F(2,3):
            s=F(1,5)-F(3,5)*(1-theta);f=s+F(3,5)
        else:
            check(f'gain_gap:theta={theta}',F(3,5)*theta>F(1,5) and F(3,5)*(1-theta)>F(1,5))
            continue
        check(f'gain_witness:theta={theta}',0<=f<=1 and 0<=s<=1 and abs(s-f)==F(3,5) and (1-theta)*f+theta*s==F(1,5))
        witness_rows.append({'theta':str(theta),'f':str(f),'s':str(s)})

    # Exact necessary sample counts: alpha=1/20, beta=1/10, h=1/5.
    # Threshold is 1-(1-2alpha-beta)^2=9/25. No logarithm is used to decide.
    budgets=[]
    check('exp_5_lower_exceeds_120',sum(F(5**k,math.factorial(k)) for k in range(9))>120)
    for kappa in (F(1,2),F(1,10),F(1,50)):
        h=F(1,5);t=kappa*h;base=1-t*t;threshold=F(9,25)
        lo=0;hi=1
        while base**hi>threshold:hi*=2
        while hi-lo>1:
            mid=(lo+hi)//2
            if base**mid<=threshold:hi=mid
            else:lo=mid
        check(f'necessary_source_budget:kappa={kappa}',base**hi<=threshold and base**(hi-1)>threshold)
        sufficient=math.ceil(40/(t*t))
        check(f'sufficient_upper_budget:kappa={kappa}',F(40,sufficient)<=t*t)
        budgets.append({'kappa':str(kappa),'h':str(h),'necessary_source_count_from_affinity':hi,
                        'conservative_sufficient_count_per_stream':sufficient,
                        'upper_certificate':'log(120)<5, hence 8 log(120)/(kappa*h)^2 < 40/(kappa*h)^2'})
    result={'title':'Finite controls for Statistical Precision under Weak Readout Gain',
            'scope':'Declared finite mathematical checks; no physical observations, independent replication, universal software certification or proof by enumeration.',
            'arithmetic':'Python arbitrary-precision integers and Fraction; displayed floats are not interval enclosures.',
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'design':{'sample_sizes':[1,2,5,20,80,320],'probability_separations':['1/100','1/20','1/5','1/2'],
                      'specified_before_execution':True},
            'TV_cases':rows,'dependence_control':{'full_TV':str(joint_tv),'source_TV':'1/5'},
            'disconnected_projection':{'exact_set':'[0,1/3] union [2/3,1]','witnesses':witness_rows},
            'sample_budget_controls':budgets,'predicates':predicates,'predicate_count':len(predicates),
            'all_passed':all(p['passed'] for p in predicates)}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'output':str(args.output),'predicates':len(predicates),'all_passed':result['all_passed'],'sample_budgets':budgets}))


if __name__=='__main__':main()
