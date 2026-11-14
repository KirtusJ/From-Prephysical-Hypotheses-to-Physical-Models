"""Recompute the Vigo eraser comparison from the two archived Figure 1 histograms."""

import argparse
import hashlib
import json
import math
import pickletools
from fractions import Fraction
from pathlib import Path


DATA = Path(__file__).parent / "results" / "eraser_vigo_source"
FILES = {
    "which_way": ("counts.npy", "32c3ddacdb1476db9234bd41318c2650497a1ac9e5d31de694c46c06d3347895"),
    "erased": ("counts2.npy", "cdd4cd90545216c9e9c157303d5914240e7715f01835129b2a9af8ecf67e384c"),
}
OUTCOMES = ("00", "01", "10", "11")


def read_counts(filename, digest):
    data = (DATA / filename).read_bytes()
    if hashlib.sha256(data).hexdigest() != digest or data[:8] != b"\x93NUMPY\x01\x00":
        raise ValueError(f"Unexpected figure input {filename}")
    offset = 10 + int.from_bytes(data[8:10], "little")
    # Read literal histogram entries without executing NumPy/Qiskit pickle payloads.
    ops = [(op.name, value) for op, value, _ in pickletools.genops(data[offset:])]
    counts = {}
    for i, (op, key) in enumerate(ops):
        if op == "BINUNICODE" and key in OUTCOMES:
            memo, number = ops[i + 1 : i + 3]
            if key in counts or memo[0] != "BINPUT" or number[0] not in {"BININT1", "BININT2"}:
                raise ValueError(f"Unexpected count encoding for {key}")
            counts[key] = number[1]
    if set(counts) != set(OUTCOMES) or sum(counts.values()) != 8192:
        raise ValueError("Incomplete histogram")
    return counts


def rates(c):
    n = sum(c.values())
    return {
        "system_zero": Fraction(c["00"] + c["10"], n),
        "agreement": Fraction(c["00"] + c["11"], n),
        "system_zero_given_record_zero": Fraction(c["00"], c["00"] + c["01"]),
        "system_zero_given_record_one": Fraction(c["10"], c["10"] + c["11"]),
    }


def normalize(cells, power, separate):
    weights = [Fraction(w) ** power for w in cells]
    denominator = sum(weights)
    if separate:
        return [
            weight / (2 * sum(weights[(i // 2) * 2 : (i // 2 + 1) * 2]))
            for i, weight in enumerate(weights)
        ]
    return [weight / denominator for weight in weights]


def run():
    panels = {}
    for setting, (name, digest) in FILES.items():
        c = read_counts(name, digest)
        panels[setting] = {"source": name, "sha256": digest, "counts": c, "rates": rates(c)}
    off = panels["which_way"]["rates"]
    on = panels["erased"]["rates"]
    interval_radius = math.sqrt(math.log(40) / 8192)
    changes = {}
    for event in ("system_zero", "agreement"):
        difference = on[event] - off[event]
        changes[event] = {
            "on_minus_off": difference,
            "individual_95pct_Hoeffding_interval": [
                float(difference) - interval_radius, float(difference) + interval_radius
            ],
        }
    for cells in ([1, 1, 1, 1], [1, 0, 0, 1], [3, 1, 1, 3]):
        for power in (1, 2, 3):
            if normalize(cells, power, False) != normalize(cells, power, True):
                raise ValueError("Balanced-sector identity failed")
    control = {}
    for key, cells in (("Z", [2, 0, 1, 1]), ("X", [1, 1, 2, 0])):
        control[key] = {
            law: sum(normalize(cells, 2, separate)[:2])
            for law, separate in (("global_square", False), ("rowwise_square", True))
        }
    if control["Z"]["global_square"] - control["X"]["global_square"] != Fraction(1, 3):
        raise ValueError("Asymmetric control failed")
    return {"panels": panels, "differences": changes, "hypothetical_record_zero_rate": control}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    with parser.parse_args().output.open("x", encoding="utf-8", newline="\n") as output:
        json.dump(run(), output, default=str, indent=2, allow_nan=False)
        output.write("\n")
