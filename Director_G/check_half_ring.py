"""Exact checks for terminal displacements and binary half-ring reads."""
from fractions import Fraction
from itertools import combinations

from sympy import Matrix, diag, eye, zeros

from check_cairo_cycle import require, transfer_matrices


def mixed_positions(ticks):
    return [Fraction(sum(v*v for v in block), 2**(ticks + 1))
            for block in transfer_matrices(ticks)]


def displacement(word, ticks):
    section = word[:ticks]
    return (section.count("R") - section.count("L")) % 8


def stationary_positions(templates, ticks):
    row = [Fraction(0)] * 8
    for word, weight in templates:
        period = len(word)
        repeated = word * (2 + ticks // period)
        for start in range(period):
            dx = displacement(repeated[start:], ticks)
            for direction in (-1, 1):
                row[(direction * dx) % 8] += weight / (2 * period)
    return row


def check_displacements():
    exact = [("RLLLL", Fraction(5, 8)), ("RLL", Fraction(3, 8))]
    near = [("LR", Fraction(1, 6)), ("LLLR", Fraction(5, 18)), ("LLLLR", Fraction(5, 9))]
    errors = []
    for t in range(7):
        target = mixed_positions(t)
        if t <= 5:
            require(stationary_positions(exact, t) == target, f"Stationary fit through five, clock {t}")
        fitted = stationary_positions(near, t)
        errors.append(sum(abs(a-b) for a, b in zip(target, fitted)) / 2)
    third = mixed_positions(3)
    gap = mixed_positions(6)[4] - 2 * (third[3] + third[5])
    require(gap == Fraction(1, 8) and max(errors) == gap / 3, "Optimal common tolerance")

    # After each twelve-step word, retrace its moves. Use the same initial
    # phase on each launch, including when translating the prepared site.
    paths = [("LRLLLLLRLLLL", 2), ("RLRRRRRLRRLL", 2), ("LLLLLLLLLRLL", 1),
             ("LLRLLLLLLLLL", 1), ("RRLLLLLLLRLL", 1), ("RRRLLLLLLLLL", 1)]
    for t in range(25):
        row = [0]*8
        for word, weight in paths:
            reverse = word[::-1].translate(str.maketrans("LR", "RL"))
            row[displacement(word + reverse, t)] += weight
        require([Fraction(v, 8) for v in row] == mixed_positions(t), f"Phase-zero fit, clock {t}")


def full_walk(ticks):
    """Translate localized two-rail transfer matrices to all input sites."""
    require(ticks % 2 == 0, "Rational amplitude normalization needs an even clock")
    blocks = [Matrix(2, 2, block) for block in transfer_matrices(ticks)]
    return Matrix(16, 16, lambda row, col: blocks[(row//2 - col//2) % 8][row%2, col%2]
                  / 2**(ticks//2))


def check_half_ring():
    unit = eye(16)
    u, v = full_walk(8), full_walk(16)
    require(v == u*u and v*u == unit, "Eight-step walk and 24-step period")
    q = diag(*([1]*8 + [-1]*8))
    observables = q, u.T*q*u, v.T*q*v
    parity = diag(*[(-1)**(j//2) for j in range(16)])
    for parity_sign in (-1, 1):
        source = (unit + parity_sign*parity)/16
        require(source.trace() == 1 and (source*parity).trace() == parity_sign, "Parity label")
        for observable in observables:
            require(parity*observable == observable*parity, "Block preserves parity")
            require((source*observable).trace() == 0, "Same first-read distribution for both sectors")
            for bit in (-1, 1):
                selected = (unit + bit*observable)/2
                prepared = 2 * selected*source*selected
                require(prepared.trace() == 1 and (prepared*parity).trace() == parity_sign,
                        "Post-read eigenpreparation retains its source-sector label")

    require(sum(observables, zeros(16)) == zeros(16), "Three half-ring observables")
    for earlier, later in combinations(observables, 2):
        require(earlier*later + later*earlier == -unit, "Projective pair anticommutator")
        for sign in (-1, 1):
            selected = (unit + sign*earlier)/2
            require(selected*later*selected == -sign*selected/2, "Conditional next outcome")
    _, midpoint, final = observables
    unread = (final + midpoint*final*midpoint)/2
    require((q*unread + unread*q)/2 == unit/4, "Endpoint correlation with all three reads")


if __name__ == "__main__":
    check_displacements()
    check_half_ring()
    print("Stationary mixed-coin fit is exact through five. Six-step sharp TV tolerance: 1/24.")
    print("Six phase-zero paths match all 24 mixed-coin position distributions.")
    print("Pair-only half-ring disagreement: 3/4. With the intermediate read: 3/8.")
