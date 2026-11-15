"""Bound the consequences of one duplicate, a fixed edit budget, and conditional timing faults."""
from fractions import Fraction as F
from pathlib import Path
from runpy import run_path


def sibling(filename):
    return run_path(str(Path(__file__).with_name(filename)))


boundary = sibling("check_one_port_boundary.py")["boundary_probabilities"]


def reject(n, threshold, coin, p):
    tail, point = boundary(n, threshold, p)
    return tail + coin * point


def check_duplicate():
    moments = sibling("check_paired_timing.py")["ideal_pair_moments"]
    lo, hi, second_lo, second_hi = moments()
    lower_weights = (1 - 2*hi + second_lo, 2*(lo - second_hi), second_lo)
    upper_weights = (1 - 2*lo + second_hi, 2*(hi - second_lo), second_hi)
    if min(lower_weights) < 0:
        raise ArithmeticError("negative lower mass")
    coin = F(115, 1024)
    lower = sum(w * reject(802, 480-i, coin, lo) for i, w in enumerate(lower_weights))
    upper = sum(w * reject(802, 480-i, coin, hi) for i, w in enumerate(upper_weights))
    if not F("0.949888445268") < lower <= upper < F("0.949888445270"):
        raise ArithmeticError("one duplicate, ideal power")
    print("802 singles and one duplicated pair, old rule: ideal power in "
          "(0.949888445268, 0.949888445270)")


def check_fault_budgets():
    source = sibling("check_real_readout_bound.py")
    p0, p1 = F("0.547843"), F("0.625662")
    if not (source["NULL_UPPER"] <= p0 < p1 <= source["IDEAL_LOWER"]):
        raise ArithmeticError("rounded fresh endpoints")
    # Increasing decision, pathwise count displacement at most eight.
    size = reject(804, 472-8, F(3, 4), p0)
    miss = 1 - reject(804, 472+8, F(3, 4), p1)
    if not (size < F("0.049329") and miss < F("0.045466")):
        raise ArithmeticError("eight arbitrary score replacements")
    print("Eight edits among 804: false rejection < 0.049329, miss < 0.045466")

    # Fault decided before the current independent draw. Counts are bounded
    # by ordinary binomial tails even when the fault probability depends on history.
    for percent, n, minimum, size_upper, miss_upper in (
            (1, 586, 344, "0.049574", "0.049344"),
            (2, 833, 488, "0.049512", "0.049479"),
            (5, 4609, 2685, "0.049826", "0.049662")):
        rate = F(percent, 100)
        size, _ = boundary(n, minimum-1, p0 + rate*(1-p0))
        power, _ = boundary(n, minimum-1, (1-rate)*p1)
        if size >= F(size_upper) or 1-power >= F(miss_upper):
            raise ArithmeticError(f"{percent}% conditional fault certificate")
        print(f"{percent}% conditional fault: {n} launches, reject >= {minimum}, "
              f"false rejection < {size_upper}, miss < {miss_upper}")


if __name__ == "__main__":
    check_duplicate()
    check_fault_budgets()
