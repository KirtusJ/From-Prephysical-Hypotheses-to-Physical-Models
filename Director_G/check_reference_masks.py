#!/usr/bin/env python3
"""Exact, unconditional port weights for a masked Hadamard walk from (0,R).

All masks retain both incoming directions. Integer amplitudes omit one factor
1/sqrt(2) per step. Squared integer amplitudes therefore have denominator 2**T.
With --sites N the full record uses N sites (default 5). The fixed comparison is
also replayed for every size 3..64. No paths or outputs are read from disk.
"""

import argparse
import itertools
import json
from collections import Counter, defaultdict
from fractions import Fraction


REFERENCE = "RLRL"
POSITIVE_SIGNAL = "LRRL"
NEGATIVE_SIGNAL = "RRLL"
PORT = (0, "L")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def trajectory(word, sites):
    position = 0
    points = []
    for direction in word:
        position = (position + (1 if direction == "R" else -1)) % sites
        points.append(position)
    return tuple(points)


def sign(word):
    incoming = "R" + word
    left_to_left = sum(a == b == "L" for a, b in zip(incoming, word))
    return (-1) ** left_to_left


def masks_for(words, sites):
    paths = [trajectory(word, sites) for word in words]
    return [set(points) for points in zip(*paths)]


def enumerate_words(sites, masks):
    survivors = {}
    summed_amplitudes = Counter()
    counts = Counter()
    for directions in itertools.product("RL", repeat=len(masks)):
        word = "".join(directions)
        path = trajectory(word, sites)
        if any(mask is not None and point not in mask for point, mask in zip(path, masks)):
            continue
        port = (path[-1], word[-1])
        gain = sign(word)
        survivors[word] = {"port": list(port), "gain": gain}
        summed_amplitudes[port] += gain
        counts[port] += 1
    return survivors, summed_amplitudes, counts


def propagate_fields(sites, masks):
    # A normalized Hadamard coin mixes amplitudes; dephased arms add
    # intensities. Their unnormalized counters obey different recurrences.
    amplitudes = {(0, "R"): 1}
    intensities = {(0, "R"): 1}
    per_tick = []
    for tick, mask in enumerate(masks, start=1):
        next_amplitudes = {}
        next_intensities = {}
        for destination in range(sites):
            if mask is not None and destination not in mask:
                continue
            for outgoing, offset, left_sign in (("R", -1, 1), ("L", 1, -1)):
                origin = (destination + offset) % sites
                right = (origin, "R")
                left = (origin, "L")
                port = (destination, outgoing)
                next_amplitudes[port] = amplitudes.get(right, 0) + left_sign * amplitudes.get(left, 0)
                next_intensities[port] = intensities.get(right, 0) + intensities.get(left, 0)
        amplitudes, intensities = next_amplitudes, next_intensities
        denominator = 2 ** tick
        per_tick.append({
            "coherent": str(Fraction(sum(a * a for a in amplitudes.values()), denominator)),
            "fully_dephased": str(Fraction(sum(intensities.values()), denominator)),
        })
    return Counter(amplitudes), Counter(intensities), per_tick


def mixed_port_weight(theta, number_of_words, signed_sum, ticks):
    """A stipulated convex mixture of classical counting and coherent readout."""
    theta = Fraction(theta)
    if not 0 <= theta <= 1:
        raise ValueError("coherence mixture coefficient is outside [0,1]")
    numerator = (1 - theta) * number_of_words + theta * signed_sum ** 2
    return Fraction(numerator, 2 ** ticks)


def check_case(sites, masks, expected_words=None):
    survivors, word_amplitudes, word_counts = enumerate_words(sites, masks)
    field_amplitudes, field_counts, per_tick = propagate_fields(sites, masks)
    if expected_words is not None:
        require(set(survivors) == set(expected_words), f"Unexpected survivors on {sites} sites: {survivors}")
    for port in set(field_amplitudes) | set(word_amplitudes):
        require(field_amplitudes[port] == word_amplitudes[port], f"Amplitude disagreement at {port}")
    for port in set(field_counts) | set(word_counts):
        require(field_counts[port] == word_counts[port], f"Classical intensity disagreement at {port}")
    denominator = 2 ** len(masks)
    mixtures = {}
    for theta in (Fraction(0), Fraction(1, 2), Fraction(1)):
        weight = mixed_port_weight(theta, field_counts[PORT], field_amplitudes[PORT], len(masks))
        mixtures[str(theta)] = str(weight)
    return {
        "mixture_port_weights": mixtures,
        "masks": [sorted(m) if m is not None else None for m in masks],
        "survivors": survivors,
        "unconditional_port_weight": str(Fraction(field_amplitudes[PORT] ** 2, denominator)),
        "fully_dephased_port_weight": str(Fraction(field_counts[PORT], denominator)),
        "survival_by_tick": per_tick,
    }


