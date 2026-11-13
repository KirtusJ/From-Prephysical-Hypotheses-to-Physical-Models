"""Fresh exact calculation of the finite experiment stated in the supplied paper.

Only the declared formulas are inputs.  No supplied program or stored results are
read.  This is shared-source checking, not independent research provenance.
The output concerns the finite 63-point model, not a continuous target interval.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import comb
from pathlib import Path
import hashlib
import json

N, M, ALPHA = 80, 4, F(1, 20)
THETAS = tuple(F(i, 6) for i in range(7))
CALIBRATION = (F(1, 5), F(1, 2), F(4, 5))
METHODS = ("joint", "plugin", "known")


@lru_cache(None)
def integer_binomial(n, probability):
    a, b = probability.numerator, probability.denominator
    weights = tuple(comb(n, k) * a**k * (b - a)**(n - k)
                    for k in range(n + 1))
    denominator = b**n
    assert sum(weights) == denominator
    return weights, denominator


@lru_cache(None)
def accepted_counts(n, probability, error, strict=True):
    weights, denominator = integer_binomial(n, probability)
    threshold = error / 2
    accepted = set()
    lower = 0
    for k, weight in enumerate(weights):
        upper = denominator - lower
        lower += weight
        left = min(lower, upper) * threshold.denominator
        right = threshold.numerator * denominator
        if left > right if strict else left >= right:
            accepted.add(k)
    return frozenset(accepted)


def value(q):
    return {"fraction": str(q), "decimal": float(q)}


def rectangle_projection(p, f, s):
    lower, upper = F(0), F(1)
    # Both constraints have the form coefficient * theta <= bound.
    for coefficient, bound in ((s[0] - f[0], p[1] - f[0]),
                               (f[1] - s[1], f[1] - p[0])):
        if coefficient == 0:
            if bound < 0:
                return None
        elif coefficient > 0:
            upper = min(upper, bound / coefficient)
        else:
            lower = max(lower, bound / coefficient)
    return None if lower > upper else (lower, upper)


def main():
    parameters = []
    law_targets = {}
    for theta, f, s in product(THETAS, CALIBRATION, CALIBRATION):
        p = (1 - theta) * f + theta * s
        parameters.append((theta, f, s, p))
        law_targets.setdefault((p, f, s), set()).add(theta)
    assert len(parameters) == 63 and len(law_targets) == 45

    outcomes = tuple(product(range(N + 1), range(M + 1), range(M + 1)))
    joint_sets, plugin_sets = {}, {}
    for x, z0, z1 in outcomes:
        joint_sets[x, z0, z1] = frozenset(
            theta for theta, f, s, p in parameters
            if x in accepted_counts(N, p, ALPHA / 3)
            and z0 in accepted_counts(M, f, ALPHA / 3)
            and z1 in accepted_counts(M, s, ALPHA / 3))
        plugin_sets[x, z0, z1] = frozenset(
            theta for theta in THETAS
            if x in accepted_counts(N, (1 - theta) * F(z0, M)
                                    + theta * F(z1, M), ALPHA))
    known_sets = {
        (f, s, x): frozenset(theta for theta in THETAS
                            if x in accepted_counts(N, (1 - theta) * f
                                                    + theta * s, ALPHA))
        for f, s, x in product(CALIBRATION, CALIBRATION, range(N + 1))
    }

    records = []
    for (p, f, s), targets in sorted(law_targets.items()):
        wx, dx = integer_binomial(N, p)
        wf, df = integer_binomial(M, f)
        ws, ds = integer_binomial(M, s)
        denominator = dx * df * ds
        total_weight = admission_weight = 0
        sums = {name: {"whole": 0, "empty": 0, "size": 0,
                       "points": {theta: 0 for theta in targets}}
                for name in METHODS}
        for x, z0, z1 in outcomes:
            weight = wx[x] * wf[z0] * ws[z1]
            total_weight += weight
            admitted = (x in accepted_counts(N, p, ALPHA / 3)
                        and z0 in accepted_counts(M, f, ALPHA / 3)
                        and z1 in accepted_counts(M, s, ALPHA / 3))
            if admitted:
                admission_weight += weight
                assert targets <= joint_sets[x, z0, z1]
            for name, reported in (
                    ("joint", joint_sets[x, z0, z1]),
                    ("plugin", plugin_sets[x, z0, z1]),
                    ("known", known_sets[f, s, x])):
                item = sums[name]
                if targets <= reported:
                    item["whole"] += weight
                if not reported:
                    item["empty"] += weight
                item["size"] += len(reported) * weight
                for theta in targets:
                    if theta in reported:
                        item["points"][theta] += weight
        assert total_weight == denominator
        methods = {}
        for name, sums_for_method in sums.items():
            methods[name] = {
                "whole_set_coverage": value(F(sums_for_method["whole"], denominator)),
                "empty_probability": value(F(sums_for_method["empty"], denominator)),
                "expected_cardinality": value(F(sums_for_method["size"], denominator)),
                "point_coverage": {
                    str(theta): value(F(numerator, denominator))
                    for theta, numerator in sorted(sums_for_method["points"].items())}
            }
        admission_product = F(1)
        for n, probability in ((N, p), (M, f), (M, s)):
            w, d = integer_binomial(n, probability)
            admission_product *= F(sum(w[k] for k in accepted_counts(
                n, probability, ALPHA / 3)), d)
        assert F(admission_weight, denominator) == admission_product
        assert F(sums["joint"]["whole"], denominator) >= 1 - ALPHA
        assert F(sums["known"]["whole"], denominator) >= 1 - ALPHA
        records.append({
            "law": {"p": str(p), "f": str(f), "s": str(s)},
            "identified_targets": [str(t) for t in sorted(targets)],
            "count_triples": len(outcomes),
            "true_law_admission": value(admission_product),
            "methods": methods
        })

    summary = {}
    for method in METHODS:
        whole = [(F(r["methods"][method]["whole_set_coverage"]["fraction"]), r["law"])
                 for r in records]
        points = [(F(v["fraction"]), r["law"], t)
                  for r in records
                  for t, v in r["methods"][method]["point_coverage"].items()]
        low_whole = min(q for q, _ in whole)
        low_point = min(q for q, _, _ in points)
        summary[method] = {
            "minimum_whole_coverage": value(low_whole),
            "whole_minimizers": [law for q, law in whole if q == low_whole],
            "laws_below_nominal_whole_coverage": sum(q < 1 - ALPHA for q, _ in whole),
            "minimum_point_coverage": value(low_point),
            "point_minimizers": [{"law": law, "theta": t}
                                 for q, law, t in points if q == low_point]
        }

    q, error = F(1, 40), F(1, 20)
    w, d = integer_binomial(1, q)
    tail_boundary = {
        "n": 1, "q": str(q), "error": str(error),
        "strict_accepted_counts": sorted(accepted_counts(1, q, error, True)),
        "closed_accepted_counts": sorted(accepted_counts(1, q, error, False)),
        "strict_coverage": value(F(sum(w[k] for k in accepted_counts(1, q, error, True)), d)),
        "closed_coverage": value(F(sum(w[k] for k in accepted_counts(1, q, error, False)), d))
    }

    # Explicit adverse check if source/reference independence is removed.
    # Both alternatives have Z0 ~ Bern(f), Z1 ~ Bern(s), with independent
    # reference streams.  Under target zero X=Z0; under target one X=1-Z0.
    delta = F(1, 10)
    f, s = F(1, 2) - delta, F(1, 2) + delta
    a, b = {}, {}
    for z0, z1 in product((0, 1), repeat=2):
        mass = (f if z0 else 1 - f) * (s if z1 else 1 - s)
        a[z0, z0, z1] = mass
        b[1 - z0, z0, z1] = mass
    joint_tv = sum(abs(a.get(k, 0) - b.get(k, 0)) for k in set(a) | set(b)) / 2
    assert joint_tv == 1
    dependence_control = {
        "delta": str(delta), "source_TV": str(2 * delta),
        "full_data_TV": str(joint_tv),
        "same_joint_reference_law": True,
        "violated_assumption": "Source observations are not independent of calibration data.",
        "scope": "Necessity of the supplied theorem's independence premise; not a counterexample to that theorem."
    }

    # Tail bounds: sum_{n>R} n^-3 <= 1/(2 R^2),
    # sum_{n>R} n^-2 <= 1/R.  These give certified rational Gibbs-mean bounds.
    cutoff = 64
    zpartial = F(1) + sum((F((2**n) // n**3, 2**n)
                          for n in range(1, cutoff + 1)), F(0))
    mpartial = sum((F(n * ((2**n) // n**3), 2**n)
                    for n in range(1, cutoff + 1)), F(0))
    mean_lower = mpartial / (zpartial + F(1, 2 * cutoff**2))
    mean_upper = (mpartial + F(1, cutoff)) / zpartial
    assert 0 < mean_lower < mean_upper < 1
    entropy_control = {
        "cost_levels": "g_n=floor(2^n/n^3), n>=1, plus one zero-cost symbol",
        "inverse_temperature": "ln(2)", "cutoff": cutoff,
        "Z_lower": value(zpartial),
        "Z_upper": value(zpartial + F(1, 2 * cutoff**2)),
        "mean_cost_lower": value(mean_lower), "mean_cost_upper": value(mean_upper),
        "limitation": "These bounds check the stated mean below one. The infinite nonattainment argument is analytic, not inferred from finite truncation."
    }
    floor = rectangle_projection((F(1, 2), F(1, 2)),
                                 (F(1, 5), F(3, 10)),
                                 (F(7, 10), F(4, 5)))
    assert floor == (F(2, 5), F(3, 5))
    output = {
        "provenance": "Fresh formula-based exact calculation with shared source/model exposure; no supplied result file used as input.",
        "model": {"source_size": N, "reference_sizes": [M, M],
                  "alpha": str(ALPHA), "thetas": [str(t) for t in THETAS],
                  "calibration_probabilities": [str(c) for c in CALIBRATION],
                  "parameter_points": len(parameters), "distinct_laws": len(records),
                  "independent_streams": True, "strict_inclusive_tail_acceptance": True},
        "summary": summary, "laws": records,
        "tail_boundary_control": tail_boundary,
        "dependence_control": dependence_control,
        "entropy_control": entropy_control,
        "calibration_floor": [str(t) for t in floor],
        "source_script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    }
    path = Path(__file__).with_name("Declared_Calibration_Exact_Checks.json")
    if path.exists():
        raise FileExistsError(path)
    path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(path), "summary": summary,
                      "tail_boundary_control": tail_boundary,
                      "dependence_control": dependence_control,
                      "entropy_mean_upper": entropy_control["mean_cost_upper"]},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
