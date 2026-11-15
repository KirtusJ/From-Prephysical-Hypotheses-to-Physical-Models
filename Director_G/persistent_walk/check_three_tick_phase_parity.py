"""Three-tick port amplitudes and finite-decision bounds, using exact arithmetic."""
from fractions import Fraction as F
from itertools import product
from math import ceil, comb, floor


def require(test, description):
    if not test:
        raise ArithmeticError(description)


def final_ports(sites, x, y):
    # Omit one factor 1/sqrt(2) per step. Squared amplitudes have denominator 8.
    r, l = [1] + [0] * (sites - 1), [0] * sites
    for tick in (1, 2, 3):
        r, l = ([r[(j-1) % sites] + l[(j-1) % sites] for j in range(sites)],
                [r[(j+1) % sites] - l[(j+1) % sites] for j in range(sites)])
        if tick == 1:
            for pos, sign in ((1, x), (-1, y)):
                r[pos] *= sign
                l[pos] *= sign
        elif tick == 2:
            r[1:] = [0] * (sites - 1)
            l[1:] = [0] * (sites - 1)
    require(sum(a*a for a in r+l) == 4, 'survival differs from 1/2')
    return r[1], l[-1]


def ideal_power(n):
    return sum(F(comb(n, h), 2**n) * min(1, F(2**h, 20)) for h in range(n+1))


def veto_bound(n, required, laws, extreme):
    # Already reached the event has value one. A negative before it ends the test.
    values = [F(1)] + [F(0)] * required
    for _ in range(n):
        values = [F(1)] + [
            extreme(p * values[k-1] + (1-p-q) * values[k] for p, q in laws)
            for k in range(1, required+1)]
    return values[-1]


def main():
    for sites, x, y in product(range(3, 14), (-1, 1), (-1, 1)):
        require(final_ports(sites, x, y) == (x+y, y-x), 'port sign or position')
    for n, expected in ((12, F(76009, 81920)), (13, F(156047, 163840))):
        power = ideal_power(n)
        require(power == expected, 'ideal power')
        print(f'Ideal cap {n}: exact power {power}, approximately {float(power):.12f}')

    for traffic, flag, baseline, actual in product(
            (False, True), (False, True), (-1, 0, 1), (-1, 0, 1)):
        if not traffic and actual != baseline:
            continue
        score = -1 if flag else actual
        require(score <= baseline + 2 * int(traffic and not flag), 'monitor bound')

    drift = F(1, 50)
    null_vertices = [(F(0), F(0)), (F(0), F(1)), (drift, F(0)),
                     ((1 + drift)/2, (1 - drift)/2)]
    min_right, max_wrong = F(498, 1000), F(2, 1000)
    target_vertices = [(min_right, F(0)), (min_right, max_wrong),
                       (1-max_wrong, max_wrong), (F(1), F(0))]
    size = veto_bound(17, 5, null_vertices, max)
    power = veto_bound(17, 5, target_vertices, min)
    require(size < F(1,20) and power > F(19,20), 'seventeen-launch decision')
    print(f'Monitored cap 17: size <= {ceil(size * 10**12) / 10**12:.12f}, power >= {floor(power * 10**12) / 10**12:.12f}')
    pooled_size = drift + (1 - drift) / 2**5
    pooled_power = (1 + F(1,20))/2
    require(pooled_size == F(81, 1600) and pooled_size > F(1,20), 'clustered errors')
    print(f'Run-wide leak: size {pooled_size}; run-wide shutter: power {pooled_power}')


if __name__ == '__main__':
    main()
