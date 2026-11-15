"""Exact checks for balanced pair tests on the two-launch sheet comparator."""
from fractions import Fraction as F
from itertools import combinations, product


def multiply(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def check_pass_effects():
    identity = [[int(i == j) for j in range(3)] for i in range(3)]
    passes = []
    for a, b in combinations(range(3), 2):
        v = [int(i == a) - int(i == b) for i in range(3)]
        passes.append([[identity[i][j] - F(v[i]*v[j], 2) for j in range(3)] for i in range(3)])
    effect = identity
    for n in range(9):
        assert all(effect[i][j] == F(1, 3) + (identity[i][j]-F(1, 3))/2**n
                   for i, j in product(range(3), repeat=2))
        terms = [multiply(multiply(p, effect), p) for p in passes]
        effect = [[sum(t[i][j] for t in terms)/3 for j in range(3)] for i in range(3)]


def check_sheet_relabel():
    def skew(i, j):
        return int((j-i)%3 == 1) - int((i-j)%3 == 1)

    for a, b, c, d in product(range(3), repeat=4):
        # A flat projection on v leaves u unchanged and conversely.
        diff = int((a+b-c-d)%3 == 0) - int((a-b-c+d)%3 == 0)
        assert diff == -skew(a,c)*skew(b,d)


def check_miss_calibration():
    # Input outer products avoid square roots in this real three-mode basis.
    for sign in (1, -1):
        launch = [1, 0, sign]
        rho = [[F(x*y, 2) for y in launch] for x in launch]
        miss = [[F(1,2), F(1,2), 0], [F(1,2), F(1,2), 0], [0, 0, 1]]
        state = multiply(multiply(miss, rho), miss)
        for visibility in (-1, 0, F(1,3), 1):
            def entry(i, j):
                crosses = (i == 2) != (j == 2)
                return state[i][j] * (visibility if crosses else 1)

            ports = [(entry(0,0) + entry(2,2) + d*(entry(0,2)+entry(2,0)))/2
                     for d in (-1, 1)]
            assert ports[0] == (5 - 4*sign*visibility) / F(16)
            assert entry(1,1) == F(1,8)
            assert sum(ports) + entry(1,1) + F(1,4) == 1


if __name__ == "__main__":
    check_sheet_relabel()
    check_pass_effects()
    check_miss_calibration()
    print("All 81 sheet entries and pass effects through eight rounds agree; signed miss probes pass.")
