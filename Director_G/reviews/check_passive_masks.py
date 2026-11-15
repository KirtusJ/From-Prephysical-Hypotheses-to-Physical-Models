"""Exact comparison of passive paths, a nonnegative flow, and a signed walk.

Start at (0,R) on the five-site ring. The same binary site masks pass or
absorb both rails. The reported detector probabilities are per launch.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import product
import json


SITES = 5
PORT = (0, "L")
ALL = frozenset(range(SITES))
EMPTY = frozenset()
MASKS = {
    "reference": ({1}, {0}, {1}, {0}),
    "positive": ({4}, {0}, {1}, {0}),
    "negative": ({1}, {2}, {1}, {0}),
    "constructive": ({1, 4}, {0}, {1}, {0}),
    "destructive": ({1}, {0, 2}, {1}, {0}),
    "open": (ALL,) * 4,
}


def check(condition, message):
    if not condition:
        raise ValueError(message)


def read_paths(masks):
    """Independently sum words, with a minus from each consecutive LL."""
    clocks = []
    for stop in range(1, len(masks) + 1):
        field, counts = Counter(), Counter()
        words = []
        for directions in product("RL", repeat=stop):
            x, previous, gain = 0, "R", 1
            for direction, mask in zip(directions, masks[:stop]):
                x = (x + (1 if direction == "R" else -1)) % SITES
                if x not in mask:
                    break
                if direction == previous == "L":
                    gain = -gain
                previous = direction
            else:
                field[x, previous] += gain
                counts[x, previous] += 1
                if (x, previous) == PORT:
                    words.append("".join(directions))
        signed = {k: F(v * v, 2**stop) for k, v in field.items()}
        fair = {k: F(v, 2**stop) for k, v in counts.items()}
        clocks.append((signed, fair, words))
    return clocks


def positive_flow(masks):
    """On each site, route mass using both incoming rail occupancies."""
    field = {(0, "R"): F(1)}
    clocks = []
    for mask in masks:
        output = {}
        for x in range(SITES):
            right = field.get((x, "R"), F(0))
            left = field.get((x, "L"), F(0))
            half = (left + right) / 2
            correction = min(left, right)
            check(half >= correction >= 0, "negative mass")
            for rail, shift, weight in (("R", 1, half + correction),
                                        ("L", -1, half - correction)):
                destination = (x + shift) % SITES
                if destination in mask:
                    output[destination, rail] = weight
        field = output
        clocks.append(field)
    return clocks


def descendants(current, keeping):
    possible = {(x + offset) % SITES for x in current for offset in (1, -1)}
    ordered = sorted(possible)
    for bits in product((False, True), repeat=len(ordered)):
        mask = frozenset(x for x, admitted in zip(ordered, bits) if admitted)
        yield keeping + (mask,), mask


def shortest_full_mask_check():
    # Bits on unreachable sites cannot affect any of the three models.
    cases = {((), frozenset({0}))}
    counts = {}
    for clock in range(1, 4):
        cases = {case for prefix, current in cases
                 for case in descendants(current, prefix)}
        counts[clock] = len(cases)
        for prefix, _ in cases:
            signed = read_paths(prefix)[-1][0]
            flow = positive_flow(prefix)[-1]
            check(all(signed.get(k, 0) == flow.get(k, 0)
                      for k in set(signed) | set(flow)),
                  f"earlier distinction at masks {prefix}")
    return counts


def efficiency_controls():
    # Deterministic behavior of two models at the constructive and open-mask
    # settings, both measured at the same detector/time. The allowed efficiency
    # change across settings is a hypothesis on the instrument, not on masks.
    theta = F(1, 2)
    null = F(3, 16)
    constructive = (1 + theta) / 8
    first_measurement = tuple(F(1, 2)*p for p in (constructive, F(3, 16) - theta/8))
    check(first_measurement == (F(3,32), F(1,16)), "common efficiency control")
    alternative_efficiencies = (F(1, 2), F(1, 3))
    alternative_measurement = tuple(p*q for p,q in zip((constructive, null), alternative_efficiencies))
    check(first_measurement == alternative_measurement, "separate-efficiency confounding")
    # Interleaving cancels drift in expectations only if the distribution of
    # efficiency is the same in the settings and independent of outcome.
    efficiencies = [F(1,4), F(3,4), F(1,2), F(1,8)]
    average_efficiency = sum(efficiencies)/len(efficiencies)
    rates = (constructive, F(3, 16) - theta/8)
    measured = tuple(sum(e*p for e in efficiencies)/len(efficiencies) for p in rates)
    check(measured == tuple(average_efficiency*p for p in rates), "balanced drift")
    check(measured[0]/measured[1] == rates[0]/rates[1], "ratio not invariant")
    return {"at_theta_half": {"constructive_and_open_observed": list(map(str, first_measurement)),
            "coherent_mixture_efficiencies": ["1/2", "1/2"],
            "positive_flow_mixture_efficiencies": list(map(str, alternative_efficiencies))},
            "balanced_drift_mean_efficiency": str(average_efficiency)}


def main():
    word_sets, table, survival = {}, {}, {}
    for name, masks in MASKS.items():
        word_clocks, flows = read_paths(masks), positive_flow(masks)
        signed, fair, words = word_clocks[-1]
        word_sets[name] = set(words)
        table[name] = (signed.get(PORT, 0), fair.get(PORT, 0),
                       flows[-1].get(PORT, 0))
        survival[name] = [sum(q.values()) for q in flows]
        if name != "open":
            for (coherent, _, _), flow in zip(word_clocks, flows):
                check(sum(coherent.values()) == sum(flow.values()),
                      f"prefix survival mismatch at {name}")
                check(all(coherent.get(k, 0) == flow.get(k, 0)
                          for k in set(coherent) | set(flow)),
                      f"prefix port mismatch at {name}")

    check(word_sets["constructive"] == word_sets["reference"] | word_sets["positive"],
          "constructive union admits extra histories")
    check(word_sets["destructive"] == word_sets["reference"] | word_sets["negative"],
          "destructive union admits extra histories")
    check(len(word_sets["reference"] | word_sets["positive"] | word_sets["negative"]) == 3,
          "signals and reference overlap")
    for name in ("reference", "positive", "negative"):
        check(table[name] == (F(1, 16),) * 3, f"singleton {name}")
    check(table["constructive"] == (F(1, 4), F(1, 8), F(1, 4)), "constructive")
    check(table["destructive"] == (0, F(1, 8), 0), "destructive")
    check(table["open"] == (F(1, 16), F(3, 16), F(3, 16)), "open masks")
    check(sum(positive_flow(MASKS["open"])[-1].values()) == 1, "unmasked conservation")

    # A single fixed path distribution predicts unions by adding path weights.
    # The three witness paths plus an unobserved word suffice for normalization.
    for theta in (F(0), F(1, 3), F(1, 2), F(1)):
        target = {k: (1-theta)*row[1] + theta*row[0] for k, row in table.items()}
        witness = target["constructive"] - target["destructive"]
        witness -= target["positive"] - target["negative"]
        check(witness == theta/4, "witness contrast")
        fit = {"reference": F(1,16), "positive": (1+theta)/16, "negative": (1-theta)/16}
        check(all(v >= 0 for v in fit.values()) and sum(fit.values()) <= 1, "invalid distribution")
        fit.update(constructive=fit["reference"]+fit["positive"],
                   destructive=fit["reference"]+fit["negative"])
        error = max(abs(target[k]-v) for k,v in fit.items())
        check(error == abs(witness)/4 == theta/16, "optimal uniform distance")
        check((1-theta)*table["open"][1] + theta*table["open"][2] - target["open"] == theta/8,
              "open-mask discriminator")

    # This relation involves all three settings and is homogeneous in efficiency.
    for theta in (F(0), F(1, 3), F(1)):
        for efficiency in (F(1, 7), F(1)):
            plus = efficiency * (1 + theta) / 8
            minus = efficiency * (1 - theta) / 8
            total = plus + minus
            difference = plus - minus
            open_coherent = efficiency * (3 - 2 * theta) / 16
            open_flow = efficiency * F(3, 16)
            check(4 * open_coherent - 3 * total == -2 * difference,
                  "three-setting coherent relation")
            check(4 * open_flow - 3 * total == 0, "three-setting flow relation")

    print(json.dumps({"terminal_weights_coherent_passive_flow":
                      {k: list(map(str,row)) for k,row in table.items()},
                      "unconditional_flow_survival":[str(x) for x in survival["open"]],
                      "all_effectively_distinct_mask_prefixes_through_tick_3":shortest_full_mask_check(),
                      "efficiency_controls":efficiency_controls(),
                      "five_reading_optimal_uniform_error":"theta/16",
                      "open_mask_rival_minus_coherent_mixture":"theta/8"}, indent=2))


if __name__ == "__main__":
    main()
