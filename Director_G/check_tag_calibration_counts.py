"""Reproduce the prospective two-sign calibration in Tag_sector_controls.md.

Run python -B check_tag_calibration_counts.py OUTPUT_DIRECTORY.
"""

import argparse
from fractions import Fraction as F
import json
from pathlib import Path

from check_tag_shot_budget import (
    RESIDUAL_BUDGET, RESIDUAL_CUTOFF, RESIDUAL_HITS, RESIDUAL_RATE_FLOOR,
    RESIDUAL_RATIO, SIZE, binomial_cdf, bounds, require, tilted,
)


REFERENCE_HITS, REFERENCE_CAP = 30000, 41500
MIN_REFERENCE_RIGHT = 14778
PILOT_LAUNCHES, MIN_PILOT_HITS = 20000, 2071


def at_least(n, hits, p):
    return 1 - binomial_cdf(n, hits - 1, p)


def complete_run(reference_gain, signal_right, signal_left, reference_window, signal_window):
    """Both signs have the same rates here. All five data sets use independent launches."""
    rate = signal_right + signal_left
    reference_finish = at_least(REFERENCE_CAP, REFERENCE_HITS, reference_gain)
    pilot_pass = at_least(PILOT_LAUNCHES, MIN_PILOT_HITS, rate)
    calibration = (reference_finish * reference_window * pilot_pass)**2
    science = at_least(RESIDUAL_BUDGET, RESIDUAL_HITS, rate) * signal_window
    result = {
        "reference_gain": str(reference_gain),
        "signal_named_hit_per_launch": str(rate),
        "reference_completion_each_sign": bounds(reference_finish),
        "reference_label_window_each_sign": bounds(reference_window),
        "pilot_pass_each_sign": bounds(pilot_pass),
        "all_calibrations_pass": bounds(calibration),
        "science_rejection_on_fresh_data": bounds(science),
        "pass_and_reject": bounds(calibration * science),
    }
    return calibration * science, result


def calculate():
    reference_boundary = 1 / (1 + RESIDUAL_RATIO)
    require(reference_boundary == F(20, 41), "fair reference odds")
    ratio_error = at_least(REFERENCE_HITS, MIN_REFERENCE_RIGHT, reference_boundary)
    rate_error = at_least(PILOT_LAUNCHES, MIN_PILOT_HITS, RESIDUAL_RATE_FLOOR)
    require(ratio_error <= SIZE < at_least(REFERENCE_HITS, MIN_REFERENCE_RIGHT - 1, reference_boundary),
            "reference count boundary and its reflection")
    require(rate_error <= SIZE < at_least(PILOT_LAUNCHES, MIN_PILOT_HITS - 1, RESIDUAL_RATE_FLOOR),
            "signal pilot count boundary")
    null_min = tilted(F(257, 444), 1 / RESIDUAL_RATIO)
    science_size = binomial_cdf(RESIDUAL_HITS, RESIDUAL_CUTOFF, null_min)
    worst_size_bound = max(science_size, ratio_error, rate_error)
    require(worst_size_bound == science_size <= SIZE, "unconditional release bound")

    # The symmetric reference has the same binomial probability in both excluded tails.
    reference_window = 1 - 2 * binomial_cdf(REFERENCE_HITS, MIN_REFERENCE_RIGHT - 1, F(1, 2))
    right, left = F(40, 512), F(34, 512)
    signal_window = binomial_cdf(RESIDUAL_HITS, RESIDUAL_CUTOFF, right / (right + left))
    primary_gain = F(3, 4)
    power, interior = complete_run(primary_gain, right * primary_gain, left * primary_gain,
                                   reference_window, signal_window)
    require(power >= F(19, 20), "complete interior experiment reaches 95 percent")

    # Autonomous signals with source-dependent path losses reproduce the full rival law.
    # With ideal physical counters all attenuation can occur before the switch.
    alias_gain = F(25, 34)
    null_right, null_left = F(49, 512) * F(500, 833), F(25, 512)
    require((null_right, null_left) == (right * alias_gain, left * alias_gain),
            "same named signal rates in both worlds")
    require(null_right / (null_right + null_left) == F(20, 37), "same signal label window")
    false_reject, alias = complete_run(alias_gain, null_right, null_left, reference_window, signal_window)
    require(false_reject > F(3, 4), "a source-dependent response breaks the size bound")

    return {
        "per_sign_plan": {
            "reference_hit_target": REFERENCE_HITS, "reference_launch_cap": REFERENCE_CAP,
            "reference_right_inclusive": [MIN_REFERENCE_RIGHT, REFERENCE_HITS - MIN_REFERENCE_RIGHT],
            "signal_pilot_launches": PILOT_LAUNCHES, "minimum_pilot_hits": MIN_PILOT_HITS,
        },
        "maximum_total_launches": 2 * (REFERENCE_CAP + PILOT_LAUNCHES) + RESIDUAL_BUDGET,
        "error_bounds": {
            "one_sided_reference_boundary": bounds(ratio_error),
            "pilot_rate_boundary": bounds(rate_error),
            "unconditional_full_procedure": bounds(worst_size_bound),
        },
        "interior_rival": interior,
        "source_dependent_autonomy_control": alias,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_directory", type=Path)
    directory = parser.parse_args().output_directory
    directory.mkdir(parents=True, exist_ok=True)
    output = directory / "tag_calibration_counts.json"
    if output.exists():
        parser.exit(2, f"Refusing to overwrite {output}\n")
    result = calculate()
    with output.open("x", encoding="utf-8", newline="\n") as f:
        json.dump(result, f, indent=2, allow_nan=False)
        f.write("\n")


if __name__ == "__main__":
    main()
