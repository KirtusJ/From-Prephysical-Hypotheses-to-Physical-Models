"""Exact necessary temporal-gain drift from saved circle-figure intervals."""
import json
from fractions import Fraction as F
from pathlib import Path


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def bound(source, early, late=13):
    """Necessary growth of either g7/g5 or g7/g9 from late to early."""
    bands = source["experiment_bands_5_7_9"]
    ratios = source["ideal_pair_to_target"]
    early_bands = [[F(n) for n in pair] for pair in bands[str(early)]]
    late_bands = [[F(n) for n in pair] for pair in bands[str(late)]]
    A = (early_bands[0][1], early_bands[2][1])
    C = (late_bands[0][0], late_bands[2][0])
    L = F(ratios[str(early)]) * early_bands[1][0]
    U = F(ratios[str(late)]) * late_bands[1][1]
    require(all(v > 0 for v in (*A, *C, L, U)), "positive comparison")
    m = max(A[0] / C[0], A[1] / C[1])
    K = L / (m * U)
    return K, L - m*U, m


def main():
    path = Path(__file__).with_name("unequal_circle_gains_output.json")
    source = json.loads(path.read_text(encoding="utf-8"))
    require(source["round_11_and_13_constraints"] ==
            [["97/366", "125/732", "40139/102846"],
             ["167/732", "31/183", "10252/57401"]], "original constraints drift")
    k11, margin11, m11 = bound(source, 11)
    k7, margin7, m7 = bound(source, 7)
    k9, margin9, m9 = bound(source, 9)
    require(m11 == F(194,167), "max component ratio")
    require(k11 == F(573429403,304842288), "round-eleven exact infimum")
    require(k7 > F(7,5) and k7 < F(3,2), "round-seven independent negative control")
    require(k11 > F(9,5) and k11 < F(19,10), "drift interval control")
    require(k9 < 1 and margin9 < 0, "adverse round-nine comparison remains")
    for candidate in (F(1), F(9,5), k11):
        require(margin11 - (candidate-1)*m11*F(10252,57401) >= 0,
                "excluded-drift boundary")
    require(margin11 - (F(19,10)-1)*m11*F(10252,57401) < 0,
            "relaxed inequality no longer excludes")
    print(json.dumps({
        "source": path.name,
        "necessary_relative_gain_growth_infimum_11_over_13": str(k11),
        "as_decimal": float(k11),
        "one_detector_symmetric_drift_factor_must_exceed": k11.numerator**0.5 / k11.denominator**0.5,
        "round_7_instead_of_11_infimum": str(k7),
        "round_9_adverse_infimum_below_one": str(k9),
        "fixed_gain_margin_11_13": str(margin11)
    }, indent=2))


if __name__ == "__main__":
    main()
