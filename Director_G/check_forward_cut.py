"""Certify the forward three-tick paths by physical words and a site recurrence."""
from argparse import ArgumentParser
from collections import defaultdict
from fractions import Fraction
from itertools import product
import json
from pathlib import Path

from check_reflecting_path import launch, physical_step


def shift(length, x, direction):
    neighbor = x + 1 - 2 * direction
    if 0 <= neighbor < length:
        return neighbor, direction
    return x, 1 - direction


def histories(length, x, ticks, start_rail=0):
    """Keep canceled histories as well as bright endpoints."""
    by_target = defaultdict(list)
    for word in product((0, 1), repeat=ticks):
        path = [(x, start_rail)]
        sign = 1
        for direction in word:
            site, rail = path[-1]
            if rail == direction == 1:
                sign = -sign
            path.append(shift(length, site, direction))
        by_target[path[-1]].append((path, sign))
    return by_target


def coefficients(length, x, clock, target):
    """Use a forward recurrence with a single intermediate port mask."""
    before = launch(length, x)
    for _ in range(clock):
        before = physical_step(before)
    weights = {}
    for site, row in enumerate(before):
        for rail, amplitude in enumerate(row):
            if amplitude:
                after = launch(length, site, rail)
                for _ in range(3 - clock):
                    after = physical_step(after)
                weight = amplitude * after[target[0]][target[1]]
                if weight:
                    weights[site, rail] = weight
    return weights


def connected(ports, edges):
    neighbors = {port: set() for port in ports}
    for a, b in edges:
        if a in ports and b in ports:
            neighbors[a].add(b)
            neighbors[b].add(a)
    reached = set()
    pending = [min(ports)]
    while pending:
        port = pending.pop()
        if port not in reached:
            reached.add(port)
            pending.extend(neighbors[port] - reached)
    return reached == ports


def report():
    scans = []
    sample = []
    for length in range(3, 41):
        edges = []
        for x in range(length):
            dark = shift(length, x, 1)
            companion = dark[0], 1 - dark[1]
            paths = histories(length, x, 3)
            assert len(paths[dark]) == 2 and len(paths[companion]) == 1
            for tick in (1, 2):
                for terminal in (dark, companion):
                    by_word = {p[tick]: sg for p, sg in paths[terminal]}
                    assert len(by_word) == len(paths[terminal])
                    assert coefficients(length, x, tick, terminal) == by_word
                a, b = [p[tick] for p, _ in paths[dark]]
                signs = [sg for _, sg in paths[dark]]
                assert sorted(signs) == [-1, 1]
                expected = ({shift(length, x, 0), shift(length, x, 1)}
                            if tick == 1 else {(x, 0), (x, 1)})
                assert {a, b} == expected
                edges.append((a, b))
                if length == 8:
                    third = paths[companion][0][0][tick]
                    sample.append({"right_launch": x, "read_tick": tick, "dark_port": dark,
                                   "ports_at_read": [a, b], "path_signs": signs,
                                   "companion_path_port_at_read": third,
                                   "split_by_middle_cut": (a[0] < 4) != (b[0] < 4)})
            for rail in (0, 1):
                for ticks in range(3):
                    paths_short = histories(length, x, ticks, rail)
                    assert all(len(group) == 1 for group in paths_short.values())
        for cut in range(1, length):
            for sites in (range(cut), range(cut, length)):
                ports = set(product(sites, (0, 1)))
                assert connected(ports, edges)
        scans.append({"wells": length, "connected_cuts": length - 1,
                      "right_launch_clocks": 2 * length})
    left = next(r for r in sample if r["right_launch"] == 0 and r["read_tick"] == 1)
    assert set(map(tuple, left["ports_at_read"])) == {(0, 0), (1, 0)}
    assert left["companion_path_port_at_read"][0] < 4
    tags = {"coherent": lambda port: (0, 1),
            "mark_only_1R_with_minus": lambda port: (0, -1 if port == (1, 0) else 1),
            "orthogonal_tags_on_0R_and_1R": lambda port: (int(port == (1, 0)), 1)}
    observed = {}
    for name, tag in tags.items():
        site = Fraction(0)
        for rail in (0, 1):
            sums = defaultdict(int)
            for path, sign in histories(8, 0, 3)[0, rail]:
                private, phase = tag(path[1])
                assert path[1][0] < 4
                sums[private] += phase * sign
            prob = Fraction(sum(n*n for n in sums.values()), 8)
            site += prob
            if rail == 0:
                dark = prob
        observed[name] = {"dark": str(dark), "site": str(site)}
    assert [(r["dark"], r["site"]) for r in observed.values()] == [
        ("0", "1/8"), ("1/2", "5/8"), ("1/4", "3/8")]
    return {"units": "path amplitudes at tick three in multiples of 1/sqrt(8)",
            "all_lengths": scans, "eight_well_controls": sample,
            "left_wall_same_bin_probabilities": observed}


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    with parser.parse_args().output.open("x", encoding="utf-8", newline="\n") as out:
        out.write(json.dumps(report(), indent=2) + "\n")
