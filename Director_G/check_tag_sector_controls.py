"""Compute the five sharp-launch panels in Tag_sector_controls.md using exact arithmetic.

Run python -B check_tag_sector_controls.py OUTPUT_DIRECTORY. Existing output is preserved.
"""
import argparse
from fractions import Fraction as F
from itertools import product
import json
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


def words(setting, tick):
    """Sum the signed direction words. A scheduled XOR occurs on arrival."""
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
        port = x, tag, rail
        tally[port] = tally.get(port, 0) + sign
    return tally


def encode(tick, x, tag, translated):
    # Deliberately change frames at selected sites and times. A real link
    # transports from the old frame at x to the next frame at its endpoint.
    flip = translated and (tick + x//2) % 3 == 1
    return tag ^ int(flip)


def panels(setting, model, translated=False):
    start, origin, initial_tag, enabled = setting
    masses = {(origin, encode(start, origin, initial_tag, translated), 0): F(1)}
    records = {}
    for tick in range(start, LAST_TICK+1):
        raw = words(setting, tick)
        signed = {(x, encode(tick, x, b, translated), r): v for (x, b, r), v in raw.items()}
        decoded = {(x, b, r): masses.get((x, encode(tick, x, b, translated), r), F(0))
                   for x, b, r in cells(tick, origin, start)}
        require(sum(decoded.values()) == 1, "marker conservation")
        require(all(m >= 0 for m in decoded.values()), "nonnegative marker")
        if model == "sector":
            require(all(m == F(raw.get(cell, 0)**2, 2**(tick-start))
                        for cell, m in decoded.items()), "signed word oracle")
        records[tick] = raw, decoded
        if tick == LAST_TICK:
            break
        future = {}
        for x, b in product(range(origin-(tick-start), origin+(tick-start)+1), (0, 1)):
            u, v = (signed.get((x, b, r), 0) for r in (0, 1))
            norm = u*u + v*v
            if model == "spectator":
                norm += sum(signed.get((x, b^1, r), 0)**2 for r in (0, 1))
            right = F(1, 2) + (F(u*v, norm) if norm else 0)
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


def run():
    all_panels, saved = {}, {}
    for name, setting in SETTINGS.items():
        start, origin, _, _ = setting
        records = {model: panels(setting, model) for model in MODELS}
        all_panels[name] = records
        for model in MODELS:
            require(records[model] == panels(setting, model, True), "spacetime tag relabel")
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
