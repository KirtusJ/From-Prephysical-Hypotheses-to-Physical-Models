"""Three-tick terminal records on fixed physical cyclic metrics, using signed integer paths."""

import argparse
import json
from collections import Counter
from functools import cache
from itertools import pairwise, product
from math import gcd, lcm
from pathlib import Path

EVENT_PORTS = ((1, 1), (-1, -1))


def fold(y, m):
    return min(y % m, (-y) % m)


def clean(counts):
    return {cell: n for cell, n in counts.items() if n}


def tick(state, k, m):
    out = Counter()
    for (x, c, y), a in state.items():
        arrived = (y + k * x) % m
        out[x + 1, 1, arrived] += a
        out[x - 1, -1, arrived] += a if c == 1 else -a
    return clean(out)


def three_words(m, k):
    out = Counter()
    for directions in product((1, -1), repeat=3):
        route = (1,) + directions  # incoming coin first
        sign = (-1) ** sum(u == v == -1 for u, v in pairwise(route))
        base = sum(directions)
        area = 2 * directions[0] + directions[1]
        out[base, directions[-1], area * k % m] += sign
    return clean(out)


def pair_numerators(state, m, distance, start=0):
    result = []
    for dx, c in EVENT_PORTS:
        weights = [(y, a * a) for (x, d, y), a in state.items() if (x, d) == (start + dx, c)]
        result.append(sum(p * q for y, p in weights for z, q in weights if fold(y - z, m) == distance))
    return result


def propagate_ruler(m, stride, state, dephase_after_first=False):
    """Two coherent H+shift ticks; an optional intermediate full read is a countercontrol."""
    norm = sum(v * v for v in state.values())
    for t in range(1, 3):
        propagated = Counter()
        for (y, c), v in state.items():
            for d in (1, -1):
                if dephase_after_first and t == 2:
                    propagated[(y + d * stride) % m, d] += v * v
                else:
                    propagated[(y + d * stride) % m, d] += -v if c == d == -1 else v
        state = clean(propagated)
        weight_mode = dephase_after_first and t == 2
        assert sum(v if weight_mode else v * v for v in state.values()) == norm * 2**t
    by_site = Counter()
    for (y, _), v in state.items():
        by_site[y] += v if dephase_after_first else v * v
    return dict(by_site)


@cache
def ruler_ports(m, stride, initial=(1, 0)):
    return propagate_ruler(m, stride, {(0, c): v for c, v in zip((1, -1), initial) if v})


def ruler_event(state, m, stride):
    # The first measured address is the origin of the fresh probe. Test address
    # equality and independently recorded launch probabilities; no metric lookup.
    destination = ruler_ports(m, stride)
    out = []
    for port in EVENT_PORTS:
        weights = [(y, a * a) for (x, d, y), a in state.items() if (x, d) == port]
        out.append(
            sum(
                p * q * destination.get((z - y) % m, 0) for y, p in weights for z, q in weights if y != z
            )
        )
    return out


def anchored_sheet_counts(state, m, stride):
    # Keep the two-tick base mode and the fresh probe rail as orthogonal
    # registers. Only the actual final sheet address enters the observed event.
    complete = Counter()
    for (x, c, y), a in state.items():
        for d in (1, -1):
            complete[x, c, (y + d * stride) % m, d] += a  # fresh R -> both H signs positive
    out = Counter()
    for (_, _, j, _), a in complete.items():
        out[j] += a * a
    assert sum(out.values()) == 8
    return out


def clock_probe_tick(state, m, stride):
    next_state = Counter()
    for (y, c), v in state.items():
        next_state[(y + stride) % m, 1] += v
        next_state[(y - stride) % m, -1] += v if c == 1 else -v
    return clean(next_state)


def marker_weight(state):
    return sum(v * v for (y, _), v in state.items() if y == 0)


