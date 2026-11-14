"""Replay the single-walk preparations that test a folded probability law on a cover."""

import argparse
from collections import Counter
import json
from math import cos, pi
from pathlib import Path

from check_cover_comparison import embed, masks, pad, read


def require(condition, message):
    if not condition:
        raise ValueError(message)


def shifted(census, shift, order):
    return Counter({(sign, (gain + shift) % order): count
                    for (sign, gain), count in census.items()})


def bins(census):
    return [[sign, gain, count] for (sign, gain), count in sorted(census.items())]


def folded(k, order):
    return min(k % order, -k % order)


def cover(coarse, fine):
    require(fine % coarse == 0, "orders must lie on one cover")
    ratio = fine // coarse
    cancelling = Counter([(1, 0), (-1, 0)])
    panels = [("cancel", cancelling)]
    panels += [(lag, Counter([(1, 0), (1, lag)])) for lag in range(coarse // 2 + 1)]
    records = []
    clocks = set()
    for label, lower in panels:
        upper = embed(lower, coarse, fine)
        low_rows = masks(lower, coarse)
        high_rows = masks(upper, fine)
        clock = max(len(low_rows), len(high_rows))
        clocks.add(clock)
        for order, rows, target in ((coarse, low_rows, lower), (fine, high_rows, upper)):
            require(read(rows, order, 0) == target, "absolute residue mismatch")
            extra = clock - len(rows)
            require(extra % 2 == 0, "return-clock parity")
            actual = read(pad(rows, clock, order), order, 0)
            require(actual == shifted(target, -(extra // 2), order), "padding changed relative gains")
        records.append(dict(lag=label, coarse=bins(lower), fine=bins(upper)))
    require(len(clocks) == 1, "two-item probes have different clocks")

    # Exact symbolic comparison. A response at lag l is tagged by the
    # orbit of exp(2 pi i l k/m); the tag uniquely determines its cosine.
    for k in range(fine // 2 + 1):
        restriction = folded(k, coarse)
        for lag in range(coarse // 2 + 1):
            require(folded(ratio * lag * k, fine) == ratio * folded(lag * restriction, coarse),
                    "the fine character did not restrict to the coarse one")

    # Fourier inversion with an independently chosen mixed source, including
    # count and both self-conjugate modes when present. The tolerance below is
    # for this floating check only. The exact inversion is proved in the paper.
    fine_weights = [k + 1 for k in range(fine // 2 + 1)]
    count = 2
    norm = count + sum(fine_weights)
    pushed = [0] * (coarse // 2 + 1)
    for k, mass in enumerate(fine_weights):
        pushed[folded(k, coarse)] += mass
    moments = [sum(w * cos(2 * pi * (k * h % coarse) / coarse)
                   for k, w in enumerate(fine_weights)) / norm for h in range(coarse)]
    recovered = [
        (1 if (2 * s) % coarse == 0 else 2) / coarse
        * sum(c * cos(2 * pi * (s * h % coarse) / coarse) for h, c in enumerate(moments))
        for s in range(len(pushed))
    ]
    require(all(abs(w - target / norm) < 1e-12 for w, target in zip(recovered, pushed)),
            "incorrect inverse or conjugacy factor")
    require(count + sum(pushed) == norm, "loss of mass at a folded frequency")
    return dict(coarse=coarse, fine=fine, clock=clocks.pop(), probes=records,
                mixed_source=dict(count=count, fine=fine_weights, denominator=norm,
                                  restricted_coarse=pushed))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_directory", type=Path)
    destination = parser.parse_args().output_directory
    pairs = [(3, 6), (4, 8), (3, 12), (5, 15), (6, 12), (8, 24), (12, 36)]
    data = dict(scope="Model probabilities on single-walker calibration runs at matched clocks.",
                covers=[cover(m, n) for m, n in pairs])
    destination.mkdir(parents=True, exist_ok=True)
    with (destination / "cover_marginals.json").open("x", encoding="utf8", newline="\n") as out:
        json.dump(data, out, separators=(",", ":"), allow_nan=False)
        out.write("\n")


if __name__ == "__main__":
    main()
