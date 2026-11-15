"""Check the six-wire gate when its Pell-selector wire is a third logical input.

Run python -I -B check_open_pell_wire.py [--qiskit]. In a separate replay
directory, pass --source-dir pointing to the velocity_experiment directory.
--qasm PATH exports the delayed-choice circuit; --mark-selector includes the
adverse physical measurement of q5 in the X basis. All reported rates refer
to all launches. The optional simulator enumerates measurement branches.
"""

import argparse
from fractions import Fraction as F
from math import sqrt
from pathlib import Path
from runpy import run_path


EIGENVALUES = ((F(1, 16), F(1, 8)), (F(9, 16), F(1, 2)))
LABEL = (F(11, 16), F(5, 16))  # Bad, good.
MARKED_RETURN = (F(533, 2048), F(149, 2048))


def require(ok, message):
    if not ok:
        raise ArithmeticError(message)


def columns(reference):
    """W on q0,q1,q5 in computational order, scaled by 4 sqrt(2)."""
    pair, capacity, _ = reference["parameters"](2)
    routing = [reference["routed_columns"](a, b, capacity) for a, b in pair]
    result = []
    for i in range(8):
        selector, logical = divmod(i, 4)
        column = []
        for row in range(64):
            branch, flag, path, dst = row >> 5, (row >> 4) & 1, (row >> 2) & 3, row & 3
            sign = -1 if selector and branch else 1
            column.append(sign * routing[branch][flag][path][4 * dst + logical])
        result.append(column)
    return result


def exact_check(cols):
    for z, rate in enumerate(LABEL):
        routed = [[v if int((row & 28) == 0) == z else 0 for row, v in enumerate(col)]
                  for col in cols]
        effect = [[F(sum(a*b for a, b in zip(left, right)), 32) for right in routed]
                  for left in routed]
        weights = []
        for selector, sign in enumerate((1, -1)):
            trace = 0
            for j in range(4):
                control = j >> 1
                eigen = EIGENVALUES[selector][control]
                if z == 0:
                    eigen = 1 - eigen
                for i in range(8):
                    lhs = effect[i][j] + sign * effect[i][j+4]
                    rhs = eigen * (int(i == j) + sign*int(i == j+4))
                    require(lhs == rhs, "full effect on X-selector eigenbasis")
                # X-basis measurement restricts columns to P+ or P- on input;
                # compare all physical output rails, including failed paths.
                for k in range(64):
                    branch = k >> 5
                    amplitude = routed[j][k] + sign*routed[j+4][k]
                    require(branch == selector or amplitude == 0,
                            "selector eigenstate changed or leaked to wrong routing")
                trace += eigen
            weights.append(trace / 8)
        expected = (F(29,64), F(15,64)) if z == 0 else (F(3,64), F(17,64))
        require(tuple(weights) == expected and sum(weights) == rate, "branch trace")
        require(sum(w*w for w in weights) == MARKED_RETURN[z], "marked Bell return")
        require(sum(effect[j][j] for j in range(8))/8 == rate, "full Bell norm")
        if z == 0:
            bad = effect
        else:
            require(all(effect[i][j] + bad[i][j] == int(i == j)
                        for i in range(8) for j in range(8)), "effect normalization")
    print("64 by 8 signed amplitudes; both 8 by 8 effects normalized. "
          "Good spectra on selector + and -: (1/16, 1/8), (9/16, 1/2), each twice.")
    print("Label G,B = 5/16,11/16. Sector errors zero. Joint Bell returns G,B: "
          "ideal 25/256,121/256; early selector measurement 149/2048,533/2048.")


def circuit(reference, pointer, marked):
    header, body = reference["small_qasm"](False).split("qubit[6] q;\n")
    gates = body.splitlines()  # Every gate in this router is self-adjoint.
    data = [f"q[{i}]" for i in range(6)] + [f"ref[{i}]" for i in range(3)]
    sector = [f"q[{i}]" for i in (2, 3, 4)]
    entangle = [line for j, wire in enumerate((0, 1, 5))
                for line in (f"h ref[{j}];", f"cx ref[{j}], q[{wire}];")]
    lines = [header.rstrip(), "qubit[6] q;", "qubit[3] ref;", "qubit herald_pointer;",
             "qubit query;", "qubit verify;", "bit herald;", "bit test;", "bit answer;"]
    if marked:
        lines += ["bit hidden;"]
    lines += entangle
    if marked:
        lines += ["h q[5];", "hidden = measure q[5];", "h q[5];"]
    lines += gates + [gate.replace("verify", "herald_pointer") for gate in pointer(sector)]
    lines += ["herald = measure herald_pointer;", "h query;", "test = measure query;",
              "if (test) {"]
    lines += ["  " + gate for gate in [*reversed(gates), *reversed(entangle), *pointer(data)]]
    lines += ["} else {", *["  " + gate for gate in pointer(sector)], "}",
              "answer = measure verify;"]
    return "\n".join(lines) + "\n"


