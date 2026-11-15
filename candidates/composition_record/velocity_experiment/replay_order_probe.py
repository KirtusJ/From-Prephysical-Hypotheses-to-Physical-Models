"""Run the exported 25-tick circuit in Qiskit Aer and keep all nine-bit words.

Usage: python replay_order_probe.py probe.qasm new_counts.json
Requires qiskit, qiskit-qasm3-import and qiskit-aer in the selected runtime.
"""
import argparse
import hashlib
import json
from importlib.metadata import version
from pathlib import Path

from qiskit import qasm3, transpile
from qiskit_aer import AerSimulator


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("qasm", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--shots", type=int, default=32768)
    parser.add_argument("--seed", type=int, default=251624)
    args = parser.parse_args()
    if args.shots < 1 or args.output.exists():
        parser.error("choose a positive shot count and a new output file")

    source = args.qasm.read_bytes()
    circuit = qasm3.loads(source.decode("ascii"))
    if (circuit.num_qubits, circuit.num_clbits) != (4, 9):
        parser.error("expected the four-qubit nine-bit exported order probe")
    backend = AerSimulator(method="statevector", shot_branching_enable=True,
                           max_parallel_threads=2)
    program = transpile(circuit, backend, optimization_level=0, seed_transpiler=args.seed)
    counts = backend.run(program, shots=args.shots, seed_simulator=args.seed).result().get_counts()
    words = {format(i, "09b"): int(counts.get(format(i, "09b"), 0)) for i in range(512)}
    if sum(words.values()) != args.shots:
        raise ValueError("returned words do not account for all attempted shots")
    report = {
        "provenance": "ideal circuit simulator", "qasm_sha256": hashlib.sha256(source).hexdigest(),
        "versions": {name: version(name) for name in ("qiskit", "qiskit-aer", "qiskit-qasm3-import")},
        "shots": args.shots, "seed": args.seed, "optimization_level": 0, "threads": 2,
        "method": "statevector", "shot_branching_enable": True,
        "bit_order": "y3 then y2 then y1, each printed most significant bit first",
        "counts": words,
    }
    with args.output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(report, stream, indent=2)
        stream.write("\n")
    for y1 in (6, 2):
        row = [words[format(y1 + 64*y3, "09b")] for y3 in range(8)]
        print(f"first code {y1}, second code 0, final code 0 through 7: {row}")


if __name__ == "__main__":
    main()
