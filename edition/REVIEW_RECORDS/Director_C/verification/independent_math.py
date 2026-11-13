#!/usr/bin/env python3
"""Independent standard-library verification of scoped unknown-PR-orientation results.
No imported director verification programs. Writes REFERENCE_RESULTS.json next to this script.
Run only in a temporary directory when validating release artifacts.
"""
from collections import Counter
from decimal import Decimal, localcontext
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
import json
PR=[w for w in product((0,1),repeat=4) if sum(w)%2]
assert len(PR)==8

def error_counting(n, prob):
    # For 1 observed context, 4 PR orientations compatible; for 2 contexts, 2;
    # for 3/4 contexts, one. Equal prior minimax via full PR symmetry.
    one=sum(x**n for x in prob)
    two=sum((prob[i]+prob[j])**n-prob[i]**n-prob[j]**n for i,j in combinations(range(4),2))
    return F(3,4)*one+F(1,2)*two

u=[F(1,4)]*4
non=[F(3,10)]*3+[F(1,10)]
for n in range(1,9):
    assert error_counting(n,u)==F(3*(2**n-1),4**n)
assert error_counting(5,u)==F(93,1024)
assert error_counting(6,u)==F(189,4096)
assert error_counting(6,non)==F(74487,1000000)
# independent brute-force check of minimax 6-round result by enumerating contexts
for prob in (u,non):
    risk=F(0)
    for cs in product(range(4),repeat=6):
        k=len(set(cs)); success={1:F(1,4),2:F(1,2),3:F(1),4:F(1)}[k]
        weight=F(1)
        for c in cs: weight*=prob[c]
        risk+=weight*(1-success)
    assert risk==error_counting(6,prob)
# Three *deliberately chosen* distinct training contexts determine an odd PR rule.
for p in PR:
    cands=[r for r in PR if all(r[c]==p[c] for c in (0,1,2))]
    assert cands==[p]
# Two contexts leave exactly two candidates
for p in PR:
    for a,b in combinations(range(4),2):
        assert sum(all(r[c]==p[c] for c in (a,b)) for r in PR)==2
# Local deterministic a=b=0 has even truth word 0000 and differs from g=0001 at context 3.
# Three contexts 0,1,2 appear during 6 training, never 3; then the next 19 also avoid 3.
# Number of onto maps from six ordered positions to 3 contexts: 3^6 - 3*2^6 + 3 = 540.
onto3=3**6-3*2**6+3
assert onto3==540
false_reject_lower=F(onto3,1)*F(3,10)**6*F(9,10)**19
assert false_reject_lower>F(1,20)
# Any *wrong* odd PR rule differs at 2 or 4 contexts; with probabilities (.3,.3,.3,.1)
# minimum mismatch probability is .4, hence test-stage chance of all matching <=.6^19.
train_error=error_counting(6,non)
biased_PR_power_upper=1-train_error+train_error*F(3,5)**19
assert biased_PR_power_upper<F(19,20)
with localcontext() as ctx:
    ctx.prec=65
    q=(Decimal(2)+Decimal(2).sqrt())/Decimal(4)
    assert q**18>Decimal('0.05')>q**19
    assert Decimal(8)*q**33<Decimal('0.05')<Decimal(8)*q**32
    power25=F(3907,4096)+F(189,4096)*F(1,2**19)
    assert power25>F(19,20)
    out={
      'PR_orientations':8,
      'uniform_training_error_5':str(error_counting(5,u)),
      'uniform_training_error_6':str(error_counting(6,u)),
      'uniform_training_success_6':str(1-error_counting(6,u)),
      'nonuniform_setting_probabilities':[str(x) for x in non],
      'nonuniform_training_error_6':str(train_error),
      'nonuniform_training_success_6':str(1-train_error),
      'nonuniform_local_25_round_false_rejection_lower':str(false_reject_lower),
      'nonuniform_local_25_round_false_rejection_lower_decimal':str(Decimal(false_reject_lower.numerator)/Decimal(false_reject_lower.denominator)),
      'nonuniform_25_round_PR_power_upper':str(biased_PR_power_upper),
      'uniform_19_test_quantum_size_bound':str(q**19),
      'uniform_18_test_quantum_size_bound':str(q**18),
      'uniform_25_round_power_ideal_PR':str(power25),
      'uniform_scan_33_quantum_Bonferroni_bound':str(8*q**33),
      'designed_3_plus_19_total_rounds':22,
      'designed_3_plus_19_null_size_upper':str(q**19),
      'designed_3_plus_19_ideal_fixed_PR_power':'1',
      'scope': 'All results describe stipulated probability models and protocols. Physical implementation, measurement independence, no communication and fresh held-out uniform settings are not established.'
    }
path=Path(__file__).with_name('REFERENCE_RESULTS.json')
path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print('INDEPENDENT_ORIENTATION_MATH_PASS',str(train_error),str(false_reject_lower),'22_design')
