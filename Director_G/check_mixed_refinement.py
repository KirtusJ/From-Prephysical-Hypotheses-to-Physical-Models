"""Native mixture anchors, monotone rail cost and finite impurity bounds.
Run python -B check_mixed_refinement.py OUTDIR. Existing results are protected."""
import argparse
import json
from collections import Counter, defaultdict
from fractions import Fraction as Q
from functools import lru_cache
from itertools import product
from math import factorial
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def fold(d, n):
    return min(d % n, (-d) % n)


def port_words(m, ticks):
    ports = defaultdict(list)
    for steps in product("RL", repeat=ticks):
        x, rail, gain, sign = 0, "R", 0, 1
        for out in steps:
            gain = (gain + x // 2) % m
            if rail == out == "L":
                sign = -sign
            x = (x + (1 if out == "R" else -1)) % (4*m)
            rail = out
        ports[x, rail].append(("".join(steps), gain, sign))
    return ports


def lag_spectrum(words, m):
    lags = Counter()
    for _, j, s in words:
        for _, k, t in words:
            lags[fold(j-k, m)] += s*t
    return Counter({i: v for i, v in lags.items() if v})


def anchors():
    cosines = {3: [Q(1), Q(-1, 2)], 4: [Q(1), Q(0), Q(-1)]}
    records = []
    for m, ticks, x, rail, expected in (
        (3, 4, 2, "R", [9, 0]), (4, 5, 3, "R", [16, 0, 0]),
        (4, 4, 0, "L", [1, 5, 1]), (4, 4, -2, "L", [1, 5, 1])
    ):
        words = port_words(m, ticks)[x % (4*m), rail]
        lags = lag_spectrum(words, m)
        scores = [sum(v*cosines[m][fold(d*j, m)] for j, v in lags.items())
                  for d in range(m//2+1)]
        require(scores == expected, "native character anchor")
        require(len(words) == (m if ticks == m+1 else 3), "count anchor")
        records.append(dict(order=m, ticks=ticks, port=[x, rail], words=words,
                            folded_cosine_coefficients=dict(sorted(lags.items())),
                            character_numerators=expected, count_numerator=len(words),
                            denominator=2**ticks))
    # Independently sum signed pairs only within terminal ports at three ticks.
    rail_rows = []
    for m in (3, 4, 5, 8):
        words_at = port_words(m, 3)
        left_lags = Counter()
        count = 0
        for (_, rail), words in words_at.items():
            if rail == "L":
                left_lags.update(lag_spectrum(words, m))
                count += len(words)
        left_lags = {k: v for k, v in left_lags.items() if v}
        bright = lag_spectrum(words_at[1, "R"], m)
        require(left_lags == {0: 4, 1: -2} and count == 4, "left total")
        require(bright == {0: 2, 1: 2} and len(words_at[1, "R"]) == 2, "bright port")
        rail_rows.append(dict(order=m, field_on_L=left_lags,
                              field_off_L=sum(left_lags.values()),
                              bright_port=dict(bright), count_L=count, denominator=8))
    return dict(short_ports=records, three_tick_rail=rail_rows)


# Rational outward enclosures of v_n(d)^2, where v_n(d)=d sinc(pi*d/n).
# Check the pi endpoints without assuming the precision of a platform float.
PI_LO = Q(3141592653589793, 10**15)
PI_HI = PI_LO + Q(1, 10**15)


def arctan_bounds(inverse, terms):
    x = Q(1, inverse)
    lo = sum((-1)**k*x**(2*k+1)/(2*k+1) for k in range(terms))
    return lo, lo + x**(2*terms+1)/(2*terms+1)


def verify_pi():
    lo5, hi5 = arctan_bounds(5, 16)
    lo239, hi239 = arctan_bounds(239, 6)
    require(PI_LO < 16*lo5-4*hi239 <= 16*hi5-4*lo239 < PI_HI, "Machin bounds")


def sinc_partial(x, last):
    return sum((-1)**j*x**(2*j)/factorial(2*j+1) for j in range(last+1))


@lru_cache(maxsize=None)
def energy_bounds(n, d):
    require(0 <= d <= n//2, "non-folded index")
    # sinc decreases on [0,pi/2], and the Taylor series alternates there.
    u = d*sinc_partial(PI_HI*d/n, 8)
    v = d*sinc_partial(PI_LO*d/n, 8)
    lo = u - d*(PI_HI*d/n)**18/factorial(19)
    return lo*lo, v*v


def monotone_cost():
    verify_pi()
    covers = positive = zero = 0
    for n in range(6, 73):
        for m in range(3, n):
            if n % m:
                continue
            covers += 1
            for d in range(n//2+1):
                b = fold(d, m)
                require(b <= d, "coarsening increased a folded residue")
                if d:
                    require(energy_bounds(n, d)[0] > energy_bounds(m, b)[1],
                            "nonzero lift did not strictly increase rail cost")
                    positive += 1
                else:
                    require(energy_bounds(n, 0) == energy_bounds(m, 0) == (0, 0),
                            "zero row")
                    zero += 1
    return dict(orders=[3, 72], proper_divisibility_pairs=covers,
                strictly_increasing_label_rows=positive, zero_rows=zero,
                enclosure="Machin pi, decreasing sinc, alternating rational Taylor brackets")


def finite_bound_rows():
    # At a fixed fine order, every sector has an (anchor, energy, bad mass)
    # vector. A linear inequality holds on their convex hull iff it holds
    # at each vertex. The following tests include all count and folded vertices
    # and check strict energy comparisons with rational outward enclosures.
    rows = []
    for m, high, orders in ((3, 2, (6, 12, 24, 60)), (4, 3, (8, 12, 24, 60))):
        for n in orders:
            tight, strict = [], []
            a, b = energy_bounds(n, 1), energy_bounds(n, high)
            require(a[0] > 0 and b[0] > a[1], "distinct reference costs")
            for d in [None, *range(n//2+1)]:
                tag = "count" if d is None else str(d)
                bad = int(d != 1)
                actual = (Q(0), Q(0)) if d is None else energy_bounds(n, d)
                # eta=16*rho/3 for order 3, eta=(5-16*P4)/2 for order 4.
                if d is None:
                    eta = 1
                elif m == 3:
                    eta = 3*int(d % 3 == 0)
                else:
                    eta = 2*int(d % 2 == 0)
                # bad <= eta + (E-A*(1-eta))/(B-A)
                # <=> E >= A*(1-bad) + B*(bad-eta).
                if d in (None, 1, high):
                    require((bad, eta) == ((1, 1) if d is None else
                                            ((0, 0) if d == 1 else (1, 0))),
                            "equality vertex")
                    tight.append(tag)
                else:
                    coefficient = bad-eta
                    upper_rhs = a[1]*(1-bad) + coefficient*b[1 if coefficient >= 0 else 0]
                    require(actual[0] > upper_rhs, "failed mixture impurity bound")
                    strict.append(tag)
            rows.append(dict(anchor_order=m, fine_order=n, high_reference=high,
                             equality_vertices=tight, strict_vertices=strict))
    return rows


def push_count_and_charges(weights, n):
    result = Counter()
    for label, weight in weights.items():
        result["count" if label == "count" else fold(label, n)] += weight
    require(sum(result.values()) == 1, "unnormalized law")
    return result


def cofinal_examples():
    specifications = {
        "ordinary": ({1: Q(1)}, 1),
        "weak_excess_only": ({1: Q(2, 3), 3: Q(1, 3)}, Q(11, 3)),
        "odd_prime_false_pass": ({3: Q(1, 2), 5: Q(1, 2)}, 17),
        "ordinary_energy_without_anchor": ({0: Q(3, 4), 2: Q(1, 4)}, 1),
        "count_with_zero_rail_excess": ({"count": Q(1)}, 0),
        "sharp_order3": ({"count": Q(1, 5), 1: Q(7, 10), 2: Q(1, 10)}, Q(11, 10)),
        "sharp_order4": ({"count": Q(1, 5), 1: Q(7, 10), 3: Q(1, 10)}, Q(8, 5)),
    }
    rows = {}
    for name, (law, expected) in specifications.items():
        energy = sum((w*k*k for k, w in law.items() if k != "count"), Q(0))
        require(energy == expected, "integer-charge moment")
        coarse3 = push_count_and_charges(law, 3)
        rho = Q(3*coarse3["count"] + 9*coarse3[0], 16)
        coarse4 = push_count_and_charges(law, 4)
        deficit = Q(2*coarse4["count"]+4*(coarse4[0]+coarse4[2]))
        bad = 1-law.get(1, 0)
        for m in (3, 4, 5, 8, 12):
            for n in (m*2, m*3, m*7):
                reduced = push_count_and_charges(push_count_and_charges(law, n), m)
                require(reduced == push_count_and_charges(law, m), "failed restriction")
        eta3, eta4 = 16*rho/3, deficit/2
        u3, u4 = (energy-1+4*eta3)/3, (energy-1+9*eta4)/8
        require(bad <= min(u3, u4), "asymptotic bounds")
        if name == "sharp_order3":
            require(bad == u3, "order-three sharpness")
        if name == "sharp_order4":
            require(bad == u4, "order-four sharpness")
        rows[name] = dict(weights={str(k): str(w) for k, w in law.items()},
                          limiting_rail_cost=str(energy), order3_null=str(rho),
                          order4_parity=str((5-deficit)/16),
                          true_nonordinary_mass=str(bad),
                          order3_uncapped_bound=str(u3), order4_uncapped_bound=str(u4))
    return rows


def run():
    return dict(scope="Finite exact word census and certified rational inequalities. "
                      "Probability data from a laboratory enter none of these tests.",
                native=anchors(), monotonic_cost=monotone_cost(),
                bounds=finite_bound_rows(), cofinal_integer_examples=cofinal_examples())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("outdir", type=Path)
    outdir = parser.parse_args().outdir
    result = run()
    outdir.mkdir(parents=True, exist_ok=True)
    with (outdir/"mixed_refinement.json").open("x", encoding="utf8", newline="\n") as f:
        json.dump(result, f, sort_keys=True, separators=(",", ":"))
        f.write("\n")
