"""Run with Python, NumPy and a fresh output directory. The force scale F is one."""

import argparse
import cmath
import json
import math
from collections import Counter
from fractions import Fraction
from pathlib import Path

import numpy as np

from check_central_window_flight import density, fixed_cf, require, sharp, stream


def settings(order, regime):
    fixed = regime == "fixed_moving_frame"
    delta = (math.pi / order) ** (1 / (3 if fixed else 4))
    pitch = delta if fixed else delta ** 2
    tick = delta ** (2 if fixed else 3)
    t = round(delta ** (-2 if fixed else -9 / 4))
    n = round(.75 / tick)
    v = math.sqrt(delta) if fixed else delta ** (33 / 32)
    halfwidth = 1 / delta if fixed else t * delta ** (17 / 16)
    require(2 * (t + n) < 4 * order, "ring light cone")
    return delta, pitch, tick, t, n, v, halfwidth


def small_word_oracle(t, n, first, last, order, s):
    """Independent signed integer multiplicities, then evaluate once at the physical character."""
    words = Counter({(0, 0, 0): 1})
    source = None
    for step in range(1, t + n + 1):
        after = Counter()
        for (x, rail, gain), weight in words.items():
            g = (gain + x // 2) % order
            after[x + 1, 0, g] += weight
            after[x - 1, 1, g] += weight if rail == 0 else -weight
        if step == t:
            after = Counter({p: a for p, a in after.items() if first <= p[0] <= last})
            source = after
        words = after

    def probabilities(table, clock):
        vals = Counter()
        for (x, rail, g), a in table.items():
            vals[x, rail] += a * cmath.exp(-2j * math.pi * s * g / order)
        masses = Counter()
        for (x, rail), a in vals.items():
            masses[x] += abs(a) ** 2 / 2 ** clock
        return masses

    return sum(probabilities(source, t).values()), probabilities(words, t + n)


def trial(order, regime, s):
    fixed = regime == "fixed_moving_frame"
    delta, pitch, tick, t, n, v, halfwidth = settings(order, regime)
    source_clock, flight_clock = t * tick, n * tick
    center = t * v
    output_center = (t + n) * v if fixed else 0.
    r, l, lo = sharp(t, order, s, 0)
    require(abs(density(r, l).sum() - 1) < 2e-10, "sharp source normalization")
    x = lo + 2 * np.arange(len(r))
    keep = abs(x - center) <= halfwidth
    require(keep.any(), "empty source interval")
    sites = [int(y) for y in x[keep]]
    counts = [math.comb(t, (t+y)//2) for y in sites]
    count_paths = sum(counts)
    count_pass = Fraction(count_paths, 2 ** t)
    count_site_weights = [float(Fraction(val, count_paths)) for val in counts]
    standardized_lower = (center - halfwidth) / math.sqrt(t)
    count_bound = math.exp(-max(standardized_lower, 0.) ** 2 / 2)
    require(float(count_pass) <= count_bound + 2e-14, "count tail bound")

    r, l = r[keep], l[keep]
    passage = float(density(r, l).sum())
    require(0 < passage <= 1, "positive coherent pass")
    er, el, end = stream(r, l, sites[0], n, order, s)
    joint = density(er, el)
    require(abs(joint.sum() - passage) < 2e-10, "unconditional terminal mass")
    y = pitch * (end + 2 * np.arange(len(joint)) - output_center)
    cf_rows = []
    for xi in (0., 1., 3.):
        target = (fixed_cf(xi, s, source_clock, flight_clock, 1.) if fixed
                  else math.cos(s * xi * flight_clock ** 2 / 2))
        actual = complex(np.dot(joint, np.exp(1j * xi * y)) / passage)
        # Future count steps stay independent of the accepted count prefix.
        count_cf = sum(w * cmath.exp(1j * xi * pitch * (pos - output_center))
                       for w, pos in zip(count_site_weights, sites)) * math.cos(xi * pitch) ** n
        cf_rows.append(dict(xi=xi, square=[actual.real, actual.imag], predicted=target,
                            abs_square_error=abs(actual-target),
                            count=[count_cf.real, count_cf.imag]))
    require(abs(complex(*cf_rows[0]["square"]) - 1) < 2e-10 and
            abs(complex(*cf_rows[0]["count"]) - 1) < 2e-12, "conditional zeroth modes")

    control = None
    if order == 127:
        p0, terminal = small_word_oracle(t, n, sites[0], sites[-1], order, s)
        maxerr = max(abs(a - terminal[end+2*j]) for j, a in enumerate(joint))
        require(abs(p0 - passage) < 2e-12 and maxerr < 2e-12, "signed word oracle")
        control = dict(absolute_pass_error=abs(p0-passage),
                       max_joint_site_error=float(maxerr))

    leading = 2 * halfwidth / (math.pi * t)
    return dict(M=order, s=s, regime=regime, delta=delta, t=t, n=n,
                source_time=source_clock, flight_time=flight_clock,
                v=v, lattice_halfwidth=halfwidth, center=center,
                terminal_lattice_origin=output_center, first=sites[0], last=sites[-1],
                occupied_site_count=len(sites), standardized_lower=standardized_lower,
                square_pass=passage, leading_square_pass=leading, square_over_leading=passage/leading,
                exact_count_pass=str(count_pass), count_pass=float(count_pass),
                count_upper_bound=count_bound,
                posterior_count_at_equal_incident_weights=float(count_pass)/(float(count_pass)+passage),
                terminal_cf_given_pass=cf_rows, signed_word_oracle=control)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    dest = parser.parse_args().directory
    rows = []
    for regime in ("shrinking_lab", "fixed_moving_frame"):
        for order in (127, 2048, 8191, 32768, 131071, 524287):
            rows.append(trial(order, regime, 1))
            # Zero-field and distinct folded labels pass the same instrument.
            if order == 2048:
                rows.extend(trial(order, regime, s) for s in (-1, 0, 2))
                plus, minus = rows[-4], rows[-3]
                require(abs(plus["square_pass"] - minus["square_pass"]) < 2e-12,
                        "conjugate passes")
                for a, b in zip(plus["terminal_cf_given_pass"], minus["terminal_cf_given_pass"]):
                    require(abs(complex(*a["square"]) - complex(*b["square"])) < 2e-10,
                            "conjugate position read")
    dest.mkdir(parents=True, exist_ok=True)
    with (dest / "moving_window_flight.json").open("x", encoding="utf8", newline="\n") as handle:
        json.dump(dict(
            scope="One sharp (0,R) launch with field applied at every departure. The window is a "
                  "single coherent binary read. Classical and fixed-action terminal laws use the "
                  "laboratory and translating coordinates, respectively. All rows are model calculations.",
            checks="Unwrapped cone, source and joint terminal mass, exact fair count pass versus "
                   "Chernoff, zero Fourier modes, signed integer word oracle at M=127, conjugate "
                   "unit position law at M=2048. No finite agreement threshold against the limit.",
            rows=rows), handle, indent=2, allow_nan=False)
        handle.write("\n")


if __name__ == "__main__":
    main()
