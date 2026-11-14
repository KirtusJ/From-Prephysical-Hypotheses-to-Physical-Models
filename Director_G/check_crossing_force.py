"""Check force readouts on binned trajectories and propagate four finite walk words."""
import argparse
import json
from fractions import Fraction as Q
from math import floor, pi, sqrt
from pathlib import Path

import numpy as np

from check_position_records import mass, prepare, step


def require(condition, message):
    if not condition:
        raise ValueError(message)


def slope_change(times, positions):
    a, b, c, d = positions
    return (d-c)/(times[3]-times[2]) - (b-a)/(times[1]-times[0])


def exact_examples():
    rows = []
    for h in (Q(1,4), Q(1,16), Q(1,64), Q(1,256)):
        times = [-2*h, -h, h, 2*h]
        through = [-s-s*s/2 for s in times]
        ordered = list(map(abs, through))
        v1, v2 = slope_change(times, through), slope_change(times, ordered)
        require((v1, v2) == (-3*h, 2), "crossing impulse")
        e = h*h
        noise = [e, -e, -e, e]
        require(slope_change(times, noise) == 4*e/h, "sharp position-error coefficient")
        # Fixed-phase rounding can hide all adjacent accelerations over specific triples.
        ticks = [-h, 0, h]
        rounded = [h * floor((t*t/2)/h + Q(1,2)) for t in ticks]
        require(rounded == [0, 0, 0], "same-bin curvature control")
        rows.append(dict(h=h, through=v1, ordered=v2, attained_error=4*e/h,
                         rounded_positions=rounded, true_acceleration=1))
    return rows


def finite_panel(order):
    delta = (pi/order)**0.25
    blocks = 2*round(delta**(-2.5)/2)
    clock = delta**3
    switch = round(0.75/clock)
    tau = switch*clock
    crossing = (2+sqrt(2))*tau
    times = [round((crossing+s)/clock) for s in (-0.6,-0.3,0.3,0.6)]
    attained = [n*clock for n in times]
    radius = 2*blocks+times[-1]+2
    x = np.arange(-radius, radius+1)
    phase = np.exp(-1j*pi/order*x)
    state, success = prepare(len(x), x, blocks, phase)
    width, offset = 0.5, 0.125
    labels = np.floor((x*delta**2-offset)/width).astype(int)
    totals = {"through": 0.0, "ordered": 0.0}
    rows = []
    for sign in (1, -1):
        for kind in totals:
            branch = state.copy()
            previous = 0
            centers, word, target = [], [], []
            for tick, time in zip(times, attained):
                for n in range(previous,tick):
                    branch = step(branch, phase if n < switch else phase.conj())
                ray = time*time/2 - max(0.,time-tau)**2
                y = sign * (ray if kind == "through" else abs(ray))
                slot = floor((y-offset)/width)
                branch *= (labels == slot)[:, None]
                target.append(y)
                word.append(slot)
                centers.append(offset+width*(slot+0.5))
                previous = tick
            prob = mass(branch)
            totals[kind] += prob
            rows.append(dict(kind=kind, sign=sign, word=word, conditional_mass=prob,
                             joint_mass=prob*success, model_impulse=slope_change(attained,target),
                             binned_impulse=slope_change(attained,centers)))
    require(len({tuple(row["word"]) for row in rows}) == 4, "overlapping words")
    other = 1-sum(totals.values())
    require(0 <= other <= 1, "invalid complementary probability")
    return dict(order=order, ticks=times, times=attained, width=width, offset=offset,
                switch_tick=switch, crossing=crossing, preparation_blocks=blocks,
                preparation_probability=success, named_words=rows, totals=totals,
                other_words_conditional_mass=other)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    dest = parser.parse_args().output
    result = dict(exact_controls=exact_examples(), finite_flights=[
        finite_panel(order) for order in (127,509,2039,8191)])
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("x", encoding="utf8", newline="\n") as stream:
        json.dump(result, stream, default=str, indent=2, allow_nan=False)
        stream.write("\n")


if __name__ == "__main__":
    main()
