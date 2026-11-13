"""Check complementary returning paths with pulse routing and selective native H.

Run python -B check_return_loop_control.py results. The area and complete
signed histories use integers. Angles are recorded in exact turns.
"""

import argparse
import json
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import pairwise, product
from math import cos, gcd, isqrt, pi, sin
from pathlib import Path

from check_loop_coin_flight import routed_step


def path_area(word):
    x = A = 0
    for d in word:
        A += x
        x += d
    assert x == 0
    return A


def min_a(d):
    """First nonempty bridge starting R and ending L with area d."""
    a = max(1, isqrt(abs(d)))
    while a * a < abs(d) or (a - d) % 2 or d < a * a - 2 * (a - 1) ** 2:
        a += 1
    return a


def synthesize(d):
    a = min_a(d)
    length = a - 1
    inversions = (a * a - d) // 2
    if length:
        full, partial = divmod(inversions, length)
        # Each early L passes all length R's. One partial L passes the
        # requested number of remaining R's. The end pulses stay fixed.
        middle = [-1] * full + [1] * (length - partial)
        if partial:
            middle.extend([-1] + [1] * partial)
        middle.extend([-1] * (length - full - bool(partial)))
    else:
        middle = []
    word = (1, *middle, -1)
    assert len(word) == 2 * a and path_area(word) == d
    gates = "I" + "".join("I" if u == v else "X" for u, v in pairwise(word))
    return a, word, gates


def nearest_integer(num, den):
    q, r = divmod(num, den)
    if 2 * r == den:
        return [q, q + 1]
    return [q + int(2 * r > den)]


def angle_error(m, d):
    error = (F(2 * d, m) - F(1, 4)) % 1
    return min(error, 1 - error)


def best_circular(m):
    # A reachable positive representative bounds a. Scan every earlier
    # half-length and every physically attainable area; this proves actual
    # minimality even when a different signed representative wraps around.
    period = m // gcd(m, 2)
    lowest = least_circle_error(m)
    classes = [r for r in range(period) if angle_error(m, r) == lowest]
    out = []
    for r in classes:
        stop = min_a(r)
        for a in range(1, stop + 1):
            hits = [d for d in range(a * a - 2 * (a - 1) ** 2, a * a + 1, 2) if d % period == r]
            if hits:
                out.append(
                    {
                        "residue": r,
                        "period": period,
                        "signed_areas_at_first_nonempty_length": hits,
                        "minimum_nonempty_a": a,
                        "scan_ceiling_a": stop,
                        "angular_error_turns": str(lowest),
                    }
                )
                break
        else:
            raise AssertionError("The explicit unwrapped representative was not attained")
    return out


def least_circle_error(m):
    # Possible phases form the grid {j/K}, K=M/gcd(M,2).
    period = m // gcd(m, 2)
    return min(abs(F(j, period) - F(1, 4)) for j in nearest_integer(period, 4))


def literal(state, gates, m):
    out = state
    for g in gates:
        out = routed_step(out, g, m)
    return out


def closed_map(initial, m, a, d, active):
    out = Counter()
    for (x, c, y), v in initial.items():
        for first in (1, -1) if active else (c,):
            s = -1 if active and first == c == -1 else 1
            out[x, -first, (y + 2 * a * x + first * d) % m] += s * v
    return {k: v for k, v in out.items() if v}


def program_row(m, d, initial):
    a, word, gates = synthesize(d)
    row = {
        "d": d,
        "minimum_nonempty_half_length": a,
        "word_R_arm": "".join("R" if j == 1 else "L" for j in word),
        "passive_gate_word": gates,
        "phase_turns": str(F(2 * d, m) % 1),
        "quarter_error_turns": str(angle_error(m, d)),
    }
    for active in (True, False):
        schedule = ("H" + gates[1:]) if active else gates
        out = literal(initial, schedule, m)
        assert out == closed_map(initial, m, a, d, active)
        assert sum(v * v for v in out.values()) == (1 + active) * sum(v * v for v in initial.values())
    if m in (3, 5, 8, 13, 32):
        row["active_complete_output"] = [
            [*k, v] for k, v in sorted(closed_map(initial, m, a, d, True).items())
        ]
        row["passive_complete_output"] = [
            [*k, v] for k, v in sorted(closed_map(initial, m, a, d, False).items())
        ]
    return row


