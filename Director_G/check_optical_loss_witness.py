"""Exact fixed-efficiency certificates for Xue et al.'s ten-step phase sweep.

Run python -B check_optical_loss_witness.py results. No optimizer or network
access is required. The figure intervals are graphical sensitivity inputs.
"""

import argparse
import json
from fractions import Fraction as F
from math import comb
from pathlib import Path

from check_clock_feedback import ONE, ZERO, Quad
from check_optical_walk_records import phase_sweep

MODELS = ("count", "alternate", "ordinary")
EXTENTS = ((239, 244), (156, 161), (87, 95), (82, 91), (86, 95))
FIGURE_SHA = "5a428e3e6478a1c0b808267e45da8902638ae68c21de3f32c172d477dc90535b"


def sign(value):
    """Exact order on a+b*sqrt(2), including the possible zero coefficients."""
    a, b = value.a, value.b
    if not a or not b or a * b > 0:
        return int(a + b > 0) - int(a + b < 0)
    difference = a * a - 2 * b * b
    assert difference != 0
    return (1 if a > 0 else -1) * (1 if difference > 0 else -1)


def amplitude_profiles():
    # The last direction fixes the number of right steps in the first nine.
    count = {}
    for x in range(-10, 11, 2):
        for d in (0, 1):
            first_nine_right = (x + 10) // 2 - d
            n = comb(9, first_nine_right) if 0 <= first_nine_right <= 9 else 0
            count[x, d] = Quad(F(n, 1024))
    assert sum(count.values(), ZERO) == ONE and sum((count[0, d] for d in (0, 1)), ZERO) == Quad(
        F(63, 256)
    )
    profiles = []
    for row in phase_sweep():
        sectors = {"count": count, "alternate": {}, "ordinary": {}}
        for key in count:
            x, d = key
            a, b = row["mode_coefficients"].get(f"{x},{d}", (0, 0))
            for label, s in (("alternate", -1), ("ordinary", 1)):
                sectors[label][key] = Quad(F(a, 2048), F(s * b, 2048))
        for field in sectors.values():
            assert sum(field.values(), ZERO) == ONE and all(sign(v) >= 0 for v in field.values())
        profiles.append(sectors)
    return profiles


def observed_bounds():
    def from_pixel(y):
        return (F(531, 2) - y) / 280

    graphic = [(from_pixel(bottom + 2), from_pixel(top - 2)) for top, bottom in EXTENTS]
    printed = graphic.copy()
    printed[3] = (F(648, 1000), F(672, 1000))
    return {"graphic": graphic, "printed135_and_other_graphic": printed}


def detect(profiles, weights, efficiencies):
    observed = []
    for sectors in profiles:
        detected = {}
        for key, e in efficiencies.items():
            assert 0 <= e <= 1
            detected[key] = Quad(e) * sum((weights[m] * sectors[m][key] for m in MODELS), ZERO)
        total = sum(detected.values(), ZERO)
        assert sign(total) > 0
        observed.append(sum((v for (x, _), v in detected.items() if x == 0), ZERO) / total)
    return observed


def inside(prob, interval):
    lo, hi = interval
    return sign(prob - Quad(lo)) >= 0 and sign(Quad(hi) - prob) >= 0


