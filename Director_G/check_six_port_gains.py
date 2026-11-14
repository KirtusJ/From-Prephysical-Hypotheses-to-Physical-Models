"""Exact stable-gain certificate for Webb et al., PR Research 5, 023094, Table IV."""

from fractions import Fraction as F
import json
from pathlib import Path


TABLE = Path(__file__).with_name("results") / "six_port_gains.json"


def normalize(vector):
    total = sum(vector)
    return [F(x, total) for x in vector]


def tv(p, r):
    return sum(abs(x - y) for x, y in zip(p, r)) / 2


def distances(data):
    weights = data["effective_port_weights"]
    rows = []
    for row in data["table_IV"]:
        observed = normalize(row["hundredths_of_percent"])
        active = set(row["active_ports"])
        predicted = normalize([w if port in active else 0 for port, w in zip("ABCDEF", weights)])
        dark = sum(p for p, port in zip(observed, "ABCDEF") if port not in active)
        rows.append((tv(observed, predicted), dark))
    return rows


def main():
    data = json.loads(TABLE.read_bytes())
    assert [sum(row["hundredths_of_percent"]) for row in data["table_IV"]] == [10006, 9914, 10003, 9994]
    rows = distances(data)
    assert max(r[0] for r in rows) == max(r[1] for r in rows) == F(326, 10006)
    # Input-independent response within each output column makes the ideal
    # support graph blind to any finite positive power with unrestricted gains.
    b = 2**0.5 - 1
    masses = [b, b, b, b, b*b, b*b]
    for q in (0.5, 1, 2, 9):
        gains = [v/m**q for v, m in zip(data["effective_port_weights"], masses)]
        for entry in data["table_IV"]:
            active = [j for j, name in enumerate("ABCDEF") if name in entry["active_ports"]]
            products = [gains[j] * masses[j]**q for j in active]
            assert all(abs(v - data["effective_port_weights"][j]) < 1e-9 for v, j in zip(products, active))
    print("Worst-row TV is exactly", max(r[0] for r in rows))
    for entry, (error, dark) in zip(data["table_IV"], rows):
        print(entry["input"], f"TV {100*float(error):.5f}%, normalized dark leakage {100*float(dark):.5f}%")


if __name__ == "__main__":
    main()
