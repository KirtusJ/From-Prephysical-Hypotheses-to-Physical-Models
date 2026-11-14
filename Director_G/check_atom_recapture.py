"""Read the pinned public recapture archive as data. Never run the upstream programs."""

import argparse
import ast
import hashlib
import io
import json
from decimal import Decimal as D
from decimal import localcontext
from fractions import Fraction
from pathlib import Path
from urllib.request import urlopen
from zipfile import ZipFile


URL = "https://zenodo.org/api/records/19690318/files/data.zip/content"
ARCHIVE_HASH = "bc5102d783ddef2b33e8957085d23cf1ad11e62a2490603298d7890c72ef8412"
EXPOSURE_HASH = "bc14bc5f7cb4e87303cb817f7f50418b717f35d8d3b9f250b6682aca672bfb23"


def require(test, detail):
    if not test:
        raise ValueError(detail)


def data_lists(content):
    """Extract numeric literals in named assignments, including np.array([...])."""
    result = {}
    for node in ast.parse(content).body:
        if not isinstance(node, ast.Assign) or not isinstance(node.targets[0], ast.Name):
            continue
        expr = node.value
        if isinstance(expr, ast.Call) and isinstance(expr.func, ast.Attribute) and expr.func.attr == "array":
            expr = expr.args[0]
        if isinstance(expr, ast.List) and all(isinstance(v, ast.Constant) for v in expr.elts):
            result[node.targets[0].id] = [D(str(v.value)) for v in expr.elts]
    return result


def g(x):
    return x*x / (x*x + (1-x)**2)


def envelope(m):
    a = 1 / D(2).sqrt()
    k = (1 + D(2).sqrt()) / 2
    lower = g(m) if m <= 1-a else 1-k*(1-m)
    upper = k*m if m <= a else g(m)
    return lower, upper


def fixed(x):
    return format(x, ".10f")


