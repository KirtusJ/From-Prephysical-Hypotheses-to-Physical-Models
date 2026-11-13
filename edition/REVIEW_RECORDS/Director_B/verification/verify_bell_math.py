#!/usr/bin/env python3
"""Independent finite Bell/CHSH controls, exact rational sqrt(2) enclosure, no imports of A/B/C checkers.
Returns JSON to stdout; does not edit source or reference data.
"""
import math,json
from fractions import Fraction as F
from decimal import Decimal as D, localcontext
from math import comb,isqrt
scale=10**45
s_lower=isqrt(2*scale**2)
s_upper=s_lower+1
qlo=F(2*scale+s_lower,4*scale)
qhi=F(2*scale+s_upper,4*scale)
p=F(199,200)
alpha=F(1,20)
power=F(19,20)
assert qlo**2 < F(1,1) and qlo<qhi
assert (s_lower*s_lower<=2*scale**2<(s_lower+1)**2)
def pmf(n,k,x):return F(comb(n,k))*x**k*(1-x)**(n-k)
def tail(n,k,x):return sum((pmf(n,j,x) for j in range(k,n+1)),F(0))
# For exact radical quantum q, use interval checks: bound size by upper qhi, bound attainable power using lower qlo.
assert F(19,20)*qlo**18 > alpha
assert qhi**19 < alpha
assert F(19,20)*F(3,4)**10 > alpha
assert F(3,4)**11 <=alpha

def randomized_bound(n,q):
 for k in range(n+2):
  a=tail(n,k,q)
  if a<=alpha:
   if k==0: return k,F(0),F(1)
   gamma=(alpha-a)/pmf(n,k-1,q)
   power_at_p=tail(n,k,p)+gamma*pmf(n,k-1,p)
   return k,gamma,power_at_p
 raise AssertionError
k27_lo,g27_lo,pw27_at_qlo=randomized_bound(27,qlo)
k27_hi,g27_hi,pw27_at_qhi=randomized_bound(27,qhi)
k28_lo,g28_lo,pw28_at_qlo=randomized_bound(28,qlo)
k28_hi,g28_hi,pw28_at_qhi=randomized_bound(28,qhi)
assert (k27_lo,k27_hi,k28_lo,k28_hi)==(27,27,28,28)
assert max(pw27_at_qlo,pw27_at_qhi)<power
assert min(pw28_at_qlo,pw28_at_qhi)>power
# Exactly 2/3 randomized boundary, and 85/128 with seven fair bits.
def boundary(n,q,g):return q**n+g*F(n)*q**(n-1)*(1-q)
assert boundary(28,qhi,F(2,3))<=alpha
assert boundary(28,p,F(2,3))>=power
assert boundary(28,qhi,F(85,128))<=alpha
assert boundary(28,p,F(85,128))>=power
# Exact certificate for minimal fixed fair-bit count in this boundary randomization family.
for bitcount in range(7):
 for j in range(2**bitcount+1):
  g=F(j,2**bitcount)
  assert boundary(28,p,g)<power or boundary(28,qlo,g)>alpha
# Check threshold 31 for win-count-only deterministic tests.
def first_deterministic(n):
 for k in range(n+2):
  if tail(n,k,qhi)<=alpha:
   return k,tail(n,k,qhi),tail(n,k,p)
 raise AssertionError
min_nonrand=None
for n in range(1,32):
 k,sz,pw=first_deterministic(n)
 if pw>=power:
  min_nonrand=n;break
assert min_nonrand==31 and k==30
# Distinct things: threshold test can be run with memory in both null and alternative using conditional bounds.
with localcontext() as ctx:
 ctx.prec=65
 q=(D(2)+D(2).sqrt())/4
 pd=D(199)/D(200)
 KL=pd*(pd/q).ln()+(1-pd)*((1-pd)/(1-q)).ln()
 gamma_min=(D('0.95')-pd**28)/(D(28)*pd**27*(1-pd))
 gamma_max=(D('0.05')-q**28)/(D(28)*q**27*(1-q))
 out={
 'quantum_q':str(q),
 'quantum_interval_lower':f'{qlo.numerator}/{qlo.denominator}',
 'quantum_interval_upper':f'{qhi.numerator}/{qhi.denominator}',
 'q18':str(q**18),'q19':str(q**19),
 'noisy_p':str(pd),'noisy_all_win_power_19':str(pd**19),
 'randomized_n27_optimal_power_upper':str(D(max(pw27_at_qlo,pw27_at_qhi).numerator)/D(max(pw27_at_qlo,pw27_at_qhi).denominator)),
 'randomized_n28_optimal_power_lower':str(D(min(pw28_at_qlo,pw28_at_qhi).numerator)/D(min(pw28_at_qlo,pw28_at_qhi).denominator)),
 'n28_random_gamma_min_for_power':str(gamma_min),'n28_random_gamma_max_for_size':str(gamma_max),
 'n28_gamma_2_3_size':str(q**28+D(2)/3*D(28)*q**27*(1-q)),
 'n28_gamma_2_3_power':str(pd**28+D(2)/3*D(28)*pd**27*(1-pd)),
 'n28_gamma_85_128_size':str(q**28+D(85)/128*D(28)*q**27*(1-q)),
 'n28_gamma_85_128_power':str(pd**28+D(85)/128*D(28)*pd**27*(1-pd)),
 'nonrandomized_win_count_min':min_nonrand,
 'n31_win_threshold':k,
 'log_eprocess_expected_drift_under_iid_noisy_alternative':str(KL),
 'claimed_conditional_memory_extension':'If P(W_i=1|past)<=q null and P(W_i=1|past)>=p alternative, increasing count rules size<=Bin(n,q) and power>=Bin(n,p); exact iid endpoints included.',
 'anytime_process':'M_n=(p/q)^S_n * ((1-p)/(1-q))^(n-S_n); quantum-null conditional expectation <= previous M. Ville P(sup M_n >=20)<=0.05.',
 'optional_stopping_adverse':'Scanning disjoint 19-round blocks for all wins without correction rejects with probability one under iid quantum endpoint.'
 }
print(json.dumps(out,sort_keys=True,indent=2))
