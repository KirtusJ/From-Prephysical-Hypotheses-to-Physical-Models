"""Finite-shot weak-tag attack and trusted-only revival of the same source.

    python -I -B replay_leaking_source.py new_replay.json

The output is a local ideal-circuit simulation with one histogram per arm.
The data arm measures the input rail and prepares a fresh output qubit
using classical outcomes. The trusted analyzer receives that output only.
The other arms call the six-qubit source inverse at the release cut.
"""

import argparse
import hashlib
import json
import math
from fractions import Fraction
from importlib.metadata import version
from pathlib import Path
from runpy import run_path

from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator


SOURCE = run_path(str(Path(__file__).with_name("coherent_source_revival.py")))
ANGLE = 2*math.atan(1/7)
ARMS = ("measure_prepare", "trusted_inverse", "erase_tag_then_inverse")


def apply_source(circuit, sequence):
    for name, controls, target in sequence:
        if name == "h":
            if controls:
                if len(controls) != 1:
                    raise ValueError("unsupported source control")
                circuit.ch(controls[0], target)
            else:
                circuit.h(target)
        elif name == "x" and controls:
            circuit.mcx(list(controls), target)
        else:
            raise ValueError(f"unsupported source gate {name} with {controls}")


def build(arm, defer=False):
    science = arm == "measure_prepare"
    width = 5 if science else 6
    circuit = QuantumCircuit(8 if science else 7, 0 if defer else width)
    apply_source(circuit, SOURCE["FORWARD"])
    circuit.ry(ANGLE, 6)
    circuit.cz(4, 6)
    circuit.barrier()  # The same tagged release state on every arm.
    if not science:
        if arm == "erase_tag_then_inverse":
            circuit.cz(4, 6)
            circuit.ry(-ANGLE, 6)
        elif arm != "trusted_inverse":
            raise ValueError(f"unknown arm {arm}")
        apply_source(circuit, SOURCE["REVERSE"])
        if not defer:
            circuit.measure(range(6), range(6))
        return circuit

    circuit.h(6)  # X-basis Helstrom guess about the source basis.
    if defer:
        # Exact joint-law cross-check. Keep both detector outcomes in
        # orthogonal registers, then sum over unreported address bits.
        circuit.ch(6, 0)
        circuit.cx(0, 7)
        circuit.ch(6, 7)
        circuit.barrier()
        circuit.ch(4, 7)
    else:
        circuit.measure(6, 2)
        with circuit.if_test((circuit.clbits[2], True)):
            circuit.h(0)
        circuit.measure(0, 3)
        with circuit.if_test((circuit.clbits[3], True)):
            circuit.x(7)
        with circuit.if_test((circuit.clbits[2], True)):
            circuit.h(7)
        circuit.barrier()  # The sender has committed its fresh output qubit.
        circuit.measure(4, 0)
        circuit.measure(5, 1)
        with circuit.if_test((circuit.clbits[0], True)):
            circuit.h(7)
        circuit.measure(7, 4)
    return circuit


def analytic(arm, index):
    if arm == "measure_prepare":
        b, s, guess, detected, final = ((index >> bit) & 1 for bit in range(5))
        if guess == b:
            return Fraction(4, 25) if detected == final == s else Fraction(0)
        return Fraction(9, 400)
    if arm == "trusted_inverse":
        # (7 U|0>|0> + Z_basis U|0>|1>)/sqrt(50). Conjugating the record
        # phase by U flips exactly the incident rail bit on the zero input.
        return {0: Fraction(49, 50), 1: Fraction(1, 50)}.get(index, Fraction(0))
    return Fraction(index == 0)


def success(arm, index):
    if arm == "measure_prepare":
        return (index >> 4) & 1 == (index >> 1) & 1
    return index == 0


def check_exact(arm):
    circuit = build(arm, defer=True)
    bits = (4, 5, 6, 0, 7) if arm == "measure_prepare" else tuple(range(6))
    probabilities = Statevector.from_instruction(circuit).probabilities(qargs=bits)
    error = max(abs(value - float(analytic(arm, i))) for i, value in enumerate(probabilities))
    if error > 1e-12:
        raise ValueError(f"deferred readout disagreed with analytic joint law: {arm}, {error}")
    target = sum(analytic(arm, i) for i in range(len(probabilities)) if success(arm, i))
    if target != dict(zip(ARMS, (Fraction(41, 50), Fraction(49, 50), Fraction(1))))[arm]:
        raise ValueError(f"incorrect exact score {arm}")
    return target


def replay(shots, seed):
    backend = AerSimulator(method="statevector", max_parallel_threads=2, shot_branching_enable=True)
    source_bytes = Path(SOURCE["__file__"]).read_bytes().replace(b"\r\n", b"\n")
    result = {"schema": "coherent-source-weak-tag-v1", "provenance": "ideal Qiskit Aer simulation",
              "source_sha256_lf": hashlib.sha256(source_bytes).hexdigest(),
              "versions": {name: version(name) for name in ("qiskit", "qiskit-aer")},
              "tag": "Ry(2 atan(1/7)) on q6 followed by CZ(q4,q6)",
              "word_order": {"measure_prepare": "final, detected, guessed basis, sign, basis",
                             "inverse_arms": "q5,q4,q3,q2,q1,q0 (trusted qubits only)"},
              "arms": {}}
    for offset, arm in enumerate(ARMS):
        target = check_exact(arm)
        program = transpile(build(arm), backend, optimization_level=0, seed_transpiler=seed+offset)
        run = backend.run(program, shots=shots, seed_simulator=seed+offset).result()
        counts = run.get_counts()
        width = 5 if arm == "measure_prepare" else 6
        full = {f"{i:0{width}b}": 0 for i in range(1 << width)}
        if not run.success or sum(counts.values()) != shots or counts.keys() - full.keys():
            raise ValueError(f"incomplete or invalid words in {arm}")
        full.update(counts)
        if any(n and not analytic(arm, int(word, 2)) for word, n in full.items()):
            raise ValueError(f"forbidden outcome in {arm}")
        hits = sum(n for word, n in full.items() if success(arm, int(word, 2)))
        # For three independent-shot simulator arms, the three two-sided
        # Hoeffding intervals cover simultaneously with probability >= 0.99.
        radius = math.sqrt(math.log(600)/(2*shots))
        result["arms"][arm] = {"shots": shots, "seed": seed+offset, "successes": hits,
                               "analytic_score": str(target),
                               "within_simultaneous_99pct_hoeffding_radius":
                                   abs(hits/shots - float(target)) <= radius,
                               "counts": full}
        print(f"{arm}: {hits}/{shots}, reference {target}")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="new JSON output path")
    parser.add_argument("--shots", type=int, default=16384, help="incident trials per arm")
    parser.add_argument("--seed", type=int, default=26041, help="first arm seed (next two consecutive)")
    args = parser.parse_args()
    if args.output.exists() or args.shots <= 0 or not 0 <= args.seed <= 2**32-3:
        parser.error("supply a fresh output file, positive shot count and a valid seed")
    payload = replay(args.shots, args.seed)
    with args.output.open("x", encoding="utf-8", newline="\n") as out:
        out.write(json.dumps(payload, indent=2) + "\n")
