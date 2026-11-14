"""Bounds on four-state average survival for the measured twelve-tick walk.

Run python -I -B check_four_state_alphabet.py. All conclusions use rational
comparisons. The four inputs are equiprobable X/Z eigenstates. The encoder
knows the recorded path. Decoders may depend on the final site and label,
and act before the trusted matching-basis measurement.
"""

from collections import defaultdict
from fractions import Fraction
from itertools import product
from math import gcd, isqrt, lcm
from pathlib import Path
from runpy import run_path


record = run_path(str(Path(__file__).with_name("check_record_messages.py")))
advance = record["advance"]
multiply = record["mul"]
require = record["require"]


def harmonic_steps(steps, k):
    """Integer-valued transition for exp(2ik theta) and its denominator."""
    weights = [a*a + c*c for a, c, _ in steps]
    power = max(0, k-1)
    common = lcm(*(w**power for w in weights))
    transitions = []
    for (a, c, sign), w in zip(steps, weights):
        z = (1, 0)
        for _ in range(2*k):
            z = multiply(z, (a, c))
        scale = common * (w if k == 0 else 1) // w**power
        transitions.append((scale*z[0], scale*z[1], sign))
    return transitions, 128*common


def bounds(moment, denominator):
    def magnitude(k, cell):
        x, y = moment[k].get(cell, (0, 0))
        square = x*x + y*y
        floor = isqrt(square)
        return Fraction(floor + (floor*floor < square), denominator[k])

    def cosine(k):
        return Fraction(sum(x for x, _ in moment[k].values()), denominator[k])

    require(cosine(0) == 1, "total incident probability")

    # On a matching determinant sector a planar orthogonal correction gives
    # excess survival cos(2 theta - phase)/2; on the other sector it gives 0.
    # max(x1,x2,x3) <= sum_i max(xi,0) also holds when all terms are negative.
    # Positive part = (x+|x|)/2. An arbitrary real planar contraction is in
    # conv O(2), so allowing arbitrary CPTP maps cannot enlarge this bound.
    # The majorant for |cos t| has coefficients (71,42,-6,1)/108 at
    # harmonics (0,2,4,6). 108 times its surplus at u=|cos t| factors as
    # (2u-1)^2 (u-1)^2 (8u^2+24u+22). Bound each shifted harmonic by its norm.
    def single_line(cell):
        return (71*magnitude(0, cell) + 108*magnitude(1, cell)
                + 42*magnitude(2, cell) + 6*magnitude(4, cell)
                + magnitude(6, cell)) / 108

    best_lines = sum(max(single_line((s, 1)), single_line((s, -1))) for s in range(8))
    three_upper = min(1, Fraction(1, 2) + Fraction(3, 4)*best_lines)

    # I,J for rotations and Z,X for reflections give exactly (1+|cos 2θ|)/2
    # on every path. Either label is valid at a tie. For 0 <= u <= 1,
    # 2u - 3u^2 + u^4 = u(1-u)^2(u+2) >= 0.
    abs_lower = Fraction(9, 16) + cosine(2)/2 - cosine(4)/16
    four_lower = Fraction(1, 2) + abs_lower/2
    return three_upper, four_lower


def direct_pauli(steps, count):
    """Exhaust tiny records with integer path columns, independent of moments."""
    four = three = 0
    for word in product(steps, repeat=count):
        z = (1, 0)
        sign = 1
        for a, c, step_sign in word:
            z = multiply((a, c), (z[0], step_sign*z[1]))
            sign *= step_sign
        a, c = z
        # I,J,Z,X attain the larger squared component in either sector. For
        # I,J,Z, a reflection uses either Z or a mismatched rotation at 1/2.
        four += max(a*a, c*c)
        three += 2*max(a*a, c*c) if sign == 1 else max(2*a*a, a*a+c*c)
    return Fraction(three, 2*128**count), Fraction(four, 128**count)


def exact_four(steps, count):
    """Combine equal projective rail gates. Keep their full incident weights."""
    states = {(1, 0, 1): 1}
    for _ in range(count):
        following = defaultdict(int)
        for (a, c, sign), mass in states.items():
            for g, h, direction in steps:
                u, v = multiply((g, h), (a, direction*c))
                divisor = gcd(u, v)
                if u < 0 or (u == 0 and v < 0):
                    divisor = -divisor
                key = (u//divisor, v//divisor, sign*direction)
                following[key] += mass*(g*g+h*h)
        states = following
    require(sum(states.values()) == 128**count, "all launch weights counted")
    return sum(Fraction(mass*max(a*a, c*c), a*a+c*c)
               for (a, c, _), mass in states.items()) / 128**count


def main():
    steps = record["read_steps"]()
    kernels = {k: harmonic_steps(steps, k) for k in (0, 1, 2, 4, 6)}
    moment = {k: {(0, 1): (1, 0)} for k in kernels}
    denominator = dict.fromkeys(kernels, 1)
    for count in range(1, 81):
        for k, (increments, scale) in kernels.items():
            moment[k] = advance(moment[k], increments)
            denominator[k] *= scale
        if count > 3 and count not in (7, 32, 64, 80):
            continue
        upper, lower = bounds(moment, denominator)
        if count <= 3:
            actual_three, actual_four = direct_pauli(steps, count)
            require(actual_three <= upper and lower <= actual_four, "direct record comparison")
            require(exact_four(steps, count) == actual_four, "gate aggregation vs word tree")
        if count in (7, 32, 64, 80):
            print(f"{count:2} writes: three-label upper {float(upper):.9f}, "
                  f"four-Pauli lower {float(lower):.9f} (rounded)")
        if count == 7:
            actual = exact_four(steps, count)
            require(actual == Fraction(226560354573, 274877906944) and lower <= actual,
                    "four-label average over all seven-write paths")
            print(f"Seven-write exact four-label score {actual}.")
        if count == 80:
            require(upper < Fraction(748, 1000) and lower > Fraction(781, 1000),
                    "finite three/four separation at eighty writes")


if __name__ == "__main__":
    main()
