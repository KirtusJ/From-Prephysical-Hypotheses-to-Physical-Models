"""Compute the five sharp-launch panels in Tag_sector_controls.md using exact arithmetic.

Run python -B check_tag_sector_controls.py OUTPUT_DIRECTORY. Existing output is preserved.
"""
import argparse
from fractions import Fraction as F
from itertools import product
import json
from math import prod
from pathlib import Path


# Protocol, read interval and expected witnesses are fixed before either model runs.
LAST_TICK = 4
SETTINGS = {
    "pure_0": (0, 0, 0, False),
    "pure_1": (0, 0, 1, False),
    "overlap_0": (0, 0, 0, True),
    "overlap_1": (0, 0, 1, True),
    "shield": (1, 1, 1, False),
}
MODELS = ("sector", "spectator")
EXPECTED = {
    "sector": (F(0), F(1, 4), F(1, 16), F(1)),
    "spectator": (F(1, 24), F(5, 24), F(1, 16), F(6, 5)),
}


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def masked(tick, site, enabled):
    return int(enabled and tick == 1 and site > 0)


def cells(tick, origin, start):
    depth = tick - start
    return product(range(origin-depth, origin+depth+1), (0, 1), (0, 1))


def words(setting, tick, *, flip_tag_zero=False):
    """Sum the signed words. At tick one the optional sign plate follows the XOR."""
    start, origin, initial_tag, enabled = setting
    tally = {}
    for path in product((0, 1), repeat=tick-start):
        x, tag, rail, sign = origin, initial_tag, 0, 1
        for time, direction in enumerate(path, start+1):
            if rail == direction == 1:
                sign = -sign
            rail = direction
            x += 1-2*rail
            tag ^= masked(time, x, enabled)
            if flip_tag_zero and enabled and time == 1 and tag == 0:
                sign = -sign
        port = x, tag, rail
        tally[port] = tally.get(port, 0) + sign
    return tally


