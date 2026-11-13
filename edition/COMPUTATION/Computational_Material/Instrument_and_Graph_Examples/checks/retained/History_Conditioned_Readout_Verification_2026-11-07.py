"""Verification of a supplied four-report probability law.

This program reconstructs formulas from the supplied measurement notes. It is not
an execution of the submitter's original verifier or a hardware simulation.
Core compatibility and TV certificates use exact rational arithmetic. The
binomial-tail check uses 70-digit Decimal arithmetic, not certified intervals.

Research direction and responsibility: Kirtus Justus
mathematical/computational checking: ChatGPT (OpenAI)
2026-11-07, Vancouver, British Columbia, PCT (UTC-07:00).
"""
from __future__ import annotations
from decimal import Decimal, localcontext
from fractions import Fraction as F
from itertools import product
from math import ceil, comb, log


def require(statement, message):
    if not statement:
        raise ArithmeticError(message)


def fmt(value):
    return f"{value} = {float(value):.15f}"


s = F(131, 320)
original_reporting_rate = F(1, 100)
m = s + (1 - 2 * s) * original_reporting_rate
A = (F(37, 100) * F(15, 16) * (1 - 2 * original_reporting_rate)) ** 4 / 4
words = list(product((0, 1), repeat=4))
Q = {w: m ** sum(w) * (1 - m) ** (4 - sum(w)) - (-1) ** sum(w) * A
     for w in words}
require(sum(Q.values()) == 1 and min(Q.values()) > 0, 'Invalid target law')


def outcome_interval(eps):
    return s * (1 - eps), s + (1 - s) * eps


def maximal_score_expectation(scores, lo, hi):
    """Independent dynamic programming over all compatible reporting trees."""
    v = scores.copy()
    for d in range(3, -1, -1):
        for w in product((0, 1), repeat=d):
            zero, one = v[w + (0,)], v[w + (1,)]
            v[w] = max((1 - lo) * zero + lo * one,
                       (1 - hi) * zero + hi * one)
    return v[()]


def target_next_probability(prefix):
    d = len(prefix)
    p0 = sum(Q[w] for w in words if w[:d + 1] == prefix + (0,))
    p1 = sum(Q[w] for w in words if w[:d + 1] == prefix + (1,))
    return p1 / (p0 + p1)


# Exact minimum uniform, history-conditional directional error cap permitting Q.
requirements = []
for d in range(4):
    for w in product((0, 1), repeat=d):
        q = target_next_probability(w)
        up = max(F(0), (q - s) / (1 - s))
        down = max(F(0), (s - q) / s)
        requirements.append((d, w, q, up, down, max(up, down)))
worst = max(requirements, key=lambda x: x[5])
epsilon_full = worst[5]
require((worst[0], worst[1]) == (3, (1, 1, 1)), 'Unexpected critical history')
lo_full, hi_full = outcome_interval(epsilon_full)
require(all(lo_full <= x[2] <= hi_full for x in requirements),
        'Full target not feasible at its predicted compatibility cap')
require(target_next_probability((1, 1, 1)) == lo_full,
        'The critical lower cap is not saturated')

# Exact primal and dual TV equality for a 1%-capped reporting process.
lo, hi = outcome_interval(original_reporting_rate)
odd = {w: F(sum(w) % 2) for w in words}
max_null_odd = maximal_score_expectation(odd, lo, hi)
expected_alt_odd = sum(Q[w] for w in words if sum(w) % 2)
require(max_null_odd == F(66265902529874879, 131072000000000000),
        'Parity null rate mismatch')
require(expected_alt_odd == F(17242828044899517, 32768000000000000),
        'Alternative parity mismatch')

fixed_prefix_tv = F(0)
for w in product((0, 1), repeat=3):
    qprefix = sum(Q[w + (z,)] for z in (0, 1))
    qone = Q[w + (1,)]
    fixed_prefix_tv += max(F(0), lo * qprefix - qone, qone - hi * qprefix)
require(fixed_prefix_tv == F(711463803568579, 32768000000000000),
        'Fixed-prefix distance mismatch')

special = (1, 0, 0, 0)
root_rate = Q[special] / (1 - lo) ** 3
require(lo <= root_rate <= hi, 'Primal root rate infeasible')
R = {(): F(1)}
for d in range(4):
    R_new = {}
    for w, mass in R.items():
        p = root_rate if not w else (hi if sum(w) % 2 == 0 else lo)
        R_new[w + (0,)] = mass * (1 - p)
        R_new[w + (1,)] = mass * p
    R = R_new
