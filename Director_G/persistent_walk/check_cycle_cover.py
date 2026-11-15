"""Compare ideal sharp launches on a five-cycle and its ten-cycle parity lift."""
from fractions import Fraction
from itertools import product
import json


def require(condition, check):
    if not condition:
        raise ArithmeticError(check)


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def rotate_minus_i(a):
    return (a[1], -a[0])


def step(state, coin):
    # Integer real and imaginary numerators share the denominator sqrt(2)^t.
    zero = (0, 0)
    out = [[zero, zero] for _ in state]
    for x, (right, left) in enumerate(state):
        if coin == "H":
            r = add(right, left)
            l = add(right, (-left[0], -left[1]))
        else:
            r = add(right, rotate_minus_i(left))
            l = add(rotate_minus_i(right), left)
        out[(x + 1) % len(state)][0] = r
        out[(x - 1) % len(state)][1] = l
    return out


def launch(sites, rail):
    state = [[(0, 0), (0, 0)] for _ in range(sites)]
    state[0][rail] = (1, 0)
    return state


def probability(a, t):
    return Fraction(a[0]**2 + a[1]**2, 2**t)


def check():
    rows = {}
    for coin, rail in product(("H", "Hprime"), (0, 1)):
        five, ten = launch(5, rail), launch(10, rail)
        for t in range(65):
            for x in range(5):
                lift = x if (x - t) % 2 == 0 else x + 5
                require(five[x] == ten[lift], "amplitude at lifted position")
                require(ten[(lift + 5) % 10] == [(0, 0), (0, 0)], "amplitude on the opposite sheet")
            if t == 7:
                p = [probability(a, t) for a in five[0]]
                rows[(coin, rail)] = (p[rail], sum(p))
            five = step(five, coin)
            ten = step(ten, coin)
    require(rows[("H", 0)] == (Fraction(25, 128), Fraction(25, 64)), "Hadamard return at tick seven")
    require(rows[("Hprime", 0)] == (Fraction(49, 128), Fraction(29, 64)), "balanced complex-coin return at tick seven")
    for coin in ("H", "Hprime"):
        require(rows[(coin, 0)] == rows[(coin, 1)], "initial rail reflection")
    print(json.dumps({"last_tick_checked": 64, "amplitudes_compared": 65 * 5 * 2 * 2 * 2,
                      "opposite_sheet": "exactly zero",
                      "tick_7_for_either_sharp_launch_rail": {
                          coin: {"same_rail_return": str(rows[(coin, 0)][0]),
                                 "summed_site_return": str(rows[(coin, 0)][1])}
                          for coin in ("H", "Hprime")}}, indent=2))


if __name__ == "__main__":
    check()