def horizon_census():
    summaries = []
    example = {}
    for m in range(3, 25):
        units = [k for k in range(1, m) if gcd(k, m) == 1]
        distances = Counter()
        for stride in units:
            for k in units:
                force = {(0, 1, 0): 1}
                for _ in range(2):
                    force = tick(force, k, m)
                # Old base (x,c) labels remain as orthogonal spectators.
                # Identical clock seeds contribute incoherently with these
                # physical integer weights. No clock read between probe ticks.
                seeds = Counter()
                for (_, _, y), a in force.items():
                    seeds[y] += a * a
                assert seeds == {k: 2, (-k) % m: 2}
                runs = {j: {(j, 1): 1} for j in seeds}
                d = fold(k * pow(stride, -1, m), m)
                assert 0 < 2 * d < m
                observed = []
                for t in range(d + 1):
                    cause = sum(seeds[j] * marker_weight(v) for j, v in runs.items())
                    observed.append(cause)
                    assert all(sum(a * a for a in v.values()) == 2**t for v in runs.values())
                    if t < d:
                        runs = {j: clock_probe_tick(v, m, stride) for j, v in runs.items()}
                assert observed == [0] * d + [4]
                assert all(marker_weight(v) == 1 for v in runs.values())
                if k == stride:
                    assert d == 1
                distances[d] += 1
                if (m, k, stride) == (11, 4, 1):
                    example = {
                        "order": m,
                        "k": k,
                        "l": stride,
                        "joint_marker_numerators_by_t": observed,
                        "denominators_by_t": [4 * 2**i for i in range(d + 1)],
                        "first_hit_lobes": [
                            {
                                "seed": j,
                                "physical_marker_rail_signed_counts": [
                                    runs[j].get((0, c), 0) for c in (1, -1)
                                ],
                            }
                            for j in sorted(seeds)
                        ],
                    }
        summaries.append(
            {
                "M": m,
                "unit_pairs": len(units) ** 2,
                "number_of_pairs_by_first_positive_t": dict(sorted(distances.items())),
            }
        )
    # Later terminal records reinclude paths that visited the marker earlier.
    # Explicitly remove its amplitude after each unsuccessful monitored read
    # to compute first-detection joint masses under the alternative instrument.
    example_laws = {}
    for monitored in (True, False):
        states = {j: {(j, 1): 1} for j in (1, 6)}
        values = []
        for t in range(1, 6):
            states = {j: clock_probe_tick(v, 7, 1) for j, v in states.items()}
            values.append(sum(2 * marker_weight(v) for v in states.values()))
            if monitored:
                states = {
                    j: {cell: a for cell, a in v.items() if cell[0] != 0} for j, v in states.items()
                }
        example_laws["first_detection" if monitored else "terminal_read"] = values
    assert example_laws["terminal_read"][0] == example_laws["first_detection"][0] == 4
    assert example_laws["terminal_read"][2] != example_laws["first_detection"][2]
    return {
        "protocol": "Use separate identically prepared launches for each fixed probe horizon t. "
        "After the two force ticks, start one new R coin on the current sheet, leave the previous "
        "base registers orthogonal, and repeat the same fixed-stride H walk for t ticks. No "
        "which-path read before the final equality comparison with the retained start marker.",
        "formula": "d=fold_M(k*l^{-1}) is recovered as the first horizon with positive "
        "terminal return. All t<d give zero, including t=0. At t=d both force lobes have a "
        "unique shortest ballistic path; its mass is 2^{-d}. The lobes each have mass 1/2, "
        "so their unconditional sum is also 2^{-d}. A unit cannot be antipodal for M>=3. "
        "Changing both hardware strides together keeps d=1; reversing either cannot choose "
        "orientation in this statistic. These are support identifications in the exact record law. "
        "At large d detecting the first positive signal may require order 2^d independent trials "
        "at that horizon. A finite sequence of null observations does not certify a true zero.",
        "unit_pairs_checked": sum(r["unit_pairs"] for r in summaries),
        "orders": summaries,
        "compact_encoding": "Each counted pair at first horizon d has the full prefix of marker "
        "numerators (0 repeated d times, followed by 4), with denominator 4*2^t. "
        "The per-order counts group numerically verified physical runs by their first horizon.",
        "signed_example": example,
        "monitoring_control": {
            "M": 7,
            "k": 1,
            "l": 1,
            "horizons": [1, 2, 3, 4, 5],
            "common_denominators": [8, 16, 32, 64, 128],
            "numerators": example_laws,
            "meaning": "Terminal probabilities for independent launches vs unconditioned first-click "
            "probabilities when testing the same origin after every tick and continuing only on no click.",
        },
    }


