"""Analyze the phase interaction in three consecutive three-tick site records."""
import argparse
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path


SETTINGS = set(itertools.product(("R", "L"), ("S", "Sdg"), ("S", "Sdg")))
EVENTS = ("same_outer_sign", "same_outer_sign_first_edge", "same_outer_sign_middle_edge")


def object_with_unique_keys(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError(f"duplicate JSON key {key}")
        obj[key] = value
    return obj


def integer(value):
    if type(value) is not int or value < 0:
        raise ValueError("counts and attempted launches must be nonnegative integers")
    return value


def displacements(word):
    if len(word) != 6 or any(c not in "01" for c in word):
        raise ValueError(f"expected one six-bit result, received {word!r}")
    value = int(word, 2)
    previous = 0
    result = []
    for offset in (0, 2, 4):
        position = (value >> offset) & 3
        left_steps = (position - previous) % 4
        result.append(3 - 2 * left_steps)
        previous = position
    return result


def summarize(data, alpha):
    if data["schema"] != "velocity-history-counts-v1":
        raise ValueError("unrecognized recording schema")
    provenance = data["provenance"]
    if provenance not in ("ideal", "simulator", "hardware"):
        raise ValueError("declare ideal, simulator or hardware provenance")
    seen = set()
    intervals = {label: [Fraction(0), Fraction(0)] for label in EVENTS}
    rows = []
    error_sum = Fraction(0)
    for arm in data["arms"]:
        setting = tuple(arm[key] for key in ("source", "phase1", "phase2"))
        if setting not in SETTINGS or setting in seen:
            raise ValueError(f"unexpected or duplicate arm {setting}")
        seen.add(setting)
        n = integer(arm["attempts"])
        if n == 0:
            raise ValueError(f"no attempts in {setting}")
        counts = arm["counts"]
        hits = [0, 0, 0]
        recorded = 0
        for word, count in counts.items():
            count = integer(count)
            first, middle, last = displacements(word)
            recorded += count
            if first * last > 0:
                hits[0] += count
                if abs(first) == 3:
                    hits[1] += count
                if abs(middle) == 3:
                    hits[2] += count
        missing = n - recorded
        if missing < 0:
            raise ValueError(f"more reports than attempts in {setting}")

        # Difference of phase-product groups, averaging the four strata in each.
        weight = Fraction(1 if setting[1] != setting[2] else -1, 4)
        for label, hit in zip(EVENTS, hits):
            ends = (weight * hit / n, weight * (hit + missing) / n)
            intervals[label][0] += min(ends)
            intervals[label][1] += max(ends)
        error_sum += weight**2 / n
        rows.append({"setting": setting, "attempts": n, "recorded": recorded,
                     "missing": missing, "events": dict(zip(EVENTS, hits))})
    if seen != SETTINGS:
        raise ValueError(f"missing arms: {sorted(SETTINGS - seen)}")

    # Equal-arm weighting is intentional even when the shot counts differ.
    # The three events reuse shots. A union bound permits their joint use.
    radius = math.sqrt(float(error_sum) * math.log(2 * len(EVENTS) / alpha) / 2)
    comparisons = {}
    for name, (lo, hi) in intervals.items():
        row = {"possible_sample_contrast": [str(lo), str(hi)]}
        if provenance != "ideal":
            row["simultaneous_interval_assuming_independent_shots"] = [
                max(-1.0, float(lo) - radius), min(1.0, float(hi) + radius)
            ]
        comparisons[name] = row
    return {"provenance": provenance, "confidence_level_if_sampled": (
            None if provenance == "ideal" else 1-alpha),
            "definition": "opposite phases minus equal phases, both source rails equally weighted",
            "comparisons": comparisons, "arms": sorted(rows, key=lambda row: row["setting"])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("histograms", type=Path)
    parser.add_argument("--alpha", type=float, default=0.05)
    args = parser.parse_args()
    if not 0 < args.alpha < 1:
        parser.error("--alpha must lie strictly between zero and one")
    data = json.loads(args.histograms.read_bytes(), object_pairs_hook=object_with_unique_keys)
    print(json.dumps(summarize(data, args.alpha), indent=2))


if __name__ == "__main__":
    main()
