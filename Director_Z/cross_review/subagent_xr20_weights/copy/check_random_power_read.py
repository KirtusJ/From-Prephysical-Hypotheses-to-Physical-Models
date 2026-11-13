"""Randomized translation-power comparator; exact records and folded inversion.

Run python -B check_random_power_read.py OUTPUT_DIRECTORY. Formal harmonic
coefficients use exact fractions. Numerical cosines are an independent check.
"""

import argparse
import json
from fractions import Fraction as F
from math import ceil, cos, log, sin, sqrt, tau
from pathlib import Path


def mult(m, k):
    return 1 if (2 * k) % m == 0 else 2


def harmonic(m, k, l):
    """Uniform-power mean of cos(kdh) cos(ldh), as a root-of-unity sum."""
    return F(int((k - l) % m == 0) + int((k + l) % m == 0), 2)


def exact_law(m, w):
    assert len(w) == m // 2 + 1 and 0 <= sum(w) <= 1
    q = []
    for k, wk in enumerate(w):
        b = mult(m, k) * sum(v * harmonic(m, k, j) for j, v in enumerate(w))
        second = mult(m, k) ** 2 * harmonic(m, k, k)
        assert b == wk and second == mult(m, k)
        q.append([str(b), str(second)])
    squares = sum(v * v / mult(m, j) for j, v in enumerate(w))
    same = sum(v / mult(m, j) for j, v in enumerate(w))
    assert squares <= same
    return {
        "weights_count_is_complement": list(map(str, w)),
        "count": str(1 - sum(w)),
        "E_Z_and_E_Z_squared": q,
        "same_d_independent_source_pair_sign_product": str(squares),
        "same_d_retained_sector_pair_sign_product": str(same),
    }


