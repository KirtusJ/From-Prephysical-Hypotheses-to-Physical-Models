"""Calibrate count and folded characters on the same uniform-force walk used for flight.

Run python -B check_force_response_calibration.py results. For calibration the
port probabilities are checked in the exact cyclotomic ring. Filtered flights
also have an independent finite momentum-integral check.
"""

import argparse
import json
import math
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from check_character_tomography import (
    Rank,
    correlate,
    direct_lag,
    port_poly,
    reduced,
    scalar,
    step,
    word_data,
)


def uniform_gain(x):
    return x


def port_rows(counts, signed, m):
    ports = {port: [0] * m for port in counts}
    for (x, c, y), value in signed.items():
        ports[x, c][y] = value
    return {port: (counts[port], correlate(v)) for port, v in ports.items()}


def fold(j, m):
    return min(j % m, (-j) % m)


def calibration(m):
    order = m // math.gcd(m, 2)
    half = order // 2
    cap = max(6, half + 2)
    assert cap < 2 * m or m == 3
    g = math.gcd(2, m)
    # For each difference in gain phase, find the lag of its half (on
    # the odd order this is a bijection). Only even residues occur if M is even.
    lag = [None] * m
    for j in range(order):
        lag[2 * j % m] = fold(j, order)
    counts = {(0, 1): 1}
    signed = {(0, 1, 0): 1}
    all_rank = Rank()
    ranks = []
    one_left = {}
    five = None
    concrete_words = []
    for t in range(1, cap + 1):
        counts, signed = step(counts, signed, m, uniform_gain)
        rows = port_rows(counts, signed, m)
        if t <= 6:
            direct = Counter()
            for word in product((1, -1), repeat=t):
                (x, c), y, v = word_data(word, m, gain=uniform_gain)
                direct[x, c, y % m] += v
                if t == 5 and (x, c) == (1, 1):
                    concrete_words.append([word, y, v])
            assert signed == {k: v for k, v in direct.items() if v}
        for port, (N, ac) in sorted(rows.items()):
            coeff = [0] * (half + 1)
            coeff[0] = N - ac[0]  # C(0)=1-c left as the affine constant
            for u in range(1, m):
                if ac[u]:
                    assert lag[u] is not None
                    coeff[lag[u]] += ac[u]
            all_rank.enter(coeff, (t, *port))
        ranks.append(len(all_rank.rows))
        if t >= 2:
            n = t - 1
            key = (n - 1, 1)
            N, ac = rows[key]
            assert N == n
            expected = Counter((2 * j) % m for j in range(n))
            assert ac == correlate([expected[y] for y in range(m)])
            one_left[n] = N, ac
        if t == 5:
            five = rows[1, 1]
    assert ranks[-1] == 1 + half and five[0] == 6
    c = 3
    weights = [1 + (11 * k + 7) % 17 for k in range(m)]
    denom = c + sum(weights)
    W = [scalar(0, m)] + [port_poly(*one_left[n], c, weights) for n in range(1, cap)]
    twice = {}
    for j in range(1, cap - 1):
        twice[j] = [a - 2 * b + d for a, b, d in zip(W[j + 1], W[j], W[j - 1])]
        assert reduced(twice[j], m) == reduced(direct_lag(weights, 2 * j), m)
    at_five = port_poly(*five, c, weights)
    signed_expected = scalar(4 * denom, m)
    for j, frac in enumerate((-2, 1, -2, 1), 1):
        signed_expected = [u + frac * v for u, v in zip(signed_expected, twice[j])]
    c_twice = reduced([a - b for a, b in zip(at_five, signed_expected)], m)
    assert c_twice == [2 * c]
    # Exact inverse DFT in the subcycle of order 'order', embedded back
    # in Z[zeta_M]. D_j has Fourier phase exp(2*pi*i*(2/g)*k*j/order).
    # Keeping the latter modular multiplier is essential at odd M.
    twice[0] = scalar(2 * (denom - c), m)
    class_weights = Counter()
    branches = defaultdict(list)
    for k, w in enumerate(weights):
        cls = fold((2 // g) * k, order)
        class_weights[cls] += w
        branches[cls].append(k)
    for s in range(half + 1):
        ans = scalar(0, m)
        for j in range(order):
            for e, z in enumerate(twice[fold(j, order)]):
                ans[(e - g * s * j) % m] += z
        result = reduced(ans, m)
        mult = 1 if 2 * s % order == 0 else 2
        assert result == [2 * order * class_weights[s] // mult]
    return {
        "M": m,
        "base_order": 4 * m,
        "folded_cycle_order": order,
        "cap_for_explicit_recovery": cap,
        "affine_rank_from_all_ports_each_tick": ranks,
        "first_full_rank": ranks.index(half + 1) + 1,
        "rank_witness_port_rows": all_rank.witness,
        "count_fraction_recovered": str(F(c, denom)),
        "folded_classes_and_exact_recovered_weights": [
            [s, branches[s], str(F(class_weights[s], denom))] for s in range(half + 1)
        ],
        "five_tick_words_once": concrete_words if m == 5 else None,
    }


def count_distribution(m_blocks, flight_ticks):
    # Given the prescribed alternate direction, one unrevealed fair direction
    # remains per two-tick block. All later flight directions are fair.
    n = m_blocks + flight_ticks
    offset = -(m_blocks % 2)
    return {offset + 2 * j - n: F(math.comb(n, j), 2**n) for j in range(n + 1)}


def filtered_state(m, blocks, flight):
    counts = {(0, 1): 1}
    signed = {(0, 1, 0): 1}
    prep_count = None
    prep_sig = None
    for t in range(1, 2 * blocks + flight + 1):
        counts, signed = step(counts, signed, m, uniform_gain)
        if t <= 2 * blocks and t % 2 == 0:
            required = (-1) ** (t // 2)
            counts = {p: n for p, n in counts.items() if p[1] == required}
            signed = {p: n for p, n in signed.items() if p[1] == required}
        if t == 2 * blocks:
            prep_count = sum(counts.values()) / 4**blocks
            prep_sig = port_rows(counts, signed, m)
    return prep_count, prep_sig, counts, port_rows(counts, signed, m)


def sector_positions(rows, m, k, den):
    roots = [math.cos(2 * math.pi * k * r / m) for r in range(m)]
    out = defaultdict(float)
    for (x, _), (_, ac) in rows.items():
        out[x] += sum(a * r for a, r in zip(ac, roots)) / den
    return dict(out)


def fold_and_flight(m, blocks, flight, prior):
    assert 2 * blocks + flight < 2 * m  # use ring centred coordinates without wraps
    count_p, prep, counts, post = filtered_state(m, blocks, flight)
    assert count_p == 2 ** (-blocks)
    den = 2 ** (2 * blocks + flight)
    x_stats = count_distribution(blocks, flight)
    actual = Counter()
    for (x, _), n in counts.items():
        actual[x] += n
    assert {k % (4 * m): v for k, v in x_stats.items()} == {
        x: F(n, sum(counts.values())) for x, n in actual.items()
    }
    laws = []
    acceptance = []
    p0 = F(math.comb(2 * blocks, blocks), 4**blocks)
    for k in range(m):
        pre = sector_positions(prep, m, k, 4**blocks)
        q = sum(pre.values())
        h = 2 * math.pi * k / m
        nodes = 2 * blocks + 1
        integrate = (
            sum(
                math.prod(
                    math.sin(2 * math.pi * j / nodes + (2 * i + 1) * h) ** 2 for i in range(blocks)
                )
                for j in range(nodes)
            )
            / nodes
        )
        assert abs(integrate - q) < 1e-12 and 0 < q <= float(p0) + 1e-12
        if 4 * k % m == 0:
            assert abs(q - float(p0)) < 1e-12
        law = sector_positions(post, m, k, den)
        assert abs(sum(law.values()) - q) < 1e-12
        laws.append(law)
        acceptance.append(q)
    for k in range(m):
        aliases = {(-k) % m}
        if m % 2 == 0:
            aliases.add((k + m // 2) % m)
        for j in aliases:
            assert all(abs(p - laws[j].get(x, 0)) < 1e-12 for x, p in laws[k].items())
    total_prob = prior[0] * count_p + sum(a * b for a, b in zip(prior[1:], acceptance))
    bayes = [prior[0] * count_p / total_prob] + [
        a * q / total_prob for a, q in zip(prior[1:], acceptance)
    ]
    assert abs(sum(bayes) - 1) < 1e-12
    mixed = defaultdict(float)
    for x, v in x_stats.items():
        mixed[x % (4 * m)] += bayes[0] * float(v)
    for component, post_weight, q in zip(laws, bayes[1:], acceptance):
        for x, p in component.items():
            mixed[x] += post_weight * p / q
    assert abs(sum(mixed.values()) - 1) < 1e-12
    return {
        "M": m,
        "blocks": blocks,
        "flight_ticks": flight,
        "counterfactual_pure_count_pass": str(F(1, 2**blocks)),
        "zero_signed_exact_pass_and_Holder_ceiling": str(p0),
        "k0_count_posterior_odds_multiplier_count_over_k0": str(
            F(2**blocks, math.comb(2 * blocks, blocks))
        ),
        "prior_count_then_k0_through_Mminus1": prior,
        "pass_by_character": acceptance,
        "unconditional_mixed_pass": total_prob,
        "rejected_mass": 1 - total_prob,
        "normalized_post_weights": bayes,
        "position_and_conditional_flight_mass": [
            [x if x < 2 * m else x - 4 * m, p] for x, p in sorted(mixed.items())
        ],
        "count_conditional_mean_lattice": -(blocks % 2),
        "count_conditional_variance_lattice": blocks + flight,
    }


def dyadic_pass_controls():
    rows = []
    for b in (1, 2, 3, 4):
        delta = 2 ** (-b)
        m = round(delta ** (-2.5) / 2) * 2
        M = 2 ** (4 * b)
        h = 2 * math.pi / M
        nodes = 2 * m + 1
        weak = (
            sum(
                math.prod(math.cos(2 * math.pi * q / nodes + (2 * i + 1 - m) * h) ** 2 for i in range(m))
                for q in range(nodes)
            )
            / nodes
        )
        peak = F(math.comb(2 * m, m), 4**m)
        counted = F(1, 2**m)
        accept = (float(counted) + weak) / 2
        assert 0 < weak <= float(peak) + 1e-14
        rows.append(
            {
                "epsilon_delta": delta,
                "M": M,
                "effective_F": 2 * math.pi,
                "even_blocks": m,
                "prior_equal_count_and_weak_pair": True,
                "weak_character_pass": weak,
                "weak_pass_over_Holder_ceiling": weak / float(peak),
                "quarter_turn_pass_over_ceiling": 1,
                "zero_field_pass_over_ceiling": 1,
                "mixed_pass": accept,
                "conditional_count_weight": float(counted) / (2 * accept),
                "conditional_weak_weight": weak / (2 * accept),
                "zero_field_count_odds_log2_multiplier": m - math.log2(math.comb(2 * m, m)),
                "scaled_count_variance_after_DO": delta**4 * m,
            }
        )
    return rows


def main():
    orders = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 16, 21, 25, 32, 63]
    trials = [calibration(m) for m in orders]
    flight_trials = []
    for m, blocks, flight in ((5, 2, 3), (8, 4, 4), (12, 6, 5), (31, 8, 10)):
        raw = [3] + [1 + ((7 * j + 2) % m) for j in range(m)]
        flight_trials.append(fold_and_flight(m, blocks, flight, [v / sum(raw) for v in raw]))
    return {
        "scope": "All examples use the same g(x)=x signed H walk from a localized (0,R) on C_(4M), "
        "without an address-dependent staircase or added sheet measurement. Coefficients are the "
        "normalized effective counting and fixed character responses of the specified preparation. "
        "Repeat terminal launches for different calibration settings. Prediction across a DO herald "
        "requires fixed shared components through that flight and the coherent direction-only instrument.",
        "one_left_formula": "Let D_j=sum b_k cos(4*pi*k*j/M). W_n=2^(n+1)P_{n+1}(n-1,R) "
        "=n+2*sum_{j=1}^{n-1}(n-j)D_j. The symmetric second difference is 2D_n. "
        "Adjacent LR/RL exchanges raise area by two, and every witness word is positive.",
        "six_tick_count": "The (1,R) numerator at t=5 is 4+2c-4D_1+2D_2-4D_3+2D_4. The one-left "
        "record through six ticks supplies all four lags. Subtract to recover c. At this same port "
        "pure count gives 6/32, unforced k=0 gives zero, while uniform signed characters give "
        "4/32 when the five even-area residues are distinct. Nyquist is inseparable from k=0 for even M.",
        "identified_class": "For H=M/gcd(M,2), identify s=fold_H((2/gcd(M,2))*k) in the inverse "
        "real Fourier transform. For even M, conjugation and adding M/2 have identical base-port "
        "laws: area at each depth has parity n*x0+n(n-1)/2, independent of history. The common sign "
        "survives native repeated coordinate/DO readouts at known ticks on one localized parity; "
        "coherent inter-parity preparations and operations need not share this alias. For a class "
        "s the physical phase distance from the nearest multiple of pi is pi*s/H.",
        "exact_terminal_tests": trials,
        "direction_only_pass": "Alternate two-tick outcomes L,R,L,... from initial R, preserving "
        "all unresolved sites and sheets coherently. Classical counting has pass 2^(-m) with "
        "conditional X=-(m mod 2)+ a sum of m fair increments. Signed character h has exact pass "
        "p_m(h)=integral(prod sin²(q+(2j+1)h))dq/(2pi) on the unwrapped cover. A "
        "trigonometric quadrature with >2m points verifies the integral. Generalized Holder gives "
        "p_m(h)<=binom(2m,m)/4^m. Both k=0 and a quarter turn h=pi/2 attain the upper bound; "
        "the latter is not in general a weak-force component.",
        "finite_predicted_flights": flight_trials,
        "dyadic_scaling_controls": dyadic_pass_controls(),
        "two_ray_scope": "For weak effective slope h_eff reduced modulo pi and conjugation, put "
        "|F_s|=(pi*s/H)/(epsilon*delta^3). In a calibrated finite mixture of bounded force "
        "magnitudes satisfying the two-ray hypotheses with epsilon=delta, even m nearest delta^(-5/2), "
        "each good success is p_m(0)(1+o(1)); its limiting characteristic function at fixed time T "
        "is cos(xi*|F_s|*T²/2) for common centre zero. The conditional mixture uses actual posterior "
        "weights, counting contributes the central point (scaled variance (epsilon*delta)^2(m+n)), "
        "and signed zero effective field contributes the same central point. Earlier unfiltered "
        "terminal ports distinguish these latter mechanisms. Among weak signed branches the filter "
        "preserves relative weights asymptotically. Count to weak signed odds are suppressed by "
        "sqrt(pi*m)*2^(-m) when that signed prior is appreciable. A pure counting run still "
        "passes rarely and stays central. If unwanted preweight eta outside a weak target family "
        "tends to zero then its postweight also tends to zero by Holder; no stronger prior "
        "rate is required for this particular filter. Strong or resonant components of appreciable "
        "posterior cannot be assigned weak rays. Scaling limits and a physical measurement law "
        "are assumptions here, not inferred from these finite records.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    out = main()
    args.directory.mkdir(parents=True, exist_ok=True)
    (args.directory / "force_response_calibration.json").write_text(
        json.dumps(out, indent=2) + "\n", encoding="utf8"
    )
    print(
        "Verified",
        len(out["exact_terminal_tests"]),
        "exact inversions and",
        len(out["finite_predicted_flights"]),
        "heralded flights.",
    )
