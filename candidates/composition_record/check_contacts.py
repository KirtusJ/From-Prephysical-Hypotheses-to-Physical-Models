"""Check closed words for the F5-valued associator on the additive group F5^3.

The ten class representatives follow C.-N. Beli, Explicit formulas for the
cohomology of the elementary abelian p-groups, https://arxiv.org/pdf/2005.11868.
Run with --output PATH to save the same JSON printed by the default invocation.
"""

import argparse
from functools import partial
from itertools import product
import json
from pathlib import Path


P = 5
ZERO = (0, 0, 0)
E1, E2, E3 = BASIS = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
VECTORS = tuple(product(range(P), repeat=3))


def add(a, b):
    return ((a[0] + b[0]) % P, (a[1] + b[1]) % P, (a[2] + b[2]) % P)


def neg(a):
    return (-a[0] % P, -a[1] % P, -a[2] % P)


def determinant(a, b, c):
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        + a[1] * (b[2] * c[0] - b[0] * c[2])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    ) % P


def carry_class(i, j, a, b, c):
    return a[i] * ((b[j] + c[j]) // P) % P


COORDINATES = tuple(product(range(3), repeat=2))
SEEDS = (determinant,) + tuple(partial(carry_class, i, j) for i, j in COORDINATES)
NAMES = ["det"] + [f"a{i+1} C{j+1}" for i, j in COORDINATES]


def contact(seed, h, x, y):
    return (seed(h, x, y) + seed(x, y, h) - seed(x, h, y)) % P


def multiply(seed, h, left, right):
    x, a = left
    y, b = right
    return add(x, y), (a + b + contact(seed, h, x, y)) % P


def inverse(seed, h, lifted):
    x, a = lifted
    minus_x = neg(x)
    return minus_x, (-a - contact(seed, h, x, minus_x)) % P


def central_part(state):
    if state[0] != ZERO:
        raise ValueError(f"Word failed to close: {state}")
    return state[1]


def fifth_power(seed, h, x):
    state = (ZERO, 0)
    for _ in range(P):
        state = multiply(seed, h, state, (x, 0))
    return central_part(state)


def commutator(seed, h, x, y):
    g, k = (x, 0), (y, 0)
    state = (ZERO, 0)
    for factor in (g, k, inverse(seed, h, g), inverse(seed, h, k)):
        state = multiply(seed, h, state, factor)
    return central_part(state)


def check(actual, expected, where):
    if actual != expected:
        raise ValueError(f"{where}: expected {expected}, observed {actual}")


def rank(rows):
    pivots = {}
    for row in rows:
        row = list(row)
        for column in range(len(row)):
            entry = row[column]
            if entry == 0:
                continue
            if column in pivots:
                row = [(a - entry * b) % P for a, b in zip(row, pivots[column])]
            else:
                inverse_entry = pow(entry, -1, P)
                pivots[column] = [(a * inverse_entry) % P for a in row]
                break
    return len(pivots)


def tomography():
    comm_rows = {}
    for h, x, y in product(VECTORS, BASIS, BASIS):
        row = [commutator(seed, h, x, y) for seed in SEEDS]
        check(row, [determinant(h, x, y)] + [0] * 9, ("commutator", h, x, y))
        comm_rows[h, x, y] = row

    power_rows = {}
    for h, x in product(VECTORS, repeat=2):
        row = [fifth_power(seed, h, x) for seed in SEEDS]
        expected = [0] + [h[i] * x[j] % P for i, j in COORDINATES]
        check(row, expected, ("fifth power", h, x))
        power_rows[h, x] = row

    menus = [
        ("commutators_only", [], 1),
        ("h_and_x_equal_e1", [power_rows[E1, E1]], 2),
        ("x_equal_e1_all_h", [power_rows[h, E1] for h in VECTORS], 4),
        ("h_equal_x_all_vectors", [power_rows[h, h] for h in VECTORS], 7),
        ("independent_h_and_x", list(power_rows.values()), 10),
    ]
    table = {}
    for name, readouts, expected_rank in menus:
        measured_rank = rank([*comm_rows.values(), *readouts])
        check(measured_rank, expected_rank, ("rank", name))
        table[name] = {
            "power_rows": len(readouts),
            "combined_rank": measured_rank,
            "kernel_dimension": len(SEEDS) - measured_rank,
        }

    minimal = [comm_rows[E1, E2, E3]]
    minimal.extend(power_rows[BASIS[i], BASIS[j]] for i, j in COORDINATES)
    identity = [[int(i == j) for j in range(10)] for i in range(10)]
    check(minimal, identity, "calibrated ten scalar readings")
    return {
        "class_columns": NAMES,
        "commutator_menu": "all 125 h, both x and y in the three standard basis labels",
        "commutator_words_per_class": len(comm_rows),
        "fifth_power_words_per_class": len(power_rows),
        "power_menus_with_common_commutator_rows": table,
        "minimal_panel_rows": ["K(e1,e2,e3)"] + [
            f"L(e{i+1},e{j+1})" for i, j in COORDINATES
        ],
        "minimal_panel_matrix": minimal,
    }


def skew_rival(a, b, c):
    return (determinant(a, b, c) + carry_class(0, 1, a, b, c)
            - carry_class(1, 0, a, b, c)) % P


def gauge(a, b):
    return a[0] ** 2 * b[1] ** 2 % P


def recalibrated(a, b, c):
    boundary = gauge(b, c) - gauge(add(a, b), c) + gauge(a, add(b, c)) - gauge(a, b)
    return (determinant(a, b, c) + boundary) % P


def rival_checks():
    seeds = (skew_rival, recalibrated)
    for h, x, y in product(VECTORS, BASIS, BASIS):
        for seed in seeds:
            observed = commutator(seed, h, x, y)
            check(observed, determinant(h, x, y), (seed.__name__, "commutator", h, x, y))
    for h, x in product(VECTORS, repeat=2):
        observed = fifth_power(skew_rival, h, x)
        check(observed, (h[0] * x[1] - h[1] * x[0]) % P, ("skew lift", h, x))
        check(fifth_power(recalibrated, h, x), 0, ("gauge lift", h, x))

    raw = [contact(recalibrated, h, E1, E1) for h in VECTORS]
    check(raw, [-2 * h[1] ** 2 % P for h in VECTORS], "raw gauge contact")
    doubled = add(E2, E2)
    value = contact(recalibrated, E2, E1, E1)
    doubled_value = contact(recalibrated, doubled, E1, E1)
    check((value, doubled_value, 2 * value % P), (3, 2, 1), "failure of additivity in h")
    return {
        "skew_rival": {
            "seed": "det + a1 C2 - a2 C1",
            "diagonal_zero_fifth_powers": sum(fifth_power(skew_rival, h, h) == 0 for h in VECTORS),
            "L(e1,e2)": fifth_power(skew_rival, E1, E2),
            "L(e2,e1)": fifth_power(skew_rival, E2, E1),
            "commutators_agreeing_with_det": len(VECTORS) * len(BASIS) ** 2,
        },
        "gauge": {
            "seed": "det + delta f, f(a,b) = a1^2 b2^2",
            "raw_word": "beta_h(e1,e1)",
            "raw_at_e2": value,
            "raw_at_2e2": doubled_value,
            "twice_raw_at_e2": 2 * value % P,
            "closed_commutators_agreeing_with_det": len(VECTORS) * len(BASIS) ** 2,
            "closed_fifth_powers_agreeing_with_det": len(VECTORS) ** 2,
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    output = parser.parse_args().output
    result = {"field": P, "tomography": tomography(), **rival_checks()}
    report = json.dumps(result, indent=2) + "\n"
    if output:
        output.write_text(report, encoding="utf-8", newline="\n")
    else:
        print(report, end="")


if __name__ == "__main__":
    main()
