"""Check a sharp-sheet five-tick power test by physical paths and by rail propagation."""
from argparse import ArgumentParser
from collections import Counter
from fractions import Fraction
from itertools import product
import json
from pathlib import Path


SWAPS = {(3, -3), (4, 2)}
SITES = range(-5, 6, 2)
SCORE = {(-3, 0): 16, (1, 1): -8, (3, 1): 1}


def check(ok, detail):
    if not ok:
        raise ValueError(detail)


def path_table(initial, swaps, ticks=5, stationary_origin=False):
    signed, counts = Counter(), Counter()
    for word in product((1, -1), repeat=ticks):
        x, s, last, sign = 0, initial, 1, 1
        for tick, move in enumerate(word, 1):
            sign *= -1 if last == move == -1 else 1
            x += move
            s ^= int(x == 0 if stationary_origin else (tick, x) in swaps)
            last = move
        signed[x, s, last] += sign
        counts[x, s, last] += 1
    return signed, counts


def propagated(initial, swaps, ticks=5, stationary_origin=False):
    before = Counter({(0, initial, 1): 1})
    for tick in range(1, ticks+1):
        after = Counter()
        for x in range(-tick, tick+1, 2):
            for s in (0, 1):
                source_sheet = s ^ (x == 0 if stationary_origin else (tick, x) in swaps)
                after[x,s,1] = before[x-1,source_sheet,1] + before[x-1,source_sheet,-1]
                after[x,s,-1] = before[x+1,source_sheet,1] - before[x+1,source_sheet,-1]
        before = after
    return before


def coordinates(table, ticks=5):
    return {(x,s): [table[x,s,1], table[x,s,-1]]
            for x in range(-ticks,ticks+1,2) for s in (0,1)}


def means(weights, score=SCORE):
    return Fraction(sum(v*weights[k] for k,v in score.items()), sum(weights.values()))


def part_weights(rows, split, q):
    weights = {}
    positive = []
    for k, (a,b) in rows.items():
        cells = (a*a,b*b) if k in split else (a*a+b*b,)
        positive.extend((v,k) for v in cells if v)
        weights[k] = sum(v**q for v in cells if v)
    return weights, positive


def labels(k):
    return ",".join(map(str, k))


def serialized(rows):
    return {labels(k): v for k, v in rows.items()}


def stationary_panel():
    ticks = 6
    score = {(6,0):16, (2,1):-8, (0,0):1, (-2,1):5}
    signed, unsigned = path_table(0, set(), ticks, stationary_origin=True)
    rows = coordinates(signed, ticks)
    counts = {k: sum(v) for k,v in coordinates(unsigned, ticks).items()}
    check(rows == coordinates(propagated(0,set(),ticks,stationary_origin=True), ticks),
          "stationary return recurrence")
    check(sum(counts.values()) == sum(a*a+b*b for a,b in rows.values()) == 64, "six-tick totals")
    other, other_unsigned = path_table(1, set(), ticks, stationary_origin=True)
    other_rows = coordinates(other, ticks)
    check(other_rows == coordinates(propagated(1,set(),ticks,stationary_origin=True), ticks),
          "opposite sheet recurrence")
    other_counts = coordinates(other_unsigned, ticks)
    for (x,s), row in rows.items():
        check(other_rows[x,1-s] == row and sum(other_counts[x,1-s]) == counts[x,s],
              "relative sheet and direction-count covariance")
    check([rows[k] for k in score] == [[1,0],[0,2],[0,-4],[0,0]], "pure and dark target rows")
    check(rows[-4,1] == [0,0] and (counts[-2,1], counts[-4,1]) == (6,2), "two dark controls")
    count_score = means(counts, score)
    check(count_score == Fraction(3,32), "positive counting score including dark output")
    no_swap = coordinates(propagated(0,set(),ticks),ticks)
    for x,s in rows:
        check([u+v for u,v in zip(rows[x,0], rows[x,1])] == no_swap[x,0],
              "sum of both sheet amplitudes is the bare walk")
    bare_score = means(part_weights(no_swap, set(), 1)[0], score)
    opposite = means(part_weights(other_rows, set(), 1)[0], score)
    ordinary = part_weights(rows, set(), 1)[0]
    pooled = Fraction(sum(c*(ordinary[x,0]+ordinary[x,1]) for (x,_),c in score.items()), 64)
    check(bare_score == Fraction(3,8) and pooled == opposite == Fraction(-7,64), "read controls")
    mixed = [k for k,(a,b) in rows.items() if a and b]
    panels = []
    for bits in product((False,True), repeat=len(mixed)):
        split = {k for k,bit in zip(mixed,bits) if bit}
        panel = {"split_coordinates": sorted(split), "powers": {}}
        for q in (0,1,2,3,5,10,30):
            weights, positive = part_weights(rows,split,q)
            normalizer = sum(weights.values())
            d = means(weights,score)
            check(len(positive)<=15 and [k for v,k in positive if v==16] == [(0,0)]
                  and max(v for v,k in positive if k!=(0,0))<=10, "unique largest static cell")
            check(d*normalizer == (4**q-4)**2 and (d==0)==(q==1), "static score square")
            panel["powers"][str(q)] = {"score":str(d), "normalizer":normalizer}
        panels.append(panel)
    check(len(panels)==32, "all five static partition choices")
    return {"scores":serialized(score), "signed_rails":serialized(rows),
            "unsigned_rails":serialized(coordinates(unsigned,ticks)), "partitions":panels,
            "counting_score":str(count_score), "no_swap_score":str(bare_score),
            "pooled_position_score":str(pooled), "uncorrected_opposite_sheet_score":str(opposite)}


