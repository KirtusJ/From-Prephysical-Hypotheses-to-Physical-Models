"""Render the stopped-position replay's shared exact interval table with Matplotlib."""
import argparse
from fractions import Fraction
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import PercentFormatter


def plot(result, destination):
    panel = result["plot"]
    if panel["provenance"] != "model" or len(panel["series"]) != 3:
        raise ValueError("expected the calculated stopped-position interval panel")
    fair, tilted, rival = [
        [(int(x), float(Fraction(lo)), float(Fraction(hi))) for x, lo, hi in series["data"]]
        for series in panel["series"]
    ]
    p = float(Fraction(result["mass"]))
    fig, (full, zoom) = plt.subplots(1, 2, figsize=(10.6, 4.9), width_ratios=[1, 1.32])
    fig.subplots_adjust(left=.075, right=.98, top=.77, bottom=.22, wspace=.31)
    fig.text(.075, .947, "Reading the first decisions of a 16-step position reference",
             fontsize=16, fontweight="semibold", color="#142633", va="top")
    fig.text(.075, .872, "Calculated hit fractions for the nonnegative half-line, including the origin",
             fontsize=10.5, color="#384b58")
    for ax, start, end in [(full, 0, 16), (zoom, 4, 16)]:
        for series, color, shift, width in [(tilted, "#dc9362", -.14, 3), (fair, "#15677a", .14, 2)]:
            for x, lo, hi in series:
                if start <= x <= end:
                    ax.vlines(x+shift, lo, hi, colors=color, linewidth=width)
                    ax.plot([x+shift, x+shift], [lo, hi], linestyle="none", marker="_",
                            markersize=4, color=color, markeredgewidth=width/1.8)
        points = [(x, lo) for x, lo, _ in rival if start <= x <= end]
        ax.plot(*zip(*points), color="#704773", marker="o", markersize=3.1, linewidth=.85)
        ax.axhline(p, color="#20252a", linestyle=(0, (3, 3)), linewidth=.9)
        ax.set_xlim(start-.55, end+.55)
        ax.set_xlabel("Monitored prefix digits", fontsize=9.5)
        ax.spines[["right","top"]].set_visible(False)
        ax.tick_params(labelsize=9, length=3)
        ax.grid(axis="y", color="#d8e1e4", linewidth=.65)
        ax.set_axisbelow(True)
    full.set_title("All 17 protocols", loc="left", fontsize=11)
    full.set_ylabel("Hit fraction", fontsize=10)
    full.set_xticks(range(0,17,4))
    full.set_ylim(-.015,1.025)
    full.yaxis.set_major_formatter(PercentFormatter(1, decimals=0))
    zoom.set_title("Later decisions, enlarged", loc="left", fontsize=11)
    zoom.set_xticks(range(4,17,2))
    zoom.set_ylim(.729,.83)
    zoom.yaxis.set_major_formatter(PercentFormatter(1, decimals=0))
    handles = [Line2D([],[], color="#15677a", lw=3, label="Fair splits"),
               Line2D([],[], color="#dc9362", lw=3, label="49–51% continuation"),
               Line2D([],[], color="#704773", marker="o", lw=1, ms=4, label="Pooled-square detector"),
               Line2D([],[], color="#20252a", linestyle="--", lw=1, label="Ordinary mass (76.87%)")]
    fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(.51,.027), ncol=4,
               frameon=False, fontsize=9, handlelength=1.7, columnspacing=1.7)
    fig.savefig(destination, dpi=155, facecolor="white", metadata={"Software":"Matplotlib"})
    plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("result", type=Path)
    parser.add_argument("png", type=Path)
    args = parser.parse_args()
    plot(json.loads(args.result.read_bytes()), args.png)
