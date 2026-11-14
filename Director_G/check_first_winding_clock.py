"""Check the winding witnesses on physical rings. Pass a fresh output directory."""

import argparse
from collections import Counter
from fractions import Fraction as F
import json
from itertools import product, zip_longest
from math import gcd
from pathlib import Path

from check_character_tomography import reduced
from check_fixed_ring_moments import at_port, check, direct_read, physical_ring


def port_contrast(a, q, d, k):
    """Return the numerator of P_plus minus P_minus at one port.

    The label-s mass difference is (zeta^(D*K*s) + zeta^(-D*K*s))/q.
    Summing over s selects lag h with h = D*K or -D*K modulo q.
    Coincident lags must contribute twice. The answer is in units of 2^-t.
    """
    shift = (d * k) % q
    return sum(a[j] * (a[(j + shift) % q] + a[(j - shift) % q]) for j in range(q))


def panel(size, q):
    d = size // gcd(size, 2)
    order = q // gcd(q, d)
    k = order // 2
    last = max(3, k*d + 1)
    clocks = range(1, last + 1)
    odd_cover = physical_ring(2*size, q, clocks) if size % 2 else None
    contrast = 0
    exclusive = None
    for t, state in physical_ring(size, q, clocks):
        if odd_cover is not None:
            cover_t, cover = next(odd_cover)
            check(cover_t == t and all(x % 2 == t % 2 for x, rail, sign, s in cover),
                  "accessible parity class")
            projected = {(x % size, rail, sign, s): v for (x, rail, sign, s), v in cover.items()}
            check(len(projected) == len(cover) and projected == state, "odd ring and its lift")
        if t == 3:
            signed, fair = at_port(state, q, -1 % size, 1)
            check(signed == [0]*q and fair == 2, "count anchor")
        if not k:
            continue
        differences = {}
        for x in range(size):
            for rail in (0, 1):
                a, _ = at_port(state, q, x, rail)
                diff = port_contrast(a, q, d, k)
                if diff:
                    differences[x, rail] = diff
        if t < last:
            check(not differences, "complete laws agreed before the last clock")
            continue
        delta_j = 2 if order % 2 == 0 else 1
        right = (t % size, 0)
        left = ((t - 2) % size, 1)
        signed_delta = 2 * (-1)**(k*d - 1) * delta_j
        check(differences == {right: signed_delta, left: -signed_delta},
              "both signs, sites and rails of the two distinguishing outputs")
        contrast = F(sum(map(abs, differences.values())), 2**(t+1))
        if order == 2:
            # Label 0 has winding phase +1. Find a lift of the effective label 1.
            other = next(s for s in range(q) if (2*d*s) % (2*q) == q)
            exclusive = []
            for port in (right, left):
                a, count = at_port(state, q, *port)
                rates = []
                for label in (0, other):
                    w = [int(s == label) for s in range(q)]
                    value = direct_read(q, a, count, w, 0)
                    check(len(value) == 1, "real winding phase")
                    rates.append(value[0])
                exclusive.append(rates)
            check(sorted(exclusive) == [[0, 4], [4, 0]], "exclusive observations in order two")
    return {"wells": size, "gain_order": q, "D": d, "Q": order, "last_clock": last,
            "odd_cover_checked": odd_cover is not None,
            "one_launch_tv_for_last_moment_pair": str(contrast) if k else None,
            "order_two_port_numerators_R_then_L": exclusive}


def minimum_launches(t):
    """Exact integer comparisons for the two sides of the 5% error boundary."""
    den = 2**(t - 2)

    def enough(n):
        return 10 * (den - 1)**n <= den**n

    low, high = 0, 1
    while not enough(high):
        low, high = high, 2*high
    while high - low > 1:
        mid = (low + high) // 2
        if enough(mid):
            high = mid
        else:
            low = mid
    check(not enough(high-1) and enough(high), "first 5 percent crossing")
    return high


def triangle_readout():
    """Enumerate four-step words and compare the optimal equal-prior two-read errors."""
    amplitudes = [Counter(), Counter()]
    for word in product((0, 1), repeat=4):
        left = sum(word)
        port = ((4 - 2*left) % 3, word[-1])
        adjacent_lefts = sum(a*b for a,b in zip(word, word[1:]))
        for phase in (0, 1):
            amplitudes[phase][port] += (-1)**(adjacent_lefts + phase*left)
    oriented = [{port: F(v*v, 16) for port, v in a.items()} for a in amplitudes]
    position = [{x: sum(p for (site, rail),p in law.items() if site == x)
                 for x in range(3)} for law in oriented]
    result = {}
    for name, (plus, minus) in (("site_and_rail", oriented), ("site_only", position)):
        check(sum(plus.values()) == sum(minus.values()) == 1, "triangle normalization")
        one = sum(min(p, minus[a]) for a,p in plus.items()) / 2
        two = sum(min(plus[a]*plus[b], minus[a]*minus[b]) for a,b in product(plus, repeat=2)) / 2
        result[name] = [str(one), str(two)]
    check(result == {"site_and_rail": ["3/8", "9/32"], "site_only": ["3/8", "19/64"]},
          "losing the final rail affects the two-launch error")
    return result


def calculate():
    cases = [(size, q) for size in range(3, 12) for q in range(1, 10)]
    cases.extend([(15, 2), (16, 21)])
    rows = [panel(size, q) for size, q in cases]
    long_row = rows[-1]
    check(long_row["last_clock"] == 81 and
          long_row["one_launch_tv_for_last_moment_pair"] == str(F(1, 2**80)),
          "previously ill-conditioned order-21 example")
    # Quadratic read in Q[zeta_q] also checks the Fourier filter at rational witness weights.
    # At Q=3 the plus weights are (4,1,1)/6 and the minus weights are (0,3,3)/6.
    for t, state in physical_ring(7, 3, {7, 8}):
        for x in range(7):
            for rail in (0, 1):
                a, count = at_port(state, 3, x, rail)
                plus = direct_read(3, a, count, [4, 1, 1], 0)
                minus = direct_read(3, a, count, [0, 3, 3], 0)
                sub = [u-v for u,v in zip_longest(plus, minus, fillvalue=0)]
                check(reduced(sub, 3) == [6*port_contrast(a, 3, 7, 1)],
                      "explicit rational order-three mixtures")
    return {"panels": rows, "triangle_equal_prior_errors_one_then_two_launches": triangle_readout(),
            "order_two_minimum_launches_for_each_error_at_most_five_percent":
            {str(size): minimum_launches(size+1) for size in (3, 7, 15)}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_directory", type=Path)
    directory = parser.parse_args().output_directory
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / "first_winding_clock.json"
    if target.exists():
        parser.exit(2, f"Refusing to overwrite {target}\n")
    result = calculate()
    with target.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write("\n")


if __name__ == "__main__":
    main()
