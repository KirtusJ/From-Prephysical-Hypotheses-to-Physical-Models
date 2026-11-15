"""Enumerate all joint port and slot outputs of the finite CHSH settings."""
from itertools import product
from math import isclose, sqrt


def correlation(h, port_x, minus, gates, swap):
    # Bell preparation has the same probabilities under a global sign.
    state = [[h, 0, 0], [0, -h if minus else h, 0]]
    if port_x:
        top, bottom = state
        state = [[h*(a+s*b) for a, b in zip(top, bottom)] for s in (1, -1)]
    for row in state:
        if swap:
            row[1], row[2] = row[2], row[1]
        for i, j in reversed(gates):
            a, b = row[i], row[j]
            row[i], row[j] = h*(a+b), h*(a-b)
    assert isclose(sum(v*v for row in state for v in row), 1)
    return sum((1 if (i == 0) == (j == 0) else -1)*state[i][j]**2
               for i, j in product(range(2), range(3)))


if __name__ == "__main__":
    cases = [
        ([(0,1),(1,2),(0,1)], True, 1.25, 1),
        ([(0,2),(0,1),(1,2),(2,0),(1,2),(1,0),(1,2)], False, 163/64, 1/8),
    ]
    for gates, swap, rational, radical in cases:
        for sign in (1, -1):
            h = sign/sqrt(2)
            correlations = [correlation(h, x, m, gates, swap)
                            for x, m in product((False, True), repeat=2)]
            zz, zm, xz, xm = correlations
            score = zz + zm + xz - xm
            assert isclose(score, rational + sign*radical*sqrt(2))
            print(len(gates), sign, correlations, score)
