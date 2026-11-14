"""Check the two-sign endpoint designs with integer binomial weights."""

import argparse
from fractions import Fraction as F
from itertools import accumulate, product
import json
from math import comb
from pathlib import Path

from check_tag_endpoint_bounds import identified_interval, observed
from check_tag_shot_budget import POWER, SIZE, binomial_cdf, bounds, require


def binomial_weights(n, last, p):
    """Yield integer binomial masses through last for 0 < p < 1."""
    a, b = p.numerator, p.denominator - p.numerator
    weight = b**n
    yield weight
    for j in range(min(n, last)):
        weight, remainder = divmod(weight * (n - j) * a, (j + 1) * b)
        require(remainder == 0, "integer binomial weight")
        yield weight


def shared_mark_cdf(paired, single, cutoff, p):
    """Lower tail when the first paired marks count twice and the rest count once."""
    double_prefix = list(accumulate(binomial_weights(paired, cutoff // 2, p)))
    total = 0
    for singles, weight in enumerate(binomial_weights(single, cutoff, p)):
        max_double = min(paired, (cutoff - singles) // 2)
        total += weight * double_prefix[max_double]
    return F(total, p.denominator ** (paired + single))


def check_small_paths():
    # Enumerate independent labels in order, then actually read both prefixes.
    p = F(1, 3)
    for plus, minus in product(range(5), repeat=2):
        counts = [F(0)] * (plus + minus + 1)
        for marks in product((0, 1), repeat=max(plus, minus)):
            ones = sum(marks)
            mass = p**ones * (1 - p)**(len(marks) - ones)
            counts[sum(marks[:plus]) + sum(marks[:minus])] += mass
        for cutoff, expected in enumerate(accumulate(counts)):
            require(shared_mark_cdf(min(plus, minus), abs(plus - minus), cutoff, p) == expected,
                    "shared marks against direct enumeration")


def pooled_counterexample(null):
    # N ~ Bin(4000, 1/2) selects plus. N and 4000-N give the same conditional law.
    half = 2000
    included = weighted = F(0)
    for offset in range(181):
        sign_mass = F(comb(2 * half, half + offset) * (2 if offset else 1), 2**(2 * half))
        included += sign_mass
        weighted += sign_mass * shared_mark_cdf(half - offset, 2 * offset, 2263, null)
    # Outside this range bound the conditional tail by zero and one.
    completion = 1 - binomial_cdf(28122, 3999, F(37, 256))
    lower, upper = completion * weighted, completion * (weighted + 1 - included)
    require(F(10350, 100000) < lower <= upper < F(10351, 100000), "pooled false rejection")
    return {
        "pair_rate": "37/256", "right_given_pair": str(null),
        "score_target": 4000, "maximum_ones": 2263, "raw_cap": 28122,
        "largest_sign_count_offset_summed": 180, "omitted_sign_mass": bounds(1 - included),
        "completion": bounds(completion),
        "unconditional_rejection_enclosure": [bounds(lower)[0], bounds(upper)[1]],
    }


def fixed_raw_power(null, rate, p):
    """Enclose the power when every retained score in 32,000 launches is used."""
    raw, first, last = 32000, 4380, 5080
    a, b = rate.numerator, rate.denominator - rate.numerator
    denominator = rate.denominator**raw
    weight = comb(raw, first) * a**first * b**(raw - first)
    k = 2480
    require(binomial_cdf(first, k, null) <= SIZE < binomial_cdf(first, k + 1, null),
            "first conditional cutoff")
    covered = weighted_ticks = 0
    scale = 10**15
    for n in range(first, last + 1):
        # Adding one Bernoulli observation can increase the critical count by at most one.
        if n > first and binomial_cdf(n, k + 1, null) <= SIZE:
            k += 1
        mark_pass = binomial_cdf(n, k, p)
        ticks = mark_pass.numerator * scale // mark_pass.denominator
        weighted_ticks += weight * ticks
        covered += weight
        weight, remainder = divmod(weight * (raw - n) * a, (n + 1) * b)
        require(remainder == 0, "integer retention weight")
    omitted = 1 - F(covered, denominator)
    lower = F(weighted_ticks, denominator * scale)
    upper = F(weighted_ticks + covered, denominator * scale) + omitted
    require(F(95110, 100000) < 2 * lower - 1 <= 2 * upper - 1 < F(95112, 100000),
            "fixed-exposure worst joint power")
    return {
        "raw_launches_per_sign": raw, "total_raw_limit": 2 * raw,
        "inclusive_retained_count_window_summed": [first, last],
        "omitted_retention_mass": bounds(omitted),
        "marginal_pass_enclosure": [bounds(lower)[0], bounds(upper)[1]],
        "worst_joint_power_enclosure": [bounds(2 * lower - 1)[0], bounds(2 * upper - 1)[1]],
    }


def calculate():
    check_small_paths()
    null = F(257, 444)
    log = observed(F(40, 512), F(34, 512), (F(1), F(255, 256), F(255, 256)))
    rate = 1 - log[2]
    _, p = identified_interval(log)
    m, k, budget = 4700, 2664, 33285
    size = binomial_cdf(m, k, null)
    next_size = binomial_cdf(m, k + 1, null)
    require(size <= SIZE < next_size, "largest admissible uncapped marginal cutoff")
    mark_pass = binomial_cdf(m, k, p)

    def power_at(cap):
        completion = 1 - binomial_cdf(cap, m - 1, rate)
        marginal = completion * mark_pass
        return marginal, max(F(0), 2 * marginal - 1)

    marginal, joint = power_at(budget)
    _, previous = power_at(budget - 1)
    require(previous < POWER <= joint, "first common per-sign cap for this target and cutoff")
    return {
        "pooled_test_with_shared_pair_labels": pooled_counterexample(null),
        "conditional_test_at_fixed_raw_exposure": fixed_raw_power(null, rate, p),
        "separate_sign_test": {
            "null_threshold": str(null), "scores_per_sign": m, "maximum_ones_per_sign": k,
            "raw_launches_per_sign": budget, "total_raw_limit": 2 * budget,
            "false_rejection_upper_bound": bounds(size), "next_uncapped_marginal_size": bounds(next_size),
            "example_retention": str(rate), "example_one_given_retention": str(p),
            "example_pass_per_sign": bounds(marginal), "worst_joint_power": bounds(joint),
            "worst_joint_power_one_fewer_per_sign": bounds(previous),
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_directory", type=Path)
    directory = parser.parse_args().output_directory
    directory.mkdir(parents=True, exist_ok=True)
    output = directory / "tag_sign_dependence.json"
    if output.exists():
        parser.exit(2, f"Refusing to overwrite {output}\n")
    result = calculate()
    with output.open("x", encoding="utf-8", newline="\n") as f:
        json.dump(result, f, indent=2, allow_nan=False)
        f.write("\n")


if __name__ == "__main__":
    main()
