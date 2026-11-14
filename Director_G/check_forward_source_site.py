"""Check four-tick source-site identities on the reflecting interval."""
from argparse import ArgumentParser
from collections import Counter
from itertools import product
import json
from pathlib import Path

from check_forward_cut import connected, histories, shift
from check_reflecting_path import launch, physical_step


def travel(length, x, rail, ticks):
    for _ in range(ticks):
        x, rail = shift(length, x, rail)
    return x, rail


def word_coefficients(group, k):
    result = Counter()
    for path, sign in group:
        result[path[k]] += sign
    return {key: val for key, val in result.items() if val}


def site_coefficients(values):
    per_site = Counter()
    for (site, _), val in values.items():
        per_site[site] += val
    return {key: val for key, val in per_site.items() if val}


def recurrence(length, x, rail, clock):
    incoming = launch(length, x, rail)
    for _ in range(clock):
        incoming = physical_step(incoming)
    by_rail = [{}, {}]
    for i, row in enumerate(incoming):
        for r, a in enumerate(row):
            if not a:
                continue
            state = launch(length, i, r)
            for _ in range(4-clock):
                state = physical_step(state)
            for f, v in enumerate(state[x]):
                if v:
                    by_rail[f][i, r] = a*v
    return by_rail


def report():
    scans = []
    exemplar = []
    for length in range(4, 33):
        edges = []
        touched = set()
        for x, rail in product(range(length), (0, 1)):
            paths = histories(length, x, 4, rail)
            for k in (2, 3):
                actual = [word_coefficients(paths[x, f], k) for f in (0, 1)]
                assert actual == recurrence(length, x, rail, k)
                if k == 2:
                    actual = [site_coefficients(values) for values in actual]
                sign = 1 - 2*rail
                same, opposite = actual[rail], actual[1-rail]
                if k == 3:
                    y, stored = travel(length, x, rail, 1)
                    expected = {(y, stored): 2*sign, (y, 1-stored): -sign}
                    other_site = travel(length, x, 1-rail, 1)[0]
                    assert len(same) == 1 and next(iter(same))[0] == other_site
                    touched.add(y)
                else:
                    z = travel(length, x, rail, 2)[0]
                    other_site = travel(length, x, 1-rail, 2)[0]
                    expected = {x: 2*sign, z: -sign}
                    assert set(same) == {other_site}
                    edges.append((x, z))
                assert opposite == expected and list(same.values()) == [-1]
                if length == 8:
                    exemplar.append({"x": x, "launch_rail": rail, "clock": k,
                                     "opposite_rail_source_amplitude": sorted(opposite.items()),
                                     "same_rail_source_amplitude": sorted(same.items())})
        assert len(touched) == length
        for cut in range(1, length):
            for sites in (set(range(cut)), set(range(cut, length))):
                assert connected(sites, edges)
        scans.append({"wells": length, "cuts": length - 1,
                      "basis_launch_and_insert_time_combinations": 4*length})
    # Reachable monitored source paths at <=3 ticks for a controlled lower bound.
    length, cut = 16, 8
    comparisons = 0
    for t in range(4):
        for x, r in product(range(length), (0, 1)):
            paths = histories(length, x, t, r)
            for k in range(t+1):
                for fin in (0, 1):
                    ordinary, marked = Counter(), Counter()
                    for path, s in paths.get((x, fin), []):
                        mid = path[k]
                        label = int(mid[0] >= cut)
                        ordinary[label] += s
                        marked[label] += -s if mid == (4, 0) else s
                    assert {b: v*v for b, v in ordinary.items()} == {
                        b: v*v for b, v in marked.items()}
                    comparisons += 1
    return {"amplitude_units": "1/4", "all_lengths": scans,
            "eight_well_source_coefficients": exemplar,
            "short_source_only_phase_control": {"wells": length, "cut": cut,
                                                 "phase_flip_at": [4, 0],
                                                 "matched_joint_source_events": comparisons}}


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    with parser.parse_args().output.open("x", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(report(), indent=2) + "\n")