def analyse(raw):
    require(hashlib.sha256(raw).hexdigest() == ARCHIVE_HASH, "archive SHA-256 mismatch")
    with ZipFile(io.BytesIO(raw)) as archive:
        require(archive.testzip() is None, "ZIP integrity")
        members = [e.filename for e in archive.infolist() if not e.is_dir()]
        exposures = archive.read("data/atom_fluorescence.txt")
        arrays = data_lists(archive.read("data/figure_1_c.py").decode("utf-8"))
    require(hashlib.sha256(exposures).hexdigest() == EXPOSURE_HASH, "exposure SHA-256 mismatch")
    counts = [Fraction(v.decode()) for v in exposures.split()]
    require(all(v.denominator == 1 for v in counts), "nonintegral EMCCD counts")
    ordered = sorted(map(int, counts))
    gaps = [(b-a, a, b) for a, b in zip(ordered, ordered[1:])]
    widest, left, right = max(gaps)
    require(sum(span == widest for span, _, _ in gaps) == 1, "nonunique widest gap")
    loaded = sum(x >= right for x in ordered)
    require((len(ordered), left, right, loaded) == (1000, 6851, 8645, 574), "threshold replay")
    require((ordered[0], ordered[-1]) == (4727, 12528), "exposure extremes")
    hist_step = 250
    first_bin = ordered[0] // hist_step * hist_step
    frequencies = [0] * ((ordered[-1] - first_bin) // hist_step + 1)
    for value in ordered:
        frequencies[(value-first_bin) // hist_step] += 1

    simulations = dict(zip(arrays["simulation_N"], arrays["simulation_P"], strict=True))
    inputs = zip(arrays["num_index_45"], arrays["short_duration_ave"], arrays["short_duration_err"],
                 arrays["long_duration_ave"], arrays["long_duration_err"], strict=True)
    rows = []
    with localcontext() as ctx:
        ctx.prec = 50
        for n, short, sd_short, long, sd_long in sorted(inputs):
            m = simulations[n]
            lo, hi = envelope(m)
            spread = max(D(0), lo-short, short-hi)
            rows.append({"pulses": int(n), "mc_short_loss": str(m),
                         "short_loss": str(short), "short_sd": str(sd_short),
                         "long_loss": str(long), "long_sd": str(sd_long),
                         "one_shared_rate_minimax_error": str(abs(long-short)/2),
                         "square_of_one_mass": fixed(g(m)),
                         "square_mixture_lower": fixed(lo), "square_mixture_upper": fixed(hi),
                         "short_distance_to_mixture_interval": fixed(spread)})
        require([r["pulses"] for r in rows if D(r["short_distance_to_mixture_interval"]) > 0]
                == [18], "number of central row mismatches")
        require(max(D(r["one_shared_rate_minimax_error"]) for r in rows) == D("0.38705"),
                "largest pulse contrast")
        for j in range(101):
            m = D(j)/100
            lo, hi = envelope(m)
            require(lo <= g(m) <= hi, "deterministic preparation outside envelope")
            require(abs(lo + envelope(1-m)[1] - 1) <= D("1e-48"), "complement")
        minimum_mean_shift = D(rows[-1]["short_loss"]) * 2 / (1+D(2).sqrt()) - D(rows[-1]["mc_short_loss"])
    return {"source": {"url": URL, "archive_sha256": ARCHIVE_HASH, "archive_bytes": len(raw),
                       "members": members, "fluorescence_member_sha256": EXPOSURE_HASH},
            "loading_calibration": {"exposures": len(ordered), "min": ordered[0], "max": ordered[-1],
                                    "largest_gap_endpoints": [left, right], "loaded": loaded,
                                    "empty": len(ordered)-loaded, "histogram_start": first_bin,
                                    "histogram_step": hist_step, "histogram_counts": frequencies},
            "short_simulation_all_points": {str(k): str(v) for k, v in simulations.items()},
            "figure_1c_comparisons": rows, "last_row_minimum_mean_shift_upward": fixed(minimum_mean_shift)}


def plot(data, output):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, (loading, losses) = plt.subplots(1, 2, figsize=(8.9, 3.4), layout="constrained")
    cal = data["loading_calibration"]
    hist = cal["histogram_counts"]
    step = cal["histogram_step"]
    xs = [cal["histogram_start"] + i*step for i in range(len(hist))]
    loading.bar(xs, hist, width=step, align="edge", color="#365f7b")
    loading.axvspan(*cal["largest_gap_endpoints"], color="#b86613", alpha=.13)
    loading.text(.41,.94,"574 above gap", transform=loading.transAxes, fontsize=9, va="top")
    loading.set(xlabel="EMCCD counts per exposure", ylabel="Exposures per 250-count bin",
                title="Single-atom loading calibration")
    rows = data["figure_1c_comparisons"]
    x = [r["pulses"] for r in rows]
    for val, sd, fmt, label, color in [
        ("long_loss", "long_sd", "s", "5.0 µs pulses", "#ab5433"),
        ("short_loss", "short_sd", "o", "0.4 µs pulses", "#246c83"),
    ]:
        losses.errorbar(x, [float(r[val]) for r in rows], yerr=[float(r[sd]) for r in rows],
                        fmt=fmt, color=color, ms=5, capsize=2, label=label)
    losses.set(xlabel="Trap pulses in the sequence", ylabel="Mean atom loss", ylim=(0,1.06),
               xticks=x, title="One fluorescence read after the sequence")
    losses.legend(frameon=False, loc="center right", fontsize=9)
    for ax in (loading, losses):
        ax.spines[["right", "top"]].set_visible(False)
    fig.savefig(output, dpi=165)
    plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--archive", type=Path, help="local copy of the pinned 11,714-byte data.zip")
    parser.add_argument("--plot", type=Path, help="also render a figure with Matplotlib")
    args = parser.parse_args()
    if args.archive:
        raw = args.archive.read_bytes()
    else:
        with urlopen(URL, timeout=30) as stream:
            raw = stream.read()
    data = analyse(raw)
    with args.output.open("xb") as stream:
        stream.write((json.dumps(data, indent=2) + "\n").encode("utf-8"))
    if args.plot:
        plot(data, args.plot)