def brute_bridges():
    rows = []
    for a in range(1, 7):
        possible = {
            path_area(w)
            for mid in product((1, -1), repeat=2 * a - 2)
            if sum(mid) == 0
            for w in [(1, *mid, -1)]
        }
        assert possible == set(range(a * a - 2 * (a - 1) ** 2, a * a + 1, 2))
        any_return = {path_area(w) for w in product((1, -1), repeat=2 * a) if sum(w) == 0}
        assert min(any_return) == -a * a and max(any_return) == a * a
        rows.append([a, min(possible), max(possible), len(possible)])
    assert all(path_area(synthesize(d)[1]) == d for d in range(-112, 113))
    return rows


def doubled_comparison(m, d, e):
    # One H split. The second loop is passive, with no second splitting H.
    # A boundary X is a local permutation (no stream) deliberately accounted
    # for here; it reverses the relative sign of the passive accumulation.
    a, _, g = synthesize(d)
    b, _, h = synthesize(e)
    state = literal({(0, 1, 0): 1}, "H" + g[1:], m)
    rows = []
    for boundary_swap in (False, True):
        intermediate = {(x, -c if boundary_swap else c, y): v for (x, c, y), v in state.items()}
        composed = literal(intermediate, h, m)
        assert composed == closed_map(intermediate, m, b, e, False)
        # Final balanced read followed by streaming; the R output is recorded.
        final = literal(composed, "H", m)
        poly = [final.get((1, 1, y), 0) for y in range(m)]
        degree = d + e if boundary_swap else d - e
        target = [1 * (i == (degree % m)) + 1 * (i == (-degree % m)) for i in range(m)]
        assert poly == target
        assert sum(v * v for v in state.values()) == 2
        detailed = []
        for tag in (-1, 1):
            # An orthogonal record of the first arm. No coherent addition
            # between tags: square the two port amplitudes separately.
            tagged = {key: v for key, v in intermediate.items() if key[1] == tag}
            outputs = literal(literal(tagged, h, m), "H", m)
            detailed.append([outputs.get((1, 1, j), 0) for j in range(m)])
        assert [sum(v * v for v in arm) for arm in detailed] == [1, 1]
        assert [sum(x) for x in zip(*detailed)] == poly
        bright = [
            abs(
                sum(
                    v * complex(cos(2 * pi * k * y / m), sin(2 * pi * k * y / m))
                    for y, v in enumerate(poly)
                )
            )
            ** 2
            / 4
            for k in range(m)
        ]
        for k, p in enumerate(bright):
            assert abs(p - (1 + cos(4 * pi * k * degree / m)) / 2) < 1e-12
        rows.append(
            {
                "extra_boundary_X_no_stream": boundary_swap,
                "exact_bright_sheet_counts": poly,
                "bright_probabilities_by_k": bright,
                "incoherent_arms_bright_all_k": "1/2",
            }
        )
    return {
        "M": m,
        "calibrated_d": d,
        "passive_reference_e": e,
        "strict_streamed_ticks_including_read": 2 * a + 2 * b + 1,
        "comparisons": rows,
    }


def selector_tick(state, m, counting):
    """Ordinary H force walk; the predicate is applied only after streaming."""
    out = Counter()
    for (x, c, y, b), v in state.items():
        for r in (1, -1):
            sign = -1 if not counting and c == r == -1 else 1
            out[x + r, r, (y + x) % m, b] += sign * v
    return {key: v for key, v in out.items() if v}


def signed_norm(state):
    return sum(v * v for v in state.values())


def character_norm(state, m, k):
    base = defaultdict(complex)
    for (x, c, y, b), v in state.items():
        angle = -2 * pi * k * y / m
        base[x, c, b] += v * complex(cos(angle), sin(angle))
    return sum(abs(z) ** 2 for z in base.values())


