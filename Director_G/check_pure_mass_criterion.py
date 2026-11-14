"""Check the site-only countermixtures and scan the balanced reciprocal cover."""
from argparse import ArgumentParser
from fractions import Fraction
from itertools import product
import json
from pathlib import Path


def advance(state):
    size = len(state)
    return [(sum(state[(j-1) % size]),
             state[(j+1) % size][0] - state[(j+1) % size][1]) for j in range(size)]


def by_words(length, ticks):
    """Use physical wells and flip a real sheet label on either seam crossing."""
    out = [[0, 0] for _ in range(2*length)]
    counts = [0] * (2*length)
    for word in product((1, -1), repeat=ticks):
        site, sheet, previous, sign = 0, 0, 1, 1
        for direction in word:
            dest = (site+direction) % length
            sheet ^= int({site, dest} == {0, length-1})
            if previous == direction == -1:
                sign = -sign
            site, previous = dest, direction
        j = site + length*sheet
        counts[j] += 1
        out[j][int(previous == -1)] += sign
    return list(map(tuple, out)), counts


def histogram(weights):
    total = sum(weights)
    return tuple(Fraction(w, total) for w in weights)


def split_one_control(site_masses):
    ordinary = histogram(site_masses)
    # k=3 occupied sites, all other sites dark. One site is split in two.
    mixing = tuple(4*p - 1 for p in ordinary)
    splits = [histogram([1+int(x == j) for x in range(3)]) for j in range(3)]
    assert sum(mixing) == 1 and min(mixing) > 0
    recovered = tuple(sum(w*row[x] for w, row in zip(mixing, splits)) for x in range(3))
    assert recovered == ordinary
    return {"ordinary": list(map(str, ordinary)), "q0_types": [list(map(str, s)) for s in splits],
            "mixing_law": list(map(str, mixing)), "recovered": list(map(str, recovered))}


def zero_geometry(length, ticks, well_groups):
    """Retain dark cells when recording the underlying physical rows."""
    rails, counts = by_words(length, ticks)
    state = [(int(j == 0), 0) for j in range(2*length)]
    for _ in range(ticks):
        state = advance(state)
    assert state == rails
    assert sum(r*r+l*l for r, l in rails) == sum(counts) == 2**ticks
    site_modes = [rails[x] + rails[x+length] for x in well_groups]
    return rails, counts, site_modes


def ring_scan():
    table = []
    for length in range(3, 91):
        state = [(int(j == 0), 0) for j in range(2*length)]
        counts = []
        for tick in range(1, 121):
            state = advance(state)
            assert sum(r*r + l*l for r, l in state) == 2**tick
            pure = set()
            for x in range(length):
                live = [a*a for a in state[x]+state[x+length] if a]
                if len(live) == 1:
                    pure.add(live[0])
            counts.append(len(pure))
        table.append({"base_length": length, "distinct_pure_masses_by_tick": counts})
    return table


def run():
    wells = (1, 3, 5)
    rails, counts, modes = zero_geometry(6, 11, wells)
    assert [sum(int(v != 0) for v in row) for row in modes] == [3, 3, 3]
    site_masses = [sum(v*v for v in row) for row in modes]
    assert site_masses == [729, 558, 761]
    mixture = split_one_control(site_masses)
    # Tagging a single occupied site separates its two sheets, exposing one pure cell.
    subset_audit = []
    for read in product((False, True), repeat=len(wells)):
        pure = []
        for row, enable in zip(modes, read):
            for obs in (row[:2], row[2:]) if enable else (row,):
                live = [a*a for a in obs if a]
                if len(live) == 1:
                    pure.append(live[0])
        assert len(set(pure)) == sum(read)
        subset_audit.append({"sheet_read_at": [x for x, bit in zip(wells, read) if bit],
                             "pure_masses": sorted(pure)})
    scores = ring_scan()
    totals = {i: sum(r["distinct_pure_masses_by_tick"].count(i) for r in scores)
              for i in range(3)}
    assert sum(totals.values()) == 88*120
    return {"six_wells": {"ticks": 11, "cover_amplitudes": rails, "word_counts": counts,
                           "base_sites": wells, "base_masses": site_masses,
                           "q0_counterexample": mixture, "partial_sheet_readouts": subset_audit},
            "scan_ticks": [1, 120], "site_only_pure_mass_counts": totals,
            "ring_scan": scores}


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("output", type=Path)
    args = cli.parse_args()
    with args.output.open("x", encoding="utf-8", newline="\n") as out:
        # One compact record per ring keeps all 10,560 settings in tick order.
        result = run()
        scans = result.pop("ring_scan")
        out.write(json.dumps(result, indent=2)[:-2] + ',\n  "ring_scan": [\n')
        out.write(",\n".join("    " + json.dumps(row) for row in scans))
        out.write("\n  ]\n}\n")
