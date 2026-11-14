"""Test one shared binary response on four blocks of heralded phonon records."""

import argparse
import csv
import hashlib
import itertools
import json
import math
from collections import Counter
from pathlib import Path


STARTS = (0, 16, 96, 112)
WIDTH = 16
PAIRS = tuple(itertools.combinations(range(4), 2))
SOURCE = "https://zenodo.org/records/20944616/files/post_selected_trajectories.csv"
ARCHIVE_MD5 = "a58ef64030570b966680747238468ce7"


def summarize(rows):
    n = len(rows)
    means = [sum(col) / n for col in zip(*rows)]
    centered = [tuple(value - mu for value, mu in zip(row, means)) for row in rows]
    cov = {(i, j): sum(row[i] * row[j] for row in centered) / n for i, j in PAIRS}
    a, b, c, d = cov[0, 1], cov[2, 3], cov[0, 2], cov[1, 3]
    tetrad = a * b - c * d
    # Delta-method influence of the plug-in covariance products, one row per trajectory.
    influences = [
        b * (x * y - a) + a * (z * w - b) - d * (x * z - c) - c * (y * w - d)
        for x, y, z, w in centered
    ]
    se = math.sqrt(sum(i * i for i in influences) / (n * (n - 1)))
    return {
        "n": n, "means": means,
        "covariances": {f"{i+1},{j+1}": v for (i, j), v in cov.items()},
        "tetrad": tetrad, "individual_iid_delta_standard_error": se,
        "individual_iid_normal_95_interval": [tetrad - 1.959964 * se, tetrad + 1.959964 * se],
    }


def analyze(source):
    with source.open("rb") as data:
        if hashlib.file_digest(data, "md5").hexdigest() != ARCHIVE_MD5:
            raise ValueError("Input differs from the versioned Zenodo archive")
        data.seek(0)
        sha = hashlib.file_digest(data, "sha256").hexdigest()
    rows = []
    parity_totals = [0] * 294
    excitation_counts = Counter()
    labels = {"0.000000000000000000e+00": 0, "1.000000000000000000e+00": 1}
    with source.open(encoding="ascii", newline="") as data:
        for record in csv.reader(data):
            if len(record) != len(parity_totals):
                raise ValueError("Incomplete parity record")
            bits = [labels[field] for field in record]
            for k, bit in enumerate(bits):
                parity_totals[k] += bit
            excitation_counts[sum(bits)] += 1
            rows.append(tuple(sum(bits[j:j+WIDTH]) / WIDTH for j in STARTS))
    if len(rows) != 8447:
        raise ValueError("Unexpected cohort size")
    cuts = [round(k * len(rows) / 4) for k in range(5)]
    return {
        "input": SOURCE, "md5": ARCHIVE_MD5, "sha256": sha,
        "read_indices_one_based_inclusive": [[j+1, j+WIDTH] for j in STARTS],
        "all_trajectory_estimate": summarize(rows),
        "file_order_quarters_sensitivity": [
            summarize(rows[lo:hi]) for lo, hi in zip(cuts, cuts[1:])
        ],
        "excited_at_each_of_294_checks": parity_totals,
        "trajectories_by_number_excited_in_294_checks": [
            excitation_counts[k] for k in range(295)
        ],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result = analyze(args.source)
    with args.output.open("x", encoding="utf-8", newline="\n") as out:
        json.dump(result, out, indent=2, allow_nan=False)
        out.write("\n")
