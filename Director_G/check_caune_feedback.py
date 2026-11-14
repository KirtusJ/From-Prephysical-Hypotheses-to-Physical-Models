"""Replay preparation-labelled double reads and decoder feedback from Zenodo 15364358."""
import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from math import log, sqrt
from pathlib import Path

import h5py


DIGEST = "dd2a3d48e86ea81094b44439fb58a3d9788757e26799bd4ee7497eb94798ed08"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def report(path):
    require(sha256(path.read_bytes()).hexdigest() == DIGEST, "unexpected HDF5 digest")
    pairs = {}
    single = {}
    rounds = {}
    with h5py.File(path, "r") as source:
        for name in ("zeros", "ones"):
            reference = source["reference_data"]
            group = reference["double_measurement"][name]
            program = group["program"][()].decode().splitlines()
            expected = ["DECLARE ro BIT[2]"]
            if name == "ones":
                expected.append("RX(pi) 50")
            expected.extend(["MEASURE 50 ro[0]", "DELAY 50 5e-7", "MEASURE 50 ro[1]"])
            require(program == expected, "unexpected reference pulse sequence")
            hits = group["result/hard_measurements/50"]
            require(hits.shape == (10000, 2), "paired reference denominator")
            counts = Counter(map(tuple, hits[:].tolist()))
            require(set(counts) <= set(product(range(2), repeat=2)), "unknown read class")
            pairs[name] = [counts[a, b] for a, b in product(range(2), repeat=2)]
            one = reference["measurement_fidelity"][name]["result/hard_measurements/50"]
            require(one.shape == (10000, 1), "one-read reference denominator")
            c = Counter(one[:, 0].tolist())
            require(set(c) <= {0, 1}, "unknown one-read class")
            single[name] = [c[0], c[1]]

        for i in range(8):
            run = source[f"circuit_{i}/result"]
            n = int(run.attrs["rounds"])
            require(n == i + 2 and run.attrs["conditional_qubit"] == 50, "feedback layout")
            reads = run["hard_measurements/50"]
            codes = run["decoder_shot_results"][:, 0].tolist()
            require(reads.shape == (1000, n+1) and len(codes) == 1000, "feedback denominator")
            counts = Counter((a, c, b) for (a, b), c in zip(reads[:, -2:].tolist(), codes))
            keys = list(product(range(2), range(3), range(2)))
            require(set(counts) <= set(keys), "unknown feedback or read class")
            matches = sum(v for (a, c, b), v in counts.items() if b == (a ^ int(c == 1)))
            rounds[str(n)] = {"cells": [counts[k] for k in keys], "action_prediction_matches": matches}

    contrasts = {}
    for a in (0, 1):
        cells = [panel[2*a:2*a+2] for panel in pairs.values()]
        sums = [sum(row) for row in cells]
        rates = [Fraction(row[1], n) for row, n in zip(cells, sums)]
        gap = rates[1] - rates[0]
        # Four two-sided conditional proportions; alpha = 0.05 by the union bound.
        widths = [sqrt(log(160)/(2*n)) for n in sums]
        lower = max(0.0, abs(float(gap)) - sum(widths))/2
        contrasts[str(a)] = {"conditional_rates": list(map(str, rates)),
                             "empirical_minimax_error": str(abs(gap)/2),
                             "iid_95_lower_bound_rounded": round(lower, 9)}
    return {"source_sha256": DIGEST, "reference_pair_order": ["00", "01", "10", "11"],
            "paired_reference_counts": pairs, "one_read_counts_zero_one": single,
            "first_bit_contrasts": contrasts,
            "feedback_order": "lexicographic (previous hard bit, raw decoder 0/1/2, final hard bit)",
            "feedback_by_round": rounds}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result = report(args.archive)
    args.output.write_bytes((json.dumps(result, indent=2) + "\n").encode("utf-8"))
