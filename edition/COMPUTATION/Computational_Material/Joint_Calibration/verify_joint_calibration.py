#!/usr/bin/env python3
"""Exact finite controls and outward binomial-tail inversion.

No empirical data. Input counts below are illustrative, not observations.
The general coverage and projection statements are proved in the companion study.
Only the declared finite grids are exhaustively checked by this program.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement
from math import comb
from pathlib import Path
import hashlib
import json
import platform
import time

started = time.monotonic()
checks = []


def require(label, condition):
    if not condition:
        raise AssertionError(label)
    checks.append(label)


def cdf(n, k, p):
    """Exact Pr[Binomial(n,p) <= k] using one integer denominator."""
    if k < 0:
        return F(0)
    if k >= n:
        return F(1)
    u, v = p.numerator, p.denominator
    return F(sum(comb(n, j) * u**j * (v-u)**(n-j)
                 for j in range(k+1)), v**n)


def cp_contains(n, k, p, alpha):
    return cdf(n, k, p) >= alpha/2 and 1-cdf(n, k-1, p) >= alpha/2


def root_bracket(n, k, target, steps=40):
    """Enclose the unique decreasing-CDF root on [0,1]."""
    assert 0 <= k < n and 0 < target < 1
    lo, hi = F(0), F(1)
    for _ in range(steps):
        mid = (lo+hi)/2
        value = cdf(n, k, mid)
        if value > target:
            lo = mid
        elif value < target:
            hi = mid
        else:
            lo = hi = mid
            break
    require(f'cdf_root_bracket_n{n}_k{k}_target{target}',
            cdf(n, k, lo) >= target >= cdf(n, k, hi))
    return lo, hi


def cp_outer(n, k, alpha):
    lower = (F(0), F(0)) if k == 0 else root_bracket(n, k-1, 1-alpha/2)
    upper = (F(1), F(1)) if k == n else root_bracket(n, k, alpha/2)
    return (lower[0], upper[1]), (lower, upper)


def projected_interval(ia, ib, iq):
    al, au = ia
    bl, bu = ib
    ql, qu = iq
    if not (0 <= bl <= bu < al <= au <= 1 and 0 <= ql <= qu <= 1):
        raise ValueError('Closed formula requires separated ordered rectangles')
    lower = max(F(0), (ql-bu)/(au-bu))
    upper = min(F(1), (qu-bl)/(al-bl))
    return None if lower > upper else (lower, upper)


def realization(ia, ib, iq, theta):
    al, au = ia
    bl, bu = ib
    qmin, qmax = (1-theta)*bl+theta*al, (1-theta)*bu+theta*au
    q = max(iq[0], qmin)
    if q > min(iq[1], qmax):
        return None
    t = F(0) if qmax == qmin else (q-qmin)/(qmax-qmin)
    a, b = al+t*(au-al), bl+t*(bu-bl)
    assert q == (1-theta)*b+theta*a
    assert al <= a <= au and bl <= b <= bu and iq[0] <= q <= iq[1]
    return a, b, q


grid = [F(i, 4) for i in range(5)]
intervals = list(combinations_with_replacement(grid, 2))
theta_grid = [F(i, 20) for i in range(21)]
projection_cases = 0
realizations = 0
for ia in intervals:
    for ib in intervals:
        if ib[1] >= ia[0]:
            continue
        for iq in intervals:
            result = projected_interval(ia, ib, iq)
            for theta in theta_grid:
                witness = realization(ia, ib, iq, theta)
                member = result is not None and result[0] <= theta <= result[1]
                require(f'projection_{ia}_{ib}_{iq}_{theta}', member == (witness is not None))
                projection_cases += 1
                realizations += witness is not None

ia, ib, iq = (F(4, 5), F(9, 10)), (F(1, 10), F(1, 5)), (F(2, 5), F(9, 20))
require('sharp_rectangular_interval', projected_interval(ia, ib, iq) == (F(2, 7), F(1, 2)))
for theta in (F(2, 7), F(1, 2)):
    require('sharp_endpoint_'+str(theta), realization(ia, ib, iq, theta) is not None)
require('residual_population_width',
        projected_interval(ia, ib, (F(17, 40), F(17, 40))) == (F(9, 28), F(13, 28)))

# Coverage controls: finite p grid, all counts for each n, and exact probabilities.
coverage_rows = []
for alpha in (F(1, 20), F(1, 10), F(1, 60)):
    minimum = F(1)
    for n in range(1, 13):
        for p in [F(i, 20) for i in range(21)]:
            coverage = sum((cdf(n, k, p)-cdf(n, k-1, p))
                           for k in range(n+1) if cp_contains(n, k, p, alpha))
            require(f'cp_coverage_{alpha}_{n}_{p}', coverage >= 1-alpha)
            minimum = min(minimum, coverage)
    coverage_rows.append({'alpha': str(alpha), 'minimum_on_grid': str(minimum),
                          'n_values': [1, 12], 'p_grid': 'i/20, i=0,...,20'})

# A point empirical law with one Bernoulli observation has zero coverage here.
a, b, theta = F(4, 5), F(1, 5), F(1, 2)
q = b+(a-b)*theta
require('adverse_true_law', q == F(1, 2))
bad = []
for k in (0, 1):
    interval = projected_interval((a, a), (b, b), (F(k), F(k)))
    require('zero_radius_empty_'+str(k), interval is None)
    bad.append({'sample_count': k, 'sample_size': 1, 'probability': '1/2',
                'projected_set': 'empty'})

# Positive contrast is a genuine conditioning parameter.
for contrast in [F(1, 2), F(1, 10), F(1, 100), F(1, 1000)]:
    a, b = (1+contrast)/2, (1-contrast)/2
    require('inverse_contrast_'+str(contrast), a-b == contrast)
    require('unit_parameter_gap_'+str(contrast), (a-b)/contrast == 1)
require('zero_contrast_unidentified', all(F(1, 2)+(F(1, 2)-F(1, 2))*t == F(1, 2) for t in theta_grid))

# Illustrative counts; Bonferroni allocation is chosen before examining counts.
alpha = F(1, 20)
counts = {'a': (100, 85), 'b': (100, 15), 'q': (200, 85)}
confidence = {}
for name, (n, k) in counts.items():
    outer, brackets = cp_outer(n, k, alpha/3)
    confidence[name] = {'n': n, 'k': k, 'error_allocation': str(alpha/3),
                        'outer_interval': [str(v) for v in outer],
                        'endpoint_brackets': [[str(v) for v in pair] for pair in brackets],
                        'display': [float(v) for v in outer]}
ci = {name: tuple(F(v) for v in row['outer_interval']) for name, row in confidence.items()}
require('illustrative_intervals_separated', ci['b'][1] < ci['a'][0])
projected = projected_interval(ci['a'], ci['b'], ci['q'])
require('illustrative_projection_nonempty', projected is not None)
for edge in projected:
    require('illustrative_endpoint_'+str(edge), realization(ci['a'], ci['b'], ci['q'], edge) is not None)

def decimal_outward(x, places, upper=False):
    scale = 10**places
    value = x.numerator*scale//x.denominator
    if upper and F(value, scale) < x:
        value += 1
    return f'{value//scale}.{value%scale:0{places}d}'

result = {
    'status': 'PASS', 'finite_predicates': len(checks),
    'projection_grid': {'cases': projection_cases, 'constructed_feasible_witnesses': realizations,
                        'interval_endpoint_grid': 'i/4, i=0,...,4',
                        'theta_grid': 'i/20, i=0,...,20'},
    'sharp_rectangular_example': {'parameter_interval': ['2/7', '1/2'],
                                 'fixed_q_17_40_interval': ['9/28', '13/28']},
    'binomial_coverage_controls': coverage_rows,
    'zero_radius_adverse_control': {'true_a': '4/5', 'true_b': '1/5', 'true_theta': '1/2',
                                    'true_q': '1/2', 'coverage': '0', 'outcomes': bad},
    'illustrative_counts': confidence,
    'projected_confidence_outer_interval': [str(x) for x in projected],
    'projected_confidence_display_outward_6dp': [decimal_outward(projected[0], 6),
                                                decimal_outward(projected[1], 6, True)],
    'root_inversion': {'arithmetic': 'Python arbitrary-precision integers and Fraction',
                       'bisection_steps': 40, 'maximum_endpoint_bracket_width': '1/1099511627776',
                       'checked_semantics': 'Exact binomial tail inequalities bracket each endpoint; outer directions retained.'},
    'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'python': platform.python_version(), 'elapsed_seconds': time.monotonic()-started,
    'limits': ['Counts are stipulated examples, not experimental data.',
               'Finite-grid checks do not prove coverage for all real probabilities; the study supplies that proof.',
               'Bonferroni projection is conservative; no shortest-region or optimality claim.',
               'No claim applies automatically to drift, dependent repetitions, adaptive stopping or unanchored calibration labels.']}
print(json.dumps(result, indent=2, sort_keys=True))
