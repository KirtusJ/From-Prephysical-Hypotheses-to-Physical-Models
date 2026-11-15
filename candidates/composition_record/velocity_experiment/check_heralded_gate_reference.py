"""Check a heralded rational approximation to I (+) H (two control sectors).

    python -I -B check_heralded_gate_reference.py
    python -I -B check_heralded_gate_reference.py --qasm new_reference.qasm
    python -I -B check_heralded_gate_reference.py --qiskit

n is the larger of two consecutive Pell indices. The six-qubit n=2 export
prepares control +, target R and measures control X, keeping every record.
Bit order (high to low): Pell branch, reject flag, two path bits, control
X result, target Z result. Success requires both path bits and reject=0.
The two Pell branch outcomes are pooled. --qiskit independently propagates
the four input columns of the actual signed routing circuit, including the
failure outputs. Only this extra check needs Qiskit and its QASM 3 importer.
"""

import argparse
from fractions import Fraction
from math import cos, pi, sin, sqrt
from pathlib import Path


def require(ok, reason):
    if not ok:
        raise ArithmeticError(reason)


def pell(index):
    a, b = 1, 0
    for _ in range(index):
        a, b = a + 2*b, a + b
    return a, b


def parameters(n):
    if n < 2:
        raise ValueError("n must be at least two")
    pair = (pell(n-1), pell(n))
    needed = max(max(a, 2*b) for a, b in pair)
    capacity = 1 << (needed-1).bit_length()
    return pair, capacity, sum(a*a for a, _ in pair)


def routing(a, b, control, path):
    if control == 0:
        return "I" if path < a else "reject"
    if path < b:
        return "Z"
    return "X" if path < 2*b else "reject"


def routed_columns(a, b, capacity):
    """Raw 4x4 Kraus numerators by final reject flag and path read.

    Columns/rows index 2*control+rail. Include every path, including
    rejected ones. An unnormalized Walsh transform implements the d output
    Hadamards after the d input Hadamards; the net divisor is capacity.
    """
    table = [[[0]*16 for _ in range(capacity)] for _ in range(2)]
    for path in range(capacity):
        for src in range(4):
            control, rail = divmod(src, 2)
            choice = routing(a, b, control, path)
            dst = src ^ int(choice == "X")
            sign = -1 if choice == "Z" and rail else 1
            table[int(choice == "reject")][path][4*dst+src] = sign
    for rows in table:
        stride = 1
        while stride < capacity:
            for base in range(0, capacity, 2*stride):
                for i in range(base, base+stride):
                    x, y = rows[i], rows[i+stride]
                    rows[i] = [s+t for s,t in zip(x,y)]
                    rows[i+stride] = [s-t for s,t in zip(x,y)]
            stride *= 2
    return table


def accumulate_gram(total, mat):
    for i in range(4):
        for j in range(4):
            total[4*i+j] += sum(mat[4*k+i]*mat[4*k+j] for k in range(4))


def identity(scale):
    return [scale if i % 5 == 0 else 0 for i in range(16)]


def check(n):
    pair, capacity, P = parameters(n)
    success, failure = [0]*16, [0]*16
    cross = 0
    for j, (a,b) in enumerate(pair, n-1):
        require(a*a-2*b*b == (-1)**j, "Pell sign")
        blocks = routed_columns(a,b,capacity)
        K = blocks[0][0]
        require(K == [a,0,0,0, 0,a,0,0, 0,0,b,b, 0,0,b,-b], "heralded routing")
        # Once ideal C is divided out, the two sector multipliers are
        # a and sqrt(2)*b. Accumulate the rational part of their product.
        cross += K[0]*K[10]
        for flag, rows in enumerate(blocks):
            for path, mat in enumerate(rows):
                accumulate_gram(success if flag == path == 0 else failure, mat)
    require(success == identity(P), "input-independent success")
    require(failure == identity(2*capacity**2-P), "full failure Gram")
    (a,b),(c,d) = pair
    require(a*d-b*c == (-1)**(n-1), "adjacent determinant")
    require(2*cross**2 == P**2-2, "dephasing coefficient squared")
    # Stable form of (1-sqrt(1-2/P²))/2. After removing C, dephasing
    # is a mixture of I and control Z with Z weight delta. The equal
    # control superposition distinguishes the two outputs perfectly.
    delta = 1/(P**2*(1+sqrt(1-2/P**2)))
    p = Fraction(P, 2*capacity**2)
    print(f"n={n} pair={pair} paths={capacity} success={p} "
          f"Choi infidelity=half diamond={delta:.10g}")
    return p, delta


