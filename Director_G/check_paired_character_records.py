"""Exact four-walker word, Fourier, joint-record, and failure controls."""

from collections import Counter
from fractions import Fraction as Q
from itertools import combinations, product
from math import prod
from pathlib import Path
import argparse
import json

from check_joint_phase_records import physical_label


def require(test, why):
    if not test:
        raise ValueError(why)


WALKS = tuple("".join(w) for w in product("RL", repeat=3) if w[0] != w[1])
PAIRS = tuple(combinations(range(4), 2))
SIGNS = tuple(product((-1, 1), repeat=4))
ROOTS = ((1, 0), (0, 1), (-1, 0), (0, -1))
COS = (1, 0, -1, 0)
SIN = (0, 1, 0, -1)
MATCH = ((0, 1), (2, 3))


def native_reads(s):
    """Group the actual 4^4 surviving words into pointer and two-rail exits."""
    reals, imags, counts = Counter(), Counter(), Counter()
    for word in product(WALKS, repeat=4):
        incoming = [w[1] for w in word]
        outgoing = [w[2] for w in word]
        labels = [physical_label(w, 4, 0) for w in word]
        pair_tags = tuple(incoming[i] == incoming[j] for i, j in MATCH)
        cell = (pair_tags, tuple(outgoing))
        sign = prod(row[2] for row in labels)
        real, imag = ROOTS[sum(k * row[3] for k, row in zip(s, labels)) % 4]
        reals[cell] += sign * real
        imags[cell] += sign * imag
        counts[cell] += 1
    scored = Counter()
    count_scored = Counter()
    for (tags, outgoing), count in counts.items():
        pair_codes = []
        for equal, (i, j) in zip(tags, MATCH):
            rail = 1 if outgoing[i] == outgoing[j] else -1
            pair_codes.append((-1 if equal else 1) * rail)
        cell = tags, outgoing
        scored[tuple(pair_codes)] += Q(reals[cell] ** 2 + imags[cell] ** 2, 2**12)
        count_scored[tuple(pair_codes)] += Q(count, 2**12)
    require(sum(scored.values()) == Q(1, 16), "coherent yield")
    require(sum(count_scored.values()) == Q(1, 16), "count yield")
    require(
        all(p == Q(1, 64) for p in count_scored.values()) and len(count_scored) == 4,
        "fair count",
    )
    return scored


def product_moments(law):
    def mean(idx):
        return sum(w * prod(s[i] for i in idx) for s, w in law.items())

    return [mean(pair) for pair in PAIRS], mean(range(4))


def sharp_interval(means):
    base = {
        s: 1 + sum(v * s[i] * s[j] for (i, j), v in zip(PAIRS, means)) for s in SIGNS
    }
    return max(-b for s, b in base.items() if prod(s) == 1), min(
        b for s, b in base.items() if prod(s) == -1
    )


def symmetric_weights(means, t):
    return {
        s: (1 + sum(v * s[i] * s[j] for (i, j), v in zip(PAIRS, means)) + t * prod(s))
        / 16
        for s in SIGNS
    }


def marginals(law, idx):
    result = Counter()
    for s, w in law.items():
        result[tuple(s[i] for i in idx)] += w
    return result


