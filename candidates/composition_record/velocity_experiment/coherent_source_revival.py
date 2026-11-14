"""Six-qubit coherent source and release-cut revival on the sixteen-site ring.

    python -I -B coherent_source_revival.py
    python -I -B coherent_source_revival.py --tag parity --qasm new.qasm

Trusted q[0] is the rail, q[1:4] the little-endian count y of L shifts
modulo eight, and q[4], q[5] protected basis and sign records. At forward
tick t the physical site is (t-2*y) modulo 16. After the shifts at 1,9 the
two reachable sites are distinguished by the low address bit. Copy that
bit reversibly, and let q[4] control the Hadamard before shift 17.

A simulated orthogonal release tag uses zero, one or two extra qubits.
Only the six trusted qubits are measured after U-dagger. The optional
--erase-tag control deliberately gives the tester access to the copy.
This imports coherent records, a controlled H and reversible motion and
storage through the audit. It models a coherent implementation; classical
source measurements as in four_state_circuit.py cannot be inverted.
"""

import argparse
from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path
from typing import NamedTuple


class Gate(NamedTuple):
    name: str
    controls: tuple
    target: int


def x(target, *controls):
    return Gate("x", controls, target)


def h(target, *controls):
    return Gate("h", controls, target)


def source_ticks():
    # Increment y on L. Apply high carries before the two lower bits change.
    shift = (x(3, 0, 1, 2), x(2, 0, 1), x(1, 0))
    for tick in range(1, 25):
        before = (h(0),) if tick in (1, 9) else ()
        if tick == 17:
            before = (h(0, 4),)
        after = {1: (x(4, 1),), 9: (x(5, 1),)}.get(tick, ())
        yield before + shift + after


TICKS = tuple(source_ticks())
FORWARD = tuple(gate for tick in TICKS for gate in tick)
# Elementary X, H and their controlled forms are self-adjoint.
REVERSE = tuple(reversed(FORWARD))
TAGS = {"none": (), "basis": (x(6, 4),), "sign": (x(6, 5),),
        "parity": (x(6, 4), x(6, 5)), "both": (x(6, 4), x(7, 5))}


def require(condition, label):
    if not condition:
        raise ValueError(label)


def evolve(state, power, gates):
    """Sparse exact real amplitudes (a+b*sqrt(2))/sqrt(2)**power."""
    for gate in gates:
        out = {}
        def add(index, a, b):
            u, v = out.get(index, (0, 0))
            out[index] = (u + a, v + b)

        mask = 1 << gate.target
        for index, (a, b) in state.items():
            enabled = all(index & (1 << bit) for bit in gate.controls)
            if gate.name == "x":
                add(index ^ mask if enabled else index, a, b)
            elif enabled:
                add(index & ~mask, a, b)
                sign = -1 if index & mask else 1
                add(index | mask, sign*a, sign*b)
            else:
                # Inactive branch of a controlled H retains its amplitude.
                add(index, 2*b, a)
        state = {index: value for index, value in out.items() if value != (0, 0)}
        if gate.name == "h":
            power += 1
    return state, power


def probability(state, power, selected):
    rational = radical = 0
    for index, (a, b) in state.items():
        if selected(index):
            rational += a*a + 2*b*b
            radical += 2*a*b
    require(radical == 0, "this fixture predicts rational selected probabilities")
    return Fraction(rational, 1 << power)


def position(index, tick):
    left_steps = (index >> 1) & 7
    return (tick - 2*left_steps) % 16


