"""Verify the translated-hyperplane test and replay a time-bin/spin acquisition."""

import argparse
from fractions import Fraction as F
import hashlib
from itertools import product
import json
from math import sqrt
from pathlib import Path


HERE = Path(__file__).resolve().parent
DATA = HERE / "spin_coincidences.json"
MAT_HASH = "dfd953e46b3961ef7478b3ecfdbc0a7fcf3fa60365ec15efa3a3b60aae0cbd84"
GATES = (219.0, 230.9, 242.8)


def hyperplane_controls():
    rows = list(product(range(5), repeat=3))
    dot = lambda h, m: sum(x*y for x, y in zip(h, m)) % 5
    directions = [h for h in rows[1:] if next(co for co in h if co) == 1]
    assert len(directions) == 31
    separating = 0
    for u in rows[1:]:
        for h in directions:
            first = {m for m in rows if dot(h, m) == 0}
            second = {tuple((x+y) % 5 for x, y in zip(m, u)) for m in first}
            if dot(h, u):
                assert first.isdisjoint(second) and len(first) == len(second) == 25
                separating += 1
            else:
                assert first == second
    assert separating == 124 * 25


def extract(path):
    import numpy as np
    from scipy.io import loadmat

    assert hashlib.sha256(path.read_bytes()).hexdigest() == MAT_HASH
    d = loadmat(path, simplify_cells=True)["Data"]
    assert d["n_configuration"] == 7
    record = {"acquisition": path.name, "sha256": MAT_HASH,
              "configurations": [str(s) for s in d["configurations"]["seq"]],
              "polarizer_deg": d["configurations"]["pol"].tolist(),
              "rf_phase_deg": d["configurations"]["rf_phase"].tolist(),
              "photon_gate_starts_ns": list(GATES), "photon_gate_width_ns": 3,
              "spin_gate_ns": [310, 360], "detectors": [4, 5]}
    for kind in ("Coincidences", "Coincidences_bg"):
        rows = []
        for c in d[kind]:
            t, ch = c["Times"][1], c["Channels"][1]
            assert t.shape == ch.shape and t.shape[1] == 2
            assert list(c["Config"]["CH"]) == [4, 5]
            assert np.isin(ch, [4, 5]).all()
            assert len(t) == c["n_Coincidences"][1]
            read = (t[:, 1] >= 310) & (t[:, 1] < 360)
            # First index is early/middle/late. Next indices label the two
            # photon and spin-readout detectors, respectively.
            gated = []
            for start in GATES:
                both = read & (t[:, 0] >= start) & (t[:, 0] < start + 3)
                pairs = [[int(np.count_nonzero(both & (ch[:, 0] == i) & (ch[:, 1] == j)))
                          for j in (4, 5)] for i in (4, 5)]
                assert sum(map(sum, pairs)) == int(np.count_nonzero(both))
                gated.append(pairs)
            gated_total = sum(sum(map(sum, gate)) for gate in gated)
            rows.append({"seconds": c["Config"]["IntTime"], "all_stored_pairs": len(t),
                         "outside_joint_gates": len(t) - gated_total, "gated": gated})
        record[kind] = rows
    return record


def spin_score(record):
    assert record["configurations"] == ["A", "C", "Bphase", "Bphase", "Bphase", "Bphase", "E"]
    rows = record["Coincidences"]
    z = [sum(map(sum, row["gated"][gate])) for row in rows[:2] for gate in (0, 2)]
    x = [sum(ch) for row in rows[2:4] for ch in row["gated"][1]]
    y = [sum(ch) for row in rows[4:6] for ch in row["gated"][1]]
    assert all(sum(map(sum, g)) >= 0 for row in rows for g in row["gated"])
    assert all(row["outside_joint_gates"] + sum(sum(map(sum, g)) for g in row["gated"])
               == row["all_stored_pairs"] for k in ("Coincidences", "Coincidences_bg") for row in record[k])
    # Same correlation sign convention as GetGHZFidelity.m.
    pz, px, py = [F(v[1] + v[2], sum(v)) for v in (z, x, y)]
    mx, my = 2 * px - 1, 2 * py - 1
    raw = pz / 2 + abs(mx - my) / 4
    # Multinomial expression for the author's independent Poisson propagation
    # within each set of four coincidence bins and across the three settings.
    var = sum(p * (1-p) / sum(c) for p, c in zip((pz, px, py), (z, x, y))) / 4
    return z, x, y, raw, sqrt(float(var))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--mat", type=Path, help="regenerate all retained bins from the pinned acquisition")
    ap.add_argument("--write", action="store_true", help="write the supplied MAT's bins")
    args = ap.parse_args()
    if args.write and args.mat is None:
        ap.error("--write requires --mat")
    if args.mat:
        data = extract(args.mat)
        if args.write:
            DATA.write_bytes((json.dumps(data, indent=2) + "\n").encode())
        else:
            assert data == json.loads(DATA.read_bytes())
    hyperplane_controls()
    z, x, y, raw, sigma = spin_score(json.loads(DATA.read_bytes()))
    assert (z, x, y) == ([36, 255, 160, 69], [237, 46, 61, 118], [32, 64, 105, 23])
    print(f"All 3,844 nonzero write/direction pairs checked. Raw fidelity {float(raw):.8f}, propagated SE {sigma:.8f}.")
