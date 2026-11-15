"""Exact gate and record replay. Optional Aer samples a fixed number of genuine writes."""

import argparse
from collections import Counter
from fractions import Fraction
from itertools import product
import json
from pathlib import Path


def require(value, message):
    if not value:
        raise ArithmeticError(message)


# Qubit 0 is the rail, qubits 1 and 2 are the low and high selector bits.
# Open controls are written as positive controls bracketed by X. The rail H
# pair acts on every address; together with CCX it realizes the addressed Z.
GATES = (
    ("h", 1), ("h", 2),
    ("x", 2), ("ccx", 1, 2, 0), ("x", 2),
    ("x", 1), ("h", 0), ("ccx", 1, 2, 0), ("h", 0), ("x", 1),
    ("h", 1), ("h", 2),
)
IDENTITY = (1, 0, 0, 1)


def multiply(a, b):
    x, y, z, w = a
    r, s, t, u = b
    return x*r+y*t, x*s+y*u, z*r+w*t, z*s+w*u


def transpose(a):
    return a[0], a[2], a[1], a[3]


def raw_matrices():
    columns = []
    for rail in (0, 1):
        state = [int(i == rail) for i in range(8)]
        for gate, *bits in GATES:
            result = [0] * 8
            flip = 1 << bits[-1]
            for i, amplitude in enumerate(state):
                if gate == "h":
                    result[i & ~flip] += amplitude
                    result[i | flip] += -amplitude if i & flip else amplitude
                else:
                    active = all(i & (1 << control) for control in bits[:-1])
                    result[i ^ flip if active else i] += amplitude
            state = result
        columns.append(state)
    # Six H numerators were used, so all columns have common denominator eight.
    result = []
    for selector in range(4):
        row = 2*selector
        result.append((columns[0][row], columns[1][row],
                       columns[0][row+1], columns[1][row+1]))
    expected = [(6, 2, 2, 2), (2, -2, -2, -2),
                (-2, 2, 2, 2), (2, -2, -2, 6)]
    require(result == expected, f"Physical selector produced {result}")
    correction = (-1, 1, 1, 1)  # numerator of X H X
    for selector in (1, 2):
        corrected = multiply(correction, result[selector])
        require(corrected in [(4, 0, 0, 4), (-4, 0, 0, -4)],
                "Null correction failed to restore the entire rail")
    require(tuple(map(sum, zip(*(multiply(transpose(m), m) for m in result))))
            == (64, 0, 0, 64), "Instrument is incomplete")
    return result


def word_law(rounds, matrices, correct=True):
    # I/2 on the input rail. Each entry remains an unnormalized matrix on that rail.
    states = {(): tuple(Fraction(x, 2) for x in IDENTITY)}
    for _ in range(rounds):
        next_states = {}
        for path, state in states.items():
            for label, matrix in enumerate(matrices):
                if correct and label in (1, 2):
                    output = tuple(x/8 for x in state)
                else:
                    raw = multiply(multiply(matrix, state), transpose(matrix))
                    output = tuple(x/64 for x in raw)
                next_states[path + (label,)] = output
        states = next_states
    law = {path: state[0] + state[3] for path, state in states.items()}
    require(sum(law.values()) == 1, "Incident input normalization")
    return law


def group(law, boundary):
    """First boundary by the penultimate write, probe immediately after it."""
    cap = len(next(iter(law))) - 1
    groups = Counter()
    for path, mass in law.items():
        score = 0
        for clock, label in enumerate(path[:cap], 1):
            score += int(label == 0) - int(label == 3)
            if abs(score) == boundary:
                # Code 0 dark; 1 is raw +; 2 is raw - or null 01; 3 is null 10.
                code = (1, 2, 3, 2)[path[clock]]
                groups[(score, code)] += mass
                break
        else:
            groups[(0, -1)] += mass
    require(sum(groups.values()) == sum(law.values()), "Lost a censored trial")
    return groups