def run():
    signed, unsigned = path_table(0, SWAPS)
    rows, counts = coordinates(signed), coordinates(unsigned)
    check(rows == coordinates(propagated(0, SWAPS)), "signed coordinate recurrence")
    check(sum(a*a+b*b for a,b in rows.values()) == sum(map(sum, counts.values())) == 32,
          "norm and complete physical paths")
    counts_by_site_sheet = {k:sum(v) for k,v in counts.items()}
    check(means(counts_by_site_sheet) == Fraction(5,8), "unsigned score")
    check(counts_by_site_sheet[1,0] == 6 and rows[1,0] == [0,0], "six paths at dark record")
    check([rows[k] for k in SCORE] == [[0,1],[0,2],[4,0]], "three pure rail coordinates")
    other_signed, other_counts = path_table(1, SWAPS)
    other_rows = coordinates(other_signed)
    check(other_rows == coordinates(propagated(1, SWAPS)), "opposite initial sheet")
    for k, v in rows.items():
        x, s = k
        check(other_rows[x,1-s] == v and coordinates(other_counts)[x,1-s] == counts[k],
              "full signed and unsigned sheet-label covariance")
    other_weights, _ = part_weights(other_rows, set(), 1)
    check(means(other_weights) == Fraction(33,32), "uncorrected opposite source")
    bare_rows = coordinates(path_table(0, set())[0])
    check(bare_rows == coordinates(propagated(0, set())), "no-swap control")
    for x in SITES:
        for rail in (0,1):
            check(rows[x,0][rail] + rows[x,1][rail] == bare_rows[x,0][rail],
                  "sheet-sum projection intertwines the walk")
    bare_weights, _ = part_weights(bare_rows, set(), 1)
    check(means(bare_weights) == Fraction(5,2), "unswapped score")
    ordinary, _ = part_weights(rows, set(), 1)
    site_w = {x: ordinary[x,0]+ordinary[x,1] for x in SITES}
    pooled_score = Fraction(sum(v*site_w[x] for (x,_),v in SCORE.items()), sum(site_w.values()))
    check(pooled_score == Fraction(33,32), "position-only score")

    mixed = [k for k,(a,b) in rows.items() if a and b]
    panels = []
    for mask in product((False,True), repeat=len(mixed)):
        split = {k for k,bit in zip(mixed,mask) if bit}
        panel = {"split_coordinates": sorted(split), "powers": {}}
        for q in (0,1,2,3,5,10,30):
            w, positive = part_weights(rows,split,q)
            check(len(positive) <= 11 and [k for v,k in positive if v == 16] == [(3,1)]
                  and max(v for v,k in positive if k != (3,1)) <= 5, "unique largest and size")
            d = means(w)
            check(d*sum(w.values()) == (4**q-4)**2, "score square identity")
            check((d == 0) == (q == 1), "power equals ordinary threshold")
            panel["powers"][str(q)] = {"normalizer": sum(w.values()), "score": str(d)}
        panels.append(panel)
    check(len(panels) == 4, "both mixed-rail cells independently partitioned")
    return {
        "six_tick_stationary_origin":stationary_panel(),
        "swaps_after_shift":sorted(SWAPS), "scores":serialized(SCORE),
        "signed_rails_by_x_and_sheet":serialized(rows),
        "unsigned_paths_by_x_sheet_and_rail":serialized(counts),
        "no_swap_rails":serialized(bare_rows), "partitions":panels,
        "ordinary_source1_score_with_uncorrected_labels":str(means(other_weights)),
        "ordinary_no_swap_score":str(means(bare_weights)),
        "ordinary_site_only_score":str(pooled_score),
        "counting_score":str(means(counts_by_site_sheet)), "counting_dark_rate":"3/16",
    }


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    report = run()
    with args.output.open("x", encoding="utf-8", newline="\n") as output:
        json.dump(report, output, indent=2)
        output.write("\n")
