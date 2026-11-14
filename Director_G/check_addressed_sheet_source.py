"""Replay a localized source through the addressed staircase on exact coordinates."""

import argparse
from collections import Counter
import cmath
import json
import math
from pathlib import Path

from check_routed_sheet_filter import build_arm, complement, stream


def require(condition, message):
    if not condition:
        raise ValueError(message)


def trace_gain(word, start, order):
    position = start
    gain = 0
    for next_rail in word:
        gain += position // 2
        position = (position + (1 if next_rail == "R" else -1)) % (4 * order)
    require(position == start, "a route did not return to its splitter")
    return gain % order


def emit(field, home, order, sheet_start, final_stage, stage):
    width = 1 << stage
    # The route generator's first argument sets its size, not the physical
    # ring. Here we only need a gain interval of length width.
    arm = build_arm(width + 1, width)
    reflected = complement(arm)
    upper = trace_gain(arm, home, order)
    lower = trace_gain(reflected, home, order)
    require((upper - lower) % order == width, "physical separation of both sheets")
    field = stream(field, order, "H")
    for previous, current in zip(arm, arm[1:]):
        field = stream(field, order, "I" if previous == current else "X")
    first = (sheet_start + lower) % order
    # Both arms returned to one base site on different rails. Apply a
    # rail permutation controlled only on the current physical sheet site.
    # Its extension to the empty input rail at that sheet site is a bijection.
    joined = {}
    for (site, rail), polynomial in field.items():
        require(site == home, "route is still spatially separated")
        for y, amplitude in polynomial.items():
            offset = (y - first) % order
            high = offset >= width
            require(offset < 2 * width and rail == ("L" if high else "R"),
                    "the physical address selected the wrong rail")
            target_rail = complement(rail) if high else rail
            require(target_rail == "R" and y not in joined, "overlap or incomplete erasure")
            joined[y] = (-1 if high and stage == final_stage else 1) * amplitude
    field = stream({(home, "R"): joined}, order, "I")
    out = (home + 1) % (4 * order)
    origin = (first + home // 2) % order
    require(set(field) == {(out, "R")}, "unexpected output at the next split")
    expected = {((origin + i) % order): (-1 if stage == final_stage and i >= width else 1)
                for i in range(2 * width)}
    require(field[out, "R"] == Counter(expected), "signed sheet amplitudes at the named port")
    require(sum(x * x for x in expected.values()) == 2 * width, "integer norm")
    return field, out, origin, len(arm) + 1


def sample(order, home, initial_y):
    height = order.bit_length() - 1
    length = 1 << height
    field = {(home, "R"): Counter({initial_y: 1})}
    origin, elapsed = initial_y, 0
    for stage in range(height):
        field, home, origin, ticks = emit(field, home, order, origin, height - 1, stage)
        elapsed += ticks
    x = field[home, "R"]
    amplitude = sum(a * cmath.exp(2j * math.pi * y / order) for y, a in x.items())
    target = 2 * abs(amplitude) ** 2 / (order * length)
    analytic = 8 * math.sin(math.pi * length / (2 * order)) ** 4 / (
        order * length * math.sin(math.pi / order) ** 2)
    require(abs(target - analytic) < 2e-13, "Fourier weight disagrees with the geometric sum")
    require(target >= 4 / math.pi ** 2 - 2e-13, "target weight below dimension-free bound")
    require(sum(x.values()) == 0, "constant mode survived the sign pattern")
    # Trace an orthogonal pointer for each final address. Each endpoint
    # has exactly one route word because every split joined disjoint halves.
    pointer_target = sum(2 * value ** 2 for value in x.values()) / (order * length)
    require(pointer_target == 2 / order, "incoherent route control")
    jump_energy = sum((x[y] - x[(y - 1) % order]) ** 2 for y in range(order))
    require(jump_energy == (8 if length == order else 6), "periodic sheet differences")
    # Evaluate the scaled rail contrast in physical coordinates. A
    # three-tick interferometer compares the sheet to its one-site shift.
    shift_overlap = sum(x[y] * x[(y - 1) % order] for y in range(order))
    rail_excess = (length - shift_overlap) / (4 * length)
    scaled_energy = (2 * order ** 2 / math.pi ** 2) * rail_excess
    require(math.isclose(scaled_energy, order ** 2 * jump_energy /
                         (4 * math.pi ** 2 * length), rel_tol=1e-14),
            "rail contrast and cyclic difference energy disagree")
    return dict(order=order, occupied=length, final_port=[home, "R"], final_origin=origin,
                ticks=elapsed, hadamards=height, target_weight=target,
                retained_route_control=pointer_target, jump_energy=jump_energy,
                rail_excess=rail_excess, scaled_energy=scaled_energy)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    directory = parser.parse_args().directory
    rows = []
    seam_checks = 0
    for order in [*range(3, 65), 95, 127, 128, 129, 191, 255, 256, 257, 511, 512]:
        base = sample(order, 0, 0)
        seam = sample(order, 4 * order - 1, order - 1)
        require(abs(base["target_weight"] - seam["target_weight"]) < 2e-13, "seam dependence")
        rows.append(base)
        seam_checks += 1
    directory.mkdir(parents=True, exist_ok=True)
    result = dict(scope="Exact physical sheet and rail values; target weights use binary64.",
                  seam_replays=seam_checks, profiles=rows)
    with (directory / "addressed_sheet_source.json").open("x", encoding="utf8", newline="\n") as f:
        json.dump(result, f, separators=(",", ":"), allow_nan=False)
        f.write("\n")


if __name__ == "__main__":
    main()