def trial(m, rows, count):
    """Full signed two-H circuit, including d=0 and all unresolved rows."""
    norm = sum(v * v for r in rows for v in r)
    results = []
    retained = []
    for d in range(m):
        power = []
        for s in (1, -1):
            post = [[v + s * r[(y - d) % m] for y, v in enumerate(r)] for r in rows]
            n = sum(v * v for r in post for v in r)
            power.append(F(n, 4 * norm))
        assert sum(power) == 1
        # Counting H branches have a distinct elementary history even at
        # d=0, with two unit-sign-insensitive histories per output.
        path_counts = []
        for final in (0, 1):
            bins = [0] * m
            for r in rows:
                for y, v in enumerate(r):
                    for first in (0, 1):
                        bins[(y + first * d) % m] += v * v
            path_counts.append(F(sum(bins), 4 * norm))
        assert path_counts == [F(1, 2), F(1, 2)]
        probabilities = [(1 - count) * p + count * c for p, c in zip(power, path_counts)]
        assert sum(probabilities) == 1
        results.append(probabilities[0] - probabilities[1])
        # Two successive same-d reads retaining the sheet. The numerator
        # of their signed-product mean is the difference of four path norms.
        repeated = 0
        for s in (1, -1):
            after = [[v + s * r[(y - d) % m] for y, v in enumerate(r)] for r in rows]
            for t in (1, -1):
                n = sum((v + t * r[(y - d) % m]) ** 2 for r in after for y, v in enumerate(r))
                repeated += s * t * F(n, 16 * norm)
        retained.append((1 - count) * repeated)
    assert results[0] == 1 - count
    table = []
    for k in range(m // 2 + 1):
        z = complex(cos(tau * k / m), sin(tau * k / m))
        b = (
            mult(m, k)
            * (1 - count)
            * sum(abs(sum(v * z**y for y, v in enumerate(r))) ** 2 for r in rows)
            / (m * norm)
        )
        fit = mult(m, k) * sum(c * cos(tau * k * d / m) for d, c in enumerate(results)) / m
        assert abs(b - fit) < 1e-12
        table.append(fit)
    assert abs(sum(table) + count - 1) < 1e-12
    independent = sum(c * c for c in results) / m
    same = sum(retained) / m
    assert abs(independent - sum(w * w / mult(m, j) for j, w in enumerate(table))) < 1e-12
    assert abs(same - sum(w / mult(m, j) for j, w in enumerate(table))) < 1e-12
    return {
        "M": m,
        "integer_rows": rows,
        "count": str(count),
        "signed_plus_minus_contrast_by_d": list(map(str, results)),
        "folded_weights_numeric": table,
        "same_d_independent_sign_product": str(independent),
        "same_d_retained_sign_product": str(same),
    }


def failures():
    m = 8
    ws = [F(1, 2), F(1, 4), F(), F(1, 4), F()]
    law = exact_law(m, ws)
    assert F(law["same_d_independent_source_pair_sign_product"]) == F(5, 16)
    assert F(law["same_d_retained_sector_pair_sign_product"]) == F(3, 4)
    # Slippage d->d+1 versus systematic unit relabeling d->3d.
    table = [sum(float(w) * cos(tau * j * (d + 1) / m) for j, w in enumerate(ws)) for d in range(m)]
    drift = []
    for j, w in enumerate(ws):
        z = mult(m, j) * sum(table[d] * cos(tau * j * d / m) for d in range(m)) / m
        assert abs(z - float(w) * cos(tau * j / m)) < 1e-12
        drift.append(z)
    pure = [
        sum(cos(tau * d / m) * cos(tau * 3 * d / m) for d in range(m)) * 2 / m,
        sum(cos(tau * 3 * d / m) ** 2 for d in range(m)) * 2 / m,
    ]
    assert abs(pure[0]) < 1e-12 and abs(pure[1] - 1) < 1e-12
    q = F(1, 4)
    flipped = [(1 - 2 * q) * w for w in ws]
    return {
        "law": law,
        "plus_one_slot_means": drift,
        "quarter_independent_sign_flip_contrasts": list(map(str, flipped)),
        "pure_1_observed_against_3_then_with_relabelled_reference": pure,
        "tagged_reference_shot_second_moment_at_pair": 4,
        "same_ensemble_independent_contrast_is_not_individually_labeled": True,
    }


def quadratic_table():
    """A nontrivial exactly invertible M=8 table over a+b sqrt(2)."""
    m = 8
    count = F(2, 7)
    seed = [1, 1, 0, 0, -1, -1, 0, 0]
    observed = trial(m, [seed], count)
    values = list(map(F, observed["signed_plus_minus_contrast_by_d"]))
    cosine = [(1, 0), (0, F(1, 2)), (0, 0), (0, -F(1, 2)), (-1, 0), (0, -F(1, 2)), (0, 0), (0, F(1, 2))]
    exact = []
    for k in range(m // 2 + 1):
        coeff = [
            sum(v * cosine[k * d % m][i] for d, v in enumerate(values)) * mult(m, k) / m for i in (0, 1)
        ]
        assert (
            abs(float(coeff[0]) + sqrt(2) * float(coeff[1]) - observed["folded_weights_numeric"][k])
            < 1e-12
        )
        exact.append(coeff)
    assert exact[1] == [F(5, 14), F(5, 28)] and exact[3] == [F(5, 14), F(-5, 28)]
    assert all(exact[k] == [0, 0] for k in (0, 2, 4))
    observed["folded_weights_as_a_plus_b_sqrt2"] = [list(map(str, r)) for r in exact]
    return observed


def main():
    formal = []
    physical = []
    expense = []
    for m in range(2, 34):
        num = m // 2 + 1
        for j in range(num):
            w = [F()] * num
            w[j] = F(1)
            formal.append({"M": m, **exact_law(m, w)})
        w = [F(j + 1, num * (num + 1)) for j in range(num)]
        formal.append({"M": m, **exact_law(m, w)})
        if m <= 12:
            rs = [
                [int(y == 0) - 2 * int(y == m - 1) for y in range(m)],
                [int(y == 1) + int(y == 2 % m) for y in range(m)],
            ]
            for c in (F(), F(2, 7), F(1)):
                physical.append(trial(m, rs, c))
        forward = F(sum(range(m)), m)
        shortest = F(sum(min(i, m - i) for i in range(m)), m)
        assert forward == F(m - 1, 2) and shortest == F(m * m // 4, m)
        if m >= 3:
            loss = 0.5 if m == 4 else (1 - cos(tau / m)) / 2
            median = ceil(log(0.5) / log(1 - loss))
            expense.append(
                {
                    "M": m,
                    "mean_forward_hops": str(forward),
                    "mean_signed_shortest_hops": str(shortest),
                    "unit_read_dark_for_pure_1": loss,
                    "one_tick_d_min_reads_for_even_chance_of_dark_vs_k0": median,
                    "random_power_E_Z_squared": 2,
                }
            )
    return {
        "ideal_harmonic_cases": formal,
        "signed_and_count_circuit_tables": physical,
        "exact_quadratic_M8_table": quadratic_table(),
        "drift_and_reuse": failures(),
        "cost_controls": expense,
        "M2_exception": "The pair 1,-1 is the self-inverse index 1; m1=1. Using 2 instead would give 2b1 and E Z²=4.",
        "protocol": "On independent common-preparation trials choose d uniformly in 0..M-1 independently after the herald. Apply H to a clean R, controlled T^d on one rail, then H and read both rails. Compare S=+1/-1. On the signed state probabilities use (I +/- T^d)/2, tracing unresolved components. On incoherent path counting each port has probability 1/2 at every d, even zero. The pure signed marker at d=0 always returns +. If the count weight is c, signed folded masses w_j sum to 1-c. Under these hypotheses E[S|d]=sum_j w_j cos(2pi jd/M).",
        "inference": "Set m_j=1 if 2j=0 mod M, else 2. Z_j=m_j S cos(2pi jd/M) has mean w_j and second moment m_j. All coordinates can use each same fresh run. With K=floor(M/2)+1, n>=8 ln(2K/alpha)/e² suffices for simultaneous absolute error e by Hoeffding and a union bound (one coordinate: use 2/alpha). Special index j has coefficient [-1,1]. Estimates can leave [0,1] on finite samples. Count c=1-E[S|0] also admits a separate calibrated d=0 subexperiment; a uniform sampler only visits it one time in M on average. Reusing a single fixed sheet does not provide independent source draws. Independent repetitions within a specified sector estimate that sector rather than an unknown ensemble. A shared reference/source state can introduce correlations even for fresh coins.",
        "relative_reference": "Inverting the full contrast against a named generator uses its known order and the ordinary numerical Fourier table as postprocessing; one need not synthesize its cosine in hardware or assume the physical sheet is a previously tagged mode. If even numerical harmonic labeling is withheld, raw d-indexed contrast and its ordinal ranking can be reported, but labeled w_1 needs a chosen convention or reference. Relabeling d and characters by a unit simultaneously permutes the harmonic names. A fresh verified folded-j reference with an independent shot at the same d gives m_j S S_ref, mean w_j; its second moment is m_j², not m_j. Comparing two unknown independent preparations instead returns sum w_j*w'_j/m_j, or sum w_j²/m_j if identical. Testing the same retained sheet twice returns sum w_j/m_j under this shift-preserving instrument and unbiased fresh counting paths.",
        "cost_and_bias": "Mean exposure (M-1)/2 forward unit hops per sample, floor(M²/4)/M if inverse hops of equal cost are allowed. Compare the unit-step k=1 vs k=0 dark marker sin²(pi/M), needing order M² fresh shots for a fixed chance to see one dark in the noise-free test. No lower bound on all possible short-setting estimators follows. If uniform ideal d is independent but binary output has pointwise TV error rho, bias <= 2 sqrt(m_j) rho by Cauchy-Schwarz. Shift slippage |Delta_d|<=s gives contrast discrepancy <=sum w_k min(2,2pi k s/M), hence estimator bias <=sqrt(m_j) times that bound. Uniform-setting TV error eta alone gives bias <=2 m_j eta for ideal conditional laws; arbitrary correlations with preparation are outside these guarantees. A fixed shift t attenuates w_j by cos(2pi jt/M); a wrong stride can relabel or alias powers. A fixed sign-flip rate p multiplies each w_j estimate by 1-2p. Systematic biases do not vanish with sample size.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    directory = parser.parse_args().directory
    result = main()
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "random_power_read.json").write_text(
        json.dumps(result, separators=(",", ":")) + "\n", encoding="utf8"
    )
    print(
        len(result["ideal_harmonic_cases"]),
        "formal cases;",
        len(result["signed_and_count_circuit_tables"]),
        "literal laws.",
    )
