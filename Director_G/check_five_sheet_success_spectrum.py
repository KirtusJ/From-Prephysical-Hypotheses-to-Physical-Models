"""Audit the four-prefix test directly on physical site, rail and sheet paths."""

import argparse
import json
from collections import defaultdict
from fractions import Fraction
from itertools import product
from pathlib import Path


def block(site, rail, source):
    outputs = defaultdict(lambda: [0] * 5)
    for directions in product((1, -1), repeat=3):
        for initial_sheet, count in enumerate(source):
            x, incoming, y, signed_count = site, rail, initial_sheet, count
            for outgoing in directions:
                y = (y + x) % 5
                x += outgoing
                if incoming == outgoing == -1:
                    signed_count = -signed_count
                incoming = outgoing
            outputs[x, incoming][y] += signed_count
    return outputs


def norm(row):
    return sum(value * value for value in row)


def physical_prefixes():
    site, rail, row = 0, 1, [1, 0, 0, 0, 0]
    joint_herald = None
    records = []
    # The herald, four tested prefixes and a fifth held-out prediction.
    for k in range(6):
        outputs = block(site, rail, row)
        target = (-1, -1) if k == 0 else (site + rail, rail)
        total_norm = 8 * norm(row)
        assert sum(map(norm, outputs.values())) == total_norm
        site, rail = target
        row = outputs[target]
        joint = Fraction(norm(row), 8 ** (k + 1))
        if k == 0:
            joint_herald = joint
        records.append({
            "constructive_prefix": k,
            "tick": 3 * (k + 1),
            "target_site_rail": list(target),
            "all_original_launches": str(joint),
            "among_initial_heralds": str(joint / joint_herald),
            "outcomes_at_next_read_given_entry": [
                {"site": x, "rail": d, "signed_sheets": sheet_row,
                 "probability": str(Fraction(norm(sheet_row), total_norm))}
                for (x, d), sheet_row in sorted(outputs.items())
            ],
        })
    return records


def compute():
    records = physical_prefixes()
    moments = [Fraction(record["among_initial_heralds"]) for record in records]
    assert moments[:5] == [1, Fraction(1, 8), Fraction(1, 32),
                           Fraction(5, 512), Fraction(13, 4096)]
    for i in range(len(moments) - 2):
        assert 64 * moments[i + 2] - 24 * moments[i + 1] + moments[i] == 0
    polynomial = [1, -24, 64]
    squared = [0] * 5
    for i, a in enumerate(polynomial):
        for j, b in enumerate(polynomial):
            squared[i + j] += a * b
    assert squared == [1, -48, 704, -3072, 4096]
    assert sum(c * v for c, v in zip(squared, moments)) == 0
    # The five exclusive, observable results for the fifteen-tick run.
    first_failure_or_pass = [moments[j] - moments[j + 1] for j in range(4)]
    first_failure_or_pass.append(moments[4])
    outcome_scores = [sum(squared[:j + 1]) for j in range(5)]
    assert sum(first_failure_or_pass) == 1 and min(first_failure_or_pass) > 0
    assert sum(p * a for p, a in zip(first_failure_or_pass, outcome_scores)) == 0

    alternate = [(Fraction(0), Fraction(41, 88)),
                 (Fraction(11, 48), Fraction(216, 407)),
                 (Fraction(1), Fraction(1, 296))]
    assert sum(w for _, w in alternate) == 1 and min(w for _, w in alternate) > 0
    other = [sum(w * x**j for x, w in alternate) for j in range(6)]
    assert other[:4] == moments[:4] and other[4] - moments[4] == Fraction(41, 24576)
    # A tiny persistent chance of 1 passes any fixed positive moment tolerance;
    # its next-success probability eventually approaches 1.
    contamination = Fraction(1, 2**24)
    contaminated = [(1 - contamination) * m + contamination for m in moments]
    assert all(abs(a - b) < contamination for a, b in zip(contaminated, moments))
    # The counter apparatus follows four genuine successive hazards then forces 0.
    hazards = [moments[j + 1] / moments[j] for j in range(4)] + [Fraction(0)]
    counter = [Fraction(1)]
    for h in hazards:
        counter.append(counter[-1] * h)
    assert counter[:5] == moments[:5] and counter[5] != moments[5]
    return {
        "source": "Integer signed path calculation with ordinary squared-norm records.",
        "physical_prefixes": records,
        "square_polynomial_ascending": squared,
        "score_by_initial_success_run_capped_at_four": outcome_scores,
        "first_failure_or_four_successes_given_herald": list(map(str, first_failure_or_pass)),
        "three_prefix_rival_atoms_and_weights": [[str(x), str(w)] for x, w in alternate],
        "three_prefix_rival_successes": list(map(str, other)),
        "three_prefix_rival_fourth_excess": str(other[4] - moments[4]),
        "counter_device_hazards": list(map(str, hazards)),
        "counter_device_successes": list(map(str, counter)),
        "contamination_at_one": str(contamination),
        "contaminated_successes": list(map(str, contaminated)),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    with args.destination.open("x", encoding="utf-8", newline="\n") as output:
        json.dump(compute(), output, indent=2)
        output.write("\n")