def certificate(profiles, bounds):
    # U and L are selected endpoints of two published return observations.
    u = bounds[0][1]
    low = bounds[3][0]
    lam = low / (4 * u)
    coefficients = {}
    mode_thresholds = {}
    for key in profiles[0]["count"]:
        centre = int(key[0] == 0)
        d = {
            m: Quad(lam * (centre - u)) * profiles[0][m][key] + Quad(low - centre) * profiles[3][m][key]
            for m in MODELS
        }
        assert sign(d["count"]) >= 0 and sign(d["alternate"]) >= 0
        if centre:
            assert sign(d["count"]) > 0 and sign(d["alternate"]) > 0
        nonordinary = d["alternate"] if sign(d["count"] - d["alternate"]) >= 0 else d["count"]
        if sign(d["ordinary"]) < 0:
            assert sign(nonordinary) > 0
            mode_thresholds[key] = nonordinary / (nonordinary - d["ordinary"])
        coefficients[key] = d
    w = mode_thresholds[0, 0]
    assert w == mode_thresholds[0, 1] and sign(w) > 0 and sign(ONE - w) > 0
    assert all(sign(r - w) >= 0 for r in mode_thresholds.values())
    assert all(sign(r - w) > 0 for (x, _), r in mode_thresholds.items() if x != 0)
    rows = []
    for key, d in coefficients.items():
        at_threshold = {}
        for m in ("count", "alternate"):
            # Test both nuisance mixtures at the endpoint. Positivity
            # for every smaller w follows by linear interpolation with w=0.
            at_threshold[m] = w * d["ordinary"] + (ONE - w) * d[m]
            assert sign(at_threshold[m]) >= 0
        rows.append(
            {
                "x": key[0],
                "rail": "V" if key[1] else "H",
                "D": {m: d[m].encode() for m in MODELS},
                "sign_D": {m: sign(d[m]) for m in MODELS},
                "sign_at_bound_against_count_and_alternate": [sign(v) for v in at_threshold.values()],
                "threshold_if_ordinary_D_negative": mode_thresholds[key].encode()
                if key in mode_thresholds
                else None,
            }
        )
    # Sharpness for the chosen two boundaries. At (-4,H) both signed
    # hypotheses have p135/p0=1/4, hence D=0 for either signed hypothesis.
    off = (-4, 0)
    assert coefficients[off]["alternate"] == coefficients[off]["ordinary"] == ZERO
    p0 = profiles[0]["ordinary"]
    ratio = (p0[0, 0] + p0[0, 1]) * Quad((1 - u) / u) / p0[off]
    assert ratio.b == 0 and ratio.a > 1
    efficiency = {key: F(int(key == off)) + F(int(key[0] == 0)) / ratio.a for key in p0}
    values = detect(profiles, {"ordinary": w, "alternate": ONE - w, "count": ZERO}, efficiency)
    assert values[0] == Quad(u) and values[3] == Quad(low)
    accepted = [inside(v, b) for v, b in zip(values, bounds)]
    assert accepted == [True, False, False, True, False]
    return {
        "U_at_zero_degrees": str(u),
        "L_at_135_degrees": str(low),
        "multiplier": str(lam),
        "sharp_two_setting_ordinary_floor": w.encode(),
        "limiting_centre_modes": [[0, "H"], [0, "V"]],
        "all_mode_coefficients_and_signs": rows,
        "two_setting_extremizer": {
            "ordinary": w.encode(),
            "alternate": (ONE - w).encode(),
            "count": "0",
            "efficiencies": {str(key): str(e) for key, e in efficiency.items() if e},
            "remaining_efficiencies": "0",
            "all_five_detected_returns": [v.encode() for v in values],
            "within_each_saved_interval": accepted,
            "meaning": "Attains the sharp two-setting floor; other measured settings reject these efficiencies.",
        },
    }


