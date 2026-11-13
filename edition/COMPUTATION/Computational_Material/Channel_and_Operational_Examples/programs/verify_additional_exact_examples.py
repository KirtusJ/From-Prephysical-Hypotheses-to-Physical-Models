#!/usr/bin/env python3
"""Exact finite checks for capacity recovery and the oriented binomial test.

These checks examine displayed examples. They do not replace the general proofs.
"""
from fractions import Fraction as F
from math import comb
import json

checks=0
def require(condition,description):
    global checks
    checks+=1
    if not condition:raise ArithmeticError(description)
def multiply(a,b):
    return [[sum((x*y for x,y in zip(row,col)),F(0)) for col in zip(*b)] for row in a]
def rational_rows(a):return [[str(x) for x in row] for row in a]

W=[[F(1,2),F(1,2),F(0),F(0)],
   [F(0),F(0),F(1,2),F(1,2)],
   [F(1,2),F(0),F(1,2),F(0)]]
K=[[F(1),F(0)],[F(1),F(0)],[F(0),F(1)],[F(0),F(1)]]
for row in W:
    require(sum(row)==1,'row normalization')
    require(sorted(x for x in row if x)!=[F(1)],'non-deterministic original row')
    require([x for x in row if x]==[F(1,2),F(1,2)],'each row has exactly one bit of entropy')
uniform_output=multiply([[F(1,2),F(1,2),F(0)]],W)[0]
require(uniform_output==[F(1,4)]*4,'capacity-achieving output')
V=multiply(W,K)
require(V==[[F(1),F(0)],[F(0),F(1)],[F(1,2),F(1,2)]],'garbled rows')
L=W[:2]
recovered=multiply(V,L)
require(recovered[:2]==W[:2],'first two rows force recovery law')
require(recovered[2]==[F(1,4)]*4,'forced recovered third row')
require(recovered[2]!=W[2],'recovery contradiction')

def binomial_boundary(n):
    # H0: counted-event probability 1/7; H1: probability 1/5.
    # The likelihood ratio is increasing in the count. Reject above k,
    # and randomize at k to have exact type-I error 1/20.
    d0=7**n;d1=5**n;above0=0;above1=0
    for k in range(n,-1,-1):
        at0=comb(n,k)*6**(n-k);at1=comb(n,k)*4**(n-k)
        if 20*(above0+at0)>=d0:
            randomize=F(d0-20*above0,20*at0)
            size=(F(above0)+randomize*at0)/d0
            power=(F(above1)+randomize*at1)/d1
            require(0<=randomize<=1,'valid randomized test')
            require(size==F(1,20),'exact test size')
            return {'n':n,'critical_count':k,'reject_above_count':k,
                    'randomization_at_count':float(randomize),
                    'randomization_exact':str(randomize),
                    'size_exact':str(size),'power':float(power),
                    'power_exact':str(power),'meets_95_percent':power>=F(19,20)}
        above0+=at0;above1+=at1
    raise ArithmeticError('No critical count found')

tests=[binomial_boundary(467),binomial_boundary(468)]
require(not tests[0]['meets_95_percent'],'467 insufficient')
require(tests[1]['meets_95_percent'],'468 sufficient')
result={'status':'PASS','checks':checks,'arithmetic':'exact integer and rational arithmetic',
        'capacity_example':{'W':rational_rows(W),'K':rational_rows(K),'WK':rational_rows(V),
          'forced_recovery':rational_rows(L),'recovered_third_row':[str(x) for x in recovered[2]],
          'both_capacities_bits':1,'common_recovery_exists':False,
          'capacity_reason':'All original conditional row entropies equal 1, output entropy is at most 2, and an input attains uniform output. The garbled channel has two outputs and contains a noiseless binary subchannel.'},
        'binomial_test':{'null_probability':'1/7','alternative_probability':'1/5','size':'1/20',
          'target_power':'19/20','results':tests,
          'minimality_reason':'For the simple iid hypotheses the randomized upper-count test is most powerful. Maximum power is nondecreasing in sample size because an extra observation may be ignored. The exact checks at 467 and 468 therefore locate the first size reaching 19/20.'},
        'limits':'No physical data. No claim about composite alternatives, adaptive designs, calibration expense or unrestricted channel equivalence.'}
print(json.dumps(result,indent=2))
