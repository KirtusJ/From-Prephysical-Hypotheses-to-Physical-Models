#!/usr/bin/env python3
"""Exact finite-family coverage under estimated binary readout calibration.

Uses only Python standard-library integer/rational arithmetic. Decimal displays
are secondary summaries, never inputs to acceptance or coverage decisions.
This is a constructed sampling experiment, not an empirical device analysis.
"""
from collections import defaultdict
from fractions import Fraction as F
from math import comb
from pathlib import Path
import json

N, M = 80, 4
ALPHA = F(1, 20)
THETAS = tuple(F(k, 6) for k in range(7))
CAL = (F(1, 5), F(1, 2), F(4, 5))
OUT = Path(__file__).resolve().parent / 'results'

def binomial_weights(n, q):
    a, b = q.numerator, q.denominator
    w = tuple(comb(n, k) * a**k * (b-a)**(n-k) for k in range(n+1))
    assert sum(w) == b**n
    return w, b**n

def accepted_counts(n, q, error):
    """Strict tail > error/2; rejection includes equality at the threshold."""
    w, d = binomial_weights(n, q)
    prefix, accepted = 0, []
    for mass in w:
        right = d - prefix
        prefix += mass
        accepted.append(2 * error.denominator * min(prefix, right)
                        > error.numerator * d)
    # Validity for each candidate is proved by tail monotonicity, and checked
    # here at every candidate actually used by this finite experiment.
    rejected_mass = sum(v for v, keep in zip(w, accepted) if not keep)
    assert F(rejected_mass, d) <= error
    return tuple(accepted)

def record(q):
    return {'fraction': str(q), 'decimal': float(q)}

def binary_projection(p, f, s):
    """Exact closed projection, or None; each argument is a [lower,upper] pair."""
    pl, pu = p; fl, fu = f; sl, su = s
    assert all(0 <= lo <= hi <= 1 for lo, hi in (p, f, s))
    lo, hi = F(0), F(1)
    # (sl-fl)*theta <= pu-fl; (fu-su)*theta <= fu-pl.
    for a, b in ((sl-fl, pu-fl), (fu-su, fu-pl)):
        if a > 0:
            hi = min(hi, b/a)
        elif a < 0:
            lo = max(lo, b/a)
        elif b < 0:
            return None
    return (lo, hi) if lo <= hi else None

def projection_checks():
    assert binary_projection((F(1,2),)*2, (F(1,5),)*2, (F(4,5),)*2) == (F(1,2),)*2
    assert binary_projection((F(1,2),)*2, (F(4,5),)*2, (F(1,5),)*2) == (F(1,2),)*2
    assert binary_projection((F(1,2),)*2, (F(1,2),)*2, (F(1,2),)*2) == (F(0),F(1))
    assert binary_projection((F(1,3),)*2, (F(1,2),)*2, (F(1,2),)*2) is None
    assert binary_projection((F(1,2),)*2, (F(1,5),F(3,10)), (F(7,10),F(4,5))) == (F(2,5),F(3,5))
    endpoints = [F(k,4) for k in range(5)]
    intervals = [(a,b) for a in endpoints for b in endpoints if a <= b]
    cases = 0
    for p in intervals:
        for f in intervals:
            for s in intervals:
                ans = binary_projection(p,f,s)
                # Independent existence check at rational theta probes: the
                # continuous image of a rectangle is its endpoint interval.
                for t in THETAS:
                    exists = max(p[0], (1-t)*f[0]+t*s[0]) <= min(p[1], (1-t)*f[1]+t*s[1])
                    included = ans is not None and ans[0] <= t <= ans[1]
                    assert exists == included
                cases += 1
    return cases