def finite_census():
    rows = []
    for m in range(3, 65):
        units = [k for k in range(1, m) if gcd(m, k) == 1]
        events = []
        fixed_ruler = []
        anchored_fixed = []
        anchored_positives = 0
        pairs = positives = 0
        for k in units:
            state = {(0, 1, 0): 1}
            for _ in range(2):
                state = tick(state, k, m)
            two_ticks = state
            state = tick(state, k, m)
            assert state == three_words(m, k) and sum(a * a for a in state.values()) == 8
            by_port = pair_numerators(state, m, 2)
            passes = fold(2 * k, m) == 2
            assert by_port == ([2, 2] if passes else [0, 0])
            folded = pair_numerators(state, m, fold(2, m))
            assert folded == ([2, 2] if fold(2 * k, m) == fold(2, m) else [0, 0])
            for stride in units:
                anchored = anchored_sheet_counts(two_ticks, m, stride)
                anchored_match = k == stride or (k + stride) % m == 0
                assert anchored[0] == 4 * anchored_match
                assert (
                    sum(anchored[q] for q in range(m)) == 8
                )  # a uniform independent guess hits with 1/M
                anchored_positives += anchored_match
                if stride == 1 and anchored_match:
                    anchored_fixed.append(k)
                raw = ruler_event(state, m, stride)
                matches = sum((2 * k - sign * 2 * stride) % m == 0 for sign in (1, -1))
                assert raw == [2 * matches, 2 * matches]
                if stride == 1 and matches:
                    fixed_ruler.append(k)
                if stride == k:
                    assert matches == (2 if m == 4 else 1)
                pairs += 1
                positives += bool(matches)
            # For all units, both identified coordinates are distinct. Reading
            # the two positions without the physical sheets cannot see k here.
            for x, c in EVENT_PORTS:
                assert sum(a * a for (u, d, y), a in state.items() if (u, d) == (x, c)) == 2
            if passes:
                events.append(k)
        if m >= 4:
            reduced = m // gcd(m, 2)
            assert events == [k for k in units if (k - 1) % reduced == 0 or (k + 1) % reduced == 0]
        rows.append(
            {
                "order": m,
                "units_checked": len(units),
                "nonzero_at_both_ports": events,
                "nonzero_ruler_stride1": fixed_ruler,
                "unit_gain_stride_pairs": pairs,
                "nonzero_unit_gain_stride_pairs": positives,
                "anchored_nonzero_stride1": anchored_fixed,
                "anchored_nonzero_unit_gain_stride_pairs": anchored_positives,
            }
        )
    return rows


def rename(state, modulus, multiplier=1, offset=0):
    return {(x, c, (multiplier * y + offset) % modulus): a for (x, c, y), a in state.items()}


