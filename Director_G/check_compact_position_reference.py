"""Join a signed flight, a strict-threshold reference, and two protected-bin transfers."""

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

from check_compact_bin_reflections import circuit_reflect, flight, odd_gcd, transport
from check_prefix_reference import prefix


def require(condition, message):
    if not condition:
        raise ValueError(message)


def walk_panel(ticks, predicate, dilute=False):
    source = {cell: n for cell, n in flight(ticks).items() if n}
    base = 1 << ticks
    marked_mass = sum(n*n for cell, n in source.items() if predicate(*cell))
    require(sum(n*n for n in source.values()) == base, "flight norm")
    bins = [[], []]
    for cell, n in sorted(source.items()):
        target = bool(predicate(*cell))
        marks = (True, False, target, target) if dilute else (target,)
        for mark in marks:
            bins[int(mark)].append(n)
    depth = ticks + 2 if dilute else ticks
    denom = 1 << depth
    numerator = sum(n*n for n in bins[1])
    require(numerator == (base + 2*marked_mass if dilute else marked_mass), "helper mass")
    if numerator in (0, denom):
        endpoint = [1 << (depth//2)] * (1 + depth % 2)
        leaves = {"positive_integer_numerators": endpoint, "marked": [bool(numerator)] * len(endpoint),
                  "width": len(endpoint)}
    else:
        leaves = prefix(depth, numerator)
    rows = {}
    for side, flight_row in enumerate(bins):
        target = [n for n, mark in zip(leaves["positive_integer_numerators"], leaves["marked"])
                  if int(mark) == side]
        if not flight_row:
            require(not target, "empty bin has occupied reference leaves")
            rows[str(side)] = {"source_modes": 0, "leaf_modes": 0, "padded_modes": 0}
            continue
        receipt = transport(flight_row, target, digit_padding=True)
        if "obstruction" in receipt:
            rows[str(side)] = {"odd_content": odd_gcd(flight_row), "obstruction": receipt["obstruction"]}
            continue
        require(receipt["target"] == target and receipt["norm2"] == sum(v*v for v in target),
                "wrong block transfer")
        rows[str(side)] = {
            "source_modes": len(flight_row), "leaf_modes": len(target), "odd_content": odd_gcd(flight_row),
            "squared_numerator": receipt["norm2"], "padded_modes": receipt["padded_width"],
            "addressed_gates_per_reflection": receipt["gates_per_reflection"],
            "transfer_receipt_sha256": hashlib.sha256(json.dumps(
                receipt, sort_keys=True, separators=(",", ":")).encode("ascii")).hexdigest(),
        }
        if "normal_reducers" in receipt:
            # Replay the bin in its padded physical addresses and readdress each output
            # to the corresponding prefix leaf, keeping the flag value on every column.
            width = receipt["padded_width"]
            state = flight_row + [0] * (width - len(flight_row))
            for gates in receipt["normal_reducers"]:
                state = circuit_reflect(state, gates)
            leaf_ids = [i for i, mark in enumerate(leaves["marked"]) if int(mark) == side]
            addressed = {(leaf, side): state[len(flight_row)+j] for j, leaf in enumerate(leaf_ids)}
            expected = {(leaf, side): leaves["positive_integer_numerators"][leaf] for leaf in leaf_ids}
            require(addressed == expected and sum(v*v for v in state) == sum(v*v for v in addressed.values()),
                    "complete readdressed flagged column mismatch")
            rows[str(side)]["readdressed_flag_components"] = len(addressed)
    return dict(ticks=ticks, four_color_helper=dilute, flight_modes=len(source),
                original_mass=str(Fraction(marked_mass, base)),
                compared_mass=str(Fraction(numerator, denom)), prefix_depth=depth,
                unit_reference_modes=denom, prefix_leaf_modes=leaves["width"], blocks=rows)


def diagonal_ensemble(t, threshold):
    """Compare whole kets grouped by first difference; the two parity twins stay coherent."""
    record = prefix(t, threshold)
    nums = record["positive_integer_numerators"]
    labels = [label.removesuffix(" twin") for label in record["parked_labels"]]
    paths = [int(label.split()[-1]) - 1 if label != "equal" else t for label in labels]
    phases = 1 << t.bit_length()
    retained_cross_terms = 0
    for i, (x, j) in enumerate(zip(nums, paths)):
        for k, (y, l) in enumerate(zip(nums, paths)):
            cross_sum = sum((-1)**((a & (j ^ l)).bit_count()) for a in range(phases))
            actual = Fraction(x*y*cross_sum, (1 << t)*phases)
            component = Fraction(x*y, 1 << t) if j == l else Fraction(0)
            require(actual == component, "dephasing or sharp path ensemble mismatch")
            if i != k and actual:
                retained_cross_terms += 1
    return dict(depth=t, labels=t+1, phases=phases, checked_ordered_pairs=len(nums)**2,
                ordered_coherent_twin_terms=retained_cross_terms)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    panels = {}
    for ticks in (3, 8, 16, 24, 32):
        name = f"nonnegative_site_at_{ticks}"
        result = walk_panel(ticks, lambda x, r: x >= 0)
        require(all("obstruction" not in b for b in result["blocks"].values()), name)
        panels[name] = result
    for dilute in (False, True):
        name = "rail_with_helper" if dilute else "rail_alone"
        result = walk_panel(4, lambda x, r: (x, r) == (2, 0), dilute)
        require(("obstruction" in result["blocks"]["1"]) != dilute, name)
        panels[name] = result
    for depth, mark in [(3, False), (3, True), (4, True)]:
        panel = walk_panel(depth, lambda x, r: mark)
        require(panel["blocks"][str(int(not mark))]["padded_modes"] == 0 and
                panel["prefix_leaf_modes"] == 1 + depth % 2, "deterministic endpoint normalization")
        panels[f"sharp_{int(mark)}_at_{depth}"] = panel
    p = Fraction(panels["nonnegative_site_at_3"]["compared_mass"])
    pooled_square = p*p/(p*p+(1-p)**2)
    require(pooled_square - p == Fraction(3, 20), "nonlinear ensemble response")
    output = dict(panels=panels, phase_controls=[diagonal_ensemble(4, 9), diagonal_ensemble(16, 28871)],
                  three_tick_rates={"signed_pure_prefix": str(pooled_square), "sharp_assigned": str(p),
                                    "pooled_square_mismatch": str(pooled_square-p)},
                  gate_convention="Count the named Walsh, sign, swap and simultaneous pair-H layers in each bin. The two orthogonal bin banks and their final readdressing are separate costs.")
    with args.output.open("x", encoding="utf8", newline="\n") as stream:
        json.dump(output, stream, indent=2)
        stream.write("\n")


if __name__ == "__main__":
    main()
