#!/usr/bin/env python3
"""Two-coupling feasibility audit for controlled Gamma scale measurements.

No external data files are needed. Uses explicit numerical checks, not Python assert.
"""
import argparse
import json
import math
from fractions import Fraction

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq


def check(condition, reason):
    if not condition:
        raise RuntimeError(reason)


def gamma2_cdf(c, u):
    return 1.0 - (1.0 + 2.0*c*u)*math.exp(-2.0*c*u)


def gamma2_pdf(c, u):
    return 4.0*c*c*u*math.exp(-2.0*c*u)


def quantile(p):
    check(0 < p < 1, "Quantile input outside (0,1)")
    hi = 2.0
    while gamma2_cdf(1, hi) < p:
        hi *= 2.0
    return brentq(lambda u: gamma2_cdf(1, u)-p, 0.0, hi, xtol=1e-14)


def lower(p, c=2.0):
    if p == 0: return 0.0
    if p == 1: return 1.0
    return 1.0 - gamma2_cdf(c, quantile(1.0-p))


def upper(p, c=2.0):
    if p == 0: return 0.0
    if p == 1: return 1.0
    return gamma2_cdf(c, quantile(p))


def mixed_response(c, lambdas, weights, eta):
    out = 0.0
    for lam, pi in zip(lambdas, weights):
        val = quad(lambda u: pi*gamma2_pdf(c*lam, u)*eta(u), 0, np.inf,
                   epsabs=5e-13, epsrel=5e-13, limit=400)[0]
        out += val
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='results.json')
    args = parser.parse_args()

    med = quantile(0.5)
    up = upper(0.5)
    lo = lower(0.5)
    check(abs(gamma2_cdf(1,med)-0.5)<2e-14,'quantile failed')
    check(abs(up+lo-1.0)<2e-14,'ROC complement failed')
    check(abs(upper(0.3)-0.6441356744687458)<2e-12,'ROC bound failed')

    # Independently integrate threshold-response extremizers.
    up_quad = quad(lambda u: gamma2_pdf(2,u), 0, med, epsabs=1e-13)[0]
    lo_quad = quad(lambda u: gamma2_pdf(2,u), med, np.inf, epsabs=1e-13)[0]
    check(abs(up_quad-up)<1e-12 and abs(lo_quad-lo)<1e-12,
          'threshold detector sharpness failed')

    # Hidden mode mixture; common gamma rate multiplier and unchanged detector.
    lambdas = [0.4, 1.8, 7.2]
    weights = [0.24, 0.51, 0.25]
    eta = lambda u: 0.15 + 0.70*(math.sin(3.0*u)**2)*math.exp(-u/5.0)
    p1 = mixed_response(1, lambdas, weights, eta)
    p2 = mixed_response(2, lambdas, weights, eta)
    check(lower(p1)-1e-11 <= p2 <= upper(p1)+1e-11,
          'unknown-mixture data processing bound failed')

    # Context-dependent instrument at couplings 1,2,3.
    p = [Fraction(1,2), Fraction(9,10), Fraction(19,20)]
    determinants = {}
    for tag, vals in [('click',p),('miss',[1-v for v in p])]:
        r0,r1,r2 = vals[0], vals[1]/4, vals[2]/9
        det = r0*r2-r1*r1
        check(det>0 and r1-r2>0 and r0-r1>0, 'moment positivity failed '+tag)
        determinants[tag] = {'hankel_det':str(det), 'r0':str(r0),
                             'r1':str(r1), 'r2':str(r2)}
    check(upper(0.5)<0.9, 'needed ROC counterexample not found')

    # Distribution-free Hoeffding test: 2 settings, independent M repetitions each.
    alpha = 0.05
    M=2500
    e=math.sqrt(math.log(4/alpha)/(2*M))
    margin = 0.95-2*e-upper(0.5+2*e)
    check(margin>0.0024, 'two-setting power certificate failed')

    # All-coupling ambiguity, checked under two explicit physical models.
    k, eta0 = 2.0, 0.6
    # Device A: z=u, coupling-dependent efficiency eta0 * exp(-2 c (k-1)u).
    # Device B: z=u/k, constant efficiency eta0/k^2.
    gap=0.0
    for c in [0.4,1.0,1.8,3.0,7.0]:
        for z in [0.05,0.3,0.9,2.0]:
            a=gamma2_pdf(c,z)*eta0*math.exp(-2*c*(k-1)*z)
            b=gamma2_pdf(c,k*z)*k*eta0/(k*k)
            gap=max(gap,abs(a-b))
    check(gap<2e-15,'all-coupling counterexample failed')

    results = {
      'result_scope': 'conditional synthetic statistical models; no physical measurement or prephysical emergence',
      'median_u_gamma_shape2_rate2':round(med,14),
      'p1_half_sharp_bounds_c2':[round(lo,14),round(up,14)],
      'sharp_upper_p1_0_3':round(upper(0.3),14),
      'threshold_integration_residual':round(max(abs(up_quad-up),abs(lo_quad-lo)),14),
      'stable_unknown_mixture':{'mode_eigenvalues':lambdas,'weights':weights,
         'p1':round(p1,12),'p2':round(p2,12),
         'lower_bound':round(lower(p1),12),'upper_bound':round(upper(p1),12)},
      'three_setting_contextual_example':{
         'probabilities':['1/2','9/10','19/20'],
         'click_and_miss_moment_checks':determinants,
         'p2_minus_roc_upper':round(0.9-up,12)},
      'two_setting_hoeffding':{
        'alpha':alpha,'M_each_coupling':M,'total_preparations':2*M,
        'alternative_p1':0.5,'alternative_p2':0.95,
        'e':round(e,14),'power_certificate_margin':round(margin,14),
        'null_false_rejection_bound':alpha,'alternative_power_lower_bound':1-alpha},
      'session_D_all_coupling_density_max_abs_residual':round(gap,14)
    }
    with open(args.output,'w',encoding='utf-8') as f:
        json.dump(results,f,indent=2,sort_keys=True,ensure_ascii=False)
        f.write('\n')
    print(json.dumps(results,sort_keys=True,indent=2))

if __name__ == '__main__':
    main()
