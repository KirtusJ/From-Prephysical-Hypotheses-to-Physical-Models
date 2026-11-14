"""Exact signed-walk flattening and carrier exchange. Run with an output JSON path."""

import argparse
import json
from collections import Counter, defaultdict
from fractions import Fraction
from functools import reduce
from itertools import product
from math import gcd
from pathlib import Path


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def walk(ticks):
    """Integer path numerators on the line, coin H then stream; common norm 2^ticks."""
    state = {(0, "R"): 1}
    for _ in range(ticks):
        output = defaultdict(int)
        for (x, rail), value in state.items():
            output[x + 1, "R"] += value
            output[x - 1, "L"] += value if rail == "R" else -value
        state = {site: value for site, value in output.items() if value}
    require(sum(value**2 for value in state.values()) == 2**ticks, "walk norm")
    return dict(sorted(state.items()))


def odd_content(values):
    g = reduce(gcd, values, 0)
    while g and g % 2 == 0:
        g //= 2
    return g


def fourth(values):
    return sum(value**4 for value in values)


def walsh(values):
    """Two real Hadamards on one addressed four-mode block; each is self-inverse."""
    numerators = [
        sum((-1)**((i & j).bit_count()) * x for j, x in enumerate(values))
        for i in range(4)
    ]
    require(all(v % 2 == 0 for v in numerators), "nonintegral four-mode result")
    return [v // 2 for v in numerators]


def pack_sector(indexed):
    """Work on the carrier alone. indexed gives carrier addresses and signed inputs."""
    values = dict(indexed)
    capacity = sum(x*x for x in values.values())  # enough blank modes for this sector
    free = iter(range(len(values), capacity))
    content = odd_content(values.values())
    trace = []
    for i in list(values):
        if values[i] < 0:
            values[i] = -values[i]
            trace.append(["phase -1", i])
    while values:
        evens = [i for i, x in values.items() if x % 2 == 0]
        if evens:
            addresses = [evens[0]] + [next(free) for _ in range(3)]
        else:
            maximum = max(values, key=values.get)
            minimum = min(values, key=values.get)
            if values[maximum] == values[minimum]:
                break
            addresses = [maximum, minimum, next(free), next(free)]
        before = [values.get(i, 0) for i in addresses]
        after = walsh(before)
        require(walsh(after) == before, "inverse Walsh")
        require(sum(x*x for x in after) == sum(x*x for x in before), "block norm")
        require(all(x > 0 for x in after), "occupied leaf")
        require(fourth(before) > fourth(after), "integer descent")
        values.update(zip(addresses, after))
        trace.append(["Walsh", addresses, before, after])
    require(set(values.values()) <= {content}, "odd content at termination")
    require(sum(x*x for x in values.values()) == capacity, "sector norm")
    return values, trace


def analyse(ticks, mask):
    state = walk(ticks)
    magnitudes = sorted(set(map(abs, state.values())))
    sectors = []
    for inside in (True, False):
        cells = [(x, c, v) for (x, c), v in state.items() if (x in mask) == inside]
        inputs = [v for x, c, v in cells]
        leaves, trace = pack_sector(enumerate(inputs))
        sectors.append(dict(marked=inside, input_cells=cells, norm_numerator=sum(v*v for v in inputs),
                            odd_gcd=odd_content(inputs), leaves=len(leaves), operations=trace))
    return dict(ticks=ticks, mask=sorted(mask), denominator_squared=2**ticks,
                magnitudes=magnitudes, cannot_split_alone=[v for v in magnitudes if odd_content([v]) != 1],
                sectors=sectors)


def route_three(panel, reference_arm):
    """Propagate both three-tick arms from physical carrier addresses through passive F."""
    bank = [(x, c, a) for x in range(-8, 8) for c in ("R", "L") for a in range(4)]
    columns = {}
    for (x, c), value in walk(3).items():
        for k in range(8):
            # Uniform K was prepared before this write. Every following operation
            # is blockwise identical on F, including the controlled two-H split.
            flag = int(k < 5) if reference_arm else int(x in panel["mask"])
            columns[(x, c, 0), k, flag] = value  # common denominator 8
    injection = {}
    for sector in panel["sectors"]:
        carrier = {i:(x, c, 0) for i, (x, c, _) in enumerate(sector["input_cells"])}
        for operation in sector["operations"]:
            if operation[0] == "phase -1":
                cell = carrier[operation[1]]
                for key in list(columns):
                    if key[0] == cell:
                        columns[key] *= -1
            else:
                _, logical, _, _ = operation
                x, c, a = carrier[logical[0]]
                require(len(logical) == 4 and a == 0 and (x,c) == (1,"R"), "conditional H site")
                for bit_value, address in enumerate(logical):
                    carrier[address] = (x, c, bit_value)
                block = [carrier[i] for i in logical]
                for k, flag in product(range(8), range(2)):
                    before = [columns.pop((cell, k, flag), 0) for cell in block]
                    for cell, value in zip(block, walsh(before)):
                        if value:
                            columns[cell, k, flag] = value
        for i, cell in sorted(carrier.items()):
            injection[cell] = len(injection)
    # Complete the requested injection of eight physical occupied sites to the
    # full 128-address carrier. Encode its output index as (junk=index//8, J=index%8).
    unused = [cell for cell in bank if cell not in injection]
    routing = {**injection, **{cell:j for j,cell in enumerate(unused, start=len(injection))}}
    require(len(bank) == len(routing) == len(set(routing.values())) == 128, "carrier permutation")
    require(all(routing[cell] < 8 for cell, _, _ in columns), "clean junk")
    routed = {(routing[cell], k, flag, 0): value for (cell,k,flag), value in columns.items()}
    paths = [[x,c,a,j] for (x,c,a), j in injection.items()]
    return routed, paths


def fully_routed(panel):
    """Make a clean 3-bit data register J after splitting. K is an independent label."""
    groups = panel["sectors"]
    require(all(s["odd_gcd"] == 1 for s in groups), "exact unit leaves required")
    marked_count = groups[0]["leaves"]
    size = 2**panel["ticks"]
    require(sum(s["leaves"] for s in groups) == size, "full carrier")
    # Positive unit leaves are ordered by sector then local address. An injection
    # of these occupied carrier addresses to J, clearing old wires, extends to a
    # permutation of the padded carrier. The experimental apparatus must provide it.
    def arm(reference, *, tag=False, phase=False, uneven=False):
        out = {}
        for j, k in product(range(size), repeat=2):
            flag = int((k if reference else j) < marked_count)
            val = (-1 if phase and j == 0 else 1) * (2 if uneven and j == 0 else 1)
            out[j, k, flag, j if tag else 0] = val
        return out

    direct_route, direct_paths = route_three(panel, False)
    reference_route, reference_paths = route_three(panel, True)
    require(direct_paths == reference_paths, "common physical routing")
    require(direct_route == arm(False) and reference_route == arm(True), "propagated J,K,F columns")

    def swap(state):
        # Only J,K change. No write, conditional phase, read or operation acts on F.
        return {(k, j, f, tag): val for (j, k, f, tag), val in state.items()}

    def compare(**options):
        original = arm(False, **options)
        left = swap(original)
        right = arm(True, **options)
        keys = left.keys() | right.keys()
        norm = sum(x*x for x in original.values())
        mismatch = sum((left.get(key, 0)-right.get(key, 0))**2 for key in keys)
        return dict(states_equal=left == right, squared_difference=str(Fraction(mismatch, norm)))

    tagged = compare(tag=True)
    phased = compare(phase=True)
    unequal = compare(uneven=True)
    ideal = compare()
    require(ideal["states_equal"] and not any(x["states_equal"] for x in [tagged, phased, unequal]),
            "full-carrier exchange and breakers")
    # Rotating only J after a target write gives the same vector as prewriting a
    # translated predicate. Counting assumes a common actual J on diagnostic arms.
    translated = []
    for t in range(size):
        left = {((j+t) % size, int(j < marked_count)): 1 for j in range(size)}
        right = {(j, int((j-t) % size < marked_count)): 1 for j in range(size)}
        require(left == right, "post-write translation")
        translated.append([j for j in range(size) if (j-t) % size < marked_count])
    require(all(sum(j in row for row in translated) == marked_count for j in range(size)),
            "balanced mask incidence")
    p = Fraction(marked_count, size)
    r = 3*p/(1+2*p)
    return dict(labels=size, marks=marked_count, physical_leaf_to_J_x_rail_scratch_J=direct_paths,
                full_routing_permutation_size=128, common_positive_pair_entries=size*size,
                atom_amplitude="1/"+str(size), direct_mass=str(p), exact=ideal,
                retained_old_J_tag=tagged, uncompensated_J_phase=phased, unequal_J_amplitudes=unequal,
                translated_mask_cells=translated, weighted_target_rate=str(r),
                weighted_reference_rate=str(p), weighted_failure_gap=str(r-p))


def noisy_rail():
    """Tick four's numerator-three port, with actually computed four scratch labels."""
    state = walk(4)
    counts = []
    bank = [(x, rail, label) for x in range(-8, 8) for rail in ("R","L") for label in range(4)]
    def noisy_bit(cell):
        x, rail, label = cell
        return label == 0 or (label >= 2 and (x,rail) == (2,"R"))
    data_a, data_b = {}, {}
    offset = 0
    for flag in (True, False):
        nodes = [cell for cell in bank if noisy_bit(cell) == flag]
        occupied = [cell for cell in nodes if cell[:2] in state]
        blank = [cell for cell in nodes if cell[:2] not in state]
        # Positions, rails and helper colors are all physical. Available blank
        # cells stay in the same helper-defined sector during every Walsh.
        addresses = occupied + blank
        sector = [state[cell[:2]] for cell in occupied]
        leaves, trace = pack_sector(enumerate(sector))
        norm = sum(value**2 for value in sector)
        require(len(leaves) == norm, "all diluted-flag leaves are units")
        require(len(addresses) >= norm, "enough sector-specific routed addresses")
        for z in range(64):
            for flag_value in (False,True):
                values = sector + [0] * len(blank)
                if flag_value == flag:
                    direct = values.copy()
                else:
                    direct = [0] * len(values)
                if flag_value == (z < 34):
                    reference = values.copy()
                else:
                    reference = [0] * len(values)
                for column in (direct, reference):
                    for op, *args in trace:
                        if op == "phase -1":
                            column[args[0]] *= -1
                        else:
                            block = args[0]
                            output = walsh([column[i] for i in block])
                            for i, value in zip(block, output):
                                column[i] = value
                # Sorting the occupied carrier to consecutive J labels cleans the
                # old position/coin/helper. Both arms use the identical permutation.
                for i in range(len(values)):
                    j = offset+i
                    if direct[i]: data_a[j,z,flag_value] = direct[i]
                    if reference[i]: data_b[j,z,flag_value] = reference[i]
        counts.append(dict(flag=flag, norm_numerator=norm, available_physical_cells=len(nodes),
                           odd_gcd=odd_content(sector),
                           Walsh_blocks=sum(op[0] == "Walsh" for op in trace)))
        offset += norm
    require(offset == 64 and sum(c["available_physical_cells"] for c in counts) == 128,
            "bijection extends over all unused addresses")
    target_swapped = {(z,j,f):v for (j,z,f),v in data_a.items()}
    require(target_swapped == data_b and len(data_b) == 64**2 and set(data_b.values()) == {1},
            "physical four-color and reference columns coincide with F untouched")
    p = Fraction(9,16)
    r = 3*p/(1+2*p)
    calibrated = Fraction(counts[0]["norm_numerator"],64)
    require(calibrated == Fraction(1,4)+p/2, "direct diluted selected-port geometry")
    weighted = Fraction(1,4) + r/2
    # Validate the sharp finite-error combination on both error orientations.
    # R_C=q+err_cal and R_C=R_mix+err_cmp. The honest-copy branch rate may
    # differ from the original by err_copy. Dummy-sharp and dummy-dark errors
    # have opposite signs in the pair of endpoints.
    sharp_tol, dark_tol, cal_tol, cmp_tol, copy_tol = map(Fraction, ("1/16","1/32","1/64","1/128","1/64"))
    worst = Fraction(0)
    bound = 2*(cal_tol+cmp_tol) + max(sharp_tol,dark_tol)/2 + copy_tol
    for bad_sharp, dark, ec, em, eb in product(
            (0,sharp_tol), (0,dark_tol), (-cal_tol,cal_tol), (-cmp_tol,cmp_tol), (-copy_tol,copy_tol)):
        sharp = 1-bad_sharp
        measured_c = calibrated + ec
        mixture = measured_c - em
        unknown_b = 2*(mixture-(sharp+dark)/4) - eb
        require(0 <= unknown_b <= 1, "admissible finite-rate witness")
        worst = max(worst, abs(unknown_b-p))
    require(worst == bound, "attained endpoint and comparison transfer bound")
    # An unresolved masked record yields an interval on original launches.
    # These illustrative totals are supplied inputs, not experimental data.
    incident, hits, unresolved = 128, 66, 3
    loss_interval = [Fraction(hits,incident),Fraction(hits+unresolved,incident)]
    require(loss_interval[0] <= calibrated <= loss_interval[1], "full-data original-launch interval")
    return dict(physical_target_port=[2,"R"], direct_probability=str(p),
                flag_rule=["always on","always off","copy target","copy target"],
                squared_denominator=64, sectors=counts, exchange_reference_mass=str(calibrated),
                exchange={"positive_entries":len(data_b),"atom_amplitude":"1/64","full_column_equal":True},
                weighted_undiluted_rate=str(r), weighted_diluted_rate=str(weighted),
                discrepancy=str(weighted-calibrated),
                transfer_error=dict(sharp=str(sharp_tol),dark=str(dark_tol),reference=str(cal_tol),
                                    comparison=str(cmp_tol),copy=str(copy_tol),attained_bound=str(bound)),
                illustrative_original_launches=dict(incident=incident,hits=hits,unresolved=unresolved,
                                                    event_rate_interval=list(map(str,loss_interval))))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    three = analyse(3, {1})
    require(walk(3) == {(-3,"L"):1, (-1,"R"):-1, (1,"L"):1, (1,"R"):2, (3,"R"):1},
            "three-tick amplitude signs")
    result = dict(three_tick=three, full_exchange=fully_routed(three))
    clocks = [analyse(t, {t-2}) for t in range(4,9)]
    clocks.append(analyse(5, {-5,3,5}))
    require(all(s["odd_gcd"] == 1 for panel in clocks for s in panel["sectors"]), "marked examples")
    result["later_clocks"] = [{**{k:v for k,v in panel.items() if k != "sectors"},
                               "sectors":[{**{k:v for k,v in s.items() if k != "operations"},
                                           "walsh_counts":dict(Counter(op[0] for op in s["operations"]))}
                                          for s in panel["sectors"]]} for panel in clocks]
    # A measured/protected rail can isolate the tick-four numerator 3. Its odd
    # divisor survives every signed Walsh in that protected sector.
    four = walk(4)
    port = next(i for i, v in four.items() if abs(v) == 3)
    blocked, _ = pack_sector([(0, four[port])])
    result["protected_single_port_breaker"] = dict(ticks=4, port=port, numerator=four[port],
                                                   terminal_magnitudes=list(blocked.values()))
    result["randomized_response_for_the_blocked_port"] = noisy_rail()
    args.output.write_bytes((json.dumps(result, indent=2) + "\n").encode("utf-8"))


if __name__ == "__main__":
    main()