def main():
    profiles = amplitude_profiles()
    intervals = observed_bounds()
    weights = {"ordinary": ONE, "alternate": ZERO, "count": ZERO}
    # Constructive five-setting control with a single strictly positive
    # mode-efficiency profile normalized to maximum efficiency one.
    additives = {(-6, 1): F(15, 2), (-2, 0): F(77, 100), (-2, 1): F(216, 100), (0, 0): F(1)}
    efficiencies = {
        key: (F(1, 100) + additives.get(key, 0)) / F(751, 100) for key in profiles[0]["count"]
    }
    returns = detect(profiles, weights, efficiencies)
    assert all(all(inside(p, b) for p, b in zip(returns, bounds)) for bounds in intervals.values())
    return {
        "source": {
            "article": "Peng Xue, Hao Qin and Bao Tang, Scientific Reports 4, 4825 (2014)",
            "primary": "https://pmc.ncbi.nlm.nih.gov/articles/PMC4001091/",
            "figure": "https://media.springernature.com/full/springer-static/image/art%3A10.1038%2Fsrep04825/MediaObjects/41598_2014_Article_BFsrep04825_Fig3_HTML.jpg",
            "figure_SHA256": FIGURE_SHA,
            "original_dimensions": [1378, 538],
            "panel": "Fig. 3(b), recurrence inset",
            "phases_deg": [0, 45, 90, 135, 180],
            "vertical_marker_extent_pixels": EXTENTS,
            "pixel_conversion": "(265.5-y)/280, bounds expanded by two pixels at both ends.",
            "printed_135": "0.660 +/- 0.012, authors' reported statistical uncertainty. The printed and "
            "graphic summaries are evaluated as alternate readings of the same experiment.",
        },
        "bounds": {tag: [[str(lo), str(hi)] for lo, hi in values] for tag, values in intervals.items()},
        "inputs": "Every model is a normalized probability distribution BEFORE detection. Count propagates "
        "classical path multiplicities. Alternate and ordinary are the two fixed-label signed eighth-root "
        "evaluations in check_optical_walk_records.phase_sweep. The 22 listed site/polarization pairs "
        "include two unreachable outer-edge modes. Pure count has return 63/256 under equal efficiency "
        "and a setting-independent detected return under any common fixed efficiencies.",
        "proof": "Write h_j=1 at the centre, zero elsewhere. For fixed efficiencies e_j>=0, positive "
        "total collected mass at both settings, and component probabilities P_sj, the upper bound "
        "at 0 deg gives sum e_j(h_j-U)P_0j<=0 and the lower bound at 135 deg gives "
        "sum e_j(L-h_j)P_135j<=0. Their positive combination defines D_j=lambda(h_j-U)P_0j "
        "+(L-h_j)P_135j with lambda=L/(4U). Exact signs below show that at w=0 all coefficients "
        "are nonnegative with both count and alternate strictly positive on both central modes. "
        "The positive observed central rate makes exclusion strict. This w=0 argument also works "
        "with component-specific fixed efficiencies, since each component's coefficients are tested "
        "separately. Under component-INDEPENDENT common mode efficiencies put w=raw ordinary fraction. "
        "At each mode the worst other coefficient is m=min(D_count,D_alt). If D_ord<0 the first "
        "possible zero of w D_ord+(1-w)m is m/(m-D_ord); other modes need no threshold. The "
        "minimum of those ratios occurs at the centre. For w below that floor all modes are "
        "nonnegative, both central modes strictly positive, contradicting the two inequalities.",
        "certificates": {tag: certificate(profiles, values) for tag, values in intervals.items()},
        "ordinary_only_common_efficiency_witness": {
            "efficiencies": {str(k): str(v) for k, v in efficiencies.items()},
            "predicted_returns": [v.encode() for v in returns],
            "all_five_inside_both_versions": True,
            "interpretation": "Illustrative strictly positive fitted efficiency pattern, not instrument calibration.",
        },
        "limits": "The floor is sharp for two graphic inequalities and conservative for the five settings "
        "together. Exact signs concern specified graphic extents and the alternative printed tolerance, "
        "not simultaneous confidence bounds or raw-count hypotheses. With independent efficiencies "
        "per component raw positive weight may be arbitrarily small, e.g. attenuate all other "
        "components while maintaining the ordinary-only detected profile. Changes in efficiencies "
        "with plate setting, additional modes, incoherence, offsets, or background require other models.",
        "exact_field": "Each record {a,b,decimal} means a+b sqrt(2); signs and all comparisons use "
        "rational arithmetic, including signs of opposite terms checked by squaring.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    data = main()
    args.directory.mkdir(parents=True, exist_ok=True)
    (args.directory / "optical_loss_witness.json").write_text(
        json.dumps(data, indent=2) + "\n", encoding="utf8"
    )
    print(
        {
            name: v["sharp_two_setting_ordinary_floor"]["decimal"]
            for name, v in data["certificates"].items()
        }
    )
