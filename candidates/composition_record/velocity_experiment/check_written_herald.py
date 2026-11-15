"""Check the actual herald instrument on the four-dimensional prepared code.

    python -I -B check_written_herald.py
    python -I -B check_written_herald.py --qasm fresh.qasm
    python -I -B check_written_herald.py --qiskit

The QASM has three recorded bits: the actual science herald, a fresh query
after that write (1 for Bell return, 0 for sector check), and its answer.
The exact checks use signed amplitudes of the six-wire gate and no hardware.
"""
import argparse
from fractions import Fraction as F
from math import sqrt
from pathlib import Path
from runpy import run_path

lib = run_path(str(Path(__file__).with_name("check_amplified_herald.py")))
require = lib["require"]
GOOD = frozenset(lib["GOOD"])
DIM = 4
DEN = 32 * DIM


def gram(v, w):
    # Joint Choi vector with external reference r and physical output k.
    return sum(a*b for x, y in zip(v, w) for a, b in zip(x, y)) / F(DEN)


def restrict(cols, good):
    return [[a if ((k in GOOD) == good) else 0 for k, a in enumerate(v)] for v in cols]


def check_fidelity_boundary(psi, branch, opposite, s):
    # Pick f=s*a² and alpha=(1-s)*b². This leaves the amplitudes of
    # v=sqrt(f)g+sqrt(alpha)b_sector rational in the original column units.
    twisted = [[(-v if i & 1 else v) for v in row] for i, row in enumerate(branch)]
    require(gram(psi, twisted) == gram(branch, twisted) == 0, "traceless branch twist")
    for a, b in ((1, 0), (F(1,2), F(1,3)), (1, 1)):
        v = [[a*g+b*h for g,h in zip(gs, bs)] for gs,bs in zip(branch, opposite)]
        f, alpha = s*a*a, (1-s)*b*b
        rest = 1-alpha-f
        require(rest >= 0 and gram(v,v)+rest == 1, "positive unit-trace branch state")
        require(gram(branch, v)**2/s == f and gram(opposite, v)**2/(1-s) == alpha,
                "attained target fidelity and sector mismatch")
        require(gram(psi, v)**2 == (s*a+(1-s)*b)**2, "attained Bell-return bound")
        for i in range(DIM):
            for j in range(DIM):
                trace = lib["dot"](v[i], v[j]) + rest/s * lib["dot"](twisted[i], twisted[j])
                require(trace == 32*int(i == j), "reference marginal is maximally mixed")
    # A positive return is possible with *zero* target fidelity. Half of the
    # opposite-sector population is in its Bell target and half in its twist.
    alpha = F(1,3)
    beta = (1-s)*alpha/2
    require(1-alpha + beta/(1-s) + (alpha-beta/(1-s)) == 1
            and beta < (1-s)*alpha, "zero-fidelity side of the sharp bound")


def check():
    psi = lib["isometry_numerators"]()
    require(gram(psi, psi) == 1, "normalized Bell preparation")
    total_return = F(0)
    for good, s in ((True, F(5, 16)), (False, F(11, 16))):
        branch = restrict(psi, good)
        require(gram(branch, branch) == s and gram(psi, branch)**2 == s*s,
                "ideal label and joint return rates")
        for i in range(DIM):
            for j in range(DIM):
                value = lib["dot"](branch[i], branch[j]) / F(32)
                require(value == s * (i == j), "full branch isometry")
        check_fidelity_boundary(psi, branch, restrict(psi, not good), s)
        total_return += gram(psi, branch)**2

        # A perfect copy of logical control (wire q1) preserves the declared
        # label and every logical basis input, but costs half of the Bell return.
        recorded = []
        for bit in (0, 1):
            sub = [[a if (k >> 1) & 1 == bit else 0 for k, a in enumerate(v)]
                   for v in branch]
            recorded.append(sub)
            require(gram(sub, sub) == s/2, "fine copy probability")
        require(sum(gram(psi, v)**2 for v in recorded) == s*s/2, "hidden control copy")
        for i in range(DIM):
            require(recorded[i >> 1][i] == branch[i], "copy invisible to basis-only probes")

        # Without the sector check choose the same label rates and then
        # transmit the whole unprojected code, optionally applying an input Z.
        twisted = [[(-a if i & 1 else a) for a in row] for i, row in enumerate(psi)]
        require(gram(psi, twisted) == 0 and gram(twisted, twisted) == 1, "orthogonal Bell state")
        hit = s*gram(psi, psi)**2 + (1-s)*gram(psi, twisted)**2
        match = s*gram(restrict(psi, good), restrict(psi, good)) + (1-s)*gram(
            restrict(twisted, good), restrict(twisted, good))
        require(hit == s and match == s, "correct return, wrong sector")
    require(total_return == F(73, 128), "total ideal post-write return probability")
    require(F(55,128)/2 + F(73,128)*F(25,146) == F(5,16),
            "per-mode rate variation under exactly the same averaged instrument")
    print("Ideal good/bad label: 5/16, 11/16. Joint Bell returns: 25/256, 121/256.")
    print("A hidden logical-control copy halves each Bell return; basis tests miss the copy.")
    print("Omitting sector verification admits exact ideal label and return counts.")


