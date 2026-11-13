"""Finite terminal coordinate support tests for the signed area walk. Standard library.

Run python -B check_holonomy_cone.py results. For the same endpoint, a length-n
record with speed-one sheet motion is supported in an arc of width 2n (2n+1
integer sites). We allow its centre to depend arbitrarily on the endpoint.
"""

import argparse
import json
from collections import Counter, defaultdict
from heapq import merge
from itertools import product
from pathlib import Path

HORIZON = 80
BASE_ORDER = 256
SHEET_ORDER = 65536
DIRECTIONS = (1, -1)


def tick(state, bounded_control=False):
    """Apply H to the coin and add the departure coordinate to the sheet."""
    out = defaultdict(int)
    for (x, c, y), v in state.items():
        gain = (x > 0) - (x < 0) if bounded_control else x
        out[x + 1, 1, y + gain] += v
        out[x - 1, -1, y + gain] += v if c == 1 else -v
    return {cell: v for cell, v in out.items() if v}


def word_check(n, start):
    out = Counter()
    for word in product(DIRECTIONS, repeat=n):
        x = y = 0
        c = start
        sign = 1
        for d in word:
            if c == d == -1:
                sign = -sign
            y += x
            x += d
            c = d
        out[x, c, y] += sign
    return {k: v for k, v in out.items() if v}


def cone_metrics(cells, width):
    """Optimize two different objectives; each may have its own optimum arc."""
    cells.sort()
    total = sum(w for y, w in cells)
    left = current = best = 0
    far_left_mass = ordered_pairs = 0
    best_start = cells[0][0]
    for y, w in cells:
        current += w
        while cells[left][0] < y - width:
            current -= cells[left][1]
            far_left_mass += cells[left][1]
            left += 1
        ordered_pairs += 2 * w * far_left_mass
        if current > best:
            best = current
            best_start = y - width
    # Distance from y to [s,s+width] equals
    # (|y-s|+|y-width-s|-width)/2. Thus s is a weighted median
    # of y and y-width, each weighted by this cell's squared numerator.
    cumulative = 0
    median = None
    for s, w in merge(cells, ((y - width, w) for y, w in cells)):
        cumulative += w
        if cumulative >= total:
            median = s
            break
    cost = sum(w * max(median - y, 0, y - median - width) for y, w in cells)
    assert cost >= total - best and (cost == 0) == (total == best)
    return [total, total - best, cost, best_start, median, ordered_pairs]


def compile_ports(state, n, exhaustive=False):
    groups = defaultdict(list)
    for (x, c, y), v in state.items():
        groups[x, c].append((y, v * v))
    rows = []
    for (x, c), cells in sorted(groups.items()):
        result = cone_metrics(cells, 2 * n)
        if exhaustive:
            tails = []
            costs = []
            for left in range(cells[0][0] - 2 * n, cells[-1][0] + 1):
                ds = [(max(left - y, 0, y - left - 2 * n), w) for y, w in cells]
                tails.append(sum(w for d, w in ds if d > 0))
                costs.append(sum(d * w for d, w in ds))
            assert result[1:3] == [min(tails), min(costs)]
            assert result[-1] == sum(w * v for y, w in cells for z, v in cells if abs(y - z) > 2 * n)
        rows.append([x, c, *result])
    assert sum(r[2] for r in rows) == 2**n
    return rows


