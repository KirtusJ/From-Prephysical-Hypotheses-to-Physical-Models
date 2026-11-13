"""Feasible normalized mixtures on the five Xue centre-return readings."""

import argparse
import json
import math
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

from check_optical_walk_records import phase_sweep


def chart_bands(observations):
    panel, = (p for p in observations["digitized_secondary"] if p["panel"] == "3b inset")
    zero, low_value, top, top_value = map(lambda v: F(str(v)), panel["y_calibration"])
    scale = (top_value - low_value) / (zero - top)
    return {
        r["phase_degrees"]: (
            float(low_value + scale * (zero - r["symbol_y_extent"][1] - 2)),
            float(low_value + scale * (zero - r["symbol_y_extent"][0] + 2)),
        ) for r in panel["readings"]
    }


def feasible_vertices(rows, intervals):
    # Coordinates are (count fraction, alternative squared fraction);
    # each named row encodes A*c+B*a <= H.
    planes = [
        ("count>=0", -1, 0, 0), ("alternate>=0", 0, -1, 0),
        ("ordinary>=0", 1, 1, 1),
    ]
    for degrees, (lo, hi) in intervals.items():
        ordinary, alternate, count = rows[degrees]
        dc, da = count - ordinary, alternate - ordinary
        planes.extend([(f"{degrees} upper", dc, da, hi - ordinary),
                       (f"{degrees} lower", -dc, -da, ordinary - lo)])

    vertices = []
    for (first, u, v, w), (second, x, y, z) in combinations(planes, 2):
        determinant = u * y - v * x
        if determinant == 0:
            continue
        c = (w * y - v * z) / determinant
        a = (u * z - w * x) / determinant
        # Inputs are rational or single square roots, well inside this many
        # ulps for the point/half-plane operations in the recorded solutions.
        roundoff = 64 * math.ulp(1.)
        if all(A*c + B*a - H <= roundoff for _, A, B, H in planes):
            vertices.append(dict(count=c, alternate=a, ordinary=1-c-a, active=[first, second]))
    return vertices


def run():
    source = Path(__file__).parent / "results" / "phase_defect_data.json"
    observations = json.loads(source.read_bytes())
    chart = chart_bands(observations)
    printed, = (r for r in observations["printed_observations"] if "135 degree" in r["name"]
                and r["metric"] == "recurrence")
    centre, sd = (F(str(printed[name])) for name in ("reported", "reported_statistical_SD"))
    printed_band = float(centre - sd), float(centre + sd)
    count_return = F(math.comb(10, 5), 2**10)
    assert count_return == F(63, 256)
    rows = {
        r["degrees"]: (r["fixed_label_return_by_embedding"]["1"],
                       r["fixed_label_return_by_embedding"]["3"], float(count_return))
        for r in phase_sweep()
    }
    # Independent closed forms and a binomial walk check. There are two input
    # polarizations, each with the same complete counting distribution.
    x = {0: 1}
    for _ in range(10):
        x = {i: x.get(i - 1, 0) + x.get(i + 1, 0) for i in range(min(x) - 1, max(x) + 2, 2)}
    assert F(x[0], sum(x.values())) == count_return
    assert list(rows) == list(chart) == [0, 45, 90, 135, 180]
    expected = [F(9, 128), F(51, 128), F(85, 128), F(43, 128), F(85, 128)]
    for (angle, (ordinary, alternate, _)), baseline in zip(rows.items(), expected, strict=True):
        split = 15 * math.sqrt(2) / 64 if angle == 135 else 0
        assert abs(ordinary - (baseline + split)) < 8 * math.ulp(1.)
        assert abs(alternate - (baseline - split)) < 8 * math.ulp(1.)

    graph = feasible_vertices(rows, chart)
    printed_only = feasible_vertices(rows, {135: printed_band})
    hybrid = feasible_vertices(rows, {**chart, 135: printed_band})
    assert len(graph) == 3 and printed_only and not hybrid
    # Analytic certificate of the empty hybrid, independent of vertex search.
    ordinary90, _, count = rows[90]
    cmin = (ordinary90 - chart[90][1]) / (ordinary90 - count)
    ordinary135 = rows[135][0]
    max135 = (1-cmin) * ordinary135 + cmin * count
    assert 0 < max135 < printed_band[0]
    # All settings see identical counts under a single fixed detector array in
    # the pure counting model. In particular these two bands cannot be attained.
    assert chart[0][1] < chart[135][0]
    lower_ordinary = (printed_band[0] - count) / (ordinary135 - count)
    assert abs(lower_ordinary - min(v["ordinary"] for v in printed_only)) < 8 * math.ulp(1.)
    return dict(
        source=observations["source"]["doi"],
        detection="Identical efficiencies for all terminal modes for the mixture polygons. "
                  "All outcomes enter each conditional detected distribution. The last pure-count "
                  "control allows arbitrary fixed mode efficiencies and requires nonzero counts.",
        model="Two phase embeddings of the fixed named mu8 scalar signed-H apparatus and "
              "the gain-blind history count, with nonnegative common weights summing to one. "
              "The phase-setting changes gains alone. This is not a fit to an unspecified physical lift.",
        count_probability=str(count_return), chart_intervals=chart, printed_interval=printed_band,
        plotted_only_vertices=graph, printed_only_vertices=printed_only,
        printed_only_minimum_ordinary=lower_ordinary, mixed_sources_vertices=hybrid,
        empty_mixed_sources=dict(c_lower_from_90=cmin, maximum_135=max135,
                                 shortfall_at_printed_lower=printed_band[0]-max135),
        count_only_fixed_detection=dict(zero_degree=chart[0], phase_135=chart[135],
                                       disjoint=True, setting_invariant=True),
        scope="Expanded marker extents use two pixels of graphical reading allowance. "
              "The reported one-statistical-SD interval is a separate deterministic sensitivity "
              "range. These are two readings of the same optical experiment, not independent "
              "observations, a common confidence region, or a systematic-error budget.",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    target = parser.parse_args().output
    target.mkdir(parents=True, exist_ok=True)
    (target / "optical_multiset_mixture.json").write_bytes(
        (json.dumps(run(), indent=2, allow_nan=False) + "\n").encode()
    )
