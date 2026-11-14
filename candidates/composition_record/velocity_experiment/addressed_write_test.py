"""Three observed sites after real, parity-addressed three-tick flights.

ordinary_word_weights()[y3,y6,y9] == (a,b) means (a+b*sqrt(2))/512.
The address counts left moves modulo four. A signed displacement in each
three-tick flight is recovered from successive addresses as in generate.py.
Run with no arguments for all prefix types and all zero words. --qasm PATH
also exports the single sharp-R circuit to a fresh file. No T gate is specified
in the walk. Controlled-H on a backend may need non-Clifford synthesis.
"""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction as F
from functools import cmp_to_key
from itertools import product
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    import generate
finally:
    sys.path.pop(0)


ZERO, ONE = (0, 0), (1, 0)
WORDS = tuple(product(range(4), repeat=3))


def add(x, y):
    return x[0]+y[0], x[1]+y[1]


def sub(x, y):
    return x[0]-y[0], x[1]-y[1]


def mul(x, y):
    a, b = x
    c, d = y
    return a*c+2*b*d, a*d+b*c


def divide(x, y):
    c, d = y
    n, m = mul(x, (c, -d))
    return F(n, c*c-2*d*d), F(m, c*c-2*d*d)


def sign(x):
    a, b = x
    if a*b >= 0:
        z = a+b
        return (z > 0) - (z < 0)
    z = a*a-2*b*b
    return ((z > 0) - (z < 0)) * (1 if a > 0 else -1)


def circuit():
    lines = []
    tick = 0
    for line in generate.circuit(0, (1, 1)).splitlines():
        if line == generate.H:
            tick += 1
            if tick % 3 == 2:
                lines.extend(("negctrl @ x q[1], q[0];", "ctrl @ h q[1], q[0];"))
                continue
        if line == "s q[0];":
            line = "id q[0];"
        lines.append(line)
    if tick != 9:
        raise ValueError("unexpected source clock")
    return "\n".join(lines) + "\n"


def ordinary_word_weights():
    # Every tick uses the common omitted factor 1/sqrt(2). Thus physical
    # X at an even address contributes sqrt(2) times the permutation.
    states = {((), 0): (ONE, ZERO)}
    for tick in range(1, 10):
        nxt = {}
        for (prefix, site), (r, l) in states.items():
            if tick % 3 == 2 and site % 2 == 0:
                daughters = mul((0, 1), l), mul((0, 1), r)
            else:
                daughters = add(r, l), sub(r, l)
            for rail, amp in enumerate(daughters):
                new_site = (site+rail) % 4
                history = prefix + (new_site,) if tick % 3 == 0 else prefix
                pair = nxt.setdefault((history, new_site), [ZERO, ZERO])
                pair[rail] = add(pair[rail], amp)
        states = nxt
    weights = {w: ZERO for w in WORDS}
    for (prefix, _), (r, l) in states.items():
        weights[prefix] = add(mul(r, r), mul(l, l))
    return weights


def enumerate_paths(text):
    """Independently traverse the 512 coin words and execute parsed address gates."""
    if tuple(text.splitlines()[:4]) != generate.PROLOGUE:
        raise ValueError("QASM prologue")
    amps = defaultdict(lambda: ZERO)
    for moves in product((0, 1), repeat=9):
        bits = [0, 0, 0]
        record = [None]*6
        previous = tick = exchanges = 0
        amplitude_sign = 1
        for line in text.splitlines()[4:]:
            if line == "negctrl @ x q[1], q[0];":
                if bits[1] == 0:
                    bits[0] ^= 1
                continue
            if line in (generate.H, "ctrl @ h q[1], q[0];"):
                rail = moves[tick]
                tick += 1
                if line == generate.H or bits[1]:
                    if bits[0] == rail == 1:
                        amplitude_sign = -amplitude_sign
                    bits[0] = rail
                else:
                    if bits[0] != rail:
                        break
                    exchanges += 1
                previous = rail
            elif line == generate.CCX:
                bits[2] ^= bits[0] & bits[1]
            elif line == generate.CX:
                bits[1] ^= bits[0]
            elif line.startswith("record["):
                dest, qubit = line.removesuffix("];").split("] = measure q[")
                i, j = int(dest[7:]), int(qubit)
                if j not in (1, 2) or record[i] is not None:
                    raise ValueError("invalid coordinate write")
                record[i] = bits[j]
            elif line not in ("barrier q;", "id q[0];"):
                raise ValueError(f"unexpected instruction {line}")
        else:
            if tick != 9 or None in record:
                raise ValueError("incomplete word")
            w = tuple(record[i]+2*record[i+1] for i in (0, 2, 4))
            if generate.displacement(w) != tuple(3-2*sum(moves[i:i+3]) for i in (0, 3, 6)):
                raise ArithmeticError("address/displacement mismatch")
            unit = amplitude_sign * 2**(exchanges//2)
            amp = (0, unit) if exchanges%2 else (unit, 0)
            amps[w, previous] = add(amps[w, previous], amp)
    return {w: add(mul(amps[w, 0], amps[w, 0]), mul(amps[w, 1], amps[w, 1])) for w in WORDS}


def verify(weights):
    if weights != enumerate_paths(circuit()) or sum_weights(weights.values()) != (512, 0):
        raise ArithmeticError("path and port calculations differ or mass is not one")
    layers = []
    for depth in range(3):
        types = Counter()
        for prefix in product(range(4), repeat=depth):
            children = [sum_weights(v for w, v in weights.items()
                                      if w[:depth+1] == prefix+(j,)) for j in range(4)]
            parent = sum_weights(children)
            if parent == ZERO:
                continue
            row = [divide(v, parent) for v in children]
            if len({p for p in row if sign(p)>0})!=3 or row.count(ZERO)!=1:
                raise ArithmeticError(f"insufficient distinct positive weights at {prefix}: {row}")
            ordered = tuple(sorted(row, key=cmp_to_key(lambda a, b: sign(sub(a, b)))))
            types[ordered] += 1
        if sum(types.values()) != 3**depth:
            raise ArithmeticError("unexpected live-prefix count")
        layers.append(types)
    return layers


def sum_weights(values):
    total = ZERO
    for v in values:
        total = add(total, v)
    return total


def pretty(x):
    a, b = x
    if b == 0:
        return str(a)
    return f"{a}{'+' if b>0 else '-'}{abs(b)}*sqrt(2)"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--qasm", type=Path, help="also export one new OpenQASM 3 file")
    args = parser.parse_args()
    weights = ordinary_word_weights()
    for depth, types in enumerate(verify(weights)):
        for row, n in types.items():
            print(f"depth {depth}: {n} x ({', '.join(pretty(x) for x in row)})")
    dark = [w for w in WORDS if weights[w] == ZERO]
    print(f"{len(dark)} dark words: " + ", ".join("".join(map(str, w)) for w in dark))
    if args.qasm:
        with args.qasm.open("xb") as out:
            out.write(circuit().encode("ascii"))


if __name__ == "__main__":
    main()