def prior_tick_control(sites):
    # The first three masks agree with the complete event. Keep everything on
    # tick four to distinguish the terminal port from final mask survival.
    report = {}
    for label, signal, expected, pre_final in (("plus", POSITIVE_SIGNAL, "1/4", "1/2"),
                                               ("minus", NEGATIVE_SIGNAL, "0", "1/4")):
        masks = masks_for((REFERENCE, signal), sites)
        partial_masks = masks[:-1] + [None]
        case = check_case(sites, partial_masks)
        require(case["unconditional_port_weight"] == expected, "Incorrect open-final-mask port weight")
        require(case["survival_by_tick"][-1] == {"coherent": pre_final, "fully_dephased": "1/4"},
                "Unrestricted last tick must preserve total incoming weight")
        report[label] = case
    return report


def comparator(sites):
    samples = {}
    for label, signal, expected, pre_final in (("plus", POSITIVE_SIGNAL, "1/4", "1/2"),
                                               ("minus", NEGATIVE_SIGNAL, "0", "1/4")):
        case = check_case(sites, masks_for((REFERENCE, signal), sites), (REFERENCE, signal))
        require(all(row["port"] == list(PORT) for row in case["survivors"].values()), "Unexpected output port")
        require(case["unconditional_port_weight"] == expected, "Incorrect coherent output")
        require(case["fully_dephased_port_weight"] == "1/8", "Incorrect dephased output")
        require(case["survival_by_tick"][2]["coherent"] == pre_final, "Incorrect pre-final survival")
        relative_sign = 1 if label == "plus" else -1
        for coefficient, weight in case["mixture_port_weights"].items():
            theta = Fraction(coefficient)
            require(Fraction(weight) == (1 + relative_sign * theta) / 8, "Incorrect mixture weight")
        samples[label] = case
    return samples


def minimal_horizon(sites):
    # Design class: three distinct histories at the same clock and same
    # named terminal port. One history is a fixed reference for both
    # settings; each coordinatewise union must admit just its specified pair
    # and the two signal histories must have opposite signs. Expand each
    # union explicitly, since unions of site masks can admit extra histories.
    search = []
    for depth in range(1, 5):
        groups = defaultdict(list)
        for directions in itertools.product("RL", repeat=depth):
            word = "".join(directions)
            port = (trajectory(word, sites)[-1], word[-1])
            groups[port].append(word)
        hits = []
        max_port_multiplicity = max(map(len, groups.values()))
        for port, group in groups.items():
            for reference in group:
                by_relative_sign = defaultdict(list)
                for word in group:
                    if word == reference:
                        continue
                    survivors, _, _ = enumerate_words(sites, masks_for((word, reference), sites))
                    if set(survivors) == {word, reference}:
                        by_relative_sign[sign(word) * sign(reference)].append(word)
                for positive, negative in itertools.product(by_relative_sign[1], by_relative_sign[-1]):
                    hits.append({"port": list(port), "reference": reference,
                                 "positive_signal": positive, "negative_signal": negative})
        search.append({"depth": depth, "hits": len(hits), "largest_port_word_count": max_port_multiplicity})
    return search


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sites", type=int, default=5)
    options = parser.parse_args()
    if options.sites < 3:
        parser.error("the isolation argument requires at least three sites")
    n = options.sites
    comparisons = comparator(n)
    singles = {}
    for word in (REFERENCE, POSITIVE_SIGNAL, NEGATIVE_SIGNAL):
        case = check_case(n, masks_for((word,), n), (word,))
        require(case["unconditional_port_weight"] == "1/16", "Incorrect singleton output")
        require(set(case["mixture_port_weights"].values()) == {"1/16"}, "Singleton depends on theta")
        singles[word] = case
    unrestricted = check_case(n, [None] * 4)
    require(unrestricted["survival_by_tick"][-1] == {"coherent": "1", "fully_dephased": "1"},
            "Unrestricted propagation must conserve probability")
    null = check_case(n, [set(), None, None, None], ())
    require(null["unconditional_port_weight"] == "0", "Empty mask must extinguish all light")
    trials = minimal_horizon(n)
    if n == 5:
        require([x["hits"] for x in trials[:3]] == [0, 0, 0] and trials[-1]["hits"] > 0,
                "Comparator horizon changed on five sites")
    for ring in range(3, 65):
        comparator(ring)
    conditional = {}
    for label, case in comparisons.items():
        incoming = case["survival_by_tick"][2]
        conditional[label] = {
            "coherent": str(Fraction(case["unconditional_port_weight"]) / Fraction(incoming["coherent"])),
            "fully_dephased": str(Fraction(case["fully_dephased_port_weight"]) / Fraction(incoming["fully_dephased"])),
        }
    print(json.dumps({
        "sites": n, "start": [0, "R"], "port": list(PORT), "clock": 4,
        "comparison": comparisons, "singleton_controls": singles,
        "without_terminal_mask": prior_tick_control(n), "unrestricted": unrestricted,
        "empty_first_mask": null, "minimum_horizon_search": trials,
        "crosscheck_sites": [3, 64], "crosscheck_complete_direction_words": 62 * 2 * 16,
        "pre_final_conditioning": {
            "description": "P(port at t=4 | first three masks passed), evaluated per setting",
            "results": conditional,
        },
        "scope": "Ideal Hadamard coin, whole-site masks, surviving branches add coherently at a rail; "
                 "dephased controls add word intensities. All reported port weights are per original launch.",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
