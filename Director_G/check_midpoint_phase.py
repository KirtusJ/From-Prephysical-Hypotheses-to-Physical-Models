"""Exact terminal-rail and adaptive-record checks for a two-mode unitary."""
import argparse
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

from check_unknown_two_mode_coin import add, check, intensity_factor_series, mul, norm, scale, star


HALF = F(1, 2)
ONE = (F(1), F(0))
NEG = (F(-1), F(0))
PHASES = (ONE, NEG, (F(0), F(1)), (F(0), F(-1)), (F(3, 5), F(4, 5)))


def matrix(a, b, scalar=ONE):
    """Both columns of scalar * [[a,b],[-conjugate(b),conjugate(a)]]."""
    return tuple(tuple(mul(scalar, z) for z in row)
                 for row in ((a, b), (scale(-1, star(b)), star(a))))


def apply(matrix_, state):
    return tuple(add(mul(x, state[0]), mul(y, state[1])) for x, y in matrix_)


def midpoint(left, plate, right):
    upper, lower = apply(right, (ONE, (0, 0)))
    return norm(apply(left, (upper, mul(plate, lower)))[1])


def matrix_tests():
    rows = []
    for seed in product((-2, 0, 1), repeat=3):
        length = sum(value**2 for value in seed)
        w, x, y, z = [F(k, 1 + length) for k in (1 - length, *(2 * v for v in seed))]
        coin = matrix((w, x), (y, z), scalar=PHASES[-1])
        upper, lower = coin[0][0], coin[1][1]
        q = norm(coin[1][0])
        check(norm(upper) == norm(lower) == 1 - q, "coin unitarity")
        rates = []
        for phase in PHASES:
            flip = midpoint(coin, phase, coin)
            defect = 4 * (q - HALF)**2 + q * norm(add(upper, scale(-1, mul(phase, lower))))
            check(1 - flip == defect, "midpoint paths and exact defect")
            rates.append(flip)
        imbalance = (1 - rates[0] - rates[1]) / 4
        check(imbalance == (q - HALF)**2, "real-sign test")
        rows.append(dict(stereographic_seed=seed, q=q, plate_rates=rates, balance=imbalance))
    return rows


def port_amplitude(beta, phase):
    # Actual two successive D_beta H operations. The two factors 1/sqrt(2)
    # multiply to 1/2. Multiply the first R-input column (1,beta) by the
    # plate and then the second coin's L-output row (beta, -beta).
    return scale(HALF, mul(beta, add(ONE, scale(-1, mul(phase, beta)))))


def target_tests():
    records = []
    for beta in PHASES:
        plate = scale(-1, star(beta))
        same = norm(port_amplitude(beta, plate))
        conjugate = norm(port_amplitude(star(beta), plate))
        check(same == 1 and conjugate == beta[0]**2, "oriented saturation")
        records.append(dict(beta=beta, plate=plate, target=same, conjugate=conjugate))
    # Rational point q=9/25 with an exact square root in both rails.
    u, v = F(4, 5), F(3, 5)
    def bias_coin(a, b):
        return (((a, 0), (b, 0)), ((b, 0), (-a, 0)))
    first, complement = bias_coin(u, v), bias_coin(v, u)
    retained = midpoint(first, NEG, first)
    changed = midpoint(complement, NEG, first)
    check(changed == 1 and retained == 4 * v**2 * u**2 < 1, "context swap")
    return dict(oriented=records, sign_counterexample=dict(q=v*v, retained=retained, changed=changed))


def history_test(a):
    """An explicit adaptive controller with outcome-dependent gaps and stops."""
    delta = (2 - a) / 8
    coins = (HALF - delta, HALF + delta)
    factors = intensity_factor_series(a, 5)
    leaves = []
    def visit(rail, previous, gaps, target, fresh, retained):
        if len(previous) == 4 or (len(previous) == 2 and previous[-2:] == (1, 1)):
            check(target == fresh, "adaptive transcript mismatch")
            leaves.append(dict(launch_rail=start, outcomes=previous, gaps=gaps,
                               target=target, refreshed=fresh, persistent=sum(retained)))
            return
        gap = 1 + (sum(previous) + rail + len(previous)) % len(factors)
        for outcome in (0, 1):
            flip_factor = factors[gap - 1]
            def probability(q):
                return q * flip_factor if outcome != rail else 1 - q * flip_factor
            conditional = [probability(q) for q in coins]
            check(all(0 <= chance <= 1 for chance in conditional), "nonphysical rate")
            visit(outcome, previous + (outcome,), gaps + (gap,),
                  target * probability(HALF), fresh * sum(conditional) / 2,
                  [mass * chance for mass, chance in zip(retained, conditional)])
    for start in (0, 1):
        visit(start, (), (), F(1), F(1), [HALF, HALF])
        here = [r for r in leaves if r["launch_rail"] == start]
        check(all(sum(r[k] for r in here) == 1 for k in ("target", "refreshed", "persistent")),
              "adaptive normalization")
    persistent_joint = sum(q*q for q in coins) / 2
    check(persistent_joint - HALF**2 == delta**2 > 0, "two consecutive flips")
    return dict(a=a, q=coins, two_flip_persistent=persistent_joint, two_flip_refreshed=HALF**2,
                tree=leaves)


def mixture_test(rows):
    weights = [F(1, 5), F(1, 4), F(1, 6)]
    count = 1 - sum(weights)
    chosen = (rows[0], rows[3], rows[17])
    first, sign = (count / 2 + sum(w * r["plate_rates"][i] for w, r in zip(weights, chosen))
                   for i in (0, 1))
    expected = sum(w * (r["q"] - HALF)**2 for w, r in zip(weights, chosen))
    check((1 - first - sign) / 4 == expected, "mixture and fair count")
    return dict(weights=weights, coherent_seeds=[row["stereographic_seed"] for row in chosen],
                c=count, bare=first, sign=sign, balance=expected)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_directory", type=Path)
    output = parser.parse_args().output_directory
    rows = matrix_tests()
    cubic_q = [F(7, 16), F(9, 16)]
    trace_squared = F(3, 2)
    bare = sum(q * trace_squared for q in cubic_q) / 2
    sign = sum(q * (4 * (1 - q) - trace_squared) for q in cubic_q) / 2
    check((bare, sign) == (F(3, 4), F(15, 64)), "cubic sign contrast")
    result = dict(plate_order=PHASES, matrix_panels=rows, mixture=mixture_test(rows),
                  target=target_tests(), cubic_unbalanced=dict(q=cubic_q, bare=bare, sign=sign),
                  adaptive=[history_test(a) for a in (F(0), F(1), F(3, 2), F(199, 100))])
    output.mkdir(parents=True, exist_ok=True)
    with (output / "midpoint_phase.json").open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, indent=2, default=str)
        stream.write("\n")


if __name__ == "__main__":
    main()
