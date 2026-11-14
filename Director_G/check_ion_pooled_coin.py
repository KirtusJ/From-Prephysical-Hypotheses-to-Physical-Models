"""Reproduce the three-step pooled-coin comparison; pass a new JSON output path."""

import argparse
import json
from collections import defaultdict
from decimal import Decimal, localcontext
from fractions import Fraction as F
from math import factorial
from pathlib import Path


def check(condition, description):
    if not condition:
        raise ValueError(description)


def coin_step(bright, dark):
    next_bright = defaultdict(int)
    next_dark = defaultdict(int)
    for k in bright.keys() | dark.keys():
        next_bright[k + 1] = bright.get(k, 0) - dark.get(k, 0)
        next_dark[k - 1] = bright.get(k, 0) + dark.get(k, 0)
    return next_bright, next_dark


def norm_kernel(terms, denominator):
    kernel = defaultdict(F)
    for a, u in terms.items():
        for b, v in terms.items():
            kernel[b - a] += F(u * v, denominator)
    return {k: v for k, v in sorted(kernel.items()) if v}


def square_read(p):
    return p ** 2 / (p ** 2 + (1 - p) ** 2)


def fixed(x):
    return format(x, ".12f")


def report():
    bright, dark = {0: 1}, {}
    kernels = []
    expected = [
        {},
        {0: F(1, 2)},
        {-2: F(1, 4), 0: F(1, 2), 2: F(1, 4)},
        {-4: F(1, 8), 0: F(1, 4), 4: F(1, 8)},
    ]
    for ticks in range(4):
        b = norm_kernel(bright, 2 ** ticks)
        h = norm_kernel(dark, 2 ** ticks)
        for k in b.keys() | h.keys():
            check(b.get(k, 0) + h.get(k, 0) == int(k == 0), "total unit mass")
        check(h == expected[ticks], "dark-sector norm coefficients")
        kernels.append({str(k): str(v) for k, v in h.items()})
        bright, dark = coin_step(bright, dark)

    q = F(259, 1000)
    ideal = F(1, 4)
    ideal_square = square_read(ideal)
    check(ideal_square == F(1, 10), "square response on sharp lattice")
    chord_slope = square_read(F(1, 2)) - ideal_square
    required_positive = (q - ideal_square) / chord_slope
    check(required_positive == F(159, 400), "minimum mean positive overlap")

    # All terms on clearing denominators have degree at most three. Four
    # distinct exact evaluations certify the universal polynomial identity.
    for c in map(F, (-1, 0, 1, 2)):
        denominator = c ** 2 - 2 * c + 5
        square_numerator = (1 + c) ** 2
        lhs = (1 + 4 * c) * denominator - 5 * square_numerator
        rhs = 4 * c * (1 - c) * (2 - c)
        check(lhs == rhs, "cleared chord identity")
    attained = (1 - required_positive) * ideal_square + required_positive / 2
    check(attained == q, "sharp hidden-mixture equality")

    # Z has equally likely eigenvalues +/-z. With z=(1+it)/sqrt(1+t²),
    # its first moment vanishes. Its second real moment changes sign.
    point_models = []
    for t in (F(0), F(1, 2), F(1), F(2)):
        c = (1 - t * t) / (1 + t * t)
        h2 = (1 + F(0)) / 2
        h3 = (1 + c) / 4
        point_models.append({"t": str(t), "two_step": str(h2),
                             "c": str(c), "three_step": str(h3)})

    dark_efficiency_ratio = q * (1 - ideal_square) / (ideal_square * (1 - q))
    flip = (q - ideal_square) / (1 - 2 * ideal_square)
    check(dark_efficiency_ratio == F(777, 247) and flip == F(159, 800),
          "acceptance and confusion controls")
    for incident, target in ((ideal_square, q), (F(1, 2), F(1, 2))):
        check(flip + (1 - 2 * flip) * incident == target, "confusion witness")
    retained = dark_efficiency_ratio * ideal_square
    check(retained / (retained + 1 - ideal_square) == q, "retention witness")

    # Rational upper bounds: exp(8) strictly exceeds this partial sum.
    exp_upper = 1 / sum(F(8 ** j, factorial(j)) for j in range(26))
    sqrt_upper = F(1732051, 10_000_000)
    check(sqrt_upper ** 2 > F(3, 100), "square root upper bound")
    overlap_upper = exp_upper + 2 * sqrt_upper
    q_upper = ideal_square + chord_slope * overlap_upper
    check(overlap_upper < F(346746, 1_000_000), "vacuum overlap bound")
    check(q_upper < F(238699, 1_000_000), "square prediction bound")
    check(q - q_upper > F(2030, 100000), "remaining discrepancy")

    with localcontext() as ctx:
        ctx.prec = 50
        observed = Decimal(259) / 1000
        mass = observed.sqrt() / (observed.sqrt() + (1 - observed).sqrt())
        vacuum = Decimal(-8).exp() + 2 * Decimal("0.03").sqrt()
        bound = Decimal("0.1") + Decimal("0.4") * vacuum
        inverted = fixed(mass)
        c_inverse = fixed(4 * mass - 1)
        check(abs(square_read(mass) - observed) < Decimal("1e-48"), "inverse")
        decimal_bounds = {"overlap": fixed(vacuum), "dark": fixed(bound),
                          "discrepancy": fixed(observed - bound)}

    return {
        "measurement": {
            "2009_DOI": "10.1103/PhysRevLett.103.090504",
            "2012_DOI": "10.1088/1367-2630/14/3/035012",
            "one_and_two_bright_and_dark": {"central": "0.50", "uncertainty": "0.01"},
            "three_2009_bright_dark": ["0.741(3)", "0.259(2)"],
            "three_2012_bright_dark": ["0.741(2)", "0.259(1)"],
            "published_scan_experiments_per_point": 1500, "precision_measurements": 60000,
            "duration_detuned_about_two_percent": "both populations approximately one half",
        },
        "dark_norm_kernel_by_ticks_zero_to_three": kernels,
        "ideal_dark_ordinary_square": [str(ideal), str(ideal_square)],
        "required_ordinary_c": str(4 * q - 1),
        "single_type_square_input_and_c": [inverted, c_inverse],
        "mixed_square_minimum_mean_positive_c": str(required_positive),
        "spectral_witnesses": point_models,
        "conditional_vacuum_bounds_rounded": decimal_bounds,
        "symmetric_flip_rate": str(flip),
        "dark_over_bright_acceptance": str(dark_efficiency_ratio),
        "same_acceptance_at_balance": str(dark_efficiency_ratio / (1 + dark_efficiency_ratio)),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    encoded = (json.dumps(report(), indent=2, sort_keys=True) + "\n").encode("utf-8")
    with args.output.open("xb") as stream:
        stream.write(encoded)
