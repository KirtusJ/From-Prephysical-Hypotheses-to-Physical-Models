"""Enumerate complete site masks and compare two-column Hadamard preparations."""

import argparse
from itertools import combinations, product
import json
from math import gcd
from pathlib import Path

from check_compact_bin_reflections import flight, transport


def require(test, detail):
    if not test:
        raise ValueError(detail)


def gram(rows):
    return [sum(a*a for a, b in rows), sum(a*b for a, b in rows),
            sum(b*b for a, b in rows)]


def odd(n):
    return n // (n & -n) if n else 0


def invariants(rows):
    minors = [a*d-b*c for (a, b), (c, d) in combinations(rows, 2)]
    return [odd(gcd(*(v[i] for v in rows))) for i in (0, 1)], odd(gcd(*minors))


def enumerate_paths(t):
    rows = {}
    for path in product((0, 1), repeat=t):
        x = t - 2*sum(path)
        for start in (0, 1):
            path_with_start = (start,) + path
            flips = sum(a*b for a, b in zip(path_with_start, path_with_start[1:]))
            out = (x, path_with_start[-1])
            rows.setdefault(out, [0, 0])[start] += (-1)**flips
    return rows


def census(t, table):
    sites = sorted({x for x, r in table})
    primitive = full_rank = 0
    rejections = []
    for size in range(1, len(sites)+1):
        for mask in combinations(sites, size):
            rows = [v for (x, r), v in table.items() if x in mask]
            contents, index = invariants(rows)
            full_rank += index != 0
            if index and contents == [1, 1]:
                primitive += 1
                if index > 1:
                    rejections.append({"sites": list(mask), "odd_minor_gcd": index})
    return {"ticks": t, "nonempty_masks": 2**len(sites)-1, "real_rank_two": full_rank,
            "rank_two_and_individually_odd_primitive": primitive,
            "primitive_pairs_with_odd_rank_drop": rejections}


def build():
    counts = []
    for t in range(9):
        rows = enumerate_paths(t)
        single = flight(t)
        require(all(row[0] == single.get(k, 0) for k, row in rows.items()), "first rail sign")
        require(gram(list(rows.values())) == [2**t, 0, 2**t], "whole-flight isometry")
        counts.append(census(t, rows))
    require(all(not c["primitive_pairs_with_odd_rank_drop"] for c in counts[:7]), "earlier mask")
    require(counts[7]["primitive_pairs_with_odd_rank_drop"] ==
            [{"sites": [-3], "odd_minor_gcd": 7}, {"sites": [3], "odd_minor_gcd": 7}], "first masks")
    table = enumerate_paths(7)
    source = [table[3, 0], table[3, 1]]
    target = [[0, 2], [3, 1], [4, 0], [4, 0]]
    complement = [v for (x, r), v in table.items() if x != 3]
    require(source == [[5, -1], [4, 2]], "right site rail labels")
    require(gram(source) == gram(target) == [41, 3, 5], "marked effect")
    require(gram(complement) == [87, -3, 123], "complement effect")
    require(gram(target+complement) == [128, 0, 128], "full target")
    require(invariants(source) == ([1, 1], 7) and invariants(target) == ([1, 1], 1),
            "separate columns versus both columns")
    inverse_action = [[a-2*b, (a+5*b)//2] for a,b in target]
    require(all((a+5*b) % 2 == 0 for a,b in target), "integer numerator")
    require(gram(inverse_action) == [49,0,49], "orthonormal over seven")
    require([[5*a+4*b,-a+2*b] for a,b in inverse_action] ==
            [[7*a,7*b] for a,b in target], "forced isometry sends both physical columns")
    gate_counts = []
    for i in (0, 1):
        receipt = transport([v[i] for v in source], [v[i] for v in target], digit_padding=True)
        require("obstruction" not in receipt, "one-column transport")
        gate_counts.append(receipt["gates_per_reflection"])

    # A concrete joint operation: pad the two physical addresses with two zeros
    # and apply H tensor H. Neither step requires a division by an odd prime.
    benign = []
    for sign in (1, -1, 1, -1):
        benign.append([a + sign*b for a,b in zip(*source)])
    require(gram(benign) == [4*v for v in gram(source)], "joint Walsh numerator at scale two")
    test = (1,-2)
    source_mix = [x*test[0]+y*test[1] for x,y in source]
    target_mix = [x*test[0]+y*test[1] for x,y in target]
    require(source_mix == [7,0] and target_mix == [-4,1,4,4], "odd-divisor witness")
    require(sum(v*v for v in source_mix) == sum(v*v for v in target_mix) == 49, "equal flag mass")
    require(all(x == 0 for x in source_mix[1:]) and [x*x for x in target_mix[2:]] == [16,16],
            "resolved read of padded output")
    return {"census": counts, "tick_seven_plus_three": {"source": source, "target": target,
            "source_and_target_marked_gram_RR_RL_LL": gram(source), "complement_gram": gram(complement),
            "forced_isometry_numerators_over_7": inverse_action, "single_column_gate_counts": gate_counts,
            "source_and_target_for_test_direction": [source_mix,target_mix],
            "both_pooled_masses_normalized_test_coin": "49/640",
            "benign_simultaneous_Walsh_image_numerators_over_2": benign}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    with args.output.open("x", encoding="utf-8", newline="\n") as out:
        json.dump(build(), out, indent=2)
        out.write("\n")
