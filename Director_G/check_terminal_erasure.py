"""Exact incident-retention bounds for a powered six-well read with erasure."""

import json
from fractions import Fraction
from itertools import product
from math import prod
from pathlib import Path


HERE = Path(__file__).resolve().parent


def probabilities(weights):
    return [Fraction(w, sum(weights)) for w in weights]


def partition_scores(masses, power):
    """Visit all set partitions, including intermediate groupings of three modes."""
    def pools(index, groups):
        if index == len(masses):
            yield sum(m ** power for m in groups)
            return
        mass = masses[index]
        for i in range(len(groups)):
            updated = list(groups)
            updated[i] += mass
            yield from pools(index + 1, updated)
        yield from pools(index + 1, [*groups, mass])

    return sorted(set(pools(0, [])))


def retention(bins, power):
    p = probabilities([sum(b) for b in bins])
    scores = [partition_scores(b, power) for b in bins]
    low = [s[0] for s in scores]
    high = [s[-1] for s in scores]
    j = min(range(len(p)), key=lambda i: high[i] / p[i])
    k = high[j] / p[j]
    weights = [max(a, k * pi) for a, pi in zip(low, p)]
    model = probabilities(weights)
    eta = k / sum(weights)
    keep = [eta * pi / ri for pi, ri in zip(p, model)]
    assert min(keep) >= 0 and max(keep) <= 1
    assert all(ki * ri == eta * pi for ki, ri, pi in zip(keep, model, p))
    assert 1 - sum(ki * ri for ki, ri in zip(keep, model)) == 1 - eta

    # Check the inequality used for the upper bound on *every* pure partition.
    # Since it is linear in normalized probabilities it also holds for mixtures.
    all_patterns = 0
    for pattern in product(*scores):
        r = probabilities(pattern)
        assert all(ri * high[j] >= r[j] * a for ri, a in zip(r, low))
        all_patterns += 1
    assert eta * sum(max(pi, a / k) for pi, a in zip(p, low)) == 1

    # Realize the optimizer with explicit launch weights on normalized vertices.
    choices = []
    for a, b, w in zip(low, high, weights):
        if a == b:
            choices.append([(a, Fraction(1))])
        else:
            right = Fraction(w - a, b - a)
            choices.append([(a, 1 - right), (b, right)])
    observed = [Fraction(0)] * len(p)
    witnesses = []
    for corner in product(*choices):
        vertex, factors = zip(*corner)
        share = prod(factors) * sum(vertex) / sum(weights)
        assert share >= 0
        if share:
            witnesses.append({"scores": vertex, "launch_share": str(share)})
            for i, ri in enumerate(probabilities(vertex)):
                observed[i] += share * ri
    assert observed == model
    assert sum(Fraction(row["launch_share"]) for row in witnesses) == 1
    return {"power": power, "incident_target": list(map(str, p)),
            "retention_ceiling": str(eta), "no_click": str(1 - eta),
            "bottleneck_bin": j, "distinct_partition_vectors": all_patterns,
            "pre_erasure": list(map(str, model)), "accept_given_bin": list(map(str, keep)),
            "attaining_partitions": witnesses}


def route(law, efficiencies, shifts, *, pre_route=False):
    n = len(law)
    clicks = [Fraction(0)] * n
    for shift in shifts:
        for i, ri in enumerate(law):
            output = (i + shift) % n
            efficiency = efficiencies[i if pre_route else output]
            clicks[i] += ri * efficiency / len(shifts)
    return clicks


def routing_controls():
    laws = [probabilities([1, 2, 4]), probabilities([1, 4, 16])]
    efficiencies = [[Fraction(0), Fraction(1, 2), Fraction(1)],
                    [Fraction(0), Fraction(1, 4), Fraction(0)]]
    examples = []
    for law, eff in zip(laws, efficiencies):
        routed = route(law, eff, range(3))
        assert probabilities(routed) == law
        assert routed == [p * sum(eff) / 3 for p in law]
        upstream = route(law, eff, range(3), pre_route=True)
        assert probabilities(upstream) != law
        assert upstream == route(law, eff, [0])
        examples.append({"cyclic_after_routing": list(map(str, routed)),
                         "loss_at_input_label": list(map(str, upstream))})
    # Uniform overall assignment alone fails if route choice discloses the type.
    # Three equal types have deterministic shifts and the same true histogram.
    correlated_eff = [[Fraction(int(channel == shift)) for channel in range(3)]
                      for shift in range(3)]
    correlated = [route(laws[0], eff, [s]) for s, eff in enumerate(correlated_eff)]
    assert all(row == [laws[0][0], 0, 0] for row in correlated)
    blind = route(laws[1], [Fraction(0)] * 3, range(3))
    assert sum(blind) == 0
    return {"type_examples": examples, "type_correlated_shifts": list(map(str, correlated[0])),
            "entirely_blind_type": list(map(str, blind))}


def main():
    archive = json.loads((HERE / "results/reciprocal_ring_score.json").read_text())
    rows = archive["all_cover_rows_R_L_unsigned"]
    masks = {"well": 0, "well_and_sheet": 3, "well_and_0R": 1}
    studies = {}
    for name, mask in masks.items():
        labels, bins = [], []
        for x in range(6):
            amplitudes = [*rows[x][:2], *rows[x + 6][:2]]
            for bit in (0, 1):
                cells = [a * a for i, a in enumerate(amplitudes)
                         if a and ((mask >> i) & 1) == bit]
                if cells:
                    labels.append([x, bit])
                    bins.append(cells)
        assert sum(map(sum, bins)) == 2048
        studies[name] = {"labels_well_bit": labels, "positive_mode_masses": bins,
                         "bounds": [retention(bins, q) for q in (0, 1, 2)]}
    assert [s["bounds"][2]["retention_ceiling"] for s in studies.values()] == [
        "1142784/1181699", "41472/242957", "2048/242957"]
    assert all(s["bounds"][1]["retention_ceiling"] == "1" for s in studies.values())
    report = {"six_well_tick": 11, "studies": studies, "routing_controls": routing_controls()}
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
