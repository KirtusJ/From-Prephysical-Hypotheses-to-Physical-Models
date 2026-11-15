"""Bound ideal 804-launch power and check the effect of reusing one timing draw."""
from fractions import Fraction
from math import comb
from pathlib import Path
from runpy import run_path


N = 250_000
SCALE = 1 << 104


def unnormalized_step(rails):
    advanced = [0] * 10
    for site in range(5):
        right, left = rails[2 * site:2 * site + 2]
        advanced[2 * ((site + 1) % 5)] = right + left
        advanced[2 * ((site - 1) % 5) + 1] = right - left
    return advanced


def rejection_probability(p):
    a, denominator = p.as_integer_ratio()
    b = denominator - a
    tail = sum(comb(804, k) * a**k * b**(804-k) for k in range(481, 805))
    boundary = comb(804, 480) * a**480 * b**324
    return Fraction(1024 * tail + 115 * boundary, 1024 * denominator**804)


def main():
    generator = run_path(str(Path(__file__).with_name('check_prelaunch_time_sampling.py')))
    thresholds = generator['make_design'](N)
    rails = [SCALE] + [0] * 9
    positive = total = signed_sum = 0
    for lag, threshold in enumerate(thresholds):
        pairs = N - abs(lag - (N - 1))
        weight = pairs * threshold
        positive += max(0, weight)
        total += abs(weight)
        signed_sum += weight * (2 * rails[0]**2 - SCALE**2)
        # The normalized two-tick step is the integer step squared, divided by two.
        rails = [v // 2 for v in unnormalized_step(unnormalized_step(rails))]

    shared_size = Fraction(positive, total)
    if shared_size != Fraction(85445659438818037790, 170891318864992614874):
        raise ValueError('Shared-setting false-rejection probability differs from the published control')

    # Each division rounds a rail by at most 1/(2*SCALE). Unitarity bounds
    # the accumulated vector error by 2*lag/SCALE. Squaring the port amplitude
    # costs at most three times that error, since the amplitude error is < 1.
    estimate = Fraction(1, 2) + Fraction(signed_sum, 2 * SCALE**2 * total)
    error = Fraction(6 * (len(thresholds) - 1), SCALE)
    lower = Fraction('0.62566370613899')
    upper = Fraction('0.62566370613900')
    if not (lower <= estimate - error and estimate + error <= upper):
        raise ValueError('Ideal success-rate interval is too narrow')
    if not (rejection_probability(lower) >= Fraction('0.950013337855') and
            rejection_probability(upper) <= Fraction('0.950013337856')):
        raise ValueError('Ideal rejection-probability interval is too narrow')
    print('Fresh settings, ideal power in [0.950013337855, 0.950013337856]')
    print('One shared setting, always-click null size =', shared_size)


if __name__ == '__main__':
    main()
