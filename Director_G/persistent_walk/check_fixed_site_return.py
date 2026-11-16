"""Check the reflection argument, the authors' figure, and the two-round gain bounds."""
import json
from argparse import ArgumentParser
from fractions import Fraction as F
from hashlib import sha256
from math import comb
from pathlib import Path
from runpy import run_path

from PIL import Image

figure = run_path(str(Path(__file__).with_name("check_circle_figure.py")))
walk = figure["walk"]
require = walk["require"]
SITES = (5, 7, 9)
ROUNDS = (9, 13)


def mass(state, sites, tick):
    return sum(walk["probability"](a, tick) for site in sites for a in state[site])


def exact_predictions():
    records = {}
    effects_checked = 0
    for n in range(3, 13):
        right, left, phase = [walk["launch"](n, rail) for rail in (0, 1, 0)]
        phase[0] = [(2, 1), (1, -3)]  # Squared input norm is 15.
        for tick in range(25):
            for x in range(n // 2 + 1):
                orbit = sorted({x, (-x) % n})
                # The Gram matrix of both columns, summed over the whole orbit.
                p = mass(right, orbit, tick)
                require(mass(left, orbit, tick) == p, "unequal diagonal entries")
                dot_re = dot_im = 0
                for site in orbit:
                    for (a, b), (c, d) in zip(right[site], left[site]):
                        dot_re += a*c + b*d
                        dot_im += a*d - b*c
                require((dot_re, dot_im) == (0, 0), "off-diagonal effect")
                require(mass(phase, orbit, tick) == 15*p, "complex input replay")
                effects_checked += 1
            if n == 10 and tick == 3:
                require([mass(s, [9], tick) for s in (right, left)] == [F(1,8), F(5,8)],
                        "unpaired position control")
            if n == 10 and tick in ROUNDS:
                # Origin 0 in the recurrence corresponds to the plotted launch m=2.
                target, pair = mass(right, [5], tick), mass(right, [3, 7], tick)
                resolved = walk["probability"](right[5][0], tick)
                require(resolved != walk["probability"](left[5][0], tick),
                        "terminal single-rail control")
                classical = F(sum(comb(tick, k) for k in range(tick + 1)
                                  if (2*k-tick) % n == 5), 2**tick)
                records[tick] = dict(target=target, pair=pair, R_to_R=resolved,
                                     classical_fair_shift=classical)
            right, left, phase = [walk["step"](s, "Hprime") for s in (right, left, phase)]
    require([(r["target"], r["pair"]) for r in records.values()] ==
            [(F(41,64), F(49,256)), (F(941,4096), F(699,2048))], "exact orbit probabilities")
    return effects_checked, records


def read_round(image, read, panel, tick, slack):
    colors = [figure["cell"](image, panel, tick, m) for m in SITES]
    first, target, last = [read(rgb, slack) for rgb in colors]
    pair = (first[0] + last[0], first[1] + last[1])
    return dict(rgb=colors, target_band=target, pair_band=pair)


def relative_gain(record, sample):
    lo, hi = sample["target_band"]
    low_sum, high_sum = sample["pair_band"]
    require(low_sum > 0, "pair gain denominator")
    ratio = record["pair"] / record["target"]
    return (ratio*lo/high_sum, ratio*hi/low_sum)


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("figure_png", type=Path)
    args = parser.parse_args()
    require(sha256(args.figure_png.read_bytes()).hexdigest() == figure["PNG_SHA"], "PNG source")
    count, exact = exact_predictions()
    gains = {}
    samples = {}
    with Image.open(args.figure_png) as image:
        require(image.size == (1003, 2040) and image.mode == "RGB", "source layout")
        read = figure["legend_reader"](image)
        for slack in range(4, 25):
            bounds = []
            for tick in ROUNDS:
                experiment = read_round(image, read, "experiment", tick, slack)
                bounds.append(relative_gain(exact[tick], experiment))
                if slack == 8:
                    numeric = read_round(image, read, "numeric", tick, slack)
                    for name in ("target", "pair"):
                        lo, hi = numeric[name+"_band"]
                        require(lo <= exact[tick][name] <= hi, "numeric plot control")
                    samples[tick] = dict(numeric=numeric, experiment=experiment)
            if slack in (4, 8, 16, 19, 20, 24):
                gains[slack] = bounds
            require((bounds[0][0] > bounds[1][1]) == (slack < 20), "gain interval crossover")
    scale = {t: tuple(q/exact[t]["target"] for q in samples[t]["experiment"]["target_band"])
             for t in ROUNDS}
    require(scale[9][0] > scale[13][1], "constant multiplier control")
    print(json.dumps(dict(cycles=[3,12], rounds=[0,24], orbit_effects_checked=count,
                          exact=exact, png_slack_eight=samples, constant_target_gain=scale,
                          target_to_pair_gain=gains), indent=2, default=str))


if __name__ == "__main__":
    main()
