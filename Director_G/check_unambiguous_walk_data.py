"""Compare Bian et al.'s published heralded-photon readouts, including every Table I row.

Run python -B check_unambiguous_walk_data.py results. The reference table is embedded.
Optional --verify-source rechecks the authors' public TeX archive using curl.
"""

import argparse
import hashlib
import io
import json
import math
import re
import subprocess
import tarfile
from pathlib import Path

PHI = [45, 54, 63, 72, 81, 90]
HWP = [12.23, 15.32, 18.9, 23.3, 29.33, 45]
# Integers times 10^-4. The final two columns are the authors' additional
# distance-to-theory statistic and uncertainty, not independent new observations.
TABLE = [
    (1, 7139, 30, 171, 46),
    (1, 5963, 38, 184, 47),
    (1, 4638, 45, 192, 47),
    (1, 3166, 54, 127, 46),
    (1, 1616, 62, 66, 44),
    (1, 60, 70, 60, 35),
    (-1, 7125, 31, 152, 45),
    (-1, 5934, 39, 156, 47),
    (-1, 4635, 45, 183, 46),
    (-1, 3146, 55, 136, 49),
    (-1, 1606, 63, 71, 43),
    (-1, 80, 71, 80, 36),
]
ROOT = "https://arxiv.org"
SOURCE = {
    "paper": "Z. Bian et al., Physical Review Letters 114, 203602 (2015)",
    "doi": "https://doi.org/10.1103/PhysRevLett.114.203602",
    "supplement": ROOT + "/pdf/1501.05540v1#page=5",
    "tex_archive": ROOT + "/e-print/1501.05540v1",
    "member": "comb.tex",
    "member_sha256": "662615a530339c727cda5c42cd1657bd45d7e25f8a1b8ea3f34e7631d63322e9",
    "archive_sha256": "000e29893522740edebbd9679be45b30b849ce7c702abdd372f0c219a2e2c6b8",
    "figure_member": "figure2.pdf",
    "figure_sha256": "1718aab957b01b0a0c97ffda6fb02b4e5dab29b7fd60904665474d2f4505c275",
    "locator": "Supplementary material, Table I; main text Fig. 2(d), paragraph giving P(1) and P(-1).",
}


def verify_source():
    archive = subprocess.check_output(["curl", "-fsSL", SOURCE["tex_archive"]])
    assert hashlib.sha256(archive).hexdigest() == SOURCE["archive_sha256"]
    with tarfile.open(fileobj=io.BytesIO(archive)) as source:
        content = source.extractfile(SOURCE["member"]).read()
        figure = source.extractfile(SOURCE["figure_member"]).read()
    assert hashlib.sha256(figure).hexdigest() == SOURCE["figure_sha256"]
    assert hashlib.sha256(content).hexdigest() == SOURCE["member_sha256"]
    lines = [
        line
        for line in content.decode("latin1").splitlines()
        if "&" in line and r"\ket{\phi^" in line and re.search(r"0\.\d{4}\(\d+\)", line)
    ]
    assert len(lines) == 12
    for i, (line, row) in enumerate(zip(lines, TABLE)):
        angles = list(map(float, re.findall(r"\$([0-9.]+)\^o\$", line)))
        assert angles == [PHI[i % 6], 45, HWP[i % 6], 22.5]
        values = [int(n) for match in re.findall(r"0\.(\d{4})\((\d+)\)", line) for n in match]
        assert values == list(row[1:]) and (r"\ket{\phi^+}" in line) == (row[0] == 1)
    assert rb"P(1)=0.0854\pm0.0015" in content and rb"P(-1)=0.0850\pm0.0015" in content
    assert rb"0.0070\pm0.0060" in content


def cosine_share(angle):
    if angle % 180 == 90:
        return 0.0
    return math.cos(math.radians(angle)) ** 2


def share(p, exponent):
    if exponent == 2:
        return p
    return p**2 / (p**2 + (1 - p) ** 2)


def output_mass(phi, theta, prep, gate, alpha_offset=0, theta_offset=0, horizontal=False):
    # The registered x=3 has one path: initial H takes the + arm; its
    # single occupied coin at x=1 keeps H; the final identity shifts to x=3.
    alpha = 1.0 if horizontal else share(cosine_share(phi / 2 + alpha_offset), prep)
    return alpha * share(cosine_share(2 * (theta + theta_offset)), gate)


