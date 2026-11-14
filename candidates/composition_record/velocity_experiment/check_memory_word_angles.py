"""Recover the four two-write rotations from the walk and count their directions."""

from itertools import combinations
from math import gcd
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def multiply(z, w):
    a, b = z
    c, d = w
    return a*c-b*d, a*d+b*c


def direction(z):
    a, b = z
    divisor = gcd(a, b)
    if a < 0 or (a == 0 and b < 0):
        divisor = -divisor
    return a//divisor, b//divisor


def letters():
    replay = run_path(str(Path(__file__).with_name("check_position_memory.py")))
    matrices = replay["scalar_kraus"]()
    table = [(0, 2, -8, -9), (2, 0, -8, 9), (8, 10, 8, -1), (10, 8, 8, 1)]
    output = []
    for x, y, a, b in table:
        first, second = matrices[x//2], matrices[y//2]
        matrix = [[sum(second[i][k]*first[k][j] for k in range(2))
                   for j in range(2)] for i in range(2)]
        require((x+y) % 16 == 2 and matrix == [[2*a, -2*b], [2*b, 2*a]],
                "signed product and displacement")
        require(a*a + b*b == (145 if x in (0, 2) else 65), "squared norm")
        output.append((a, b))
    return output


def main():
    rotations = letters()
    require(17**2 % 29 == 28 and (-17+144*17) % 29 == 24, "first residue")
    require(all((63+s*16*17) % 29 for s in (-1, 1)), "second factor is a unit")
    require(3**2 % 5 == 4 and (63+16*3) % 5 == 1, "second residue")
    # All equal-length Gaussian products, deduplicated after each multiplication.
    products = {(1, 0)}
    for k in range(1, 9):
        products = {multiply(z, w) for z in products for w in rotations}
        reps = {direction(z): z for z in products}
        require(len(reps) == (k+1)**2, "distinct projective directions")
        for (a, b), (c, d) in combinations(reps.values(), 2):
            cross = b*c-a*d
            p, q = a*a+b*b, c*c+d*d
            require(cross and cross % 16 == 0, "collision angle determinant")
            # The deficit is at least 4 cross^2 / [2(p+q)4096^k].
            require(4*cross**2 * 145**k >= 256*2*(p+q), "integer loss bound")
        print(f"{2*k:2} writes, {len(reps)} directions, displacement {2*k % 16}")


if __name__ == "__main__":
    main()
