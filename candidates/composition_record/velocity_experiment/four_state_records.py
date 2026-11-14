"""Score every launch of the native four-preparation memory test.

score INPUT.json[.gz] reads the detector record. simulate runs a new Aer replay.
The encoder receives only the intermediate absolute position codes. The trusted
tester uses the separate preparation bits and the probe code to score the result.
"""
import argparse
import gzip
import hashlib
import json
from fractions import Fraction
from importlib.metadata import version
from pathlib import Path
from runpy import run_path


def natural(value, name):
    if type(value) is not int or value < 0:
        raise ValueError(f"{name} must be a nonnegative integer")
    return value


def read_record(path):
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8") as stream:
        def unique(pairs):
            mapping = {}
            for key, value in pairs:
                if key in mapping:
                    raise ValueError(f"duplicate JSON key {key!r}")
                mapping[key] = value
            return mapping
        return json.load(stream, object_pairs_hook=unique)


def position_label(steps, positions):
    """Four Pauli labels, with identity/Z winning a first-column magnitude tie."""
    a, c, sign, previous = 1, 0, 1, 0
    for current in positions:
        displacement = (12 - 2*(current-previous)) % 16
        g, h, direction = steps[displacement//2]
        a, c = g*a - h*direction*c, h*a + g*direction*c
        sign *= direction
        previous = current
    if sign > 0:
        return "I" if abs(a) >= abs(c) else "J"
    return "Z" if abs(a) >= abs(c) else "X"


def score(data):
    if data["schema"] != "four-state-walk-v1":
        raise ValueError("unknown record schema")
    m = natural(data["blocks"], "blocks")
    attempts = natural(data["attempts"], "attempts")
    if not attempts:
        raise ValueError("positive incident attempts required")
    counts = data["counts"]
    if not isinstance(counts, dict):
        raise ValueError("counts must map fixed-width binary words to integers")
    steps = run_path(str(Path(__file__).with_name("check_record_messages.py")))["read_steps"]()
    prepared = [[0, 0] for _ in range(4)]
    labels = dict.fromkeys(("I", "J", "Z", "X"), 0)
    malformed_jumps = 0
    for word, count in counts.items():
        natural(count, "count")
        if len(word) != 3*m+5 or set(word) - {"0", "1"}:
            raise ValueError(f"invalid fixed-width word {word!r}")
        bits = int(word, 2)
        basis, sign = bits & 1, (bits >> 1) & 1
        positions = [(bits >> (2+3*j)) & 7 for j in range(m)]
        label = position_label(steps, positions)
        labels[label] += count
        previous = positions[-1] if positions else 0
        result = ((bits >> (2+3*m)) - previous) % 8
        row = prepared[2*basis+sign]
        row[0] += count
        if result > 1:
            malformed_jumps += count
            continue
        flip = label == "J" or (label == "X" and basis == 0) or (label == "Z" and basis == 1)
        if result ^ int(flip) == sign:
            row[1] += count
    recorded = sum(row[0] for row in prepared)
    if recorded > attempts:
        raise ValueError("more recorded counts than incident attempts")
    successes = sum(row[1] for row in prepared)
    return {"attempts": attempts, "missing": attempts-recorded, "invalid_final_jumps": malformed_jumps,
            "successes": successes, "success_per_attempt": str(Fraction(successes, attempts)),
            "preparations": dict(zip(("R", "L", "+", "-"), prepared)), "label_counts": labels}


def simulate(args):
    from qiskit import qasm3, transpile
    from qiskit_aer import AerSimulator

    if args.blocks < 0 or args.shots < 1 or args.output.exists():
        raise ValueError("select a nonnegative block count, positive shots and a new output path")
    source = args.qasm.read_bytes()
    exporter = run_path(str(Path(__file__).with_name("four_state_circuit.py")))["exported"]
    normalized = source.decode("ascii").replace("\r\n", "\n")
    variants = {exporter(args.blocks): "coherent", exporter(args.blocks, True): "copy-at-17"}
    if normalized not in variants:
        raise ValueError("input does not match either four-state circuit for the selected block count")
    circuit = qasm3.loads(source.decode("ascii"))
    if (circuit.num_qubits, circuit.num_clbits) != (4, 3*args.blocks+5):
        raise ValueError("circuit width disagrees with --blocks")
    backend = AerSimulator(method="statevector", max_parallel_threads=2, shot_branching_enable=True)
    program = transpile(circuit, backend, optimization_level=0, seed_transpiler=args.seed)
    counts = backend.run(program, shots=args.shots, seed_simulator=args.seed).result().get_counts()
    data = {"schema": "four-state-walk-v1", "provenance": "ideal circuit simulator",
            "blocks": args.blocks, "attempts": args.shots, "seed": args.seed,
            "arm": variants[normalized],
            "qasm_sha256": hashlib.sha256(source).hexdigest(),
            "versions": {n: version(n) for n in ("qiskit", "qiskit-aer", "qiskit-qasm3-import")},
            "counts": dict(sorted(counts.items()))}
    if sum(counts.values()) != args.shots:
        raise ValueError("simulator returned an incomplete acquisition")
    result = score(data)
    payload = (json.dumps(data, indent=2)+"\n").encode("utf-8")
    with args.output.open("xb") as stream:
        stream.write(gzip.compress(payload, mtime=0) if args.output.suffix == ".gz" else payload)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_subparsers(dest="mode", required=True)
    modes.add_parser("score").add_argument("input", type=Path)
    replay = modes.add_parser("simulate")
    replay.add_argument("qasm", type=Path)
    replay.add_argument("output", type=Path)
    replay.add_argument("--blocks", type=int, required=True)
    replay.add_argument("--shots", type=int, default=8192)
    replay.add_argument("--seed", type=int, default=24127)
    args = parser.parse_args()
    result = score(read_record(args.input)) if args.mode == "score" else simulate(args)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
