#!/usr/bin/env python3
"""Exact-rational checks of finite-horizon readout identifiability.

Responsible researcher: Kirtus Justus. Mathematical/computational assistance: ChatGPT (OpenAI).
No original verifier is imported. No experimental claims.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import math
import mpmath as mp

HERE=Path(__file__).resolve().parent
WORDS=list(product((0,1), repeat=4))
s=F(131,320)
t=F(37,100)
r=F(1,16)
e=F(1,100)
m=s+(1-2*s)*e
v=(1-r)*(1-2*e)
A=t**4*v**4/4

def requirement(flag,message):
    if not flag:
        raise RuntimeError(message)

def pbern(word,p):
    val=F(1)
    for bit in word:
        val *=p if bit else (1-p)
    return val

def sign_product(word):
    out=1
    for bit in word:
        out *= (2*bit-1)
    return out

# The target observation law, independently defined.
Q={y:pbern(y,m)-A*sign_product(y) for y in WORDS}
requirement(all(z>0 for z in Q.values()) and sum(Q.values())==1,'target not a probability law')
prefixes=list(product((0,1),repeat=3))
pref={w:Q[w+(0,)]+Q[w+(1,)] for w in prefixes}
D={w:Q[w+(1,)]-s*pref[w] for w in prefixes}
L=sum(abs(z) for z in D.values())
formula=8*A-(m-s)*(2*m-1)**3
requirement(L==formula,'closed form causal-freshness deficit failed')
ff={w:(1 if D[w]>0 else -1) for w in prefixes}
req_p111=abs(Q[(1,1,1,1)]/pref[(1,1,1)]-s)

# Read in the supplied exact positive coupling certificate.
with (HERE/'TRANSPORT_CERTIFICATE.json').open(encoding='utf-8') as f:
    cert=json.load(f)
requirement(len(cert['entries'])==36,'wrong number of positive transport entries')
T={(tuple(int(c) for c in a['ideal_word']),tuple(int(c) for c in a['reported_word'])):F(a['joint_mass']) for a in cert['entries']}
requirement(len(T)==36 and all(z>0 for z in T.values()),'transport invalid or duplicated')
requirement(sum(T.values())==1,'transport not normalized')
for z in WORDS:
    requirement(sum(T.get((z,y),F(0)) for y in WORDS)==pbern(z,s),f'ideal marginal for {z}')
for y in WORDS:
    requirement(sum(T.get((z,y),F(0)) for z in WORDS)==Q[y],f'reported marginal for {y}')
for i in range(4):
    for bit in (0,1):
        error_mass=sum(prob for (z,y),prob in T.items() if z[i]==bit and y[i]!=z[i])
        requirement(error_mass==e*(s if bit else 1-s),f'conditional bit-flip rate i={i}, bit={bit}')

# Data-processing triangle: L <= Pr(Y4 != Z4) + TV((W,Z4),W x Bern(s)).
last_error=sum(prob for (z,y),prob in T.items() if z[3]!=y[3])
eta=F(0)
signed_future=F(0);signed_report=F(0)
for w in prefixes:
    joint_z1=sum(prob for (z,y),prob in T.items() if y[:3]==w and z[3]==1)
    eta+=abs(joint_z1-s*pref[w])
    signed_future+=ff[w]*(joint_z1-s*pref[w])
    signed_report+=ff[w]*D[w]
requirement(signed_report==L,'observed signed witness is not TV optimum')
requirement(last_error==e,'last-bit error mismatch')
requirement(eta==L-e,'rational certificate does not saturate causal tradeoff')
requirement(signed_future==eta,'future witness not sharp')
requirement(signed_report-signed_future==e,'report-error contribution not sharp')

# A lower bound on mutual information when Z4's marginal is Bern(s).
requirement(sum(prob for (z,y),prob in T.items() if z[3]==1)==s,'ideal last-bit marginal wrong')
minimum_information=2*float(eta)**2

# Recompute the 8,982-record exponential test at high precision.
mp.mp.dps=75
sm=mp.mpf(s.numerator)/s.denominator
cm=mp.mpf('-0.001827')
N=8982
W={y:mp.fprod([mp.mpf(bit)-sm for bit in y]) for y in WORDS}
null_lambda=mp.mpf('0.3653')
alt_lambda=mp.mpf('0.4412')
max_null=mp.mpf(0)
for mask in WORDS:
    bound=mp.fsum(
        mp.fprod([sm if (y[i]^mask[i]) else (1-sm) for i in range(4)])
        *mp.exp(null_lambda*(cm-W[y]))
        for y in WORDS
    )
    max_null=max(max_null,bound)
alt_bound=mp.fsum(
    (mp.mpf(Q[y].numerator)/Q[y].denominator)*mp.exp(alt_lambda*(W[y]-cm))
    for y in WORDS
)
requirement(max_null**N<mp.mpf('0.05'),'source null bound does not pass')
requirement(alt_bound**N<mp.mpf('0.05'),'source alternative miss bound does not pass')

def number(x,prec=17):
    return format(float(x),f'.{prec}g')

result={
  'date_vancouver':'2026-11-07',
  'responsible_researcher':'Kirtus Justus',
  'status':'Exact rational model and numerical verification only; no apparatus observations',
  'ideal_probability_s':str(s),
  'observed_probability_m':str(m),
  'correlation_amplitude_A':str(A),
  'target_probability_min':str(min(Q.values())),
  'causal_freshness_total_variation':{'fraction':str(L),'decimal':number(L)},
  'exact_transport_certificate':{
    'positive_entries':len(T),
    'per_true_bit_flip_rate':str(e),
    'last_bit_error':str(last_error),
    'prefix_future_dependence_total_variation':str(eta),
    'prefix_future_dependence_decimal':number(eta),
    'triangle_bound_saturated':True,
    'mutual_information_lower_bound_nats':number(minimum_information),
    'all_ideal_and_reported_marginals_exact':True,
    'all_eight_conditional_flip_constraints_exact':True,
  },
  'rare_prefix_111':{
    'probability':number(pref[(1,1,1)]),
    'conditional_reported_one':number(Q[(1,1,1,1)]/pref[(1,1,1)]),
    'conditional_gap_from_fresh_s':number(req_p111),
    'minimum_freshness_gap_if_history_conditional_report_error_at_most_0_01':number(req_p111-e)
  },
  'source_exponential_test':{
    'records':N,
    'upper_false_rejection_probability':mp.nstr(max_null**N,20),
    'upper_missed_detection_probability':mp.nstr(alt_bound**N,20),
    'lambdas':{'null':'0.3653','alternative':'0.4412'},
    'threshold':'-0.001827'
  }
}
(HERE/'RESULTS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
print('exact rational coupling VERIFIED; total-variation tradeoff saturated')
print('TV=',number(L),'last error=',number(e),'minimum future dependence=',number(eta))
print('source exponential test bounds:',mp.nstr(max_null**N,16),mp.nstr(alt_bound**N,16))
