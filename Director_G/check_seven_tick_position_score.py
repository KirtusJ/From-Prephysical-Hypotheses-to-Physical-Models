"""Enumerate the passive seven-tick survey and enclose its score coefficients."""
from argparse import ArgumentParser
from collections import Counter
from fractions import Fraction
from itertools import product
import json
from math import ceil, floor
from pathlib import Path

from check_two_column_transport import check, walk


def point(v):
    return Fraction(v), Fraction(v)


def add(x, y):
    return x[0] + y[0], x[1] + y[1]


def subtract(x, y):
    return x[0] - y[1], x[1] - y[0]


def mul(x, y):
    corners = [a * b for a in x for b in y]
    return min(corners), max(corners)


def ratio(x, y):
    check(y[0] > 0, "positive denominator interval")
    return mul(x, (1 / y[1], 1 / y[0]))


def enclose(x, digits=12):
    scale = 10**digits
    return Fraction(floor(x[0]*scale), scale), Fraction(ceil(x[1]*scale), scale)


def k_interval(m):
    z = Fraction(m-1, m+1)
    lower = 2*m*sum(z**(2*j+1)/(2*j+1) for j in range(100))
    upper = lower + 2*m*z**201/(201*(1-z*z))
    return enclose((lower, upper), 10)


def coefficient_boxes():
    lo_millis = {4: 5545, 5: 8047, 9: 19775, 16: 44361, 17: 48164}
    k = {m: k_interval(m) for m in lo_millis}
    for m, lower in lo_millis.items():
        check(Fraction(lower, 1000) < k[m][0] <= k[m][1] < Fraction(lower+1, 1000),
              "printed rational logarithm bracket")
    delta = subtract(mul(k[5], k[16]), mul(k[17], k[4]))
    b = enclose(ratio(mul(k[9], subtract(k[16], k[17])), delta))
    c = enclose(ratio(mul(k[9], subtract(k[5], k[4])), delta))
    a = subtract(subtract(point(9), mul(point(5), b)), mul(point(17), c))
    check(-1 < b[0] <= b[1] < 0 < c[0] <= c[1] < 1, "signs for both strict minima and count")
    return k, delta, a, b, c


def path_tables():
    signed, unsigned = Counter(), Counter()
    for word in product((0, 1), repeat=7):
        x, previous, amplitude = 0, 0, 1
        for rail in word:
            x += 1-2*rail
            amplitude *= (-1)**(previous*rail)
            previous = rail
        signed[x, previous] += amplitude
        unsigned[x] += 1
    rows = {x: [r[0] for r in rails] for x, rails in sorted(walk(7).items())}
    check(all(pair == [signed[x,0], signed[x,1]] for x, pair in rows.items()), "signed histories")
    check(sum(unsigned.values()) == sum(a*a+b*b for a,b in rows.values()) == 128, "complete records")
    return rows, unsigned


def positive_power(v, q):
    return v**q if v else 0


def masses(rows, q, rail_sites):
    weights = {}
    for x, (a,b) in rows.items():
        cells = (a*a, b*b) if x in rail_sites else (a*a+b*b,)
        weights[x] = sum(positive_power(v, q) for v in cells)
    return weights


def score(weights, a, b, c):
    linear = add(mul(a, point(weights[-7])), mul(b, point(weights[-3])))
    linear = add(linear, mul(c, point(weights[-5])))
    numerator = add(linear, point(-weights[-1]+2*(weights[1]-weights[-5])))
    return ratio(numerator, point(sum(weights.values())))


def strings(box):
    return [str(v) for v in box]


def run():
    rows, unsigned = path_tables()
    k, delta, a, b, c = coefficient_boxes()
    panels = {}
    for q in (0, 1, 2, 4, 16, 64):
        panels[str(q)] = {}
        for family, resolved in [("site", set()), ("rail", set(rows))]:
            weights = masses(rows, q, resolved)
            check(weights[1] == weights[-5], "the two site/rail multisets agree")
            box = score(weights, a, b, c)
            if q == 1:
                check(box[0] <= 0 <= box[1], "ordinary value inside coefficient enclosure")
                # Eliminate a using a=9-5b-17c to check exact cancellation.
                check(9*weights[-7] == weights[-1] and 5*weights[-7] == weights[-3]
                      and 17*weights[-7] == weights[-5], "exact ordinary score")
            else:
                check(box[0] > 0, "positive finite-power control")
            panels[str(q)][family] = {"weights": weights, "score_interval": strings(box)}
    count_score = score(unsigned, a, b, c)
    check(count_score[0] > Fraction(4, 128), "counting separated")
    hybrid = masses(rows, 2, {1})
    hybrid_score = score(hybrid, a, b, c)
    check(hybrid_score[1] < 0, "site-dependent rail resolution breaks sign")
    return {
        "signed_r_l_and_unsigned_count": {str(x): [*pair, unsigned[x]] for x, pair in rows.items()},
        "k_intervals": {str(m): strings(box) for m, box in k.items()},
        "coefficient_intervals": {key: strings(val) for key, val in
                                  [("determinant",delta), ("a",a), ("b",b), ("c",c)]},
        "powers": panels,
        "counting_score": strings(count_score),
        "only_plus_one_rail_resolved_q2": {"weights": hybrid, "score_interval": strings(hybrid_score)},
    }


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("output", type=Path)
    args = cli.parse_args()
    panel = run()
    with args.output.open("x", encoding="utf-8", newline="\n") as out:
        json.dump(panel, out, indent=2)
        out.write("\n")