def expected_probe(boundary):
    # In the ring of matrices xI+yB with B=X+Z and B^2=2I.
    x, y = 1, 0
    for _ in range(boundary):
        x, y = 2*x + 2*y, x + 2*y
    coefficient = Fraction(2*x*y, x*x + 2*y*y)
    return {sign: (0, Fraction(3, 8) + sign*coefficient/2,
                   Fraction(1, 2) - sign*coefficient/2, Fraction(1, 8))
            for sign in (-1, 1)}


def aer_words(rounds, shots, seed):
    import qiskit
    import qiskit_aer
    from qiskit import ClassicalRegister, QuantumCircuit, transpile
    from qiskit_aer import AerSimulator

    qc = QuantumCircuit(4)
    qc.h(3)
    qc.cx(3, 0)  # purify I/2; subsequently qubit 3 is untouched
    for i in range(rounds):
        read = ClassicalRegister(2, f"r{i}")
        qc.add_register(read)
        for gate, *bits in GATES:
            getattr(qc, gate)(*bits)
        qc.measure([1, 2], read)
        for null in (1, 2):
            with qc.if_test((read, null)):
                qc.x(0)
                qc.h(0)
                qc.x(0)
        if i + 1 < rounds:
            qc.reset(1)
            qc.reset(2)
    sim = AerSimulator(method="statevector", max_parallel_threads=3, shot_branching_enable=True)
    compiled = transpile(qc, sim, optimization_level=0, seed_transpiler=seed)
    output = sim.run(compiled, shots=shots, seed_simulator=seed).result()
    words = {tuple(int(bits, 2) for bits in reversed(word.split())): count
             for word, count in output.get_counts().items()}
    require(sum(words.values()) == shots, "Aer shot accounting")
    return words, {"qiskit": qiskit.__version__, "qiskit_aer": qiskit_aer.__version__,
                   "method": "statevector", "seed": seed, "shots": shots}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--aer", action="store_true")
    parser.add_argument("--shots", type=int, default=32768)
    parser.add_argument("--seed", type=int, default=269271)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    matrices = raw_matrices()
    rounds = 4
    law = word_law(rounds, matrices)
    require(len(law) == 4**rounds, "Wrong complete panel")
    corrected, uncorrected = (word_law(3, matrices, flag) for flag in (True, False))
    require(corrected[(0, 1, 0)] == Fraction(17, 512) and
            uncorrected[(0, 1, 0)] == Fraction(1, 512), "Null correction control")
    results = {}
    for boundary in (1, 2):
        groups = group(law, boundary)
        expected = expected_probe(boundary)
        for sign in (-1, 1):
            total = sum(groups[(sign*boundary, i)] for i in range(4))
            row = tuple(groups[(sign*boundary, i)]/total for i in range(4))
            require(row == expected[sign], "Probe row disagrees with stopped-state prediction")
        print(f"boundary {boundary}, censored {groups[(0, -1)]}, "
              f"plus {[str(x) for x in expected[1]]}, minus {[str(x) for x in expected[-1]]}")
        results[str(boundary)] = {f"{a},{b}": str(n) for (a,b), n in sorted(groups.items())}
    report = {"cap": 3, "rounds": rounds, "exact_groups": results}
    if args.aer:
        words, metadata = aer_words(rounds, args.shots, args.seed)
        report["simulator"] = metadata
        report["complete_words"] = {
            "".join(map(str, word)): {"probability": str(law[word]), "count": words.get(word, 0)}
            for word in product(range(4), repeat=rounds)
        }
        tv = sum(abs(Fraction(words.get(w, 0),args.shots)-law[w]) for w in law)/2
        report["empirical_total_variation"] = str(tv)
        report["observed_groups"] = {
            str(m): {f"{a},{b}": n for (a,b),n in sorted(group(words,m).items())} for m in (1,2)
        }
        print(f"Aer {args.shots} shots, all {len(law)} bins, observed TV {tv}")
    if args.out:
        with args.out.open("x", encoding="utf-8") as target:
            json.dump(report, target, indent=2)
            target.write("\n")


if __name__ == "__main__":
    main()
