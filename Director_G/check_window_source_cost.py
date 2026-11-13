"""Check finite heralding budgets from the localized signed Hadamard walk."""

import argparse
import json
from fractions import Fraction
from itertools import product
from pathlib import Path


def signed_walk(ticks):
    state = {0: [1, 0]}
    for _ in range(ticks):
        following = {}
        for site, (right, left) in state.items():
            following.setdefault(site + 1, [0, 0])[0] += right + left
            following.setdefault(site - 1, [0, 0])[1] += right - left
        state = following
    return state


def enumerate_words(ticks):
    counts = {}
    for steps in product((1, -1), repeat=ticks):
        sign = 1
        previous = 1
        for step in steps:
            if previous == step == -1:
                sign = -sign
            previous = step
        counts.setdefault(sum(steps), [0, 0])[int(previous == -1)] += sign
    return counts


def window_trial(ticks, low, high, expected_probability, expected_budget):
    state = signed_walk(ticks)
    if ticks == 16:
        assert enumerate_words(ticks) == state
    norm = sum(r*r + l*l for r, l in state.values())
    assert norm == 2**ticks
    rows = [[site, *state.get(site, (0, 0))] for site in range(low, high + 1)]
    mass = sum(r*r + l*l for _, r, l in rows)
    p = Fraction(mass, norm)
    assert p == expected_probability

    # The exact threshold is failure <= 1/20, including equality.
    failure = 1 - p
    trials = 0
    residual = Fraction(1)
    while 20 * residual > 1:
        trials += 1
        residual *= failure
    assert trials == expected_budget
    assert 20 * residual <= 1 < 20 * failure**(trials - 1)
    return dict(ticks=ticks, inclusive_window=[low, high], site_right_left=rows,
                total_raw_score=norm, accepted_raw_score=mass, p=str(p),
                one_trial_failure=str(failure), min_trials_for_95_percent=trials,
                failure_before_threshold=float(failure**(trials - 1)),
                failure_at_threshold=float(residual))


def clock_powers(r):
    tick = 2 + r
    duration = tick - Fraction(14, 5)
    acceptance = Fraction(11, 10)
    return dict(epsilon_power=str(r), tick_power=str(tick),
                one_attempt_duration_power=str(duration),
                mean_serial_time_power=str(duration - acceptance),
                required_lane_growth_power_at_fixed_deadline=str(acceptance - duration))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="directory for window_source_cost.json")
    args = parser.parse_args()
    cases = [window_trial(16, 0, 2, Fraction(1275, 16384), 37),
             window_trial(64, 2, 6, Fraction(282728967155285175, 9223372036854775808), 97)]
    scales = [clock_powers(Fraction(1)), clock_powers(Fraction(9, 10))]
    assert [s['mean_serial_time_power'] for s in scales] == ['-9/10', '-1']
    result = dict(model="Sharp (0,R), unwrapped integer sites, one coherent inclusive yes/no flag. Both rails contribute squared signed counts.",
                  trials="Independent fresh copies, or the same conditional yes probability after every failure. The fractions and minimal budgets are exact. The two failure decimals are display values.",
                  exponent_inputs="T ~ delta^(-14/5), p ~ (2/pi)delta^(11/10), zero overhead; the lane count divided by delta^(-required_lane_growth_power_at_fixed_deadline) must diverge for success tending to one.",
                  exact=cases, ideal_clock_powers=scales)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'window_source_cost.json').write_bytes((json.dumps(result, indent=2) + '\n').encode('utf-8'))


if __name__ == '__main__':
    main()
