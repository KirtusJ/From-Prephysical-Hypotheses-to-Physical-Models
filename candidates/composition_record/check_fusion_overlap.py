"""Check the Hai et al. Pauli circuit and the proposed six-overlap product."""

from cmath import exp
from fractions import Fraction
from itertools import product
from math import atan2, hypot, pi, prod


def arm(bits, route):
    # Written products act rightmost first. Tuple order is physical qubits 1, 2, 3.
    first, second, third = bits
    if route == 1:  # X3 Z3
        phase = (-1) ** third
    else:  # Z2 X3 Z1
        phase = (-1) ** (first + second)
    return (first, second, 1 - third), phase


def check_echo():
    # Read left to right as circuit time, appending one gate at a time.
    detailed = ("Z3", "X3", "Z1", "X3", "Z2")
    schematic = ("X3", "Z3", "Z1", "X3", "Z2")  # A1 dagger followed by A2.
    def propagate(bits, word):
        state = list(bits)
        sign = 1
        for gate in word:
            qubit = int(gate[1]) - 1
            if gate[0] == "X":
                state[qubit] ^= 1
            else:
                sign *= (-1) ** state[qubit]
        return tuple(state), sign

    states = list(product(range(2), repeat=3))
    for basis in states:
        parity = (-1) ** sum(basis)
        assert propagate(basis, detailed) == (basis, parity)
        assert propagate(basis, schematic) == (basis, -parity)
    for a, b in product(states, repeat=2):
        out_a, sign_a = arm(a, 1)
        out_b, sign_b = arm(b, 2)
        overlap = int(out_a == out_b) * sign_a * sign_b
        assert overlap == int(a == b) * (-1) ** sum(a)


def add(a, b):
    return tuple((x + y) % 5 for x, y in zip(a, b))


def coboundary(pair, a, b, c):
    return (pair(b, c) - pair(add(a, b), c) + pair(a, add(b, c)) - pair(a, b)) % 5


def check_six_orders():
    e1, e2, e3 = (1, 0, 0), (0, 1, 0), (0, 0, 1)
    even = ((e1, e2, e3), (e2, e3, e1), (e3, e1, e2))
    odd = ((e1, e3, e2), (e3, e2, e1), (e2, e1, e3))
    orders = even + odd

    # Check each independent pair-table entry occurring in the six coboundaries.
    entries = set()
    for a, b, c in orders:
        entries.update(((b, c), (add(a, b), c), (a, add(b, c)), (a, b)))
    for entry in entries:
        def pair(a, b):
            return int((a, b) == entry)

        deltas = [coboundary(pair, *order) for order in orders]
        assert (sum(deltas[:3]) - sum(deltas[3:])) % 5 == 0
        if entry == (e2, e3):
            assert deltas[0] == 1

        gain = complex(0.712, 0.177)  # Example only, common to all six readers.
        for seed in range(5):
            signs = [1, 1, 1, -1, -1, -1]
            readings = [
                gain * exp(2j * pi * (sign * seed + delta) / 5)
                for sign, delta in zip(signs, deltas)
            ]
            oriented = prod(readings[:3]) * prod(z.conjugate() for z in readings[3:])
            assert abs(oriented - abs(gain) ** 6 * exp(2j * pi * seed / 5)) < 1e-14
    return len(entries)


if __name__ == "__main__":
    check_echo()
    entry_count = check_six_orders()
    z, y = Fraction(712, 1000), Fraction(177, 1000)
    print(f"Quadrature radius {hypot(z, y):.8f}, polar angle {atan2(y, z)/pi:.8f} pi")
    print(f"Distance from ideal even-parity signal {hypot(1 - z, y):.8f}")
    print(f"Distance from opposite schematic sign {hypot(-1 - z, y):.8f}")
    print(f"Minimum distance to any real parity expectation {float(abs(y)):.3f}")
    print(f"Verified 64 matrix entries, {entry_count} pair controls, and five determinant seeds.")
