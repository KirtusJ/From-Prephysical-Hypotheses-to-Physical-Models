"""Export the private four-preparation position-record experiment as OpenQASM 3.

    python -I -B four_state_circuit.py --blocks 2 --qasm new_four_state.qasm
    python -I -B four_state_circuit.py --blocks 0 --qasm new_source_check.qasm

One rail qubit q[0] and counter qubits q[1], q[2], q[3] start in zero. The
counter y counts left steps modulo eight, and x = (tick - 2*y) modulo 16.
At tick 24 all source branches have x=8 and y=0.

The single classical register is named record. Bit 0 is the basis (0=Z,
1=X), bit 1 is the sign (0=R/plus, 1=L/minus). Each intermediate absolute
y uses three fresh bits, low bit first, starting at bit 2. The last three
bits hold the probe's absolute y. Subtract the previous y (zero on the
zero-write preparation bypass) modulo eight
to read the probe rail (0=R/plus, 1=L/minus). Printed Qiskit words put
the highest-numbered bit on the left. The trusted evaluator keeps the
source and probe bits private from the position-stream encoder.

With --copy-at-17, a low address measurement on the first shift of the
third preparation flight copies which rail was taken on every launch.
It temporarily uses the final probe's low bit. The probe overwrites it.
"""

import argparse
from pathlib import Path
from runpy import run_path


walk = run_path(str(Path(__file__).with_name("check_scalar_walk.py")))
qasm_tick = walk["qasm_tick"]
ALL_SCALAR = walk["ALL_SCALAR"]


def measure_address(start):
    return [f"record[{start + bit}] = measure q[{1 + bit}];" for bit in range(3)]


def exported(blocks, copy_at_17=False):
    """Generate a 24 + 12*blocks + 1 tick circuit with its final probe."""
    if not isinstance(blocks, int) or isinstance(blocks, bool) or blocks < 0:
        raise ValueError("blocks must be a nonnegative integer")
    lines = [
        "OPENQASM 3.0;",
        'include "stdgates.inc";',
        "qubit[4] q;",
        f"bit[{5 + 3 * blocks}] record;",
    ]
    for bit in (0, 1):
        # Measuring the low address bit after the first step resolves R/L.
        # Seven more shifts return y to zero, retaining that rail.
        lines.extend(qasm_tick("H"))
        lines.append(f"record[{bit}] = measure q[1];")
        for _ in range(7):
            lines.extend(qasm_tick("I"))

    # R/L becomes +/- on the X branch. Eight shifts bring both coherent
    # components to one physical site and the same counter value.
    controlled_basis = "if (record[0]) { h q[0]; }"
    lines.append(controlled_basis)
    for shift in range(8):
        lines.extend(qasm_tick("I"))
        if copy_at_17 and shift == 0:
            lines.append(f"record[{2 + 3 * blocks}] = measure q[1];")
    lines.append("barrier q;")

    for block in range(blocks):
        for gate in ALL_SCALAR:
            lines.extend(qasm_tick(gate))
        lines.extend(measure_address(2 + 3 * block))
        lines.append("barrier q;")

    lines.append(controlled_basis)
    lines.extend(qasm_tick("I"))
    lines.extend(measure_address(2 + 3 * blocks))
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--blocks", type=int, default=1,
                        help="number of twelve-tick writes; zero probes the source immediately")
    parser.add_argument("--qasm", required=True, type=Path, help="new output path")
    parser.add_argument("--copy-at-17", action="store_true",
                        help="copy the first direction of the third source flight")
    args = parser.parse_args()
    if args.blocks < 0:
        parser.error("--blocks must be nonnegative")
    program = exported(args.blocks, copy_at_17=args.copy_at_17)
    with args.qasm.open("x", encoding="ascii", newline="\n") as output:
        output.write(program)
    print(f"{args.qasm}: 4 qubits, {5 + 3 * args.blocks} classical bits, {25 + 12 * args.blocks} ticks")


if __name__ == "__main__":
    main()