def check_forward():
    state, power = {0: (1, 0)}, 0
    sites = {1: {1, 15}, 8: {8}, 9: {7, 9}, 16: {0}, 17: {1, 15}, 24: {8}}
    for tick, gates in enumerate(TICKS, 1):
        state, power = evolve(state, power, gates)
        if tick in sites:
            require({position(i, tick) for i in state} == sites[tick], f"sites at {tick}")
        if tick in (1, 9):
            bit = 4 if tick == 1 else 5
            require(all(i >> bit & 1 == i & 1 for i in state), f"direction write at {tick}")

    # Independent physical path calculation. Over each eight-shift flight
    # a fixed rail displaces +8 or -8, which coincide mod 16. H2 contributes
    # (-1)^(basis*sign). H3 on the X branch adds (-1)^(sign*output_rail).
    expected = {}
    for basis, sign, rail in product(range(2), repeat=3):
        key = (basis << 4) | (sign << 5) | rail  # y=0 at clock 24
        if basis:
            expected[key] = ((-1)**(basis*sign + sign*rail), 0)
        elif rail == sign:
            expected[key] = (0, 1)
    require(power == 3 and state == expected, "physical forward path phases")
    for label in range(4):
        require(probability(state, power, lambda i: i >> 4 == label) == Fraction(1, 4),
                f"label probability {label}")
    return state, power


def partition_probability(mode):
    # U† followed by 000000 tests the full incident pure source projector.
    # Tracing an orthogonal tag removes coherences between different groups.
    group_sizes = Counter()
    for basis, sign in product(range(2), repeat=2):
        group = {"none": 0, "basis": basis, "sign": sign, "parity": basis ^ sign,
                 "both": (basis, sign)}[mode]
        group_sizes[group] += 1
    return Fraction(sum(size**2 for size in group_sizes.values()), 16)


def check_all():
    state, power = check_forward()
    for initial in range(64):
        actual, p = evolve({initial: (1, 0)}, 0, FORWARD + REVERSE)
        require(p == 6 and actual == {initial: (8, 0)}, "inverse on trusted basis")
    print("Source at tick 24: x=8, four labels of weight 1/4; all 64 inverse columns pass.")
    print("tag     U-dagger on trusted six    erased-tag control")
    for mode, copy in TAGS.items():
        cut, q = evolve(state, power, copy)
        values = []
        for erased in (False, True):
            control = tuple(reversed(copy)) if erased else ()
            out, p = evolve(cut, q, control + REVERSE)
            require(probability(out, p, lambda _: True) == 1, "normalization")
            values.append(probability(out, p, lambda i: i & 63 == 0))
        require(values == [partition_probability(mode), 1], f"{mode} revival")
        print(f"{mode:7} {str(values[0]):26} {values[1]}")


def instruction(gate):
    wires = ", ".join(f"q[{i}]" for i in (*gate.controls, gate.target))
    n = len(gate.controls)
    modifier = "" if not n else "ctrl @ " if n == 1 else f"ctrl({n}) @ "
    return f"{modifier}{gate.name} {wires};"


def export(mode, erase):
    copy = TAGS[mode]
    size = max((gate.target + 1 for gate in copy), default=6)
    lines = ["OPENQASM 3.0;", 'include "stdgates.inc";', f"qubit[{size}] q;",
             "bit[6] trusted;"]
    for tick, gates in enumerate(TICKS, 1):
        lines.append(f"// source tick {tick}")
        lines.extend(map(instruction, gates))
    lines += ["barrier q;", "// release cut"]
    lines.extend(map(instruction, copy))
    lines.append("barrier q;")
    if erase:
        lines.append("// Deliberate control: give the tester access to the tag.")
        lines.extend(map(instruction, reversed(copy)))
    lines.append("// Invert the source on q[0] through q[5] only.")
    lines.extend(map(instruction, REVERSE))
    lines.extend(f"trusted[{i}] = measure q[{i}];" for i in range(6))
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--qasm", type=Path, help="export circuit to a fresh path")
    parser.add_argument("--tag", choices=TAGS, default="none")
    parser.add_argument("--erase-tag", action="store_true", help="reverse the release copy")
    args = parser.parse_args()
    check_all()
    if args.qasm:
        with args.qasm.open("x", encoding="ascii", newline="\n") as out:
            out.write(export(args.tag, args.erase_tag))