def run():
    projection_cases = projection_checks()
    models, identified = [], defaultdict(int)
    for j,t in enumerate(THETAS):
        for f in CAL:
            for s in CAL:
                p = (1-t)*f+t*s
                models.append((j,p,f,s))
                identified[(p,f,s)] |= 1 << j
    assert len(models) == 63 and len(identified) == 45
    jp = {p: accepted_counts(N,p,ALPHA/3) for _,p,_,_ in models}
    jr = {q: accepted_counts(M,q,ALPHA/3) for q in CAL}
    plug_ps = {(1-t)*F(a,M)+t*F(b,M) for t in THETAS
               for a in range(M+1) for b in range(M+1)}
    pp = {p: accepted_counts(N,p,ALPHA) for p in plug_ps}
    kp = {p: accepted_counts(N,p,ALPHA) for _,p,_,_ in models}
    joint, plugin = {}, {}
    for a in range(M+1):
        for b in range(M+1):
            for k in range(N+1):
                joint[(k,a,b)] = sum(1 << j for j,t in enumerate(THETAS)
                    if any(jj == j and jp[p][k] and jr[f][a] and jr[s][b]
                           for jj,p,f,s in models))
                plugin[(k,a,b)] = sum(1 << j for j,t in enumerate(THETAS)
                    if pp[(1-t)*F(a,M)+t*F(b,M)][k])
    rows = []
    for (p,f,s), target in sorted(identified.items()):
        wp, dp = binomial_weights(N,p)
        wf, df = binomial_weights(M,f)
        ws, ds = binomial_weights(M,s)
        denom = dp*df*ds
        masses = {'joint':0,'plugin':0,'known':0}
        empty = {'joint':0,'plugin':0,'known':0}
        size = {'joint':0,'plugin':0,'known':0}
        point = {name:[0]*len(THETAS) for name in masses}
        law_accept_mass = 0
        for k, pk in enumerate(wp):
            known = sum(1 << j for j,t in enumerate(THETAS)
                        if kp[(1-t)*f+t*s][k])
            for a, fa in enumerate(wf):
                for b, sb in enumerate(ws):
                    weight = pk*fa*sb
                    masks = {'joint':joint[(k,a,b)],'plugin':plugin[(k,a,b)],'known':known}
                    if jp[p][k] and jr[f][a] and jr[s][b]:
                        law_accept_mass += weight
                        assert masks['joint'] & target == target
                    for name, mask in masks.items():
                        if mask & target == target: masses[name] += weight
                        if mask == 0: empty[name] += weight
                        size[name] += mask.bit_count()*weight
                        for j in range(len(THETAS)):
                            if target & (1 << j) and mask & (1 << j): point[name][j] += weight
        actual_law_coverage = F(law_accept_mass,denom)
        independent_product = (sum(F(x,dp) for x,ok in zip(wp,jp[p]) if ok)
            * sum(F(x,df) for x,ok in zip(wf,jr[f]) if ok)
            * sum(F(x,ds) for x,ok in zip(ws,jr[s]) if ok))
        assert actual_law_coverage == independent_product >= 1-ALPHA
        assert F(masses['joint'],denom) >= actual_law_coverage
        assert F(masses['known'],denom) >= 1-ALPHA
        rows.append({'p':str(p),'f':str(f),'s':str(s),
                     'population_identified_set':[str(t) for j,t in enumerate(THETAS) if target & (1<<j)],
                     'whole_set_coverage':{name:record(F(v,denom)) for name,v in masses.items()},
                     'point_coverage':{name:{str(t):record(F(point[name][j],denom)) for j,t in enumerate(THETAS) if target & (1<<j)} for name in masses},
                     'empty_probability':{name:record(F(v,denom)) for name,v in empty.items()},
                     'expected_cardinality':{name:record(F(v,denom)) for name,v in size.items()},
                     'true_joint_law_acceptance':record(actual_law_coverage)})
    summaries = {}
    for name in ('joint','plugin','known'):
        ordered = sorted(rows,key=lambda r:F(r['whole_set_coverage'][name]['fraction']))
        summaries[name] = {'minimum_whole_set_coverage':ordered[0]['whole_set_coverage'][name],
                           'minimizing_laws':[{k:r[k] for k in ('p','f','s','population_identified_set')} for r in ordered if r['whole_set_coverage'][name]['fraction']==ordered[0]['whole_set_coverage'][name]['fraction']],
                           'laws_below_nominal':sum(F(r['whole_set_coverage'][name]['fraction']) < 1-ALPHA for r in rows),
                           'minimum_point_coverage':record(min(F(v['fraction']) for r in rows for v in r['point_coverage'][name].values()))}
    result = {'experiment':{'source_n':N,'reference_n_each':M,'alpha':str(ALPHA),
                           'theta_grid':[str(t) for t in THETAS],'reference_grid':[str(q) for q in CAL],
                           'parameter_points':len(models),'distinct_observable_laws':len(rows),
                           'count_triples_per_law':(N+1)*(M+1)**2,
                           'probability_method':'Exact integer binomial weights; rational final probabilities; no simulation.',
                           'joint_rule':'Keep a full parameter triple iff each inclusive tail is > alpha/6. Project onto theta.',
                           'plug_in_rule':'Treat reference fractions as exact; keep theta iff both source tails are > alpha/2.',
                           'known_rule':'Use actual fixed reference probabilities; keep theta iff both source tails are > alpha/2.',
                           'scope':'One fixed sample size, declared 63-point parameter family (45 laws), stipulated independent streams; no observed physical data.'},
              'checks':{'projection_rectangles':projection_cases,'theta_probes_each':len(THETAS),
                        'normalization':'Exact for every generated binomial mass function',
                        'coverage_identity':'Integer enumeration equals factorized true-law admission probability for all 45 laws',
                        'whole_set_inclusion':'Checked at every accepted true-law count triple',
                        'known_calibration_control':'Whole-set coverage >= 19/20 for every law'},
              'summary':summaries,'rows':rows}
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'joint_calibration_results.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'summary':summaries,'checks':result['checks']},indent=2))

if __name__ == '__main__':
    run()
