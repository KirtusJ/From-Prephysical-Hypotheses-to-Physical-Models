"""Recompute the Hadamard half-line effect and signed release from integer paths."""

from fractions import Fraction
from math import atan, comb, pi, sqrt


IDENTITY = (1, 0, 0, 1)
ZERO = (0, 0, 0, 0)


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def advance(cells):
    """Apply the unnormalized H, then stream R to x+1 and L to x-1."""
    output = {}
    for x, (a, b, c, d) in cells.items():
        output.setdefault(x + 1, [0] * 4)[:2] = (a + c, b + d)
        output.setdefault(x - 1, [0] * 4)[2:] = (a - c, b - d)
    return output


def gram(matrix):
    a, b, c, d = matrix
    return a*a + c*c, a*b + c*d, b*b + d*d


def tagged_mass(matrix, denominator, rail_component):
    a, b, c = gram(matrix)
    return (a + c + rail_component * (a - c + 2*b)) / (2*denominator)


def moments(law, tick):
    require(sum(law.values()) == 1 and min(law.values()) >= 0, "Invalid law")
    mean = sum(x*p for x, p in law.items()) / tick
    second = sum(x*x*p for x, p in law.items()) / tick**2
    cdf = sum(p for x, p in law.items() if 2*x <= tick)
    return mean, second, cdf


def release_panel(cells, tick, g):
    denominator = 2**tick
    point = {x: tagged_mass(m, denominator, g) for x, m in cells.items()}
    mean, second, cdf = moments(point, tick)
    coherent_means = []
    for relative_sign in (1, -1):
        law = {}
        for x in range(-tick - 1, tick + 2, 2):
            left = cells.get(x + 1, ZERO)
            right = cells.get(x - 1, ZERO)
            matrix = [a + relative_sign*b for a, b in zip(left, right)]
            law[x] = tagged_mass(matrix, 2*denominator, g)
        coherent_means.append(moments(law, tick)[0])
    require(sum(coherent_means) == 2*mean, "Coherence did not cancel in the mixture")
    return mean, second, cdf, *coherent_means


def main():
    cells = {0: IDENTITY}
    g = Fraction(2, 3)  # positive m=1 tag; s_X=s_Z=g
    print("t  mean/t  second/t^2  Pr(x/t<=1/2)  coherent-plus  coherent-minus")
    for tick in range(1, 513):
        cells = advance(cells)
        denominator = 2**tick
        if tick % 2:
            # Full symmetric 2x2 effect, including its off-diagonal entry.
            entries = [0, 0, 0]
            for x, matrix in cells.items():
                for i, value in enumerate(gram(matrix)):
                    entries[i] += value if x > 0 else -value
            j = tick // 4
            c = Fraction((-1)**j * comb(2*j, j), 2 * 4**j)
            offset = 2*c*c if tick % 4 == 1 else Fraction(0)
            sx = Fraction(1, 2) + offset
            sz = Fraction(1, 2) - offset
            require(tuple(Fraction(x, denominator) for x in entries) == (sz, sx, -sz),
                    f"Half-line effect at t={tick}")
            require(g*(sx + sz) == g, f"Tagged sign at t={tick}")
        else:
            j = tick // 4
            c = Fraction((-1)**j * comb(2*j, j), 2 * 4**j)
            sign = 1 if tick % 4 == 0 else -1
            require(tuple(Fraction(x, 2**(tick//2)) for x in cells[0])
                    == (c, sign*c, -sign*c, c), f"Origin kernel at t={tick}")
        if tick in (16, 64, 256, 512):
            row = release_panel(cells, tick, g)
            print(tick, *(f"{float(x):.8f}" for x in row))
    root = sqrt(2)
    second = 1 - 1/root
    limit_cdf = 0.5 + (1 - 2*float(g))*atan(1/root)/pi
    limit = (2*g*second, second, limit_cdf, 2*g*(root-1), 2*g*(3-2*root))
    print("limit", *(f"{x:.8f}" for x in limit))
    print("Passed 256 odd-time operator and 256 even-time return-matrix checks.")


if __name__ == "__main__":
    main()
