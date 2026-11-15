"""Replay calibration, grouped mass and Gaussian position controls."""
import argparse
import json
from fractions import Fraction
from math import erf, expm1, log, sqrt
from pathlib import Path


def main(calibration):
    rows = calibration["all_sites"]
    masses = {row["x"]: row["site_numerator"] for row in rows}
    assert [masses[x] for x in (-2, 0, 4)] == [4, 36, 324]
    splits = []
    for k in (2, 4, 8, 16, 32, 64):
        for direction in (-1, 1):
            u = Fraction(direction, k)
            q = 1 + float(u)
            # One group has 2^k cells with 2^(-k) times the single-cell weight.
            ratio = Fraction(2)**(-direction)
            group = ratio / (1+ratio)
            score = 324**q * expm1(-float(u)*log(9))**2 / sum(m**q for m in masses.values())
            raw = sum(w*masses[x]**q for x, w in [(-2, 81), (0, -18), (4, 1)])
            direct = raw / sum(m**q for m in masses.values())
            assert abs(direct-score) < 1e-12
            assert abs(group-Fraction(1, 2)) == Fraction(1, 6)
            splits.append({"k": k, "q": str(1+u), "many_cell_probability": str(group),
                           "log_mass_variance_at_one": (k*log(2))**2/4,
                           "calibration_site_score": score, "k_squared_score": k*k*score})
    gaussian = []
    for variance in (1, 1/16, 1/256):
        for q in (0.5, 0.75, 1, 1.5, 2):
            if q == 1:
                distance = 0
            else:
                crossing = sqrt(variance*log(q)/(q-1))
                # A centered normal puts erf(x/sqrt(2v)) in [-x,x].
                distance = abs(erf(crossing/sqrt(2*variance/q))
                               - erf(crossing/sqrt(2*variance)))
            length_bound = abs(log(q))/(2*sqrt(2))
            assert distance <= length_bound + 1e-14
            gaussian.append({"ordinary_variance": variance, "q": q,
                             "powered_variance": variance/q,
                             "log_density_variance": 1/(2*q*q),
                             "exact_formula_tv": distance, "integrated_bound": length_bound})
    return {"source_masses": masses, "two_groups": splits, "gaussian_controls": gaussian}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    source = Path(__file__).parent / "results/addressed_position_score.json"
    result = main(json.loads(source.read_text(encoding="utf-8")))
    with args.output.open("x", encoding="utf-8", newline="\n") as f:
        json.dump(result, f, indent=2)
        f.write("\n")
