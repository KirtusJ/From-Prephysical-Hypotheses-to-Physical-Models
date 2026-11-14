"""Bound both tails of a mean endpoint test under arbitrary dependence between signs."""

import argparse
from fractions import Fraction as F
import json
from math import isqrt
from pathlib import Path

from check_tag_endpoint_bounds import identified_interval, observed
from check_tag_shot_budget import POWER, SIZE, binomial_cdf, bounds, require


def chernoff_enclosure(m, count, p):
    """Enclose the Chernoff bound for the combined two-sign count at a strict interior cutoff."""
    x = F(count, 2 * m)
    require(0 < x < 1 and 0 < p < 1, "interior Bernoulli probabilities")
    z = x * (1 - p) / (p * (1 - x))
    squared = (1 - p + p * z)**(2 * m) / z**count
    scale = 10**15
    root = isqrt(squared.numerator * scale**2 // squared.denominator)
    lower, upper = F(root, scale), F(root + 1, scale)
    require(lower**2 <= squared < upper**2, "directed square-root enclosure")
    return lower, upper


def calculate():
    null = F(257, 444)
    right, left = F(40, 512), F(34, 512)
    plus = observed(right, left, (F(1), F(1), F(1)))
    minus = observed(right, left, (F(1), F(185, 204), F(1)))
    rate = 1 - plus[2]
    p_plus, p_minus = identified_interval(plus)[1], identified_interval(minus)[1]
    p = (p_plus + p_minus) / 2
    require((rate, 1 - minus[2]) == (F(37, 256), F(37, 256)), "both retention probabilities")
    require((p_plus, p_minus, p) == (F(20, 37), F(7, 12), F(499, 888)) and
            p_plus < p < null < p_minus and null - p == F(5, 296), "asymmetric score law")

    # At equal marginal parameters identical iid label sequences attain equality
    # in the moment comparison. For two scores at each sign this defeats pooling.
    coupled, independent = (1 - null)**2, (1 - null)**4
    require(independent < SIZE < coupled, "zero-count rejection changes sides of 5 percent")
    require(binomial_cdf(2, 0, null) == coupled and binomial_cdf(4, 0, null) == independent,
            "zero-count binomial controls")

    m, cutoff, raw = 22000, 25096, 155000
    require(p < F(cutoff, 2 * m) < F(cutoff + 1, 2 * m) < null,
            "lower tail under the null and upper tail at the rival")
    size_lo, size_hi = chernoff_enclosure(m, cutoff, null)
    fail_lo, fail_hi = chernoff_enclosure(m, cutoff + 1, p)
    timeout = binomial_cdf(raw, m - 1, rate)
    power = 1 - fail_hi - 2 * timeout
    require(size_hi < SIZE and power > POWER, "unconditional design guarantees")
    return {
        "null_threshold": str(null), "true_pair_right_fraction_at_each_sign": str(right / (right + left)),
        "left_certification": ["1", "185/204"], "outside_certification_at_both_signs": "1",
        "retention_at_both_signs": str(rate), "one_probabilities": [str(p_plus), str(p_minus)],
        "mean_one_probability": str(p), "gap_below_threshold": str(null - p),
        "scores_per_sign": m, "raw_cap_per_sign": raw, "maximum_total_raw": 2 * raw,
        "largest_combined_one_count_to_reject": cutoff,
        "enclosure_of_null_chernoff_bound": [bounds(size_lo)[0], bounds(size_hi)[1]],
        "enclosure_of_rival_chernoff_bound_for_excess_ones": [bounds(fail_lo)[0], bounds(fail_hi)[1]],
        "marginal_rival_timeout": bounds(timeout),
        "unconditional_rival_power_at_least": bounds(power)[0],
        "two_per_sign_zero_ones": {"shared_labels": str(coupled), "independent_labels": str(independent)},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_directory", type=Path)
    directory = parser.parse_args().output_directory
    directory.mkdir(parents=True, exist_ok=True)
    output = directory / "tag_mean.json"
    if output.exists():
        parser.exit(2, f"Refusing to overwrite {output}\n")
    result = calculate()
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write("\n")


if __name__ == "__main__":
    main()
