"""Finite-test bounds under independent loss/reset and an affine detector.

Python 3.9+ standard library. Keep check_shorter_return.py from research
commit f9da544f6b438fca30b195854f47a7f480ee0630 alongside this file.
Both regular and optimized Python retain every numerical check.
"""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import importlib.util

N0 = 250_000
R = 37_000
SURVIVAL_FLOOR = F(2_499_999, 2_500_000)
CONTRAST_FLOOR = F(891, 1000)
SCALE = 10**60


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def power_interval(value, exponent):
    """Signed endpoints are integer multiples of 1/SCALE; value is nonnegative."""
    lo = value.numerator * SCALE // value.denominator
    hi = -((-value.numerator * SCALE) // value.denominator)
    acc_lo = acc_hi = SCALE
    while exponent:
        if exponent % 2:
            acc_lo = acc_lo * lo // SCALE
            acc_hi = -((-acc_hi * hi) // SCALE)
        lo, hi = lo * lo // SCALE, -((-hi * hi) // SCALE)
        exponent //= 2
    return F(acc_lo, SCALE), F(acc_hi, SCALE)


def verify_design(n, launches, threshold, attenuation_floor, mean_floor):
    r = SURVIVAL_FLOOR
    x = r**2
    _, x_n_upper = power_interval(x, n)
    geometric_mean_lower = (1 - x_n_upper) / (n * (1 - x))
    attenuation_lower = geometric_mean_lower**2
    require(attenuation_lower > attenuation_floor, "attenuation lower bound")

    # These uniform penalties cover independent loss and reset, including either pure case.
    nonresonant = F(23, 25) * (2 / (n * r * F(23, 100)))**2
    reset = F(2, 10) * (2 / (n * r * F(3, 5)))**2
    offset = F(1, 2) * (2 / (n * F(3, 5)))**2
    alternative = CONTRAST_FLOOR * F(2, 25) * attenuation_lower
    alternative -= nonresonant + reset + offset
    require(alternative > mean_floor, "alternative lower bound")
    null = F(1, 2) * F(2 * R, n)**2
    require(null < threshold < mean_floor, "threshold separation")

    variance = (1 + F(2, n)**2) / 8
    margin = min(threshold - null, mean_floor - threshold)
    exponent = launches * margin**2 / (2 * (variance + margin / 3))
    # A positive finite exponential series certifies exp(exponent)>20.
    require(sum(exponent**k / factorial(k) for k in range(15)) > 20,
            "five-percent error bound")
    lo, hi = power_interval(r, 4 * (n - 1))
    print(f"N={n}, launches={launches}, threshold={threshold}, max tick={4*(n-1)}")
    print(f"  null <= {null}, signal > {mean_floor}, schedule survival > {attenuation_floor}")
    micro_lower = lo * 10**6 // 1
    micro_upper = -((-hi * 10**6) // 1)
    print(f"  worst-time survival at r0 in [{micro_lower}, {micro_upper}] / 10^6")
    print(f"  Bernstein exponent >= {exponent}, each error < 1/20")


def run():
    original = Path(__file__).with_name("check_shorter_return.py")
    module_spec = importlib.util.spec_from_file_location("shorter", original)
    shorter = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(shorter)
    shorter.frequency_checks()
    require(shorter.RESOLVENT_BOUND == R and shorter.STATE_CAP == 55,
            "prior resolvent certificate")
    print("Prior 55-state packing, nonresonant frequencies and second harmonic verified.")
    verify_design(N0, 14_100, F(5118, 100000), F(8214641, 10**7), F(585539, 10**7))
    verify_design(450_000, 2_400, F(319, 10000), F(7052443, 10**7), F(502698, 10**7))


if __name__ == "__main__":
    run()