def report_history_census():
    """Check unrestricted words, including the opposite-sign and nonreturn controls."""
    rows = []
    for n in range(1, 9):
        candidates = list(product((1, -1), repeat=n))
        equal_sign = opposite_sign = returned = 0
        for tail in product((1, -1), repeat=n - 1):
            word = (1, *tail)
            live = []
            first_failed = Counter()
            for path in candidates:
                first_bit = int(path[0] == -1)
                reports = tuple(c == target * path[0] for c, target in zip(path[1:], word[1:]))
                if False in reports:
                    first_failed[2 + reports.index(False)] += 1
                    continue
                erased_bit = first_bit ^ int(path[-1] != word[-1])
                sign = (-1) ** sum(c == r == -1 for c, r in pairwise((1, *path)))
                assert erased_bit == 0
                live.append((path, sign))
            assert {p for p, s in live} == {word, tuple(-j for j in word)}
            assert all(first_failed[t] == 2 ** (n - t + 1) for t in range(2, n + 1))
            assert len(live) + sum(first_failed.values()) == 2**n
            relative = live[0][1] * live[1][1]
            assert relative == (-1) ** sum(c == r for c, r in pairwise(word))
            equal_sign += int(relative == 1)
            opposite_sign += int(relative == -1)
            returned += int(sum(word) == 0)
        rows.append(
            {
                "ticks": n,
                "R_start_masks": 2 ** (n - 1),
                "returning": returned,
                "equal_signed_pair": equal_sign,
                "opposite_signed_pair": opposite_sign,
                "joint_success": str(F(2, 2**n)),
            }
        )
    return rows


def word_select(word, m, initial, save_output):
    assert word[0] == 1 and word[-1] == -1 and len(word) % 2 == 0 and sum(word) == 0
    assert all(c == 1 for x, c, y in initial)
    n = len(word)
    a = n // 2
    d = path_area(word)
    common_sign = (-1) ** sum(u == v == -1 for u, v in pairwise(word))
    assert common_sign == (-1) ** sum(u == v == 1 for u, v in pairwise(word))
    start = {(x, c, y, 0): v for (x, c, y), v in initial.items()}
    initial_power = signed_norm(start)
    denoms = [character_norm(start, m, k) for k in range(m)]
    for counting in (False, True):
        # The count control uses a nonnegative incoherent source with the
        # same coordinate diagonal; pure character checks below use the
        # actual signed source and its separately normalized Fourier slice.
        src = {p: v * v if counting else v for p, v in start.items()}
        split = selector_tick(src, m, counting)
        live = {(x, c, y, b ^ int(c == -1)): v for (x, c, y, b), v in split.items()}
        assert {key[-1] for key in live} == {0, 1}
        bins = []
        for t, target in enumerate(word[1:], 2):
            arrived = selector_tick(live, m, counting)
            matches = {}
            fails = {}
            for (x, c, y, b), v in arrived.items():
                first = 1 - 2 * b
                # Same yes/no report for both successful arms. Site, current
                # direction, and the private first-rail bit remain unreported.
                outcome = matches if c == target * first else fails
                outcome[x, c, y, b] = v
            norm = sum(fails.values()) if counting else signed_norm(fails)
            p = F(norm, initial_power * 2**t)
            assert p == F(1, 2 ** (t - 1))
            if not counting:
                for k, source_norm in enumerate(denoms):
                    assert abs(character_norm(fails, m, k) - 2 * source_norm) < 1e-10
            bins.append(str(p))
            live = matches
        success = F(sum(live.values()) if counting else signed_norm(live), initial_power * 2**n)
        assert success == F(1, 2 ** (n - 1)) and sum(map(F, bins), success) == 1
        if counting:
            read_counts = selector_tick(live, m, True)
            bright_count = sum(v for (x, c, y, b), v in read_counts.items() if c == 1)
            assert 2 * bright_count == sum(read_counts.values())
            continue
        erased = {(x, c, y, b ^ int(c == 1)): v for (x, c, y, b), v in live.items()}
        assert all(b == 0 for x, c, y, b in erased)
        expected = closed_map(initial, m, a, d, True)
        assert {(x, c, y): v for (x, c, y, b), v in erased.items()} == {
            p: common_sign * v for p, v in expected.items()
        }
        for k, source_norm in enumerate(denoms):
            assert abs(character_norm(erased, m, k) - 2 * source_norm) < 1e-10
        if save_output:
            saved_coordinates = [[*p, v] for p, v in sorted(erased.items())]
        # Recombiner consumes another genuine H tick, including its x gain.
        readouts = {}
        sheet_unresolved = {}
        for tag, state in (("erased", erased), ("retained", live)):
            final = selector_tick(state, m, False)
            bright = {p: v for p, v in final.items() if p[1] == 1}
            sheet_unresolved[tag] = str(F(signed_norm(bright), signed_norm(final)))
            probabilities = []
            for k, source_norm in enumerate(denoms):
                if source_norm < 1e-12:
                    probabilities.append(None)
                    continue
                p = character_norm(bright, m, k) / (4 * source_norm)
                expected_p = (1 + cos(4 * pi * k * d / m)) / 2 if tag == "erased" else 0.5
                assert abs(p - expected_p) < 1e-10
                probabilities.append(p)
            readouts[tag] = probabilities
    result = {
        "M": m,
        "reference_word": list(word),
        "other_word": [-j for j in word],
        "d": d,
        "common_internal_H_sign": common_sign,
        "first_failed_report_at_ticks_2_to_n": bins,
        "joint_success_all_components": str(success),
        "conditional_bright_after_extra_H_by_k": readouts,
        "conditional_bright_summed_over_physical_sheet": sheet_unresolved,
        "count_bright_given_success": "1/2",
    }
    if save_output:
        result["unnormalized_success_after_bit_erasure_x_rail_sheet_bit_coefficient"] = saved_coordinates
    return result