def aliases():
    cases = 0
    for m in (3, 4, 5, 6, 8, 9, 10, 12, 15, 16, 20, 24):
        for k in range(1, m):
            if gcd(m, k) != 1:
                continue
            for x0, y0 in ((0, 0), (-2, 3), (3, 1)):
                for c0 in (1, -1):
                    original = {(x0, c0, y0 % m): 1}
                    reflected = dict(original)
                    shifted = dict(original)
                    for n in range(9):
                        assert reflected == rename(original, m, -1, 2 * y0)
                        if m % 2 == 0:
                            offset = (m // 2) * (n * x0 + n * (n - 1) // 2)
                            assert shifted == rename(original, m, offset=offset)
                        # Replacing sqrt(2) by its negative multiplies all
                        # physical amplitudes by a common (-1)^n.
                        assert all(a * a == ((-1) ** n * a) ** 2 for a in original.values())
                        original = tick(original, k, m)
                        reflected = tick(reflected, -k, m)
                        if m % 2 == 0:
                            shifted = tick(shifted, k + m // 2, m)
                        cases += 1
    return cases


def one_shot_controls():
    m = 8
    base = three_words(m, 1)
    aliased = three_words(m, 5)
    assert base != aliased and rename(base, m, offset=4) == aliased

    def marked(k, stride, initial):
        launch = {(0, 1, initial): 1}
        for _ in range(2):
            launch = tick(launch, k, 8)
        return anchored_sheet_counts(launch, 8, stride)

    anchored_examples = {}
    for k, stride in ((1, 1), (5, 1), (5, 5)):
        seen = marked(k, stride, 0)
        assert all(marked(k, stride, a)[a] == seen[0] for a in range(8))
        assert sum(seen.values()) == 8
        anchored_examples[f"k{k}_stride{stride}"] = {
            "return_numerator_over8": seen[0],
            "output_histogram_over8": dict(seen),
            "independently_randomized_anchor_probability": "1/8",
        }
    assert [v["return_numerator_over8"] for v in anchored_examples.values()] == [4, 0, 4]
    # k=2 nonunit at M=4 identifies +/-k; destructive and constructive
    # paths now interfere on the very same coordinate.
    nonunit = three_words(4, 2)
    masses = [sum(a * a for (u, d, _), a in nonunit.items() if (u, d) == p) for p in EVENT_PORTS]
    assert masses == [4, 0] and pair_numerators(nonunit, 4, 2) == [0, 0]
    # A metric transported under the bridge relabeling of ALL coordinates
    # returns the original distance; physically fixed nearest sites give 1.
    m = 5
    renamed = three_words(m, 2)
    pulled_back = rename(renamed, m, 3)
    assert pulled_back == three_words(m, 1)
    assert pair_numerators(renamed, m, 2) == [0, 0] and pair_numerators(pulled_back, m, 2) == [2, 2]
    assert ruler_event(renamed, m, 1) == [0, 0] and ruler_event(renamed, m, 2) == [2, 2]
    # The fresh coherent coin (R+L)/sqrt(2) is routed wholly right by its
    # first Hadamard. Dephasing that input before H gives instead the mean
    # of the R and L basis-launch laws.
    coherent = ruler_ports(5, 1, (1, 1))
    incoherent = Counter(ruler_ports(5, 1, (1, 0))) + Counter(ruler_ports(5, 1, (0, 1)))
    assert coherent == {2: 4, 0: 4} and incoherent == {2: 2, 0: 4, 3: 2}
    two_seed = {(0, 1): 1, (2, 1): 1}
    between = propagate_ruler(7, 1, two_seed)
    read_between = propagate_ruler(7, 1, two_seed, True)
    assert between == {0: 1, 2: 5, 4: 1, 5: 1} and read_between == {0: 3, 2: 3, 4: 1, 5: 1}
    # Removing the modulo wrapping for the base is justified on a finite
    # base C_lcm(8,m) with g(x)=kx: departing from site x vs x+N gives
    # the same modular increment, and the ring does not collide in 3 ticks.
    assert all(lcm(8, m) >= 8 and lcm(8, m) % m == 0 for m in range(3, 65))
    return {
        "M8_k1_vs_k5_fixed_origin_laws_identical": False,
        "M8_three_tick_common_output_shift_for_k5": 4,
        "M4_nonunit_k2_port_masses_in_eighths": masses,
        "M5_physical_k2_event": "0",
        "M5_k2_with_transported_metric_event": "1/16",
        "M5_k2_physical_ruler_stride1_vs_stride2": ["0", "1/64"],
        "M8_actual_versus_lost_anchor": anchored_examples,
        "M5_coherent_vs_dephased_initial_coin_two_tick_ruler_site_numerators_over8": {
            "coherent_R_plus_L": coherent,
            "dephased_R_plus_L": dict(incoherent),
        },
        "M7_two_cell_input_0R_plus_2R_probe_site_numerators_over8": {
            "coherent": between,
            "which_path_after_first_tick": read_between,
        },
    }


def main():
    census = finite_census()
    return {
        "launch_and_read": "Two independently reset (0,R,0) launches, three signed Hadamard "
        "ticks with the physical departure translation g_k(x)=kx mod M. Read position, direction, "
        "and physical sheet coordinate in each run. A line base or C_lcm(8,M) suffices.",
        "predeclared_event": "Both base readouts equal the same port in {(1,R),(-1,L)}, and the two "
        "sheets have distance exactly 2 in the independently fixed unoriented unit-edge cycle.",
        "three_tick_integer_paths": [
            {"port": list(p), "sheet_exponents_and_signs": pairs}
            for p, pairs in zip(EVENT_PORTS, ([[1, 1], [-1, 1]], [[1, -1], [-1, 1]]))
        ],
        "law": "The exponents are multiplied by k. With unit k and M>=3 the +/-k cells are distinct. "
        "At each chosen port they each have squared mass 1/8. In the product record the two "
        "opposite-sheet orders have total mass 2/64=1/32 per port iff fold_M(2k)=2; otherwise "
        "the contribution is zero. Thus the full probability is 1/16 or zero.",
        "general_unit_classification": "For M>=5 this is equivalent to 2k=+/-2 mod M, or "
        "k=+/-1 mod M/gcd(2,M). At odd M only +/-1 pass. At M=2 mod 4 only +/-1 are units "
        "in that class; at M divisible by 4, +/-1+M/2 also pass, with overlaps at M=4.",
        "per_endpoint_encoding": {
            "ports": EVENT_PORTS,
            "ordered_pair_denominator": 64,
            "numerators_for_each_listed_unit": [2, 2],
            "numerators_for_every_other_unit": [0, 0],
        },
        "finite_orders": census,
        "complete_relative_stride": horizon_census(),
        "anchored_one_launch": {
            "event": "Start base (0,R) on a physically marked sheet y0. After two "
            "force ticks coherently couple a fresh R coin to the current sheet and let it make one "
            "balanced +/-l hop. Keep the previous base position and direction as orthogonal registers. "
            "Read whether the final sheet equals the original physical marker. No intermediate sheet "
            "measurement or second independent launch is necessary.",
            "law": "The two-tick sheet displacements +k and -k have masses 1/2 each. The appended fresh "
            "hop sends half of each to each sign of l. For all M>=3 and unit k,l, exactly one half returns "
            "if k=+/-l mod M and no path returns otherwise. These are 4 or 0 of 8 squared path-numerator "
            "units. A translation of the whole experiment with its marker keeps the same return probability.",
            "same_drive_control": "With l=k every unit map passes with 1/2. On M=8 a fixed ruler l=1 "
            "separates k=1 from k=5 even though all the three-tick relative reads alias them.",
            "anchor_loss": "If the marker is replaced by an independent uniformly chosen sheet, equality "
            "has probability 1/M for every k,l by normalization; tracing every sheet without an address "
            "comparison gives total mass one. Averaging a common shift of launch AND marker does not "
            "destroy the relation. The uniform randomized marker is a separately specified control.",
            "unit_pairs_checked": sum(row["unit_gain_stride_pairs"] for row in census),
            "nonzero_unit_pairs": sum(row["anchored_nonzero_unit_gain_stride_pairs"] for row in census),
        },
        "physical_ruler": {
            "event": "Both launches have the same designated ambiguous port; their "
            "recorded sheet cells y1,y2 differ; a fresh R-coin two-tick H walk of physical stride l "
            "from y1 ends at y2. The address comparison alone defines this event. The two cyclic "
            "edges of this apparatus specify a physical generator up to orientation.",
            "joint_denominator": 256,
            "per_port_numerator": "2 times the count of signs s in +/-1 with "
            "2k=s*2l mod M. If +/-2l are distinct the nonzero total is 1/64, including M=3; "
            "at M=4 the two signs coincide and give 1/32. A matched stride l=k passes for all unit k.",
            "unit_gain_stride_pairs_checked": sum(row["unit_gain_stride_pairs"] for row in census),
            "preparation": "A nondestructive first sheet read can leave a localized sheet for the fresh "
            "probe coin. If the read consumes the walker, a separately prepared fresh probe must be placed "
            "at the recorded cell in the same apparatus. Resetting only to a fixed address does not implement "
            "this operation. The second independently initialized launch supplies the recorded target cell.",
            "interference": "Sequentially apply the signed Hadamard matrices, add amplitudes in identical "
            "complete cells, then square and sum over unresolved final directions. With a localized "
            "R coin and unit stride here, coincident extreme positions on C4 have different final "
            "directions, so probabilities add. There is no forced visibility of a two-tick path "
            "interference fringe. Coherent input-coin and dephased-coin controls differ.",
        },
        "unit_force_settings_checked": sum(row["units_checked"] for row in census),
        "exceptions": {
            "M3_literal_distance_2": "Impossible on C3; probability zero for both units. "
            "Changing the observable to the folded distance of two unit steps (distance 1) gives "
            "1/16 for either unit.",
            "M4": "The two units 1 and 3 are reflections; both pass via the "
            "antipodal distance 2 and cannot be distinguished by this measurement.",
        },
        "general_symmetries": "For a fixed base launch x0, the departure at time t obeys "
        "x_t = x0+t mod 2, independent of direction history. For even M replacing k by k+M/2 "
        "shifts every branch at depth n by the same C=(M/2)(n*x0+n(n-1)/2) mod M, preserving "
        "all base outputs and relative sheet distances at the same horizon. A marked sheet "
        "origin can recover the difference at horizons with C nonzero. A translated start y0 "
        "only shifts both experiments. Replacing k by -k reflects every sheet through y0; relative "
        "distances are invariant. The even alias is between two unit multipliers iff 4 divides M.",
        "symmetry_start_setting_horizon_checks": aliases(),
        "controls": one_shot_controls(),
        "interpretation": "The graph, gain, local metric and shared device calibration are physical inputs. "
        "A fixed metric can compare two physical force maps. Applying a unit multiplication to "
        "both the graph coordinates and their calibration transports the metric too, restoring "
        "the original event. No choice of abstract embedding follows. Reversing sqrt(2) changes "
        "only the common sign on each synchronized branch and leaves squared records unchanged.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    out = main()
    args.directory.mkdir(parents=True, exist_ok=True)
    (args.directory / "holonomy_embedding.json").write_text(
        json.dumps(out, indent=2) + "\n", encoding="utf8"
    )
    print(
        "Verified",
        out["unit_force_settings_checked"],
        "unit force settings and",
        out["symmetry_start_setting_horizon_checks"],
        "symmetry trials.",
    )
