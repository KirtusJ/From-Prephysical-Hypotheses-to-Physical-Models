"""Double ratio of the target-port coincidences in Defienne et al., Table S1."""

import argparse
import json
import math
from fractions import Fraction
from pathlib import Path


def conditional_interval(a, b, c, d):
    """Equal-tail Fisher interval conditional on both margins of independent Poisson cells."""
    n, m, k = a + b, c + d, a + c
    lo, hi = max(0, k - m), min(n, k)
    support = range(lo, hi + 1)
    # log[C(n,x) C(m,k-x)] up to a common additive constant, using adjacent ratios.
    logs = [0.0]
    for x in range(lo, hi):
        ratio = (n - x) * (k - x) / ((x + 1) * (m - k + x + 1))
        logs.append(logs[-1] + math.log(ratio))

    def tail(theta, upper):
        weighted = [v + (x - a) * math.log(theta) for x, v in zip(support, logs)]
        maximum = max(weighted)
        probs = [math.exp(v - maximum) for v in weighted]
        cut = a - lo
        return math.fsum(probs[cut:] if upper else probs[:cut + 1]) / math.fsum(probs)

    def endpoint(upper):
        left, right = 0.5, 4.0
        if (tail(left, upper) < 0.025) != upper or (tail(right, upper) < 0.025) == upper:
            raise ValueError("Interval endpoint outside the bracket")
        for _ in range(46):
            mid = (left + right) / 2
            if (tail(mid, upper) < 0.025) == upper:
                left = mid
            else:
                right = mid
        return (left + right) / 2

    return [endpoint(True), endpoint(False)], tail(1.0, True)


def run():
    # Rows use the two route configurations; columns use matched and delayed inputs.
    a, b, c, d = 6038, 3491, 8088, 7949
    double_ratio = Fraction(a * d, b * c)
    ci, tail = conditional_interval(a, b, c, d)
    if not 1 < ci[0] < float(double_ratio) < ci[1]:
        raise ValueError("Conditional interval disagrees with observed direction")
    # Separate reported run-to-run relative errors for a,b,c,d from the table.
    rel_errors = [0.018, 0.023, 0.013, 0.021]
    max_log_se = sum(rel_errors)
    common_run_contrast = float(double_ratio) - 1
    return {
        "source_doi": "10.1126/sciadv.1501054",
        "supplement_pdf_sha256": "a81865f4c03dc24236f3ce725221d9b8e5462224104b71026e38a7758245dd62",
        "seconds_per_cell": 900, "coincidence_window_ns": 2.5,
        "row_order": ["both routes superposed", "individually directed"],
        "column_order": ["zero delay", "0.4 mm delay"],
        "target_counts": [[a, b], [c, d]], "relative_errors_in_order": rel_errors,
        "raw_count_contrasts": [str(Fraction(a, b) - 1), str(Fraction(c, d) - 1)],
        "published_contrasts_and_sd": [[0.72, 0.07], [0.017, 0.035]],
        "cross_ratio": str(double_ratio), "cross_ratio_float": float(double_ratio),
        "fixed_margins_independent_Poisson_95_interval": ci,
        "one_sided_null_inclusive_upper_tail": tail,
        "approx_log_sd_independent_reported_errors": math.hypot(*rel_errors),
        "max_linearized_log_sd_arbitrary_correlation": max_log_se,
        "approx_95_sensitivity_envelope_with_max_log_sd": [
            float(double_ratio) * math.exp(sign * 1.96 * max_log_se) for sign in (-1, 1)
        ],
        "if_directed_control_is_neutral_overlap_term": common_run_contrast,
        "if_independent_HOM_visibility_transfers_balancing_factor": common_run_contrast / 0.86,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result = run()
    with args.output.open("x", encoding="utf-8", newline="\n") as out:
        json.dump(result, out, indent=2, allow_nan=False)
        out.write("\n")
