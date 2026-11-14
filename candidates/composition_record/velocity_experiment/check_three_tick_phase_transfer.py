"""Replay three physical shifts and certify a mixed-sign, positive-power rival.

Run python -I -B check_three_tick_phase_transfer.py. No external dependencies.
"""

from collections import defaultdict
from fractions import Fraction as F
from itertools import product
from math import isqrt


def require(condition, message):
    if not condition:
        raise ValueError(message)


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def multiply(a, b):
    return a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def scale(a, sign):
    return sign * a[0], sign * a[1]


def norm(a):
    return a[0]**2 + a[1]**2


def outputs(splitter, payload):
    """Two Gaussian integer coefficients per rail/site: idle and addressed.
    Common outer denominators are omitted; the science H coefficient multiplies
    the signed phase divided by sqrt(2). Calibration uses the phase directly.
    """
    zero = (0, 0)
    table = defaultdict(lambda: [zero, zero])
    for first, second, last in product(range(2), repeat=3):
        x1 = 1 - 2 * first
        addressed = x1 == -1
        if not addressed or payload == "minus-X":
            if second == first:
                continue
            coin = -1 if addressed else 1
        else:
            coin = -1 if first == second == 1 else 1
        x3 = (x1 + 1 - 2 * second + 1 - 2 * last) % 8
        # The final transpose entry (last, second) equals U[second, last].
        amplitude = scale(multiply(splitter[first][0], splitter[second][last]), coin)
        cell = table[x3, last]
        index = int(addressed)
        cell[index] = add(cell[index], amplitude)
    return dict(table)


def check_paths():
    zero = (0, 0)
    splitters = (
        (((3, 0), (4, 0)), ((4, 0), (-3, 0))),
        (((3, 0), (4, 0)), ((0, 4), (0, -3))),
    )
    # A third matrix is built explicitly below from independent row/column
    # phases on the real 5-12-13 reflection; all entries have scale 325.
    core = ((5, 12), (12, -5))
    rows, cols = ((3, 4), (4, -3)), ((5, 0), (0, 5))
    phased = tuple(tuple(scale(multiply(rows[i], cols[j]), core[i][j])
                         for j in range(2)) for i in range(2))
    for matrix in (*splitters, phased):
        (a, b), (c, d) = matrix
        column_inner = add(multiply((a[0], -a[1]), b), multiply((c[0], -c[1]), d))
        require(column_inner == zero and norm(a) + norm(c) == norm(b) + norm(d),
                "outer columns are not scaled orthonormal")
        ac, ad, bc, cd = multiply(a, c), multiply(a, d), multiply(b, c), multiply(c, d)
        require(norm(ac) == norm(cd) > 0, "full-support comparator")
        require(outputs(matrix, "H") == {
            (1, 0): [ac, ac], (5, 1): [zero, scale(cd, -1)],
            (7, 1): [ad, bc], (7, 0): [zero, scale(multiply(c, c), -1)],
        }, "science physical output paths")
        require(outputs(matrix, "minus-X") == {
            (1, 0): [ac, scale(ac, -1)], (7, 1): [ad, scale(bc, -1)],
        }, "calibration physical output paths")
    print("Three physical ticks: all science and calibration path coefficients agree.")


def sqrt_floor(x, scale_factor=10**9):
    return F(isqrt(x.numerator * scale_factor**2 // x.denominator), scale_factor)


def bounds_on_scores(sign, power):
    """Positive rational intervals on each escorted 3-4-5 site probability."""
    unit = F(1, 10**9)
    r = sqrt_floor(F(2))
    p1 = sorted(((216 + sign * 144 * r) / 625, (216 + sign * 144 * (r + unit)) / 625))
    p3 = F(72, 625)
    raw = [p1, (1 - p3 - p1[1], 1 - p3 - p1[0]), (p3, p3)]
    if power == 2:
        vals = [(lo**2, hi**2) for lo, hi in raw]
    else:
        require(power == F(1, 2), "unsupported test power")
        vals = [(sqrt_floor(lo), sqrt_floor(hi) + unit) for lo, hi in raw]
    low_sum, high_sum = map(sum, zip(*vals))
    return [(lo / high_sum, hi / low_sum) for lo, hi in vals], raw


def mix(a, b, v):
    return tuple((1 - v) * x + v * y for x, y in zip(a, b))


def check_counterfeit():
    """First fix the sign frequency, then mix powers to match code 3."""
    power_half = F(1, 2)
    low, target = bounds_on_scores(1, power_half)
    low_minus, _ = bounds_on_scores(-1, power_half)
    high, _ = bounds_on_scores(1, 2)
    high_minus, _ = bounds_on_scores(-1, 2)
    for v in (F(0), F(1, 20)):
        l1, l3 = (mix(low[i], low_minus[i], v) for i in (0, 2))
        h1, h3 = (mix(high[i], high_minus[i], v) for i in (0, 2))
        t3 = target[2][0]
        require(h3[1] < t3 < l3[0], "no strict interpolation at code 3")
        # The same strict bracketing holds throughout the interval by affinity.
        weight_lo = (t3 - h3[1]) / (l3[1] - h3[0])
        weight_hi = (t3 - h3[0]) / (l3[0] - h3[1])
        require(0 < weight_lo <= weight_hi < 1, "invalid averaging weights")
        lo = weight_lo * l1[0] + (1 - weight_hi) * h1[0] - target[0][1]
        hi = weight_hi * l1[1] + (1 - weight_lo) * h1[1] - target[0][0]
        bracket = (F(28, 1000), F(30, 1000)) if v == 0 else (-F(3, 1000), -F(2, 1000))
        require(bracket[0] < lo <= hi < bracket[1], "code 1 residual lost its certified sign")
        print(f"Conjugate fraction {v}: code 1 residual lies in {bracket}.")


if __name__ == "__main__":
    check_paths()
    check_counterfeit()