def encode(tick, x, tag, translated):
    # Deliberately change frames at selected sites and times. A real link
    # transports from the old frame at x to the next frame at its endpoint.
    flip = translated and (tick + x//2) % 3 == 1
    return tag ^ int(flip)


def right_fraction(model, u, v, a, b):
    """A custom denominator receives the two squared sector norms."""
    selected = u*u + v*v
    other = a*a + b*b
    if model == "relative_sign":
        denominator = u*u + (v-a)**2 + other
        return F(1, 2) + (F(u*(v-a), denominator) if denominator else 0)
    if model == "cusp":
        total = selected + other
        bias = F(u*v - abs(u*a), total) if total else 0
        return F(1, 2) + min(F(1, 2), max(-F(1, 2), bias))
    if callable(model):
        denominator = model(selected, other)
    elif model == "sector":
        denominator = selected
    elif model == "spectator":
        denominator = selected + other
    elif model == "max_norm":
        denominator = max(selected, other)
    else:
        raise ValueError(f"Unknown model {model}")
    return F(1, 2) + (F(u*v, denominator) if denominator else 0)


def panels(setting, model, translated=False, last_tick=LAST_TICK, *, flip_tag_zero=False):
    start, origin, initial_tag, enabled = setting
    masses = {(origin, encode(start, origin, initial_tag, translated), 0): F(1)}
    records = {}
    for tick in range(start, last_tick+1):
        raw = words(setting, tick, flip_tag_zero=flip_tag_zero)
        signed = {(x, encode(tick, x, b, translated), r): v for (x, b, r), v in raw.items()}
        decoded = {(x, b, r): masses.get((x, encode(tick, x, b, translated), r), F(0))
                   for x, b, r in cells(tick, origin, start)}
        require(sum(decoded.values()) == 1, "marker conservation")
        require(all(m >= 0 for m in decoded.values()), "nonnegative marker")
        if model == "sector":
            require(all(m == F(raw.get(cell, 0)**2, 2**(tick-start))
                        for cell, m in decoded.items()), "signed word oracle")
        records[tick] = raw, decoded
        if tick == last_tick:
            break
        future = {}
        for x, b in product(range(origin-(tick-start), origin+(tick-start)+1), (0, 1)):
            u, v = (signed.get((x, b, r), 0) for r in (0, 1))
            other_u, other_v = (signed.get((x, b^1, r), 0) for r in (0, 1))
            right = right_fraction(model, u, v, other_u, other_v)
            require(0 <= right <= 1, "conditional probability")
            mass = sum(masses.get((x, b, r), F(0)) for r in (0, 1))
            for rail, chance in enumerate((right, 1-right)):
                y = x + 1-2*rail
                old_label = encode(tick, x, b, translated)
                new_label = encode(tick+1, y, old_label ^ masked(tick+1, y, enabled), translated)
                port = y, new_label, rail
                require(port not in future, "unique oriented predecessor")
                future[port] = mass*chance
        masses = future
    return records


def check_finite_calibration():
    setting = SETTINGS["overlap_0"]
    final_tick = 9
    reference = panels(setting, "sector", last_tick=final_tick)
    # Panels ending at tick eight only use splitters at ticks zero through seven.
    fractions = {F(1)}
    for tick in range(8):
        raw, _ = reference[tick]
        for (x, b, rail), u in raw.items():
            v = raw.get((x, b, 1), 0)
            if rail == 0 and u*v:
                selected = u*u + v*v
                other = sum(raw.get((x, b^1, r), 0)**2 for r in (0, 1))
                fractions.add(F(selected, selected + other))

    def polynomial(r):
        return prod((r - a)**2 for a in fractions)

    target = F(37, 38)
    require(len(fractions) == 12 and target not in fractions, "eight-tick calibration set")
    for tick in range(3, 9):
        raw, _ = reference[tick]
        x = tick - 2
        require((raw[x, 1, 0], raw[x, 1, 1]) == (x, 1), "right-first inner edge")
        require((raw[x, 0, 0], raw.get((x, 0, 1), 0)) == (1, 0), "left-first inner edge")

    right_port, left_port = (7, 1, 0), (5, 1, 1)
    _, autonomous = reference[final_tick]
    require((autonomous[right_port], autonomous[left_port]) == (F(49, 512), F(25, 512)),
            "autonomous tick-nine daughters")
    required_curvatures = []
    for multiplier, right, left in ((1, F(43, 512), F(31, 512)),
                                     (3, F(40, 512), F(34, 512))):
        scale = multiplier * target / polynomial(target)

        def denominator(selected, other):
            total = selected + other
            if total == 0:
                return 0
            return selected + total * scale * polynomial(F(selected, total))

        require(denominator(0, 1) > 0, "empty selected sector on the unit sphere")
        analytic = panels(setting, denominator, last_tick=final_tick)
        require(all(analytic[t] == reference[t] for t in range(9)), "entire calibration prefix")
        require(analytic == panels(setting, denominator, True, final_tick), "analytic tag relabel")
        _, output = analytic[final_tick]
        require((output[right_port], output[left_port]) == (right, left),
                "two positive tick-nine daughters")
        flipped = panels(setting, denominator, last_tick=final_tick, flip_tag_zero=True)
        require(all(flipped[t][1] == analytic[t][1] for t in analytic), "sign-even analytic panels")
        local_split = right / (right + left)
        required_curvatures.append(2 * 6**2 * abs(F(49, 74) - local_split))
    require(required_curvatures == [F(216, 37), F(324, 37)], "necessary curvature at tick eight")


def check_sign_control():
    setting = SETTINGS["overlap_0"]
    for name in ("pure_0", "pure_1"):
        calibrated = panels(SETTINGS[name], "sector")
        for model in ("relative_sign", "cusp"):
            require(panels(SETTINGS[name], model) == calibrated, "pure-tag sign controls")
    total_right = F(0)
    total_parent = F(0)
    local_splits = []
    for flipped in (False, True):
        sign = -1 if flipped else 1
        records = panels(setting, "relative_sign", last_tick=9, flip_tag_zero=flipped)
        cusp = panels(setting, "cusp", last_tick=9, flip_tag_zero=flipped)
        require(records == panels(setting, "relative_sign", True, 9, flip_tag_zero=flipped),
                "physical sign operation in a different tag frame")
        scaled_mass = F(1)  # At t=2, x=0, the tag-one parent has mass 1/4.
        for n in range(7):
            tick = n + 2
            raw, parent = records[tick]
            require((raw.get((n, 1, 0), 0), raw.get((n, 1, 1), 0)) == (n, 1),
                    "selected edge signed words")
            require((raw.get((n, 0, 0), 0), raw.get((n, 0, 1), 0)) == (sign, 0),
                    "spectator edge signed words")
            mass = sum(parent[n, 1, rail] for rail in (0, 1))
            require(2**tick * mass == scaled_mass, "edge marker recurrence")
            _, daughters = records[tick + 1]
            right, left = daughters[n + 1, 1, 0], daughters[n - 1, 1, 1]
            expected = F(1, 2) + (F(2*n, n*n + 5) if flipped else 0)
            require(right + left == mass and right / mass == expected, "conditional sign response")
            _, cusp_daughters = cusp[tick + 1]
            require(cusp_daughters[n + 1, 1, 0] == cusp_daughters[n - 1, 1, 1] > 0,
                    "sign-even cusp has zero edge slope")
            scaled_mass = 2 * expected * scaled_mass + 1
            if n == 2:
                total_right += right
                total_parent += mass
                local_splits.append(right / mass)
    require(sum(local_splits) / 2 == F(13, 18) and total_right / total_parent == F(151, 198),
            "equal-setting mean and pooled counts")


def run():
    check_finite_calibration()
    check_sign_control()
    all_panels, saved = {}, {}
    for name, setting in SETTINGS.items():
        start, origin, _, _ = setting
        records = {model: panels(setting, model) for model in MODELS}
        all_panels[name] = records
        for model in MODELS:
            require(records[model] == panels(setting, model, True), "spacetime tag relabel")
        max_norm = panels(setting, "max_norm")
        require(max_norm == records["sector"], "larger-norm rule reproduces every four-tick cell")
        require(max_norm == panels(setting, "max_norm", True), "larger-norm spacetime tag relabel")
        saved[name] = []
        for tick in records["sector"]:
            raw, autonomous = records["sector"][tick]
            _, rival = records["spectator"][tick]
            if name.startswith("pure") or name == "shield" or tick <= 3:
                require(autonomous == rival, "pure or pre-discriminator agreement")
            rows = [[x, b, r, raw.get((x,b,r), 0), str(autonomous[x,b,r]), str(rival[x,b,r])]
                    for x, b, r in cells(tick, origin, start)]
            saved[name].append({"tick": tick, "cells": rows})
    for first, flipped in (("pure_0", "pure_1"), ("overlap_0", "overlap_1")):
        for model in MODELS:
            for tick, (raw, first_masses) in all_panels[first][model].items():
                swap_raw, swap_masses = all_panels[flipped][model][tick]
                for (x,b,r), m in first_masses.items():
                    require(swap_masses[x,b^1,r] == m, "global complement mass")
                    require(swap_raw.get((x,b^1,r),0) == raw.get((x,b,r),0), "global complement tally")
    tests = {}
    for model in MODELS:
        raw, parent = all_panels["overlap_0"][model][3]
        require(tuple(raw.get((1,b,r),0) for b,r in product((0,1),repeat=2)) == (1,0,1,1),
                "selected and spectator input rails")
        mass = sum(parent[1,1,r] for r in (0,1))
        require(mass == F(1,4), "overlap parent mass")
        overlap = all_panels["overlap_0"][model][4][1]
        shield = all_panels["shield"][model][4][1]
        isolated_parent = sum(all_panels["shield"][model][3][1][1,1,r] for r in (0,1))
        dark, a, b = (0,1,1), (-2,1,1), (2,1,0)
        require((isolated_parent, shield[dark], shield[a], shield[b]) ==
                (F(1,2), 0, F(1,8), F(1,2)), "shield values")
        contrast = (overlap[a]*shield[b])/(overlap[b]*shield[a])
        require((overlap[dark],overlap[b],overlap[a],contrast) == EXPECTED[model], "joint witnesses")
        tests[model] = dict(overlap_parent=str(mass), shield_parent=str(isolated_parent),
                            left_given_parent=str(overlap[dark]/mass), shield_left_given_parent="0",
                            left_joint=str(overlap[dark]), positive_ports_overlap=[str(overlap[a]),str(overlap[b])],
                            positive_ports_shield=[str(shield[a]),str(shield[b])], cross_ratio=str(contrast))
    # Continue the overlap flight to a splitter where the selected sector has smaller norm.
    for model, expected_mass in (("sector", F(1, 256)), ("max_norm", F(5, 512))):
        extended = panels(SETTINGS["overlap_0"], model, last_tick=8)
        raw, parent = extended[7]
        require((raw[-1, 1, 0], raw[-1, 1, 1]) == (1, 2), "tick-seven selected rails")
        require(sum(raw[-1, 0, r]**2 for r in (0, 1)) == 8, "tick-seven other sector norm")
        require(sum(parent[-1, 1, r] for r in (0, 1)) == F(5, 128), "tick-seven parent mass")
        _, terminal = extended[8]
        require(terminal[-2, 1, 1] == expected_mass, "tick-eight tagged left daughter")
    return dict(columns=["site","tag","rail (0=R,1=L)","signed words","sector mass","spectator mass"],
                settings=saved, witnesses=tests)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    dest = parser.parse_args().directory
    dest.mkdir(parents=True, exist_ok=True)
    output = dest/"tag_sector_controls.json"
    if output.exists():
        parser.exit(2, f"Refusing to overwrite {output}\n")
    result = run()
    with output.open("x", encoding="utf-8", newline="\n") as f:
        json.dump(result, f, separators=(",",":"), allow_nan=False)
        f.write("\n")


if __name__ == "__main__":
    main()
