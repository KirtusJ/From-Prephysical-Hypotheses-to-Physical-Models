"""Verify the finite launch design in Tag_sector_controls.md with integer arithmetic.

Run python -B check_tag_shot_budget.py OUTPUT_DIRECTORY.
"""

import argparse
from fractions import Fraction as F
import json
from math import comb
from pathlib import Path


HITS, CUTOFF, LAUNCHES = 1839, 1029, 13549
SIZE, POWER = F(1, 20), F(19, 20)


def require(condition, description):
    if not condition:
        raise ValueError(description)


def binomial_cdf(n, k, p):
    """Sum integer binomial weights over 0 through k, with one common denominator."""
    if k < 0:
        return F(0)
    if k >= n or p == 0:
        return F(1)
    if p == 1:
        return F(0)
    a, d = p.numerator, p.denominator
    b = d - a
    weight = total = b**n
    for j in range(k):
        weight, rem = divmod(weight * (n - j) * a, (j + 1) * b)
        require(rem == 0, "binomial weight must be integral")
        total += weight
    return F(total, d**n)


def small_raw_tree(settings, launches, hits, cutoff):
    """Enumerate fresh raw launches, retaining the sign on every unnamed outcome."""
    complete = reject = F(0)

    def visit(left, needed, rights, sign, mass):
        nonlocal complete, reject
        if needed == 0:
            complete += mass
            if rights <= cutoff:
                reject += mass
            return
        if left == 0:
            return
        r, q = settings[sign]
        visit(left - 1, needed, rights, sign, mass * (1 - r))
        for next_sign in range(2):
            visit(left - 1, needed - 1, rights + 1, next_sign, mass * r * q / 2)
            visit(left - 1, needed - 1, rights, next_sign, mass * r * (1 - q) / 2)

    for sign in range(2):
        visit(launches, hits, 0, sign, F(1, 2))
    return complete, reject


def bounds(x):
    """Enclose a rational between consecutive multiples of 10^-12 (or exactly)."""
    scale = 10**12
    lo, rem = divmod(x.numerator * scale, x.denominator)

    def decimal(ticks):
        whole, tail = divmod(ticks, scale)
        return f"{whole}.{tail:012d}"

    return [decimal(lo), decimal(lo + int(rem != 0))]


def calculate():
    depth = 6
    pure = F(1, 2) + F(depth, depth**2 + 1)
    boundary = pure - F(6, 2 * depth**2)
    right, left = F(40, 512), F(34, 512)
    pair = right + left
    rival = right / pair
    require((pure, boundary, rival, pair) == (F(49, 74), F(257, 444), F(20, 37), F(37, 256)),
            "tick-nine model inputs")

    for p in (F(0), F(1, 3), F(3, 5), F(1)):
        for n in range(7):
            for k in range(-1, n + 2):
                direct = sum(comb(n, j) * p**j * (1 - p)**(n - j)
                             for j in range(min(k, n) + 1))
                require(binomial_cdf(n, k, p) == direct, "small binomial sum")
    for b in range(1, 5):
        for k in range(3):
            finish, reject = small_raw_tree(((pair, rival), (pair, rival)), b, 2, k)
            require(finish == 1 - binomial_cdf(b, 1, pair), "small deadline")
            require(reject == finish * binomial_cdf(2, k, rival), "last launch included")

    size = binomial_cdf(HITS, CUTOFF, boundary)
    next_size = binomial_cdf(HITS, CUTOFF + 1, boundary)
    label_power = binomial_cdf(HITS, CUTOFF, rival)
    timeout = binomial_cdf(LAUNCHES, HITS - 1, pair)
    power = (1 - timeout) * label_power
    previous_power = (1 - binomial_cdf(LAUNCHES - 1, HITS - 1, pair)) * label_power
    require(size <= SIZE < next_size, "null cutoff boundary")
    require(previous_power < POWER <= power, "raw launch boundary")

    # A linear response on the tested segment, with unequal arrival rates under the null.
    r_plus, r_minus = F(1, 4), F(1, 32)
    q_plus, q_minus = pure - F(1, depth), pure + F(1, depth)
    mean = (q_plus + q_minus) / 2
    pooled = (r_plus * q_plus + r_minus * q_minus) / (r_plus + r_minus)
    raw_rate = (r_plus + r_minus) / 2
    require(mean == pure and pooled == F(532, 999) < boundary, "unequal arrival control")
    finish, reject = small_raw_tree(((r_plus, q_plus), (r_minus, q_minus)), 2, 2, 0)
    require(finish == raw_rate**2 and reject / finish == (1 - pooled)**2,
            "completion selects faster signs")
    require(reject < (1 - mean)**2 < reject / finish, "conditional and unconditional null tails")
    wrong_power = (1 - binomial_cdf(LAUNCHES, HITS - 1, raw_rate)) * binomial_cdf(HITS, CUTOFF, pooled)
    require(wrong_power > F(94, 100), "per-launch sign randomization breaks size control")

    return {
        "design": {
            "named_hits": HITS,
            "maximum_right_to_reject": CUTOFF,
            "raw_launch_cap": LAUNCHES,
            "null_lower_bound": str(boundary),
            "rival_right_given_hit": str(rival),
            "rival_named_hit_per_launch": str(pair),
            "timeout_rejects": False,
        },
        "exact_decimal_enclosures": {
            "size_upper_bound": bounds(size),
            "uncapped_size_at_cutoff_plus_one": bounds(next_size),
            "rival_uncapped_power": bounds(label_power),
            "rival_timeout": bounds(timeout),
            "rival_unconditional_power": bounds(power),
            "rival_power_one_fewer_launch": bounds(previous_power),
        },
        "fresh_sign_each_launch_control": {
            "true_equal_sign_mean": str(mean),
            "pooled_mean": str(pooled),
            "named_hit_per_launch": str(raw_rate),
            "null_rejection_enclosure": bounds(wrong_power),
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_directory", type=Path)
    directory = parser.parse_args().output_directory
    directory.mkdir(parents=True, exist_ok=True)
    output = directory / "tag_shot_budget.json"
    if output.exists():
        parser.exit(2, f"Refusing to overwrite {output}\n")
    result = calculate()
    with output.open("x", encoding="utf-8", newline="\n") as f:
        json.dump(result, f, indent=2, allow_nan=False)
        f.write("\n")


if __name__ == "__main__":
    main()
