"""Check signal-only inference from certified left, right, outside and unresolved outcomes.

Run python -B check_tag_endpoint_bounds.py OUTPUT_DIRECTORY.
"""

import argparse
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

from check_tag_shot_budget import POWER, SIZE, binomial_cdf, bounds, require


def observed(right, left, efficiencies):
    """Log probabilities in (certified R, certified L, certified outside, unresolved) order."""
    truth = (right, left, 1 - right - left)
    known = tuple(p * efficiency for p, efficiency in zip(truth, efficiencies))
    return (*known, 1 - sum(known))


def identified_interval(log):
    right, left, outside, unresolved = log
    require(sum(log) == 1 and min(log) >= 0 and outside < 1, "valid log with possible pair")
    return right / (1 - outside), (right + unresolved) / (1 - outside)


def check_extremes():
    # Enumerate all allocations of the missing weight in four-unit observed panels.
    for right, left, outside in product(range(5), repeat=3):
        unresolved = 4 - right - left - outside
        if unresolved < 0 or outside == 4:
            continue
        completions = []
        for missing_right in range(unresolved + 1):
            for missing_left in range(unresolved - missing_right + 1):
                pair = right + left + missing_right + missing_left
                if pair:
                    completions.append(F(right + missing_right, pair))
        log = tuple(F(n, 4) for n in (right, left, outside, unresolved))
        require(identified_interval(log) == (min(completions), max(completions)),
                "attained extremes against all integer completions")


def calculate():
    check_extremes()
    right, left = F(40, 512), F(34, 512)
    outside = 1 - right - left
    null = F(257, 444)
    certification = F(255, 256)
    log = observed(right, left, (F(1), certification, certification))
    rate = 1 - log[2]
    _, upper = identified_interval(log)
    for right_eff in (F(0), F(1, 8), F(1)):
        other_log = observed(right, left, (right_eff, certification, certification))
        require(1 - other_log[2] == rate and identified_interval(other_log)[1] == upper,
                "right certification does not affect the adverse score")
    require((rate, upper) == (F(9691, 65536), F(5356, 9691)), "retention and adverse score")

    hits, cutoff, budget = 4000, 2263, 28122
    size = binomial_cdf(hits, cutoff, null)
    next_size = binomial_cdf(hits, cutoff + 1, null)
    mark_power = binomial_cdf(hits, cutoff, upper)
    timeout = binomial_cdf(budget, hits - 1, rate)
    power = (1 - timeout) * mark_power
    previous = (1 - binomial_cdf(budget - 1, hits - 1, rate)) * mark_power
    require(size <= SIZE < next_size and previous < POWER <= power, "finite test boundaries")

    critical = (1 - null) / (left + (1 - null) * outside)
    at_boundary = observed(right, left, (F(0), critical, critical))
    require(critical == F(2816, 2853) and identified_interval(at_boundary)[1] == null,
            "common certification threshold")
    no_outside = observed(right, left, (F(1), F(1), F(0)))
    require(identified_interval(no_outside)[1] == F(239, 256), "ordinary two-port-only log")
    unclassified_null = null * (right + left) - right
    boundary_right = right + unclassified_null
    boundary_left = left - unclassified_null
    common_log = observed(right, left, (F(1), boundary_left / left, F(1)))
    require(unclassified_null == F(17, 3072) and boundary_right / (right + left) == null and
            common_log == observed(boundary_right, boundary_left, (right / boundary_right, F(1), F(1))),
            "same four records at known pair mass, exactly on the null boundary")

    # Same fixed parent, outside readout and sign in all three models. Move the unavoidable
    # disagreement between named ports into the unresolved category.
    aliases = {}
    for name, other_right, other_left in (("c1", 43, 31), ("sector_autonomy", 49, 25)):
        rival_log = observed(right, left, (F(1), F(other_left, 34), F(1)))
        other_log = observed(F(other_right, 512), F(other_left, 512),
                             (F(40, other_right), F(1), F(1)))
        require(rival_log == other_log and identified_interval(rival_log) ==
                (F(40, 74), F(other_right, 74)), "indistinguishable logs at fixed pair mass")
        aliases[name] = [str(p) for p in other_log]

    return {
        "one_sided_null": str(null),
        "certification_at_rival_example": {"left": str(certification), "outside": str(certification)},
        "common_certification_at_equality": str(critical),
        "retention_probability": str(rate),
        "one_given_retention": str(upper),
        "retained_target": hits, "maximum_ones_to_reject": cutoff, "raw_launch_cap": budget,
        "size_upper_bound": bounds(size), "next_uncapped_size": bounds(next_size),
        "rival_uncapped_power": bounds(mark_power), "rival_timeout": bounds(timeout),
        "rival_unconditional_power": bounds(power), "rival_power_one_fewer_launch": bounds(previous),
        "two_port_only_upper_fraction": "239/256",
        "smallest_unresolved_mass_to_reach_probability_null_at_known_pair_mass": str(unclassified_null),
        "indistinguishable_logs_R_L_outside_unresolved": aliases,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_directory", type=Path)
    directory = parser.parse_args().output_directory
    directory.mkdir(parents=True, exist_ok=True)
    output = directory / "tag_endpoint_bounds.json"
    if output.exists():
        parser.exit(2, f"Refusing to overwrite {output}\n")
    result = calculate()
    with output.open("x", encoding="utf-8", newline="\n") as f:
        json.dump(result, f, indent=2, allow_nan=False)
        f.write("\n")


if __name__ == "__main__":
    main()
