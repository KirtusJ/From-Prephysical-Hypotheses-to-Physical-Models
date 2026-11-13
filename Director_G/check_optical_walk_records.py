"""Compare a local fourth-power readout to two published balanced optical walks."""

import argparse
import hashlib
import json
import math
from fractions import Fraction as F
from pathlib import Path


# Sum of the four vertical edge lengths of each bar in fig2.pdf, in
# twelfths of one PDF point. These are drawing coordinates, never counts.
# Within each depth the positions run from -t to +t by twos.
BAR_EDGES = {
    "measured": [
        [10620, 10866], [5412, 10710, 5362], [2702, 8420, 7728, 2634],
        [1317, 7794, 3568, 7562, 1244], [728, 6980, 3402, 2492, 7240, 643],
        [348, 6930, 3710, 1990, 3176, 5142, 189],
    ],
    "theory": [
        [10742, 10744], [5370, 10742, 5372], [2686, 8056, 8058, 2686],
        [1343, 8057, 2684, 8058, 1344], [672, 7386, 2686, 2684, 7386, 671],
        [336, 6043, 3020, 2686, 3020, 6042, 335],
    ],
}
FIGURE_SHA = "b5c9e17b1e83ff9de18a3f220273c5872337eee08332d028d9ed8d15b8350eac"


def check_figure(path):
    """Optional readback of the pinned author source figure using PyMuPDF."""
    import pymupdf

    assert hashlib.sha256(path.read_bytes()).hexdigest() == FIGURE_SHA
    styles = {"[] 0": "theory", "[ .5 4 6 4 ] 0": "measured"}
    corners = [(0, 0), (12.083, 7.02), (19.083, -6.33), (31.166, .69)]
    footpoints = []
    for t in range(1, 7):
        for x in range(-t, t + 1, 2):
            for index, (dx, dy) in enumerate(corners):
                # Two oblique axes in panel (a). The left corner of the
                # first bar at t=6 is the reference in PDF-page coordinates.
                bx = 160.70 + 18.585 * (t - 6) + 29.375 * (x + 6) + dx
                by = 453.62 + 10.82 * (t - 6) - 9.75 * (x + 6) + dy
                footpoints.append((bx, by, t, x, index))
    heights = {}
    with pymupdf.open(path) as pdf:
        for drawing in pdf[0].get_drawings():
            style = styles.get(drawing.get("dashes"))
            if style is None or drawing["rect"].x1 > 566:
                continue
            for kind, *points in drawing["items"]:
                if kind != "l":
                    continue
                start, end = points
                length = abs(end.y - start.y)
                if abs(end.x - start.x) > .003 or length < .12:
                    continue
                distances = [(abs(start.x - bx) + abs(max(start.y, end.y) - by), t, x, i)
                             for bx, by, t, x, i in footpoints]
                distance, t, x, i = min(distances)
                if distance < 1:  # Drawing feet within one point; distinct feet further apart.
                    value = round(length * 12)
                    key = style, t, x, i
                    assert heights.setdefault(key, value) == value
    assert len(heights) == 2 * 27 * 4
    for style, rows in BAR_EDGES.items():
        for t, row in enumerate(rows, 1):
            for x, expected in zip(range(-t, t + 1, 2), row, strict=True):
                samples = [heights[style, t, x, i] for i in range(4)]
                assert max(samples) - min(samples) <= 1
                assert sum(samples) == expected, (style, t, x, samples, expected)


def tv(a, b):
    return sum(abs(x - y) for x, y in zip(a, b, strict=True)) / 2


def normalized(row):
    return [F(v, sum(row)) for v in row]