def pointer(wires):
    flips = ["x " + w + ";" for w in wires]
    controls = ", ".join([*wires, "verify"])
    return [*flips, f"ctrl({len(wires)}) @ x {controls};", *reversed(flips)]


def circuit():
    core = lib["reference"]["small_qasm"](False)
    header, body = core.split("qubit[6] q;\n")
    gates = body.splitlines()
    registers = ["qubit[6] q;", "qubit[2] ref;", "qubit herald_pointer;",
                 "qubit query;", "qubit verify;", "bit herald;", "bit test;", "bit answer;"]
    entangle = ["h ref[0];", "cx ref[0], q[0];", "h ref[1];", "cx ref[1], q[1];"]
    mask = tuple(f"q[{i}]" for i in (2, 3, 4))
    first_write = [line.replace("verify", "herald_pointer") for line in pointer(mask)]
    all_data = tuple(f"q[{i}]" for i in range(6)) + ("ref[0]", "ref[1]")
    ret = [*reversed(gates), *reversed(entangle), *pointer(all_data)]
    sector = pointer(mask)
    lines = [header.rstrip(), *registers, *entangle, *gates, *first_write,
             "herald = measure herald_pointer;", "h query;", "test = measure query;",
             "if (test) {", *("  " + ln for ln in ret),
             "} else {", *("  " + ln for ln in sector), "}", "answer = measure verify;"]
    return "\n".join(lines) + "\n"


def qiskit_check():
    """Exact projected branches of the parsed dynamic QASM, without shot sampling."""
    import numpy as np
    from qiskit import QuantumCircuit, qasm3
    from qiskit.quantum_info import Statevector

    qc = qasm3.loads(circuit())
    positions = {c: i for i, c in enumerate(qc.clbits)}

    def propagate(ops, state, seen, mass):
        if not ops:
            yield tuple(seen[i] for i in range(3)), mass
            return
        inst, *tail = ops
        op, wires, bits = inst
        if op.name == "measure":
            bit, wire = bits[0], wires[0]
            for value in (0, 1):
                arr = state.data.copy()
                arr[((np.arange(len(arr)) >> wire) & 1) != value] = 0
                p = float(np.vdot(arr, arr).real)
                if p > 1e-14:
                    yield from propagate(tail, Statevector(arr/sqrt(p)), {**seen, bit:value}, mass*p)
        elif op.name == "if_else":
            cond, val = op.condition
            which = 0 if bool(seen[positions[cond]]) == bool(val) else 1
            block = op.blocks[which]
            extra = [(cmd.operation, [wires[block.find_bit(q).index] for q in cmd.qubits],
                      [bits[block.find_bit(b).index] for b in cmd.clbits]) for cmd in block.data]
            yield from propagate(extra + tail, state, seen, mass)
        else:
            # Group unitary instructions through the next real measurement.
            count = 1
            gather = QuantumCircuit(qc.num_qubits)
            gather.append(op, wires)
            while count < len(ops) and ops[count][0].name not in ("measure", "if_else"):
                gate, on, _ = ops[count]
                gather.append(gate, on)
                count += 1
            yield from propagate(ops[count:], state.evolve(gather), seen, mass)

    seq = [(cmd.operation, [qc.find_bit(q).index for q in cmd.qubits],
            [positions[b] for b in cmd.clbits]) for cmd in qc.data]
    actual = dict(propagate(seq, Statevector.from_int(0, 2**qc.num_qubits), {}, 1.0))
    want = {}
    for z, s in ((1, F(5,16)), (0, F(11,16))):
        want[z, 0, z] = s/2
        want[z, 1, 1] = s*s/2
        want[z, 1, 0] = s*(1-s)/2
    require(set(actual) == set(want)
            and max(abs(actual[k]-float(v)) for k, v in want.items()) < 2e-9,
            "actual dynamic instrument branches")
    print("Qiskit dynamic QASM: all six bright and two dark (z,test,answer) rows verified.")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--qasm", type=Path, help="export the genuine write and delayed random check")
    p.add_argument("--qiskit", action="store_true", help="propagate every parsed dynamic branch")
    args = p.parse_args()
    check()
    if args.qiskit:
        qiskit_check()
    if args.qasm:
        with args.qasm.open("x", encoding="ascii", newline="\n") as out:
            out.write(circuit())


if __name__ == "__main__":
    main()