def main():
    assert BASE_ORDER > 2 * HORIZON
    # If a candidate ball centre is farther than 2A+n from 0, it is worse
    # for every occupied y than the ball centred on 0. Within that range
    # no circular metric wraps. A=n(n-1)/2 bounds all possible |y|.
    area = HORIZON * (HORIZON - 1) // 2
    assert SHEET_ORDER > 6 * area + 2 * HORIZON
    states = [{(0, c, 0): 1} for c in DIRECTIONS]
    bounded = {(0, 1, 0): 1}
    saved = []
    for n in range(1, HORIZON + 1):
        states = [tick(state) for state in states]
        for state, start in zip(states, DIRECTIONS):
            if n <= 13:
                assert state == word_check(n, start)
        # On mirrored words the two Hadamard products differ by a fixed
        # sign (-1)^(n-number of turns); turn parity is fixed by the port.
        right, left = states
        assert len(right) == len(left)
        for (x, c, y), v in right.items():
            assert left[-x, -c, -y] == (-1) ** (n - int(c == -1)) * v
        rows = compile_ports(right, n, exhaustive=n <= 10)
        totals = [sum(r[i] for r in rows) for i in (3, 4)]
        two_launch = sum(r[-1] for r in rows)
        same_port = sum(r[2] ** 2 for r in rows)
        if n <= 10:
            lrows = compile_ports(left, n, exhaustive=True)
            assert totals == [sum(r[i] for r in lrows) for i in (3, 4)]
            assert two_launch == sum(r[-1] for r in lrows)
        den = 2**n
        if n <= 16:
            bounded = tick(bounded, bounded_control=True)
            bounded_rows = compile_ports(bounded, n)
            assert not any(r[3] or r[4] or r[-1] for r in bounded_rows)
        if n >= 7:
            p = n // 2
            q = (n - 1) // 2
            assert 2 * p * q > 2 * n
            # Unique extreme words at a common port. Confirm both amplitudes
            # are +/-1, without appealing to counts that may cancel elsewhere.
            U = p * (p - 1) // 2 + q * p - q * (q - 1) // 2 + (p - q)
            D = -q * (q - 1) // 2 - p * q + p * (p - 1) // 2 + (p - q)
            assert U - D == 2 * p * q and all(abs(right[p - q + 1, 1, y]) == 1 for y in (U, D))
            assert totals[0] >= 1
        saved.append(
            {
                "tick": n,
                "denominator": den,
                "right_and_mirrored_left_ports": rows,
                "minimum_TV_escaped_numerator": totals[0],
                "minimum_fixed_base_fibre_W1_numerator": totals[1],
                "minimum_TV": totals[0] / den,
                "minimum_fixed_base_fibre_W1_cells": totals[1] / den,
                "two_launch_denominator": den**2,
                "two_launch_same_port_numerator": same_port,
                "two_launch_same_port_distance_over_2n_numerator": two_launch,
                "two_launch_unconditional_probability": two_launch / den**2,
            }
        )
    assert all(r["minimum_TV_escaped_numerator"] == 0 for r in saved[:6])
    assert (
        saved[6]["minimum_TV_escaped_numerator"] == 8
        and saved[6]["minimum_fixed_base_fibre_W1_numerator"] == 16
    )
    seven = word_check(7, 1)
    assert [r["two_launch_same_port_distance_over_2n_numerator"] for r in saved[:7]] == [0] * 6 + [20]
    seven_pairs = [(r[0], r[1], r[-1]) for r in saved[6]["right_and_mirrored_left_ports"] if r[-1]]
    assert seven_pairs == [(-3, -1, 2), (-1, -1, 6), (-1, 1, 2), (1, -1, 2), (1, 1, 6), (3, 1, 2)]
    witness = [[y, v] for (x, c, y), v in sorted(seven.items()) if (x, c) == (1, 1)]
    assert witness == [
        [-9, 1],
        [-7, -1],
        [-5, -2],
        [-3, 1],
        [-1, -1],
        [1, -1],
        [3, 1],
        [5, -2],
        [7, -1],
        [9, 1],
    ]
    # A balanced splitter and two deterministic mirrors are a different
    # instrument from an unrestricted H walk. Model its optional ideal read.
    two_paths = {
        "clock_localized_bright_prob": "1/2",
        "character_bright_prob_formula": "(1+s*cos(2*pi*k*18/128))/2",
        "relative_route_sign": "s=+1 when the chosen route signs are matched. Opposite relative sign swaps outputs.",
        "arm_tag_left_readable_bright_probability": "1/2",
        "required_controls": "Coherent two-path splitter, deterministic turn/hold routing and final recombination "
        "or postselection with its actual yield. Uncompute every auxiliary route tag before the recombiner.",
    }
    return {
        "model": "H coin (minus only from L to L), shift x by outgoing direction, add the departure x "
        "to a sheet initially localized at 0. Start base (0,R) or (0,L). Integer amplitude "
        "numerator divided by sqrt(2^n). No intermediate read, discard, filter or Fourier preparation.",
        "base_ring_order": BASE_ORDER,
        "sheet_ring_order": SHEET_ORDER,
        "speed_in_comparison": 1,
        "extent": "The line coordinates inject into the two rings up to every saved horizon. Define g(x) "
        "by the centred base representative on the ring. The largest |sheet position| is n(n-1)/2. "
        "The ring is large enough for the optimal circular support and transport fits to use "
        "the displayed line distances. From the origin the bounded control moves by at most one.",
        "port_columns": [
            "endpoint_x",
            "direction",
            "total_squared_numerator",
            "minimum_excluded_squared_numerator",
            "minimum_distance_weighted_numerator",
            "left_end_of_one_TV_arc",
            "left_end_of_one_W1_arc",
            "ordered_two_launch_same_port_distance_over_2n_numerator",
        ],
        "encoding": "Direct R launch rows. The L launch was propagated independently at every horizon. "
        "Its row at (-x,-c) has the same numerical mass and cost. Reflect the full arc "
        "[s,s+2n] to [-s-2n,-s] for a valid optimum. All mass and cost numerators use the "
        "tick denominator stated in each row. Ordered independent pair numerators use its square.",
        "two_launch_event": "Two independent complete launches start from the same localized preparation "
        "with the same direction and initial sheet. Read (x,c,y) at tick n. Count ordered pairs "
        "whose terminal (x,c) agree and whose circular sheet distance exceeds 2n. The event has zero "
        "probability on any fixed common endpoint frame obeying the speed-one cone, even if the hidden "
        "frame is randomly chosen once for both launches. A separately randomized frame per launch is "
        "a different physical setting. Both unconditional and same-port event masses use denominator "
        "4^n. Native probabilities multiply because these are two independently initialized runs.",
        "target_marginal_relaxation": "Every terminal (x,c) may choose its own translated arc of 2n+1 sheet "
        "coordinates: one definite common frame per port, independently of hidden route or random "
        "frame label. TV distance to all such laws is the sum over ports of the minimum excluded "
        "mass. Any outside mass forces that much mismatch; moving it inside each optimal arc "
        "attains equality, even keeping the base-port marginal. This is a relaxation of any "
        "actual unit-speed microscopic dynamics from one localized physical sheet.",
        "W1_definition": "When coupling only identical base ports with their native marginals, measure "
        "cyclic distance in clock cells. Nearest-site transport into the best arc gives the "
        "exact sum of the minimum mean distances. This is not transport permitting free disposal "
        "or arbitrary changes of the base port or a direct prediction for sheet-blind records.",
        "checks": {
            "independent_both_start_signed_trees": HORIZON,
            "independently_listed_all_words_through": 13,
            "exhaustive_all_integer_arc_positions_through": 10,
            "speed_one_control_g_sign_x_all_tail_and_cost_zero_through": 16,
            "first_positive_horizon": 7,
            "seven_tick_1R_area_and_signed_counts": witness,
            "seven_tick_unconditional_TV": "1/16",
            "seven_tick_unconditional_fixed_base_fibre_W1": "1/8",
            "seven_tick_1R_port_probability": "1/8",
            "seven_tick_1R_conditional_TV": "1/8",
            "seven_tick_1R_conditional_W1": "1/4",
            "seven_tick_two_independent_launches_event_probability": "5/4096",
            "seven_tick_pairs_nonzero_port_x_direction_numerator_over_16384": seven_pairs,
        },
        "all_horizon_positive_control": "At n, take R^p L^q R and L^q R^p R, with p=floor(n/2), "
        "q=floor((n-1)/2). For final base (p-q+1,R), their prefix is a rearrangement of p positive "
        "and q negative steps. Exchanging adjacent LR to RL raises total area by exactly two. "
        "The two unique extremes are separated by 2pq, have squared mass 2^-n each for both starts, "
        "and cannot cancel. If pq>vn and the ring does not fold this separation, no radius-vn "
        "arc contains both. Thus full joint TV>=2^-n; fibrewise W1>=2^-n(2pq-2vn). For v=1 this "
        "holds at every n>=7 with sufficient ring size. These lower bounds decay; finite data "
        "alone do not give a positive limiting defect. No convergence of area/n is assumed.",
        "optional_controlled_interferometer": two_paths,
        "rows": saved,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    result = main()
    args.directory.mkdir(parents=True, exist_ok=True)
    (args.directory / "holonomy_cone.json").write_text(
        json.dumps(result, separators=(",", ":")) + "\n", encoding="utf8"
    )
    print(
        "Verified both launches through",
        HORIZON,
        "ticks. Final optimized TV =",
        result["rows"][-1]["minimum_TV"],
    )
