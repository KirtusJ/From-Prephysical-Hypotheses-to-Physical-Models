"""Enumerate all joint port and slot outputs of the finite CHSH settings."""
from itertools import product
from math import isclose, sqrt


def correlation(h, port_x, minus):
    # Bell preparation has the same probabilities under a global sign.
    state = [[h, 0, 0], [0, -h if minus else h, 0]]
    if port_x:
        top, bottom = state
        state = [[h*(a+s*b) for a, b in zip(top, bottom)] for s in (1, -1)]
    for row in state:
        row[1], row[2] = row[2], row[1]
        for i, j in [(0, 1), (1, 2), (0, 1)]:
            a, b = row[i], row[j]
            row[i], row[j] = h*(a+b), h*(a-b)
    assert isclose(sum(v*v for row in state for v in row), 1)
    return sum((1 if (i == 0) == (j == 0) else -1)*state[i][j]**2
               for i, j in product(range(2), range(3)))


if __name__ == "__main__":
    for sign in (1, -1):
        h = sign/sqrt(2)
        zz, zm, xz, xm = [correlation(h, x, m) for x, m in product((False, True), repeat=2)]
        score = zz + zm + xz - xm
        assert isclose(score, 1.25 + sign*sqrt(2))
        print(sign, (zz, zm, xz, xm), score)
