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


def tilted(q, ratio):
    """Recorded right fraction after multiplying the true odds by the throughput ratio."""
    return ratio * q / (1 - q + ratio * q)


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


def switched_read(right, left, efficiencies, crossed):
    """Physical launch probabilities in counter order (A, B, no named count)."""
    at_a, at_b = (left, right) if crossed else (right, left)
    a = at_a * efficiencies[0]
    b = at_b * efficiencies[1]
    return a, b, 1 - a - b


def detector_exchange(right, left, boundary, label_power):
    total = right + left
    rival = right / total
    efficiencies = (F(1), F(1, 2))
    direct = switched_read(right, left, efficiencies, False)
    crossed = switched_read(right, left, efficiencies, True)
    decoded_right = (direct[0] + crossed[1]) / 2
    decoded_left = (direct[1] + crossed[0]) / 2
    rate = decoded_right + decoded_left
    require(rate == F(111, 1024) and decoded_right / rate == rival, "decoded counter assignments")

    budget = 18089
    timeout = binomial_cdf(budget, HITS - 1, rate)
    power = (1 - timeout) * label_power
    previous_power = (1 - binomial_cdf(budget - 1, HITS - 1, rate)) * label_power
    require(previous_power < POWER <= power, "deadline with unequal counters")

    # Choosing the assignment once per hit weights the two normalized orientations equally.
    direct_control = switched_read(F(3, 4), F(1, 4), efficiencies, False)
    crossed_control = switched_read(F(3, 4), F(1, 4), efficiencies, True)
    held = (direct_control[0] / (1 - direct_control[2]) +
            crossed_control[1] / (1 - crossed_control[2])) / 2
    require(held == F(51, 70) != F(3, 4), "holding the detector assignment through misses")

    # Compare the complete counter log at either orientation for two upstream loss models.
    autonomous_arrivals = F(49, 512) * F(40, 49), F(25, 512)
    rival_arrivals = right, left * F(25, 34)
    require(autonomous_arrivals == rival_arrivals == (F(40, 512), F(25, 512)), "upstream alias")
    for swapped in (False, True):
        require(switched_read(*autonomous_arrivals, efficiencies, swapped) ==
                switched_read(*rival_arrivals, efficiencies, swapped), "switch-resolved counter law")

    critical_squared = (boundary / (1 - boundary)) / (rival / (1 - rival))
    require(critical_squared == F(257, 220), "critical squared throughput bound")
    for kappa in (F(1), F(21, 20), F(27, 25), F(11, 10)):
        lower, upper = tilted(boundary, 1 / kappa), tilted(rival, kappa)
        require((lower > upper) == (kappa**2 < critical_squared), "residual throughput threshold")
        for delta in (F(0), F(1, 10), 1 - boundary):
            observed_mean = (tilted(boundary + delta, 1 / kappa) +
                             tilted(boundary - delta, 1 / kappa)) / 2
            require(observed_mean >= lower, "least favorable null sign fractions")
    return {
        "counter_efficiencies": [str(e) for e in efficiencies],
        "rival_named_hit_per_launch": str(rate),
        "raw_launch_cap": budget,
        "rival_timeout": bounds(timeout),
        "rival_unconditional_power": bounds(power),
        "rival_power_one_fewer_launch": bounds(previous_power),
        "held_assignment_right_at_true_three_quarters": str(held),
        "matched_upstream_arrivals": [str(p) for p in autonomous_arrivals],
        "critical_squared_residual_ratio": str(critical_squared),
    }


def residual_design(boundary, rival):
    """Bound rejection for unequal sign-specific arrival rates under a residual mismatch."""
    kappa, rate_floor = F(21, 20), F(1, 10)
    hits, cutoff, budget = 13300, 7445, 136130
    null_min, rival_max = tilted(boundary, 1 / kappa), tilted(rival, kappa)
    require((null_min, rival_max) == (F(5140, 9067), F(21, 38)), "recorded mean bounds")
    size = binomial_cdf(hits, cutoff, null_min)
    next_size = binomial_cdf(hits, cutoff + 1, null_min)
    mark_power = binomial_cdf(hits, cutoff, rival_max)
    timeout = binomial_cdf(budget, hits - 1, rate_floor)
    power = (1 - timeout) * mark_power
    previous_power = (1 - binomial_cdf(budget - 1, hits - 1, rate_floor)) * mark_power
    require(size <= SIZE < next_size, "residual cutoff boundary")
    require(previous_power < POWER <= power, "residual launch boundary")

    # Show simultaneous attainment with positive effective efficiencies on the rival's two paths.
    right_eff = rate_floor * rival_max / F(40, 512)
    left_eff = rate_floor * (1 - rival_max) / F(34, 512)
    require(0 < left_eff <= right_eff <= 1 and right_eff / left_eff == kappa,
            "feasible equal-rate endpoint")

    # A genuine finite deadline does not justify reusing the old cutoff with this mismatch.
    old_label_tail = binomial_cdf(HITS, CUTOFF, null_min)
    old_reject = old_label_tail * (1 - binomial_cdf(18089, HITS - 1, rate_floor))
    require(old_reject > SIZE, "uncorrected cutoff at the boundary of the probability null")

    # Raw enumeration with a mark above the rival mean limit at one sign and a faster
    # arrival at that sign. Actual completion and the right count can be dependent.
    settings = ((rate_floor, F(1, 2)), (F(1, 5), 2 * rival_max - F(1, 2)))
    reference_finish = 1 - binomial_cdf(4, 1, rate_floor)
    label_tail = binomial_cdf(2, 0, rival_max)
    finish, reject = small_raw_tree(settings, 4, 2, 0)
    require(reference_finish * label_tail <= reject < finish * label_tail,
            "reference waits independent of marks, actual waits dependent")
    _, endpoint = small_raw_tree(((rate_floor, rival_max), (rate_floor, rival_max)), 4, 2, 0)
    require(endpoint == reference_finish * label_tail, "equal rates attain the product")

    # An average of 1/10 across signs allows a strictly smaller completion probability.
    average_only = ((F(19, 200), rival_max), (F(21, 200), rival_max))
    finish, reject = small_raw_tree(average_only, 2, 1, 0)
    proposed_bound = (1 - binomial_cdf(2, 0, rate_floor)) * (1 - rival_max)
    require(finish == F(7599, 40000) and reject == F(129183, 1520000) < proposed_bound == F(17, 200),
            "arithmetic average of hit rates is insufficient")
    return {
        "throughput_ratio_limit": str(kappa),
        "minimum_hit_rate_each_sign": str(rate_floor),
        "recorded_null_minimum": str(null_min),
        "recorded_rival_maximum": str(rival_max),
        "named_hits": hits,
        "maximum_right_to_reject": cutoff,
        "raw_launch_cap": budget,
        "size_upper_bound": bounds(size),
        "uncapped_size_at_cutoff_plus_one": bounds(next_size),
        "rival_uncapped_power_lower_bound": bounds(mark_power),
        "rival_timeout_upper_bound": bounds(timeout),
        "rival_sharp_power_lower_bound": bounds(power),
        "rival_worst_power_one_fewer_launch": bounds(previous_power),
        "endpoint_effective_efficiencies": [str(right_eff), str(left_eff)],
        "old_cutoff_null_rejection_at_18089": bounds(old_reject),
        "average_rate_only_control": {"actual_power": str(reject), "proposed_bound": str(proposed_bound)},
    }


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
        "detector_exchange": detector_exchange(right, left, boundary, label_power),
        "finite_residual_mismatch": residual_design(boundary, rival),
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