def walk(steps, power, handedness=1):
    # Gaussian integer coordinates. The omitted common amplitude factor is
    # 1/sqrt(2**(t+1)) at depth t. Mass is read only at the end of each launch.
    modes = {(0, 0): (1, 0), (0, 1): (0, handedness)}
    mass = {(0, 0): F(1, 2), (0, 1): F(1, 2)}
    for t in range(1, steps + 1):
        next_modes, next_mass = {}, {}
        for x in range(1 - t, t, 2):
            h, v = [modes.get((x, c), (0, 0)) for c in (0, 1)]
            m = sum(mass.get((x, c), 0) for c in (0, 1))
            outputs = [(h[0] + sign * v[0], h[1] + sign * v[1]) for sign in (1, -1)]
            weights = [(a*a + b*b)**(power // 2) for a, b in outputs]
            assert sum(weights) > 0 or m == 0
            for c, z in enumerate(outputs):
                dest = x + 2*c - 1, c
                next_modes[dest] = z
                next_mass[dest] = m * F(weights[c], sum(weights)) if sum(weights) else F(0)
        modes, mass = next_modes, next_mass
        coords = [(x, c) for x in range(-t, t + 1, 2) for c in (0, 1)]
        joint = [mass.get(key, F(0)) for key in coords]
        assert sum(joint) == 1
        if power == 2:
            exact = [F(sum(n*n for n in modes.get(key, (0, 0))), 2**(t+1)) for key in coords]
            assert joint == exact
        yield joint, [joint[i] + joint[i+1] for i in range(0, len(joint), 2)]


def phase_sweep():
    """Enumerate every ten-tick signed path in Z[z]/(z^4+1), with z=exp(i*pi/4)."""
    rows = []
    for setting in range(5):
        modes = {}
        for path in range(2**10):
            for initial in (0, 1):
                # Circular launch weights are 1 and -i=z^6. Every branch
                # has the same eleven factors of 1/sqrt(2).
                x, coin, exponent = 0, initial, 6*initial
                for t in range(10):
                    dest = (path >> t) & 1
                    exponent += setting * (x == 0) + 4 * (coin == dest == 1)
                    x += 2*dest - 1
                    coin = dest
                period, j = divmod(exponent % 8, 4)
                cell = modes.setdefault((x, coin), [0]*4)
                cell[j] += (-1)**period
        squared, resolved = {}, {}
        for (x, coin), coeffs in modes.items():
            poly = [0]*4
            for j, a in enumerate(coeffs):
                for k, b in enumerate(coeffs):
                    period, r = divmod((j-k) % 8, 4)
                    poly[r] += a*b*(-1)**period
            assert poly[2] == 0 and poly[3] == -poly[1]
            resolved[f"{x},{coin}"] = poly[:2]
            squared[x] = [u+v for u,v in zip(squared.get(x,[0]*4),poly)]
        assert all(c[2] == 0 and c[3] == -c[1] for c in squared.values())
        assert [sum(c[i] for c in squared.values()) for i in range(4)] == [2048,0,0,0]
        a, b = squared[0][:2]
        # z-z^3 = sqrt(2); its automorphic images are +/-sqrt(2).
        rows.append(dict(degrees=45*setting, rational=str(F(a,2048)),
                         sqrt2_coefficient=str(F(b,2048)),
                         position_coefficients={str(x):[c[0],c[1]] for x,c in sorted(squared.items())},
                         mode_coefficients=resolved,
                         fixed_label_return_by_embedding={
                             str(k):(a + sign*b*math.sqrt(2))/2048
                             for k, sign in ((1,1), (3,-1), (5,-1), (7,1))}))
    return rows


def phase_odds(rows, by_polarization=False):
    # At fixed depth the nuisance efficiencies cancel at the origin.
    # Off-origin the odds ratio is a convex combination of the sitewise
    # ratios, with weights proportional to efficiency times P_135(site).
    ranges = {}
    for k, sign in ((1, 1), (3, -1), (5, -1), (7, 1)):
        field = "mode_coefficients" if by_polarization else "position_coefficients"
        profiles = [{x:(a + sign*b*math.sqrt(2))/2048 for x, (a,b) in row[field].items()}
                    for row in rows[3:]]
        p, q = profiles
        centre = "0,0" if by_polarization else "0"
        if by_polarization:
            assert p[centre] == p["0,1"] and q[centre] == q["0,1"]
        else:
            assert {x for x in q if q[x] == 0} == {"-4", "4"}
        assert all(px > 0 or q[x] == 0 for x,px in p.items())
        ratios = {x:(p[centre]*q[x])/(q[centre]*px) for x,px in p.items()
                  if x.split(",")[0] != "0" and px > 0}
        ranges[str(k)] = dict(ratios=ratios, lower=min(ratios.values()), upper=max(ratios.values()))
    return ranges


def figure_odds():
    # Fig. 3(b) inset, y downwards. Axis at y=265.5 gives zero and
    # y=41.5 gives 0.8. Include both sides of each red marker/cap.
    def odds(pixel):
        p = (F(531,2) - pixel) / 280
        return p / (1-p)

    centre = odds(F(82+91,2)) / odds(F(86+95,2))
    low = odds(91+2) / odds(86-2)
    high = odds(82-2) / odds(95+2)
    assert centre == F(537,505) and low < centre < high
    return dict(centres=str(centre), expanded_graphic_extent=[float(low),float(high)],
                scope="Both full symbol extents expanded by two pixels. Graphic sensitivity only.")


def run():
    square, quartic = [list(walk(18, p)) for p in (2, 4)]
    assert all(list(walk(18, p, -1)) == result for p, result in ((2, square), (4, quartic)))
    rows = []
    for i, (heights, solid) in enumerate(zip(BAR_EDGES["measured"], BAR_EDGES["theory"], strict=True)):
        t, b, q = i + 1, square[i][1], quartic[i][1]
        e = normalized(heights)
        # Each bar is drawn from rounded endpoints on a 1/12-point grid.
        # Allow one grid unit in each vertical length, i.e. four in its sum.
        # Normalizing a vector with total coordinate error <= delta changes
        # TV by at most delta / plotted total (triangle inequality).
        eps = F(4 * len(heights), sum(heights))
        assert tv(normalized(solid), b) < F(4 * len(solid), sum(solid))
        rows.append(dict(step=t, positions=list(range(-t, t+1, 2)), square=list(map(str, b)),
                         local_quartic=list(map(str, q)), observed_edge_sum=heights,
                         theoretical_edge_sum=solid, observed_figure=list(map(float, e)),
                         model_tv_exact=str(tv(b, q)), figure_tv_square=float(tv(e, b)),
                         figure_tv_quartic=float(tv(e, q)), figure_precision_tv_bound=float(eps),
                         needed_efficiency_contrast={
                             name:float(max(v / p for v, p in zip(e, law)) /
                                        min(v / p for v, p in zip(e, law)))
                             for name, law in (("square", b), ("quartic", q))}))
    distance = sum(F(row["model_tv_exact"]) for row in rows) / 6
    radius = F(63, 2000)
    assert distance == F(14855, 159198) and distance > 2 * radius
    means = {k:sum(row[k] for row in rows) / 6
             for k in ("figure_tv_square", "figure_tv_quartic", "figure_precision_tv_bound")}

    # Site 0 relative to +2, at depth 4 divided by depth 2. Under a common
    # efficiency per signed position both odds acquire the same factor.
    def cross_ratio(rows_at_2_and_4):
        r2, r4 = rows_at_2_and_4
        return (r4[2] / r4[3]) / (r2[1] / r2[2])

    odds = {name:float(cross_ratio([law[1][1], law[3][1]]))
            for name, law in (("square", square), ("quartic", quartic))}
    odds["figure"] = float(cross_ratio([normalized(BAR_EDGES["measured"][i]) for i in (1, 3)]))
    fidelity = {}
    for index, measure in enumerate(("joint", "position")):
        b, q = square[-1][index], quartic[-1][index]
        fid = math.fsum(math.sqrt(float(x * y)) for x, y in zip(b, q))**2
        radius18 = math.sqrt(.03)
        d = tv(b, q)
        fidelity[measure] = dict(square=list(map(str,b)), local_quartic=list(map(str,q)),
                                 model_tv=float(d), model_affinity_squared=fid,
                                 observed_square_tv_upper=radius18,
                                 observed_quartic_tv_lower=float(d) - radius18)
        assert float(d) > 2*radius18
    phases = phase_sweep()
    return dict(xue_fixed_phase_labels=dict(source="https://pmc.ncbi.nlm.nih.gov/articles/PMC4001091/",
                                            setting="Fig. 3(b), ten steps, same field automorphism on plate and launch",
                                            observations="Use the printed recurrence 0.660 +/- 0.012 at 135 degrees. The other phase-sweep markers and the 135-degree drawing are retained in phase_defect_data.json.",
                                            position_coefficient_basis="(a+b sqrt(2))/2048, nominal k=1",
                                            centre_odds_135_over_180_common_efficiencies=phase_odds(phases),
                                            centre_odds_135_over_180_common_mode_efficiencies=phase_odds(phases, True),
                                            centre_odds_135_over_180_figure=figure_odds(),
                                            rows=phases),
                broome=dict(source="https://arxiv.org/abs/1002.4923v2", figure="fig2.pdf, panel (a)",
                            figure_sha256=FIGURE_SHA, data_kind="Normalized heights in the author graphic; integer edge lengths are not photon counts.",
                            mean_reported=.031, mean_model_tv=str(distance),
                            rounded_radius_upper=float(radius), empirical_quartic_lower=float(distance-radius),
                            means_from_drawing=means, rows=rows, same_signed_position_odds_ratio=odds),
                fenwick=dict(source="https://arxiv.org/html/2404.02238v1", measure="Fig. 3 and Eq. (6), two single-bin circular inputs at step 18",
                             source_fidelity_floor=.97, signal_mean_photons_per_pulse=.8,
                             time_bin_map="j=(t+x)/2. H stays and V advances.", **fidelity))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_directory", type=Path)
    parser.add_argument("--figure", type=Path, help="verify the transcription against Broome's original fig2.pdf")
    args = parser.parse_args()
    if args.figure:
        check_figure(args.figure)
    data = run()
    args.output_directory.mkdir(parents=True, exist_ok=True)
    dest = args.output_directory / "optical_walk_records.json"
    dest.write_bytes((json.dumps(data, indent=2) + "\n").encode())
    print(dest, hashlib.sha256(dest.read_bytes()).hexdigest())