def propagated_read(phi, theta, sign, prep, gate, horizontal=False):
    # Independent explicit propagation of Jones amplitudes and local masses.
    angle = 0 if horizontal else math.radians(phi / 2) * sign
    amplitudes = {(0, 0): math.cos(angle), (0, 1): math.sin(angle)}
    h = share(math.cos(angle) ** 2, prep)
    mass = {(0, 0): h, (0, 1): 1 - h}
    for coins in ({}, {-1: 45, 1: theta}, {0: 22.5}):
        new_amp, new_mass = {}, {}
        for x in {x for x, d in amplitudes}:
            a, b = (amplitudes.get((x, d), 0) for d in (0, 1))
            if x in coins:
                rad = math.radians(2 * coins[x])
                u, v = math.cos(rad) * a + math.sin(rad) * b, math.sin(rad) * a - math.cos(rad) * b
                incoming = mass.get((x, 0), 0) + mass.get((x, 1), 0)
                total = abs(u) ** gate + abs(v) ** gate
                weights = [incoming * abs(z) ** gate / total if total else 0 for z in (u, v)]
            else:
                u, v = a, b
                weights = [mass.get((x, d), 0) for d in (0, 1)]
            for d, z in enumerate((u, v)):
                target = (x + (1 if d == 0 else -1), d)
                new_amp[target], new_mass[target] = z, weights[d]
        amplitudes, mass = new_amp, new_mass
        assert (
            abs(sum(mass.values()) - 1) < 1e-12
            and abs(sum(z * z for z in amplitudes.values()) - 1) < 1e-12
        )
    return {x: sum(mass.get((x, d), 0.0) for d in (0, 1)) for x in (-3, -1, 1, 3)}


def odds_adjust(p, ratio):
    return ratio * p / (1 - p + ratio * p)


def fit_ratio(pred, rows):
    # One common efficiency ratio for x=3 relative to the two conclusive
    # ports treated together. Descriptive unweighted least squares, no shot model.
    def error(log_r):
        return sum(
            (odds_adjust(p, math.exp(log_r)) - r["measured_probability"]) ** 2
            for p, r in zip(pred, rows)
        )

    a, b = -5.0, 5.0
    for _ in range(90):
        c, d = (2 * a + b) / 3, (a + 2 * b) / 3
        if error(c) < error(d):
            b = d
        else:
            a = c
    ratio = math.exp((a + b) / 2)
    return {
        "efficiency_ratio": ratio,
        "rmse": math.sqrt(error(math.log(ratio)) / len(rows)),
        "residuals": [r["measured_probability"] - odds_adjust(p, ratio) for p, r in zip(pred, rows)],
    }


def score(pred, rows):
    errors = [r["measured_probability"] - p for p, r in zip(pred, rows)]
    # Inverting the monotone odds map gives an interval of efficiency ratios
    # for each row analytically. This checks every common ratio, even those
    # outside the illustrative 0.8..1.2 stress range.
    efficiency_intervals = []
    for i, (p, r) in enumerate(zip(pred, rows)):
        y = r["measured_probability"]
        tol = 3 * r["reported_statistical_error"]
        lo, hi = max(0, y - tol), min(1, y + tol)
        if p == 0:
            assert lo == 0
            continue
        assert 0 < p < 1 and hi < 1
        efficiency_intervals.append((lo / (1 - lo) * (1 - p) / p, hi / (1 - hi) * (1 - p) / p, i + 1))
    low = max(efficiency_intervals, key=lambda z: z[0])
    high = min(efficiency_intervals, key=lambda z: z[1])
    return {
        "mean_absolute_error": sum(map(abs, errors)) / len(rows),
        "rmse": math.sqrt(sum(e * e for e in errors) / len(rows)),
        "residuals": errors,
        "standardized_residuals": [e / r["reported_statistical_error"] for e, r in zip(errors, rows)],
        "largest_absolute_error_row": 1 + max(range(len(rows)), key=lambda j: abs(errors[j])),
        "fitted_relative_detector_efficiency": fit_ratio(pred, rows),
        "common_efficiency_feasibility_at_nominal_angles": {
            "allowance": "Three individual published statistical errors per row; a descriptive tolerance.",
            "required_lower_bound": low[0],
            "limiting_lower_row": low[2],
            "required_upper_bound": high[1],
            "limiting_upper_row": high[2],
            "all_rows_feasible": low[0] <= high[1],
            "all_nontrivial_rows_lower_upper_row": efficiency_intervals,
        },
    }


