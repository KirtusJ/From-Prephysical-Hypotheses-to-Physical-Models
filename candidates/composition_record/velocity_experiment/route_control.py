"""Export one deterministic nine-tick address-read control matching a science arm.

Each three-tick segment goes right first, then left. Its displacement specifies
how many moves of each kind are needed. Rail 0 denotes R and rail 1 denotes L.
The control checks basis-state address writes. Transfer to a coherent science
shot requires matched routing, timing, readout and bookkeeping on hardware.
"""
import argparse
from itertools import product
from pathlib import Path
import re
import sys

# Import the sibling generator even when invoked as "python -I route_control.py".
sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    import generate
finally:
    sys.path.pop(0)


MOVES = (-3, -1, 1, 3)
BIT_READ = re.compile(r"record\[(\d+)\] = measure q\[(\d+)\];")


def export(source, signs, displacements):
    if len(displacements) != 3 or any(d not in MOVES for d in displacements):
        raise ValueError("expected three displacements from {-3,-1,1,3}")
    if source not in (0, 1) or signs not in generate.PATTERNS:
        raise ValueError("invalid source or pulse pair")
    targets = []
    for d in displacements:
        left = (3-d)//2
        targets.extend([0]*(3-left) + [1]*left)
    current = source
    coin_gates = []
    for target in targets:
        # In OpenQASM 3 stdgates.inc, id is the single-qubit identity.
        coin_gates.append("id q[0];" if current == target else "x q[0];")
        current = target
    lines = generate.circuit(source, signs).splitlines()
    if lines.count(generate.H) != len(coin_gates):
        raise ValueError("science circuit does not contain nine opening coins")
    replacements = iter(coin_gates)
    return "\n".join(next(replacements) if line == generate.H else line for line in lines) + "\n"


def read_control(text):
    """Execute the emitted basis gates; return bit word, final rail and phase i**k."""
    lines = text.splitlines()
    if tuple(lines[:4]) != generate.PROLOGUE:
        raise ValueError("unexpected OpenQASM declarations")
    bits = [0, 0, 0]
    record = [None]*6
    phase = 0
    for line in lines[4:]:
        if line in ("id q[0];", "barrier q;"):
            continue
        if line == "x q[0];":
            bits[0] ^= 1
        elif line == generate.CCX:
            bits[2] ^= bits[0] & bits[1]
        elif line == generate.CX:
            bits[1] ^= bits[0]
        elif line in ("s q[0];", "sdg q[0];"):
            phase += bits[0] if line == "s q[0];" else -bits[0]
        else:
            match = BIT_READ.fullmatch(line)
            if match is None:
                raise ValueError(f"unknown control statement {line}")
            dest, qubit = map(int, match.groups())
            if dest not in range(6) or qubit not in (1, 2) or record[dest] is not None:
                raise ValueError("invalid address-bit measurement")
            record[dest] = bits[qubit]
    if None in record:
        raise ValueError("incomplete address word")
    return "".join(map(str, reversed(record))), bits[0], phase % 4


def verify():
    for source, signs in product((0, 1), generate.PATTERNS):
        words = set()
        for ds in product(MOVES, repeat=3):
            text = export(source, signs, ds)
            word, last_rail, phase = read_control(text)
            # Independent oracle: recover the left-step address from cumulative
            # signed displacement and elapsed ticks, without applying circuit gates.
            positions = tuple(((3*i-sum(ds[:i]))//2) % 4 for i in (1, 2, 3))
            expected = "".join(f"{n:02b}" for n in reversed(positions))
            last = tuple(int(d < 3) for d in ds)
            if (word, last_rail, phase) != (expected, last[2],
                                            (signs[0]*last[0]+signs[1]*last[1]) % 4):
                raise ValueError(f"wrong quantum route or read for {source}, {signs}, {ds}")
            if generate.displacement(positions) != ds:
                raise ValueError("science displacement convention differs")
            words.add(word)
        if len(words) != 64:
            raise ValueError("incomplete deterministic control coverage")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", choices=("R", "L"), help="science arm's initial rail")
    parser.add_argument("--phases", choices=("S", "Sdg"), nargs=2, help="first and second boundary pulses")
    parser.add_argument("--displacements", type=int, choices=MOVES, nargs=3,
                        help="three signed lengths, in chronological order")
    parser.add_argument("--output", type=Path, help="create one new .qasm file; default is stdout")
    parser.add_argument("--check", action="store_true", help="verify all 512 controls, then exit")
    args = parser.parse_args()
    if args.check:
        if any(v is not None for v in (args.source, args.phases, args.displacements, args.output)):
            parser.error("--check runs alone")
    elif any(v is None for v in (args.source, args.phases, args.displacements)):
        parser.error("specify --source, --phases and --displacements for the control")
    verify()
    if args.check:
        print("Verified 512 deterministic circuits, covering all 64 joint words in each arm.")
        return
    signs = tuple(1 if name == "S" else -1 for name in args.phases)
    text = export(int(args.source == "L"), signs, tuple(args.displacements))
    if args.output is None:
        sys.stdout.write(text)
    else:
        with args.output.open("xb") as out:
            out.write(text.encode("ascii"))


if __name__ == "__main__":
    main()
