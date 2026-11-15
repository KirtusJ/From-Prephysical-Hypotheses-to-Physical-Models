"""Exact finite bounds on recovering a Bell pair from a compressed position record.

The decoder may also know the final site. Run python -I -B check_record_messages.py.
"""
from fractions import Fraction
from itertools import product
from math import lcm, prod
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def mul(z, w):
    a, b = z
    c, d = w
    return a*c - b*d, a*d + b*c


def read_steps():
    checker = run_path(str(Path(__file__).with_name("check_position_memory.py")))
    steps = []
    for (a, b), (c, d) in checker["scalar_kraus"]():
        sign = 1 if a*d - b*c > 0 else -1
        require((b, d) == (-sign*c, sign*a), "O(2) coordinate")
        steps.append((a, c, sign))
    return steps


def frequency_steps(steps, common, frequency):
    """Integer numerators for w exp(i n theta)/128, denominator 128*common."""
    weighted = []
    for a, c, sign in steps:
        w = a*a + c*c
        square = mul((a, c), (a, c))
        if frequency == 0:
            value, scale = (w, 0), common
        elif frequency == 2:
            value, scale = square, common
        elif frequency == 4:
            value, scale = mul(square, square), common//w
        else:
            raise ValueError(frequency)
        weighted.append((value[0]*scale, value[1]*scale, sign))
    return weighted


def advance(current, increments):
    updated = {}
    for (site, sign), (u, v) in current.items():
        for j, (a, b, left_sign) in enumerate(increments):
            key = (site+j) % 8, left_sign*sign
            x, y = mul((a, b), (u, left_sign*v))
            old_x, old_y = updated.get(key, (0, 0))
            updated[key] = old_x+x, old_y+y
    return updated


def bounds(moments, denominator):
    """Upper bound for any two messages and lower bound for the specified three."""
    mass, second, fourth = moments
    upper_two = 0
    extra_three = 0
    for site in range(8):
        upper_at_site = []
        for sign in (1, -1):
            key = site, sign
            w, imaginary_mass = mass[key]
            x, y = second[key]
            require(imaginary_mass == 0 and x*x+y*y <= w*w, "moment normalization")
            # Two times the largest eigenvalue of the subnormalized Choi matrix.
            # abs(x)+abs(y) upper bounds the magnitude of its harmonic.
            upper_at_site.append(w + abs(x) + abs(y))
            if sign == 1:
                extra_three += w + fourth[key][0]
            else:
                extra_three += 2*x
        upper_two += max(upper_at_site)
    require(sum(w for w, _ in mass.values()) == denominator, "incident denominator")
    return min(Fraction(1), Fraction(upper_two, denominator)), (
        Fraction(1, 2) + Fraction(extra_three, 4*denominator))


def direct_score(steps, word):
    phase, sign = (1, 0), 1
    for j in word:
        a, c, left_sign = steps[j]
        phase = mul((a, c), (phase[0], left_sign*phase[1]))
        sign *= left_sign
    a, c = phase
    return a*a, max(a*a, c*c) if sign == 1 else a*a


def main():
    steps = read_steps()
    common = lcm(*(a*a+c*c for a, c, _ in steps))
    harmonics = [frequency_steps(steps, common, n) for n in (0, 2, 4)]
    moments = [{(0, 1): (1, 0)} for _ in harmonics]
    denominator = 1
    for m in range(1, 65):
        moments = [advance(part, inc) for part, inc in zip(moments, harmonics)]
        denominator *= 128*common
        # At one write a site has only one orientation sector.
        for part in moments:
            for key in product(range(8), (1, -1)):
                part.setdefault(key, (0, 0))
        upper_two, lower_three = bounds(moments, denominator)
        if m <= 4:
            scores = [direct_score(steps, w) for w in product(range(8), repeat=m)]
            binary, ternary = (Fraction(sum(col), 128**m) for col in zip(*scores))
            require(binary <= upper_two and lower_three <= ternary, "direct word check")
        if m in (8, 16, 32, 64):
            print(f"{m} writes: two-label upper <= {float(upper_two):.9f} (rounded); "
                  f"three-label lower >= {float(lower_three):.9f} (rounded)")
        if m == 32:
            require(upper_two < Fraction(564, 1000) and lower_three > Fraction(640, 1000),
                    "finite two/three separation")
    # Same terminal site, two equally likely orders, H + one shift reads site 9.
    for word, expected in (((0, 4), 729), ((4, 0), 25)):
        a, c = 1, 0
        for j in word:
            g, h, sign = steps[j]
            a, c = mul((g, h), (a, sign*c))
        weight = prod(steps[j][0]**2 + steps[j][1]**2 for j in word)
        require(Fraction((a+c)**2, 2*weight) == Fraction(expected, 754),
                "ordered native position read")


if __name__ == "__main__":
    main()