def main():
    rows = []
    models = {
        "squared": (2, 2),
        "quartic_preparation_and_local_plates": (4, 4),
        "squared_preparation_quartic_walk_plate": (2, 4),
    }
    for i, (sign, p, err, d, de) in enumerate(TABLE):
        j = i % 6
        phi, theta = PHI[j], HWP[j]
        row = {
            "phi_deg": phi,
            "input_sign": sign,
            "preparation_HWP_deg": sign * phi / 4,
            "HWP_minus1_tick2_deg": 45,
            "HWP_plus1_tick2_deg": theta,
            "HWP_zero_tick3_deg": 22.5,
            "measured_probability": p / 10000,
            "reported_statistical_error": err / 10000,
            "authors_distance": d / 10000,
            "authors_distance_statistical_error": de / 10000,
            "ideal_continuous_design_born": math.cos(math.radians(phi)),
        }
        for name, (prep, gate) in models.items():
            value = output_mass(phi, theta, prep, gate)
            ports = propagated_read(phi, theta, sign, prep, gate)
            assert abs(value - ports[3]) < 1e-12 and ports[-3] < 1e-12
            row[name] = value
        rows.append(row)
    summaries = {name: score([r[name] for r in rows], rows) for name in models}
    # Within one half-turn the shares are monotone in both angles. Clip to
    # [0,90] so the extrema are valid even at the nominally dark endpoint.
    # One degree at the physical plate displaces its Jones angle by two degrees.
    for name, (prep, gate) in models.items():
        ranges = []
        for i, r in enumerate(rows):
            phi, theta = PHI[i % 6], HWP[i % 6]
            bounds = [
                share(cosine_share(min(90, max(0, phi / 2 + s * 2))), prep)
                * share(cosine_share(min(90, max(0, 2 * theta + s * 2))), gate)
                for s in (1, -1)
            ]
            assert bounds[0] <= r[name] + 1e-14 and r[name] <= bounds[1] + 1e-14
            rates = [odds_adjust(bounds[0], 0.8), odds_adjust(bounds[1], 1.2)]
            # A separate adversarial 1% contamination can land entirely in
            # either event. These allowances are chosen stress tests.
            interval = [0.99 * rates[0], 0.99 * rates[1] + 0.01]
            y = r["measured_probability"]
            gap = max(interval[0] - y, 0, y - interval[1])
            ranges.append({"lower": interval[0], "upper": interval[1], "minimum_absolute_residual": gap})
        summaries[name]["stress_intervals"] = ranges
        summaries[name]["outside_stress_interval_by_over_three_reported_errors"] = [
            i + 1
            for i, q in enumerate(ranges)
            if q["minimum_absolute_residual"] > 3 * rows[i]["reported_statistical_error"]
        ]
    # The author figure includes both extreme ports and reverses the sign of
    # the bright extreme relative to the shift equations. The union is invariant.
    pure = {
        "phi_deg": 45,
        "input": "H",
        "P_plus1": 0.0854,
        "P_minus1": 0.0850,
        "individual_statistical_errors": [0.0015, 0.0015],
        "inferred_P_abs_x_3": 1 - 0.0854 - 0.0850,
        "maximum_sum_statistical_error_if_sd": 0.003,
        "reported_quantity": "Complement of P(-1)+P(+1) over the four odd final positions. "
        "If the reported errors are standard deviations, the triangle inequality "
        "bounds the union standard deviation by 0.003 without a covariance assumption.",
        "figure_coordinate_discrepancy": "In the pinned author's Figure 2(d), both large bars appear at "
        "x=-3 and x=+3 has a small experimental bar. The shift equations "
        "and narrative put the ideal bright extreme at +3. The absolute-position "
        "union is insensitive to this labeling discrepancy; the complement "
        "is not a measured individual signed-port probability.",
    }
    for label, exponent in (("squared", 2), ("quartic", 4)):
        q = output_mass(45, HWP[0], 2, exponent, horizontal=True)
        ports = propagated_read(45, HWP[0], 1, 2, exponent, horizontal=True)
        assert abs(q - ports[-3] - ports[3]) < 1e-12 and ports[-3] < 1e-12
        pure[label] = q
        pure[label + "_nominal_ports_in_equation_convention"] = ports
        p = pure["inferred_P_abs_x_3"]
        pure[label + "_implied_relative_efficiency"] = p * (1 - q) / (q * (1 - p))
        bounds = [output_mass(45, HWP[0], 2, exponent, theta_offset=s, horizontal=True) for s in (1, -1)]
        pure[label + "_stress_interval"] = [
            0.99 * odds_adjust(bounds[0], 0.8),
            0.99 * odds_adjust(bounds[1], 1.2) + 0.01,
        ]
    for label, (_, gate) in models.items():
        # Assumes the same effective relative efficiency for the extreme
        # event as a whole and the middle pair in both the table and the H run.
        ratio = pure[("squared" if gate == 2 else "quartic") + "_implied_relative_efficiency"]
        residuals = [r["measured_probability"] - odds_adjust(r[label], ratio) for r in rows]
        summaries[label]["pure_H_efficiency_transfer"] = {
            "relative_efficiency": ratio,
            "residuals": residuals,
            "rmse": math.sqrt(sum(e * e for e in residuals) / len(residuals)),
        }
    return {
        "source": SOURCE,
        "rows": rows,
        "model_summaries": summaries,
        "pure_H_control": pure,
        "source_discrepancy": "At plus 90 degrees Table I gives 0.0060(70); the main prose gives 0.0070 +/- 0.0060. "
        "The analysis consistently uses Table I for the 12-row comparison.",
        "authors_distance_definition": "One half the sum of absolute differences between measured and theoretical position "
        "probabilities (total variation). The distance and its error are transcribed; they "
        "use the same records and are not added to the inconclusive-frequency residuals.",
        "data_type": "Measured heralded APD coincidence frequencies normalized over all output positions of the step. "
        "The supplement gives probabilities and statistical uncertainties, not per-port integer counts, "
        "exposure or event records. No raw event total, Poisson likelihood or joint significance is reconstructed.",
        "apparatus": "Type-I down-conversion, heralded polarization preparation, HWPs and birefringent beam-displacer shifts. "
        "The paper reports 0.992 interference visibility per step, 7 ns coincidence window and APD dark rate "
        "below 100/s. These do not determine accidental coincidences or relative collection efficiencies.",
        "model": "Keep the published HWP field matrix. Within each mixing pair, redistribute its incoming mass in "
        "proportion to the output absolute amplitudes to the chosen power; identity propagation carries mass "
        "unchanged. The prepared spinor is cos(phi/2) H +/- sin(phi/2) V, implemented with PBS and HWP. "
        "For x=3 the local shares multiply. Evaluated at the tabulated physical settings with no fitted "
        "parameters for nominal predictions. The fitted odds ratio, odds range 0.8..1.2, independent "
        "+/-1-degree plate errors and <=1% contamination are separate sensitivity examples, not measured bounds.",
        "limits": "The inconclusive arm does not recombine at the third tick. The comparison tests a quartic extension "
        "to the calibrated nonbalanced polarization rotations, including a version using Born-prepared weights. "
        "A rule specified only for balanced Hadamard mixing with no stated response for other angles is "
        "underdetermined here. Interference visibility is not the only possible imperfection. Angle-dependent "
        "detection losses or altered Jones amplitudes could change the comparison.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    parser.add_argument("--verify-source", action="store_true")
    args = parser.parse_args()
    if args.verify_source:
        verify_source()
    data = main()
    args.directory.mkdir(parents=True, exist_ok=True)
    (args.directory / "unambiguous_walk_data.json").write_text(
        json.dumps(data, indent=2, allow_nan=False) + "\n", encoding="utf8"
    )
    print({k: v["rmse"] for k, v in data["model_summaries"].items()})