def small_qasm(probe):
    pair, capacity, _ = parameters(2)
    require(capacity == 4, "n=2 register size")
    # q0 target, q1 control, q2 low and q3 high path bits, q4 reject,
    # q5 fair Pell index. Route choices read q5 in the Z basis alone.
    lines = ["OPENQASM 3.0;", 'include "stdgates.inc";', "qubit[6] q;"]
    if probe:
        lines += ["bit[6] record;", "h q[1]; // prepare control +"]
    lines += ["h q[5];", "h q[2];", "h q[3];"]
    controls = (5, 1, 2, 3)
    for branch, (a,b) in enumerate(pair):
        for control in range(2):
            for path in range(capacity):
                chosen = routing(a,b,control,path)
                if chosen == "I":
                    continue
                match = (branch, control, path & 1, path >> 1)
                toggles = [f"x q[{wire}];" for wire,bit in zip(controls,match) if not bit]
                name, target = ("x", 4) if chosen == "reject" else (chosen.lower(), 0)
                lines.extend(toggles)
                lines.append(f"ctrl(4) @ {name} q[5], q[1], q[2], q[3], q[{target}];")
                lines.extend(reversed(toggles))
    lines += ["h q[2];", "h q[3];"]
    if probe:
        lines += ["h q[1]; // read control X", "record = measure q;"]
    return "\n".join(lines)+"\n"


def check_qiskit():
    from qiskit import qasm3
    from qiskit.quantum_info import Statevector

    pair, cap, P = parameters(2)
    program = qasm3.loads(small_qasm(False))
    raw = []
    for src in range(4):
        initial = Statevector.from_int(src, 64)
        raw.append(initial.evolve(program).data)
    scale = 1/(cap*sqrt(2))
    for branch, (a,b) in enumerate(pair):
        routes = routed_columns(a,b,cap)
        for i in range(32):
            flag, path, dst = i >> 4, (i >> 2) & 3, i & 3
            for src in range(4):
                actual = raw[src][(branch << 5) + i]
                wanted = scale*routes[flag][path][4*dst+src]
                require(abs(actual-wanted) < 1e-11, "QASM Kraus column")

    # Two control signs times two normalized H eigenstates. Match the
    # ideal control-X outcome after conditioning on every reference success.
    p = P/(2*cap**2)
    coherence = sqrt(1-2/P**2)
    eigenspinors = ((1,(cos(pi/8),sin(pi/8))), (-1,(-sin(pi/8),cos(pi/8))))
    for phase in (1,-1):
        for eigen, spin in eigenspinors:
            incoming = tuple(s*factor/sqrt(2) for factor in (1,phase) for s in spin)
            accepted = correct = 0.0
            for branch in range(2):
                outputs = [sum(raw[src][(branch << 5)+dst]*incoming[src] for src in range(4))
                           for dst in range(4)]
                accepted += sum(abs(v)**2 for v in outputs)
                correct += sum(abs(outputs[r]+phase*eigen*outputs[2+r])**2/2 for r in range(2))
            require(abs(accepted-p) < 1e-11, "coherent input success")
            require(abs(correct/p-(1+coherence)/2) < 1e-11, "H eigenstate witness")
    # Verify the actually exported, rational sharp-rail witness as well.
    probe = qasm3.loads(small_qasm(True)).remove_final_measurements(inplace=False)
    probs = Statevector.from_instruction(probe).probabilities()
    accept = sum(probs[i] for i in range(64) if i & 0b11100 == 0)
    plus = sum(probs[i] for i in range(64) if i & 0b11110 == 0)
    require(abs(accept-p) < 1e-11 and abs(plus/p-17/20) < 1e-11, "exported control-X probe")
    print("n=2 QASM: all 256 full-output column entries, four control/eigenstate witnesses, "
          "and P(control X=+ | accepted, target R)=17/20 verified.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--qasm", type=Path, help="write the six-qubit n=2 probe to a fresh file")
    parser.add_argument("--qiskit", action="store_true", help="check the n=2 circuit with Statevector")
    args = parser.parse_args()
    for n in range(2,8):
        check(n)
    if args.qiskit:
        check_qiskit()
    if args.qasm:
        with args.qasm.open("x", encoding="ascii", newline="\n") as stream:
            stream.write(small_qasm(True))