def selector_trials():
    out = []
    inputs = {
        "localized": {(0, 1, 0): 1},
        "signed_packet": {(-2, 1, 0): 2, (0, 1, 1): -3, (0, 1, 4): 1, (2, 1, 6): -1},
    }
    for name, initial in inputs.items():
        for a in range(1, 5):
            for middle in product((1, -1), repeat=2 * a - 2):
                if sum(middle) != 0:
                    continue
                word = (1, *middle, -1)
                r = word_select(word, 8, initial, a <= 2)
                r["source"] = name
                out.append(r)
    witness = next(
        row for row in out if row["source"] == "localized" and row["reference_word"] == [1, -1, 1, -1]
    )
    assert witness["joint_success_all_components"] == "1/8"
    assert witness["first_failed_report_at_ticks_2_to_n"] == ["1/2", "1/4", "1/8"]
    fringe = witness["conditional_bright_after_extra_H_by_k"]
    assert abs(fringe["erased"][1]) < 1e-12 and abs(fringe["retained"][1] - 0.5) < 1e-12
    return out


def main():
    brute = brute_bridges()
    orders = []
    for m in range(3, 257):
        raw = {(-3, 1, 3): 2, (0, 1, 1): -3, (4, 1, 0): 1, (0, -1, 1): 2, (4, -1, 1): -1}
        initial = {(x, c, y % m): v for (x, c, y), v in raw.items()}
        ds = nearest_integer(m, 8)
        schedules = [program_row(m, d, initial) for d in ds]
        circle = best_circular(m)
        assert all((r["angular_error_turns"] == "0") == (m % 8 == 0) for r in circle)
        if min(ds) >= 9:
            for d in ds:
                assert min_a(d) <= isqrt(d - 1) + 2
        orders.append({"M": m, "unwrapped_nearest_choices": schedules, "modular_optima": circle})
    controls = [doubled_comparison(8, 1, 1), doubled_comparison(16, 2, 1), doubled_comparison(13, 1, 0)]
    return {
        "construction": "Ordinary T^M=I, departure g=x, line (no base wraps). Global pulses use H "
        "at the first tick for a splitter or I for passive transport. All later pulses are I or X "
        "according to changes in the R-start word. Its complementary path is then automatic, even "
        "on overlapping broad packets. No arm-label read or arbitrary unsigned sheet increment.",
        "closed_map": "For either first direction s=+/-1, final site equals its initial x, final rail "
        "is -s, and sheet gains 2a*x+s*d. Active split includes 1/sqrt(2) and a minus only for "
        "incoming L with s=L. Passive input follows its existing rail with no split. Complete signed "
        "integer maps for mixed sites, mixed signs and both rails are checked against literal ticks.",
        "sharp_time": "Every returning n=2a path satisfies |x_t-x0|<=min(t,2a-t). Hence its centred "
        "area is between -a² and +a²; opposite extremal paths saturate relative diameter 2a². "
        "For h=2*pi/M approaching a quadrature modulo 2*pi with relative error o(1) requires "
        "n >= (1-o(1))*sqrt(M/2) on this fixed physical stride. In pulse family starting R and "
        "ending L, freezing the two endpoints leaves a-1 of each middle step. Their inversion "
        "counts cover 0..(a-1)^2, changing area by 2. Allowed areas are exactly "
        "a²-2(a-1)^2,a²-2(a-1)^2+2,...,a². Nonempty minimal lengths are checked separately for "
        "positive, zero and negative d. A zero-area target admits zero passive duration, or an "
        "onsite H splitter if such a gate without streaming is supplied; this is different from "
        "a nonempty R-to-L routed return.",
        "precision": "Terminal rail ratio L/R=exp(-i*2d*h) on an R launch, removing the common "
        "phase including the x-dependent momentum kick. Unwrapped nearest d to M/8 gives angular "
        "error <=2*pi/M, in O(sqrt(M)) streaming time with O(1) parity overhead. Table reports "
        "positive target +1/4 for theta=2d*h in turns; the ratio has its negative. Modular phases "
        "form the order M/gcd(M,2) subgroup; exact quarter iff 8 divides M. Odd-cycle wrapping "
        "can give a better phase than the fastest unwrapped construction; the separate modular "
        "table does not identify its global angular optimum with the short unwrapped latency.",
        "latency_scope": "This lower bound concerns phase differences of two fixed equal-time returning "
        "physical histories, not arbitrary filtering, pre-existing superpositions or complex controls. "
        "Changing to predetermined real X/I steering after a split is a supplied apparatus. Arbitrary "
        "complex phase gates would supply the phase being generated. The common momentum kick has "
        "magnitude 2a|h| and must be included in a packet flight; this checker does not simulate it.",
        "brute_bridge_columns": ["a", "min_R_to_L_area", "max_R_to_L_area", "number_distinct"],
        "brute_bridge_results": brute,
        "orders": orders,
        "passive_composition_controls": controls,
        "native_H_relative_direction_word_controls": selector_trials(),
        "arbitrary_relative_direction_report_census": report_history_census(),
        "selective_instrument": "Use unmodified H each stream tick. Copy the first split direction "
        "coherently into a blank bit; after subsequent ticks project only on the predicate "
        "current rail = prescribed direction times private first rail. Every successful report "
        "is shared by both complementary words. Retain all failed branches separately. Since "
        "the success word ends opposite to its first rail, bit XOR controlled by final R returns "
        "the bit to blank. For an initial R the two H products have the same sign: the number "
        "of turns is odd and the number of equal successive directions among 2a-1 transitions "
        "is even. Distinct output rails make the success effect 2^(1-2a) on that initial rail. "
        "Tests include all R-start L-end zero-displacement words through eight ticks and extended "
        "signed initial data. Accepted spinors match real pulse routing after common amplitude "
        "normalization. Native H is unchanged, but the coherent first-rail copy, relative "
        "predicate projectors, bit erasure and synchronized report/control are still required. "
        "At a of order sqrt(M) the postselection cost can be exponential, even if 2a streamed "
        "flight ticks are short. Dark phase-sensitive recombiner requires no surviving arm label. "
        "For arbitrary relative-direction masks the same count and bit erasure hold; the two H "
        "products acquire relative sign (-1)^(number of equal consecutive directions). "
        "Recombination of a localized launch at one base site requires a returning pair.",
        "detector_scope": "Final H reads a cosine and cannot resolve orientation on its own. Difference "
        "of the bright probabilities of the d-e and d+e loop settings equals sin(2dh)sin(2eh). "
        "All route tags, if present, must be coherently erased. A permanent orthogonal record "
        "of the two arms instead gives 1/2 under both H readouts. Absolute conjugation leaves "
        "all real-device records unchanged.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    data = main()
    args.directory.mkdir(parents=True, exist_ok=True)
    (args.directory / "return_loop_control.json").write_text(
        json.dumps(data, separators=(",", ":")) + "\n", encoding="utf8"
    )
    print(
        "Verified",
        len(data["orders"]),
        "clock orders and",
        len(data["passive_composition_controls"]),
        "two-loop read checks.",
    )