def qiskit_table(qc):
    """Enumerate final public-clbit probabilities, summing the optional private bit."""
    import numpy as np
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Statevector

    def instructions(block, qubits, bits):
        return [(cmd.operation, [qubits[block.find_bit(q).index] for q in cmd.qubits],
                 [bits[block.find_bit(b).index] for b in cmd.clbits]) for cmd in block.data]

    def propagate(ops, state, seen, weight):
        while ops:
            op, wires, bits = ops[0]
            if op.name == "measure":
                for value in range(2):
                    arr = state.data.copy()
                    arr[((indices >> wires[0]) & 1) != value] = 0
                    prob = float(np.vdot(arr, arr).real)
                    if prob > 1e-13:
                        propagate(ops[1:], Statevector(arr/sqrt(prob)),
                                  {**seen, bits[0]: value}, weight*prob)
                return
            if op.name == "if_else":
                condition, expected = op.condition
                branch = int(seen[qc.find_bit(condition).index] != expected)
                ops = instructions(op.blocks[branch], wires, bits) + ops[1:]
                continue
            run = QuantumCircuit(qc.num_qubits)
            n = 0
            while n < len(ops) and ops[n][0].name not in ("if_else", "measure"):
                run.append(ops[n][0], ops[n][1])
                n += 1
            state, ops = state.evolve(run), ops[n:]
        key = tuple(seen[i] for i in range(3))
        public[key] = public.get(key, 0.0) + weight

    public = {}
    indices = np.arange(1 << qc.num_qubits)
    propagate(instructions(qc, range(qc.num_qubits), range(qc.num_clbits)),
              Statevector.from_int(0, len(indices)), {}, 1.0)
    return public


def check_qiskit(reference, pointer, cols):
    import numpy as np
    from qiskit import qasm3
    from qiskit.quantum_info import Statevector

    native = qasm3.loads(reference["small_qasm"](False))
    raw = np.array([Statevector.from_int((i & 3) + ((i >> 2) << 5), 64)
                    .evolve(native).data for i in range(8)]).T
    require(np.max(np.abs(raw - np.asarray(cols).T/sqrt(32))) < 1e-10,
            "QASM mismatch on signed entries")
    good = raw[(np.arange(64) & 28) == 0, :]
    eigen = np.linalg.eigvalsh(good.conj().T @ good)
    target = sorted(float(v) for row in EIGENVALUES for v in row for _ in range(2))
    require(np.max(np.abs(eigen-target)) < 1e-10, "numerical effect eigenvalues")
    for marked in (False, True):
        qc = qasm3.loads(circuit(reference, pointer, marked))
        require(qc.num_qubits == 12, "dynamic circuit width")
        counts = qiskit_table(qc)
        wanted = {}
        for z, s in enumerate(LABEL):
            ret = MARKED_RETURN[z] if marked else s*s
            wanted[z, 0, z] = s/2
            wanted[z, 1, 1] = ret/2
            wanted[z, 1, 0] = (s-ret)/2
        require(set(wanted) == set(counts) and
                max(abs(counts[key] - float(prob)) for key, prob in wanted.items()) < 2e-9,
                "dynamic herald/query/answer probabilities")
    print("Qiskit: 512 complex entries, spectrum, and 12-qubit dynamic public tables "
          "including dark rows agree for the ideal and marked instruments.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, default=Path(__file__).parent)
    parser.add_argument("--qasm", type=Path, help="write a fresh OpenQASM 3 file")
    parser.add_argument("--mark-selector", action="store_true", help="include X read in export")
    parser.add_argument("--qiskit", action="store_true", help="run both 12-qubit dynamic checks")
    args = parser.parse_args()
    written = run_path(str(args.source_dir/"check_written_herald.py"))
    reference = written["lib"]["reference"]
    pointer = written["pointer"]
    cols = columns(reference)
    exact_check(cols)
    if args.qiskit:
        check_qiskit(reference, pointer, cols)
    if args.qasm:
        with args.qasm.open("x", encoding="ascii", newline="\n") as out:
            out.write(circuit(reference, pointer, args.mark_selector))


if __name__ == "__main__":
    main()