require(R[special] == Q[special], 'Special leaf not matched')
TV = sum(abs(Q[w] - R[w]) for w in words) / 2
f = odd.copy()
f[special] = 1 - ((1 - lo - hi) / (1 - lo)) ** 3
require(all(0 <= x <= 1 for x in f.values()), 'Dual score outside [0,1]')
dual = sum(Q[w] * f[w] for w in words) - maximal_score_expectation(f, lo, hi)
require(TV == dual == F(7284851823181053032590319,
                         352902543707699200000000000),
        'Exact dual-primal certificate mismatch')

# Root where a parity-only test loses population discrimination, by bisection.
def parity_ceiling_float(e):
    x = float(s)
    lower, upper = x * (1 - e), x + (1 - x) * e
    t = 1 - lower - upper
    return upper * (1 - t ** 4) / (1 - t)

left, right = 0.0, 1.0
for _ in range(100):
    middle = (left + right) / 2
    if parity_ceiling_float(middle) < float(expected_alt_odd):
        left = middle
    else:
        right = middle
epsilon_parity = (left + right) / 2
require(0.04412165 < epsilon_parity < 0.04412167,
        'Parity compatibility boundary mismatch')


def decimal_fraction(v: F):
    return Decimal(v.numerator) / Decimal(v.denominator)


def decimal_binomial_tail_and_atom(n, k, p):
    """P(K>k) and P(K=k), using forward atom recurrence at 70 digits."""
    pmf = Decimal(comb(n, k)) * p ** k * (1 - p) ** (n - k)
    tail = Decimal(0)
    atom = pmf
    for j in range(k + 1, n + 1):
        atom = atom * (n - j + 1) / j * p / (1 - p)
        tail += atom
    return tail, pmf


def randomized_tail_power(n, k, alpha):
    with localcontext() as ctx:
        ctx.prec = 70
        p0, p1 = decimal_fraction(max_null_odd), decimal_fraction(expected_alt_odd)
        t0, a0 = decimal_binomial_tail_and_atom(n, k, p0)
        t1, a1 = decimal_binomial_tail_and_atom(n, k, p1)
        rho = (Decimal(alpha) - t0) / a0
        require(0 <= rho <= 1, 'Boundary randomization is not admissible')
        return +rho, +(t1 + rho * a1), +(t0 + rho * a0)


checks = ((6342, 3272, '0.05'), (6343, 3272, '0.05'),
          (6757, 3488, '0.04'), (6758, 3489, '0.04'))
powers = []
for n, k, alpha in checks:
    rho, power, size = randomized_tail_power(n, k, alpha)
    powers.append((n, k, alpha, rho, power, size))
require(powers[0][4] < Decimal('0.95') < powers[1][4],
        '5%-size adjacent crossing failed')
require(powers[2][4] < Decimal('0.95') < powers[3][4],
        '4%-size adjacent crossing failed')

# One-sided zero-error Clopper-Pearson allocation (30 directional history cells).
calibration_failure_budget = 0.01
per_cell_budget = calibration_failure_budget / 30
n_zero_errors = ceil(log(per_cell_budget) / log(0.99))
require(n_zero_errors == 797, 'Calibration count mismatch')

print('=== Mathematical compatibility (all rational, except parity root) ===')
print('Alternative odd probability:      ', fmt(expected_alt_odd))
print('Null odd ceiling, 1% cap:        ', fmt(max_null_odd))
print('TV at fixed three-bit marginal: ', fmt(fixed_prefix_tv))
print('TV with all four rates adjustable:', fmt(TV))
print('Primal and dual certificates agree exactly:', TV == dual)
print('Root rate of attaining report law:', fmt(root_rate))
print('Critical history:', worst[1], ' q=', fmt(worst[2]))
print('Minimum cap making full Q feasible:', fmt(epsilon_full))
print(f'Parity-only compatibility threshold: {epsilon_parity:.15f}')
print('Conditionals at last slot (depth3):')
for d, w, q, up, down, need in requirements:
    if d == 3:
        print(' ', ''.join(map(str, w)), f'q={float(q):.12f}, epsilon_needed={float(need):.12f}')
print('=== Independent Decimal binomial power check (not an interval certificate) ===')
for n, k, alpha, rho, power, size in powers:
    print(f'n={n}, alpha={alpha}, boundary k={k}, randomized fraction={rho:.15f}, '
          f'power={power:.15f}, attained size={size:.15f}')
print('Illustrative zero-failure calibration: 30 cells, simultaneous 99% coverage')
print('At least', n_zero_errors, 'zero-error references per cell,',
      30 * n_zero_errors, 'classified cell observations in all.')
print('No claim of stationarity, calibration transport, quantum realization or hardware trials.')