def four_signs():
    panels = {}
    for s in SIGNS:
        rows = native_reads(s)
        require(rows[(s[0] * s[1], s[2] * s[3])] == Q(1, 16), "wrong native signs")
        panels[str(s)] = {str(k): str(v) for k, v in sorted(rows.items())}
    laws = [{s: Q(1, 8) for s in SIGNS if prod(s) == parity} for parity in (-1, 1)]
    for order in range(4):
        for idx in combinations(range(4), order):
            require(
                marginals(laws[0], idx) == marginals(laws[1], idx), "proper marginal"
            )
    for law in laws:
        means, t = product_moments(law)
        require(sharp_interval(means) == (-1, 1), "parity interval")
        restored = symmetric_weights(means, t)
        require(all(restored[s] == law.get(s, 0) for s in SIGNS), "sign reconstruction")
    independent = {s: Q(1, 16) for s in SIGNS}
    decoded = []
    for law, correlated in ((laws[0], False), (laws[1], False), (independent, True)):
        freq = Counter()
        for s, weight in law.items():
            u, v = s[0] * s[1], s[2] * s[3]
            joint = (Q(1, 8) if u == v else Q(0)) if correlated else Q(1, 16)
            for k, p in {
                (u, v): joint,
                (u, 0): Q(1, 4) - joint,
                (0, v): Q(1, 4) - joint,
                (0, 0): Q(1, 2) + joint,
            }.items():
                freq[k] += weight * p
        require(sum(freq.values()) == 1 and min(freq.values()) >= 0, "decoded law")
        decoded.append(freq)
    require(decoded[1] == decoded[2], "joint loss false pass")
    tv = (
        sum(
            abs(decoded[0][k] - decoded[1][k])
            for k in decoded[0].keys() | decoded[1].keys()
        )
        / 2
    )
    require(tv == Q(1, 16), "discrimination advantage")
    raw = {
        s: Q((i + 1) ** 2, sum(j * j for j in range(1, 17)))
        for i, s in enumerate(SIGNS)
    }
    means, t = product_moments(raw)
    lo, hi = sharp_interval(means)
    for v in (lo, t, hi):
        w = symmetric_weights(means, v)
        require(
            min(w.values()) >= 0 and product_moments(w) == (means, v),
            "sharp feasible interval",
        )
    require(
        min(symmetric_weights(means, lo - Q(1, 1000)).values()) < 0
        and min(symmetric_weights(means, hi + Q(1, 1000)).values()) < 0,
        "excluded endpoints",
    )
    return dict(
        word_panels=panels,
        decoded_tables=[{str(k): str(v) for k, v in d.items()} for d in decoded],
        parity_minus_means=product_moments(laws[0]),
        parity_plus_means=product_moments(laws[1]),
        asymmetric_example=dict(means=means, fourfold=t, feasible=[lo, hi]),
    )


def full_fourier():
    labels = tuple(product(range(4), repeat=4))
    raw = Counter(
        {
            (1, 1, 1, 1): 13,
            (1, 1, 1, 3): 11,
            (1, 3, 0, 2): 7,
            (0, 0, 0, 0): 5,
            (2, 2, 2, 2): 3,
            (2, 0, 1, 0): 2,
        }
    )
    count = 5
    den = sum(raw.values()) + count
    coeffs = []
    for lag in labels:
        total = 0
        for s, mass in raw.items():
            angles = [i * j % 4 for i, j in zip(lag, s)]
            expansion = 0
            for width in (0, 2, 4):
                for subset in combinations(range(4), width):
                    term = prod(
                        SIN[a] if k in subset else COS[a] for k, a in enumerate(angles)
                    )
                    expansion += (-1) ** (width // 2) * term
            require(expansion == COS[sum(angles) % 4], "matching contrast identity")
            total += mass * expansion
        coeffs.append(total)
    require(den - coeffs[0] == count, "global fair count")
    recovered = {}
    for s in labels:
        numerator = sum(
            v * COS[sum(i * j for i, j in zip(s, lag)) % 4]
            for v, lag in zip(coeffs, labels)
        )
        wanted = Q(raw[s] + raw[tuple(-i % 4 for i in s)], 2 * den)
        sym = Q(numerator, len(labels) * den)
        require(sym == wanted, "inverse Fourier")
        if sym:
            recovered[str(s)] = str(sym)
    return dict(
        count_weight=str(Q(count, den)),
        symmetrized_weights=recovered,
        moment_numerators=coeffs,
        denominator=den,
        lag_order="lexicographic 0 through 3",
    )


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("output", type=Path)
    out = ap.parse_args().output
    result = dict(
        three_tick_experiment=four_signs(), all_order_four_frequencies=full_fourier()
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("x", encoding="utf8", newline="\n") as stream:
        json.dump(result, stream, indent=2, default=str)
        stream.write("\n")


if __name__ == "__main__":
    main()
